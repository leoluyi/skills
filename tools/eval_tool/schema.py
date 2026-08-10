"""Small, shared eval schema used by the unified eval CLI."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple


class EvalError(Exception):
    pass


class Row(NamedTuple):
    case_id: int
    slug: str
    detail: str
    critical: bool


def slug_of(expectation: str) -> str:
    return expectation.split(":", 1)[0].strip()


def detail_of(expectation: str) -> str:
    head, sep, tail = expectation.partition(":")
    return tail.strip() if sep else head.strip()


def resolve_ids(spec: str, known: set[int]) -> tuple[int, ...]:
    selected: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            left, right = token.split("-", 1)
            try:
                lo, hi = int(left), int(right)
            except ValueError as exc:
                raise EvalError(f"bad --ids range: {token!r}") from exc
            if lo > hi:
                raise EvalError(f"inverted --ids range: {token!r}")
            selected.update(range(lo, hi + 1))
        else:
            try:
                selected.add(int(token))
            except ValueError as exc:
                raise EvalError(f"bad --ids value: {token!r}") from exc
    unknown = sorted(selected - known)
    if unknown:
        raise EvalError(f"--ids names absent case id(s): {unknown}")
    if not selected:
        raise EvalError("--ids selected nothing")
    return tuple(sorted(selected))


def load_cases(skill_dir: Path) -> tuple[dict, ...]:
    path = skill_dir / "evals" / "evals.json"
    if not path.exists():
        raise EvalError(f"missing {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvalError(f"cannot read {path}: {exc}") from exc
    cases = raw.get("evals") if isinstance(raw, dict) else None
    if not isinstance(cases, list) or not cases:
        raise EvalError(f"{path}: expected non-empty 'evals' list")
    seen: set[int] = set()
    out = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise EvalError(f"{path}: evals[{index}] must be an object")
        required = {"id", "prompt", "expected_output", "expectations"}
        missing = required - set(case)
        if missing:
            raise EvalError(f"{path}: evals[{index}] missing {sorted(missing)}")
        case_id = case["id"]
        if not isinstance(case_id, int) or isinstance(case_id, bool) or case_id in seen:
            raise EvalError(f"{path}: invalid or duplicate case id {case_id!r}")
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            raise EvalError(f"{path}: case {case_id} has empty prompt")
        if not isinstance(case["expected_output"], str):
            raise EvalError(f"{path}: case {case_id} expected_output must be string")
        expectations = case["expectations"]
        if not isinstance(expectations, list) or not expectations:
            raise EvalError(f"{path}: case {case_id} needs non-empty expectations")
        if any(not isinstance(item, str) or not item.strip() for item in expectations):
            raise EvalError(f"{path}: case {case_id} expectations must be non-empty strings")
        slugs = [slug_of(item) for item in expectations]
        if len(slugs) != len(set(slugs)):
            raise EvalError(f"{path}: case {case_id} repeats expectation slug")
        seen.add(case_id)
        out.append(case)
    return tuple(out)


def load_config(skill_dir: Path, cases: tuple[dict, ...]) -> dict:
    """Load the small config, accepting annotation config during migration."""
    path = skill_dir / "evals" / "config.json"
    if path.exists():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise EvalError(f"cannot read {path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise EvalError(f"{path}: top level must be object")
        unknown = set(raw) - {"profile", "quick_ids", "critical_expectations"}
        if unknown:
            raise EvalError(f"{path}: unknown key(s) {sorted(unknown)}")
        profile = raw.get("profile", "standard")
        quick_ids = tuple(raw.get("quick_ids", ()))
        critical = tuple(raw.get("critical_expectations", ()))
    else:
        profile, quick_ids, critical = "standard", (), ()

    known = {case["id"] for case in cases}
    if any(not isinstance(item, int) for item in quick_ids):
        raise EvalError(f"{path}: quick_ids must contain integers")
    missing = sorted(set(quick_ids) - known)
    if missing:
        raise EvalError(f"{path}: quick_ids names absent case id(s): {missing}")
    if not quick_ids:
        quick_ids = tuple(case["id"] for case in cases) if len(cases) <= 6 else ()
    if len(quick_ids) > 6:
        raise EvalError(f"{path}: quick_ids may contain at most 6 ids")
    if profile not in {"standard", "high-risk"}:
        raise EvalError(f"{path}: profile must be standard or high-risk")
    critical_set = set(critical)
    known_selectors = {
        f"{case['id']}/{slug_of(expectation)}"
        for case in cases for expectation in case["expectations"]
    }
    unknown_critical = sorted(critical_set - known_selectors)
    if unknown_critical:
        raise EvalError(f"{path}: critical expectation(s) absent: {unknown_critical}")

    # During migration, infer humanizer's protected rows from its existing
    # declaration. This keeps the old quality boundary intact until config.json
    # is written, while every new skill uses explicit selectors.
    legacy = skill_dir / "evals" / "annotation-config.json"
    legacy_critical: set[str] = set()
    if legacy.exists() and not critical_set:
        try:
            legacy_raw = json.loads(legacy.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise EvalError(f"cannot read {legacy}: {exc}") from exc
        vc = legacy_raw.get("verdict_class", {})
        patterns = [re.compile(p) for p in vc.get("protection_patterns", [])]
        overrides = vc.get("overrides", {})
        for case in cases:
            for expectation in case["expectations"]:
                slug = slug_of(expectation)
                klass = overrides.get(slug)
                if klass == "保護" or (klass is None and any(p.search(slug) for p in patterns)):
                    legacy_critical.add(f"{case['id']}/{slug}")
        critical_set = legacy_critical
        if legacy_raw.get("profile") == "high-risk":
            profile = "high-risk"
    return {"profile": profile, "quick_ids": quick_ids, "critical": critical_set, "path": path}


def rows(cases: tuple[dict, ...], config: dict) -> tuple[Row, ...]:
    critical = config["critical"]
    return tuple(
        Row(case["id"], slug_of(expectation), detail_of(expectation),
            f"{case['id']}/{slug_of(expectation)}" in critical)
        for case in cases
        for expectation in case["expectations"]
    )


def validate_skill(skill_dir: Path) -> dict:
    cases = load_cases(skill_dir)
    config = load_config(skill_dir, cases)
    trigger = skill_dir / "evals" / "trigger-queries.json"
    if trigger.exists():
        try:
            raw = json.loads(trigger.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise EvalError(f"cannot read {trigger}: {exc}") from exc
        queries = raw.get("queries") if isinstance(raw, dict) else None
        if not isinstance(queries, list) or not queries:
            raise EvalError(f"{trigger}: expected non-empty queries list")
        for query in queries:
            if not isinstance(query, dict) or not isinstance(query.get("prompt", query.get("query")), str):
                raise EvalError(f"{trigger}: every query needs prompt/query string")
            expected = query.get("expected_trigger", query.get("should_trigger"))
            if not isinstance(expected, bool):
                raise EvalError(f"{trigger}: every query needs boolean expected_trigger/should_trigger")
    return {"cases": cases, "config": config, "rows": rows(cases, config)}

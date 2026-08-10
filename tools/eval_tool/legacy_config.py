"""Legacy annotation config and fixture layer."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .legacy_errors import (
    CLASSES,
    CONFIG_PATH,
    HIT,
    PROTECTION,
    Chunk,
    ConfigError,
    FixtureError,
    Row,
    ScoreEvalsError,
)
from .schema import EvalError, detail_of, load_cases, slug_of

CONFIG_KEYS = {
    "skill_paths",
    "protocol",
    "rewrite_case_ids",
    "smoke_ids",
    "global_rewrite_checks",
    "unscored_slug_prefixes",
    "chunks",
    "verdict_class",
    "ai_index_not_applicable",
    "baseline_incompatible",
}


def load_config(skill_dir: Path) -> dict | None:
    """Return the validated config, or None when the skill has not opted in."""
    path = skill_dir / CONFIG_PATH
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"{path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"{path}: top level must be an object")
    unknown = set(raw) - CONFIG_KEYS
    if unknown:
        raise ConfigError(f"{path}: unknown key(s) {sorted(unknown)}")
    return {
        "skill_paths": _str_list(path, raw, "skill_paths", required=True),
        "protocol": _protocol(path, raw.get("protocol")),
        "rewrite_case_ids": _unique_int_list(path, raw, "rewrite_case_ids"),
        "smoke_ids": _unique_int_list(path, raw, "smoke_ids"),
        "global_rewrite_checks": _global_checks(path, raw.get("global_rewrite_checks")),
        "unscored_slug_prefixes": _str_list(path, raw, "unscored_slug_prefixes"),
        "chunks": _chunk_pairs(path, raw.get("chunks")),
        "verdict_class": _verdict_class(path, raw.get("verdict_class")),
        "ai_index_not_applicable": _id_reason_map(
            path, raw.get("ai_index_not_applicable", {}), "ai_index_not_applicable"
        ),
        "baseline_incompatible": _incompatible(path, raw.get("baseline_incompatible", [])),
        "path": path,
    }


def _str_list(path: Path, raw: dict, key: str, required: bool = False) -> tuple[str, ...]:
    value = raw.get(key, [])
    if required and not value:
        raise ConfigError(f"{path}: '{key}' is required and must be a non-empty list")
    if not isinstance(value, list) or any(not isinstance(v, str) or not v for v in value):
        raise ConfigError(f"{path}: '{key}' must be a list of non-empty strings")
    return tuple(value)


def _int_list(path: Path, raw: dict, key: str) -> tuple[int, ...]:
    value = raw.get(key, [])
    if not isinstance(value, list) or any(
        not isinstance(v, int) or isinstance(v, bool) for v in value
    ):
        raise ConfigError(f"{path}: '{key}' must be a list of integers")
    return tuple(value)


def _unique_int_list(path: Path, raw: dict, key: str) -> tuple[int, ...]:
    """Reject duplicates: rows dedupe by id but the report's arithmetic counts
    the declared list, so a repeated id prints a sum that does not add up.
    """
    value = _int_list(path, raw, key)
    seen: set[int] = set()
    repeated: set[int] = set()
    for item in value:
        if item in seen:
            repeated.add(item)
        seen.add(item)
    if repeated:
        raise ConfigError(f"{path}: '{key}' repeats id(s) {sorted(repeated)}")
    return value


def _protocol(path: Path, value: object) -> dict:
    if not isinstance(value, dict):
        raise ConfigError(f"{path}: 'protocol' must be an object")
    for key in ("file", "criteria_section"):
        if not isinstance(value.get(key), str) or not value[key]:
            raise ConfigError(f"{path}: 'protocol.{key}' is required and must be a string")
    unknown = set(value) - {"file", "criteria_section"}
    if unknown:
        raise ConfigError(f"{path}: unknown key(s) in 'protocol': {sorted(unknown)}")
    return {"file": value["file"], "criteria_section": value["criteria_section"]}


def _global_checks(path: Path, value: object) -> dict:
    if not isinstance(value, dict) or not value:
        raise ConfigError(f"{path}: 'global_rewrite_checks' must be a non-empty object")
    for name, klass in value.items():
        if klass not in CLASSES:
            raise ConfigError(
                f"{path}: global_rewrite_checks[{name!r}] is {klass!r}, "
                f"want one of {list(CLASSES)}"
            )
    return dict(value)


def _chunk_pairs(path: Path, value: object) -> tuple[tuple, ...]:
    """Parse chunk declarations: [lo, hi] ranges or {"ids": [...]} explicit sets.

    The explicit form exists because contiguous ranges cannot mix verdict
    classes when the fixture's ids arrived direction-partitioned (all-hit runs
    of ids next to all-protection runs): a chunk that only holds protection
    cases hands a degenerate flag-nothing runner a perfect score. An id set
    interleaves both directions without renumbering cases — renumbering would
    orphan every verdict in evals/annotations.json, which is keyed by case id.
    """
    if not isinstance(value, list) or not value:
        raise ConfigError(
            f"{path}: 'chunks' must be a non-empty list of [lo, hi] pairs "
            'or {"ids": [...]} objects'
        )
    specs: list[tuple] = []
    for index, item in enumerate(value):
        if isinstance(item, dict):
            unknown = set(item) - {"ids"}
            if unknown:
                raise ConfigError(
                    f"{path}: unknown key(s) in chunks[{index}]: {sorted(unknown)}"
                )
            ids = item.get("ids")
            if (
                not isinstance(ids, list)
                or not ids
                or any(not isinstance(v, int) or isinstance(v, bool) for v in ids)
            ):
                raise ConfigError(
                    f"{path}: chunks[{index}].ids must be a non-empty list of integers"
                )
            specs.append(("ids", tuple(ids)))
            continue
        ok = (
            isinstance(item, list)
            and len(item) == 2
            and all(isinstance(v, int) and not isinstance(v, bool) for v in item)
        )
        if not ok:
            raise ConfigError(
                f"{path}: chunks[{index}] must be a [lo, hi] integer pair "
                f'or an {{"ids": [...]}} object, got {item!r}'
            )
        if item[0] > item[1]:
            raise ConfigError(f"{path}: chunks[{index}] is inverted: {item!r}")
        specs.append(("range", item[0], item[1]))
    return tuple(specs)


def _verdict_class(path: Path, value: object) -> dict:
    if not isinstance(value, dict):
        raise ConfigError(f"{path}: 'verdict_class' must be an object")
    unknown = set(value) - {"protection_patterns", "hit_patterns", "overrides", "no_touch"}
    if unknown:
        raise ConfigError(f"{path}: unknown key(s) in 'verdict_class': {sorted(unknown)}")
    compiled = {}
    for key in ("protection_patterns", "hit_patterns"):
        patterns = value.get(key, [])
        if not isinstance(patterns, list):
            raise ConfigError(f"{path}: 'verdict_class.{key}' must be a list of regexes")
        out = []
        for pattern in patterns:
            if not isinstance(pattern, str) or not pattern:
                raise ConfigError(f"{path}: verdict_class.{key} holds a non-string: {pattern!r}")
            try:
                out.append(re.compile(pattern))
            except re.error as exc:
                raise ConfigError(f"{path}: verdict_class.{key} bad regex {pattern!r} — {exc}") from exc
        compiled[key] = tuple(out)
    overrides = value.get("overrides", {})
    if not isinstance(overrides, dict):
        raise ConfigError(f"{path}: 'verdict_class.overrides' must be an object")
    for slug, klass in overrides.items():
        if klass not in CLASSES:
            raise ConfigError(
                f"{path}: verdict_class.overrides[{slug!r}] is {klass!r}, "
                f"want one of {list(CLASSES)}"
            )
    compiled["overrides"] = dict(overrides)
    compiled["no_touch"] = _id_reason_map(
        path, value.get("no_touch", {}), "verdict_class.no_touch"
    )
    return compiled


def _id_reason_map(path: Path, value: object, label: str) -> dict[int, str]:
    """Parse {"41": "reason"} declarations keyed by case id.

    Keys are JSON strings because JSON objects cannot hold integer keys; the
    parsed map uses ints so lookups match case ids without a cast at every
    call site. Reasons are required: a bare id list would record *that* a case
    is exempt while losing *why*, and the why is the part a later maintainer
    needs before deleting the entry.
    """
    if not isinstance(value, dict):
        raise ConfigError(f"{path}: '{label}' must be an object of id → reason")
    out: dict[int, str] = {}
    for key, reason in value.items():
        if not isinstance(key, str) or not key.isdigit():
            raise ConfigError(f"{path}: {label} key {key!r} must be a case id string")
        if not isinstance(reason, str) or not reason:
            raise ConfigError(f"{path}: {label}[{key!r}] needs a non-empty reason string")
        out[int(key)] = reason
    return out


def _incompatible(path: Path, value: object) -> tuple[dict, ...]:
    if not isinstance(value, list):
        raise ConfigError(f"{path}: 'baseline_incompatible' must be a list")
    entries = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ConfigError(f"{path}: baseline_incompatible[{index}] must be an object")
        unknown = set(item) - {"ids", "reason"}
        if unknown:
            raise ConfigError(
                f"{path}: unknown key(s) in baseline_incompatible[{index}]: {sorted(unknown)}"
            )
        ids = item.get("ids")
        if not isinstance(ids, list) or any(
            not isinstance(v, int) or isinstance(v, bool) for v in ids
        ):
            raise ConfigError(f"{path}: baseline_incompatible[{index}].ids must be integers")
        reason = item.get("reason", "")
        if not isinstance(reason, str):
            raise ConfigError(f"{path}: baseline_incompatible[{index}].reason must be a string")
        entries.append({"ids": tuple(ids), "reason": reason})
    return tuple(entries)


def load_fixture(skill_dir: Path) -> tuple[dict, ...]:
    try:
        return load_cases(skill_dir)
    except EvalError as exc:
        raise FixtureError(str(exc)) from exc


def unscored_notes(cases: tuple[dict, ...], config: dict) -> dict[int, tuple[str, ...]]:
    """Collect the expectations that are not scored but are written for the
    grader — unscored is not the same as unseen; the runner never gets them.
    """
    prefixes = config["unscored_slug_prefixes"]
    return {
        case["id"]: tuple(
            expectation
            for expectation in case["expectations"]
            if any(slug_of(expectation).startswith(prefix) for prefix in prefixes)
        )
        for case in cases
    }


def classify(slug: str, verdict_class: dict) -> str:
    """Decide a slug's class here, never in the grader.

    The ship gate's absolute condition is stated over protection-class rows,
    so the class has to be identical in every chunk and every run; a grader
    re-deriving it per prompt would make the denominator drift.
    """
    override = verdict_class["overrides"].get(slug)
    if override:
        return override
    is_protection = any(p.search(slug) for p in verdict_class["protection_patterns"])
    is_hit = any(p.search(slug) for p in verdict_class["hit_patterns"])
    if is_protection and is_hit:
        raise ConfigError(
            f"expectation slug {slug!r} matches both protection_patterns and "
            "hit_patterns; add a verdict_class.overrides entry"
        )
    if not is_protection and not is_hit:
        raise ConfigError(
            f"expectation slug {slug!r} matches neither protection_patterns nor "
            "hit_patterns; add a pattern or a verdict_class.overrides entry"
        )
    return PROTECTION if is_protection else HIT


def build_rows(cases: tuple[dict, ...], config: dict) -> tuple[Row, ...]:
    """Expand the fixture into scored rows: expectations plus global checks."""
    unscored = config["unscored_slug_prefixes"]
    rewrite_ids = set(config["rewrite_case_ids"])
    rows: list[Row] = []
    for case in cases:
        for expectation in case["expectations"]:
            slug = slug_of(expectation)
            if any(slug.startswith(prefix) for prefix in unscored):
                continue
            rows.append(
                Row(
                    case_id=case["id"],
                    slug=slug,
                    detail=detail_of(expectation),
                    klass=classify(slug, config["verdict_class"]),
                    origin="eval",
                )
            )
        if case["id"] in rewrite_ids:
            for name, klass in config["global_rewrite_checks"].items():
                rows.append(
                    Row(
                        case_id=case["id"],
                        slug=f"全域:{name}",
                        detail=f"rewrite 模式全域檢核：{name}",
                        klass=klass,
                        origin="global",
                    )
                )
    return tuple(rows)


def validate_declared_ids(cases: tuple[dict, ...], config: dict) -> None:
    known = {case["id"] for case in cases}
    missing = [i for i in config["rewrite_case_ids"] if i not in known]
    if missing:
        raise ConfigError(
            f"rewrite_case_ids names id(s) absent from evals.json: {sorted(missing)}"
        )
    missing = [i for i in config["smoke_ids"] if i not in known]
    if missing:
        raise ConfigError(
            f"smoke_ids names id(s) absent from evals.json: {sorted(missing)}"
        )
    for index, entry in enumerate(config["baseline_incompatible"]):
        absent = [i for i in entry["ids"] if i not in known]
        if absent:
            raise ConfigError(
                f"baseline_incompatible[{index}].ids names id(s) absent from "
                f"evals.json: {sorted(absent)}"
            )


def build_chunks(cases: tuple[dict, ...], config: dict) -> tuple[Chunk, ...]:
    """Expand chunk declarations and prove they partition the fixture's ids.

    A range skips ids the fixture never had (gaps are normal); an explicit id
    set does not get that leniency — naming an absent id means the config and
    the fixture are from different generations, and skipping it silently would
    shrink a chunk without anyone noticing.
    """
    known = {case["id"] for case in cases}
    seen: dict[int, int] = {}
    duplicated: list[int] = []
    phantom: list[int] = []
    chunks: list[Chunk] = []
    for index, spec in enumerate(config["chunks"]):
        explicit = spec[0] == "ids"
        candidates = spec[1] if explicit else range(spec[1], spec[2] + 1)
        covered = []
        for case_id in candidates:
            if case_id not in known:
                if explicit:
                    phantom.append(case_id)
                continue
            if case_id in seen:
                duplicated.append(case_id)
                continue
            seen[case_id] = index
            covered.append(case_id)
        lo = min(covered) if explicit and covered else (spec[1] if not explicit else 0)
        hi = max(covered) if explicit and covered else (spec[2] if not explicit else 0)
        chunks.append(Chunk(lo=lo, hi=hi, case_ids=tuple(covered)))
    missing = sorted(known - set(seen))
    problems = []
    if missing:
        problems.append(f"ids covered by no chunk: {missing}")
    if duplicated:
        problems.append(f"ids covered by more than one chunk: {sorted(set(duplicated))}")
    if phantom:
        problems.append(f"explicit chunk ids absent from evals.json: {sorted(set(phantom))}")
    if problems:
        raise ConfigError("chunks do not partition evals.json — " + "; ".join(problems))
    empty = [f"[{c.lo}, {c.hi}]" for c in chunks if not c.case_ids]
    if empty:
        raise ConfigError(f"chunk range(s) cover no case at all: {', '.join(empty)}")
    return tuple(chunks)


def criteria_section(skill_dir: Path, config: dict) -> str:
    """Return the protocol's criteria section verbatim, heading included."""
    path = skill_dir / config["protocol"]["file"]
    if not path.exists():
        raise ConfigError(f"missing declared protocol file: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"cannot read {path}: {exc}") from exc
    wanted = config["protocol"]["criteria_section"]
    lines = text.split("\n")
    start, level = None, 0
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not match:
            continue
        if start is None and match.group(2) == wanted:
            start, level = index, len(match.group(1))
            continue
        if start is not None and len(match.group(1)) <= level:
            return "\n".join(lines[start:index]).strip()
    if start is None:
        raise ConfigError(f"{path}: no heading named {wanted!r} (protocol.criteria_section)")
    return "\n".join(lines[start:]).strip()


def parse_ids(spec: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Parse an --ids selector like '1-9,20' into (listed ids, ranged ids).

    The two are kept apart because they mean different things when an id does
    not exist: a listed id is a typo, a span over a hole in the fixture's
    numbering is not.
    """
    listed: list[int] = []
    ranged: list[int] = []
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token.lstrip("-"):
            lo_text, _, hi_text = token.partition("-")
            try:
                lo, hi = int(lo_text), int(hi_text)
            except ValueError:
                raise ScoreEvalsError(f"--ids: bad range {token!r}") from None
            if lo > hi:
                raise ScoreEvalsError(f"--ids: inverted range {token!r}")
            ranged.extend(range(lo, hi + 1))
            continue
        try:
            listed.append(int(token))
        except ValueError:
            raise ScoreEvalsError(f"--ids: bad id {token!r}") from None
    if not listed and not ranged:
        raise ScoreEvalsError(f"--ids: selected nothing from {spec!r}")
    return tuple(sorted(set(listed))), tuple(sorted(set(ranged)))


def resolve_ids(spec: str, known: set[int]) -> tuple[int, ...]:
    """Resolve --ids against the fixture, tolerating holes inside a range."""
    listed, ranged = parse_ids(spec)
    unknown = sorted(i for i in listed if i not in known)
    if unknown:
        raise ScoreEvalsError(f"--ids names id(s) absent from evals.json: {unknown}")
    selected = tuple(sorted(set(listed) | {i for i in ranged if i in known}))
    if not selected:
        raise ScoreEvalsError(
            f"--ids: {spec!r} matches no id in evals.json"
        )
    return selected

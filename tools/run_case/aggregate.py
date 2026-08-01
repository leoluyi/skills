"""Multi-round aggregation of run-case results.

A single round's protection number is not a verdict. Measured over seven
rounds on one skill state, the new arm's protection-class failures ranged 0–3
and the *failing rows differed almost entirely between rounds* — eight distinct
rows failed at least once, none failed consistently. Against that variance an
absolute per-round "zero protection false kills" gate is a coin flip: it clears
whenever a round happens to draw zero, and blocks a version no worse than the
one that cleared.

So the gate moves off the single round and onto what repetition can actually
distinguish. A real defect recurs; sampling noise does not. A protection row is
**confirmed** only when the new arm fails it in at least two rounds, and it is
confirmed rows — not any round's raw count — that block shipping.

Two guards keep that from becoming a loophole. A version that fails three
*different* protection rows every round has no repeats yet is plainly worse, so
the new arm's mean protection failures must also not exceed the baseline's. And
every round must have measured the same thing: same skill text, same baseline,
same rubric, same models. Rounds that do not agree on all of those are not a
sample, and aggregating them is an error rather than a warning.
"""

from __future__ import annotations

import json
from pathlib import Path

from run_case.errors import RunCaseError
from run_case.report import HIT, PROTECTION

# Two rounds can only ever say "these two agreed" or "these two differed"; the
# first is indistinguishable from two identical draws of the same noise. Three
# is the smallest sample where a row failing twice is more likely a defect than
# a coincidence.
MIN_ROUNDS = 3

# A row the new arm failed in this many rounds or more is a defect, not a draw.
CONFIRM_AT = 2

# Every field that must match across rounds for them to be one sample. Each
# names something that changes what was measured rather than how it came out.
IDENTITY_FIELDS = (
    "skill",
    "baseline_ref",
    "baseline_dir",
    "new_blob_sha256",
    "base_blob_sha256",
    "criteria_sha256",
    "grader_brief_sha256",
    "runner",
    "grader",
    "runner_model",
    "grader_model",
)


def load_round(path: Path) -> dict:
    """Read one round's result JSON, rejecting anything that cannot be scored."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RunCaseError(f"cannot read {path}: {exc}") from None
    except json.JSONDecodeError as exc:
        raise RunCaseError(f"{path} is not valid JSON: {exc}") from None
    if not isinstance(data, dict) or "results" not in data:
        raise RunCaseError(f"{path} is not a run-case result file")
    if data.get("partial"):
        raise RunCaseError(
            f"{path} is a partial (--ids) run — a subset score cannot stand in "
            "for a round, since the rows it never ran read as passes"
        )
    missing = [name for name in IDENTITY_FIELDS if name not in data]
    if missing:
        raise RunCaseError(
            f"{path} predates aggregate scoring — it lacks {', '.join(missing)}. "
            "Re-run it; rounds whose skill text cannot be identified cannot be "
            "pooled with rounds whose can."
        )
    return dict(data, source=str(path))


def identity_errors(rounds: tuple[dict, ...]) -> list[str]:
    """Name every field on which the rounds disagree about what they measured."""
    errors = []
    first = rounds[0]
    for name in IDENTITY_FIELDS:
        seen = {r[name] for r in rounds}
        if len(seen) > 1:
            values = ", ".join(
                f"{Path(r['source']).name}={r[name]!r}" for r in rounds
            )
            errors.append(f"{name} differs across rounds: {values}")
    run_ids = [r.get("run_id") for r in rounds]
    if len(set(run_ids)) != len(run_ids):
        errors.append(
            "the same run_id appears twice — one round counted as two would "
            "confirm its own failures"
        )
    if len(rounds) < MIN_ROUNDS:
        errors.append(
            f"{len(rounds)} round(s) given, {MIN_ROUNDS} is the minimum: below "
            "that, a row failing twice cannot be told from noise agreeing twice"
        )
    del first
    return errors


def row_key(result: dict) -> tuple[int, str]:
    return (result["case_id"], result["expectation"])


def failure_counts(rounds: tuple[dict, ...], klass: str, arm: str,
                   incompatible: frozenset[int]) -> dict[tuple[int, str], int]:
    """How many rounds each row failed in, for one class and one arm."""
    counts: dict[tuple[int, str], int] = {}
    for data in rounds:
        for result in data["results"]:
            if result["class"] != klass or result[arm] != "fail":
                continue
            if klass == HIT and result["case_id"] in incompatible:
                continue
            key = row_key(result)
            counts[key] = counts.get(key, 0) + 1
    return counts


def per_round_totals(rounds: tuple[dict, ...], klass: str, arm: str,
                     incompatible: frozenset[int]) -> tuple[int, ...]:
    totals = []
    for data in rounds:
        totals.append(sum(
            1 for result in data["results"]
            if result["class"] == klass and result[arm] == "fail"
            and not (klass == HIT and result["case_id"] in incompatible)
        ))
    return tuple(totals)


def incompatible_ids(rounds: tuple[dict, ...]) -> frozenset[int]:
    ids: set[int] = set()
    for data in rounds:
        for entry in data.get("incompatible_entries", ()):
            ids.update(entry.get("ids", ()))
    return frozenset(ids)


def mean(values: tuple[int, ...]) -> float:
    return sum(values) / len(values) if values else 0.0


def aggregate(rounds: tuple[dict, ...]) -> dict:
    """Score the pooled rounds and return the ship decision with its evidence."""
    errors = identity_errors(rounds)
    if errors:
        raise RunCaseError("rounds are not one sample:\n  " + "\n  ".join(errors))

    incompatible = incompatible_ids(rounds)
    n = len(rounds)

    prot_new = failure_counts(rounds, PROTECTION, "new", incompatible)
    prot_base = failure_counts(rounds, PROTECTION, "base", incompatible)
    hit_new = failure_counts(rounds, HIT, "new", incompatible)
    hit_base = failure_counts(rounds, HIT, "base", incompatible)

    confirmed = sorted(
        (key for key, count in prot_new.items() if count >= CONFIRM_AT),
        key=lambda key: (-prot_new[key], key[0], key[1]),
    )
    # Rows that failed exactly once are the ones a further round would settle.
    unconfirmed = sorted(
        (key for key, count in prot_new.items() if count < CONFIRM_AT),
        key=lambda key: (key[0], key[1]),
    )

    prot_new_totals = per_round_totals(rounds, PROTECTION, "new", incompatible)
    prot_base_totals = per_round_totals(rounds, PROTECTION, "base", incompatible)
    hit_new_totals = per_round_totals(rounds, HIT, "new", incompatible)
    hit_base_totals = per_round_totals(rounds, HIT, "base", incompatible)

    reasons = []
    if confirmed:
        named = ", ".join(
            f"{case_id}/{slug} ({prot_new[(case_id, slug)]}/{n})"
            for case_id, slug in confirmed[:8]
        )
        rest = len(confirmed) - min(len(confirmed), 8)
        reasons.append(
            f"{len(confirmed)} confirmed protection-class false kill(s) — failed "
            f"in {CONFIRM_AT}+ of {n} rounds: {named}"
            + (f", and {rest} more" if rest else "")
        )
    if mean(prot_new_totals) > mean(prot_base_totals):
        reasons.append(
            f"protection-class mean regressed: new arm {mean(prot_new_totals):.2f} "
            f"per round vs baseline {mean(prot_base_totals):.2f} — no single row "
            "repeats, but the arm kills more protected spans than the baseline does"
        )
    if mean(hit_new_totals) > mean(hit_base_totals):
        reasons.append(
            f"hit-class mean regressed: new arm {mean(hit_new_totals):.2f} "
            f"failure(s) per round vs baseline {mean(hit_base_totals):.2f} "
            "(comparative denominator)"
        )

    return {
        "rounds": n,
        "sources": [r["source"] for r in rounds],
        "run_ids": [r.get("run_id") for r in rounds],
        "skill": rounds[0]["skill"],
        "new_version": rounds[0].get("new_version"),
        "base_version": rounds[0].get("base_version"),
        "baseline_ref": rounds[0]["baseline_ref"],
        "new_blob_sha256": rounds[0]["new_blob_sha256"],
        "base_blob_sha256": rounds[0]["base_blob_sha256"],
        "confirm_at": CONFIRM_AT,
        "confirmed_protection": [
            {"case_id": c, "expectation": s, "rounds_failed": prot_new[(c, s)]}
            for c, s in confirmed
        ],
        "unconfirmed_protection": [
            {"case_id": c, "expectation": s, "rounds_failed": prot_new[(c, s)]}
            for c, s in unconfirmed
        ],
        "protection_per_round_new": prot_new_totals,
        "protection_per_round_base": prot_base_totals,
        "hit_per_round_new": hit_new_totals,
        "hit_per_round_base": hit_base_totals,
        "protection_mean_new": mean(prot_new_totals),
        "protection_mean_base": mean(prot_base_totals),
        "hit_mean_new": mean(hit_new_totals),
        "hit_mean_base": mean(hit_base_totals),
        "repeated_base_protection": sorted(
            (f"{c}/{s}" for (c, s), count in prot_base.items() if count >= CONFIRM_AT)
        ),
        "repeated_base_hit": sorted(
            (f"{c}/{s}" for (c, s), count in hit_base.items() if count >= CONFIRM_AT)
        ),
        "repeated_new_hit": sorted(
            (f"{c}/{s}" for (c, s), count in hit_new.items() if count >= CONFIRM_AT)
        ),
        "ship": not reasons,
        "reasons": reasons,
    }


def _round_row(label: str, totals: tuple[int, ...], average: float) -> str:
    return f"| {label} | " + " | ".join(str(t) for t in totals) + f" | {average:.2f} |"


def aggregate_markdown(agg: dict) -> str:
    n = agg["rounds"]
    lines = [
        f"# run-case aggregate — {agg['skill']} — {n} rounds",
        "",
        f"- new arm: version {agg['new_version']}, "
        f"blob sha256 `{agg['new_blob_sha256']}`",
        f"- base arm: `{agg['baseline_ref']}`, version {agg['base_version']}, "
        f"blob sha256 `{agg['base_blob_sha256']}`",
        f"- a protection row counts as confirmed at {agg['confirm_at']} of {n} rounds",
        "",
        "## Rounds pooled",
        "",
        "| # | source | run id |",
        "|---|---|---|",
    ]
    for index, (source, run_id) in enumerate(zip(agg["sources"], agg["run_ids"]), 1):
        lines.append(f"| {index} | `{Path(source).name}` | `{run_id}` |")
    header = "| class / arm | " + " | ".join(f"r{i}" for i in range(1, n + 1)) + " | mean |"
    lines += [
        "",
        "## Failures per round",
        "",
        header,
        "|---" * (n + 2) + "|",
        _round_row("保護 new", agg["protection_per_round_new"], agg["protection_mean_new"]),
        _round_row("保護 base", agg["protection_per_round_base"], agg["protection_mean_base"]),
        _round_row("命中 new", agg["hit_per_round_new"], agg["hit_mean_new"]),
        _round_row("命中 base", agg["hit_per_round_base"], agg["hit_mean_base"]),
        "",
        "## Protection rows the new arm failed",
        "",
    ]
    if agg["confirmed_protection"] or agg["unconfirmed_protection"]:
        lines += ["| case | expectation | rounds failed | status |", "|---|---|---|---|"]
        for entry in agg["confirmed_protection"]:
            lines.append(
                f"| {entry['case_id']} | {entry['expectation']} | "
                f"{entry['rounds_failed']}/{n} | **confirmed** |"
            )
        for entry in agg["unconfirmed_protection"]:
            lines.append(
                f"| {entry['case_id']} | {entry['expectation']} | "
                f"{entry['rounds_failed']}/{n} | unconfirmed |"
            )
        lines += [
            "",
            "Unconfirmed rows are the ones another round would settle: they failed "
            "once, which is what a defect and a bad draw look like alike.",
        ]
    else:
        lines.append("None — the new arm passed every protection row in every round.")
    lines += ["", "## Gate", ""]
    if agg["ship"]:
        lines.append(
            "SHIP — no confirmed protection false kill; neither class's mean "
            "regressed against the baseline."
        )
    else:
        lines.append("NO-SHIP — " + "; ".join(agg["reasons"]))
    return "\n".join(lines)

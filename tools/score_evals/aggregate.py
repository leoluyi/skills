"""Multi-round aggregation of score-evals results.

A single round's protection number is not a verdict. Measured over seven rounds
on one skill state, the new arm's protection-class failures ranged 0–3 and the
*failing rows differed almost entirely between rounds* — eight distinct rows
failed at least once, none failed consistently. Against that variance an
absolute per-round "zero protection false kills" gate is a coin flip.

So the gate moves off the single round and onto what repetition can distinguish.
A real defect recurs; sampling noise does not. Three things decide what counts
as recurrence, and each of them is measured rather than assumed — see
`calibration.py` for the null they come from.

**Only the new arm's own damage counts.** A row red in both arms is the
baseline's debt. Charging it to a branch that merely failed to fix it is what
made this gate red on changes that touched nothing near it: of eight rows it
once called confirmed false kills, seven were already red on main.

**Confirmation scales with the sample.** At a fixed two rounds, more rounds meant
more chances for an unstable row to land on two, so the null's 95th percentile
climbed from 3 confirmed rows at three rounds to 11 at eight — the gate
dissolved as evidence accumulated. A majority reverses that.

**A count of rows, compared against its own mirror, replaces the class mean.**
The old mean guardrail asked whether the new arm killed more protected spans per
round than the baseline, and fired whenever the difference was above zero; that
difference's own round-to-round spread was four to eight times the threshold, so
it fired on 47% of comparisons between a text and itself. The row margin —
rows that regressed on net, minus rows that improved — answers the same question
about broad shallow damage, but a single flaky row can move it by at most one,
and the improving side subtracts the corpus's own flakiness back out.

Class means are still reported. They are the fastest read on what happened; they
are simply no longer allowed to decide.
"""

from __future__ import annotations

import json
from pathlib import Path

from score_evals.calibration import confirm_at, load_calibration, thresholds
from score_evals.errors import ScoreEvalsError
from score_evals.report import HIT, PROTECTION

# Two rounds can only ever say "these two agreed" or "these two differed"; the
# first is indistinguishable from two identical draws of the same noise. Three
# is the smallest sample that can pool at all.
MIN_ROUNDS = 3

# Three rounds can clear a change but cannot condemn one. Splitting the archive
# against itself, three rounds produce up to 3 confirmed protection rows and up
# to 4 hit rows from nothing at all, so a block at that sample size needs an
# effect too large to be the kind of regression worth catching. Six rounds bring
# the same ceilings down to 1.
BLOCK_MIN_ROUNDS = 6

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
    "runner_effort",
    "grader_effort",
    "baseline_source",
)


def load_round(path: Path) -> dict:
    """Read one round's result JSON, rejecting anything that cannot be scored."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ScoreEvalsError(f"cannot read {path}: {exc}") from None
    except json.JSONDecodeError as exc:
        raise ScoreEvalsError(f"{path} is not valid JSON: {exc}") from None
    if not isinstance(data, dict) or "results" not in data:
        raise ScoreEvalsError(f"{path} is not a score-evals result file")
    if data.get("partial"):
        raise ScoreEvalsError(
            f"{path} is a partial (--ids) run — a subset score cannot stand in "
            "for a round, since the rows it never ran read as passes"
        )
    missing = [name for name in IDENTITY_FIELDS if name not in data]
    if missing:
        raise ScoreEvalsError(
            f"{path} predates aggregate scoring — it lacks {', '.join(missing)}. "
            "Re-run it; rounds whose skill text cannot be identified cannot be "
            "pooled with rounds whose can."
        )
    return dict(data, source=str(path))


def identity_errors(rounds: tuple[dict, ...]) -> list[str]:
    """Name every field on which the rounds disagree about what they measured."""
    errors = []
    for name in IDENTITY_FIELDS:
        seen = {r[name] for r in rounds}
        if len(seen) > 1:
            values = ", ".join(f"{Path(r['source']).name}={r[name]!r}" for r in rounds)
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
    return errors


def incompatible_ids(rounds: tuple[dict, ...]) -> frozenset[int]:
    ids: set[int] = set()
    for data in rounds:
        for entry in data.get("incompatible_entries", ()):
            ids.update(entry.get("ids", ()))
    return frozenset(ids)


def paired_rows(rounds: tuple[dict, ...], klass: str,
                incompatible: frozenset[int]) -> list[dict]:
    """One entry per row, holding how the two arms differed across the rounds."""
    runs: dict[tuple[int, str], dict[str, list[bool]]] = {}
    for data in rounds:
        for result in data["results"]:
            if result["class"] != klass:
                continue
            if klass == HIT and result["case_id"] in incompatible:
                continue
            key = (result["case_id"], result["expectation"])
            entry = runs.setdefault(key, {"new": [], "base": []})
            entry["new"].append(result["new"] == "fail")
            entry["base"].append(result["base"] == "fail")

    rows = []
    for (case_id, expectation), arms in runs.items():
        pairs = list(zip(arms["new"], arms["base"]))
        rows.append({
            "case_id": case_id,
            "expectation": expectation,
            "new_failed": sum(arms["new"]),
            "base_failed": sum(arms["base"]),
            "regressed": sum(1 for n, b in pairs if n and not b),
            "improved": sum(1 for n, b in pairs if b and not n),
            "both_failed": sum(1 for n, b in pairs if n and b),
        })
    rows.sort(key=lambda row: (-row["regressed"], -row["new_failed"],
                               row["case_id"], row["expectation"]))
    return rows


def per_round_totals(rounds: tuple[dict, ...], klass: str, arm: str,
                     incompatible: frozenset[int]) -> tuple[int, ...]:
    return tuple(
        sum(
            1 for result in data["results"]
            if result["class"] == klass and result[arm] == "fail"
            and not (klass == HIT and result["case_id"] in incompatible)
        )
        for data in rounds
    )


def mean(values: tuple[int, ...]) -> float:
    return sum(values) / len(values) if values else 0.0


def score_class(rows: list[dict], n: int, klass: str, table: dict) -> dict:
    """Apply the calibrated thresholds to one class's paired rows."""
    # Each row lands in exactly one bucket, most-actionable first. A row that
    # both carries a pre-existing gap and had one extra bad round reads as the
    # gap: the branch did not create it, and a single extra round is what a
    # draw looks like.
    at = confirm_at(n)
    confirmed = [row for row in rows if row["regressed"] >= at]
    pre_existing = [
        row for row in rows
        if row["regressed"] < at and row["both_failed"] >= at
    ]
    unconfirmed = [
        row for row in rows
        if row["regressed"] < at and row["both_failed"] < at and row["regressed"] > 0
    ]
    margin = sum(
        (row["regressed"] > row["improved"]) - (row["improved"] > row["regressed"])
        for row in rows
    )
    limits = thresholds(n, klass, table)
    breaches = []
    if limits is None:
        breaches.append(
            f"{klass}: no calibration for {n} rounds — thresholds unknown, so "
            "nothing here can be called a regression or cleared as noise"
        )
    else:
        if len(confirmed) > limits["confirmed_max"]:
            named = ", ".join(
                f"{row['case_id']}/{row['expectation']} ({row['regressed']}/{n})"
                for row in confirmed[:8]
            )
            rest = len(confirmed) - min(len(confirmed), 8)
            breaches.append(
                f"{klass}: {len(confirmed)} row(s) the new arm broke on its own in "
                f"{at}+ of {n} rounds, above the {limits['confirmed_max']} that "
                f"identical text produces — {named}"
                + (f", and {rest} more" if rest else "")
            )
        if margin > limits["row_margin_max"]:
            breaches.append(
                f"{klass}: row margin {margin:+d}, above the "
                f"{limits['row_margin_max']:+d} identical text produces — more "
                "rows got worse than got better, spread too thin to repeat on "
                "any single row"
            )
    return {
        "class": klass,
        "confirm_at": at,
        "confirmed": confirmed,
        "unconfirmed": unconfirmed,
        "pre_existing": pre_existing,
        "row_margin": margin,
        "thresholds": limits,
        "breaches": breaches,
    }


def steering_ids(scored: tuple[dict, ...]) -> tuple[int, ...]:
    """Case ids worth re-running with --ids while iterating on a fix.

    A partial run rechunks the fixture, so it cannot stand in for a round and
    cannot confirm a fix — a green there has been observed not to survive a full
    round. What it does cheaply is disconfirm: a row still red on three cases is
    red on eighteen.
    """
    ids = set()
    for entry in scored:
        for row in entry["confirmed"]:
            ids.add(row["case_id"])
    return tuple(sorted(ids))


def aggregate(rounds: tuple[dict, ...], table: dict | None = None) -> dict:
    """Score the pooled rounds and return the ship decision with its evidence."""
    errors = identity_errors(rounds)
    if errors:
        raise ScoreEvalsError("rounds are not one sample:\n  " + "\n  ".join(errors))

    table = table if table is not None else load_calibration()
    incompatible = incompatible_ids(rounds)
    n = len(rounds)

    scored = tuple(
        score_class(paired_rows(rounds, klass, incompatible), n, klass, table)
        for klass in (PROTECTION, HIT)
    )
    breaches = [reason for entry in scored for reason in entry["breaches"]]

    if not breaches:
        verdict = "SHIP"
    elif n < BLOCK_MIN_ROUNDS:
        verdict = "INCONCLUSIVE"
    else:
        verdict = "NO-SHIP"

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
        "calibration": {
            "method": table.get("method", "cross-round"),
            "base_blob_sha256": table.get("base_blob_sha256"),
            "criteria_sha256": table.get("criteria_sha256"),
            "pool_rounds": table.get("pool_rounds"),
            "percentile": table.get("percentile"),
            "stale_criteria": (
                table.get("criteria_sha256") is not None
                and table["criteria_sha256"] != rounds[0]["criteria_sha256"]
            ),
        },
        "classes": scored,
        "protection_per_round_new": per_round_totals(rounds, PROTECTION, "new", incompatible),
        "protection_per_round_base": per_round_totals(rounds, PROTECTION, "base", incompatible),
        "hit_per_round_new": per_round_totals(rounds, HIT, "new", incompatible),
        "hit_per_round_base": per_round_totals(rounds, HIT, "base", incompatible),
        "steering_ids": steering_ids(scored),
        "verdict": verdict,
        "reasons": breaches,
    }


def _round_row(label: str, totals: tuple[int, ...]) -> str:
    return (f"| {label} | " + " | ".join(str(t) for t in totals)
            + f" | {mean(totals):.2f} |")


def _row_lines(rows: list[dict], n: int, status: str) -> list[str]:
    return [
        f"| {row['case_id']} | {row['expectation']} | {row['regressed']}/{n} "
        f"| {row['improved']}/{n} | {row['both_failed']}/{n} | {status} |"
        for row in rows
    ]


def aggregate_markdown(agg: dict) -> str:
    n = agg["rounds"]
    cal = agg["calibration"]
    lines = [
        f"# score-evals aggregate — {agg['skill']} — {n} rounds",
        "",
        f"- new arm: version {agg['new_version']}, blob sha256 `{agg['new_blob_sha256']}`",
        f"- base arm: `{agg['baseline_ref']}`, version {agg['base_version']}, "
        f"blob sha256 `{agg['base_blob_sha256']}`",
        f"- thresholds: {cal['percentile']:.0%} of a "
        + (
            f"same-call null resampled from {cal['pool_rounds']} --null-run "
            "round(s) (two independent baseline generations judged in one "
            "grader call)"
            if cal.get("method") == "same-call" else
            f"cross-round null built by splitting {cal['pool_rounds']} "
            "same-baseline rounds against themselves"
        ),
        "",
        "## Rounds pooled",
        "",
        "| # | source | run id |",
        "|---|---|---|",
    ]
    for index, (source, run_id) in enumerate(zip(agg["sources"], agg["run_ids"]), 1):
        lines.append(f"| {index} | `{Path(source).name}` | `{run_id}` |")

    if cal["stale_criteria"]:
        lines += [
            "",
            "The calibration was measured under a different rubric than these "
            "rounds ran under. Its ceilings still describe the old setup; "
            "regenerate with `--calibrate` once six rounds exist under this one.",
        ]

    header = "| class / arm | " + " | ".join(f"r{i}" for i in range(1, n + 1)) + " | mean |"
    lines += [
        "",
        "## Failures per round",
        "",
        header,
        "|---" * (n + 2) + "|",
        _round_row("保護 new", agg["protection_per_round_new"]),
        _round_row("保護 base", agg["protection_per_round_base"]),
        _round_row("命中 new", agg["hit_per_round_new"]),
        _round_row("命中 base", agg["hit_per_round_base"]),
        "",
        "Reported, not judged: the round-to-round spread of these means is "
        "several times the difference any threshold on them would act on.",
    ]

    for entry in agg["classes"]:
        limits = entry["thresholds"]
        if limits is None:
            ceiling = "uncalibrated at this round count"
        else:
            ceiling = (
                f"blocks above {limits['confirmed_max']} confirmed row(s) or a "
                f"row margin above {limits['row_margin_max']:+d}"
            )
            if limits["calibrated_at"] != n:
                ceiling += (
                    f", borrowed from the {limits['calibrated_at']}-round "
                    "calibration, whose null is noisier and whose ceiling is "
                    "therefore the looser one"
                )
        lines += [
            "",
            f"## {entry['class']} — rows",
            "",
            f"Confirmed at {entry['confirm_at']}+ of {n} rounds. "
            f"Row margin {entry['row_margin']:+d}. {ceiling}.",
            "",
        ]
        body = (
            _row_lines(entry["confirmed"], n, "**新臂造成**")
            + _row_lines(entry["pre_existing"], n, "既有缺口")
            + _row_lines(entry["unconfirmed"], n, "未確認")
        )
        if body:
            lines += [
                "| case | expectation | 新臂獨有紅 | 新臂獨有綠 | 兩臂同紅 | status |",
                "|---|---|---|---|---|---|",
                *body,
            ]
        else:
            lines.append("None — the new arm broke nothing the baseline held.")

    if agg["steering_ids"]:
        ids = ",".join(str(i) for i in agg["steering_ids"])
        lines += [
            "",
            "## Steering",
            "",
            f"    tools/score-evals {agg['skill']} --baseline {agg['baseline_ref']} --ids {ids}",
            "",
            "A partial run rechunks the fixture, so it can only disconfirm: a row "
            "still red on a handful of cases is red on the whole set, but a row "
            "that turns green there has been seen to stay red in a full round.",
        ]

    lines += ["", "## Gate", ""]
    if agg["verdict"] == "SHIP":
        lines.append(
            "SHIP — no class exceeded what identical text produces on the same "
            "statistics."
        )
    elif agg["verdict"] == "INCONCLUSIVE":
        lines.append(
            f"INCONCLUSIVE — {'; '.join(agg['reasons'])}. At {n} rounds this "
            f"cannot be called a regression; take it to {BLOCK_MIN_ROUNDS} rounds "
            "to settle it."
        )
    else:
        lines.append("NO-SHIP — " + "; ".join(agg["reasons"]))
    return "\n".join(lines)

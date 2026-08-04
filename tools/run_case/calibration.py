"""Thresholds measured against a null built from the archive, not derived.

Every gate statistic needs a number that separates "the new arm is worse" from
"the grader drew differently this time". Estimating that number from a variance
model failed here: the round-to-round spread was four to eight times the value
the guardrail acted on, so the guardrails fired on coin flips.

What replaces the model is a null with a known answer. Rounds that share a base
blob scored the same text every time, so splitting those rounds into two
disjoint halves and calling one half the new arm produces a comparison in which
every reported regression is a false alarm. Run thousands of such splits and the
95th percentile of each statistic is its false-alarm ceiling, counted rather
than assumed.

`tools/run-case --calibrate` regenerates `calibration.json` from any set of
rounds sharing a base blob. Re-run it whenever the corpus, the rubric or the
grader model changes: those numbers describe one measurement setup, not a
property of the statistics.

One limit is baked into the method. The null splits *across* rounds, while a
real gate compares the two arms inside a single grader call, which shares that
call's draw. The null therefore carries more noise than the comparison it
calibrates, and its thresholds run loose — a gate built on them under-blocks
rather than over-blocks. Closing that gap needs a round dispatched with the two
arms on identical text.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

from run_case.errors import RunCaseError
from run_case.report import HIT, PROTECTION

CALIBRATION_PATH = Path(__file__).with_name("calibration.json")

# The percentile of the null a statistic must exceed before it blocks. At 0.95
# one gate in twenty blocks a change that is no worse than the baseline, which
# is the cost of not letting real regressions through twenty times as often.
NULL_PERCENTILE = 0.95

# How many random half-splits to draw when calibrating. The statistics are
# small integers, so the percentile stabilises well before this.
SPLITS = 4000


def confirm_at(rounds: int) -> int:
    """How many rounds a row must regress in before it counts as confirmed.

    A fixed count of two makes the gate looser the longer it runs: with more
    rounds, any unstable row gets more chances to land on two. Measured against
    the null, a fixed two gives a 95th percentile of 3 confirmed rows at three
    rounds and 11 at eight — the gate dissolves exactly when more evidence
    should be sharpening it.

    A majority reverses that. The same null gives 3 rows at three rounds and 1
    at six, because a row now has to fail more often as the sample grows. At
    three rounds a majority is two, so this leaves the original rule unchanged
    where it started.
    """
    return rounds // 2 + 1


def load_calibration(path: Path | None = None) -> dict:
    path = path or CALIBRATION_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RunCaseError(f"cannot read calibration table {path}: {exc}") from None
    except json.JSONDecodeError as exc:
        raise RunCaseError(f"{path} is not valid JSON: {exc}") from None
    return data


def thresholds(rounds: int, klass: str, table: dict | None = None) -> dict | None:
    """The false-alarm ceilings for this round count, or None if uncalibrated.

    Round counts between calibrated points fall back to the nearest calibrated
    count at or below them, which is the conservative direction: fewer rounds
    means a noisier null and a higher ceiling.
    """
    table = table if table is not None else load_calibration()
    entries = table.get("thresholds", {})
    available = sorted(
        int(key.split("/")[0]) for key in entries if key.endswith(f"/{klass}")
    )
    usable = [n for n in available if n <= rounds]
    if not usable:
        return None
    return dict(entries[f"{usable[-1]}/{klass}"], calibrated_at=usable[-1])


def _row_table(rounds: tuple[dict, ...], arm: str, klass: str,
               incompatible: frozenset[int]) -> dict[tuple[int, str], list[bool]]:
    table: dict[tuple[int, str], list[bool]] = defaultdict(list)
    for data in rounds:
        for result in data["results"]:
            if result["class"] != klass:
                continue
            if klass == HIT and result["case_id"] in incompatible:
                continue
            table[(result["case_id"], result["expectation"])].append(
                result[arm] == "fail"
            )
    return table


def paired_stats(new_table: dict, base_table: dict, at: int) -> tuple[int, int]:
    """(confirmed new-arm-only regressions, row margin) for one paired table.

    A row regresses in a round when the new arm fails it and the baseline does
    not; it improves when the reverse happens. Rows red in both arms score
    neither way — they are the baseline's own debt, and charging them to a
    branch that merely failed to fix them is what made the old gate red on
    changes that touched nothing near them.

    The margin counts *rows*, not cells, so a single flaky row can move it by
    at most one. That is what lets it see a regression spread thinly across
    many rows, which is the shape the per-row rule is blind to by construction.
    """
    confirmed = margin = 0
    for key in set(new_table) & set(base_table):
        new_runs, base_runs = new_table[key], base_table[key]
        worse = sum(1 for n, b in zip(new_runs, base_runs) if n and not b)
        better = sum(1 for n, b in zip(new_runs, base_runs) if b and not n)
        if worse >= at:
            confirmed += 1
        margin += (worse > better) - (better > worse)
    return confirmed, margin


def calibrate(pool: tuple[dict, ...], splits: int = SPLITS, seed: int = 0) -> dict:
    """Measure each statistic's false-alarm distribution from a pooled null."""
    blobs = {r["base_blob_sha256"] for r in pool}
    if len(blobs) != 1:
        raise RunCaseError(
            "calibration needs rounds that scored the same baseline text: "
            f"{len(blobs)} distinct base blobs given"
        )
    if len(pool) < 6:
        raise RunCaseError(
            f"{len(pool)} rounds given; 6 is the minimum, since a split needs "
            "three rounds on each side to produce the smallest gate-sized null"
        )

    incompatible: set[int] = set()
    for data in pool:
        for entry in data.get("incompatible_entries", ()):
            incompatible.update(entry.get("ids", ()))
    frozen = frozenset(incompatible)

    rng = random.Random(seed)
    entries: dict[str, dict] = {}
    for half in range(3, len(pool) // 2 + 1):
        for klass in (PROTECTION, HIT):
            confirmed, margins = [], []
            at = confirm_at(half)
            for _ in range(splits):
                order = list(range(len(pool)))
                rng.shuffle(order)
                left = tuple(pool[i] for i in order[:half])
                right = tuple(pool[i] for i in order[half : 2 * half])
                c, m = paired_stats(
                    _row_table(left, "base", klass, frozen),
                    _row_table(right, "base", klass, frozen),
                    at,
                )
                confirmed.append(c)
                margins.append(m)
            index = int(NULL_PERCENTILE * splits)
            entries[f"{half}/{klass}"] = {
                "confirm_at": at,
                "confirmed_max": sorted(confirmed)[index],
                "row_margin_max": sorted(margins)[index],
            }

    first = pool[0]
    return {
        "note": (
            "False-alarm ceilings measured by splitting a shared-baseline round "
            "pool against itself. A statistic blocks only when it exceeds the "
            "ceiling. Regenerate with tools/run-case --calibrate after any "
            "change to the corpus, the rubric or the grader model."
        ),
        "percentile": NULL_PERCENTILE,
        "splits": splits,
        "pool_rounds": len(pool),
        "base_blob_sha256": first["base_blob_sha256"],
        "criteria_sha256": first.get("criteria_sha256"),
        "grader": first.get("grader"),
        "grader_model": first.get("grader_model"),
        "runner": first.get("runner"),
        "runner_model": first.get("runner_model"),
        "sources": sorted(Path(r["source"]).name for r in pool if "source" in r),
        "thresholds": entries,
    }

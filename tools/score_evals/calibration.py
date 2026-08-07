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

`tools/score-evals --calibrate` regenerates `calibration.json` from any set of
rounds sharing a base blob. Re-run it whenever the corpus, the rubric or the
grader model changes: those numbers describe one measurement setup, not a
property of the statistics.

A same-call null closes that gap directly rather than working around it: two
independent baseline generations, drawn from the baseline bank
(``tools/score_evals/bank.py``, ``--build-bank``) and judged inside one grader
call (``--null-run A,B``), give a comparison with the real gate's own pairing
structure — the same single-call draw — with a known answer, since both
labelled arms are baseline text. ``calibrate_same_call`` pools those null-run
results directly: no cross-round splitting, no shared-noise correction,
because the noise it needs is already the one the real gate has.

``calibrate`` (the cross-round split, below) remains for a skill with no
same-call null pool yet — regenerate the real calibration with
``calibrate_same_call`` once ``--null-run`` results exist for that baseline;
the cross-round path is a fallback, not the target state.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

from score_evals.errors import ScoreEvalsError
from score_evals.report import HIT, PROTECTION

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
        raise ScoreEvalsError(f"cannot read calibration table {path}: {exc}") from None
    except json.JSONDecodeError as exc:
        raise ScoreEvalsError(f"{path} is not valid JSON: {exc}") from None
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
        raise ScoreEvalsError(
            "calibration needs rounds that scored the same baseline text: "
            f"{len(blobs)} distinct base blobs given"
        )
    if len(pool) < 6:
        raise ScoreEvalsError(
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
        "method": "cross-round",
        "note": (
            "False-alarm ceilings measured by splitting a shared-baseline round "
            "pool against itself. A statistic blocks only when it exceeds the "
            "ceiling. This null pairs across separate grader calls, so its "
            "ceilings run loose relative to the real gate's single-call "
            "comparison — prefer calibrate_same_call once a --null-run pool "
            "exists for this baseline. Regenerate with tools/score-evals "
            "--calibrate after any change to the corpus, the rubric or the "
            "grader model."
        ),
        "percentile": NULL_PERCENTILE,
        "splits": splits,
        "pool_rounds": len(pool),
        "base_blob_sha256": first["base_blob_sha256"],
        "criteria_sha256": first.get("criteria_sha256"),
        "grader": first.get("grader"),
        "grader_model": first.get("grader_model"),
        "grader_effort": first.get("grader_effort"),
        "runner": first.get("runner"),
        "runner_model": first.get("runner_model"),
        "runner_effort": first.get("runner_effort"),
        "sources": sorted(Path(r["source"]).name for r in pool if "source" in r),
        "thresholds": entries,
    }


# Round counts the gate ever asks calibration for: MIN_ROUNDS through
# BLOCK_MIN_ROUNDS, from aggregate.py. Kept as a local constant rather than an
# import — aggregate.py imports this module, so importing back would cycle.
SAME_CALL_TARGET_ROUNDS = (3, 4, 5, 6)

# Below this, sampling with replacement cannot produce variance: a pool of 1
# draws the same round every time, and every threshold comes out identical to
# that round's own noise rather than a percentile over many. A 6-round bank
# gives C(6,2) = 15 null-run pairs, which is the pool this was designed for.
MIN_SAME_CALL_POOL = 3


def _same_call_identity_errors(null_pool: tuple[dict, ...]) -> list[str]:
    if len(null_pool) < MIN_SAME_CALL_POOL:
        return [
            f"{len(null_pool)} --null-run result(s) given, "
            f"{MIN_SAME_CALL_POOL} is the minimum — below that, sampling with "
            "replacement cannot produce real variance (a 6-round bank gives "
            "15 null-run pairs; that is the intended pool size)"
        ]
    not_null = [r.get("source", "?") for r in null_pool if not r.get("null")]
    if not_null:
        return [
            f"not a --null-run result: {', '.join(str(s) for s in not_null)} — "
            "same-call calibration only pools --null-run outputs"
        ]
    blobs = {r["base_blob_sha256"] for r in null_pool}
    if len(blobs) != 1:
        return [
            "same-call calibration needs null-runs that all compared the same "
            f"baseline blob: {len(blobs)} distinct base blobs given"
        ]
    return []


def calibrate_same_call(null_pool: tuple[dict, ...], splits: int = SPLITS, seed: int = 0,
                        target_rounds: tuple[int, ...] = SAME_CALL_TARGET_ROUNDS) -> dict:
    """Measure false-alarm ceilings by resampling a pool of same-call null runs.

    Each element of ``null_pool`` is one ``--null-run`` result: two independent
    baseline generations, judged inside a single grader call, labelled the way
    a real gate's new/base arms would be. Its ``new``/``base`` columns already
    are the comparison a real N-round gate would see if the new arm were no
    different from the baseline — no cross-round splitting is needed to
    construct that, because every null-run result already is one.

    To simulate an N-round gate, draw N null-run rounds *with replacement*
    (the pool is typically much smaller than a cross-round pool — 15 pairs
    from a 6-round bank — so without replacement would cap N at the pool size)
    and score them exactly as a real N-round aggregate would: pair each row's
    per-round (A-failed, B-failed) columns and count regressions the same way
    ``aggregate.paired_rows``/``score_class`` do.
    """
    errors = _same_call_identity_errors(null_pool)
    if errors:
        raise ScoreEvalsError("same-call calibration pool is invalid:\n  " + "\n  ".join(errors))

    incompatible: set[int] = set()
    for data in null_pool:
        for entry in data.get("incompatible_entries", ()):
            incompatible.update(entry.get("ids", ()))
    frozen = frozenset(incompatible)

    rng = random.Random(seed)
    entries: dict[str, dict] = {}
    for n in target_rounds:
        for klass in (PROTECTION, HIT):
            confirmed, margins = [], []
            at = confirm_at(n)
            for _ in range(splits):
                sample = tuple(rng.choice(null_pool) for _ in range(n))
                c, m = paired_stats(
                    _row_table(sample, "new", klass, frozen),
                    _row_table(sample, "base", klass, frozen),
                    at,
                )
                confirmed.append(c)
                margins.append(m)
            index = int(NULL_PERCENTILE * splits)
            entries[f"{n}/{klass}"] = {
                "confirm_at": at,
                "confirmed_max": sorted(confirmed)[index],
                "row_margin_max": sorted(margins)[index],
            }

    first = null_pool[0]
    return {
        "method": "same-call",
        "note": (
            "False-alarm ceilings measured by resampling, with replacement, a "
            "pool of --null-run results — each already a single blind grader "
            "call comparing two independent baseline generations. A statistic "
            "blocks only when it exceeds the ceiling. Regenerate with "
            "tools/score-evals --calibrate after any change to the corpus, the "
            "rubric, the grader model, or the baseline bank."
        ),
        "percentile": NULL_PERCENTILE,
        "splits": splits,
        "pool_rounds": len(null_pool),
        "base_blob_sha256": first["base_blob_sha256"],
        "criteria_sha256": first.get("criteria_sha256"),
        "grader": first.get("grader"),
        "grader_model": first.get("grader_model"),
        "grader_effort": first.get("grader_effort"),
        "runner": first.get("runner"),
        "runner_model": first.get("runner_model"),
        "runner_effort": first.get("runner_effort"),
        "sources": sorted(Path(r["source"]).name for r in null_pool if "source" in r),
        "thresholds": entries,
    }

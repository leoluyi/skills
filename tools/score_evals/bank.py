"""Baseline-arm output bank: persist a runner's baseline text across rounds so
each round only has to dispatch the new arm.

The baseline arm answers the same prompt every round — the text being judged
never changes, only the grader's draw does. Re-dispatching it every round paid
for a regeneration nobody needed: the rule blob and every case prompt, resent
in full, for an output whose content is not the thing under test. This module
dispatches a small pool of independent baseline generations once (``build``)
and lets every later round — on this branch or any other sharing the same
baseline blob — read one back instead of regenerating it.

Storage: ``skills/<skill>/evals/baseline-bank/<base_blob_sha256[:12]>/``
holds ``manifest.json`` plus ``r<round>/chunk<index>.out`` for each round the
bank was built with. The bank is keyed on the *blob* hash, not the branch or
ref name, so any branch that happens to compare against the same baseline text
shares the same bank for free.

Reuse requires an exact match, checked at load time rather than assumed:
same runner family, model and reasoning effort (a different effort answered a
different question even under the same model name), and the same runner
prompt per chunk — chunk layout, the rule blob, the grader/runner brief, or a
case's prompt text all feed that prompt, so any of them changing invalidates
the bank silently unless caught here. A mismatch is a hard error with a
rebuild instruction, never a silent fallback to a live dispatch: blending a
bank round from one measurement setup into a run under another would corrupt
the round the same way a version bump would.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

from score_evals.dispatch import RUNNER_TIMEOUT, dispatch
from score_evals.errors import ScoreEvalsError

BANK_DIRNAME = "baseline-bank"
MANIFEST_NAME = "manifest.json"


def bank_dir(skill_dir: Path, base_blob_sha256: str) -> Path:
    """The bank directory for one baseline blob. Keyed on content, not a ref
    name, so a baseline reachable under two different refs still shares it.
    """
    return skill_dir / "evals" / BANK_DIRNAME / base_blob_sha256[:12]


def prompt_sha256(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def chunk_out_path(root: Path, round_index: int, chunk_index: int) -> Path:
    return root / f"r{round_index}" / f"chunk{chunk_index}.out"


def load_manifest(root: Path) -> dict | None:
    path = root / MANIFEST_NAME
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScoreEvalsError(f"{path}: {exc}") from exc


def build(root: Path, rounds: int, family: str, model: str, effort: str | None,
          base_blob_sha256: str, baseline_ref: str, baseline_dir: str,
          base_version: str, chunk_prompts: dict[int, str], jobs: int) -> dict:
    """Dispatch ``rounds`` independent baseline generations per chunk and
    persist them. No grading happens here — the bank only ever stores what a
    runner said, never a verdict about it.
    """
    if rounds < 1:
        raise ScoreEvalsError(f"--rounds must be at least 1, got {rounds}")
    root.mkdir(parents=True, exist_ok=True)
    jobs_list = [
        (round_index, chunk_index, prompt)
        for round_index in range(1, rounds + 1)
        for chunk_index, prompt in sorted(chunk_prompts.items())
    ]
    total = len(jobs_list)
    errors: list[str] = []
    done_count = 0
    # dispatch() writes raw/*.out and raw/*.err under whatever workspace it is
    # given. That workspace must be scratch, not the bank root: the bank root
    # is what a later round reads back verbatim, and a diagnostic .err file
    # sitting next to chunk0.out is not part of what a runner said.
    scratch = Path(tempfile.mkdtemp(prefix="score-evals-bank-"))

    def run_one(item: tuple[int, int, str]) -> None:
        round_index, chunk_index, prompt = item
        out_path = chunk_out_path(root, round_index, chunk_index)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        text, _ = dispatch(
            family, prompt, scratch, f"bank-r{round_index}-c{chunk_index}", RUNNER_TIMEOUT
        )
        out_path.write_text(text, encoding="utf-8")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            pending = {pool.submit(run_one, item): item for item in jobs_list}
            for future in concurrent.futures.as_completed(pending):
                item = pending[future]
                done_count += 1
                try:
                    future.result()
                    outcome = "ok"
                except Exception as exc:  # noqa: BLE001 — see dispatch.worker_failure
                    outcome = "FAILED"
                    errors.append(f"round {item[0]} chunk {item[1]}: {exc}")
                print(f"[{done_count}/{total}] bank r{item[0]} c{item[1]} {outcome}",
                      file=sys.stderr, flush=True)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if errors:
        # Whatever chunk<N>.out files already landed under root before the
        # failure stay on disk — they are correct, real runner output, just
        # short of a full set. No manifest is written, so load_manifest still
        # returns None and a retried --build-bank starts clean.
        raise ScoreEvalsError("bank build failed:\n  " + "\n  ".join(sorted(errors)))

    manifest = {
        "base_blob_sha256": base_blob_sha256,
        "baseline_ref": baseline_ref,
        "baseline_dir": baseline_dir,
        "base_version": base_version,
        "runner": family,
        "runner_model": model,
        "runner_effort": effort,
        "rounds": rounds,
        "chunk_prompt_sha256": {
            str(index): prompt_sha256(prompt) for index, prompt in chunk_prompts.items()
        },
    }
    (root / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_and_load(root: Path, manifest: dict, round_index: int,
                     chunk_prompts: dict[int, str], family: str, model: str,
                     effort: str | None) -> dict[int, tuple[str, Path]]:
    """Return ``{chunk_index: (text, path)}`` for one bank round.

    Every check here is load-bearing, not defensive filler: a bank built under
    a different runner, model, effort, or prompt would silently answer a
    different question than the one this round is asking, and the whole point
    of freezing the baseline is that nobody re-reads it by hand each round to
    notice.
    """
    if manifest["runner"] != family or manifest["runner_model"] != model \
            or manifest.get("runner_effort") != effort:
        raise ScoreEvalsError(
            f"{root}: bank was built with runner={manifest['runner']} "
            f"model={manifest['runner_model']} effort={manifest.get('runner_effort')}, "
            f"this run wants runner={family} model={model} effort={effort} — "
            "rebuild the bank for this setup, or match the run to the bank's"
        )
    if not (1 <= round_index <= manifest["rounds"]):
        raise ScoreEvalsError(
            f"{root}: round {round_index} is out of range 1..{manifest['rounds']}"
        )
    out: dict[int, tuple[str, Path]] = {}
    for chunk_index, prompt in chunk_prompts.items():
        want = prompt_sha256(prompt)
        got = manifest["chunk_prompt_sha256"].get(str(chunk_index))
        if got != want:
            raise ScoreEvalsError(
                f"{root}: chunk {chunk_index}'s runner prompt no longer matches "
                "the bank (rule blob, chunk layout, or a case's prompt text "
                "changed since the bank was built) — rebuild with --build-bank"
            )
        path = chunk_out_path(root, round_index, chunk_index)
        if not path.exists():
            raise ScoreEvalsError(f"{root}: missing {path} for round {round_index}")
        out[chunk_index] = (path.read_text(encoding="utf-8"), path)
    return out


def pick_round(skill_dir: Path, base_blob_sha256: str, rounds: int) -> int:
    """The smallest bank round not already recorded as used by an existing
    results file for this baseline blob, so a branch's own multi-round series
    draws distinct baseline generations round to round.

    Reuse across *different* branches is deliberate and unrestricted — that is
    the savings this bank exists to produce — so this only ever looks at
    ``bank_round`` values already written into results files, never mutates
    anything itself.
    """
    used: set[int] = set()
    evals_dir = skill_dir / "evals"
    for path in sorted(evals_dir.glob("results-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        if data.get("baseline_source") != "bank":
            continue
        if data.get("base_blob_sha256") != base_blob_sha256:
            continue
        candidate = data.get("bank_round")
        if isinstance(candidate, int):
            used.add(candidate)
    for candidate in range(1, rounds + 1):
        if candidate not in used:
            return candidate
    raise ScoreEvalsError(
        f"all {rounds} bank round(s) already used by an existing results file "
        "for this baseline — pass --bank-round to reuse one deliberately, or "
        "rebuild the bank with more rounds (--build-bank --rounds N)"
    )

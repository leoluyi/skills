"""Score a skill's behaviour evals (``evals.json``) and report ship/no-ship.

Command-line layer: argument parsing, the prepare/materialize/execute pipeline
that drives the other modules in order, the dry-run summary, and the top-level
error handling that turns a ScoreEvalsError into a one-line message.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import itertools
import json
import secrets
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

from score_evals import bank
from score_evals.arms import (
    GRADER_BRIEF,
    arm_blob,
    arm_version,
    files_from_ref,
    files_from_worktree,
    grader_prompt,
    runner_prompt,
    write_arm,
)
from score_evals.config import (
    build_chunks,
    build_rows,
    criteria_section,
    load_config,
    load_fixture,
    resolve_ids,
    unscored_notes,
    validate_declared_ids,
)
from score_evals.aggregate import aggregate, aggregate_markdown, load_round
from score_evals.calibration import CALIBRATION_PATH, calibrate, calibrate_same_call
from score_evals.dispatch import (
    CLAUDE_MODEL,
    CODEX_EFFORT,
    CODEX_MODEL,
    DispatchError,
    grade_chunk,
    label_for_new,
    reconcile,
    run_pipeline,
    worker_failure,
)
from score_evals.errors import CONFIG_PATH, Chunk, Row, ScoreEvalsError
from score_evals.report import (
    chunk_table_lines,
    denominators,
    derivation_lines,
    report_markdown,
    verdict,
)
from score_evals.smoke import format_report, run_smoke, select_cases as smoke_select_cases

SMOKE_EFFORTS = ("low", "medium", "high", "xhigh")

FAMILIES = ("codex", "claude")


def prepare(args: argparse.Namespace, repo_root: Path) -> dict:
    """Load and validate everything that must hold before any dispatch."""
    skill_dir = repo_root / "skills" / args.skill
    if not skill_dir.is_dir():
        raise ScoreEvalsError(f"no such skill: {skill_dir}")
    config = load_config(skill_dir)
    if config is None:
        return {"opted_in": False, "skill_dir": skill_dir}
    cases = load_fixture(skill_dir)
    validate_declared_ids(cases, config)
    chunks = build_chunks(cases, config)
    criteria = criteria_section(skill_dir, config)
    rows = build_rows(cases, config)
    known = {case["id"] for case in cases}
    selected = resolve_ids(args.ids, known) if args.ids else None
    return {
        "opted_in": True,
        "skill_dir": skill_dir,
        "config": config,
        "cases": cases,
        "chunks": chunks,
        "criteria": criteria,
        "notes": unscored_notes(cases, config),
        "rows": rows,
        "selected": selected,
    }


def materialize(repo_root: Path, skill_dir: Path, config: dict, baseline: tuple[str, str]) -> dict:
    workspace = Path(tempfile.mkdtemp(prefix="score-evals-"))
    prefixes = config["skill_paths"]
    ref, base_dir = baseline
    # The new arm comes off the working tree on purpose: the version being
    # gated is the one on disk, including edits that are not committed yet.
    new_files = files_from_worktree(skill_dir, prefixes)
    base_files = files_from_ref(repo_root, ref, base_dir, prefixes)
    write_arm(workspace, "new", new_files)
    write_arm(workspace, "base", base_files)
    (workspace / "empty").mkdir(parents=True, exist_ok=True)
    return {
        "workspace": workspace,
        "new_files": new_files,
        "base_files": base_files,
        "new_version": arm_version(new_files),
        "base_version": arm_version(base_files),
    }


def chunk_row_map(chunks: tuple[Chunk, ...], rows: tuple[Row, ...],
                  selected: tuple[int, ...] | None) -> tuple[dict[int, tuple[Row, ...]], dict[int, tuple[int, ...]]]:
    chunk_rows, chunk_ids = {}, {}
    keep = set(selected) if selected is not None else None
    for index, chunk in enumerate(chunks):
        ids = tuple(i for i in chunk.case_ids if keep is None or i in keep)
        if not ids:
            continue
        chunk_ids[index] = ids
        chunk_rows[index] = tuple(row for row in rows if row.case_id in set(ids))
    if not chunk_rows:
        raise ScoreEvalsError("selection leaves no chunk to run")
    return chunk_rows, chunk_ids


def scoped_denominators(ctx: dict, chunk_rows: dict, chunk_ids: dict) -> dict:
    """Denominators over the rows this run scores, not the whole fixture."""
    if ctx["selected"] is None:
        return denominators(ctx["rows"], ctx["cases"], ctx["config"])
    ids = {case_id for index in chunk_ids for case_id in chunk_ids[index]}
    rows = tuple(row for index in sorted(chunk_rows) for row in chunk_rows[index])
    cases = tuple(case for case in ctx["cases"] if case["id"] in ids)
    return denominators(rows, cases, ctx["config"])


def discard_workspace(workspace: Path) -> None:
    """Remove the scratch workspace: it holds the full skill text plus every
    runner and grader output, and nothing downstream reads it after the run.
    """
    shutil.rmtree(workspace, ignore_errors=True)
    print(f"removed workspace {workspace}")


def dry_run_report(ctx: dict, arms: dict, dn: dict, baseline_source: str,
                   bank_round: int | None) -> None:
    print(f"skill: {ctx['skill_dir'].name}")
    print(f"workspace: {arms['workspace']}")
    print(
        f"base arm source: {baseline_source}"
        + (f" (round {bank_round})" if bank_round is not None else "")
    )
    print(f"new/  version {arms['new_version']} — {len(arms['new_files'])} file(s):")
    for rel, _ in arms["new_files"]:
        print(f"  {rel}")
    print(f"base/ version {arms['base_version']} — {len(arms['base_files'])} file(s):")
    for rel, _ in arms["base_files"]:
        print(f"  {rel}")
    print()
    for line in derivation_lines(dn, ctx["config"]):
        print(line)
    print()
    for line in ctx["chunk_lines"]:
        print(line)
    print()
    if ctx["selected"] is not None:
        print(
            f"partial selection: {len(ctx['selected'])} case id(s) — such a run "
            "refuses to write the .md report"
        )
    print("dry run: validated and materialized, dispatched nothing")


def execute(ctx: dict, arms: dict, args: argparse.Namespace, run_id: str,
            chunk_rows: dict, chunk_ids: dict,
            base_texts: dict[int, tuple[str, Path]] | None = None) -> tuple[dict, ...]:
    cases_by_id = {case["id"]: case for case in ctx["cases"]}
    # base_texts, when given, came from the bank: no base runner job is built
    # or dispatched, and its (text, path) pair is seeded straight into
    # run_pipeline as if that dispatch had already landed.
    dispatch_arms = ("new",) if base_texts is not None else ("new", "base")
    blobs = {"new": arm_blob(arms["new_files"])}
    if base_texts is None:
        blobs["base"] = arm_blob(arms["base_files"])
    plan = [
        {
            "family": args.runner, "arm": arm, "chunk": index,
            "workspace": arms["workspace"], "tag": f"runner-c{index}-{arm}",
            "prompt": runner_prompt(
                blobs[arm], tuple(cases_by_id[i] for i in chunk_ids[index])
            ),
        }
        for index in sorted(chunk_ids)
        for arm in dispatch_arms
    ]
    preseeded = (
        {(index, "base"): base_texts[index] for index in chunk_ids}
        if base_texts is not None else None
    )
    mapping = {index: label_for_new(run_id, index) for index in chunk_ids}
    # A nonce of its own, never derived from run_id: run_id decides the A/B
    # mapping, and the grader must not hold anything that could reconstruct it.
    nonce = secrets.token_hex(8)

    def grader_item(index: int, new_text: str, base_text: str) -> dict:
        first, second = (
            (new_text, base_text) if mapping[index] == "A" else (base_text, new_text)
        )
        sources = tuple(
            {
                "id": i,
                "prompt": cases_by_id[i]["prompt"],
                "notes": ctx["notes"].get(i, ()),
            }
            for i in chunk_ids[index]
        )
        return {
            "family": args.grader, "chunk": index, "workspace": arms["workspace"],
            "tag": f"grader-c{index}", "rows": chunk_rows[index], "nonce": nonce,
            "prompt": grader_prompt(
                ctx["criteria"], chunk_rows[index], sources, first, second, nonce
            ),
        }

    runner_out, graded = run_pipeline(plan, grader_item, args.jobs, preseeded=preseeded)
    ctx["mapping"] = mapping
    ctx["runner_paths"] = {
        f"c{index}-{arm}": str(path) for (index, arm), (_, path) in runner_out.items()
    }
    return reconcile(chunk_rows, graded, mapping)


def resolve_baseline_arm(ctx: dict, arms: dict, args: argparse.Namespace,
                         chunk_ids: dict[int, tuple[int, ...]]
                         ) -> tuple[dict[int, tuple[str, Path]] | None, str, int | None]:
    """Decide whether this round reads its base arm from the bank or dispatches
    it live, and return what ``execute`` and ``build_context`` need either way.

    ``--no-bank`` is the only silent-free way out: a missing or mismatched
    bank is a hard error with a rebuild instruction, never a fallback to a
    live dispatch chosen for you — that fallback would let a run's baseline
    source drift without anyone deciding it should.
    """
    if args.no_bank:
        return None, "live", None
    base_blob_sha256 = hashlib.sha256(arm_blob(arms["base_files"]).encode("utf-8")).hexdigest()
    root = bank.bank_dir(ctx["skill_dir"], base_blob_sha256)
    manifest = bank.load_manifest(root)
    if manifest is None:
        raise ScoreEvalsError(
            f"no baseline bank at {root} for this baseline text — build one "
            f"first: tools/score-evals {args.skill} --baseline {args.baseline} "
            "--build-bank, or pass --no-bank to dispatch a live baseline arm "
            "this round"
        )
    cases_by_id = {case["id"]: case for case in ctx["cases"]}
    base_blob = arm_blob(arms["base_files"])
    chunk_prompts = {
        index: runner_prompt(base_blob, tuple(cases_by_id[i] for i in chunk_ids[index]))
        for index in chunk_ids
    }
    round_index = args.bank_round or bank.pick_round(
        ctx["skill_dir"], base_blob_sha256, manifest["rounds"]
    )
    base_texts = bank.verify_and_load(
        root, manifest, round_index, chunk_prompts, args.runner,
        CODEX_MODEL if args.runner == "codex" else CLAUDE_MODEL,
        CODEX_EFFORT if args.runner == "codex" else None,
    )
    return base_texts, "bank", round_index


def incompatible_entries(config: dict, rows: tuple[Row, ...]) -> list[dict]:
    """Attribute each deducted row to exactly one entry.

    Entries may overlap; counting rows per entry independently would let the
    per-entry column sum past the single deduction the denominator applies.
    """
    claimed: set[int] = set()
    entries = []
    for entry in config["baseline_incompatible"]:
        ids = set(entry["ids"]) - claimed
        claimed |= set(entry["ids"])
        entries.append({
            "ids": entry["ids"],
            "reason": entry["reason"],
            "rows": sum(1 for row in rows if row.case_id in ids),
        })
    return entries


def build_context(args: argparse.Namespace, ctx: dict, arms: dict, dn: dict,
                  run_id: str, results: tuple[dict, ...], baseline: tuple[str, str],
                  baseline_source: str, bank_round: int | None) -> dict:
    incompatible = {i for e in ctx["config"]["baseline_incompatible"] for i in e["ids"]}
    entries = incompatible_entries(ctx["config"], ctx["rows"])
    return {
        "skill": args.skill,
        "date": datetime.date.today().isoformat(),
        "run_id": run_id,
        # "bank" means the base arm was read from evals/baseline-bank/ instead
        # of dispatched this round; bank_round is which of its rounds. Rounds
        # with different baseline_source, or a different bank_round drawn from
        # a live dispatch, never describe the same measurement setup.
        "baseline_source": baseline_source,
        "bank_round": bank_round,
        "null": False,
        "new_dir": str(ctx["skill_dir"]),
        "new_version": arms["new_version"],
        "new_files": len(arms["new_files"]),
        # The blob is the exact text the runner was given, so its hash is the
        # only honest answer to "did these rounds measure the same skill?".
        # A version string is a claim; an unbumped edit leaves it unchanged.
        "new_blob_sha256": hashlib.sha256(
            arm_blob(arms["new_files"]).encode("utf-8")
        ).hexdigest(),
        "baseline_ref": baseline[0],
        "baseline_dir": baseline[1],
        "base_version": arms["base_version"],
        "base_files": len(arms["base_files"]),
        "base_blob_sha256": hashlib.sha256(
            arm_blob(arms["base_files"]).encode("utf-8")
        ).hexdigest(),
        "runner": args.runner,
        "runner_model": CODEX_MODEL if args.runner == "codex" else CLAUDE_MODEL,
        # Reasoning effort is part of the measurement setup, same as the model
        # name: a run at "high" and a run at "xhigh" answered different
        # questions even though runner_model reads identical.
        "runner_effort": CODEX_EFFORT if args.runner == "codex" else None,
        "grader": args.grader,
        "grader_model": CODEX_MODEL if args.grader == "codex" else CLAUDE_MODEL,
        "grader_effort": CODEX_EFFORT if args.grader == "codex" else None,
        "grader_brief_sha256": hashlib.sha256(GRADER_BRIEF.encode("utf-8")).hexdigest(),
        # The criteria come from the working tree, so a run is only comparable
        # to another run that graded by the same rubric text.
        "criteria_sha256": hashlib.sha256(ctx["criteria"].encode("utf-8")).hexdigest(),
        "workspace": str(arms["workspace"]),
        "chunk_lines": ctx["chunk_lines"],
        "derivation": derivation_lines(dn, ctx["config"]),
        # denominators describes the rows this run actually scored; the
        # full-fixture figures sit beside it so a partial run's JSON never
        # reads as if it had scored the whole fixture.
        "denominators": ctx["dn_scoped"],
        "denominators_full_fixture": dn,
        "incompatible_entries": entries,
        "results": results,
        "verdict": verdict(results, incompatible),
        "mapping_label_of_new_arm": ctx["mapping"],
        "mapping_note": (
            "mapping_label_of_new_arm[chunk] is the label (A or B) the NEW arm "
            "wore in that chunk's grader prompt; the base arm wore the other"
        ),
        "runner_paths": ctx["runner_paths"],
        "partial": args.ids is not None,
    }


def write_outputs(report: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json_path = out_path.with_suffix(".json")
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {json_path}")
    if report["partial"]:
        print(
            f"partial run (--ids): refusing to write {out_path} — a partial score "
            "must never become a citable baseline"
        )
        return
    out_path.write_text(report_markdown(report) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("skill", nargs="?", help="skill slug under skills/")
    parser.add_argument(
        "--baseline", metavar="REF[:DIR]",
        help="git ref for the comparison arm, with an optional skill-dir override",
    )
    parser.add_argument(
        "--aggregate", nargs="+", metavar="RESULTS.json",
        help="score N completed rounds together instead of dispatching a new one",
    )
    parser.add_argument(
        "--calibrate", nargs="+", metavar="RESULTS.json",
        help="rewrite calibration.json from a pool of rounds: same-call "
             "(--null-run outputs) if every round in the pool is one, else "
             "cross-round (splitting the baseline arm against itself)",
    )
    parser.add_argument(
        "--build-bank", action="store_true",
        help="dispatch --rounds independent baseline-arm generations and "
             "store them in evals/baseline-bank/ for later rounds — on this "
             "branch or any other sharing the same baseline blob — to reuse "
             "instead of re-dispatching; dispatches nothing else",
    )
    parser.add_argument(
        "--rounds", type=int, default=6,
        help="rounds to build with --build-bank (default 6)",
    )
    parser.add_argument(
        "--null-run", metavar="A,B",
        help="score bank round A against bank round B in one blind grader "
             "call, no runner dispatch; writes a null-marked result meant "
             "for --calibrate, never for --aggregate",
    )
    parser.add_argument(
        "--null-sweep", type=int, nargs="?", const=0, metavar="N",
        help="score all C(N,2) pairs of the bank's first N rounds, in "
             "concurrent batches — the whole null pool --calibrate wants, "
             "in one command; omit N to sweep every round the bank holds. "
             "Skips pairs already scored against this bank, so re-running "
             "retries only what failed",
    )
    parser.add_argument(
        "--null-batch", type=int, default=5, metavar="N",
        help="pairs in flight at once under --null-sweep (default 5); each "
             "pair dispatches one grader call per chunk, so the wire sees "
             "N x chunks at a time — lower it if a provider starts throttling",
    )
    parser.add_argument(
        "--bank-round", type=int,
        help="pin the bank round used as this round's base arm (default: "
             "the smallest round not yet used by an existing results file "
             "for this baseline)",
    )
    parser.add_argument(
        "--no-bank", action="store_true",
        help="dispatch a live base arm instead of reading evals/baseline-bank/",
    )
    parser.add_argument(
        "--smoke", action="store_true",
        help="fast single-arm, absolute-judged inner loop over config's "
             "smoke_ids (or --ids): no baseline, no bank, no gate verdict, "
             "and nothing is ever written to evals/ — advisory only",
    )
    parser.add_argument(
        "--effort", choices=SMOKE_EFFORTS, default=None,
        help="codex reasoning effort for --smoke's runner and grader calls "
             "(default xhigh); has no meaning outside --smoke — the gate's "
             "effort is fixed by calibration, not a flag",
    )
    parser.add_argument("--ids", help="run a subset, e.g. 1-9,20; marks the run partial")
    parser.add_argument("--jobs", type=int, default=12, help="concurrency cap (default 12)")
    parser.add_argument("--runner", choices=FAMILIES, default="codex")
    parser.add_argument("--grader", choices=FAMILIES, help="default: codex, same as --runner")
    parser.add_argument("--out", help="report path (default skills/<skill>/evals/results-<date>-score-evals.md)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    modes = (
        bool(args.aggregate), bool(args.calibrate), args.build_bank,
        bool(args.null_run), args.null_sweep is not None, args.smoke,
    )
    if sum(modes) > 1:
        parser.error(
            "--aggregate, --calibrate, --build-bank, --null-run, --null-sweep "
            "and --smoke each dispatch (or score) a different thing; pick one"
        )

    if args.aggregate or args.calibrate:
        mode = "--aggregate" if args.aggregate else "--calibrate"
        conflicting = [
            name for name, value in (
                ("skill", args.skill), ("--baseline", args.baseline),
                ("--ids", args.ids), ("--out", args.out),
                ("--rounds", args.rounds != 6), ("--bank-round", args.bank_round),
                ("--no-bank", args.no_bank), ("--effort", args.effort),
            ) if value
        ]
        if conflicting:
            parser.error(
                f"{mode} scores rounds that already exist; it dispatches "
                f"nothing, so {', '.join(conflicting)} has no meaning here"
            )
        return args

    if args.build_bank:
        if args.skill is None or args.baseline is None:
            parser.error("--build-bank needs a skill slug and --baseline")
        conflicting = [
            name for name, value in (
                ("--ids", args.ids), ("--out", args.out),
                ("--bank-round", args.bank_round), ("--no-bank", args.no_bank),
                ("--effort", args.effort),
                # No dry-run preview exists for this mode — dispatch is the
                # entire point, so silently ignoring the flag would let it
                # look like a safe preview and dispatch for real instead.
                ("--dry-run", args.dry_run),
            ) if value
        ]
        if conflicting:
            parser.error(
                f"--build-bank dispatches baseline-only rounds; "
                f"{', '.join(conflicting)} has no meaning here"
            )
        if args.rounds < 1:
            parser.error(f"--rounds must be at least 1, got {args.rounds}")
        if args.jobs < 1:
            parser.error(f"--jobs must be at least 1, got {args.jobs}")
        return args

    if args.null_run:
        if args.skill is None or args.baseline is None:
            parser.error("--null-run needs a skill slug and --baseline (to locate the bank)")
        conflicting = [
            name for name, value in (
                ("--ids", args.ids), ("--out", args.out),
                ("--bank-round", args.bank_round), ("--no-bank", args.no_bank),
                ("--effort", args.effort),
                # --null-batch paces pairs, and this mode runs exactly one.
                ("--null-batch", args.null_batch != 5),
                # Same reasoning as --build-bank above: no dry-run preview
                # exists, so the flag must refuse rather than be swallowed.
                ("--dry-run", args.dry_run),
            ) if value
        ]
        if conflicting:
            parser.error(
                f"--null-run scores two bank rounds directly; "
                f"{', '.join(conflicting)} has no meaning here"
            )
        if args.jobs < 1:
            parser.error(f"--jobs must be at least 1, got {args.jobs}")
        # --grader, if given, is honored as-is; otherwise it is resolved once
        # the bank manifest names the runner family it was built with.
        return args

    if args.null_sweep is not None:
        if args.skill is None or args.baseline is None:
            parser.error("--null-sweep needs a skill slug and --baseline (to locate the bank)")
        conflicting = [
            name for name, value in (
                ("--ids", args.ids), ("--out", args.out),
                ("--bank-round", args.bank_round), ("--no-bank", args.no_bank),
                ("--effort", args.effort), ("--dry-run", args.dry_run),
            ) if value
        ]
        if conflicting:
            parser.error(
                f"--null-sweep scores bank rounds against each other; "
                f"{', '.join(conflicting)} has no meaning here"
            )
        # 0 is the "no count given" sentinel; the bank's own round count
        # stands in for it once the manifest is loaded.
        if args.null_sweep != 0 and args.null_sweep < 2:
            parser.error(
                f"--null-sweep needs at least 2 rounds to form a pair, got {args.null_sweep}"
            )
        if args.null_batch < 1:
            parser.error(f"--null-batch must be at least 1, got {args.null_batch}")
        if args.jobs < 1:
            parser.error(f"--jobs must be at least 1, got {args.jobs}")
        return args

    if args.smoke:
        if args.skill is None:
            parser.error("--smoke needs a skill slug")
        conflicting = [
            name for name, value in (
                ("--baseline", args.baseline), ("--out", args.out),
                ("--rounds", args.rounds != 6), ("--bank-round", args.bank_round),
                ("--no-bank", args.no_bank),
                ("--runner", args.runner != "codex"), ("--grader", args.grader),
            ) if value
        ]
        if conflicting:
            parser.error(
                f"--smoke always runs both arms on codex and writes nothing "
                f"to evals/; {', '.join(conflicting)} has no meaning here"
            )
        if args.jobs < 1:
            parser.error(f"--jobs must be at least 1, got {args.jobs}")
        args.effort = args.effort or "xhigh"
        return args

    if args.effort is not None:
        parser.error("--effort only has meaning under --smoke")

    if args.skill is None or args.baseline is None:
        parser.error("a skill slug and --baseline are required unless --aggregate is used")
    if args.grader is None:
        args.grader = "codex"
    if args.jobs < 1:
        parser.error(f"--jobs must be at least 1, got {args.jobs}")
    if args.bank_round is not None and args.bank_round < 1:
        parser.error(f"--bank-round must be at least 1, got {args.bank_round}")
    if args.bank_round is not None and args.no_bank:
        parser.error("--bank-round pins a bank round; --no-bank skips the bank entirely — pick one")
    return args


def run_aggregate(args: argparse.Namespace) -> int:
    rounds = tuple(load_round(Path(p)) for p in args.aggregate)
    null_rounds = [r for r in rounds if r.get("null")]
    if null_rounds:
        named = ", ".join(str(Path(r["source"]).name) for r in null_rounds)
        raise ScoreEvalsError(
            f"--aggregate: {named} — a --null-run result measures the noise "
            "floor, not a change; pass it to --calibrate instead"
        )
    agg = aggregate(rounds)
    print(aggregate_markdown(agg))
    return 0 if agg["verdict"] == "SHIP" else 1


def run_calibrate(args: argparse.Namespace) -> int:
    pool = tuple(load_round(Path(p)) for p in args.calibrate)
    is_null = [bool(r.get("null")) for r in pool]
    if all(is_null):
        table = calibrate_same_call(pool)
    elif any(is_null):
        raise ScoreEvalsError(
            "--calibrate: pool mixes --null-run results with normal ones — "
            "pass one kind only (same-call rounds calibrate together, cross-"
            "round rounds calibrate together, never both)"
        )
    else:
        table = calibrate(pool)
    CALIBRATION_PATH.write_text(
        json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {CALIBRATION_PATH} from {len(pool)} rounds")
    print(f"  base blob {table['base_blob_sha256'][:12]}, "
          f"criteria {(table['criteria_sha256'] or '')[:12]}")
    for key, entry in table["thresholds"].items():
        rounds_at, klass = key.split("/")
        print(f"  {rounds_at} rounds / {klass}: confirmed at {entry['confirm_at']}+, "
              f"blocks above {entry['confirmed_max']} confirmed row(s) "
              f"or a row margin above {entry['row_margin_max']:+d}")
    return 0


def parse_baseline(args: argparse.Namespace) -> tuple[str, str]:
    ref, _, base_dir = args.baseline.partition(":")
    if not ref:
        raise ScoreEvalsError(f"--baseline: no git ref in {args.baseline!r}")
    return ref, base_dir or f"skills/{args.skill}"


def run_build_bank(args: argparse.Namespace, repo_root: Path) -> int:
    ctx = prepare(args, repo_root)
    if not ctx["opted_in"]:
        print(f"{args.skill}: no {CONFIG_PATH} — not opted in, skipped")
        return 0
    baseline = parse_baseline(args)
    _, chunk_ids = chunk_row_map(ctx["chunks"], ctx["rows"], None)
    cases_by_id = {case["id"]: case for case in ctx["cases"]}
    base_files = files_from_ref(repo_root, baseline[0], baseline[1], ctx["config"]["skill_paths"])
    base_blob = arm_blob(base_files)
    base_blob_sha256 = hashlib.sha256(base_blob.encode("utf-8")).hexdigest()
    base_version = arm_version(base_files)
    chunk_prompts = {
        index: runner_prompt(base_blob, tuple(cases_by_id[i] for i in chunk_ids[index]))
        for index in chunk_ids
    }
    root = bank.bank_dir(ctx["skill_dir"], base_blob_sha256)
    model = CODEX_MODEL if args.runner == "codex" else CLAUDE_MODEL
    effort = CODEX_EFFORT if args.runner == "codex" else None
    bank.build(
        root, args.rounds, args.runner, model, effort, base_blob_sha256,
        baseline[0], baseline[1], base_version, chunk_prompts, args.jobs,
    )
    print(
        f"wrote baseline bank {root} — {args.rounds} round(s), "
        f"{len(chunk_prompts)} chunk(s), runner {args.runner} ({model}"
        + (f", effort {effort}" if effort else "") + ")"
    )
    return 0


def null_setup(args: argparse.Namespace, repo_root: Path) -> dict | None:
    """Everything a null comparison needs that does not depend on which pair
    is being scored: the fixture, the baseline blob, the chunk prompts, and
    the bank manifest. Hoisted out of the per-pair work because a sweep would
    otherwise redo it — including a git read per pair — once per pair rather
    than once per run. Returns None when the skill has not opted in.
    """
    ctx = prepare(args, repo_root)
    if not ctx["opted_in"]:
        print(f"{args.skill}: no {CONFIG_PATH} — not opted in, skipped")
        return None
    baseline = parse_baseline(args)

    chunk_rows, chunk_ids = chunk_row_map(ctx["chunks"], ctx["rows"], None)
    ctx["chunk_lines"] = chunk_table_lines(ctx["chunks"], chunk_rows, chunk_ids)
    cases_by_id = {case["id"]: case for case in ctx["cases"]}

    base_files = files_from_ref(repo_root, baseline[0], baseline[1], ctx["config"]["skill_paths"])
    base_blob = arm_blob(base_files)
    base_blob_sha256 = hashlib.sha256(base_blob.encode("utf-8")).hexdigest()
    chunk_prompts = {
        index: runner_prompt(base_blob, tuple(cases_by_id[i] for i in chunk_ids[index]))
        for index in chunk_ids
    }

    root = bank.bank_dir(ctx["skill_dir"], base_blob_sha256)
    manifest = bank.load_manifest(root)
    if manifest is None:
        raise ScoreEvalsError(
            f"no baseline bank at {root} — build one first: tools/score-evals "
            f"{args.skill} --baseline {args.baseline} --build-bank"
        )
    return {
        "ctx": ctx,
        "baseline": baseline,
        "chunk_rows": chunk_rows,
        "chunk_ids": chunk_ids,
        "cases_by_id": cases_by_id,
        "dn": denominators(ctx["rows"], ctx["cases"], ctx["config"]),
        "base_blob_sha256": base_blob_sha256,
        "base_version": arm_version(base_files),
        "chunk_prompts": chunk_prompts,
        "root": root,
        "manifest": manifest,
        "grader": args.grader or "codex",
    }


def bank_round_texts(setup: dict, round_index: int) -> dict:
    """Load and verify one bank round's chunk texts, memoized on the setup.

    A sweep reads each round once instead of twice per pair it appears in —
    2 x C(N,2) loads become N. The cache is filled before any thread starts,
    so concurrent pairs only ever read it.
    """
    cache = setup.setdefault("texts", {})
    if round_index not in cache:
        manifest = setup["manifest"]
        cache[round_index] = bank.verify_and_load(
            setup["root"], manifest, round_index, setup["chunk_prompts"],
            manifest["runner"], manifest["runner_model"], manifest.get("runner_effort"),
        )
    return cache[round_index]


def run_null(args: argparse.Namespace, repo_root: Path) -> int:
    try:
        round_a, round_b = (int(part.strip()) for part in args.null_run.split(","))
    except ValueError:
        raise ScoreEvalsError(
            f"--null-run wants 'A,B' (two bank round numbers), got {args.null_run!r}"
        ) from None
    if round_a == round_b:
        raise ScoreEvalsError(f"--null-run: rounds must differ, got {args.null_run!r} twice")
    setup = null_setup(args, repo_root)
    if setup is None:
        return 0
    return null_pair(setup, args, round_a, round_b)


def null_pair(setup: dict, args: argparse.Namespace, round_a: int, round_b: int) -> int:
    """Score one pair of bank rounds against each other. Shared by --null-run
    and --null-sweep. Reads from `setup` and writes nothing back to it beyond
    the memoized round texts, so concurrent pairs do not interfere.
    """
    ctx = setup["ctx"]
    baseline = setup["baseline"]
    chunk_rows, chunk_ids = setup["chunk_rows"], setup["chunk_ids"]
    cases_by_id = setup["cases_by_id"]
    dn = setup["dn"]
    base_blob_sha256 = setup["base_blob_sha256"]
    base_version = setup["base_version"]
    manifest = setup["manifest"]
    grader = setup["grader"]

    texts_a = bank_round_texts(setup, round_a)
    texts_b = bank_round_texts(setup, round_b)

    run_id = uuid.uuid4().hex
    workspace = Path(tempfile.mkdtemp(prefix="score-evals-null-"))
    # A wears the label the real gate's "new" arm would wear; B wears "base".
    # Both are baseline text, so this comparison's ground truth is known: any
    # row that reads as a regression here is the false-alarm rate itself.
    mapping = {index: label_for_new(run_id, index) for index in chunk_ids}
    nonce = secrets.token_hex(8)

    def grader_item(index: int) -> dict:
        a_text, _ = texts_a[index]
        b_text, _ = texts_b[index]
        first, second = (a_text, b_text) if mapping[index] == "A" else (b_text, a_text)
        sources = tuple(
            {"id": i, "prompt": cases_by_id[i]["prompt"], "notes": ctx["notes"].get(i, ())}
            for i in chunk_ids[index]
        )
        return {
            "family": grader, "chunk": index, "workspace": workspace,
            "tag": f"null-grader-c{index}", "rows": chunk_rows[index], "nonce": nonce,
            "prompt": grader_prompt(
                ctx["criteria"], chunk_rows[index], sources, first, second, nonce
            ),
        }

    jobs = [dict(grader_item(index), kind="grader") for index in sorted(chunk_ids)]
    graded: dict[int, tuple[dict, ...]] = {}
    errors: list[str] = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = {pool.submit(grade_chunk, job): job for job in jobs}
            for future in concurrent.futures.as_completed(futures):
                job = futures[future]
                try:
                    graded[job["chunk"]] = future.result()
                except DispatchError as exc:
                    errors.append(str(exc))
                except Exception as exc:  # noqa: BLE001 — see worker_failure
                    errors.append(worker_failure(job, exc))
    finally:
        discard_workspace(workspace)
    if errors:
        raise ScoreEvalsError("null-run grader dispatch failed:\n  " + "\n  ".join(sorted(errors)))

    results = reconcile(chunk_rows, graded, mapping)
    report = {
        "skill": args.skill,
        "date": datetime.date.today().isoformat(),
        "run_id": run_id,
        "null": True,
        "bank_round_a": round_a,
        "bank_round_b": round_b,
        "baseline_source": "bank",
        "bank_round": None,
        "baseline_ref": baseline[0],
        "baseline_dir": baseline[1],
        # Both labelled arms are baseline text — the null's whole premise —
        # so both blob hashes are the same base_blob_sha256 by construction,
        # not a coincidence to double-check.
        "new_version": base_version,
        "base_version": base_version,
        "new_blob_sha256": base_blob_sha256,
        "base_blob_sha256": base_blob_sha256,
        "runner": manifest["runner"],
        "runner_model": manifest["runner_model"],
        "runner_effort": manifest.get("runner_effort"),
        "grader": grader,
        "grader_model": CODEX_MODEL if grader == "codex" else CLAUDE_MODEL,
        "grader_effort": CODEX_EFFORT if grader == "codex" else None,
        "grader_brief_sha256": hashlib.sha256(GRADER_BRIEF.encode("utf-8")).hexdigest(),
        "criteria_sha256": hashlib.sha256(ctx["criteria"].encode("utf-8")).hexdigest(),
        "chunk_lines": ctx["chunk_lines"],
        "derivation": derivation_lines(dn, ctx["config"]),
        "denominators": dn,
        "denominators_full_fixture": dn,
        "incompatible_entries": incompatible_entries(ctx["config"], ctx["rows"]),
        "results": results,
        "mapping_label_of_new_arm": mapping,
        "mapping_note": (
            "mapping_label_of_new_arm[chunk] is the label bank round A wore "
            "in that chunk's grader prompt; bank round B wore the other"
        ),
        "runner_paths": {},
        "partial": False,
    }
    out_path = (
        ctx["skill_dir"] / "evals"
        / f"null-{report['date']}-r{round_a}v{round_b}-score-evals.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path}")
    return 0


def existing_null_pairs(skill_dir: Path, base_blob_sha256: str) -> set[tuple[int, int]]:
    """Pairs already scored against *this* bank. A null result names its pair
    in the filename but carries the blob it was measured on inside, and only
    the blob decides whether the result still describes the current bank — a
    same-named file from an older bank is not a pair that can be skipped.
    """
    done: set[tuple[int, int]] = set()
    for path in sorted((skill_dir / "evals").glob("null-*-score-evals.json")):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if report.get("base_blob_sha256") != base_blob_sha256:
            continue
        a, b = report.get("bank_round_a"), report.get("bank_round_b")
        if isinstance(a, int) and isinstance(b, int):
            done.add((min(a, b), max(a, b)))
    return done


def run_null_sweep(args: argparse.Namespace, repo_root: Path) -> int:
    """Score every pair of bank rounds, in concurrent batches.

    One --null-run per pair would serialize C(N,2) waves of a pool sized for
    chunks, so the pairs are what gets batched: --jobs still bounds the chunks
    inside a pair, and --null-batch bounds how many pairs are in flight, which
    together put batch x chunks dispatches on the wire at once.

    A pair that fails does not stop the sweep. Its siblings are independent
    measurements, and killing fourteen good pairs because a fifteenth hit a
    rate limit would waste the whole run; the failures are listed at the end
    and re-running the same command picks up only what is missing.
    """
    setup = null_setup(args, repo_root)
    if setup is None:
        return 0
    ctx, manifest = setup["ctx"], setup["manifest"]
    base_blob_sha256 = setup["base_blob_sha256"]
    # No count given: the bank knows how many rounds it holds, and asking the
    # caller to repeat it is only a way to get it wrong.
    rounds = args.null_sweep or manifest["rounds"]
    if rounds < 2:
        raise ScoreEvalsError(
            f"--null-sweep needs at least 2 bank rounds to form a pair, "
            f"but {setup['root']} holds {rounds}"
        )
    if manifest["rounds"] < rounds:
        raise ScoreEvalsError(
            f"--null-sweep {rounds} wants {rounds} bank rounds, but "
            f"{setup['root']} holds {manifest['rounds']}"
        )

    all_pairs = list(itertools.combinations(range(1, rounds + 1), 2))
    done = existing_null_pairs(ctx["skill_dir"], base_blob_sha256)
    pairs = [pair for pair in all_pairs if pair not in done]
    if done:
        print(f"skipping {len(done)} pair(s) already scored against this bank")
    if not pairs:
        print(f"all {len(all_pairs)} pair(s) already scored — nothing to do")
        return 0
    print(f"sweeping {len(pairs)} pair(s), {args.null_batch} in flight at a time")

    # Fill the round-text cache before any thread starts: after this the cache
    # is read-only, so the pairs need no lock around it.
    for round_index in sorted({r for pair in pairs for r in pair}):
        bank_round_texts(setup, round_index)

    # One pool over every pair, not a loop of per-batch pools. Batching with a
    # barrier would make each group wait on its slowest pair before the next
    # starts, which is the same stall --null-sweep exists to remove; a single
    # pool keeps --null-batch pairs in flight continuously as slots free.
    failures: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.null_batch) as pool:
        futures = {
            pool.submit(null_pair, setup, args, a, b): (a, b)
            for a, b in pairs
        }
        for future in concurrent.futures.as_completed(futures):
            a, b = futures[future]
            try:
                future.result()
            except Exception as exc:  # noqa: BLE001 — one pair must not sink the sweep
                failures.append(f"r{a}v{b}: {exc}")

    if failures:
        print(
            f"\n{len(failures)} of {len(pairs)} pair(s) failed; re-run the same "
            f"command to retry only these:",
            file=sys.stderr,
        )
        for line in sorted(failures):
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"\nswept {len(pairs)} pair(s) cleanly")
    return 0


def run_smoke_cli(args: argparse.Namespace, repo_root: Path) -> int:
    """The fast inner loop: one worktree arm, absolute judging, no baseline,
    no bank, no gate verdict, nothing written to evals/. See smoke.py.
    """
    skill_dir = repo_root / "skills" / args.skill
    if not skill_dir.is_dir():
        raise ScoreEvalsError(f"no such skill: {skill_dir}")
    config = load_config(skill_dir)
    if config is None:
        print(f"{args.skill}: no {CONFIG_PATH} — not opted in, skipped")
        return 0
    cases = load_fixture(skill_dir)
    validate_declared_ids(cases, config)
    if args.dry_run:
        selected = smoke_select_cases(cases, config, args.ids)
        print(f"skill: {args.skill}")
        print(f"effort: {args.effort}  jobs: {args.jobs}")
        print(f"selected case(s): {', '.join(str(c['id']) for c in selected)}")
        print("dry run: validated and selected, dispatched nothing")
        return 0
    report = run_smoke(repo_root, skill_dir, config, cases, args.ids, args.jobs, args.effort)
    print(format_report(report))
    return 0 if report["ok"] else 1


def run(args: argparse.Namespace, repo_root: Path) -> int:
    ctx = prepare(args, repo_root)
    if not ctx["opted_in"]:
        print(f"{args.skill}: no {CONFIG_PATH} — not opted in, skipped")
        return 0
    baseline = parse_baseline(args)
    chunk_rows, chunk_ids = chunk_row_map(ctx["chunks"], ctx["rows"], ctx["selected"])
    ctx["chunk_lines"] = chunk_table_lines(ctx["chunks"], chunk_rows, chunk_ids)
    dn = denominators(ctx["rows"], ctx["cases"], ctx["config"])
    ctx["dn_scoped"] = scoped_denominators(ctx, chunk_rows, chunk_ids)
    arms = materialize(repo_root, ctx["skill_dir"], ctx["config"], baseline)
    base_texts, baseline_source, bank_round = resolve_baseline_arm(ctx, arms, args, chunk_ids)
    if args.dry_run:
        # Deliberate: a dry run exists to be inspected, so its workspace stays.
        dry_run_report(ctx, arms, dn, baseline_source, bank_round)
        return 0
    try:
        run_id = uuid.uuid4().hex
        results = execute(ctx, arms, args, run_id, chunk_rows, chunk_ids, base_texts)
        report = build_context(
            args, ctx, arms, dn, run_id, results, baseline, baseline_source, bank_round
        )
        default_out = (
            ctx["skill_dir"] / "evals" / f"results-{report['date']}-score-evals.md"
        )
        write_outputs(report, Path(args.out) if args.out else default_out)
    finally:
        discard_workspace(arms["workspace"])
    gate = report["verdict"]
    reason = "; ".join(gate["reasons"]) or "protection-class false kills 0; hit-class did not regress"
    scope = " (partial run — not a citable verdict)" if report["partial"] else ""
    print(f"{'SHIP' if gate['ship'] else 'NO-SHIP'}{scope} — {reason}")
    return 0 if gate["ship"] else 1


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent.parent
    try:
        if args.aggregate:
            return run_aggregate(args)
        if args.calibrate:
            return run_calibrate(args)
        if args.build_bank:
            return run_build_bank(args, repo_root)
        if args.null_run:
            return run_null(args, repo_root)
        if args.null_sweep is not None:
            return run_null_sweep(args, repo_root)
        if args.smoke:
            return run_smoke_cli(args, repo_root)
        return run(args, repo_root)
    except ScoreEvalsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

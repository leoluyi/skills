"""Score a skill's behaviour evals (``evals.json``) and report ship/no-ship.

Command-line layer: argument parsing, the prepare/materialize/execute pipeline
that drives the other modules in order, the dry-run summary, and the top-level
error handling that turns a RunCaseError into a one-line message.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import secrets
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

from run_case import bank
from run_case.arms import (
    GRADER_BRIEF,
    arm_blob,
    arm_version,
    files_from_ref,
    files_from_worktree,
    grader_prompt,
    runner_prompt,
    write_arm,
)
from run_case.config import (
    build_chunks,
    build_rows,
    criteria_section,
    load_config,
    load_fixture,
    resolve_ids,
    unscored_notes,
    validate_declared_ids,
)
from run_case.aggregate import aggregate, aggregate_markdown, load_round
from run_case.calibration import CALIBRATION_PATH, calibrate, calibrate_same_call
from run_case.dispatch import (
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
from run_case.errors import CONFIG_PATH, Chunk, Row, RunCaseError
from run_case.report import (
    chunk_table_lines,
    denominators,
    derivation_lines,
    report_markdown,
    verdict,
)

FAMILIES = ("codex", "claude")


def prepare(args: argparse.Namespace, repo_root: Path) -> dict:
    """Load and validate everything that must hold before any dispatch."""
    skill_dir = repo_root / "skills" / args.skill
    if not skill_dir.is_dir():
        raise RunCaseError(f"no such skill: {skill_dir}")
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
    workspace = Path(tempfile.mkdtemp(prefix="run-case-"))
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
        raise RunCaseError("selection leaves no chunk to run")
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
        raise RunCaseError(
            f"no baseline bank at {root} for this baseline text — build one "
            f"first: tools/run-case {args.skill} --baseline {args.baseline} "
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
        "--bank-round", type=int,
        help="pin the bank round used as this round's base arm (default: "
             "the smallest round not yet used by an existing results file "
             "for this baseline)",
    )
    parser.add_argument(
        "--no-bank", action="store_true",
        help="dispatch a live base arm instead of reading evals/baseline-bank/",
    )
    parser.add_argument("--ids", help="run a subset, e.g. 1-9,20; marks the run partial")
    parser.add_argument("--jobs", type=int, default=12, help="concurrency cap (default 12)")
    parser.add_argument("--runner", choices=FAMILIES, default="codex")
    parser.add_argument("--grader", choices=FAMILIES, help="default: the family the runner is not")
    parser.add_argument("--allow-same-family", action="store_true")
    parser.add_argument("--out", help="report path (default skills/<skill>/evals/results-<date>-run-case.md)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    modes = (bool(args.aggregate), bool(args.calibrate), args.build_bank, bool(args.null_run))
    if sum(modes) > 1:
        parser.error(
            "--aggregate, --calibrate, --build-bank and --null-run each "
            "dispatch (or score) a different thing; pick one"
        )

    if args.aggregate or args.calibrate:
        mode = "--aggregate" if args.aggregate else "--calibrate"
        conflicting = [
            name for name, value in (
                ("skill", args.skill), ("--baseline", args.baseline),
                ("--ids", args.ids), ("--out", args.out),
                ("--rounds", args.rounds != 6), ("--bank-round", args.bank_round),
                ("--no-bank", args.no_bank),
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

    if args.skill is None or args.baseline is None:
        parser.error("a skill slug and --baseline are required unless --aggregate is used")
    if args.grader is None:
        args.grader = "claude" if args.runner == "codex" else "codex"
    if args.grader == args.runner and not args.allow_same_family:
        parser.error(
            f"runner and grader are both {args.runner}; cross-family grading is the "
            "default for a reason — pass --allow-same-family to override"
        )
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
        raise RunCaseError(
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
        raise RunCaseError(
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
        raise RunCaseError(f"--baseline: no git ref in {args.baseline!r}")
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


def run_null(args: argparse.Namespace, repo_root: Path) -> int:
    ctx = prepare(args, repo_root)
    if not ctx["opted_in"]:
        print(f"{args.skill}: no {CONFIG_PATH} — not opted in, skipped")
        return 0
    baseline = parse_baseline(args)
    try:
        round_a, round_b = (int(part.strip()) for part in args.null_run.split(","))
    except ValueError:
        raise RunCaseError(
            f"--null-run wants 'A,B' (two bank round numbers), got {args.null_run!r}"
        ) from None
    if round_a == round_b:
        raise RunCaseError(f"--null-run: rounds must differ, got {args.null_run!r} twice")

    chunk_rows, chunk_ids = chunk_row_map(ctx["chunks"], ctx["rows"], None)
    ctx["chunk_lines"] = chunk_table_lines(ctx["chunks"], chunk_rows, chunk_ids)
    dn = denominators(ctx["rows"], ctx["cases"], ctx["config"])
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
    manifest = bank.load_manifest(root)
    if manifest is None:
        raise RunCaseError(
            f"no baseline bank at {root} — build one first: tools/run-case "
            f"{args.skill} --baseline {args.baseline} --build-bank"
        )
    grader = args.grader or ("claude" if manifest["runner"] == "codex" else "codex")
    if grader == manifest["runner"] and not args.allow_same_family:
        raise RunCaseError(
            f"bank runner and grader are both {grader}; cross-family grading "
            "is the default for a reason — pass --allow-same-family to override"
        )

    texts_a = bank.verify_and_load(
        root, manifest, round_a, chunk_prompts,
        manifest["runner"], manifest["runner_model"], manifest.get("runner_effort"),
    )
    texts_b = bank.verify_and_load(
        root, manifest, round_b, chunk_prompts,
        manifest["runner"], manifest["runner_model"], manifest.get("runner_effort"),
    )

    run_id = uuid.uuid4().hex
    workspace = Path(tempfile.mkdtemp(prefix="run-case-null-"))
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
        raise RunCaseError("null-run grader dispatch failed:\n  " + "\n  ".join(sorted(errors)))

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
        / f"null-{report['date']}-r{round_a}v{round_b}-run-case.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path}")
    return 0


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
            ctx["skill_dir"] / "evals" / f"results-{report['date']}-run-case.md"
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
        return run(args, repo_root)
    except RunCaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

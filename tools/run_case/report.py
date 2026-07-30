"""Scoring and reporting: derive the two denominators, decide the ship gate,
and render the markdown report.
"""

from __future__ import annotations

from run_case.errors import CLASSES, HIT, PROTECTION, Chunk, Row


def denominators(rows: tuple[Row, ...], cases: tuple[dict, ...], config: dict) -> dict:
    raw = sum(len(case["expectations"]) for case in cases)
    unscored = raw - sum(1 for row in rows if row.origin == "eval")
    globals_ = sum(1 for row in rows if row.origin == "global")
    incompatible_ids = sorted({i for e in config["baseline_incompatible"] for i in e["ids"]})
    deducted = sum(1 for row in rows if row.case_id in set(incompatible_ids))
    return {
        "raw": raw,
        "unscored": unscored,
        "global": globals_,
        "absolute": len(rows),
        "deducted": deducted,
        "comparative": len(rows) - deducted,
        "incompatible_ids": incompatible_ids,
    }


def derivation_lines(dn: dict, config: dict) -> list[str]:
    prefixes = ", ".join(config["unscored_slug_prefixes"]) or "none"
    checks = len(config["global_rewrite_checks"])
    cases = len(config["rewrite_case_ids"])
    return [
        f"absolute denominator: {dn['raw']} − {dn['unscored']} + {dn['global']} = {dn['absolute']}",
        f"  {dn['raw']} raw expectations in evals.json",
        f"  − {dn['unscored']} unscored (slug prefix: {prefixes})",
        f"  + {dn['global']} global rewrite rows ({cases} rewrite case(s) × {checks} check(s))",
        f"comparative denominator: {dn['absolute']} − {dn['deducted']} = {dn['comparative']}",
        f"  − {dn['deducted']} rows on baseline-incompatible ids {dn['incompatible_ids']}",
    ]


def chunk_table_lines(chunks: tuple[Chunk, ...], chunk_rows: dict[int, tuple[Row, ...]],
                      chunk_ids: dict[int, tuple[int, ...]]) -> list[str]:
    """Table the chunks that will actually run, so --ids never overstates it."""
    lines = ["| chunk | range | cases | ids | rows |", "|---|---|---|---|---|"]
    for index in sorted(chunk_ids):
        chunk = chunks[index]
        ids = ", ".join(str(i) for i in chunk_ids[index])
        lines.append(
            f"| {index} | [{chunk.lo}, {chunk.hi}] | {len(chunk_ids[index])} | "
            f"{ids} | {len(chunk_rows[index])} |"
        )
    return lines


def verdict(results: tuple[dict, ...], incompatible: set[int]) -> dict:
    protection_fails = [
        r for r in results if r["class"] == PROTECTION and r["new"] == "fail"
    ]
    new_hit_fails = [
        r for r in results
        if r["class"] == HIT and r["new"] == "fail" and r["case_id"] not in incompatible
    ]
    base_hit_fails = [
        r for r in results
        if r["class"] == HIT and r["base"] == "fail" and r["case_id"] not in incompatible
    ]
    reasons = []
    if protection_fails:
        named = [f"{r['case_id']}/{r['expectation']}" for r in protection_fails[:8]]
        rest = len(protection_fails) - len(named)
        listed = ", ".join(named) + (f", and {rest} more" if rest else "")
        reasons.append(f"{len(protection_fails)} protection-class false kill(s) on the new arm: {listed}")
    if len(new_hit_fails) > len(base_hit_fails):
        reasons.append(
            f"hit-class regressed: new arm {len(new_hit_fails)} failure(s) vs "
            f"baseline {len(base_hit_fails)} (comparative denominator)"
        )
    return {
        "ship": not reasons,
        "reasons": reasons,
        "protection_failures_new": len(protection_fails),
        "hit_failures_new": len(new_hit_fails),
        "hit_failures_base": len(base_hit_fails),
    }


def class_counts(results: tuple[dict, ...]) -> list[str]:
    lines = ["| class | arm | pass | total |", "|---|---|---|---|"]
    for klass in CLASSES:
        subset = [r for r in results if r["class"] == klass]
        for arm in ("new", "base"):
            passes = sum(1 for r in subset if r[arm] == "pass")
            lines.append(f"| {klass} | {arm} | {passes} | {len(subset)} |")
    return lines


def _header_lines(ctx: dict) -> list[str]:
    """Instrument facts first: nobody can compare two runs without them."""
    return [
        f"# run-case — {ctx['skill']} — {ctx['date']}",
        "",
        f"- run id: `{ctx['run_id']}`",
        f"- new arm: working tree `{ctx['new_dir']}`, version {ctx['new_version']}, "
        f"{ctx['new_files']} file(s)",
        f"- base arm: `{ctx['baseline_ref']}:{ctx['baseline_dir']}`, version "
        f"{ctx['base_version']}, {ctx['base_files']} file(s)",
        f"- runner: {ctx['runner']} ({ctx['runner_model']})",
        f"- grader: {ctx['grader']} ({ctx['grader_model']})",
        f"- grader brief sha256: `{ctx['grader_brief_sha256']}`",
        f"- grading criteria sha256: `{ctx['criteria_sha256']}`",
        f"- scratch workspace (removed after the run): `{ctx['workspace']}`",
    ]


def report_markdown(ctx: dict) -> str:
    dn, results = ctx["denominators"], ctx["results"]
    non_green = [r for r in results if "fail" in (r["new"], r["base"])]
    disagreed = [r for r in results if not r["class_read_agrees"]]
    lines = [
        *_header_lines(ctx),
        "",
        "## Chunks",
        "",
        *ctx["chunk_lines"],
        "",
        "## Denominators",
        "",
        "```",
        *ctx["derivation"],
        "```",
        "",
        "## baseline_incompatible deductions",
        "",
        "| ids | rows deducted | reason |",
        "|---|---|---|",
    ]
    for entry in ctx["incompatible_entries"]:
        lines.append(f"| {list(entry['ids'])} | {entry['rows']} | {entry['reason']} |")
    lines += [
        "", "## Per-class pass counts (absolute denominator)", "",
        *class_counts(results), "",
        "## Non-green rows", "",
    ]
    lines += _rows_block(non_green)
    lines += ["", "## class_read disagreements", ""]
    lines += _disagreement_block(disagreed)
    gate = ctx["verdict"]
    lines += [
        "", "## Gate", "",
        f"- protection-class failures, new arm (absolute {dn['absolute']}): "
        f"{gate['protection_failures_new']}",
        f"- hit-class failures, new arm (comparative {dn['comparative']}): "
        f"{gate['hit_failures_new']}",
        f"- hit-class failures, base arm (comparative {dn['comparative']}): "
        f"{gate['hit_failures_base']}",
        "",
        f"{'SHIP' if gate['ship'] else 'NO-SHIP'} — "
        + ("; ".join(gate["reasons"]) if gate["reasons"]
           else "protection-class false kills 0; hit-class did not regress"),
        "",
    ]
    return "\n".join(lines)


def _rows_block(rows: list[dict]) -> list[str]:
    if not rows:
        return ["None."]
    out = ["| case | expectation | class | new | base | grader reason |", "|---|---|---|---|---|---|"]
    for row in rows:
        reason = row["reason"].replace("|", "｜").replace("\n", " ")
        out.append(
            f"| {row['case_id']} | {row['expectation']} | {row['class']} | "
            f"{row['new']} | {row['base']} | {reason} |"
        )
    return out


def _disagreement_block(rows: list[dict]) -> list[str]:
    if not rows:
        return ["None."]
    out = ["| case | expectation | tool class | grader class_read |", "|---|---|---|---|"]
    for row in rows:
        out.append(
            f"| {row['case_id']} | {row['expectation']} | {row['class']} | "
            f"{row['class_read'] or '(none)'} |"
        )
    return out

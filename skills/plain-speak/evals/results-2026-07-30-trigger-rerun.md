# Trigger-layer rerun — 2026-07-30

**Type:** trigger-layer health check (`tools/run-eval` against `evals/trigger-queries.json`),
not a content-quality run. Exists to close the backlog item recorded when the
description extractor was fixed: any pass rate recorded before 2026-07-19 was
measured against a truncated `description: >-` (the extractor fed the router the
literal string `>-`, so it guessed from the skill name alone). This skill uses
`description: >-`, so its prior numbers, if any existed, would have been void.

**Method:** `./tools/run-eval plain-speak`, router = `claude` (CLI-login path,
`ANTHROPIC_API_KEY` dropped for the subprocess per the tool's own note).

**Result:** 17/17 — `agent: claude   total: 17   pass: 17   fail: 0   error: 0`.
11 positive cases (single-term, rewrite-passage, explain-for-pm, explain-error,
exec-summary-prep, named-listener, review-draft ×2, recall-previous-answer ×2,
recall-pending-question), all correctly triggering; 6 negative cases (routes to
humanizer-zh, formal-doc-structure, rfp-writing, deep-technical-answer,
casual-chat, deeper-technical-not-lowering), all correctly not triggering.

**Disposition:** trigger layer confirmed sound against the fixed extractor. No
rule or description change needed.

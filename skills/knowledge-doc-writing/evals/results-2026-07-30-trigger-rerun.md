# Trigger-layer rerun — 2026-07-30

**Type:** trigger-layer health check (`tools/run-eval` against `evals/trigger-queries.json`),
not a content-quality run. This skill's trigger layer had never actually been
verified: `trigger-queries.json` was authored fresh during the 2026-07-19
eval-layout migration (this skill had no real trigger file before), and any pass
rate recorded before that date would have been measured against a truncated
`description: >-` (the extractor fed the router the literal string `>-`, so it
guessed from the skill name alone).

**Method:** `./tools/run-eval knowledge-doc-writing`, router = `claude`
(CLI-login path, `ANTHROPIC_API_KEY` dropped for the subprocess per the tool's
own note).

**Result:** 17/17 — `agent: claude   total: 17   pass: 17   fail: 0   error: 0`.
7 positive cases (ids 1-7) and 10 negative cases (ids 8-17: routes to
formal-doc-structure ×2, rfp-writing, humanizer-zh ×2, plain-speak,
learn-loop-interactive ×2, mechanical-doc-gen, casual-chat — the skill's
documented exclusions), all correct.

**Disposition:** trigger layer confirmed sound on its first real run. No rule or
description change needed.

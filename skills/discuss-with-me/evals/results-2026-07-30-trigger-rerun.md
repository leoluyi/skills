# Trigger-layer rerun — 2026-07-30 (dual-CLI)

**Type:** trigger-layer health check (`tools/run-eval` against
`evals/trigger-queries.json`), not the content-quality dual run recorded in
`results-2026-07-30.md` (that file's cases 1-8 are `evals.json`'s A/B content
cases — a different file, a different question). This run exists to close a
specific incident: the same day's trigger rerun logged cases 9-16 failing with
`run-eval: claude -p produced no parseable TRIGGER/NONE decision.`, and it was
unclear whether that was a one-off CLI session problem or a router-path
regression.

**Method:** `./tools/run-eval discuss-with-me` twice — once with the default
`claude` router, once with `RUN_EVAL_AGENT=codex` after fixing several latent
defects in the codex branch: unpinned model/effort (and no
`--ignore-user-config`, so a local `$CODEX_HOME/config.toml` default silently
wins over an explicit `-m`/`-c` pin); no working-directory handling, so any
invocation from outside the repo failed outright; stderr discarded, so a
failure carried no diagnostic; and, once stderr was captured, the diagnostic
still printed the CLI's own startup banner instead of the actual error,
because it took the first 200 bytes of stderr rather than the tail where
`codex exec` actually writes failures. See `tools/run-eval`'s codex branch
comments for the verified detail on each.

**Result:** both routers pass all 16 cases, case-by-case identical:

`agent: claude  total: 16  pass: 16  fail: 0  error: 0`
`agent: codex   total: 16  pass: 16  fail: 0  error: 0`

9 positive cases (ids 1-9: explicit-both-unsure ×2 [zh-tw/en], unsettled-decision,
challenge-request, stress-test, red-team, poke-holes, converging-too-fast,
falsifier-request) and 7 negative cases (ids 10-16: answer-already-settled,
doc-writing, settled-concept, factual-lookup, debugging, plain-language-review,
uncertainty-but-checkable), all correct on both CLIs.

**Disposition:** the 2026-07-30 9-16 failure was a one-off `claude -p` session
problem, not a router-path regression — a clean rerun on the same router
passes, and an independent CLI (codex) agrees case-by-case. No rule or
description change needed. The codex-branch fixes are a standing improvement:
this is the first time that branch has actually been exercised and shown to
agree with the claude branch, which is what makes dual-CLI cross-verification
usable for future incidents of this shape.

# Skills backlog — repo 層

Repo-wide and `tools/` work. A single skill's own items live in `skills/<name>/backlog.md`.

Signal: friction hit 2+ times. Closed items do not stay here — provenance lives in commit
messages, each skill's `design-notes.md`, and `evals/results-*.md`.

## Measurement infrastructure

The whole repo's ship gate is written against `evals.json`, and **nothing runs it**.
`tools/run-eval` only exercises `trigger-queries.json` (whether the router fires). Every
content-quality round so far has been hand-composed: 6 runner + 6 grader agents for the
87/88 baseline, 8 more for the 2.0.0 round, scored with throwaway scripts. Each fix round
pays that tax again, which is why these three sit above every skill-level item.

- [ ] **`tools/run-case` — dispatch runner + grader over `evals.json` / `corpus.md`.** The
  protocol is already proven by hand and should be baked in rather than re-derived each
  round: **blind runner** (loads the skill's `SKILL.md` + all `references/`, must not open
  `evals/`; case input extracted to prompt-only, expectations withheld), **separated
  graders** (one per chunk, gets only that chunk's runner output and that chunk's key —
  no skill, no `results-*.md`), and **denominator reconciliation** printed with the score.
  One lesson to encode: the grader brief must match `regression-protocol.md`'s stated bar
  and nothing stricter — the 2.0.0 round's deliberately-strict first brief scored 80/88
  where the neutral brief scored 83/88, and the two rounds were then incomparable to the
  baseline. Wants per-chunk parallel dispatch (the shape the two hand rounds converged on),
  not a single-shot pair.

- [ ] **`tools/annotate` — yes/no adjudication helper for eval cases.** Wanted 2026-07-30,
  straight out of the session that found it. When a run disagrees with the key, the fastest
  way to settle it turned out not to be reading rule text — it was showing the author the raw
  sentence and asking 「這句有沒有 AI 味？」 with two buttons. Four such questions overturned
  three cases in one round, where two rounds of rule-wording argument had settled nothing.
  The tool should: pull a case's quoted span out of `evals.json`, present span + genre + one
  line of context (never the expectation, never the rule name — those bias the answer), take
  有/沒有, and write the verdict plus a one-line rationale into `evals/judged-cases.md` as
  品味層 語料, flagging any case whose verdict now contradicts its `expected-direction`. Runs
  over a filtered set (a whole id range, or only cases that failed a given run). Dev-side,
  `uv` fine, never part of skill runtime.

- [ ] **`tools/add-case` — append a judged case in the frozen format without hand-editing
  JSON.** Lowest of the three in value, and the one most likely to be unnecessary once
  `annotate` exists.

- [ ] **`check-labels` has no equivalent gate for skills other than humanizer-zh.**
  Found 2026-07-30 while wiring it into CI (`.github/workflows/humanizer-zh-labels.yml`, a
  separate workflow file rather than a second job in `docs-check.yml` — GitHub Actions applies
  `on.paths` at the whole-workflow level, not per-job, so a second job in that file would still
  run, and could block, on a catalog-only PR that never touches humanizer-zh). The tool
  hard-depends on `references/zh-rules.md`, `references/hidden-author.md`, and
  `evals/corpus.md` — no other skill has these, so running it against one fails with
  `missing rule file` (exit 2), not a clean skip. Worth deciding whether a second skill ever
  grows a `corpus.md` in this same shape, or whether label hygiene for everyone else needs a
  different, lighter check.

## `tools/run-eval`

`RUN_EVAL_AGENT=codex` is now a real second router, not just a documented option — it had never
actually been exercised. Fixed 2026-07-30, all verified live against a real `codex` install:
model/effort were unpinned and silently overridable by `$CODEX_HOME/config.toml` (fixed with
`-m`/`-c model_reasoning_effort` plus `--ignore-user-config`, the flag that actually makes a
pin authoritative); it broke outright when invoked from outside the repo (fixed with
`-C "$REPO_ROOT"`, `--skip-git-repo-check` kept as a fallback); stderr was discarded on failure,
and once captured, a first-review fix that copied the `claude` branch's `head`-based snippet
still printed only `codex exec`'s startup banner, never the actual error, because the real
failure sits at the *tail* of stderr, not the head (fixed, verified against a real invalid-model
error); and it had no `ANTHROPIC_API_KEY`-style env-drop for policy parity with the claude
branch's "never a billed API call" stance (added `env -u OPENAI_API_KEY` defensively — not
reproduced as a live failure on this CLI's ChatGPT-login mode, but zero-cost and the failure
mode, if it exists elsewhere, would be silent). Verified against `discuss-with-me`'s 16-case
trigger set from both inside and outside the repo — both routers agree case-by-case
(`evals/results-2026-07-30-trigger-rerun.md` in that skill's dir). This is now the tool to reach
for whenever a run-eval failure needs to be told apart from a genuine router regression, rather
than re-running the same CLI and hoping.

## Per-skill backlogs

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — 2.0.0's ship path, and the instrument defects under it
- [`skills/avoid-china-writing/backlog.md`](skills/avoid-china-writing/backlog.md) — one missing eval axis
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice profile
- [`skills/infographic-design/backlog.md`](skills/infographic-design/backlog.md) — negation in `references/`
- [`skills/knowledge-doc-writing/backlog.md`](skills/knowledge-doc-writing/backlog.md) — no open items
- [`skills/plain-speak/backlog.md`](skills/plain-speak/backlog.md) — real transcripts needed for two untestable-by-prompt behaviours

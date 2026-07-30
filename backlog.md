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

- [ ] **Wire `tools/check-labels` into `docs-check.yml`.** It validates every rule label
  against the names the skill actually declares, plus the corpus 解析契約, and is
  regression-tested against six injected fault classes (unresolvable name, non-substring
  引文片段, invalid 判定, a purely parenthetical `（缺口` label, an invented sub-signal under a
  real parent, a malformed judgment row). Today it gates only when run by hand.

## `tools/run-eval`

- [ ] **`jq -r '.expected_trigger // .should_trigger'` treats `false` as absent.** Found
  2026-07-28; latent, not live — every `trigger-queries.json` in the repo uses
  `should_trigger`. jq's `//` falls through whenever the left side is `false`, not just
  `null`, so a fixture using the newer `expected_trigger` key (which the script's own usage
  comment says it supports) would read as `null` → every negative case FAILs forever, with no
  error surfaced. Fix: `if has("expected_trigger") then .expected_trigger else .should_trigger end`.

- [ ] **`discuss-with-me` cases 9–16 errored with "not logged into claude.ai via the CLI".**
  Noted 2026-07-30 while shipping that skill's 0.2.0 (`main` renamed it from
  `open-question-loop`). Cases 1–8 passed; 9–16 all failed with `run-eval: claude -p produced
  no parseable TRIGGER/NONE decision.` A different symptom from the 2026-07-28
  `ANTHROPIC_API_KEY` credit-exhaustion bug (that one silently swallowed "Credit balance is
  too low"; this is a plain login-state message) — either a genuinely expired CLI session, or
  that same failure mode surfacing new diagnostic text after the `env -u ANTHROPIC_API_KEY`
  fix. Needs a clean rerun with `claude /login` state confirmed, to tell a one-off session
  hiccup from a router-path regression.

## Per-skill backlogs

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — 2.0.0's ship path, and the instrument defects under it
- [`skills/avoid-china-writing/backlog.md`](skills/avoid-china-writing/backlog.md) — one missing eval axis
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice profile
- [`skills/infographic-design/backlog.md`](skills/infographic-design/backlog.md) — negation in `references/`
- [`skills/knowledge-doc-writing/backlog.md`](skills/knowledge-doc-writing/backlog.md) — trigger layer never verified
- [`skills/plain-speak/backlog.md`](skills/plain-speak/backlog.md) — two behaviours a single-prompt harness can't reach

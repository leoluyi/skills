# Skills backlog — repo 層

Repo-wide and `tools/` work. A single skill's own items live in `skills/<name>/backlog.md`.

Signal: friction hit 2+ times. Closed items do not stay here — provenance lives in commit
messages, each skill's `design-notes.md`, and `evals/results-*.md`.

## Measurement infrastructure

The whole repo's ship gate is written against `evals.json`, and **nothing runs it**.
`tools/run-eval` only exercises `trigger-queries.json` (whether the router fires). Every
content-quality round so far has been hand-composed: 6 runner + 6 grader agents for the
87/88 baseline, 8 more for the 2.0.0 round, scored with throwaway scripts. Each fix round
pays that tax again, which is why `run-case` sits above every skill-level item.

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

- [ ] **`tools/add-case` — append a judged case in the frozen format without hand-editing
  JSON.** Lowest in value of the tools proposed so far, and the one most likely to be
  unnecessary once `annotate` exists — that item now lives in
  [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md), since the 有/沒有 question
  it asks is that skill's judgment call. This one stays repo-level: `evals/judged-cases.md`
  exists under `infographic-design` too, so the append format is not one skill's.

- [ ] **Nobody but humanizer-zh has opted into `check-labels`.** The tool stopped being
  humanizer-specific on 2026-07-30 — it now reads `skills/<name>/evals/label-check.json` for
  where a skill's rule names live, skips any skill without that file, and CI
  (`.github/workflows/eval-labels.yml`) runs `--all` over `skills/**`. So the mechanism exists
  and the open question is narrower: which other skills actually want label hygiene gated.
  `infographic-design` is the near candidate — it has `evals/judged-cases.md` but no rule
  taxonomy to resolve labels against, so opting it in means deciding what its canonical names
  even are. Don't opt a skill in just because it can be.

## Per-skill backlogs

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — 2.0.0's ship path, the instrument defects under it, and `tools/annotate`
- [`skills/avoid-china-writing/backlog.md`](skills/avoid-china-writing/backlog.md) — one missing eval axis
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice profile
- [`skills/infographic-design/backlog.md`](skills/infographic-design/backlog.md) — negation in `references/`
- [`skills/knowledge-doc-writing/backlog.md`](skills/knowledge-doc-writing/backlog.md) — no open items
- [`skills/plain-speak/backlog.md`](skills/plain-speak/backlog.md) — real transcripts needed for two untestable-by-prompt behaviours

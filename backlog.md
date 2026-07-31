# Skills backlog — repo 層

Repo-wide and `tools/` work. A single skill's own items live in `skills/<name>/backlog.md`.

Signal: friction hit 2+ times. Closed items do not stay here — provenance lives in commit
messages, each skill's `design-notes.md`, and `evals/results-*.md`.

## Measurement infrastructure

`tools/run-eval` exercises `trigger-queries.json` (whether the router fires);
`tools/run-case` scores the behaviour layer against `evals.json`. A skill opts into the
latter by shipping `evals/run-case.json`.

`corpus.md` is still hand-run — `run-case` reads `evals.json` only, and the corpus's
judgment-table format is a different parse. Whether that is worth automating depends on
whether the corpus stays a regression guard (see the saturation item in
[`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md)); a saturated fixture
does not earn a harness.

- [ ] **`tools/run-eval` redacts its stderr tail in the wrong order.** `tools/run-eval:190-193`
  pipes `tail -c 400 | sed` — it slices the window *before* redacting, so a key straddling the
  cut loses its `sk-` prefix and the surviving suffix prints verbatim. Found while reviewing
  `run-case`, which had the identical bug and now sanitizes first, then tails. Left unfixed
  there deliberately: it is a different tool, and folding a silent one-line security fix into
  an unrelated change is how such fixes escape review. Low severity — dev-side diagnostics
  only — but it is a one-line reorder.

- [ ] **`tools/run-case` leaves the grader's A/B labels unresolved in the Markdown report.** The
  non-green table gives resolved `new`/`base` verdict columns, but the grader-reason text beside
  them still says "A does X, B does Y" — and the A/B mapping is per-chunk, keyed on
  `sha256(run_id + chunk)`, so the reader cannot tell which arm a reason describes without
  opening the `.json`. Anonymity is the point *during* grading; keeping it *after* just makes the
  most useful column unreadable. Fix: substitute the resolved arm names into the reason string
  when rendering the Markdown, leaving the raw A/B text in the `.json` for audit.

- [ ] **`tools/run-case` is silent for its whole dispatch phase.** Between the prepare lines and
  the final verdict it prints nothing — `dispatch.py` has no output at all — so a 20-minute run
  is a black box, and the only way to read progress is to count `raw/*.out` against the expected
  12 runner + 6 grader jobs. Fix: emit one line per job completion to **stderr**, not stdout
  (stdout is the result surface; `--dry-run`'s output has to stay parseable), carrying a
  `[n/total]` counter and the job tag. `print(..., flush=True)` is load-bearing — redirected to a
  file, Python block-buffers, so an unflushed progress line is still invisible until exit. The
  counter needs a lock or `as_completed` sequencing, since the pool runs `--jobs` wide.

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

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — 2.0.0's ship path, the instrument defects under it, and `tools/annotate` (now also the blind human-vs-AI judgment harness)
- [`skills/avoid-china-writing/backlog.md`](skills/avoid-china-writing/backlog.md) — one missing eval axis
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice profile
- [`skills/infographic-design/backlog.md`](skills/infographic-design/backlog.md) — negation in `references/`
- [`skills/knowledge-doc-writing/backlog.md`](skills/knowledge-doc-writing/backlog.md) — no open items
- [`skills/plain-speak/backlog.md`](skills/plain-speak/backlog.md) — real transcripts needed for two untestable-by-prompt behaviours

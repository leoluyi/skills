# knowledge-doc-writing backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

- [ ] **The trigger layer has never actually been verified.** Two overlapping reasons, one
  rerun clears both:
  - `trigger-queries.json` was authored fresh during the 2026-07-19 eval-layout migration —
    this skill had no real trigger file before (its old `prompts.json` was content-quality
    material mislabeled), so its 6 negative queries came from `SKILL.md`'s documented exclusions
    rather than being carried over from a run.
  - Any pass rate recorded before 2026-07-19 was measured against a truncated description:
    `tools/run-eval`'s extractor only handled single-line YAML scalars, so for a skill using
    `description: >-` it fed the router the literal string `>-` and the router guessed from the
    skill name alone. The extractor is fixed; this skill has not been rerun since.
    (`blog-writing-zh` 12/12 and `briefing-outline` 10/10 came back clean on the same sweep;
    `plain-speak` is the other one still outstanding.)

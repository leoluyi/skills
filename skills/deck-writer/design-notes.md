# Deck Writer Design Notes

## Provenance

Requested import source: `leoluyi/social-image-kit/.agents/skills/deck-writer` at commit `ad7cfbbf9d47d4dede1dafd1b41782cc4e2f7327`.

The source repository had no `LICENSE`, `COPYING`, or `NOTICE` file at that commit, and the latest commit touching the source skill was authored by `Casper <wcc723@users.noreply.github.com>`.
Treating unlicensed source text as all-rights-reserved, this implementation preserves only general functional ideas and uses newly written prose, examples, schema, routing boundaries, and evaluation cases.

Source-specific coupling to `slide-html`, L01-L20 identifiers, Claude-only paths, and its rigid phase gates was intentionally omitted so the skill remains self-sufficient and portable across agentskills.io consumers.

## Baseline

This is a new skill in this repository.
Its required baseline is vanilla behavior without the skill loaded.

## Evaluation: 2026-08-10

Two early comparison rounds were discarded because behavior agents could read `evals.json` and therefore saw the expectations.
The ship comparison used fresh agents that received only the raw case prompts; skill arms additionally read `SKILL.md`, while vanilla arms read no skill.

Two independent runs per arm were judged blind by Claude CLI.
The skill arm won all six case comparisons after correcting one X/Y transcription error in the judge's Set 2 report.
The decisive differences were stable slide scaffolding, claim/job/form outlines, explicit evidence gaps, and refusing unsupported numeric commitments.

The fixture and skill were authored in the same root session, so qualitative conclusions remain author-contaminated even though generation and judging were independent.
The result supports that the added mechanisms address gaps observed in vanilla outputs; it is not evidence of universal superiority.

See `evals/results-2026-08-10.md` for mappings, per-case outcomes, and protection failures.

# plain-speak — design notes

Iteration log and rationale. Not loaded by the skill; for maintainers.

## v1.4.0 — 計畫可執行度 (2026-07-28)

**Problem.** The existing `具體優先於抽象` guardrail only had a descriptive face — its
examples are all past-tense checkable facts. A plan-bearing input abstracts differently: a
**原則** ("分階段導入、控制風險") reads as content because it has a subject and a verb,
so it slips past a guard tuned to spot obviously-empty modifiers like「大幅」「全面」.

**Fix.** Extended the same guardrail bullet with a prescriptive face: when the material is a
plan, the concrete form is a **做法** — who does what, and what counts as done. Added a
tie-break sentence against the pre-existing `representative-concrete` rule (fold lists of
>3 items into a theme clause), because a plan's moves are what the reader is waiting on, not
evidence to fold away — without the tie-break the two rules would collide head-on on any
plan with more than 3 action items.

**Placement decision.** Considered a separate `## Explaining a plan` section (more room to
define shape) versus extending the existing guardrail bullet (single source of truth for
the abstraction axis). Chose the extension — 原則 is a face of the same abstraction problem
具體 already owns, not a new mode.

**Eval design took two iterations to get right — this is the useful lesson for next time.**
The first version of eval case 5 used a 3-move plan. This looked reasonable but was a design
flaw: 3 items sits at/below the pre-existing `representative-concrete` rule's own trigger
threshold ("more than ~3 things"), so baseline was never actually at risk of folding it —
the case couldn't discriminate between versions no matter how the rule was written. The A/B
on that version came back a near-tie (v1.4.0 3/4, v1.3.0 4/4 across 4 reps/arm), which read
at first like the new rule might be a no-op per `engineering-guidelines.md`'s own standard
("a rule that doesn't measurably change behavior shouldn't ship").

Rather than ship on a shrug or revert on a shrug, redesigned the case to 4 moves —
deliberately past the folding threshold — before deciding either way. That version produced
a clean, reproducible result: v1.4.0 kept all 4 actions with their numbers in 2/2 reps;
v1.3.0 baseline independently stripped 3 of 4 numbers into vague thematic language
("拉到三倍" instead of stating 10→30, etc.) in 2/2 reps. Full log:
`evals/results-2026-07-28-plan-concreteness.md`.

**Takeaway for future rule additions to this skill:** when a new rule is meant to override
an existing threshold-based rule (here, the >3-item fold), the eval case must sit clearly on
the far side of that threshold, not at its boundary — otherwise a near-tie A/B result is
uninformative rather than reassuring.

**Not changed:** `description`/trigger surface (verified byte-identical except `version:`),
`catalog.md` (the new rule refines an existing highlight rather than adding scope),
`trigger-queries.json`.

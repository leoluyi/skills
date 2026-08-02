# Plan → Goal

A rough plan says how to do something; a goal spec says what "done" looks like. This skill bridges the two: it takes a plan that's probably still coarse, fleshes it out, exposes the holes in it, has you rule on the ones that matter, and only then hands you a goal spec with completion conditions an agent can check by itself — so an autonomous run doesn't have to guess your intent mid-execution.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a plan-to-goal -y
```

To update later:

```
npx skills update plan-to-goal
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/plan-to-goal/SKILL.md)

## What it does

The skill runs in two phases with a gate between them.

**Phase 1** reads your plan (and the code it touches) without executing anything, then produces a review with five fixed parts: the real finished state in plain language, a set of completion conditions that are each checkable by running a command (a test suite passing, a typecheck clean, a grep returning nothing — never an adjective like "clean" or "refactored well"), the plan's genuine holes stated as open questions, the high-risk, hard-to-reverse steps worth paying attention to, and the run's read/write surface — which paths it may read, which it may write, what is off-limits, and whether it may reach outside the machine at all. It also carries forward any "do not touch" constraints already in the plan.

**The gate** sorts those holes into two piles: the ones only you can decide (asked as 2-4 labelled options plus an "other" escape hatch) and the ones exploration already settled (stated as an answer for you to confirm, not re-asked). Either way, you see the whole resolved picture — done-definition, every fork's answer, the constraints, the surface, the conditions — for one yes/no before anything is finalized. Extra work the model notices along the way stays out of the goal and gets listed separately.

**Phase 2**, only after you confirm, writes a goal file holding a short decision record (what got decided and why) plus six elements:

```
Outcome: <the confirmed finished state, scoped to the original plan>
Verification: <machine-verifiable conditions, each naming a command and its expected result>
Constraints: <carried-forward "do not" rules, verbatim>
Boundaries: <what may be read, written, left alone, and whether anything may leave the machine>
Iteration Policy: <what to record per round: what it did, what came of it, what to try next>
Blocked Stop Condition: <what counts as stuck, and the report to leave behind>
```

Then it hands you one line to paste, not the whole file:

```
/goal 依 @plans/goal-<slug>-<date>.md 執行。Done when: <conditions>. Stop after <N> turns.
```

That split is deliberate. A goal condition is a predicate, not a context container — the goal mechanism re-reads it every round to judge whether the work is done, so a page of prose in that slot makes the judgement mushier each time (and is miserable to paste into a terminal). The long context lives in the file and gets pulled in by a file mention. The stop limit is mandatory: a goal loops until its condition is met, and an unreachable condition (a flaky test, a pre-existing failure) would otherwise spin until something else stops it. Where your agent has no goal command or no file-mention syntax, the file's full text is the prompt instead.

## When to use

Reach for it exactly when you already have a plan — from plan mode or written by hand — and it's still rough, high-level, or unfinished, and you want an agent to run it unattended without drifting off course or declaring victory too early. Fleshing out the gaps before the run starts is the entire point: it moves every wrong guess to the cheapest moment, before tokens and file edits happen.

## When not to

Don't use it to write a plan from scratch — that's plan mode's job, not this skill's. And don't use it for a task small enough that one prompt would finish it; writing a goal spec for a one-line typo is pure overhead.

## How it works

The mechanism is a forced separation between describing done and deciding on ambiguity. A condition only counts if it names a command and an expected result — "no file still imports the old module," checked with `grep -r "legacy/payment" src/` returning nothing, not "the refactor is clean." Constraints work the same way: "do not modify anything under `legacy/`" survives verbatim from the original plan into the final goal, rather than being reworded or dropped.

Constraints and boundaries stay separate for the same reason: a constraint is a rule about *how* the work happens ("keep the old interface"), a boundary is *where* it may happen ("write only under `src/payments/`"). A run can respect every constraint and still wander into the wrong directory.

A worked example from the skill: a plan that says "refactored the payment module across ~14 files, want to run it" gets fleshed into conditions like `npm test` passing, `npm run typecheck` clean, and `grep -r "legacy/payment" src/` empty — plus one genuinely open hole ("three call sites pass a deprecated flag — keep or drop?") asked as a choice, one hole the exploration already closed ("does `refundLegacy` still have callers?" — no, confirmed by grep) stated rather than asked, and one boundary question the code can't answer (may the run push?). The resulting goal file reads:

```
Outcome: Every payment call site runs on the new module and the old one is gone from src/.
Verification: npm test passes; npm run typecheck is clean; grep -r "legacy/payment" src/ returns nothing.
Constraints: do not modify anything under legacy/; keep the deprecated flag on the three flagged call sites.
Boundaries: read anything in the repo; write only under src/payments/ and its tests; legacy/ is read-only; commit locally, never push.
Iteration Policy: per round, record which call sites moved, what the three commands returned, and the next call site to take.
Blocked Stop Condition: stop after three distinct failed hypotheses on one blocker, or if a condition turns out to be unreachable. Report what was tried, where it jammed, what is missing, and what decision would unblock it.
```

And the line you paste:

```
/goal 依 @plans/goal-payment-refactor-2026-08-02.md 執行。Done when: npm test passes, npm run typecheck is clean, and grep -r "legacy/payment" src/ returns nothing. Stop after 25 turns.
```

## Related skills

This skill is meant to run after a plan already exists — typically straight out of plan mode, or a plan you wrote by hand. It composes with whatever produced that plan rather than replacing it; it doesn't do the planning itself, only the tightening that makes a plan safe to hand to an unattended run.

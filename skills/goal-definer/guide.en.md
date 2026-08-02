# Goal Definer

A long-running agent doesn't usually fail by doing the wrong thing. It fails by deciding it's finished. "Optimize the checkout speed" is satisfied by a single cache header; "tidy up our customer data" is satisfied by deduplicating one column. This skill interviews a fuzzy task until it becomes a six-element goal prompt that another agent could work against for hours, and could verify without you looking at the result.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a goal-definer -y
```

To update later:

```
npx skills update goal-definer
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/goal-definer/SKILL.md)

## What it does

It runs a conversation, one question at a time, never as a form to fill in. Six things come out of it:

- **Outcome** — the finished state in observable terms. Vague answers get pushed back: "better", "更完整", "more polished" are refused until you say what specifically changes, who uses the result, and what decision it supports.
- **Verification** — how the agent proves it's done without you eyeballing it. For engineering work that means tests, lint, benchmark thresholds, error counts. For writing, strategy or research it means inspectable criteria: does it answer the named questions, cite the required sources, match the defined audience, avoid the named anti-patterns, hit the target format.
- **Constraints** — what can't change, what can't be assumed, what data and systems are off-limits, what style or strategy is forbidden.
- **Boundaries** — the read/write surface. What it may read, what it may modify, what it must not touch, whether anything may leave the machine.
- **Iteration Policy** — what gets logged each round. At minimum: what this round did, what came of it, what's most worth trying next.
- **Blocked Stop Condition** — when to give up and what the report has to contain: what was tried, where it jammed, what information is missing, and what decision from you would unblock it.

Then it hands back three things: a diagnosis naming where your original phrasing was ambiguous, the paste-ready goal prompt, and one line on the highest-risk thing left to sanity-check.

## When to use

When the task will take hours, you don't have a plan for it yet, and the way you'd describe it out loud is still a verb like "optimize", "clean up" or "rewrite". Those verbs are where agents stop early, because they're true of almost any amount of work.

## When not to

Not when you already have a written plan — Plan → Goal takes it from there, asking the code instead of asking you. Not for writing the plan itself. And not for a task one prompt would finish; a goal spec for a one-line change is pure overhead, and the skill will say so and stop rather than humour you.

## How it works

The whole design is a refusal to accept an unverifiable answer. "Higher quality" isn't a criterion, so it gets pushed on; if you can't make it concrete, the skill says so in the diagnosis instead of quietly writing a generic goal around the hole. It also won't invent constraints or boundaries you didn't state — anything that looks important but wasn't mentioned gets asked about, not assumed.

Where the task genuinely hinges on subjective quality ("the article should sound human"), it points you at distilling a taste rubric first and feeding that into Verification, rather than pretending a machine check exists.

## Related skills

`taste-distiller` produces the rubric that Verification can point at when the standard is a matter of taste rather than a passing command. `plan-to-goal` covers the neighbouring case: you already have a plan, so the questions go to the code first and only the genuinely open forks come to you.

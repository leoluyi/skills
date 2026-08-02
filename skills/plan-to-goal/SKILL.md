---
name: plan-to-goal
description: >-
  Turn a rough plan into a bounded, verifiable goal spec — objective, machine-checkable done-when conditions, do-not constraints, and a stop limit — that an agent can execute autonomously without drifting. Use this whenever the user has a plan (from plan mode or written by hand) and wants to run it autonomously — phrases like "turn this plan into a goal", "make this a /goal", "run this autonomously", "let it run on its own", 「把這個計畫變成可以自動跑的 goal」, 「讓它自己跑完」, 「這個 plan 還很粗，幫我補完再自動執行」, or when the user has just finished plan mode and asks what's next. Especially use it when the user admits their plan is rough, high-level, or unfinished, because the whole point is to flesh the plan out and surface its gaps BEFORE an autonomous run burns tokens on a vague target. Do NOT invoke for writing a plan from scratch (that is plan mode itself), or for a task small enough that one prompt would do — a goal spec is overhead for a one-line typo.
app-description: >-
  把粗略或手寫的計畫轉成可自動執行的 goal spec：目標、可機器驗證的完成條件、禁止事項與停止上限。觸發：「把這個計畫變成可以自動跑的 goal」「讓它自己跑完」「這個 plan
  還很粗，幫我補完再自動執行」，或 turn this plan into a goal、run this autonomously。
version: 2.0.0
license: MIT
disable-model-invocation: true
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: agent-workflow planning autonomous-execution goal-setting verification
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F3AF"
---

# Plan → Goal

A rough plan and a goal spec are not two artifacts you convert between. They are two halves of one thing: the plan says *how* to do it, the goal says *what "done" looks like*. This skill bridges them — it takes a plan that is probably still coarse, fleshes it out, exposes its holes, makes the user adjudicate the ones that matter, and only then emits a goal with machine-verifiable completion criteria.

The reason it exists: handing a rough plan straight to an autonomous run means the agent spends that run *guessing the user's intent* mid-execution, and a wrong guess isn't discovered until tokens and file edits have already happened. Fleshing the plan out first moves every guess to the cheapest possible moment — before anything runs.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the plan, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## The workflow

Two phases with a gate between them. Phase 1 produces a review the user reads; the model then **stops and waits**; only after approval does Phase 2 emit the goal. Running both in one breath throws away the entire value of the skill — the gate is where a wrong assumption costs one sentence instead of a whole run.

### Phase 1 — Flesh out and expose holes

Read the plan and whatever code it touches. Execute nothing. Then produce these five sections, in order, as a review for the user.

1. **What "done" actually looks like.** The real finished state in plain language, *including the parts the rough plan didn't mention*. This is where the model earns its keep: it has seen enough similar tasks to know what the user will forget. Completion: the finished state is stated without reference to steps.

2. **Verifiable completion conditions.** Every condition is checkable by running a command — a test suite passing, a typecheck clean, a search returning nothing, a build succeeding. No adjectives: "refactor is clean" is not a condition; "no file still imports the old module" is. Anything that can't be phrased as something a machine checks stays in the prose above and never enters the goal. Completion: every condition names a command and its expected result.

3. **Holes in the current plan.** The edge cases the plan skipped and the places where the user's intent is genuinely ambiguous — written as questions for the user, not as decisions already made.

4. **High-risk steps.** Which steps are hard to reverse or expensive to get wrong, so the user knows where to pay attention.

5. **The read/write surface.** Which files, directories, APIs and data the run may read; which of those it may write; what it must not touch; and whether it may reach outside the machine at all — push to a remote, call an API, send anything. Derive this from the plan and the code first: the files the plan names, the directories they live in, the tests and configs that have to move with them. Only what the code genuinely cannot settle — usually the outward-facing calls and the git permissions — goes to the gate as a question. Completion: every path the run may write is named, and the outward-facing answer is explicit rather than assumed.

Also collect every "do not touch" constraint already in the plan (keep the old interface, don't modify `legacy/`, stay inside `src/`). These reappear verbatim in the final goal, so gather them now.

Constraints and the read/write surface are near neighbours and easy to collapse into one list. Keep them apart: a constraint is a rule about *how* the work is done (keep the old interface, don't change the public API shape), the surface is *where* it may happen. A run that respects every constraint can still wander into the wrong directory, and a run confined to the right directory can still break the interface.

### The gate — resolve what you can, ask only what's left, confirm once

The gate exists so the user rules on the real forks and confirms the endpoint. But **fleshing the plan out usually resolves most forks on its own** — the code makes the answer obvious, or the plan already implied it. A question whose answer became clear in Phase 1 is friction, not diligence.

So sort the section-3 holes into two piles first:

- **Genuinely open** — a real judgment call the code can't settle: a product decision, a trade-off with no obviously-right side, an intent that is truly ambiguous. Only these become questions.
- **Resolved by Phase 1** — exploration made the answer clear, or only one option is viable. Don't ask. State the answer you landed on and *why*, as something the user confirms at the end rather than decides now.

**When holes are genuinely open,** ask them as choices: 2–4 mutually exclusive options per hole, each labelled by outcome with its trade-off in one line, plus a final "其他（我自己說明）" / "Other — I'll specify" so the user is never boxed in. Name which way you lean and why, then wait. Use a tappable-choice tool where one exists; otherwise a short numbered list. If one answer would make a later question moot, ask the gating one first and let it prune the rest.

**When nothing is genuinely open,** don't manufacture questions — go straight to the confirmation.

**The confirmation happens every time,** questions or not: the whole resolved picture in one place for a single yes/no — the "done" definition, every fork with its answer (whether the user just picked it or Phase 1 settled it), the carried-forward constraints, the read/write surface, and the completion conditions. Frame it as "here's the whole thing — confirm and I'll write the goal, or tell me what to change." The user always eyeballs the full picture before a goal exists; they only actively *answer* on the forks that needed them. Completion: the user has confirmed, or named what to change.

Write the confirmation the way the goal itself has to read: no adjective stands in for a criterion. "The refactor will be clean", "docs will be improved", "coverage gets better" are the same failure the completion conditions exist to prevent, and letting one through here means the user signs off on a picture the goal can't express. Every line either names something observable or is cut.

**When the user satisfied the gate on the way in** — the handed-over plan already resolves the holes and states the conditions ("keep the old interface, don't touch `legacy/`, done when tests and typecheck pass with no stale imports") — keep the confirmation light: echo the resolved picture back in a sentence or two and move on. Staging a formal sign-off for something already spelled out is theatre.

**Scope discipline:** Phase 1 may have surfaced extra work worth doing ("while we're here, add a cache"). Keep it out of the goal. Say plainly that the goal covers the original plan's scope only, and list the extras separately as things to pick up later. A bounded refactor turning into an unbounded project is the failure mode an autonomous run is least able to notice.

### Phase 2 — Emit the goal

Only after the user confirms, produce two parts.

**Part A — the decision record.** A short recap: the confirmed "done" definition, each resolved hole with its ruling, the carried-forward constraints, the read/write surface, and the stop limit. This is what the user signed off on, and the reason a saved goal is still legible months later.

**Part B — the goal file,** written to disk, holding six elements assembled from Part A:

```
Outcome: <the confirmed finished state, scoped to the original plan>
Verification: <the confirmed machine-verifiable conditions, each naming a command and its expected result>
Constraints: <the carried-forward "do not" rules, verbatim>
Boundaries: <what the run may read, what it may write, what it must not touch, and whether it may reach outside the machine>
Iteration Policy: <what to record per round — at minimum: what this round did, what came of it, what is most worth trying next>
Blocked Stop Condition: <what counts as stuck, and the report to leave — what was tried, where it jammed, what information is missing, what decision would unblock it>
```

- Outcome and Verification are two different readers' halves: Outcome is the finished state a human reads, Verification is what a machine checks. Neither substitutes for the other, and collapsing them back into one line loses whichever reader it was not written for.
- Verification conditions come *only* from the confirmed list — nothing the user didn't approve.
- Constraints carry the Phase 1 rules verbatim; Boundaries carry the Phase 1 read/write surface.
- Iteration Policy and Blocked Stop Condition are honoured by the agent, not enforced by the harness — no goal mechanism checks that a round was logged. They are worth writing anyway: an autonomous run that leaves no trail is unauditable afterwards, and one with no stated surrender condition grinds against an impossible step until the turn limit cuts it off. Say plainly that these two are conventions the run follows, not gates it trips.

Then give the user **one line to paste**, not the whole file:

```
/goal 依 @<path-to-goal-file> 執行。Done when: <the machine-verifiable conditions>. Stop after <N> turns.
```

- The one-line form exists because a goal condition is a predicate, not a context container: the goal mechanism re-reads that text every round to judge whether the work is finished. A page of prose in that slot makes the judgement mushier every round, and it is miserable to paste into a terminal. The long context belongs in the file, pulled in by a file mention; the condition stays narrow.
- Always set a stop limit. A goal loops until its condition is met; an unreachable condition (a pre-existing broken test, a flaky suite) spins and burns tokens until something stops it. The limit is the stop-loss.
- Where the agent has no goal command, or no file-mention syntax, the goal file's full text is the prompt instead. Say which form applies rather than assuming the user's tool.
- If the user wants it truly unattended (CI, cron, headless), point out that it needs the agent's non-interactive mode with tool permissions pre-granted, or it stalls on the first permission prompt. Their call to make, not something to add silently.

**Cost:** an autonomous run is a different order of magnitude from a normal turn — tens of thousands of tokens for a single-file goal, hundreds of thousands for a multi-file one. One line of heads-up before they kick it off, so the bill isn't a surprise.

### Where the goal file goes

Name it `goal-<slug>-<YYYY-MM-DD>.md`, where `<slug>` is a short kebab-case tag from the objective (`payment-refactor`, `auth-jwt-migration`). The date keeps successive goals on the same target in order and stops a re-run from clobbering the earlier record. Suggest a location that fits the repo's layout, and let the user rename or redirect it rather than scattering files.

Write **both** parts into it: Part A as prose, then Part B's six elements. The record is what makes the file worth keeping — the elements alone lose the "why", and months later that is the only thing that makes an old goal legible.

If the user would rather not have a file at all, hand them Part B inline and say the tradeoff out loud: no version history, nothing to review in a PR, and the whole thing has to be pasted by hand.

## What good looks like

**Rough plan in:** "Refactored the payment module across ~14 files, want to run it."

**Phase 1 out (abridged):** done = every call site migrated and the old module deleted; conditions = `npm test` green, `npm run typecheck` clean, `grep -r "legacy/payment" src/` empty; holes = three call sites pass a deprecated flag — keep or drop?; risk = the shared checkout path; surface = writes confined to `src/payments/` and its tests, `legacy/` read-only, no pushing.

**Gate:** one hole genuinely open, one already resolved, one surface question the code can't answer.

> The deprecated flag is a real judgment call, so it's asked: **(a) keep it** — safest, no behaviour change, deprecation lingers; **(b) drop it** — cleaner, but callers relying on it break; **(c) other** — you specify.
>
> "Does `refundLegacy` still have callers" isn't asked — Phase 1's grep showed none, so it's stated as "removing it; grep confirms no callers" for confirmation at the end.
>
> The write surface isn't asked either — the plan names the files, so it's stated. Whether the run may push is asked, because nothing in the code implies an answer.
>
> Then the whole picture in one place: done-definition, the flag decision, the `refundLegacy` removal, the constraints, the surface, the three conditions. "Confirm and I'll write the goal?"

User picks **(a)**, says commits are fine but no pushing, and confirms.

**Part B, written to `plans/goal-payment-refactor-2026-08-02.md`:**

```
Outcome: Every payment call site runs on the new module and the old one is gone from src/.
Verification: npm test passes; npm run typecheck is clean; grep -r "legacy/payment" src/ returns nothing.
Constraints: do not modify anything under legacy/; keep the deprecated flag on the three flagged call sites.
Boundaries: read anything in the repo; write only under src/payments/ and its tests; legacy/ is read-only; commit locally, never push.
Iteration Policy: per round, record which call sites moved, what the three commands returned, and the next call site to take.
Blocked Stop Condition: stop after three distinct failed hypotheses on one blocker, or if a condition turns out to be unreachable. Report what was tried, where it jammed, what is missing, and what decision would unblock it.
```

**The line the user pastes:**

```
/goal 依 @plans/goal-payment-refactor-2026-08-02.md 執行。Done when: npm test passes, npm run typecheck is clean, and grep -r "legacy/payment" src/ returns nothing. Stop after 25 turns.
```

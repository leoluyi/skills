# Discuss With Me

This skill is a thinking partner for a question that neither you nor the model can answer yet — an open design direction, a bet under real uncertainty, a diagnosis running on thin evidence. It is not a teaching tool (that's for questions with a settled answer) and not a debugging tool (that's for questions with a discoverable one). It exists for the case where two fluent parties reasoning together would happily produce a confident, well-organized answer regardless of whether it's actually right — and keeps that from happening by widening the options, labelling what's found versus guessed, attacking the assumptions the conclusion depends on, and leaving behind a record of what would prove it wrong.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a discuss-with-me -y
```

To pull updates later:

```
npx skills update discuss-with-me
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/discuss-with-me/SKILL.md)

## What it does

- **Widens before converging.** Puts more options on the table than you brought — five for a narrow question, closer to twenty for a wide-open one — including ones that cut against the direction the conversation is already drifting toward. Hands you the cut and asks which to keep, drop, or merge.
- **Grounds every load-bearing claim.** Sorts each one into found (a source says it, cited), inferred (follows from something found, plus a named step), or guessed (neither). Marks these inline as it writes, not as an afterthought, because a guess reads exactly like a fact once the prose is smooth.
- **Attacks the assumptions the direction actually rests on.** Once a direction is forming, runs a red-team pass: for each load-bearing assumption, names what would break it, the cheapest evidence that would settle it, and the threshold at which the direction gets abandoned rather than patched.
- **Verifies outside the context that built the conclusion.** Hands the record — nothing else — to a reader with no history in the conversation: a subagent, a new session, or a different model family. The same pull toward agreement that threatens the discussion also makes the original context a poor judge of its own output.
- **Leaves a record, not a decision doc.** Writes what survived into a file that carries its own falsification alongside the conclusion — killed options, the strongest case against, and what's still open — so someone reading it later can tell what was known versus guessed, and whether anything since has changed enough to reopen it.

## When to use

Use it when the answer is unknown to both sides: an open design direction with no obvious winner, a strategy call under real uncertainty, a diagnosis running on thin evidence, or a discussion that's been converging for a while without anyone naming what would make it wrong. Also use it invoked bare, mid-conversation, with no question attached — that reads as "your last answer had something in it I can't act on yet," and the skill goes looking in its own previous turn for the unargued premise.

## When not to

Skip it when the user already has the answer and just wants it written up — that's a drafting job for `knowledge-doc-writing` or `formal-doc-structure`. Skip it when the concept has a settled answer the user hasn't met yet — teach it, or use `learn-loop`; dressing up a known answer as joint inquiry wastes their time and flatters both sides. Also skip it for plain factual lookups, debugging, and code review — the test is whether the answer is unknown to both parties, not whether the topic feels hard.

## How it works

The record-template (`references/record-template.md`) is what makes the output different from a decision doc: every load-bearing sentence in the "current best account" section carries an inline `[found]` / `[inferred]` / `[guessed]` tag, the killed-options table stays in the file even after a direction wins, and the open-questions section is required to be non-empty while the question is genuinely open — an empty one means the record is lying. The file is edited in place across passes rather than appended to, so it survives a context reset instead of degrading into an append-only log nobody rereads.

The redteam-pass (`references/redteam-pass.md`) is what turns "we think X" into something checkable. It extracts four to seven load-bearing assumptions (more than that means the discussion is being catalogued, not attacked), then for each one produces a *fails-if* condition specific enough to recognize on sight, the *cheapest evidence* that would move belief, a *kill criterion* decided before anything is sunk into the direction, and *who would know* the answer already. Assumptions get ranked by damage-if-wrong against cost-to-check, and a separate "wrong-and-silent" category exists for failures that wouldn't announce themselves for months — the flavour discussions consistently miss because they only imagine failures they'd notice.

## Related skills

- **knowledge-doc-writing** — use it once the answer is settled and the job is organizing it into a reference document, not discovering it.
- **formal-doc-structure** — use it for a formal internal document (簽呈, 會議紀錄, 評估報告) where the content is already decided and the task is structure.
- **learn-loop** — use it when the concept has a known answer and the goal is the user learning it, not the pair jointly discovering it.

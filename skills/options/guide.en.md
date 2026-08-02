# Options

Answering an open-ended question by typing is slow, and half the time the answer you'd give is one of three the model already had in mind. This skill turns that around: it re-asks whatever is currently pending as tappable choices, and then keeps every direction decision clickable for the rest of the session.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a options -y
```

To update later:

```
npx skills update options
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/options/SKILL.md)

## What it does

Two things, in order.

First it acts on what's already on the table — the last thing asked in prose, or the decision the model was about to make on its own, re-asked right now as selectable choices. Same question, same context, no restarting the topic and no asking you to repeat yourself. If nothing is pending it says so in one line and moves on.

Then, for the rest of the session, any decision that affects direction — architecture, library, data model, scope, sequencing — stops and becomes 2-4 mutually exclusive options instead of a choice made for you. Each is labelled by outcome rather than tone, names its trade-off in one line, and the recommended one comes first and says why. The "Other" escape hatch is added automatically, so it never costs an option slot.

## When to use

When you're tired of typing answers to open questions, or when you've noticed decisions being made on your behalf and want them surfaced before they land.

## When not to

Not for reversible or mechanical steps — those should just get done, and turning them into questions is its own kind of friction. Not for laying out an entire decision space in full; that's Breakdown. And it steps aside on request: say "autonomous" or "run to completion" and it drops out entirely, batching the decisions into a closing summary instead.

## How it works

The rules that make the choices actually usable are about the shape of the option set, not the tone.

**Combinations are pre-enumerated.** When choices could combine, it proposes "A only", "A + B", "all three" as their own mutually exclusive options, so one click still settles it. Multi-select is reserved for the case where the combinations are too many to list — otherwise the assembly work gets pushed back onto you, which is what you were trying to avoid.

**The axis gets covered honestly.** One axis per question, both ends listed, including "keep it as is". If a sensible choice is neither listed nor a blend of two that are, the axis was cut wrong and gets redone rather than patched.

**Nothing already settled gets re-asked.** Anything you've already constrained stays constrained.

Where no tappable-choice tool exists, it falls back to a short numbered list — and plain text is also the right form when the answer is genuinely open-ended: a name, a number, a URL.

## Related skills

`breakdown` is the heavyweight version — it lays out every case at uniform depth before any decision is put to you, where Options just makes the pending one clickable. `autopilot` is the opposite setting entirely: it explicitly suspends this behaviour and batches every decision into one report at the end.

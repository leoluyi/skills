# Breakdown

The failure this skill exists to prevent is a recommendation that arrives before the ground has been laid — where three options were considered, two were dismissed in a clause each, and you never got to see the one that was quietly dropped. Breakdown inverts the order: every case in full first, then the decisions split out for you to make, and only then a recommendation that has to account for every case it started with.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a breakdown -y
```

To update later:

```
npx skills update breakdown
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/breakdown/SKILL.md)

## What it does

Three phases, and phase 3 deliberately does not happen in the same message.

**Phase 1** enumerates the distinct cases *before* evaluating any of them, and names the axis they vary on so you can judge whether it was cut the right way. Each case gets its own section covering what it is, what is actually true about it (with paths, values, versions, error text — each item marked **fact**, verified and where, or **inference**, reasoned and from what), why it's distinct from its neighbours, what follows from it, and what remains unknown. The do-nothing case is on the list. So is the awkward one nobody wants. Anything deliberately left out appears under an "excluded" heading with a reason, because a silent omission reads as coverage.

**Phase 2** splits the problem into the individual decisions it contains, one question per decision, each carrying what hinges on it — which phase 1 cases it selects between, and how the recommendation moves with your answer. It only asks what changes the outcome; anything it could establish by reading the code, or that you already told it, doesn't get asked. Then it stops. It doesn't answer its own questions and doesn't start editing the part it thinks is settled anyway.

**Phase 3** arrives after you answer: the recommendation as a decision rather than a menu, which of your answers drove it, where a different answer would have flipped it, what happened to *every* case from phase 1, what it decided without asking, what's still uncertain, and the single next step.

## When to use

When a conclusion showed up too fast and you want the ground under it. Also when the space is genuinely wide — several credible approaches, several code paths, several failure modes — and you'd rather see them all laid out at uniform depth than trust a summary of them.

## When not to

Not when there's one pending decision you'd like made clickable — that's Options, and it's a fraction of the work. Not when nobody knows the answer yet and the value is in exploring it together. And not for a question with a settled answer you could simply look up.

## How it works

Two rules do most of the work. The first is that facts and inferences are never blurred: every claim is tagged as one or the other, with its source or its reasoning. The second is uniform depth — if one case gets four sentences and another gets a clause, that asymmetry is a decision made on your behalf, so the thin one either gets filled in or gets an explicit note saying why it can't be.

It also refuses to pad. If the subject genuinely has two cases, you get two, and it says so rather than manufacturing a fifth to look thorough.

If you'd rather not answer, saying "just decide" skips phase 2 — every unanswered question becomes an explicitly stated assumption in phase 3 instead of a silent one.

## Related skills

`options` handles the narrow version: one pending decision, re-asked as tappable choices, without the full enumeration. `discuss-with-me` is for the case where the answer is unknown to both sides and the point is joint exploration rather than laying out a space you already suspect the shape of.

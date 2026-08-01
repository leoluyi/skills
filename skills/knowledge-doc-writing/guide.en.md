# Knowledge Doc Writing (Diátaxis)

This skill turns a technical topic you've studied or researched — a conversation transcript, raw source material, or a from-scratch investigation — into a single lasting reference document split into four cleanly separated Diátaxis sections: tutorial, how-to, reference, and explanation. It writes only what the material can actually support, and names the gaps instead of padding them with invented content.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a knowledge-doc-writing -y
```

To update later:

```
npx skills update knowledge-doc-writing
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/knowledge-doc-writing/SKILL.md)

## What it does

Every piece of input material gets routed through a **compass** — two yes/no questions applied to each chunk:

1. **Action or cognition?** Does this material have the reader *do* something, or does it build understanding?
2. **Acquisition or application?** Does it serve the reader while they're still acquiring the skill (studying), or while they're applying a skill they already have (working)?

The two answers point to exactly one of four quadrants:

| | Acquisition (at study) | Application (at work) |
|---|---|---|
| **Action** | tutorial | how-to |
| **Cognition** | explanation | reference |

Each piece of material lands in exactly one section. A passage that answers both quadrants at once is a signal to split it, not to write it twice. The result is an auditable material-to-section assignment table, checked before any prose gets written.

The four sections stay pure and never mix:

- **tutorial** — a single safe straight line for a first-time reader, first-person-plural imperative voice, no branching, no digressions.
- **how-to** — assumes competence, goal-oriented, if-then branching allowed, no teaching.
- **reference** — describe-only, neutral, mirrors the underlying product's own structure, no argument.
- **explanation** — the only section allowed to carry judgment: a What/Why argument, trade-off decisions, mental models, common misconceptions.

If a quadrant has no material behind it — commonly tutorial or how-to, when a topic was researched but never actually run hands-on — that section is marked as an explicit gap with the condition needed to fill it, rather than being faked or left as an empty shell.

Inside explanation, a comparative recipe runs as an internal device rather than a section of its own: definition, behavioral boundary, comparative analysis, a boundary-judgment table for the grey areas, and a decision framework that states both when to adopt and when not to — the "when not to" half carries as much weight as the "when to," since a comparison that skips it reads as advertising rather than analysis.

## When to use

Use this when you want to distill a technical topic you studied or researched into one lasting reference document, cleanly split into tutorial, how-to, reference, and explanation sections. That covers digesting a conversation transcript, reorganizing raw source material (official docs, specs, meeting notes) by reader need rather than by the source's own table of contents, and researching an unfamiliar topic from scratch (with mandatory primary-source checks and as-of dating).

It also handles rewriting an existing technical document, branching on intent rather than on the verb used:

- **Refresh currency or fold in new material** → a point-patch: keep the document's original shape and change only the parts affected by staleness or new content. This path never runs the compass and never reorders the whole document.
- **Reorganize or restructure** → hand the material to the compass and rebuild the four sections from scratch.

## When not to

- Internal administrative documents — 簽呈, meeting minutes, evaluation reports — even when the input is an existing document that looks like it belongs here; hand those to **formal-doc-structure** instead.
- RFPs or procurement specs — use **rfp-writing**.
- Blog posts — use **blog-writing-zh**.
- Language-only cleanup that doesn't touch structure — use **humanizer-zh**.
- A spoken plain-language explanation with no document to produce — use **plain-speak**.
- The interactive learning loop itself, where the user does their own hands-on distillation — that's **learn-loop**'s job, not this skill's.

## How it works

The compass is the load-bearing mechanism: nothing gets written until every piece of material has been run through both questions and logged in the assignment table. A section only gets written if it has material behind it, and it's held to its boundary's purity — reference never carries an opinion, explanation never turns into an empty scaffold, tutorial never grows real-world branching, how-to never turns into a teaching aside.

After drafting, two adjacent-pair checks catch the most common blurs, because adjacent quadrants share one dimension and are the easiest to confuse for each other:

- **tutorial ↔ how-to** (both action-oriented, differing only on study-vs-work) — the most damaging blur, since it blocks a beginner with real-world branching they aren't ready for. Any conditional step that assumes prior judgment gets pulled out of tutorial and placed in how-to.
- **reference ↔ explanation** (both propositional, differing only on describe-vs-discuss) — any argument or opinion that leaked into reference gets pulled out and placed in explanation.

Anything that crosses a boundary becomes a cross-link, never inline-mixed prose. A gap section gets a single line noting the gap and the condition that would fill it — never a placeholder paragraph pretending to be content.

This skill sits downstream of **learn-loop**. `learn` owns the interactive learning loop and the hands-on distillation itself — digesting material into your own words, judging whether you actually understand it — and that step is never delegated or redone here. What this skill receives is understanding that's already settled: its only job is reorganizing that understanding for an external reader, filling in the context a third party would need, converting or dropping vault-specific markup like wikilinks, and carrying forward already-verified sources with the as-of date updated to publication time.

Before delivery, two quality gates run in order — functional quality (every claim traced to a primary source, as-of dates and version ranges marked, no fabricated sources, a de-AI pass to zero) always clears before any polish for flow or beauty. A document can be complete and shippable with only one or two of the four sections written, as long as every section is either covered or explicitly marked as a gap — no silent omissions, no shell sections waiting to be filled in later.

## Related skills

- **formal-doc-structure** — owns 簽呈, meeting minutes, and evaluation reports; administrative documents route there even when they arrive in a format that looks like this skill's territory.
- **rfp-writing** — owns RFPs and procurement specs, which follow structural rules that conflict with this skill's Diátaxis routing.
- **blog-writing-zh** — owns blog posts and reader-voice composition, a different genre from a reference document.
- **humanizer-zh** — owns pure language-layer de-AI cleanup when no structural reorganization is needed; this skill calls it as the de-AI pass before delivery when available.
- **plain-speak** — owns spoken, on-the-spot plain-language explanation with no document as the deliverable.
- **learn-loop** — owns the interactive learning loop and the hands-on distillation itself; this skill only picks up after that distillation is done, to reorganize and add reader context.

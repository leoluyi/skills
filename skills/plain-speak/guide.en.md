# Plain Speak: Jargon into Plain Language

Turn a technical term, code snippet, or dense engineering paragraph into one line your PM, exec, or customer can actually repeat back. It works from a single anchor — who the reader is — and holds every rewrite to a "could this person repeat it in a meeting?" bar.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a plain-speak -y
```

Update later with:

```
npx skills update plain-speak
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/plain-speak/SKILL.md)

## What it does

Pins down the actual reader first — a CFO, a PM, a salesperson, a customer, or (by default) a non-technical manager who knows the product but not the stack — because the same term gets a different plain-language version depending on who's listening. It then produces a repeat-test line: what the thing does, and what it's for, with any unavoidable jargon glossed inline (`idempotent(冪等)`) rather than left to carry meaning on its own. It replies in whatever language the user wrote the request in.

It also reviews an already-written plain-language draft against the same bar, marking each criterion pass or fail and fixing what fails, instead of rewriting blind.

Invoked mid-conversation with nothing attached, the target becomes the preceding turn: it re-explains the last substantive answer, or — if a question was just put to the user and left unanswered — re-poses that question in plain language, option by option, so the user can just answer it.

## When to use

Reach for it to explain a technical term, code snippet, error, or dense engineering text to a non-technical reader, to check whether a plain-language draft actually lands, or to have the answer or question you just got re-done in plain language.

## When not to

Not for de-AI voice cleanup (use `humanizer-zh`), for structuring a whole formal document like a memo or report (use `formal-doc-structure`), or for an RFP (use `rfp-writing`).

## How it works

This skill lowers the **audience** — it doesn't touch voice, structure, or document type. That's a deliberate boundary against three sibling skills that operate on different axes of the same prose:

- `humanizer-zh` strips AI-sounding phrasing from already-finished text — a voice-layer cleanup, not an audience shift.
- `formal-doc-structure` organizes a whole formal business document into the right sections for its type — a structural job, not a translation job.
- `rfp-writing` enforces the specific conventions of an RFP document — a document-type job, distinct from lowering language for a reader.

A passage can need any one of these independently of the others: jargon aimed at a PM can still be in an AI-ish voice, or correctly plain but structurally disorganized. Plain Speak only handles the audience axis.

## Related skills

- **humanizer-zh** — owns removing AI-isms and polishing tone in prose; this skill doesn't touch voice.
- **formal-doc-structure** — owns organizing a whole formal document like a memo or report; this skill only lowers language, not structure.
- **rfp-writing** — owns RFP-specific conventions; those requirements conflict with a plain-language rewrite aimed at a general reader.

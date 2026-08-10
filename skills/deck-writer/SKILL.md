---
name: deck-writer
description: >-
  Plan and write a complete presentation as slide-by-slide Markdown, including the deck brief, narrative outline, assertion-style titles, full on-slide copy, evidence, tables, chart specifications, and speaker notes. Use when the user asks to 規劃簡報內容、寫投影片文案、整理簡報大綱、把主題拆成幾頁, or turn source material into a presentation-ready content deck. Do not invoke for producing a .pptx or rendered slides, visual styling, reviewing an existing deck one issue at a time, or general long-form documents.
version: 0.1.0
license: MIT
compatibility: Any AI coding assistant that supports the agentskills.io SKILL.md format and can read and write Markdown files. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: presentation deck-writing slides storytelling markdown zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "✍️"
---

# Deck Writer

Turn a topic or source bundle into a complete content deck whose argument can be reviewed before anyone spends time on visual production.

Write the deck, not commentary about how a deck might be written.
Every slide must advance the audience from the opening premise toward the requested conclusion or action.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output: option labels, generated-document headings, table column names, not just prose.
If the user explicitly asks for another language, that wins.

Language follows the request, not the source material.
When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output.
Never mirror this file's language into your response.

## Shape the deck

Start from three decisions:

- **Audience and setting:** who will see it, what they already know, and what authority or constraints they bring.
- **Outcome:** the one belief, decision, or action the deck should create.
- **Scale:** slide count or speaking time, plus any sections the user has already committed to.

Recover these from the user's material before asking.
If a missing decision would materially change the deck, ask for the missing decisions together in one compact message.
When the request already contains plausible choices, present two or three mutually exclusive options and state how each one changes the storyline, evidence, or scale.
Do not recommend an option unless the material supports that judgment.
When the request already fixes the audience, outcome, scale, and source material, begin the work immediately.

Treat supplied material as the evidence boundary.
Separate sourced facts from recommendations and mark unresolved gaps instead of inventing plausible numbers, quotes, customer claims, or citations.
Recommendations may organize the work, but they must not turn missing inputs into commitments.
Do not invent numerical targets, day-by-day allocations, severity labels, success thresholds, or implementation details when the source does not provide them.
When the user provides speaking time but no slide count, describe the relative depth and pacing without assigning a page count unless they ask for one.
Name those items as decisions to make or evidence gaps to resolve.
When current external facts are necessary, use available research tools and retain source URLs or document references beside the claims they support.

Distill the material into a small set of content units before assigning slides:

- claims and supporting evidence;
- comparisons and tradeoffs;
- sequences, mechanisms, or causal chains;
- decisions, risks, and actions;
- definitions needed to understand the argument.

Arrange those units into an arc that serves the requested outcome.
Use a checkpoint for a large or materially ambiguous deck: show a compact table with one row per slide and columns for its assertion-style claim, its job or evidence, and its proposed content form, then ask for approval before writing full copy.
Keep supporting caveats outside the table instead of expanding each slide into sub-bullets.
For a bounded request, write the full deck in the same turn and offer revision afterward.

## Write each slide

Give each slide one main claim.
Write its title as the claim the audience should carry forward, rather than a topic label.
Use the body to prove, explain, compare, or operationalize that claim.

Prefer concrete information over ornamental slogans.
Open with the thesis, decision, tension, or strongest evidence unless the setting genuinely requires a formal cover.
End with the requested decision, action, or durable synthesis.

Choose the content form from the material:

- Use a table when exact comparison across repeated fields matters.
- Use a chart specification when a quantitative relationship matters, and include exact data, units, labels, highlight, and source.
- Use a process or sequence when order, dependency, or state change matters.
- Use a compact list when the items are peers and ordering carries no hidden argument.
- Use prose only when a sentence communicates the claim more directly than a diagram or list.

Information density is useful only while the slide remains scannable.
Cut subordinate material before shrinking language into fragments that lose meaning.
Move detail into speaker notes when the audience needs the conclusion on screen but the presenter needs the reasoning at hand.

Preserve the presenter's register when source material reveals one.
For Chinese decks, write natural Taiwan business usage and avoid mainland-China vocabulary and literal translation patterns.

## Artifact contract

Write the result to a path the user names.
Otherwise use `docs/decks/<YYYY-MM-DD>-<slug>/<slug>-content-v1.md` relative to the current project.

Do not overwrite an existing version unless the user explicitly asks.
For revisions, increment `vN` and summarize what changed from the previous version.

Use this document shape:

```markdown
---
deck: <title>
audience: <audience and setting>
outcome: <belief, decision, or action>
slide_count: <number>
created: <YYYY-MM-DD>
language: <locale>
---

# <deck title>

## Slide 01: <assertion-style title>

**Purpose:** <job this slide performs in the argument>
**Layout cue:** <table | chart | process | comparison | list | statement>

<complete on-slide copy or structured content>

**Source notes:** <URLs, file references, or "User-provided material">

### Speaker notes

<optional delivery context that should not appear on the slide>
```

Adapt the body fields to the selected content form.
Keep the frontmatter keys and slide heading pattern stable so downstream presentation tools can parse the artifact without depending on this skill.

## Finish

Read the saved artifact back and verify that:

- slide count matches the brief;
- every slide has one clear claim and a defined role in the arc;
- on-slide copy is complete, with no unmarked placeholders;
- quantitative claims retain units and source notes;
- the ending delivers the requested decision, action, or synthesis;
- the output path exists and the prior version remains intact.

Report the path, slide count, argument arc, and any evidence gaps the presenter must resolve before visual production.
Stop after the content artifact unless the user also asked for rendering or a presentation file.

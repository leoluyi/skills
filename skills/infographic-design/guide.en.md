# Infographic Design

Design-system-grade explanatory graphics — timelines, comparisons, process diagrams — as clean, self-contained SVG or a single HTML file. Language-agnostic, and built to be saved and reshared rather than embedded once and forgotten.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a infographic-design -y
```

Update later with:

```
npx skills update infographic-design
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/infographic-design/SKILL.md)

## What it does

Given a subject and an audience, it plans a graphic before drawing one: picks a message, a palette, a layout archetype (process/flow, comparison, hierarchy, timeline, part-whole, geo, hero-stat), and a signature element the graphic will be remembered by. It then builds that plan as either an SVG file (the default, and the source of truth for PNG/PDF export) or a single self-contained HTML file when motion or interactivity earns its place — directional flow gets animated, structural lines stay still, and `prefers-reduced-motion` is respected. It is language-agnostic — the subject can be described and labeled in any language, and the same process applies whether the output text ends up in English, Chinese, or a mix.

It covers three recurring forms directly:

- A **timeline** — dated or sequenced milestones laid out so the reader can trace progression at a glance.
- A **comparison** — two or more things set against shared criteria, with the distinguishing facts pulled to the surface rather than buried in prose.
- A **process / "how it works"** diagram — a mechanism walked through step by step, with a worked example threading every step rather than abstract boxes and arrows.

It also handles ByteByteGo-style technical explainers (numbered walkthrough welded to the diagram) and single-file animated HTML recaps for a learning session that just ended — that route needs no further prompting once a teaching dialogue wraps up.

Every build follows the same internal discipline regardless of form: a three-level text hierarchy (headline, section, support), an 8-point layout grid with generous whitespace, honest quantity rendering (zero-baseline bars, no 3-D, no dual axes), and a palette bound to fixed neutral/theme/accent roles. None of that is exposed as configuration — it is simply how the skill builds.

## When to use

Reach for it when you need an infographic, one-pager, timeline, comparison, or how-it-works diagram — or a visual recap of something just taught, which needs no further prompting to trigger. It also applies when another skill needs a figure designed for a document it is producing, and to reviewing an existing graphic for what could be improved.

An explicit ask for an infographic, 資訊圖表, 懶人包, or one-pager always qualifies, even when the underlying data is precise — precision and infographic form are not in tension. 懶人包 names the form rather than the content, though: a lookup table wearing that label is still a cheatsheet. Numbers that serve as evidence inside an explanation (a funnel's drop-off, a cache hit-rate) stay in scope too.

## When not to

Skip it for a single standalone chart embedded in analysis output, for dashboards or BI tooling, for slide decks (use a pptx workflow instead), and for explaining a single term in plain language (use plain-speak).

It also steps aside for data-dense graphics where the numbers themselves are the subject or where precise scales matter — annual-results decks, survey findings, statistical graphics. The distinction is what the user names: the exclusion applies only when they ask for a chart, plot, or dashboard. Asking for an infographic that happens to contain precise numbers is still an infographic request.

Two more it declines. A cheatsheet — a dense quick-reference sheet of commands, syntax, parameters, or rules that a reader scans to look something up — is the opposite artifact from an infographic: lookup wants exhaustive rows, this wants one message that lands in a single read. And authoring a knowledge or technical document is knowledge-doc-writing's job, not something to route through this skill. The reverse direction stays open: that skill may call here to design a figure inside its document.

## How it works

The design work — message, palette, layout, hierarchy, honest quantities, accessibility — is a self-critique pass: before delivery, the skill checks its own draft against the brief and, where one exists, against a real-world exemplar of the genre (a published diagram in the same style, held up side by side). That pass is judgment, and it stays judgment; it is not something a script can verify.

Underneath it sits a deterministic gate, run as `python scripts/check.py out.svg --bg "<canvas>" --pad <card-padding>`, which wraps two objective checks:

- `check_contrast.py` — verifies WCAG contrast ratios (4.5:1 for text, 3:1 for large text or graphic elements) so no color pairing is silently unreadable.
- `check_text_fit.py` — catches the most common failure mode in generated SVG: text that overflows its box or gets clipped by its container.

These two are hard gates — they catch reader-harming defects (parse errors, broken references, clipped text, failing contrast) that are true regardless of taste, and a build is not considered finished until `check.py` exits 0. If it flags something, the fix order is: cut words first, then shrink type, and only as a last resort enlarge boxes by growing the canvas while holding the grid's gaps.

Everything else the gate reports — font-naming conventions, emoji use, CSS variable/renderer compatibility, restyle structure — is advisory: a judgment call left to whoever is building the graphic, never a blocking condition. That split mirrors a broader principle this project follows: a check only earns the right to block delivery when it catches an objective, reader-harming defect, not a style preference.

## Related skills

- **plain-speak** — use it instead when the job is explaining one term or concept in words, with no diagram needed.
- A data-visualization workflow (not a skill in this repo) — reach for one instead when the numbers are themselves the subject: charts, dashboards, and BI-style displays where a precise scale matters more than a mechanism's story.

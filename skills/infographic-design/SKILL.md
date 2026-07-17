---
name: infographic-design
description: >-
  Design polished, professional infographics as self-contained SVG or
  single-file HTML. Use when the user asks for an infographic, 資訊圖表,
  懶人包, 一頁式圖表/one-pager, 視覺化摘要, 圖解, a visual summary, a stats
  sheet, a timeline/comparison/process ("how it works") graphic, a poster, or
  says "把這些數據做成圖" / "make this visual / shareable" — even without the
  word "infographic". Also use to review or improve an existing infographic
  design ("幫我看這張圖表哪裡可以改"). Do NOT invoke for a single standalone
  chart embedded in analysis output, for dashboards / BI tooling, for slide
  decks (use a pptx workflow — an infographic is one self-contained canvas,
  not a deck), or for explaining a term in plain language (use plain-speak).
version: 0.1.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: design infographic data-visualization svg visual-communication
  agentskills_spec: "1.0"
  openclaw:
    emoji: "📊"
---

# Infographic Design — 資訊圖表設計

Turn information into a single self-contained visual that communicates one
clear message in under 10 seconds of scanning. A viewer who spends 8 seconds
should walk away with the headline takeaway; a viewer who spends 2 minutes
should get the full supporting story. The three-level hierarchy below serves
both readers at once — that is the core mechanism of this skill.

## When to use

- Use when the deliverable is **one visual canvas** carrying a message:
  infographic, one-pager, visual explainer, timeline/comparison/process
  graphic, stats poster, social-share visual.
- Use when reviewing an existing infographic for design/communication quality.
- Skip when the deliverable is a multi-slide deck, an interactive dashboard,
  or a chart that lives inside a larger report — those have different
  information-density budgets and this skill's rules would over-simplify them.

## Procedure

Follow in order. Skipping step 1 is the most common cause of weak
infographics — every later decision (layout, hierarchy, color) depends on it.

### 1. Distill ONE message

Write a single sentence before touching visuals: "After seeing this, the
viewer should understand ___." An infographic arguing two or three ideas
loses all of them. If the material holds multiple stories, pick the strongest
or propose a series. Cut every fact that doesn't serve the message; round
numbers (68.37% → 68%) unless precision IS the point.

### 2. Pick the output format (recommend, then let the user choose)

Decide format *before* designing — the static-vs-interactive fork changes how
you build, and the target platform sets dimensions (step 5). **Recommend a
default with a one-line why, list the alternatives, and let the user pick.**
If the user already named a format, skip the ask and use it. With no signal,
default to SVG.

| Where it will live / intent | Recommended | Why | Also offer |
|---|---|---|---|
| General, unsure, will be reused & rebranded | **SVG** | scales to any size, restyles in one edit, agent-editable, converts to anything | PNG |
| Interactive — hover reveals, toggles, scroll-story, animation | **HTML** (single file) | the only format that carries interaction | — |
| Paste into chat / social / docs that don't render SVG | **PNG** | renders everywhere, flat | keep SVG source too |
| Print, poster, or a formal one-pager to send | **PDF** | fixed physical size, print-ready | SVG source |
| Must live inside a slide deck | **PPTX** (via the pptx skill) | native deck asset | PNG placed on a slide |

SVG is the **source of truth** for every static case: design in SVG, then
convert to PNG/PDF at the end (see "Building the output"). Only HTML and PPTX
change the actual build — HTML is designed natively, PPTX routes to the pptx
skill. So in practice the ask is really two questions: *static or
interactive?* and *which file do you want to walk away with?*

### 3. Choose a layout archetype

Match archetype to content shape, not aesthetics:

| Content shape | Archetype |
|---|---|
| One dominant statistic + support | Hero-stat |
| Events over time | Timeline |
| Steps in a sequence | Process/flow |
| Two+ options side by side | Comparison |
| Many stats, equal weight | Dashboard grid |
| Parts of a whole thing | Anatomical/labeled |
| Ranked items | Ordered list |
| Geographic data | Map-centric |

Read `references/layouts.md` for wireframes, dimensions per target platform,
and reading-pattern rules (F vs Z) **before** laying anything out.

For **technical/system explainers** (how a protocol, pipeline, or
architecture works — a mechanism, not statistics), also read
`references/bytebytego-style.md`. It captures the numbered-walkthrough style
(badged step numbers welded onto a directional box-and-arrow flow, one-point
diagrams, a worked example entity) that makes complex flows read as a
sequence — layered on the Process/flow and Anatomical archetypes.

### 4. Build the three-level hierarchy

Exactly three levels — more confuses, fewer flattens:

- **L1 — takeaway**: headline + hero number/graphic. Biggest, boldest,
  highest contrast, where the eye lands first. 2–3× larger than body content.
- **L2 — sections**: subheads, key figures, chart titles. A reader of only
  L1+L2 gets the full skeleton.
- **L3 — support**: labels, captions, body text, sources. Quiet and small.

Assign every element a level before styling it. One font family; vary
size/weight/color across levels rather than mixing fonts.

### 5. Compose on a grid with generous whitespace

12-column grid landscape, 4–6 portrait; base spacing unit (8px) and only
multiples of it everywhere. Target ~60% content / 40% air — cramped
infographics read as untrustworthy. Group related items tightly, separate
unrelated groups with whitespace before reaching for boxes or divider lines
(proximity does the organizational work more cleanly).

### 6. Visualize data honestly

For each number pick the encoding that fits the comparison being made — a
single big styled numeral often beats any chart. Hard rules: bar axes start
at zero, no 3-D, no dual axes, area scales with value. Delete chartjunk.
Read `references/charts.md` for the chart-selection table, big-number
styling, and the full integrity rules.

### 7. Apply color and type systems

One dominant neutral / one theme color / one accent, ~60/30/10, accent
reserved for the L1 takeaway (scarcity is what makes it pop). One font
family, three text styles mapped to the three levels. Read
`references/color-typography.md` for ready contrast-checked palettes, chart
palette rules (categorical/sequential/diverging), and exact type scales.

### 8. Accessibility pass (non-negotiable)

- Text contrast ≥ 4.5:1; meaningful graphics ≥ 3:1 vs adjacent colors.
- Never encode meaning in color alone — pair with label, position, pattern,
  or icon. No red/green as sole differentiator.
- Minimum text ~11–12px equivalent at intended viewing size.
- Every chart title states its takeaway ("Sales doubled after launch"), not
  its topic ("Sales 2023–2025").

### 9. Self-critique before delivering

Run and fix failures:

1. Squint test — does the L1 element still dominate with eyes half-closed?
2. 8-second test — can a first-time viewer state the message from a glance?
3. Anything encoded in color alone?
4. Margins/gaps consistent, everything on the grid?
5. Any text that could become an icon, a number, or be deleted?
6. Data source credited (small, L3, bottom)?
7. Numbers add up; axes start where they claim?

## Building the output

Build in whatever the user chose in step 2. In practice:

- **SVG, PNG, or PDF** → **build the SVG**; it is the source of truth for all
  three. Deliver the SVG as-is, or convert at the end (recipes below). Every
  static archetype is built this way.
- **HTML** (interactive) → build a single self-contained `.html` file
  natively; the SVG rules below about hierarchy, palette, and honesty still
  apply, but layout/reveal logic lives in HTML/CSS/JS.
- **PPTX** → build the SVG, then hand off to the pptx skill to place it.

Deliver the source SVG alongside any converted file so the user can restyle
later. Conversion recipes (run after render-and-inspect):

- PNG: `cairosvg in.svg -o out.png -W 1600` (or `rsvg-convert -w 1600`) —
  set width to ~2× the intended display width for crispness.
- PDF (print): `cairosvg in.svg -o out.pdf` — size the `viewBox` to the real
  page (e.g. A4 = 794×1123 at 96dpi) so it prints at true scale.

Core SVG rules (full mechanics in `references/svg-construction.md`, which you
should read before building your first SVG):

- Fix a `viewBox` sized to the archetype (dimensions in
  `references/layouts.md`); design at that size. If content doesn't fit,
  cut content — never shrink whitespace or type.
- Define palette + text styles once in a `<style>` block (CSS variables).
- **SVG text does not wrap.** Break every line manually into separate
  `<text>`/`<tspan>` lines and budget line length up front — overflow runs
  silently off-canvas. This is the #1 SVG failure mode.
- Inline vector icons, not emoji (emoji render inconsistently and clash in
  style). Don't freehand them — use the construction grid + 30-icon starter
  library in `references/icons.md` (paste `<symbol>`s, place with `<use>`,
  colour via `currentColor`).
- **Structure for restyle** (Step 2 promised it): one `:root` `<style>` block
  of CSS variables for the whole palette/type scale, classes mapped to the
  three hierarchy levels, semantic `<g id="…">` groups named by content, and
  region comments — so a later rebrand is a five-line `:root` edit, not a
  hex-hunt. Full pattern in `references/svg-construction.md`.
- Set `font-family` explicitly everywhere; prefer system stacks (they survive
  PNG/PDF conversion, where embedded web fonts often silently drop).
- **Render-and-inspect before delivering**: convert the SVG to PNG
  (`cairosvg` or `rsvg-convert`) and actually look at it. This is how you
  catch text overflow, collisions, uneven spacing, and CJK tofu (□) that
  aren't visible in the markup — run the step-9 checklist against the
  rendered image, not the code.
- **Run the quality gate before delivering** — one command, pass/fail:
  `python scripts/check.py out.svg --bg "<canvas>" --pad <card-padding>`.
  It hard-fails on text overflow, text below WCAG 4.5:1 (resolving each
  label's real background), unnamed fonts, or emoji in text; it warns if the
  SVG isn't structured for restyle. Fix every hard failure before delivering
  (exit 0 = pass). The gate wraps `check_text_fit.py` and `check_contrast.py`,
  which you can still run individually while iterating.
- Export: SVG is the source of truth; convert to PNG/PDF as needed. Deck
  embedding goes through a pptx workflow instead.

## Delivery guard (do not skip)

An infographic is only done when it passes the output-quality guard. This is a
hard precondition for delivery, not a suggestion — **never present or hand off
an infographic that hasn't passed both layers below.**

1. **Deterministic gate** — run `python scripts/check.py out.svg --bg
   "<canvas>" --pad <card-padding>`. It must exit 0 (PASS). It hard-fails on
   text overflow, text under WCAG 4.5:1, unnamed fonts, or emoji in text. If
   it fails, fix and re-run; do not deliver a FAIL.
2. **Judgment guard** — the gate then prints a short self-attest checklist
   (one message, one dominant L1, honest charts, no colour-only encoding,
   source cited). These aren't machine-checkable; confirm each honestly and
   fix any "no" before delivering.

State the gate result to the user (e.g. "quality gate: PASS") when handing
over. HTML output: run the same judgment guard and check contrast/overflow in
the browser, since the SVG script won't apply. This guard is what keeps the
skill's quality promises real rather than aspirational: SVG text doesn't wrap
and low contrast hides in the markup, so the failures it catches — a caption
overflowing its card, a grey label under 4.5:1 — are exactly the ones that
survive a casual eyeball and reach the reader.

## Reviewing an existing infographic

Run the step-9 checklist plus: identify the intended one message (can't find
one → finding #1), count hierarchy levels, check chart honesty (axis
truncation, 3-D, dual axes), spot-check contrast ratios. Deliver findings
ordered by impact, each with a concrete fix.

## Why these rules

Infographics are consumed in seconds, unaided — no presenter, no tooltip, no
second page. Every rule above exists to survive that environment: one
message because attention is a single-shot resource; three levels because
scanning eyes triage, not read; whitespace and grids because perceived order
is perceived credibility; integrity rules because a shareable graphic that
misleads keeps misleading long after context is lost; accessibility because
a graphic that fails 3:1 contrast or color-only encoding silently excludes
part of every audience it reaches.

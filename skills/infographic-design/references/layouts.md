# Layout Archetypes, Dimensions, and Reading Patterns

## Dimensions by use case

Pick dimensions first — layout decisions cascade from aspect ratio.

| Use case | Size (px) | Ratio | Notes |
|---|---|---|---|
| Social share (feed) | 1080 × 1080 or 1080 × 1350 | 1:1 / 4:5 | Very few sections; one hero element |
| Pinterest / long-scroll | 1000 × 2100–3000 | ~1:2–1:3 | Sectioned vertical narrative |
| Presentation slide | 1280 × 720 or 1920 × 1080 | 16:9 | Z-pattern; large type (min ~18px body) |
| Print poster / one-pager | A4/Letter portrait (e.g. 1240 × 1754 @150dpi) | ~1:1.4 | Denser is acceptable; still keep 40% air |
| Blog embed | 800–1200 wide, height as needed | — | Mobile-legible at 50% scale |
| App / chat embed | ~700–900 wide | — | Compact hero-stat or single-section layouts |

## Reading patterns

- **Z-pattern** — for sparse, landscape layouts (slides, hero-stat). Eye moves top-left → top-right → diagonal → bottom-right. Put the headline top-left, hero visual center/right, conclusion or CTA bottom-right.
- **F-pattern** — for text-heavier or vertical layouts. Strong horizontal scan at top, weaker scans below, then a vertical skim down the left edge. Front-load section headers on the left; put key numbers at line starts.
- **Vertical spine** — for timelines and long-scroll: a literal central or left line the eye rides down; alternate content left/right of it for rhythm.

Viewers should never wonder where to look next. If two elements compete, demote one.

## Archetype wireframes

### Hero-stat
```
┌────────────────────────────┐
│  KICKER (small caps)       │
│  Headline takeaway (L1)    │
│                            │
│        68%                 │  ← hero number, 15–25% of canvas height
│   one-line context (L2)    │
│                            │
│ ┌─────┐ ┌─────┐ ┌─────┐    │  ← 3 supporting stat cards (L2/L3)
│ └─────┘ └─────┘ └─────┘    │
│  source · date (L3)        │
└────────────────────────────┘
```
Rules: only ONE hero number. Supporting cards identical in size and structure. If two stats feel hero-worthy, use the dashboard grid instead.

### Timeline
Vertical: central or left spine, nodes at consistent intervals, alternating or single-side cards. Horizontal: band across the middle, dates below, events above. Rules: consistent node styling; scale spacing to time only if you label it — otherwise use even spacing and say so. 5–9 events max; beyond that, group into eras.

### Process / flow
Numbered stages (large numerals are Level 2), uniform stage cards, explicit connectors (arrows/chevrons). Left→right for ≤5 steps landscape; top→bottom or serpentine (S-path with clear connectors) for more. Rule: the numbering must be impossible to miss — number is often the biggest element in each card.

### Comparison
Two columns of identical structure, mirrored row by row so each row compares one attribute. A center divider or "VS" token at top. Rules: same row heights both sides; if one option "wins", let the accent color say so — don't distort sizes. For 3+ options, switch to a comparison table with iconified cells.

### Dashboard grid
Modular card grid (2×2, 2×3, 3×3). Each card = one metric: label (L3, top), value (L2, huge), delta/context (L3). Rules: uniform card size and internal layout; at most one card may break the grid (2× width) to serve as the Level-1 anchor.

### Anatomical / labeled diagram
Central illustration at ~50–60% of canvas, callout labels around it connected by thin leader lines (never crossing). Rules: leader lines all same weight and color; labels aligned to an invisible column left and right, not scattered.

### Ordered list / ranking
Descending visual weight: #1 gets the largest card/type, later items shrink or condense. Big rank numerals as anchors. Rule: the size gradient must be obvious enough to read as ranking without reading the numbers.

## Grid mechanics

- 12-column grid for landscape, 4–6 for portrait/social. Gutter ≈ 2× base spacing unit.
- Pick a base spacing unit (8px is standard) and use only multiples of it for every margin, gap, and padding.
- Outer margin: minimum ~24px at 800px width, scale proportionally; keep all four consistent.
- Section separation: prefer whitespace (2–3× internal gap) over ruled lines; use hairline dividers only if whitespace alone fails.
- 60/40 rule: if the canvas feels full, remove content — never shrink whitespace below ~40%.

## Sequence pitch (stacked steps / rows)

When steps or rows have variable heights (some cards are 2 lines, some 4),
you have two levers: the **anchor pitch** (distance between the fixed
elements — step badges, node centers, row baselines) and the **card height**
(which floats with content). Keep the *anchor pitch even* and let card height
float within it; the eye tracks the evenly-spaced anchors and reads a steady
rhythm even when card sizes differ. Do NOT set the gap *between cards* to a
constant — that makes the anchors uneven and the sequence feels jittery.
Reserve enough pitch for the tallest card so nothing collides.

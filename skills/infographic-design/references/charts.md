# Quantities Inside an Explanation

Quantities enter this skill as *evidence* — the drop-off that proves a funnel
leaks, the hit-rate that justifies a cache, the before/after that motivates a
redesign. Graphics whose numbers are themselves the subject (annual results,
survey findings, statistical analysis) were handed off at the door; if you
find yourself choosing among trend lines, distributions, scatters, or dual
axes, that is the hand-off signal, not a design decision.

## Choosing the embedded form

Ask: what single comparison does this piece of evidence carry?

| Evidence | Embedded form | Avoid |
|---|---|---|
| One standout value | Hero numeral (no chart) | Gauge with one needle |
| A vs B (vs C) | 2–3 horizontal bars | Pie; 3-D bars |
| Part of whole (2–4 parts) | Proportion block: stacked bar / waffle | Pie with tiny slices |
| Progress toward goal | Filled progress bar | Speedometer gauges |
| "X out of Y people" | Icon array / waffle (10×10) | Scaled icons (area illusion) |
| Stage-to-stage loss | Chevron / funnel widths | Sankey unless flows genuinely split |

Simpler wins: a hero number beats a gauge, a waffle beats a pie, three bars
beat a clustered chart. One embedded form = one comparison; a second
comparison is a second element, or it isn't evidence — it's a dataset.

## Hero numbers

The single most powerful quantity-as-evidence element. Pattern:

- Numeral at 4–8× body size, heaviest weight, accent color.
- Unit/symbol (%, $, ×) at ~40–50% of numeral size, lighter weight, so "68" stays the thing the eye lands on and "%" reads as its unit.
- One-line context directly beneath in Level-2 style ("of teams shipped faster").
- Optional micro-visual echo (tiny ring at 68%, or 68 of 100 waffle cells filled) reinforcing the value.
- Round aggressively: 2.7× not 2.71×; "~1 in 3" often lands harder than "34%".

## Icon arrays / waffles

For "X out of Y people" stats: grid of identical icons/cells, X filled in accent, rest in muted neutral. Rules: identical icon size (vary count, never size — area scaling misleads), 10×10 or 5×10 grids read instantly, fill in reading order.

## Data integrity rules (hard rules)

1. **Bar axes start at zero.** Bars encode length; truncation lies. Line charts may use non-zero axes if clearly labeled.
2. **No 3-D**, no perspective, no drop shadows on data marks — all distort perceived values.
3. **Area scales with value.** If a circle represents 2×, its AREA is 2×, not its diameter. Prefer bars/waffles, which avoid the problem.
4. **No dual y-axes** to manufacture correlation. Use two small charts.
5. **Consistent scales** across charts meant to be compared; identical y-ranges for side-by-side comparisons.
6. **Label the actual values** on infographic charts (there's no tooltip). With direct labels, axis ticks and gridlines can usually be deleted entirely.
7. **Cite the source** — small, bottom, Level 3: "Source: [name], [year]".

## Chartjunk deletion pass

For every chart, delete until removal would lose information: chart borders, backgrounds, most gridlines (keep ≤3 faint ones only if values aren't directly labeled), redundant legends (label series directly at line ends / on bars), axis lines when labels suffice, tick marks, repeated units on every label (put "%" once in the title or on the first label).

## Declarative chart titles

Title = the finding, not the topic. "Mobile overtook desktop in 2024" not "Traffic by device, 2020–2025". The topic/measure detail goes in a Level-3 subtitle if needed.

## SVG chart construction tips

- Compute bar/point positions from data with explicit math in your head or a script — misaligned scales from an eyeballed layout are instantly visible.
- Direct-label bars at the bar end (inside if the bar is long enough with contrast-checked text, outside otherwise).
- Round bar corners subtly (2–4px) or not at all; heavy rounding distorts perceived length.
- For lines: 2.5–3px stroke, `stroke-linecap="round"`, dots only on emphasized points, series label at the line's right end in the line's color.

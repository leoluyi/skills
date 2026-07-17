# SVG Construction Mechanics

SVG is the primary output of this skill. It is resolution-independent,
restyleable in one edit, embeddable anywhere, and convertible to PNG/PDF/deck
assets. This file covers the practical mechanics — the environment-specific
knowledge that isn't obvious and that bites on the first build.

## Canvas and coordinates

- Open with `<svg viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg">` at
  the archetype dimensions from `layouts.md`. The `viewBox` is your design
  surface; everything scales from it. Omit fixed `width`/`height` so the host
  controls display size.
- **There is no auto-layout.** Every element is absolutely positioned. Decide
  the grid up front (pick a base unit, e.g. 8, and place on multiples) and
  compute positions — don't nudge by eye. Misalignment is instantly visible
  in the render.
- Group with `<g transform="translate(x,y)">` so a section can be moved as a
  unit; position children relative to the group origin.

## Text — the #1 failure mode

**SVG `<text>` does not wrap.** A long string runs straight off its card or
the canvas, silently. This is the single most common defect — do not trust
your eye, measure it. Rules:

- Break copy into lines yourself, one `<text>` (or `<tspan dy="1.4em">`) per
  line. **Budget the line length before writing copy.** Quick estimate for a
  proportional sans: `max_chars ≈ box_inner_width / (0.55 × font_size)`.
  (e.g. a 330px card with 16px padding = 298px inner, at 13px → ~41 chars;
  a 49-char line overflows.) If a label needs three lines, that's a signal to
  cut words or widen the box, not to let it run.
- **Verify with the script, don't eyeball it.** `python
  scripts/check_text_fit.py --svg out.svg --pad <card-padding>` measures every
  `<text>`, finds the card it sits in (resolving nested `translate()`), and
  flags any line that overflows — including ones that look fine at a glance.
  Also `--text "…" --size N --max <inner-width>` to pre-check a single line.
  Fix every overflow (shorten the copy, widen the box, or drop a size) before
  delivering.
- Set `font-family` on the root `<svg>` and rely on inheritance; override per
  class in the `<style>` block. Always name a concrete family — an unnamed
  font renders as an ugly serif default and breaks on conversion.
- `text-anchor` = `start` / `middle` / `end` for left/center/right. There is
  no vertical-center; approximate the baseline (~0.32em below the visual
  center for typical fonts) or use `dominant-baseline="central"` (well
  supported in browsers, patchy in some converters — verify in the render).
- `<foreignObject>` gives real HTML text wrapping but does **not** render in
  most SVG→PNG/PDF converters. Only use it for browser-only SVG; for anything
  exported, hand-break lines.

## CJK / multilingual text (中文・日本語・한국어)

System font stacks that work for Latin often **drop CJK glyphs to tofu (□)
when converting SVG→PNG/PDF**, because the headless renderer has no CJK font
installed — the browser looked fine, the exported PNG is full of boxes. This
is the most common non-Latin failure. Rules:

- **Name a CJK-capable family explicitly** in the stack, don't rely on
  fallback. Good cross-platform stacks:
  - TC: `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif`
  - SC: `"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif`
  - JP: `"Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif`
- **For export, install the font on the render machine** (the SVG references
  it by name; the converter needs the actual file). E.g.
  `apt-get install fonts-noto-cjk`, then verify with `fc-list | grep -i noto`.
  Always render-and-inspect the PNG specifically for tofu before delivering.
- **Line budgeting is by character count, not word count.** CJK has no spaces
  and each Han/Kana/Hangul glyph is ~1em wide (full-width), so a line fits
  roughly `column_width_px / font_size` characters — easy to budget, but you
  must still hand-break every line (no auto-wrap). Latin words mixed in are
  ~0.5em/char; account for them.
- **Do not letter-space CJK** body text, and avoid ALL-CAPS transforms (no
  effect on Han, and it mangles mixed strings). Kickers that are all-caps in
  English should stay normal-case in CJK.
- CJK reads fine at slightly larger min sizes — bump L3 body ~1px vs the Latin
  scale, since dense glyphs lose legibility faster when small.

## Reusable machinery in `<defs>`

Define once, reference many:

- **Markers** for arrowheads: one per color/direction you use
  (`<marker id="arrTheme" orient="auto">…</marker>`, then
  `marker-end="url(#arrTheme)"`). ByteByteGo-style flows need at least a
  request and a response marker.
- **Filters** for a soft card shadow:
  `<feDropShadow dx="0" dy="1" stdDeviation="2.4" flood-opacity="0.09"/>`.
  Keep shadows subtle; heavy shadows read as dated.
- **Gradients** sparingly — flat or <5% range only (see color-typography).
- Put the palette and text styles in a single `<style>` block using CSS
  custom properties so a restyle is one edit.

## Icons

- Draw as inline `<path>` / primitive shapes on a common size grid (e.g. 24×24
  in their own `<g transform>`). One construction language throughout: all
  line (`fill="none" stroke-width="2"`) or all filled — never mixed.
- Tint with the theme color via `stroke`/`fill`; keep icons monochrome so the
  palette stays controlled. No emoji (inconsistent cross-platform rendering).
- For provider/cloud glyphs, redraw as monochrome silhouettes rather than
  pasting full-color vendor logos.

## Charts in SVG

- Compute every bar length / point position from the data with explicit math
  (in a script if the numbers are non-trivial) — never eyeball a scale.
  `x = leftPad + (value / maxValue) * plotWidth`.
- Direct-label values on the marks (there's no tooltip); with direct labels
  you can usually delete axes and gridlines entirely.
- Bar corners rounded ≤4px or not at all — heavy rounding distorts perceived
  length. Lines: 2.5–3px, `stroke-linecap="round"`, label the series at its
  right end in the line's color.
- Enforce the honesty rules from `charts.md` (zero baseline for bars, no 3-D,
  area ∝ value) — SVG makes it easy to accidentally cheat, so check.

## Accessibility in SVG

- Add `<title>` (and `<desc>` for complex graphics) as the first children of
  `<svg>` for screen readers.
- Contrast and no-color-alone rules from `color-typography.md` apply to the
  rendered pixels — verify against the PNG, not intentions.

## The build → render → inspect loop (do this every time)

Markup can look right and render wrong (overflow, collisions, baseline drift).
Always rasterize and look before delivering:

```bash
# cairosvg (pip install cairosvg) — reliable, no system deps beyond cairo
python3 -c "import cairosvg; cairosvg.svg2png(url='out.svg', write_to='out.png', output_width=820)"
# or rsvg-convert (apt-get install librsvg2-bin)
rsvg-convert -w 820 out.svg -o out.png
```

Then view the PNG and run the step-8 checklist against the *image*: squint
test, text overflow, collisions, consistent gaps, is the L1 element dominant.
Iterate on the SVG, re-render, re-check.

## Export

- **PNG**: `cairosvg`/`rsvg-convert` at `output_width` = intended pixel size
  (2× for retina/social).
- **PDF**: `cairosvg out.svg -o out.pdf` (vector, print-ready).
- **PPTX/DOCX embedding**: go through the pptx/docx skill; embed the PNG (or
  SVG where the tool supports it), don't rebuild the graphic.
- Web/HTML: inline the SVG directly or reference the `.svg` file — no
  conversion needed.

## Icons — use the vocabulary, don't freehand

Freehanding icons is where a set loses coherence. Use the construction grid
and the 30-icon starter library in `references/icons.md`: paste the `<symbol>`
blocks you need into `<defs>`, place with `<use href="#ic-name" width="24"
height="24">`, and colour via CSS `color` (the paths use `currentColor`, so
one rule recolours every icon). Keep all icons in a tier the same rendered
size, and if you must draw a new one, draw it on the same 24-grid / 2px
round-stroke language so it looks native.

## Structuring for restyle

Step 2 promises the user can rebrand the graphic later. That only holds if
the SVG is built so a rebrand touches *one* place, not fifty inline hexes.
Rules:

- **One theme block, CSS custom properties.** Put the whole palette and type
  scale in a single `<style>` on `:root` — `--bg, --theme, --accent, --ink,
  --muted`, plus `--fs-h1` etc. Every element references a variable; **never
  hardcode a hex or font-size inline**. A rebrand is then editing `:root`.

```xml
<style>
  :root{ --bg:#F7F9FC; --theme:#2C5F8A; --accent:#E8683A; --ink:#1A2733; --muted:#5b6b78; }
  .l1{ font-size:34px; font-weight:800; fill:var(--ink); }
  .l2{ font-size:17px; font-weight:700; fill:var(--ink); }
  .l3{ font-size:13px; font-weight:400; fill:var(--muted); }
  .card{ fill:#fff; } .ico{ color:var(--theme); }
</style>
```

- **Classes mapped to the hierarchy**, not one-off styles. Text is `.l1/.l2/
  .l3` (the three levels); surfaces `.card`; icons `.ico`. Changing a level's
  look is one rule. Avoid per-element `fill="..."` that duplicates a class.
- **Separate geometry from colour.** Coordinates and shapes live in the
  markup; all colour/size lives in the `<style>` via classes/vars. A rebrand
  never has to touch a path's `d`.
- **Semantic `<g>` groups, content-named.** Wrap each region in
  `<g id="header">`, `<g id="step-3">`, `<g id="payoff">` — named by *what it
  is*, not `top-left`. An editor (human or agent) can then jump straight to
  "the payoff band."
- **Comment the regions.** `<!-- ===== Step 3: verify ===== -->` before each
  group. Cheap, and it turns a wall of markup into a navigable document.
- **Note the base unit once** in a comment (`<!-- base spacing = 8 -->`)
  since SVG geometry can't use CSS vars; keep gaps as visible multiples of it.

Built this way, "make it match our brand" is a five-line `:root` edit, and an
agent asked to "change step 3's label" finds `<g id="step-3">` immediately.

## Common pitfalls checklist

- [ ] Every `font-family` explicitly named? CJK stack named where needed?
- [ ] Web font used but exporting to PNG/PDF? (will drop — use system font)
- [ ] Arrowheads via shared `<marker>`, not hand-drawn triangles that drift?
- [ ] Icons from the vocabulary, one size per tier, not freehanded?
- [ ] Colour only via `:root` vars/classes — no inline hexes to hunt down?
- [ ] Semantic `<g id>` groups + region comments for later editing?
- [ ] Positions computed, not eyeballed? Gaps all multiples of the base unit?
- [ ] **Ran the gate?** `python scripts/check.py out.svg --bg <canvas> --pad <n>` — text-fit + contrast + font + emoji; exit 0 to deliver.
- [ ] Rendered to PNG and actually looked at before delivering?

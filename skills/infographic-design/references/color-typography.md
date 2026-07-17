# Color and Typography Systems

## The 60/30/10 structure

Every infographic palette has three roles:

- **60% — Dominant neutral**: background + most surfaces. Off-white (#FAFAF7, #F7F8FA) or deep dark (#101418, #14161f) — rarely pure #FFF/#000, which feel harsh.
- **30% — Theme color**: section accents, chart marks, icons. This carries the topic's personality.
- **10% — Accent**: the Level-1 takeaway ONLY. Its scarcity is what makes the hero pop. If the accent appears in more than ~3 places, it stops working.

Plus a text ramp on the neutral: primary text (near-max contrast), secondary (~70%), tertiary/captions (~50% but still ≥4.5:1).

## Ready-to-use palettes (all contrast-checked on their background)

| Mood | Background | Theme | Accent | Text |
|---|---|---|---|---|
| Corporate trust | #F7F9FC | #2C5F8A | #E8683A | #1A2733 |
| Modern tech (dark) | #12151C | #4C7DF0 | #3AD6A3 | #EDF1F7 |
| Editorial warm | #FAF6F0 | #7A5C3E | #C0392B | #2B2118 |
| Health / fresh | #F6FAF7 | #2E7D5B | #F2A93B | #1E3329 |
| Bold playful | #FFF9F2 | #6C4AB6 | #FF7A59 | #241B35 |
| Minimal mono | #FAFAFA | #555555 | #D64545 | #171717 |

Adjust hues to brand colors when the user has them, keeping the role structure.

## Categorical / sequential / diverging (for charts)

- **Categorical** (unordered groups): max 5–6 distinguishable hues at similar lightness; beyond 6, group into "Other" or use one hue + direct labels. Never rely on red-vs-green alone.
- **Sequential** (low→high): single hue, vary lightness monotonically (light = low, dark = high). Derive tints from the theme color.
- **Diverging** (below/above a midpoint): two hues meeting at a neutral midpoint (e.g., blue ↔ warm orange). Reserve red↔green only with a second cue (labels, icons).
- **Emphasis pattern**: often best of all — everything in muted neutral gray, ONE series/bar in the accent. Instant hierarchy, automatic accessibility.

## Accessibility numbers

- Text vs background: ≥ 4.5:1 (large text ≥24px regular / ≥19px bold: ≥3:1).
- Data marks, icons, chart elements vs adjacent colors: ≥ 3:1.
- Quick mental check: on white, colors lighter than ~#949494 fail 3:1; text lighter than ~#767676 fails 4.5:1.
- Every color-encoded meaning gets a redundant cue: direct label, pattern, position, or icon.

## Typography system

**One font family** (two max: display + body). Reliable stacks / pairings:

- Neutral pro: `Inter, -apple-system, "Segoe UI", sans-serif` for everything.
- Editorial: display serif (`Georgia, "Times New Roman", serif` or a loaded serif) + sans body.
- Techy: `"IBM Plex Sans"` or `"Space Grotesk"` display + `Inter` body.
- Numbers: use tabular figures where columns of numbers align (`font-variant-numeric: tabular-nums`).
- CJK (中文/日本語/한국어): name a CJK-capable stack explicitly (e.g. `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif`) — and see the CJK section in `svg-construction.md`, since exported PNGs turn to tofu (□) without the font installed on the render machine.

**Three text styles, mapped to the three hierarchy levels** (example scale at ~1000px width; scale proportionally):

| Style | Size | Weight | Case / color |
|---|---|---|---|
| L1 Headline | 40–56px | 700–800 | Sentence case, primary text or accent |
| L1 Hero numeral | 90–160px | 800 | Accent color |
| L2 Section head / key figure | 20–28px | 600–700 | Primary text |
| L3 Body / label | 13–16px | 400–500 | Secondary text |
| L3 Caption / source / kicker | 10–12px | 500, kickers in ALL-CAPS + letter-spacing 0.08em | Tertiary text |

Rules: line-height ~1.1–1.2 for headlines, 1.4–1.5 for body; line length ≤ ~70 characters; never justify text; ALL-CAPS only for short kickers/labels, never sentences; don't letter-space lowercase body text.

## Icon style

Consistency beats beauty: all icons same construction (all line at one stroke weight — 1.75–2px at 24px size — or all filled), same corner rounding, same optical size, drawn on a common grid. Color them with the theme color or text color, not a rainbow. Draw simple geometric line icons as SVG paths; avoid emoji in professional infographics (inconsistent rendering and style).

## Backgrounds and depth

- Flat color or a very subtle (<5% lightness range) gradient; never busy patterns behind text.
- Cards: background surface 2–4% lighter/darker than canvas, 8–16px radius, either a hairline border (~8% opacity of text color) OR a soft shadow (`0 1px 3px rgba(0,0,0,.08)`) — not both.
- Decorative shapes (blobs, dot grids) only in empty corners at low opacity, never behind data or text.

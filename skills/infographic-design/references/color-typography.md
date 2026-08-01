# Color and Typography Systems

## The 60/30/10 structure

Every infographic palette has three roles:

- **60% — Dominant neutral**: background + most surfaces. Off-white (#FAFAF7, #F7F8FA) or deep dark (#101418, #14161f) — rarely pure #FFF/#000, which feel harsh.
- **30% — Theme color**: section accents, chart marks, icons. This carries the topic's personality.
- **10% — Accent**: the Level-1 takeaway ONLY. Its scarcity is what makes the hero pop. If the accent appears in more than ~3 places, it stops working.

Plus a text ramp on the neutral: primary text (near-max contrast), secondary (~70%), tertiary/captions (~50% but still ≥4.5:1).

## Deriving a palette (method first, examples second)

A palette is derived, not picked from a menu. Name 4–6 hex roles — background,
ink (text ramp), theme, accent, and 2–3 category tints — and derive the hues
from the subject's own world: security borrows deep navy and lock-teal,
health borrows living greens, a hardware topic borrows its enclosure and PCB.
The brief's brand colours always win; slot them into the roles. Then verify
every text-carrying colour with `scripts/check_contrast.py` *before*
committing — a beautiful mid-tone that lands at 3.4:1 is a headings-only
colour, and finding that out after layout is expensive.

The verified starting points below are worked examples of the role
structure, not a catalog — adjust hues to the subject, keep the roles. Every
row is verified with the script (don't trust a table that says "checked" —
run it): every **theme** clears 4.5:1 and is body-text-safe; **accents** are
display-class — hero numerals, badges, marks, fills (≥3:1) — and three also
clear 4.5:1 for small emphasis text: business-teal's teal, modern-tech's
green, editorial-warm's crimson.

| Mood | Background | Theme | Accent | Text |
|---|---|---|---|---|
| Corporate trust | #F7F9FC | #2C5F8A | #E8683A | #1A2733 |
| Business teal (navy + teal) | #F4F7F8 | #21456E | #0E7A72 | #1E2A32 |
| Modern tech (dark) | #12151C | #4C7DF0 | #3AD6A3 | #EDF1F7 |
| Editorial warm | #FAF6F0 | #7A5C3E | #C0392B | #2B2118 |
| Health / fresh | #F6FAF7 | #2E7D5B | #BA7508 | #1E3329 |
| Bold playful | #FFF9F2 | #6C4AB6 | #E5552F | #241B35 |
| Minimal mono | #FAFAFA | #555555 | #D64545 | #171717 |

For muted, low-saturation moods (gallery-quiet, "expensive"): derive them the
same way, but know the trap — grey-tempered mid-tones usually land at
3.3–3.5:1, legal only for large headings and marks, never body text. If a
muted theme fails 4.5:1, keep body text in the dark ink and let the *tints*
(pale category fills with dark text) carry the softness instead. Note the
calibration warning in SKILL.md: warm-cream-plus-terracotta is the named
AI-default look — a muted palette drifting there is a default, not a choice.

## Applying a palette (design principles)

Having a palette isn't using it well. Assign colour by these principles, in
order:

1. **Colour is a job, not decoration.** Give every colour a role before
   placing it — background, text, theme, accent, category. If a colour isn't
   encoding something (structure, category, emphasis, state), it shouldn't be
   there. "It looks nice" is not a role.
2. **Proportion 60/30/10.** ~60% dominant neutral (bg + most surfaces), ~30%
   theme, ~10% accent. The accent's power is its scarcity — ≤3 places (badge
   *systems* excepted; see `bytebytego-style.md`). Overspend it and the eye
   has nowhere to land.
3. **Match contrast to hierarchy.** The three levels are a colour job too:
   highest contrast on L1 (headline/hero), medium on L2, quiet on L3
   (captions/sources). Colour reinforces the reading order the layout sets.
4. **Reserve the accent for the one thing.** It marks the single most
   important element — the takeaway, the focal step, the winning option.
   Accent two things and you halve each one's pull.
5. **Category colour is a promise.** If blue = "client", blue means client
   everywhere and nowhere else; readers learn the legend once, so reusing a
   category hue as decoration breaks the contract. Cap distinct categories at
   ~5–6; beyond that, group.
6. **Value before hue.** Light/dark separation reads faster and more
   universally than hue difference — and survives greyscale and colour
   blindness. Make it parse in greyscale first; hue is a bonus layer, not
   load-bearing. This is why the emphasis pattern (everything muted, one
   element in accent) is the most reliable move here.
7. **Colour reinforces; layout organizes.** Grouping is done by proximity and
   position — colour confirms it, it shouldn't carry structure that spacing
   should. And never encode meaning by colour alone: pair with label,
   position, icon, or pattern.
8. **Restraint reads as quality.** Fewer hues looks more professional.
   Default to one neutral + one accent; add a hue only when it encodes a real
   distinction. The minimal-mono palette leans on this directly.

Applying the specific palettes:
- **Explainer / flow** (bytebytego): theme for the primary flow, accent for
  the focal step + badges, a muted neutral for the secondary (response) path.
- **Dashboard / comparison**: category tints for box/column types; accent on
  the one highlighted metric or winning option.
- **Data / charts**: see the next section — sequential (one hue, vary
  lightness), diverging (two hues around a neutral midpoint), or the emphasis
  pattern (grey + one accent).

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

Rules: line-height ~1.1–1.2 for headlines, 1.4–1.5 for body; line length ≤ ~70 characters; set text ragged-right; reserve ALL-CAPS for short kickers and labels, and keep sentences in sentence case; letter-spacing belongs to ALL-CAPS runs, where it earns its keep.

## Icon style

Consistency beats beauty: all icons same construction (all line at one stroke weight — 1.75–2px at 24px size — or all filled), same corner rounding, same optical size, drawn on a common grid. Color them with the theme color or text color, so the icon set reads as one system. Draw simple geometric line icons as SVG paths — they render identically everywhere and inherit the icon system's stroke weight, which is what makes emoji the wrong tool for a professional infographic.

## Backgrounds and depth

- Flat color or a very subtle (<5% lightness range) gradient — text sits on an even field, so pattern stays out from under it.
- Cards: background surface 2–4% lighter/darker than canvas, 8–16px radius, either a hairline border (~8% opacity of text color) OR a soft shadow (`0 1px 3px rgba(0,0,0,.08)`) — not both.
- Decorative shapes (blobs, dot grids) live in empty corners at low opacity, where data and text are absent.

**One surface = one meaning.** Surfaces are an encoding channel, not
decoration, so fix the vocabulary before you build and hold it everywhere.
A workable default for explanatory graphics: a **card** (canvas-contrast
surface, hairline or shadow) is a *thing* — a component, an actor, a
concept; a **tinted band** behind a group is a *region* — a stage, a
lane, a lesson, a trust boundary; a **dashed tinted box** is *commentary*
— a note, a caveat, a gotcha, something the drawing is telling you about
itself rather than a part of the mechanism. A reader learns this in the
first screen and then relies on it: the moment a note is drawn as a card,
they read an annotation as a component and the mechanism silently gains a
part that does not exist. Whatever vocabulary you choose, the three must
stay visually distinct at a glance, and nothing may carry two meanings.

# ByteByteGo-Style Technical Explainers

A named style variant for **technical/system explainers** — how a protocol,
pipeline, or architecture works. Modeled on the traits the community
consistently identifies in Alex Xu / ByteByteGo diagrams. Reach for this when
the content is a *mechanism* (steps, flows, request paths, component
interactions), not statistics. It layers on top of the **Process/flow** and
**Anatomical/architecture** archetypes; the base rules (one message, three
levels, honesty, accessibility) still apply.

## The signature, and why each part works

1. **Numbered walkthrough welded to the diagram.** Badged step numbers
   (①②③ or "Step 0 / Step 1 …") sit *on* the box-and-arrow flow, and the
   accompanying prose walks the exact same numbers in order. This is the
   core move: the diagram shows the topology, the numbers impose a reading
   sequence onto it, so a static image reads like a walkthrough. Without the
   numbers a flow diagram is a map with no route drawn on it.

2. **One diagram = one point, declaratively framed.** Each visual is
   introduced as "the diagram below shows how X works" and earns its place by
   making a single claim. Complex systems become a *sequence* of
   single-point diagrams (progressive reveal: high-level overview → detailed
   components → scenarios/trade-offs) rather than one everything-diagram.
   Trying to show the whole system at once is the failure mode this prevents.

3. **Explicit directional connectors.** Every arrow shows flow direction
   (request vs response often distinguished by style/color); nothing is an
   undirected line. In the original, connectors are literally animated
   (draw.io flow animation) — in a static SVG, encode direction with
   arrowheads, numbered order, and a request/response color split instead.

4. **A concrete example entity grounds the abstraction.** "Let's take process
   1234…", "a user in Tokyo requests video.mp4…". One named actor threads
   through every step so the abstract flow has something specific to follow.
   Abstract-only flows are the thing readers bounce off.

5. **Cheat-sheet grid variant for taxonomies.** When the content is a
   *catalog* rather than a flow (security topics, design patterns, API
   styles), the same DNA appears as a grid of labeled category tiles, each
   with a 🔹-style header + a few tight bullets. This is the dashboard-grid
   archetype wearing this style's skin.

## Concrete construction (SVG)

- **Step badges**: filled circles in the accent color, white numeral,
  ~28–36px, placed at the exact point on the flow where that step happens.
  The numeral is a Level-2 element — big enough to scan the sequence without
  reading labels.
- **Nodes**: rounded rectangles (8–12px radius), a component icon top-left,
  a bold node name, an optional one-line role beneath. Keep every node the
  same visual weight unless one is deliberately the focus.
- **Icons**: one consistent set — line OR filled, single stroke weight. For
  cloud/architecture, lean on recognizable provider/service glyphs but keep
  them monochrome (tint with theme color), not full-color vendor logos, so
  the palette stays controlled.
- **Connectors**: 2px, arrowhead at the destination, gentle orthogonal
  routing (right-angle elbows) that never crosses another connector where
  avoidable. Request path in the theme color, response/return path in a
  muted neutral or dashed — the split reads instantly.
- **Lanes / grouping**: when steps span tiers (client / gateway / service /
  DB), use faint labeled bands or a light background per tier so the reader
  sees *where* each step happens, not just the order.
- **Layout**: left→right or top→bottom for ≤6 steps; for request/response
  round-trips, a there-and-back path (down the request side, back up the
  response side) mirrors the real interaction.

## Palette and tone

Restrained and technical: one neutral surface, one theme color for the
primary flow, one accent for step badges / the focal component. Avoid the
rainbow — in these diagrams color carries meaning (request vs response,
tier), so spending it on decoration destroys that signal. See
`color-typography.md`; the "Modern tech (dark)" and "Corporate trust"
palettes both suit this style.

**Accent-count exception.** `color-typography.md` says the accent should
appear in ≤3 places. Numbered step badges are a *system* use of the accent —
one repeating element type — so a row of badges counts as **one** accent use,
not one per badge. Keep the badge system, but then spend at most one *other*
accent moment (usually the final payoff band); don't also accent a node, a
title, and an arrow, or the sequence stops reading as the single accented
thing.

## When NOT to use this style

- Stat-driven infographics (use hero-stat / dashboard-grid straight).
- Content with no inherent sequence or component interaction — forcing step
  numbers onto non-sequential material invents an order that misleads.
- Marketing/emotional pieces — this style reads as engineering documentation,
  which is exactly why it's trusted for technical content and wrong for
  persuasion.

## Attribution note

Reproduce the *techniques* (numbered walkthrough, one-point diagrams,
directional flow, worked example), never copy a specific ByteByteGo diagram's
exact composition or assets. The style is a method; the output should be your
own diagram of the user's system.

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

2. **The title is baked into the image.** ByteByteGo diagrams almost always
   carry a prominent title *inside* the graphic — usually a question ("How
   does HTTPS work?") or a declarative claim ("A request travels through five
   layers"). Embed it as the L1 headline in the SVG/`<figure>` itself, top of
   the canvas, not only in the surrounding prose. This is what makes the image
   **self-contained and shareable**: when it's reposted stripped of its
   article, the title travels with it and the diagram still explains itself.
   Default to a question or a one-line finding, not a bare topic label ("HTTPS
   handshake") — the phrasing states the point the diagram makes.

3. **One diagram = one point.** Each visual earns its place by making a single
   claim (the title above *is* that claim). Complex systems become a
   *sequence* of single-point diagrams (progressive reveal: high-level
   overview → detailed components → scenarios/trade-offs) rather than one
   everything-diagram. Trying to show the whole system at once is the failure
   mode this prevents.

4. **Explicit directional connectors.** Every arrow shows flow direction
   (request vs response often distinguished by style/color); nothing is an
   undirected line. In the original, connectors are literally animated
   (draw.io flow animation). **For HTML output**, reproduce that: give each
   directional flow line `class="flow"` and the baseline CSS in
   `svg-construction.md` animates it (marching dashes, auto-off under
   `prefers-reduced-motion`). **For static output** (SVG-as-image/PNG/PDF),
   encode direction with arrowheads, numbered order, and a request/response
   color split instead. Either way, structural/containment lines stay still —
   only flow moves.

5. **A concrete example entity grounds the abstraction.** "Let's take process
   1234…", "a user in Tokyo requests video.mp4…". One named actor threads
   through every step so the abstract flow has something specific to follow.
   Abstract-only flows are the thing readers bounce off.

6. **Cheat-sheet grid variant for taxonomies.** When the content is a
   *catalog* rather than a flow (security topics, design patterns, API
   styles), the same DNA appears as a grid of labeled category tiles, each
   with a 🔹-style header + a few tight bullets. This is the dashboard-grid
   archetype wearing this style's skin.

## Making abstract concepts visual (the harder, more valuable half)

The signature above draws *systems* (components and flows). The deeper skill
is making *intangible concepts* — a request, a key, consistency, hashing,
consensus — legible. The move is always the same: **give the invisible a body
and a place.** Concretely:

1. **Concretize the invisible.** Represent an intangible as a small labeled
   object that exists somewhere on the diagram. A "request" is a chip riding
   an arrow; a "session key" is a key glyph; an "encrypted payload" is a chip
   with a lock on it. Static SVG: place the token *on* the connector at the
   step where it exists, and show its **transformation across steps** (a
   plaintext chip at step 2 becomes a lock+chip at step 3) — that before→after
   is how you render an invisible operation like encryption or hashing.

2. **Spatialize the logical relationship.** Dependency, flow, hierarchy, and
   containment become position, arrows, nesting, and lanes; prose carries only
   what geometry cannot. If a caption merely narrates what an arrow already
   shows, cut the caption. Static
   SVG: tiers as labeled horizontal bands, "A is part of B" as a nested
   rounded-rect, "A depends on B" as a directed edge, "these are peers" as
   equal-weight siblings on one row.

3. **Anchor the abstraction to one familiar system.** Teach the generic
   mechanism through a concrete instance the reader already knows, and show
   both at once. Static SVG: label the abstract node ("hash function") and put
   a worked instance directly beneath it ("bit.ly/xyz → 3f2a"). The concrete
   example carries the concept; the generic label makes it transferable.

4. **Make the trade-off spatial.** Abstract design tensions (consistency vs
   availability, push vs pull) become a side-by-side comparison with visible
   pros/cons, so the tension is *seen*, not read. Static SVG: the comparison
   archetype — one column per approach, aligned pro/con rows (tick/cross by
   shape, with colour as reinforcement so the mark survives a greyscale print).

5. **Sequence a progressive reveal.** ByteByteGo animates overview → detail →
   trade-offs; a static canvas can't, so **serialize** it: a strip of small
   multiples (or numbered zoom-ins), each making one point, read left to
   right. Give each depth its own frame: three depths in one frame is the
   density trap that makes a "one image" oversimplify.

Guiding test: for every abstract noun in the content, ask "what object is it,
and where does it live on the canvas?" If you can't answer, you're about to
write a label where you should draw a thing.

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
  routing (right-angle elbows) that routes around other connectors wherever the
  layout allows. Request path in the theme color, response/return path in a
  muted neutral or dashed — the split reads instantly.
- **Lanes / grouping**: when steps span tiers (client / gateway / service /
  DB), use faint labeled bands or a light background per tier so the reader
  sees *where* each step happens, not just the order.
- **Layout**: left→right or top→bottom for ≤6 steps; for request/response
  round-trips, a there-and-back path (down the request side, back up the
  response side) mirrors the real interaction.

## Base-position information density

At the home position (SKILL step 1), density is the deliverable —
but density means *more relations shown*, not more pixels filled. Three rules
that separate a reference diagram from a thinned-out walkthrough:

1. **The payload rides on the arrow.** In a message/sequence diagram, what
   crosses the wire is the content. Put it *on* the connector as small chips
   ("cipher suites", "server random · B"), not only in a prose card below —
   the arrow then answers "what moved?" at the point where it moves.

2. **Ownership by position.** Which party acts is encoded by *where* the card
   sits: client-side work hangs off the client's lifeline, server-side off
   the server's. A card floating between lanes loses the who-does-this
   information the lanes exist to carry.

3. **Draw derivations as data-flow.** A sentence stating the conclusion is the
   thing this replaces. If the
   mechanism's point is that things *combine* (inputs → output, A+B+C →
   session key), show converging arrows into the result — on every party that
   performs the combination, mirrored if both do. The converging mini-diagram
   lets the reader verify the claim instead of taking it on trust. Give
   recurring tokens a letter badge (A/B/C) plus a one-line footer legend.

The failure mode these prevent: drift below the home position — parties
spatialized but payloads, ownership, and the causal join thinned into
captions. Density does not fall because drawing relations is hard; it falls
only when a dial was deliberately pulled. If the mechanism's core relation
isn't *drawn*, the diagram isn't at home yet.

## Palette and tone

Restrained and technical: one neutral surface, one theme color for the
primary flow, one accent for step badges / the focal component. Hold the
palette to those three — in these diagrams color carries meaning (request vs
response, tier), so every hue spent on decoration costs signal. See
`color-typography.md`; the "Modern tech (dark)" and "Corporate trust"
palettes both suit this style.

**Accent-count exception.** `color-typography.md` says the accent should
appear in ≤3 places. Numbered step badges are a *system* use of the accent —
one repeating element type — so a row of badges counts as **one** accent use,
not one per badge. Keep the badge system, but then spend at most one *other*
accent moment (usually the final payoff band). Once a node, a title and an
arrow each take the accent too, the sequence stops reading as the single
accented thing.

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

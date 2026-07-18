# Learn-Loop Viz — 學習迴圈視覺化

A named chart type for turning a **completed teaching dialogue** (a guided
teaching session, a tutoring thread, any multi-turn lesson) into ONE
long-scroll visual that replays the learning journey.

In dial terms (SKILL step 1) this is the canonical **retention pull**: the
graphic stays at the home position on density and dimension — nothing about
teaching licenses thinner content — and pulls exactly two dials toward the
reader: *redundancy* (dual naming) and *familiarity* (the analogy
vocabulary). Both pulls are provenance-bound: the analogies and checkpoints
come from the source dialogue, harvested below, never invented at drawing
time. It layers on top of `bytebytego-style.md` — read that file first;
everything there still applies. This file adds only what is unique to
visualizing *how something was learned*.

The core claim: after a good lesson, the learner's retrieval path IS the
lesson's path. A recap diagram that reorganizes the material into
"logical" textbook order destroys that path. This chart type preserves it.

## Step 0 — Harvest the dialogue (do this before any layout)

Mine the source conversation for six assets. If an asset is missing, note
it and degrade gracefully (see "When NOT to use"):

1. **Concept sequence in the order actually taught** — not the order a
   textbook would use. List each lesson/segment as a candidate PART.
2. **The analogy system** — the metaphor vocabulary built up during the
   lessons (e.g. 園區=叢集、房子=Pod、櫃檯=Ingress、總機=kube-proxy、
   查號台=DNS). Collect the full term↔analogy mapping table.
3. **The worked example entity** — the concrete actor that threaded the
   lessons (e.g. 一個打開 shop.example.com/api/orders 的請求). If the
   lessons used one, the diagram MUST use the same one.
4. **Checkpoint questions and the misconception each caught** — every
   quiz moment, especially ones the learner got wrong or that revealed a
   trap (ping 不通 ClusterIP 是正常的、門禁忘了放行 DNS)。
5. **Contrast pairs taught via comparison** — anything the lesson taught
   as "A vs B" (iptables 翻手冊 vs eBPF 直查)。
6. **The convergence sentence** — the final one-line summary the learner
   accepted or produced (「大門管進來、查號台管名字、總機管轉接…」)。

## The signature (beyond ByteByteGo)

1. **Order the sections by the concept chain the lesson built — which,
   after a lesson that worked, is the order it was taught in. This is the
   one rule that cannot be traded.** Each section rests on the a-ha of the
   one before it: a reader who has just understood section N holds exactly
   what section N+1 assumes, and nothing in section N+1 requires a concept
   that has not been earned yet. That dependency chain is the retrieval
   path. The taught order matters because a lesson that held together
   *had* to build its concepts in a workable order — not because the
   transcript is sacred. Title each section by its place in the course
   (第 1 課 / Lesson 1), not by the part of the system it covers.

   **Fold, don't transcribe.** Real dialogues wander: a clarification that
   corrects an earlier simplification, a tangent, an answer given out of
   order, a question the learner circled back to. Fold each of those into
   the concept it belongs to, and let a genuine detour become a note or an
   extra lesson where it happened. Keep the chain, not the timestamps.

   **Never re-sort** into the order a reference doc, an architecture
   diagram, or a request's journey would use — that destroys the only
   thing this chart type exists to preserve. The trap: the dialogue's own
   closing summary is usually in journey order
   ("進來的路:櫃檯 → 小門 → 改寫 → 門牌"). That sentence belongs in the
   payoff band and **only** there; it is a summary, not a section plan. If
   you find yourself opening with "the request's journey", you have
   silently switched to a reference diagram — go back to the harvest and
   re-sort by lesson.
2. **Dual vocabulary everywhere.** Every component node shows the
   technical term as its title AND the lesson's analogy as a small chip
   (top-right of the node). A footer line maps the full analogy↔term
   table so the chips stay decodable outside the conversation.
3. **Checkpoints become margin notes.** Each harvested quiz/gotcha turns
   into a dashed-border note box placed adjacent to the step it tests —
   "the exam becomes the margin notes". These are the highest-retention items for the learner; never cut them before cutting body copy.
4. **Worked example and payoff** follow `bytebytego-style.md` unchanged —
   with one addition each: the example's concrete values stay identical
   across all PARTs, and the payoff band is the learner's own convergence
   sentence near-verbatim, never a new summary invented for the graphic.
5. **Provenance line** in the footer: 「依 YYYY-MM ○○ 學習對話整理 ·
   示意圖經簡化,數值為範例」。 A learn-loop viz is a record of a
   specific dialogue; say so.

## Construction addenda (SVG)

- Long-scroll portrait, 1000 × 2500–3500. All ByteByteGo mechanics apply
  (badges, lanes, orthogonal directional connectors, request vs
  query/control split).
- **Analogy chip**: rounded rect (h≈20, r=10), band-tint fill, theme-color
  10.5px bold text, top-right inside the node card.
- **Note box** (checkpoint gotcha): dashed hairline border, band-tint
  fill (NOT white — must read as annotation, not component), small info
  icon + bold 13px title + 12px body. House rule: white card w/ shadow =
  component; dashed tinted box = note.
- **Comparison inset**: render the harvested A-vs-B as two mini-visuals
  ("翻手冊" = stacked rule rows with the hit row outlined; "直查" = one
  key→value table), not as prose.
- Accent budget unchanged from bytebytego-style.md: step-badge system +
  the payoff band only.

## Required output: one self-contained animated HTML file

This route has no format decision — the deliverable is a single HTML file,
always, and the request does not need to ask for motion. A learning recap is
scrolled and re-opened later, so it gets the full construction vocabulary by
default rather than on request: the flow-animation baseline and page frame
(`references/svg-construction.md`, "HTML output"), an icon on every recurring
node type (`references/icons.md`), and the card / band / note surface
vocabulary (`references/color-typography.md`). None of these are upgrades
here; a recap without landmarks is a wall of text nobody revisits. Ship the
SVG source alongside the HTML, and skip SKILL step 2 entirely.

Route-specific on top of that baseline: bands are *lessons*, so a band's
label is the lesson title; and the request path and the query/control path
are the two flow types this subject always has, so they always take the two
dash patterns.

## When NOT to use

- The material was never taught in dialogue — no analogy system, no
  checkpoints to harvest. Use plain bytebytego-style instead; faking
  "checkpoints" invents a lesson that didn't happen.
- Single concept, single mechanism — one ordinary diagram suffices.
- The dialogue taught opinions/selection advice rather than mechanisms
  (選型比較) — that is a Comparison archetype, not a learn-loop.

## Gate additions (self-attest alongside the standard checklist)

- [ ] Every harvested checkpoint appears as a note box?
- [ ] Every analogy chip is decodable via the footer mapping?
- [ ] Section order matches the taught order, zoom-ins included?
- [ ] The payoff band is the learner's convergence sentence, not a new
      summary invented for the graphic?
- [ ] Worked-example values consistent across all PARTs?

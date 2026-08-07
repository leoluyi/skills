# Node: `layoutspec` 版面規格

Specify how one slide — or a small set that has to look like siblings — should be laid out: what occupies the frame, at what visual weight, in what order the eye takes it, and what gets left out. The artifact is a specification a human can execute in PowerPoint, Keynote, or Google Slides, plus a paste-ready prompt for whatever image tool the presenter already uses.

This node produces a spec and a prompt, not an image. Say so in the first exchange rather than letting the presenter wait for a picture that is not coming — what they get is something they or a designer can build, and a prompt they can paste into whatever image tool they already use. That holds regardless of what the surrounding environment can render; the deliverable here is the specification, and a picture generated without one is a mood board.

Going wrong looks like a spec full of numbers — 「標題 32pt，靠左 1.2cm」 — that reads as precise and executes as nothing, because it was written against an aspect ratio and template the presenter is not using. The spec that survives contact names weight and order: what is largest, what the eye lands on first, what is deliberately quiet.

## Entry check

Ask which slide, and what it has to accomplish. One slide at a time, or one small set that shares a pattern — a spec covering nine unrelated slides is nine thin specs, and each of them would have been better alone.

Read `docs/deck-consulting/slidecheck.md` and `docs/deck-consulting/outline.md` if they exist; either one tells you what this slide is for and saves the first three questions. Neither is required. Without them, ask directly what single thing the audience should walk away from this slide believing, and note in the artifact that the spec was built from that answer rather than from a structure on disk.

Ask the viewing condition — projected, read on screen, or both — and whether the deck has a template with fixed fonts and colours already. A spec that ignores an existing template gets translated back into it badly by whoever executes it.

Ask who will build the slide. A spec for the presenter working alone at 11pm is a different document from a spec handed to a designer: the first names moves inside the tools they have, the second can name intent and leave execution open. Getting this wrong produces a spec that is either patronising or unbuildable.

## Steps

1. **Name the slide's single message in one sentence.** Not its topic. If the answer contains 「以及」 or a comma splice, the slide is two slides, and that is worth saying now rather than after the layout is specified. Complete when the user has confirmed a sentence you could put in the headline.

2. **Inventory what is available and what is required.** Which numbers, which chart, which screenshot, which quote actually exist. Mark anything the presenter would have to create or obtain — a spec resting on a photograph nobody has is a spec that stalls. Complete when every element in the spec is either in hand or explicitly flagged as needing production.

3. **Offer layout families, labelled by what they do to the audience.** Derive them from this slide's message: 單一數字撐全頁, 左右對比, 主張加三項證據, 流程推進, 時間軸, 圖為主文字為註. For each, one line on what it makes easy and what it makes hard. Complete when the user picks one, or describes a shape in their own words.

4. **Rank every element by visual weight, first to last.** Assign each a place in the reading order — what the eye lands on, what it goes to next, what it finds only if it looks. Anything you cannot place in the order is a candidate for removal; say so and let the user decide. Complete when the ranking is a single ordered list with no ties.

5. **Assign colour roles.** Decide the one thing colour is encoding on this slide, and neutralise everything else. Where the template supplies a palette, work inside it. Complete when every coloured element's colour has a stated reason.

6. **Write the spec in relative terms** — proportion of the frame, relative weight, position expressed as a region, spacing expressed as relationships rather than measurements. Where the presenter has a fixed template, give template-anchored values as a secondary line, never as the primary spec. Complete when every element in the ranking has a stated size relationship and a region, with no bare pixel or point value standing alone.

7. **Write the image prompt, scoped to what image tools are good at.** Composition, background, illustration, mood, empty regions reserved for text — never the actual words. Complete when the prompt could be pasted into any image tool by someone who has not read the rest of the artifact.

8. **Write the spec** to `docs/deck-consulting/layoutspec.md` in the shape below, then say in one line what the layout is optimising for and what it gave up to get it.

## Craft

**Weight and order beat pixel values, and the reason is not portability alone.** Numbers describe a rendering; weight and order describe what the audience experiences, which is the thing actually being designed. A spec that says 「這個數字要壓過頁面上其他所有東西」 executes correctly at any aspect ratio, in any template, by any person, and stays correct when the deck gets restyled next quarter. A spec that says 「96pt」 is wrong the moment the slide is 4:3, or the number turns out to be six digits, or the template's heading font has a larger x-height than the one you imagined.

Give numbers as a convenience under the intent, never in place of it. When the presenter has a template in front of them, a concrete starting value saves them ten minutes — but it goes on the second line, marked as a starting point, so that when it does not fit they adjust the number instead of abandoning the intent.

**Reading order is a claim about the argument.** Deciding what the eye reaches first is deciding what the audience concludes before they have the rest of the evidence — which is usually the right move, since they will form a view in the first two seconds regardless. If the intended first landing is the conclusion, the layout has to make it heaviest. If the intended landing is the surprising number, the conclusion becomes a caption under it and the number gets the frame.

When the reading order and the argument disagree, the audience follows the reading order — every time, and without noticing they did. This is why the ranking in step 4 is the load-bearing part of the whole spec: get it right and a plain slide works, get it wrong and no amount of styling recovers it.

**Never ask an image tool to render the slide's real text.** Image models garble type, invent letterforms, cannot be edited afterwards, and will not match the deck's font. The prompt asks for the plate — background, illustration, structure, and explicitly reserved empty regions where the text will go — and the real words are set in the slide tool on top, where they stay editable, searchable, and on-brand.

Say this in the artifact next to the prompt. A presenter who does not know it will paste the headline into the prompt, get back something that looks almost right at thumbnail size, and only discover the mangled characters when it is on the wall.

**An image prompt is a description of a picture, not a description of a slide.** Image tools respond to subject, composition, viewpoint, lighting, medium, and mood; they do not respond to 「左邊放三個要點」. Translate the spec: a reserved text region becomes 「畫面左側三分之一保持乾淨、低對比、無主體」, a mood becomes a named medium and palette, a corporate register becomes a style reference rather than an adjective. Keep it to a few sentences — long prompts do not produce more control, they produce averaging.

Say what the prompt is for, too. Most slides in a business deck do not want a generated image at all; they want white space and one chart. Offer the prompt where an image genuinely earns the frame — an opening slide, a section break, a concept with no data behind it — and say plainly when this slide is not one of those, instead of generating a prompt because the node has a slot for it.

**When space runs short, the order of retreat is fixed.** Cut words first, then remove an element, then reduce the chart's series, and shrink the type last. The cheap move is always shrinking type, and it is the one move that turns a crowded slide into an unreadable one. Every other move at least leaves the survivors legible.

Write the retreat order into the spec itself rather than only saying it here. Whoever executes the layout will hit the wall at 11pm and take the cheapest path unless the document in front of them says which path to take.

**Specify the empty space as an element, or it will be filled.** Blank regions left unnamed read as unfinished to the person building the slide, and something migrates in. Give the empty region a job — 「這塊留白是讓標題有份量的原因」 — and it survives review.

The same applies to the person reviewing the deck later, who will look at the space and ask why nothing is there. A named reason is an answer; an unnamed gap is an invitation.

**The chart type is a layout decision, and it usually arrives pre-decided.** The presenter brings whatever the spreadsheet produced, and specifying a layout around it inherits a choice nobody made deliberately. Ask what the chart has to show — a comparison between two things, a trend, a share of a whole, a distribution — and let that pick the form. A stacked bar defended as 「資料就是這樣」 is often three numbers that wanted to be three words.

When you change the chart type, say what the old one made hard, because the presenter has looked at it long enough to have stopped seeing it.

**Two elements land; the third is optional.** A projected slide gets a headline and one thing — a chart, an image, a number, a diagram. Whatever is third arrives only if the first two left the reader with attention to spare, which under presentation conditions they usually do not. This is not a limit on how much can fit; it is a statement about what will be received. Specify the third element knowing it is a bonus, and never let the argument depend on it.

**A spec for a set of slides is a spec for one slide plus a rule for what varies.** Say which parts are fixed across the set (position of the headline, the colour role, the reading order) and which slot changes per slide. Specifying each member separately guarantees drift.

Drift across sibling slides is more noticeable than any single slide's flaws, because the audience sees the pages in sequence and reads the inconsistency as a mistake even when each page is fine alone. Write the fixed parts once and the varying slot as a list.

**Say what the layout gives up.** Every layout family buys something at a price. 單一數字撐全頁 lands hard and carries no nuance, which is a problem in a room that will ask about methodology. 左右對比 is legible instantly and forces a false symmetry when the two sides are not actually comparable. 流程推進 makes sequence obvious and makes the steps look equally weighted when one of them is the whole difficulty.

Name the cost as part of the recommendation. It is what lets the presenter overrule you knowledgeably when they know something about the room that you do not — and they usually do.

## Output shape

Write `docs/deck-consulting/layoutspec.md` with these sections. When the spec covers a set, repeat 視覺層級 and 閱讀動線 per slide and keep everything else shared.

- **這頁要說的一句話** — the single message, verbatim, as confirmed by the user.
- **版面家族與取捨** — the chosen family, what it optimises, what it sacrifices.
- **視覺層級** — an ordered list, heaviest first, each item naming its element and why it sits there.
- **閱讀動線** — where the eye lands, and where it goes next, in two or three sentences.
- **色彩角色** — what colour encodes here; everything else stated as neutral.
- **留白與空間** — the regions deliberately left empty and what each is doing.
- **素材清單** — every element, marked 已有 or 待製作.
- **空間不足時的取捨順序** — 先刪字，再減元素，最後才縮字級.
- **生圖提示詞** — a paste-ready prompt in a fenced block, describing the plate only, with a line above it stating that the real text is set afterwards in the slide tool and that this skill does not generate the image itself.

The spec should be short enough to keep open in a second window while building the slide. If it grows past a page, the ranking in 視覺層級 is doing the work and the rest is commentary — cut back to the ordering, the colour role, and the retreat order.

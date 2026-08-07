# Deck Consulting

Deck Consulting advises on a presentation the way a senior consultant would — but not all at once. The work is cut into eleven nodes, entered one at a time, and each node leaves an artifact on disk so the next one picks up from that instead of re-reading the raw material from scratch.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a deck-consulting -y
```

To pull updates later:

```
npx skills update deck-consulting
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/deck-consulting/SKILL.md)

## What it does

It replaces an unbounded "have a look at my deck" with a list of nodes, each one sitting's work:

| Node | What it settles | Reads |
|---|---|---|
| `positioning` 溝通定位 | Who is in the room, what they can grant, the best outcome and the floor | — |
| `distill` 素材汰選 | Raw material cut to a chosen number of points at a chosen emphasis | positioning |
| `headline` 主張式標題 | Descriptive labels rewritten as assertions someone could disagree with | content or outline, positioning |
| `outline` 骨架定形 | Structural form, the axis the sections divide on, the detail headings | positioning |
| `onepager` 單頁濃縮 | The whole argument on one page: 主張, 綱要, the ask | outline, positioning |
| `storyline` 敘事編排 | Order, spoken transitions, an arc sayable in one breath | outline, positioning |
| `opening` 破題定錨 | The hook, the framing, and what the room is promised | positioning, outline |
| `closing` 收束提請 | A recap mirroring the opening, and the ask | positioning, opening |
| `delivery` 口說轉譯 | Rhetorical device and register, written out as speakable script | any content node, positioning |
| `slidecheck` 逐頁診斷 | Per-slide layout findings ranked by reader cost, each with one edit | positioning (optional) |
| `layoutspec` 排版藍圖 | A layout spec for one slide, plus a paste-ready image-tool prompt | slidecheck or outline |

A node loads its own reference file only on entry, so a session that only wants five headlines rewritten never pays for the other ten. When a node finishes it names the one or two nodes that now make sense and stops — it does not chain onward uninvited, because each node is a decision the presenter makes, not a pipeline stage.

## When to use

Reach for it when you have raw material and a date, and need one part of the deck settled: what the presentation is actually for, how the case is structured, what the titles assert, how the sections connect, how it opens and closes — or what a deck someone else built is costing the room on layout.

## When not to

Not for producing the .pptx file itself (what you get is the spec and the content, not the file), for designing an infographic (use infographic-design), for stripping AI-writing patterns out of Chinese prose (use humanizer-zh), or for writing a 簽呈 or an evaluation report (use formal-doc-structure).

## How it works

**State lives in files, not in the conversation.** Node artifacts are plain Markdown under `docs/deck-consulting/`: `positioning.md`, `outline.md` (structure plus the one-pager), `content.md` (distilled points and headlines), `script.md` (故事線, 開場, 收尾, 講稿 — one section per node), `slidecheck.md`, `layoutspec.md`. Where a file is shared, each node owns one named section and rewrites only that one; where a change makes a sibling section wrong, it says so rather than editing it. That is what lets you come back a week later — the thing being resumed is the file, not last week's conversation.

Revise something upstream and it names which downstream artifacts just went stale, and offers to re-run them. A rewritten `outline.md` sitting silently next to a `script.md` that contradicts it is the outcome this file contract exists to prevent.

**No node blocks.** A missing input is named along with what proceeding without it costs — usually that the output has no standard to be judged against, so it comes out generically competent instead of pointed — and then you get both options: run the prerequisite first, or work from whatever is at hand. Someone who wants five headlines rewritten in two minutes gets five headlines rewritten in two minutes.

Three entry scenarios cover most sessions:

- **A full run from raw material.** A pile of material and a date: start at `positioning` to fix the room, the stakes, the best outcome and the floor, then `distill` or `outline` depending on how raw the material is, then `onepager`, `storyline`, `opening`, `closing`, and `delivery` if a script is needed. Each stop waits for your confirmation before the next.
- **A headline-only quick pass.** Say "rewrite these titles so they say something" and paste the titles. `headline` tells you that without `positioning.md` the headlines will be accurate but not aimed, then does what you chose. Titles with no facts under them come back as specific questions to answer, not as a confident sentence invented to fill the slot.
- **Picking up a deck someone else built.** Nothing but a deck and a meeting on Thursday: enter `slidecheck`. It states the viewing condition it is assuming and asks in the same breath rather than waiting on an answer (that answer moves half the judgements, and the findings it would flip are marked as such), reads each slide for the single thing it communicates, then ranks findings by what they cost the reader — 讀不到 (below-floor type, clipping, contrast), 讀錯 (a misleading axis, colour implying a grouping the data lacks), 讀得慢 (no hierarchy, a slide making two arguments). Findings drawn from anything weaker than a legible screenshot are marked 推測 and written as a question you can settle in ten seconds. Slides whose fix is a rebuild rather than an edit hand off to `layoutspec`.

**Every claim traces back to something you supplied.** A number, a name, or what the CFO cares about that the material does not contain gets asked for or marked as a gap. Invented content is the one failure a presenter cannot catch before they are standing in front of the room, so the rule applies at every node — and cuts get the same treatment: anything dropped is named along with the part of the positioning it lost against, because a cut you cannot audit is a cut you will quietly reinstate.

## Related skills

- **infographic-design** — use it instead when what you want is a standalone explanatory graphic rather than a presentation's content and layout.
- **humanizer-zh** — use it instead once the script and headlines are structurally settled and the remaining job is stripping AI-writing patterns from the Chinese.
- **formal-doc-structure** — use it instead when the deliverable is a 簽呈, 會議紀錄 or evaluation report rather than something spoken to a room.
- **briefing-outline** — use it instead when you're distilling several sources into a 說明提綱 for a manager rather than designing a presentation that asks for something.

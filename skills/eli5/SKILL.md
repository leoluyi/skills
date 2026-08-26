---
name: eli5
description: >-
  Explain a topic to someone who knows nothing about it, as a single-file HTML
  picture explainer: big visuals, very few words, no jargon. Trigger on /eli5
  <topic>, 「用五歲小孩聽得懂的方式解釋」, 「幫我做一個超簡單的圖解說明」,
  "explain X like I'm 5", or "make me a dead-simple picture explainer of X".
  Not for plain-language rewrites of existing prose (plain-speak), dense
  information graphics for informed readers (infographic-design), slide decks,
  or accurate technical documentation.
app-description: >-
  把一個主題做成「完全外行也看得懂」的單檔 HTML 圖解：畫面大、字少、零術語，用日常生活的比喻代替專有名詞。
  觸發：/eli5 <主題>、「用五歲小孩聽得懂的方式解釋」、「幫我做一個超簡單的圖解」。
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. Output is a self-contained HTML file; no external tools or APIs required.
metadata:
  author: Lu Yi
  tags: explainer learning visual html teaching
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F9F8"
  provenance: >-
    Adapted from the community eli5 plugin by Thariq Shihipar
    (anthropics/claude-plugins-community, MIT).
---

# eli5

Explain the topic like the reader knows nothing about it and has no reason to
care yet. Output is one self-contained HTML file dominated by pictures, carrying
as few words as the explanation can survive on.

## When to use

- Use when the ask is「解釋給完全不懂的人聽」and the deliverable is a visual,
  not a paragraph.
- Skip when the reader already knows the domain and wants density — that is
  `infographic-design`.
- Skip when there is existing prose to simplify rather than a topic to explain —
  that is `plain-speak`.

## Procedure

1. **Find the one thing.** Name the single idea the reader must walk away with.
   Everything that does not serve it is cut, including facts that are true and
   interesting. A second idea is a second explainer.
2. **Find the everyday analogy.** Map the topic onto something the reader has
   physically handled — post, queues, keys, water, a phonebook. The analogy must
   hold for the whole explainer; if it breaks halfway, pick another one rather
   than patching it.
3. **Break it into 3-6 steps.** Each step is one picture and one short sentence.
   If a step needs two sentences, it is two steps.
4. **Draw it.** Inline SVG, big shapes, strong contrast, labels in the picture.
   Each step gets a visual that would still be readable with the caption removed.
   No stock-icon soup, no decorative clip art that carries no meaning.
5. **Strip the words.** Delete every term the reader would have to look up, every
   qualifier, and every sentence that only exists to be precise. Numbers stay
   only when the number is the point.
6. **Close with the payoff.** One line on what this lets the reader understand or
   do next — not a summary of what they just read.
7. **Say what you simplified.** Below the explainer (not inside it), list in one
   or two lines the places where the analogy is not literally true, so the reader
   can go deeper without carrying a wrong model.

## Output

Write a single `.html` file: inline CSS and SVG, no external fetches, readable
on a phone, sensible in both light and dark. Where the harness can publish
artifacts, publish it and hand back the link; otherwise leave the file on disk
and give the path. If a sibling skill for artifact design or diagramming is
available, prefer it for the visual pass — this skill's job is the explanation,
not the styling engine.

Keep it to one screen-scroll. An eli5 that needs a table of contents has stopped
being an eli5.

## Why

The failure mode of a beginner explainer is not being too simple, it is being
secretly complete: the writer keeps the caveats, keeps the correct vocabulary,
and adds an analogy on top. The reader then has to learn both the topic and the
analogy. Cutting to one idea, one analogy, and one picture per step is what makes
the thing land — and the honest note about what was simplified is what keeps a
useful lie from becoming a wrong belief.

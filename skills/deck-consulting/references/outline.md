# Node: `outline` 架構搭建

Decide the shape of the argument: which structural form this presentation takes, how many top-level sections it has, what axis those sections divide on, and what sits under each of them. The outline is the load-bearing artifact — headlines, storyline, opening and closing all attach to it, so a category set that is wrong here stays wrong everywhere downstream.

Going wrong looks like an outline that mirrors how the presenter's work was organized: 專案背景 / 執行過程 / 遇到的困難 / 未來規劃. Every section is true, none of them is a step the room has to take before it can decide, and the same evidence could sit in any two of them. The output is a topic covered rather than a case made.

## Entry check

Read `docs/deck-consulting/outline.md` if it exists. If it does, this is a revision: show the current structure, ask whether the form, the categories, or only the detail headings are wrong, and re-run from there. A changed category set invalidates the 一頁收攏 section in the same file and the 故事線 section in `script.md` — say so, and offer to re-run them.

Read `docs/deck-consulting/positioning.md`. If it is missing, say so plainly: without it there is no standard to judge a structure against, so any form you propose will be generically sensible rather than pointed at this room. Offer both paths — run `positioning` first, or proceed from whatever material is at hand and treat the structure as provisional. Do what the user chooses.

Read the raw material either way. The forms you offer have to be derived from what they actually have; a structural menu that could be handed to any presenter is the tell that you skipped this.

## Steps

1. **State the spine in one sentence.** What the room has to decide, and what the presenter is claiming they should decide. Not the topic — the claim. This sentence is what every later category gets tested against. Complete when the user confirms the sentence or corrects it into one they would actually say out loud.

2. **Choose the structural form.** Offer forms derived from their material and their positioning, labelled by what the room experiences rather than by the technique — 「先講結論，再講為什麼」, 「先讓他們感受問題有多貴，再給解法」, 「把兩條路攤開讓他們選」, 「照他們心裡會冒出來的問題順序回答」, 「按時間軸走：現況、做了什麼、接下來」. Say what each optimizes and what it costs against the positioning. Complete when the user has picked one and can say in a line why the other candidates lost.

3. **Fix the count and the axis.** Settle how many top-level sections there are and name, in one phrase, the axis they divide on. Complete when the axis is stated and every top-level section visibly sits on it.

4. **Test the set against the spine.** Walk the user's material item by item and place each under exactly one section; then ask what the decision needs that nothing covers. Complete when no piece of evidence has two plausible homes and everything the room has to accept has a section.

5. **Write the detail headings.** Under each top-level section, the two to four supporting points, all at the same altitude within that section. Complete when every section has children, none has a single child, and no section is carrying three times the children of its neighbours.

6. **Write the outline** to `docs/deck-consulting/outline.md` in the shape below, say in one line what changed, and name what makes sense next — `onepager` to compress it, `storyline` to order and connect it, `headline` once the detail headings need to carry assertions.

## Craft

**Four is usually the ceiling, and the reason is not attention span.** When a top-level set runs past four, two of the items are almost always the same category described from different angles — 成本效益 and 投資報酬 divide on nothing. The test is not the count itself but whether you can name the dividing axis in one phrase and have every item sit on it. If naming the axis requires an "and", the set was assembled rather than derived, and the fix is to merge the pair that shares an axis and promote whatever was hiding a level down.

**Organize by the decision, not by what the presenter knows.** A presenter's natural categories are their org chart, their workstreams, and the chronology of their own effort — all of which are real, and none of which is what the room needs in order to say yes. Run each top-level section through: *is this something the room has to accept before it can decide?* Sections that fail are usually background, and background belongs demoted, folded into whichever section needs it, or in an appendix nobody opens. This is the single highest-leverage move in the node and the one presenters resist most, because the work that took longest tends to lose its section.

**Overlap shows up as evidence with two homes, gaps show up as an unanswerable objection.** Rather than inspecting the categories abstractly, place the actual material: an item that fits two sections means the axis is not clean, and one section is about to steal the other's punch. For gaps, voice the room's most likely objection and ask which section answers it — an objection with no home is a missing section, not a missing slide.

**Unequal depth is a structural signal, not a cosmetic one.** A section with seven children next to sections with two is usually two sections wearing one label, or the thin ones are details that were promoted to look symmetrical. Fix the level, not the appearance.

**Mixed altitude inside a section hides a missing level.** When one section's children read 「為什麼現在要做」 and 「第三季採購時程」, a layer has collapsed. Either the timing detail belongs one level deeper under a heading it supports, or the section is doing two jobs.

**Structure is not slide count.** A top-level section may be one slide or nine, and deciding that here forces the presenter to negotiate their page budget before they have an argument. Keep the outline about the shape of the case; let the count fall out later.

## Output shape

Write `docs/deck-consulting/outline.md` with these sections. Prose plus a nested list — readable, not a form.

- **主軸** — the spine sentence: the decision the room faces and what the presenter claims.
- **結構形式** — the chosen form in a sentence, plus what it deliberately gives up.
- **分類邏輯** — the axis the top-level sections divide on, in one phrase, and why that axis serves this room.
- **大綱** — a nested list: each top-level section with its detail headings beneath. Headings stay descriptive here; `headline` is where they become assertions.
- **未納入** — the material that did not get a home, each with the section it lost to or the reason it does not serve the spine.

Leave the file open for the `onepager` node, which appends a sibling `一頁收攏` section beneath this one. When you revise the outline, that section is stale — flag it rather than rewriting it silently.

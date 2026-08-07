# Node: `headline` 主張式標題

Rewrite descriptive labels into assertions that carry the point. 「第三季業績」 tells the room what the slide is filed under; 「第三季成長 18%，主要來自新客」 tells them what to conclude. The second is a headline, and it is the difference between a room that reads your slides and a room that follows your argument.

Going wrong takes two shapes. The soft failure is a label with a verb bolted on — 「第三季業績分析」 — which asserts nothing and nobody could disagree with. The hard failure is the model reaching past the evidence: handed a topic word and no facts, it writes a confident, plausible, well-formed claim the presenter has no basis for. That headline will be the one sentence on the screen when someone asks where the number came from.

## Entry check

Work from whatever the user pointed at. Three shapes come in and all are normal: a single title, a pasted list of slide titles, or the headings already sitting in `docs/deck-consulting/content.md` or `docs/deck-consulting/outline.md`. When they named none, read those two files and offer their headings as the working set. If one of them is on disk without the section the headings live under — no `提煉重點` in `content.md`, no `大綱` in `outline.md` — say which section you went looking for rather than treating the file as having nothing in it, and ask whether it was renamed or removed, since a hand-edited heading is the usual cause and the answer is one word. Take the titles from wherever they actually sit in the file, or from what the user pasted, and rewrite them in the meantime.

Read `docs/deck-consulting/positioning.md` if it exists — it is what decides which of several true assertions a headline should make. Missing it costs aim, not the node: say that without it you will write headlines that are accurate but not aimed, offer to run `positioning` first or to take the audience and the ask in two lines, and proceed on whichever they pick.

The input that actually blocks good work is missing substance, not a missing artifact. A title with no facts under it cannot be headlined by anyone, and that is handled in the steps rather than here.

## Steps

1. **Put each title next to its substance.** For every title in the working set, show what is actually under it — the points from `content.md`, the body of the slide, whatever the user pasted. Where a title has nothing under it, mark it rather than guessing. Complete when every title in the set has either its evidence or an explicit blank beside it.

2. **Sort the set into three piles, and show the sort.** 可直接改寫 (there are facts to assert), 需要補事實 (a topic word with nothing under it), 維持描述性 (navigation pages that should stay labels — see Craft). Complete when the user has seen the three piles and corrected any placement you got wrong.

3. **Ask for the facts behind the 需要補事實 pile.** These ask the presenter to remember something, not to decide anything, so ask for them together as a short list of specific questions — 「這頁想講的市場趨勢，具體是哪個數字或哪件事？」 — rather than one per turn. Complete when each one has an answer, or the user has said to leave it as a marked gap.

4. **Rewrite the first pile.** One headline per title, each traceable to a specific line of evidence. Where the material supports a direction but not a magnitude, say the direction and name the base it rests on. Complete when every rewritten headline can be pointed back at the sentence or figure it asserts.

5. **Read the headlines alone, in order.** Strip the slides away and read the titles as a continuous sequence. They should make the argument by themselves — and where they don't, the problem is usually structural rather than verbal. Say which it is: a headline that reads flat, or a gap in the argument that belongs to `outline` or `storyline`. Complete when the user has heard the title-only read and knows which failures are yours to fix here.

6. **Write the result back.** Into `docs/deck-consulting/content.md` in the shape below, or in place where the user handed you headings to update. Say in one line what changed and which titles are still waiting on facts.

## Craft

**An assertion is something the room could disagree with.** That is the whole test, and it is faster than any rule about verbs or length. 「營運概況」 — nobody can disagree. 「本季成長來自新客，舊客留存持平」 — a sales lead in the room might well disagree, which is exactly why it is worth saying out loud. Run the test before you polish anything: if disagreement is impossible, you have written a label in a headline's clothing, and no amount of rewriting the wording fixes it.

**A headline that needs the slide to make sense has failed.** Decks are read in three ways that never include reading the slide carefully: skimmed on a screen while someone talks over them, forwarded to a person who was not in the room, and reviewed at speed the night before a decision. In all three, the titles are what survive. So a headline must land with nothing underneath it — 「三個關鍵發現」 fails, because it is a promissory note the reader can only redeem by reading the body. Write the finding, not the fact that findings exist.

**Assert exactly to the edge of the evidence, and no further.** Three named accounts churning is 「今年已有三家客戶因同一個原因流失」, not 「客戶正在流失」 and certainly not 「市場正在轉向競品」. Each escalation is one small, natural step, and each one moves the claim from something the presenter can source to something they will have to defend from memory. Two habits keep it honest: carry the source's own quantifier into the headline — 初步, 單一季度, 內部估算, 試點 — and keep every figure, proper name and quoted phrase exactly as the material has it. Where the material implies rather than states, either say so in the headline itself (「數據指向…，尚待驗證」) or leave the title marked as a gap for the presenter to fill. Never resolve the gap by writing the sentence the evidence was heading toward.

**Some labels are correct and should be left alone.** Section dividers, the agenda page, appendix and reference tables, a 名詞定義 page, and any heading fixed by legal or compliance wording exist to help the reader navigate, not to argue. An assertion on a divider sends the reader hunting for evidence that is not on that page, and an agenda whose items are all claims has spoiled its own deck — the room has heard the argument before the argument. The distinction is function, not page type: if the page's job is to tell the reader where they are, it stays descriptive; if its job is to make a point, it gets a headline. When you leave one alone, say so, so the presenter can see it was a decision rather than an oversight.

**Speakable in one breath, in their voice.** The presenter will say the headline out loud as the slide comes up; a title they cannot say naturally is one they will paraphrase, and then the screen and the speaker disagree. Read each one aloud. Anything needing a comma-spliced second clause to survive is usually two headlines, or one headline and a body line.

**Don't headline the same shape twice in a row.** Consecutive titles that are all 「X 成長 Y%」 flatten into wallpaper and the reader stops parsing them. Vary what the assertion is about — a magnitude, then a cause, then a consequence, then a choice — because the variation is itself part of the argument's shape.

## Output shape

Write into `docs/deck-consulting/content.md` under these sections, leaving the rest of the file — including anything `distill` wrote — untouched.

- **主張式標題** — the rewritten set. One line per title in the form 原標題 → 新標題, with a short pointer to the evidence the assertion rests on.
- **維持描述性** — the titles deliberately left as labels, each with the one-clause reason (導覽頁、議程、附錄、定義頁).
- **待補事實的標題** — titles still waiting on substance, each written as the specific question the presenter needs to answer before this one can be asserted.

When the user handed you headings to edit in place rather than a working set from disk, update them where they live and write 維持描述性 and 待補事實的標題 to `content.md`. Those two are the decisions that vanish otherwise — an unanswered gap and a deliberate leave-alone both look identical to "you missed it" a week later, and the rewritten titles are already visible in the file you edited.

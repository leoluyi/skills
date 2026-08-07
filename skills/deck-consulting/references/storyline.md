# Node: `storyline` 敘事編排

Turn a set of sections into something that runs. Fix the order, decide what each adjacency is doing, name the arc in a single breath, and write the sentences the presenter actually says when moving from one section to the next. The outline settles what the case is made of; this node settles the experience of sitting through it.

Going wrong looks like a deck where every section is defensible and the room still cannot say what it just heard. The sections were laid end to end, each one opened with 「接下來看第二個部分」, and the audience was left to assemble the argument themselves — which they will not do, because they are also reading email.

## Entry check

Read `docs/deck-consulting/script.md` if it exists. If it already has a `故事線` section, this is a revision: show the current order and transitions, ask whether the order, the arc, or only the wording is wrong, and re-run from there. Leave the `開場`, `收尾`, and `講稿` sections alone — they belong to other nodes — but say which of them your reordering has made stale.

Read `docs/deck-consulting/outline.md`. If it is missing, say so plainly: without a settled section set there is nothing to order, so any storyline you write is really an outline in disguise and will be redone once the structure lands. Offer both — run `outline` first, or work from whatever section list the user can give verbally. Do what the user chooses.

Read `docs/deck-consulting/positioning.md` when it exists. Order is decided against what the room can grant, and the 可接受底線 is what tells you where an early exit is survivable.

## Steps

1. **Label every adjacency.** Walk the section list in pairs and mark each as 依賴 — the next section's claim uses the previous section's conclusion as a premise — or 並列, where both support the same claim independently. Complete when every adjacent pair carries one label and the user agrees with it.

2. **Fix the order.** Dependent chains have their order forced; peer sets do not, so order those by weight against the positioning — usually strongest first, or the most-resisted first when the room needs time to absorb it. Complete when every adjacency has a stated reason for sitting where it does, not merely a label.

3. **Name the arc.** One line the presenter can hold in their head when they lose their place: 「問題比他們以為的貴 → 只有兩條路 → 我建議這條，代價是什麼」. Complete when the line covers every section and can be said in one breath.

4. **Write the transitions.** One spoken sentence, sometimes two, for each adjacency, in the presenter's own register. Complete when each transition names something specific from the section just finished and something specific from the one starting — a transition that would survive swapping in a different section is not doing its job.

5. **Run the interruption test.** At each section boundary, ask what the room walks out with if the meeting stops there. Complete when every boundary has an answer, and when any boundary that answers "nothing usable" has been fixed by reordering or by moving the ask earlier.

6. **Assemble the linking script** and write it to `docs/deck-consulting/script.md` as a `故事線` section. Say in one line what changed, and name what makes sense next — `opening` and `closing` to bookend it, `delivery` to put the whole thing in a consistent register.

## Craft

**The transition is where a deck actually breaks.** Sections are usually fine; the seams are where the room loses the thread, and 「接下來我們看下一個部分」 is not a seam, it is an admission that there isn't one. A working transition does two things in order: it closes the loop the previous section opened — states the conclusion that section earned, in one clause — and then poses the question the next section exists to answer. The room arrives at the next section already holding the question, which is the only reason they will listen to the answer.

**Tell a real sequence from a list pretending to be one, because the transitions differ completely.** The test is mechanical: can you swap two adjacent sections and leave the transitions untouched? If yes, it is a list, whatever the numbering implies. Lists want signposting — say the count up front, then give each item its weight — and their order is a rhetorical choice you can revisit. Sequences want dependency carried out loud, because the room has to be holding the previous conclusion to accept the next claim, and if the presenter does not say so, they will not be. Dressing a list as a sequence is worse than either: it promises an accumulating argument and delivers three unrelated points, and the room feels the shortfall without being able to name it.

**Order for the meeting that gets cut short.** Senior rooms interrupt, run over, and leave. A deck ordered so the payload arrives at slide 20 is a deck that frequently delivers nothing. Walk the boundaries and ask what has been banked at each one; where an early stop leaves the presenter with nothing, either move the ask forward or accept the risk deliberately. This is also the cheapest sanity check on the outline — a structure where nothing is banked until the end is usually one that saved its conclusion out of habit rather than design.

**Transitions are spoken, so write them spoken.** 「如前所述」 and 「綜上所述」 exist only on paper; out loud they signal that the presenter is reading. Write in the register the presenter's own material shows — and where a section arrives with no natural bridge, a short pause plus a plain declarative outperforms a manufactured link. Contrived continuity is more audible than an honest gear change.

**Name the seam where the deck changes direction.** Somewhere the presenter stops describing and starts asking — bad news into recommendation, analysis into request. Rooms feel that turn, and if it is unmarked it reads as a setup. Saying it plainly — 「講到這裡都是現況，接下來是我的判斷，可以不同意」 — buys back the credibility the turn costs, and separates what is observed from what is argued, which is exactly the distinction a sceptical decider is trying to make anyway.

**The arc is a delivery tool, not a summary.** Its job is to let the presenter recover when they lose their place, and to let anyone in the room reconstruct the whole after hearing half. If it takes more than one breath to say, the deck has more moving parts than it can carry live, and the honest recommendation is to go back to `outline` and merge something.

## Output shape

Write into `docs/deck-consulting/script.md` under a top-level `## 故事線` section. That file is shared: `storyline`, `opening`, `closing`, and `delivery` own `故事線`, `開場`, `收尾`, and `講稿` respectively. Rewrite only `故事線` and leave the others exactly as they are; when your reordering makes another section wrong, say so rather than editing it.

Inside the section:

- **敘事弧** — the one-breath line.
- **段落順序** — the sections in final order, each with one clause on why it sits there and whether the adjacency before it is 依賴 or 並列.
- **轉場口白** — the spoken transitions, one entry per seam, written as the presenter would say them.
- **中斷韌性** — one line per boundary: what the room has banked if the meeting ends there.

Keep 轉場口白 verbatim and speakable. It is the part the presenter reads off a note card, so anything that needs to be translated into speech at delivery time has failed here.

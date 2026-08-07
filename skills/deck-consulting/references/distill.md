# Node: `distill` 素材汰選

Take whatever raw material the presenter has — a pasted brain-dump, a document, a folder of slide screenshots, last quarter's deck — and reduce it to a fixed number of points at a chosen emphasis. The output is not a summary. A summary tries to represent the material; a distillation tries to serve the room, and the difference is that a distillation throws away true things on purpose.

Going wrong looks like a tidier version of the input: the same twelve topics, shorter sentences, nothing actually gone. The other failure mode is worse and quieter — the points read beautifully but a number has drifted, two findings have been fused into one claim neither source made, or a hedge has been ironed flat. The presenter will not catch that until someone in the room asks where the number came from.

## Entry check

Read `docs/deck-consulting/positioning.md` if it exists. The positioning is what decides which points survive, so when it is missing, say so plainly: without it you can rank by what looks important in the material, but nothing tells you what the room needs, and the result will be a competent generic summary. Offer both — run `positioning` first, or name the audience and the ask in two lines right now and proceed on that. Do what they choose.

Read `docs/deck-consulting/content.md` if it exists. If it does, this is a re-distillation: show the current points, ask whether the count, the emphasis, or the source material is what changed, and re-run from that step rather than from scratch.

Take stock of what material is actually in hand before asking anything else. If there is none, ask for it — this node has nothing to rank without it.

## Steps

1. **Inventory the material and read it back.** One short paragraph per source: what it is, roughly how much is in it, and what it appears to be arguing. Where the material is images, work slide by slide — say what is on each one, and name explicitly anything you cannot read: an axis label that is too small, a number cut off at the edge, a chart with no legend. An unreadable figure is a figure you do not have; ask for it rather than reconstructing it from the shape of the bars. Complete when the user recognizes their own material in your description and has answered the questions about what was unreadable.

2. **Fix the number of points.** Offer counts tied to what each one buys — 三點（口頭轉述得住）, 五點（一頁投影片的上限）, 七到八點（完整交代，但聽眾記不住） — and say which fits the occasion you read in the positioning. Complete when the user has named a number.

3. **Fix the emphasis.** Offer angles derived from their positioning and their material — 爭取資源, 進度回報, 建立風險意識, 說服採用某方案, 讓對方選 A 或 B. Name for each what it will push to the front and what it will push out. Complete when the user has picked one, and understands that a different pick produces a different set of points from the same material.

4. **Rank against the emphasis, out loud.** Order every candidate point by how much it moves the chosen emphasis, not by how much material sits behind it. Show the ranking with the cut line drawn at the chosen number. Complete when the user has seen the whole ranked list, including what fell below the line.

5. **Write the surviving points.** One or two sentences each, at a single altitude, each carrying a pointer back to where in the material it came from. Mark anything the material implies but does not state. Complete when every point traces to a source and every gap is marked rather than filled.

6. **Write `docs/deck-consulting/content.md`** in the shape below. Say in one line what changed, and name what makes sense next — usually `headline` to turn these points into assertions, or `outline` when the structure is still open.

## Craft

**A number the presenter picked beats "the important ones."** Asked to keep what matters, you will keep everything defensible, because every point in their material is defensible — that is why they wrote it down. A fixed count converts an open-ended judgement into a forced ranking, and forced ranking is the only operation that produces a real cut. Letting the presenter choose the number matters just as much: the count is where the pain lives, and a cut they authorized is a cut they will still be standing behind when someone in the room asks why their favorite chart is gone.

**Emphasis is the sort key, and it changes the answer.** The same material distilled for 爭取預算 and for 進度回報 should not produce the same five points, and if it does, one of the two is wrong. A budget ask leads with the cost of doing nothing and the size of the gap; the delivery detail the team is proud of drops below the line. A status update leads with what shipped and what slipped; the cost-of-inaction argument becomes noise, because nobody in that room is being asked to fund anything. When the two versions come out identical, you sorted by what was prominent in the source instead of by what the room needs.

**Every figure, name, and quoted phrase survives verbatim or does not survive.** Condensation is exactly where 「約 15–20%」 becomes 「近兩成」, where 「試點客戶反映」 becomes 「客戶反映」, where 「初步數據顯示可能有關」 becomes 「數據顯示相關」. Each of those is a small, natural, entirely invisible act of sharpening, and each one is a sentence the presenter cannot defend when challenged. Carry numbers, proper names, dates, and any qualifier the source attached — 初步, 部分, 內部估算, 單一客戶 — into the point unchanged. When a qualifier makes a point too clumsy to keep, that is information: the point is weaker than it looked, and it may belong below the cut line rather than in cleaner clothes.

**Never merge two sources into one point.** Two findings from two places, fused into a single confident sentence, produce a claim neither source actually made — and it is undetectable afterward, because the merged sentence reads better than either original. Points may sit next to each other; they may not be welded. Where two items genuinely belong together, keep both traces visible in the point so the presenter can see it rests on two legs.

**Hold one altitude.** A list that mixes 「第三季營收成長 18%」 with 「整體策略需要調整」 reads as noise, because the reader cannot tell whether the second is a conclusion drawn from the first or an unrelated item. Pick the altitude the emphasis calls for and keep every point at it. If one point refuses to sit at that level, it is usually the framing for the others rather than a peer of them — say so, and let `outline` or `headline` place it.

**What not to cut.** The rule is ranking, but three things override it. The single item that is the only evidence for the ask survives even if it ranks low on interest — an ask with no evidence under it is what the room will attack. Anything the presenter has already promised this audience stays, because dropping it silently reads as evasion. And the one fact that cuts against the argument stays if the room already knows it; the presenter naming it first is worth far more than the space it costs.

## Output shape

Write `docs/deck-consulting/content.md` with these sections. When the file already exists from another node, replace these sections and leave the rest alone.

- **素材來源** — one line per source: what it was, and for images, which slides were unreadable and what was asked about them.
- **提煉設定** — the chosen count and emphasis, in one line each, so a later re-run knows what it is changing.
- **提煉重點** — the numbered points, one or two sentences each, each ending with a short pointer to its source (slide number, section, or the phrase it came from).
- **捨棄與理由** — what fell below the line, one line each, naming the part of the emphasis or positioning it lost against.
- **待補資料** — the gaps: figures that were unreadable, claims the material only implies, facts the argument needs and does not have. Each written as a question the presenter can answer.

Keep the whole file readable in one screen-and-a-half. The point of distilling is that the next node reads this instead of the raw material.

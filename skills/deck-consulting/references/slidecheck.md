# Node: `slidecheck` 逐頁診斷

Look at the slides the presenter actually has and report what is costing the reader, ranked, each with one concrete edit. This is the only node that starts from the artifact rather than from the argument — someone can arrive here with nothing but a deck and a meeting on Thursday.

Going wrong looks like a tidy list of forty observations in slide order, every one phrased as a problem, none of them separated by how much they actually cost. A presenter who reads that fixes the font sizes on slide 12 and never notices that slide 4 is making two arguments at once. The output that earns its keep is short, ordered by damage, and says out loud which slides to leave alone.

## Entry check

Ask for the slides in whatever form exists: screenshots, an exported PDF, the deck file, or — when none of those can be shared — a written description of what is on each page. All four are workable; they are not equally reliable, and the difference has to be carried into the artifact rather than quietly absorbed. Say which one you got and what it lets you judge.

A written description is the weakest input and still worth running. It will surface slides carrying two messages, missing headlines, and charts doing the wrong job, because those are properties of the content rather than of the rendering. It will not surface anything about size, contrast, spacing, or alignment. Say which half of the review the user is getting before you start, so a thin report is an expected outcome rather than a disappointing one.

Say plainly what an image cannot settle. A low-resolution screenshot will not tell you whether body text clears the legibility floor, and a PDF page shows composition but not what the projector will do to a pale grey. Naming the limit costs one line and is the difference between a review the presenter can act on and one they have to re-verify.

A flattened export hides builds. A slide that arrives looking impossibly dense may be six elements that appear one at a time, and calling it crowded would be wrong in a way the presenter will notice immediately. When a slide looks over-full in a way that seems deliberate, ask whether it animates before reporting it, and mark it 推測 if the answer never comes.

One thing changes nearly every judgement below: **projected in a room, read on a laptop, or both.** Ask it — but do not wait on it. State the assumption you are working under, deliver the full review in the same reply, and mark the findings that would change if the answer comes back different. A presenter with one evening left needs the review now; holding it hostage to a clarifying question spends their turn and returns nothing.

Read `docs/deck-consulting/positioning.md` if it happens to be on disk — it tells you what each slide is supposed to be buying, which sharpens every ranking here. It is not a prerequisite. Without it, judge each slide against the message it appears to be making, and say that is what you did.

## Steps

1. **Say what you are looking at.** Number of slides, the form you received them in, the viewing condition you are assuming and where it came from, and any slide you cannot read well enough to judge. Complete when that is stated — the review continues in the same reply rather than pausing here.

2. **Read each slide for its one message, before noticing anything about its appearance.** Write down, in a handful of words, the single thing you took away. Do this from the slide alone, without the surrounding narration. Slides where you cannot produce one, or where you produce two, are already the most valuable findings in the review — record them now, because once you start noticing fonts you will stop being able to see this. Complete when every slide has a message written next to it or is marked as producing none.

3. **Sweep for what the reader cannot receive at all.** Type below the legibility floor for the stated viewing condition, text or objects clipped by the frame edge, contrast too low to resolve, a table whose cells have collapsed. These are settled by measurement, not taste — and where the image is too coarse to measure, say so rather than estimating. Complete when every such instance is located by slide and element.

4. **Check what the visuals claim.** A truncated or unlabelled axis, a pie of percentages that do not total, an area chart where the eye reads area but the data is linear, two colours that imply a grouping the data does not have, a screenshot cropped past the point where it still shows what it is cited for. These mislead a reader who is paying attention, which makes them worse than the ones that merely slow people down. Complete when every chart and data graphic has been read for what a stranger would conclude from it.

5. **Then read for effort.** No visual hierarchy, so the eye has no entry point. Related things placed apart and unrelated things placed together. Alignment drift. A body of text that has to be read linearly because nothing is doing the work of structure. These are real costs and belong in the report — below the two tiers above.

6. **Rank across the whole deck, and prune.** Order by reader cost, not slide order. Keep the advisory tier short; if it runs past a handful of items, you have started listing preferences. Say which slides are fine — a review with no clean slides in it reads as reflex, and the presenter discounts the whole thing. Complete when the top three findings are the three you would actually spend the presenter's remaining evening on.

7. **Write one edit per finding.** Not 「簡化這頁」 — an instruction the presenter cannot execute without redoing your thinking. Name the specific move: which sentence becomes the headline, which two slides this one splits into, which series drops out of the chart. Complete when each finding names an edit the presenter could perform without asking a follow-up question.

8. **Write the report** to `docs/deck-consulting/slidecheck.md` in the shape below, then say in one line what the top finding was and offer `layoutspec` for any slide whose fix is a rebuild rather than an edit.

## Craft

**嚴重度 is about the reader, not about your taste.** Three tiers, and they are not interchangeable:

- **讀不到** — the reader cannot receive the content: below-floor type, clipped or overflowing content, contrast that fails at the back of the room. Objective, and the only tier that should read as a defect.
- **讀錯** — the reader receives something false: a misleading axis, colour implying a grouping the data lacks, a crop that removes the caveat.
- **讀得慢** — the reader gets there, but pays: no hierarchy, weak grouping, drifting alignment, a slide carrying two messages.

Anything else is 建議 — phrased as an option, never as a failure, and never counted in the same list as the three tiers above.

Protect the top tier by keeping it small. A review that marks everything as a problem gets discounted whole, and when that happens the 讀不到 items — the ones that were objectively true and cheap to fix — go unfixed along with the opinions. Severity is what buys the report its credibility; spending it on preferences is spending it on nothing.

**Judge each slide the way the room will get it: a few seconds, no narration, no memory of the previous slide.** The presenter cannot do this — they know what the slide means, so they see the meaning instead of the surface, which is exactly why they need someone else to look. Take the first thing you register and write it down before you reason. That first impression is the finding; the considered reading you produce thirty seconds later is a reading no audience member will ever perform.

**The commonest defect is not ugliness, it is a slide making two arguments.** It survives review because each half looks fine. The audience reads whichever half is visually heavier and misses the other, and the presenter blames attention span. The fix is a split, or a demotion of one half to a note.

The split is often what the presenter has been resisting, because it takes the deck from 18 slides to 20 and they have been told to keep it short. Say the trade out loud: a slide count is not a cost, an unread argument is, and two slides that each land in five seconds take less of the room's time than one that takes twenty and lands half.

**「文字太多」 is not a finding.** Every presenter already knows there is too much text, and the advice has no execution attached, so they shave adjectives and the slide stays unreadable. The useful version names what the text is *for*. This paragraph is the speaker's script and belongs in the notes. These four bullets are one claim and its three supports, so the claim becomes the headline and the supports become the body. This list is really a table with the column headings deleted.

Density is a symptom of a structural decision nobody made. Naming the decision is the fix, and it is also the reason this node keeps handing slides back to `headline` and `outline` rather than trimming words in place.

**Without a way to measure, use the thumbnail test.** Shrink the slide until it is roughly the size of a postage stamp, or view it at the smallest zoom the viewer allows. What survives is what the room gets in the first seconds: the headline should still be readable as text, the one important number should still be findable, and the accent colour should still point at something. What disappears at that size was never carrying weight at full size either — it was occupying it.

This is a proxy, not a measurement, and it should be reported as one. It reliably catches a headline that is too light or too long, a chart with no focal point, and a slide with no entry point at all. It will not tell you whether 14pt body text is legible from row 12, and nothing available here will. When that is the open question, say it is open and tell the presenter to stand at the back of the actual room.

**Decorative colour and encoding colour cannot share a slide.** Colour is encoding when a difference in hue means a difference in the data — this series versus that one, this quarter highlighted because it is the point. It is decorative when it varies for interest. Once both are present, the reader has no way to know whether a colour change is meaningful, so they check, and checking is the cost. The repair is nearly always subtractive: everything neutral except the one thing being asserted.

This is also the single highest-yield edit available on most business decks, because the default is a template palette applied to every series in every chart. Greying out four of five bars costs a minute and changes what the slide says.

**Alignment is read as carelessness by people who cannot name it.** An audience will not say 「這幾個方塊差了三個像素」. They will register that the deck feels unprepared, and discount the argument accordingly. This is why alignment sits in the 讀得慢 tier and not in 建議 — the cost is to the presenter's credibility, not to anyone's aesthetics, and it is usually the cheapest thing in the entire report to fix.

**A deck that will be read is a different artifact from a deck that will be projected.** Read on a laptop, the type floor drops, dense slides become acceptable, and a slide that stands alone without narration is a virtue. Projected, the floor rises hard, anything at the frame edge risks being cut, and pale greys vanish under room light. When the answer is "both", resist averaging. An averaged deck is bad at both jobs: too dense to project, too thin to read alone. Tag findings by the mode they apply to, and where the conflict is real, say the honest thing — one source deck, two exports, with the read-alone version carrying the detail the projected one moved into the notes.

**Some layout findings are structure findings wearing a costume.** Three consecutive slides that each look crowded, where the crowding is the same three categories repeated, is not a layout problem — it is one slide that got split by topic instead of by argument. A slide whose headline cannot be written because the slide has no point is not a headline problem. When the honest fix is upstream, say so and name `outline`, `headline`, or `storyline` rather than prescribing a cosmetic repair that leaves the cause in place. Presenters accept this readily when you show the pattern across slides; they reject it when it arrives as an assertion about a single page.

**Findings the presenter cannot execute are not findings.** A corporate template with a fixed font, a locked colour palette, and a mandatory footer band is a constraint, not a defect, and telling someone to abandon it wastes the one review they were going to read. Ask early whether the template is theirs to change. When it is not, work inside it — the levers that survive almost any template are word count, element count, hierarchy, grouping, alignment, and which single thing gets the accent colour, and those are usually where the damage was anyway.

**Mark observation apart from inference.** A finding from a screenshot you could actually read is 觀察. A finding from a written description, or from an image too coarse to measure, is 推測 — write it as a question the presenter can settle in ten seconds by opening the file: 「第 7 頁的內文如果小於標題的一半，投影時後排會讀不到，請確認」.

Fabricated layout findings are the one failure here that the person receiving the report cannot catch. They open the file, see the thing is fine, and from then on every other finding is suspect. One of them costs the whole report its standing, which makes 推測 the cheapest label in this document to apply.

## Output shape

Write `docs/deck-consulting/slidecheck.md` with these sections.

- **檢視條件** — what you received, the viewing condition, and what you could not judge from it.
- **整體判讀** — two or three sentences on the pattern that repeats across the deck. This is usually more valuable than any single slide's finding.
- **優先處理** — the top three, ranked by reader cost, each with its slide number, its tier, and its edit.
- **逐頁問題** — by slide: 嚴重度 tier, the problem in one line, 觀察 or 推測, and the edit. Slides with nothing worth reporting are listed as clean, not omitted.
- **維持現狀** — what is working and should survive the revision, so a presenter under time pressure does not rebuild it.

Length is part of the design here. A presenter reads this the night before, with limited hours left, and acts on the top of it. If the report runs long enough that 優先處理 stops being the thing they act on, the ranking has been wasted — cut the advisory tier until it fits.

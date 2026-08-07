# Node: `closing` 收束提請

Build the last two minutes: a recap that mirrors the opening's promise item for item, then the ask. The mirroring is the whole point. A closing that recaps what the presenter found most interesting, rather than what the opening promised, reads to the room as a different presentation that happens to have been delivered in the same hour.

Going wrong looks like a summary slide with five bullets and a final line thanking everyone for their time. Five bullets is not a recap of a three-item promise, and a thank-you hands the room back with nothing to do. The other failure is the ask that cannot be refused because it cannot be acted on — 「請各位支持這個方向」 — which the room accepts warmly and forgets by the afternoon.

## Entry check

Read `docs/deck-consulting/positioning.md` for the 目標三層 and the 採取姿態, and the `開場` section of `docs/deck-consulting/script.md` for the 承諾清單 you are mirroring. Those two are what this node is made of: the promise supplies the recap, the tiers supply the ask.

Either can be missing. Say which, say what it costs — without the opening's promise the recap has nothing to mirror and becomes a summary of the deck, which is a different and weaker thing; without the positioning the ask has no floor to fall back to and will be pitched at whatever feels bold — and offer both paths: run `opening` or `positioning` first, or reconstruct the promise in two minutes from the outline and the presenter's answer to "what do you want them holding when they walk out". Then do what they choose.

`script.md` can also be on disk and still not hold what this node reads: no `開場` section at all, or a `開場` that carries no `承諾清單`. Say which of the two is missing by name instead of reporting the opening as never written — the presenter usually knows, because a renamed heading is their own edit, and the question costs them one word. It changes nothing about proceeding: a closing asked for now gets written now, mirroring whatever promise-shaped lines the `開場` does contain, with each reconstructed item marked so the presenter can see which ones you supplied.

If a `收尾` section is already in `script.md`, this is a revision: show it, ask whether the recap or the ask is what is wrong, and rework only that part.

## Steps

1. **Lay the promise out and mark each item against the body.** Take the 承諾清單 from the `開場` section, and for each item say plainly whether the deck as it now stands delivers it, delivers part of it, or does not deliver it. Name the section that delivers each one. Complete when every promise item carries a verdict the presenter agrees with.

2. **Resolve the mismatches before writing a word of recap.** For anything not delivered, offer the real choices: cut it from both opening and closing, restore the section that would deliver it, or keep it and say the gap out loud in the room. Recommend one and say why. Complete when no promise item is left in a state where the recap would have to fake it.

3. **Write the recap as a mirror.** Same items, same order, same nouns as the opening used. Each item is now stated as settled rather than promised — the promise said what they would be able to decide, the recap says what they now know that lets them decide it. Complete when the recap can be read next to the 承諾清單 line by line with nothing extra and nothing missing.

   One line per item, no sub-points. A recap that grows sub-points is re-presenting the body, and the room stops listening for the ask.

4. **Decide which tier is actually in play.** Ask the presenter which of the 目標三層 they expect to be live by the time they reach the end, and how they would tell from the room. Then write the ask for that tier, plus a one-line fallback for the tier below it that they can reach for without visibly retreating. Complete when the presenter can say what they will do if the room has clearly gone cold.

   Ask them for the signal in concrete terms — who has stopped taking notes, who has started asking implementation questions, whether the decider has looked at their phone twice. A tier switch made on a feeling gets made too late; a tier switch tied to an observable gets made in time to matter.

5. **Make the ask specific enough to be refused.** Name the person or role, the action, the date, and — where the positioning structured it as a choice — the two options they are choosing between. Read it back and ask what refusing would sound like; if there is no clean way to say no, the ask is not yet an ask. Complete when the presenter can state it in one sentence with a name and a date in it.

   Where the presenter is unsure how hard to push, offer the shapes and let them pick by ear:

   - **要一個決定** — the full commitment, named and dated. Highest value, and the one that can be lost outright.
   - **要一個二選一** — the same decision framed as a choice between two options you brought. The room is inside the decision before it can reject the premise.
   - **要一個小的第一步** — a pilot, a two-week trial, one department. Cheap to grant, and it converts a position into a commitment.
   - **要一個時間** — a follow-up meeting with named attendees and a date. What to reach for when the decider is not in the room.
   - **要一個授權** — permission to proceed without further approval up to a stated limit. Often easier to grant than money.

6. **Write it in their voice and read it back as speech.** Use the register established for the opening; if none was established, read the presenter's own material for how they talk, and when the material shows no voice, ask 白話口語 or 正式簡練 with a sample of each before writing. Then read it aloud: split any sentence you cannot say in one breath. The ask especially — it is the sentence most likely to be delivered in a rush. Complete when the ask survives being said out loud without a stumble.

   Watch for the ask growing a cushion when it is read aloud — 「不知道各位覺得…」, 「如果方便的話」, 「大概」. A presenter uncomfortable with the ask adds these on the way out of their mouth, and each one gives the room an exit. Point them out by name so the presenter hears themselves doing it.

7. **Write down what happens if they say yes.** One or two lines the presenter says immediately after a yes: what they will send, to whom, by when. A room that grants something and then hears nothing for two weeks quietly ungrants it, and the presenter loses on follow-through what they won in the room. Complete when the first post-meeting action has an owner and a date.

8. **Write the `收尾` section** into `docs/deck-consulting/script.md` in the shape below, then say in one line what changed and name what makes sense next — usually `delivery` for the passages that still read like a document, or `slidecheck`.

## Craft

**An ask stated as 「請各位支持」 or 「請各位考慮」 gets nothing, because nothing is being asked of anyone.** There is no actor, no verb with a date, and nothing to decline — so the room grants the easiest thing, agreement in principle, and no calendar changes. A specific ask names who does what by when: 「請財務在月底前把這筆預算放進 Q3 草案，我下週把細項給您。」 It sounds smaller and it is worth more, because it can be tracked, and because refusing it takes a sentence of reason — and that sentence is the most valuable thing the presenter can leave with.

**The size of the ask is set by the room's authority, not by the presenter's need.** A room that cannot approve the number will not approve the number however well the case is made, and asking anyway converts a productive meeting into a recorded failure. Check the stakeholder map for what each party can actually grant, and pitch the ask at the largest thing the people present are able to give. Where that is smaller than what the presenter needs, the closing's job becomes getting the real decider into the next room — say that plainly rather than letting them aim at a wall.

**A refusable ask is an informative ask.** The reason to prefer something that can be cleanly declined is not politeness; it is that a clean no tells the presenter which objection is the live one, which is the 情報收穫 tier they would otherwise go home without. Build one question into the closing that collects it even when the answer is yes: 「如果今天沒辦法決定，主要卡在哪一點？」 Asked after the ask, not instead of it.

**When the 可接受底線 is what is actually in play, the closing changes shape rather than volume.** The instinct is to make the same ask more forcefully and lose it on the record, which makes the second attempt harder than the first. The better move is to not spend the no: ask for the floor — the smaller commitment, the next meeting, or the understanding that doing nothing has a cost — and attach a date on which the full ask returns. The full ask stays alive, and the presenter walks out with something. Say plainly that this is what you are doing, because a presenter who does not realize they have switched tiers will deliver the floor with the disappointment audible.

**A recap of things the opening never promised reads as a different presentation.** The room does not consciously compare the two lists, but they feel the mismatch as a loss of shape — the sense that the hour covered a topic rather than made a case. This is why the mirror is worth the constraint it imposes. If the recap wants to include something the opening never mentioned, the honest reading is usually that the opening's promise was wrong, not that the recap should be widened. Say which one you think it is and send the fix back to `opening` rather than absorbing it here.

**Nothing new enters in the recap.** A fact appearing for the first time in the last ninety seconds reads as something that was being held back, and it reopens the argument at the exact moment it should be closing. If it is load-bearing enough to belong in the recap, it belongs in the body — say so, and name the section it should go into rather than smuggling it in here.

**When the room grants it early, stop presenting and close.** Sometimes the decision lands at minute eight, and the presenter keeps going because there are fourteen slides left. Every additional slide is a fresh opportunity to raise an objection to something already agreed. Write a short-form closing — the ask alone, two sentences, no recap — and say plainly when to reach for it: the moment the decider says something that only makes sense if they have already decided yes.

**Mirror with the opening's own words, not better ones.** The improved phrasing you reach for in the recap reads to the room as a new topic, and they spend the sentence working out whether it is the same thing. Sameness is doing structural work here — it is what tells a listener the presentation has closed rather than merely stopped.

**The recap is the promise settled, not the deck compressed.** Three promise items produce three recap lines even if the deck had nine sections. Anything true and interesting that was never promised does not belong here; it belongs in the body, or in the answer to a question, or nowhere.

**Ask the person who can grant it, by name, out loud.** An ask addressed to 「各位」 in a room of eight is addressed to nobody, and everyone waits to see who moves first. Naming the one person whose yes is the yes — 「王副總，我想請您今天給我一個方向」 — costs nothing and removes the diffusion. Where the decider is not in the room, say whose decision it is and ask the room for the thing they can actually give, which is usually a recommendation or a meeting.

**Put the ask before the questions, not after them.** A closing that ends on Q&A lets the last five minutes be shaped by whoever asks the sharpest question, and the ask arrives, if at all, into a room already re-litigating a detail. Make the ask, take the questions, then restate the ask in one sentence and stop. The restatement is short enough that nobody minds hearing it twice, and it puts the room back where the presenter needs it.

**Do not end on 謝謝聆聽.** The last thing said is the thing the room acts on, and gratitude is not actionable. End on the ask, then stop talking. Script the silence explicitly — a presenter who does not know the pause is intentional will fill it, usually by softening the ask they just made.

## Output shape

Write into `docs/deck-consulting/script.md` under a top-level `## 收尾` section. That file is shared: `storyline`, `opening`, `closing`, and `delivery` each own one named section in it. Rewrite only `收尾` and leave the others exactly as they are; when your change makes another section wrong — a promise item you dropped, for instance — say so rather than editing it.

The `收尾` section holds:

- **承諾對照** — the promise items from `開場` with the recap line for each, laid out so the mirroring is visible at a glance.
- **收尾重述** — the recap as continuous speakable script.
- **行動請求** — the ask in one sentence, with the person, the action, and the date; plus the option pair where the ask is a choice.
- **退守選項** — one line on the floor ask and the signal that would make the presenter reach for it.
- **情報問句** — the one question that collects the 情報收穫 tier whether the answer is yes or no.
- **提早成交版** — two or three sentences to use when the room decides before the deck ends.
- **答應之後** — the first follow-up action, its owner, and its date, in one line.
- **收尾逐字稿** — the whole closing as speakable script in the presenter's register, ending on the ask, with the pause marked.

The 承諾對照 is working material as much as output — a presenter who can see the two columns side by side catches a drifting deck faster than any note from you will make them.

Keep it to what fits in about ninety seconds. A closing that runs long lets the room start packing up before the ask arrives.

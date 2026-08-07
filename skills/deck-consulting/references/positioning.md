# Node: `positioning` 溝通定位

Establish what this presentation is *for*, in a form the other nodes can be judged against. Everything downstream — what gets cut, what leads, how the opening lands — resolves against this artifact.

Going wrong looks like a brief full of adjectives: "說服高層支持數位轉型". That is a topic with a verb attached. A positioning brief names a room, a decision that room can make, and what the presenter walks out with in each of three outcomes.

## Entry check

Read `docs/deck-consulting/positioning.md` if it exists. If it does, this is a revision: show what is currently there, ask which part is wrong, and re-run only the affected steps. Then flag every downstream artifact on disk as stale, because a changed positioning invalidates the standard everything else was judged against.

Read whatever material the user has given — slides, a document, a list of points. If they have given none, ask for either the material or three to five points they intend to make; do not run this node on nothing, because every option you offer below has to be derived from their specifics or it is filler.

## Steps

1. **Read the material and name what you see.** One short paragraph: what this looks like it is about, and what is conspicuously absent. This is also the check that you actually read it — the user should recognize their own deck in your description. Complete when the user confirms or corrects it.

2. **Fix the room.** Offer situations derived from the material — an internal review, a budget request, a status update to a sponsor, a pitch to a customer, a kickoff to people who will do the work. Complete when the user has named the situation and roughly who is in the room.

3. **Map the stakeholders.** Not "the audience" — the specific roles that can move. Push past the obvious one by asking about each axis that plausibly applies: who up the chain has to approve; which peer department is affected and may resist; whether anyone external is present; who has already taken a public position. Complete when you have at least the decider and one other party with a distinct stake, and know what each one can grant or withhold.

4. **Name what the presenter wants.** Two separate things, asked separately. First the content: which points must land, from their material. Then the personal stake: what changes for *them* if this goes well — budget, headcount, a mandate, cover for a decision already made, visibility. Complete when both are on the table. The second is the one people skip and the one that decides the ask.

5. **Read the board back.** Two or three sentences of candid assessment: what the presenter has going for them, what is genuinely against them, and what kind of situation this is. Say the uncomfortable part — that the ask is large relative to their track record, that the real blocker is not in the room, that the decision was probably already made. A consultant who only reflects optimism is worthless.

6. **Offer postures, and let them hear one.** Two or three ways to play it, each carrying the same three-tier outcome in different proportions (see Craft). For each: what it optimizes, what it costs, and one sample sentence in the presenter's voice so they can hear what it sounds like out loud. Complete when the user picks one.

7. **Write the brief** to `docs/deck-consulting/positioning.md`, in the shape below. Then say in one line what it now governs, and name the nodes that make sense next — usually `outline`, or `distill` when the material is raw.

## Craft

**Three tiers, always.** A presentation aimed at a single binary outcome is fragile: one "no" and the whole occasion was a loss, which is exactly the pressure that makes presenters oversell. Give every posture three tiers instead:

- **最佳結果** — the full ask lands. State it as an observable event, not a feeling: "核准 300 萬預算", not "讓老闆認同".
- **可接受底線** — the ask fails and the meeting was still worth holding. Usually a smaller commitment, a next meeting, or an understanding you needed them to have — most often that the cost of doing nothing is real.
- **情報收穫** — what the presenter learns regardless. Which objection is the live one, who actually decides, what the unstated constraint is. This tier is free and almost always skipped.

The three do not trade off evenly across postures, and naming which one a posture sacrifices is the whole value of offering a choice.

**Turn a yes/no into a which-one.** A room asked to approve or reject will default to rejecting, because rejecting is free. A room asked to choose between two framed options is already inside the decision. Where the ask can be structured as a choice, structure it — and say so in the brief, because it changes what the closing node has to build.

**Tier the information against the aim, not against how much work it took.** The chart that took three days goes in the low tier if it does not move the decision. Say that out loud when you tier it, because that is the sentence that makes the cut stick.

**The floor is not a weaker version of the ask.** "至少讓他們理解方案 B" is a weaker ask. "確保他們理解什麼都不做的風險" is a floor — it is a different outcome that survives the ask failing. If the floor collapses into "they liked it", it is not a floor.

## Output shape

Write `docs/deck-consulting/positioning.md` with these sections. Prose, not a form to fill — but every section present, because the downstream nodes look for them by name.

- **溝通場景** — the situation and the room, two or three lines.
- **利害關係人** — one line per party: who they are, what they can grant or withhold, what they are likely to resist.
- **目標三層** — 最佳結果 / 可接受底線 / 情報收穫, one line each, each observable.
- **採取姿態** — the chosen posture in a sentence, and what it deliberately sacrifices.
- **該做與不該做** — a short Do list and Don't list, each item concrete enough to check a slide against.
- **資訊順位** — 高 / 中 / 低, listing the user's actual material items under each, with a clause on why each low-tier item lost.

Keep it to roughly one page. A positioning brief that runs long stops being the thing you re-read before every later decision, which is its only job.

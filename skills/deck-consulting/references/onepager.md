# Node: `onepager` 單頁濃縮

Collapse the whole presentation onto a single page: one claim, a small number of 綱要 that are the reasons the claim holds, and a couple of supporting lines under each. This page is the argument in miniature — the thing the presenter opens with when the meeting is cut to ten minutes, and the thing that gets forwarded to the person who was not in the room.

Going wrong looks like a table of contents wearing a one-pager's layout: 市場趨勢 / 現況盤點 / 三大方向 / 後續規劃, each with two neutral bullets. Nothing on the page can be disagreed with, so nothing on it can be agreed to either. A reader finishes it knowing what will be covered and not what they are being asked for.

## Entry check

Read `docs/deck-consulting/outline.md`. If the file has a `單頁濃縮` section already, this is a revision: show it, ask whether the 主張 or the 綱要 are what is wrong, and re-run from there.

If `outline.md` is missing, say so: without a settled structure there is nothing to compress, so the page would be built straight from raw material and would come out as a generically competent summary rather than this deck's argument. Offer both — run `outline` first, or build the page directly from the material and accept that the deck may later disagree with it. Do what the user chooses.

A third case sits between those two and is worth separating: the file is on disk but the `大綱` it should carry is not in it. Say that by name — the file is here, the section is not — and ask whether it was renamed or removed, since a hand-edited heading is the usual cause and the answer takes one word. Treating it as a missing file instead sends the presenter off to re-run `outline` over structure they already have. Nothing is waiting on the answer: compress whatever section-shaped content the file does hold, or the material directly, and note in the page which one it came from.

Read `docs/deck-consulting/positioning.md` when it exists. The page has to end in the ask, and the ask lives there.

## Steps

1. **Write the 主張 first, before looking at sections.** One sentence stating what this presentation argues and what it wants. Complete when the sentence contains a verb, names something specific, and could be contradicted by a reasonable person in the room — a sentence nobody could disagree with is a topic, and needs another pass.

2. **Derive the 綱要 from the 主張, not from the outline's sections.** Three or four, each the answer to "why should I believe the 主張". They will often align with the deck's sections; where they don't, follow the argument. Complete when each 綱要 reads as a standalone claim and the set of them, taken together, is enough to make the 主張 hold.

3. **Give each 綱要 its supporting lines.** Usually two: the strongest specific the presenter actually has, and the thing that makes it credible — the mechanism, the comparison, or the honest limitation. Complete when every line carries a number, a name, or an event rather than a category, and every one of them traces to the user's material.

4. **Land the ask.** One closing line naming what the presenter wants the reader to do, at the specificity the positioning's 最佳結果 set. Complete when a reader who saw only this page would know what decision is in front of them.

5. **Read it against the outline and against the clock.** Name what fell off the page and check the 主張 still stands without it; then read the page aloud. Complete when every drop is named with the reason it lost, and the read-through fits inside the window the presenter would realistically be given.

6. **Write the page** into `docs/deck-consulting/outline.md` as its own `單頁濃縮` section, say in one line what changed, and name what makes sense next — usually `storyline`, or `opening` when the 主張 turns out to be the hook.

## Craft

**A 綱要 that cannot be disagreed with is not a 綱要.** Test each one by putting 「我不同意」 in front of it. 「市場趨勢」 fails — there is nothing to refuse. 「這個市場的成長已經停在我們的既有客群，再投入只會拉高獲客成本」 can be refused, which is what makes it worth putting on the page. The mechanical version of this fix is nouns into verbs, but the real move is committing to a position the presenter is willing to defend.

**Not a summary of the deck — the deck with the evidence thinned.** A summary preserves coverage and loses force; this page preserves the argument and drops the proof down to one specific per claim. The diagnostic is what happens when you thin it: if the argument stops working once each 綱要 has only its single strongest piece of evidence, the case was being carried by volume rather than by reasoning, and the honest report back is that the deck has a weak spine, not that the page needs more lines.

**Resist one-to-one with the deck's sections.** Some sections exist for procedural reasons — background the room expects, an appendix, a compliance note — and earn no line here. One 綱要 may draw on two sections. Forcing the mapping is exactly how the page reverts to a table of contents, because the section list is organized for delivery and the page is organized for persuasion.

**Write it to survive without the presenter.** This page gets forwarded, quoted in an email, and read by the person who actually decides but did not attend. Anything that only makes sense with narration — a chart reference, 「如同稍早提到」, an unexplained internal codename — fails there. The test is handing it to someone with no context and asking what they think they are being asked for.

**One page is a constraint on the argument, not on the typography.** When it does not fit, the count is wrong: two 綱要 are the same reason, or a supporting line is doing a whole 綱要's job. Shrinking the font converts a structural problem into an unreadable page and hides the signal that would have fixed the deck.

**Order the 綱要 by what the room resists, not by what is easiest to say.** The reason they are most likely to reject goes early enough that the rest of the page can absorb the objection. Leaving it last means the reader closes the page on their strongest doubt.

## Output shape

Append to `docs/deck-consulting/outline.md` as a sibling section titled `單頁濃縮`, beneath the outline's own sections. It lives in the same file deliberately: when the structure changes, the compression is visibly stale next to it instead of drifting in a file nobody reopens.

Inside the section:

- **主張** — the one sentence, on its own line.
- **綱要** — three or four, each a claim, each with its two supporting lines nested beneath.
- **訴求** — the ask, one line.

Nothing else. A dated header, a scope note, and a glossary are how this page becomes a two-pager. If the presenter needs framing around it, that belongs to `opening`.

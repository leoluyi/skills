# The red-team pass

Run this when a direction has formed and before it gets written down as settled.
The pass converts "we think X" into "X rests on these four things, and here is
what would break each one".

## 1. Extract the load-bearing assumptions

An assumption is load-bearing when the direction collapses without it. Most of
what a discussion produces isn't: it's colour, context, or a preference that
could flip without changing the conclusion. Chase those and the pass produces a
long list of nothing.

Two questions find the real ones:

- If this turned out to be false, would we choose differently? If no, drop it.
- Is it doing work nothing else does? If two assumptions fail together, they're
  one assumption.

Four to seven is the usual yield. A list of fifteen means you're cataloguing the
discussion instead of attacking it.

Pull them from three places: what the pair asserted, what the pair *implied* and
never said (these are the dangerous ones — unstated assumptions can't be
checked), and what the pair ruled out early without evidence.

## 2. Attack each one

For every surviving assumption, produce four fields. Vague entries in any of them
mean the assumption hasn't actually been attacked yet.

- **Fails if** — the specific condition under which this is false. Not "if we're
  wrong about scale" but "if sustained write throughput exceeds ~2k/s". A
  condition you couldn't recognize on sight isn't written sharply enough.
- **Cheapest evidence** — the smallest thing that would move belief: one query,
  one document, one conversation with the person who'd know, one afternoon's
  test. Prefer evidence obtainable this week over evidence that requires the
  project to be half-built.
- **Kill criterion** — the threshold at which the direction is abandoned rather
  than patched. Decide it now, while nothing is sunk. A direction with no kill
  criterion isn't a decision, it's an attachment.
- **Who would know** — the person, team, doc, or dataset that already holds the
  answer. Often the cheapest evidence is that someone has already checked.

## 3. Rank

Order by damage if wrong, then by cost to check. The top of the list is a
high-damage assumption that happens to be cheap to settle — that's the next
action, and it usually beats another round of discussion.

Separate three flavours of wrong, because they get different treatment:

| Flavour | What it means | Treatment |
|---|---|---|
| Wrong-and-recoverable | Costs time, direction survives | Note it, move on |
| Wrong-and-expensive | Costs rework or credibility | Get evidence before committing |
| Wrong-and-silent | Failure wouldn't announce itself for months | Build the detection now, not the fix |

Wrong-and-silent is the one discussions consistently miss, because the pair is
imagining failures they'd notice.

## 4. Report honestly

State plainly which assumptions survived the attack and why — a pass that finds
everything fragile is not more rigorous, it's less useful, and it trains the user
to discount the next one. Never invent a weakness the idea doesn't have.

Where the attack found nothing because you lack the domain knowledge to attack,
say that instead of producing a generic risk. "I can't evaluate whether the
vendor's throughput claim is plausible" is information; a manufactured concern
about vendor lock-in is noise.

## 5. Pre-mortem, when the attack comes up thin

If the assumption list feels tidy and nothing looks fragile, run the inversion
instead: assume it's twelve months later and this failed badly. Narrate why, in
past tense, concretely. The past tense matters — it licenses the specificity that
"what could go wrong" doesn't, and it routinely surfaces the failure the forward
pass suppressed.

Feed whatever it produces back into step 1 as new candidate assumptions.

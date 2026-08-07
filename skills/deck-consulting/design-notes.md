# deck-consulting — design notes

Development record and rationale. Not loaded at runtime; for maintainers.

## What this skill is

A presentation consultant that works one node at a time. Eleven nodes — `positioning`, `distill`,
`headline`, `outline`, `onepager`, `storyline`, `opening`, `closing`, `delivery`, `slidecheck`,
`layoutspec` — each with its own reference file, its own entry check, and one artifact on disk at
the end. The presenter enters a node, makes the decisions only they can make, and leaves with a
file. Nothing chains automatically.

The problem it addresses is not that presenters lack content. It is that they organize by what they
know instead of by what the room needs in order to say yes, and that the resulting deck covers the
topic while asking for nothing. Every node is judged against the positioning artifact, which is what
makes a cut defensible and a headline aimed rather than merely accurate.

## One skill with eleven nodes, not eleven skills

The obvious alternative was a skill per node — `deck-positioning`, `deck-headline`, and so on. It
was rejected on three grounds.

**Context load.** The eleven references total roughly 770 lines. Loading them together at every
invocation would be indefensible, so the split-skill design is often argued for on context grounds.
But the same saving is already available inside one skill: `SKILL.md` carries the node table and the
shared contracts, and a node's reference file is read only on entry. A session that wants five
headlines rewritten pays for `SKILL.md` plus `references/headline.md` and nothing else. The context
argument for splitting does not survive lazy reference loading.

**Cognitive load and the trigger surface.** Eleven skills means eleven descriptions competing in the
same trigger space, all about presentations, all firing on the same phrasings. The routing failure
that produces is worse than any context saving: the user says 「投影片太多講不完」 and eleven
near-identical descriptions each half-match. One skill with one description, which then names the
node, moves the routing decision from the trigger layer (where it is a guess against a description)
into the session (where the model has actually read the user's material).

**The positioning artifact is the shared foundation, and splitting it would create cross-skill
dependencies.** Nine of the eleven nodes read `positioning.md`. Under a split, that is a hard
`run deck-positioning first` prerequisite pointing from one skill into another — which this repo
forbids, both because a skill must complete its own job standalone and because the dependency graph
would be a fan-in on a single skill everything else needs. Inside one skill the same relationship is
a soft prerequisite: the node says what is missing, says what proceeding without it costs, offers
both paths, and does what the user picks. That degradation is only expressible when the nodes share
a runtime.

## User-invoked

`disable-model-invocation: true`. The deciding test is whether the model can usefully reach for this
on its own, and here it cannot. The skill opens a multi-turn consulting engagement that asks the
presenter for decisions and writes files into their working tree — a wrong autonomous entry costs
them a directory of artifacts and a conversation they did not ask for, which is a different order of
cost from a skill that produces one paragraph. The trigger phrasings are also generic enough
(「幫我看一下簡報」) that a model-invoked version would fire inside sessions that were about
something else, such as building slides programmatically.

The cost of user-invocation is discoverability, and it is real: someone with a deck problem has to
know this exists. That is paid down by the catalog entry and the guide rather than by opening the
trigger surface.

## Why state lives in files

`docs/deck-consulting/` holds the artifacts as plain Markdown. The alternative — carrying the
positioning, the outline and the storyline in the conversation — fails on three counts.

A deck is not built in one sitting. The positioning is settled on Monday, the storyline on Thursday,
and the layout review happens the night before. Conversation state does not survive that gap, and
re-establishing it costs the user a re-explanation each time.

Downstream nodes need to *read* their inputs, not be told about them. `storyline` reading
`outline.md` gets the actual section set; `storyline` being told about it gets a paraphrase that has
already drifted.

Staleness has to be visible. When `outline` is revised, the artifacts derived from it are wrong, and
files make that both detectable and nameable — the node can say which files just went stale and
offer to re-run them. In conversation the stale version is simply further up the scrollback, where
nobody will notice it contradicts the new one. `onepager` writing into `outline.md` rather than its
own file is the sharpest version of this bet: the compression sits directly beneath the structure it
compresses, so a structural change leaves the two visibly inconsistent.

The files are also the user's, in their repo, readable and editable without this skill. That matters
for a deliverable someone will hand to a designer or paste into a slide tool.

## Iteration log

### 2026-08-07 — v0.1.0 pre-ship dual run

Four cases from `evals/evals.json` (1 positioning, 3 headline traceability, 4 storyline with the
prerequisite absent, 5 slidecheck from a description), each run twice: once with the skill loaded,
once vanilla, as independent parallel agents launched together and unaware of each other. One
repetition per arm.

With-skill won every case. Decisively on 1, 4 and 5; narrowly on 3, where vanilla independently
produced a defensible sourced title and warned against 「證實」「顯著」 on its own.

Where the margin came from, case by case:

- **Case 1.** Vanilla gave strong substantive advice and no durable standard — no named starting
  point, no floor that survives refusal, nothing written down. With-skill produced the three-tier
  brief, three postures with sample lines, and a file path.
- **Case 3.** Both arms held the evidence line. With-skill additionally caught the ambiguity vanilla
  missed: 翊宸 not having reported is either a timing fact or a negative result, and which one it is
  changes the title.
- **Case 4.** Vanilla invented an ask ("請您裁示要走哪一個") and a budget-routing question the user
  never mentioned. With-skill left every unknown as a bracketed slot and put the ask back as the one
  open question, which is the traceability rule holding under time pressure.
- **Case 5.** Vanilla asserted 「九欄在會議室後排讀不到」 and 「投影必爆」 from a verbal description
  containing no type sizes — exactly the fabricated-rendering-finding failure. With-skill asserted
  no rendering fact and marked every inference.

One defect the run exposed and the fix: with-skill's first pass on case 5 stopped to ask the
viewing-condition question and delivered only a partial review, which contradicts the skill's own
no-node-blocks rule. `references/slidecheck.md` now states the assumption, asks in the same breath,
and delivers the full review in one reply. The re-run cleared all six of that case's expectations.

Contamination: one agent authored both the skill and this comparison, so the qualitative judgments
carry author bias. The deterministic parts — whether a figure survived verbatim, whether a rendering
claim was asserted from a description — are objective. Single repetition per arm, so a small margin
is not separable from sampling noise; the three decisive cases are not close enough for that to
matter, and case 3's narrow margin is reported as narrow rather than as a win.

### 2026-08-07 — round two, full coverage

Closed the four unrun cases (2, 6, 7, and a new case 8 for an English session), repeated case 3, and
rewrote the three conformance-phrased expectations as reader outcomes. With-skill now wins all eight.
Full write-up in `evals/results-2026-08-07.md`.

**The finding worth keeping: every defect this skill has produced so far is the same defect.** Three
rounds of fixes, three different nodes, one behaviour — the node asks before it delivers. `slidecheck`
gated on the viewing condition. `distill` gated on the positioning artifact and lost two cases
outright by never producing the points at all. The English session got Chinese section headings with
no explanation, which is the same shape one level down: the reply withholds something the reader
needs in order to act on what it just handed them.

That this kept happening is the interesting part, because `SKILL.md` already said no node blocks, in
those words, from the first draft. The rule was there and the nodes went around it — each one for a
locally good reason, and each one by narrowing the general rule while restating it. `distill` is the
clearest specimen: its entry check offered "run `positioning` first, or name the audience and the ask
in two lines", which reads like the two-path offer and is in fact two gates, because the escape hatch
the general rule provides — proceed on whatever is at hand — had quietly been dropped in the
restatement.

The structural lesson is about where a rule lives. A general rule restated inside eleven references
is eleven chances to restate it slightly wrong, and the wrongness is invisible at review time because
each local version reads reasonably on its own. The fix was to stop relying on the restatements and
give the rule its own paragraph upstream, in the one place every path passes through: a request that
already carries its own parameters is answered before it is questioned. Named as its own rule with
its own failure mode attached, rather than left as an implication of the soft-prerequisite paragraph
above it.

Also hardened, though no case failed on it: seven entry checks could not tell "input file absent"
from "file present, my section renamed", so a user's hand-edit degraded silently into the
missing-input path. Each now names the missing section and asks the one-word question without
waiting on the answer.

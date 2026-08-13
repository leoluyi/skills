# Humanizer (English + zh-TW)

This skill strips AI writing tells out of a draft. It runs two separate checks, and **one of them switches itself off depending on what kind of document you hand it** — that's the part most people get wrong, and the reason this page exists.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a humanizer-zh -y
```

Keep it current:

```
npx skills update humanizer-zh
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/humanizer-zh/SKILL.md)

## What it does

It hunts two different defects, and they're independent judgments:

**Something that shouldn't be there.** A phrase standing in for a fact.

> This platform doesn't just offer a rich, diverse range of courses — it lays a solid foundation for every employee's career growth.

"Doesn't just... it..." props up a contrast with no content behind it, "rich, diverse" never says how many courses, "lays a solid foundation" delivers nothing concrete. 45 rules chase this (of the 47 rules across 8 classes, minus the two — `hidden author` and `stance vacuum` — that flex by document type), and **every document type gets checked**.

**Someone missing.** Every sentence is individually fine, but nobody sounds like they wrote the whole thing.

> Self-hosting and managed hosting each have trade-offs, depending on team needs. Monthly versus annual billing is the same — it depends.

Not one sentence carries the author's own choice, a concrete time/amount/scenario, or a spoken-register break from the pattern. This is `hidden author` (作者隱身) — a whole-document judgment, visible only when you step back, and it only runs on signed-voice writing.

There are three finished-prose modes (rewrite, detect-only, edit-in-place), and a protected list locked before any edit — prices, dates, commitment clauses, named quotes, code — these stay exactly as written even if they technically match a rule; a hit there gets marked "protected," not rewritten. It **doesn't write for you**: when stripping the AI-voice leaves nothing behind, it flags the gap in place rather than inventing an experience to fill it; `hidden author` in particular only reports, never rewrites. It also **doesn't inject a voice** — giving a piece opinion, metaphor, and rhythm is addition, that's `blog-writing-zh`'s job; this skill only subtracts.

If no draft exists yet, but you manually invoke it to prepare writing context for a downstream planning or writing skill, read [writing preflight](https://github.com/leoluyi/skills/blob/main/skills/humanizer-zh/references/writing-preflight.md). This pre-draft handoff produces a writing contract, style guardrails, and gaps; it does not write the document or replace the skill that owns composition.

When you manually invoke it with no mode, exact file path, or draft content, it defaults to `preflight`. When you provide an exact file path without a mode, it stops and asks whether you want `detect` or `modify` instead of guessing.

## When to use

Reach for it as a final de-AI pass before shipping a README, ADR, blog post, or any English/Chinese draft that reads machine-generated.

## When not to

Use `blog-writing-zh` when you need to compose a piece or give it a human voice from scratch; this skill's `preflight` only prepares a writing handoff for the downstream writer and does not compose the document.

## How it works

The whole skill's logic in one sentence: **classify the genre first, lock down what can't be touched, then run two independent questions down two separate tracks, and finally check whether any fact got lost along the way.**

### Your document's genre decides whether check #2 runs

The skill first classifies what kind of document you gave it:

| | Examples | `hidden author` check |
|---|---|---|
| **Signed voice** | blog posts, newsletters, opinion pieces, deep-dive essays, personal writing | Runs |
| **Functional** | docs, README, reference, spec, RFP, SOP, official memos, 簽呈, project plans, proposals, investor letters | Skipped |

When it can't tell, it defaults to functional and says so.

**Why functional documents skip it.** Not laziness — that check is guaranteed to misfire on these. It's asking whether the author's judgment, experience, metaphor, tone, and rhythm are present, and a well-written 簽呈 shouldn't have any of those five. This gate sits in front of everything else.

That doesn't mean your memo is clean: turning off `hidden author` still leaves **the other rules running**. The 簽呈 example above gets:

```
Hidden author: not applicable (functional document)

5 hits:
・"Amid the wave of digital transformation..."        parachuted opening claim
・"doesn't just... it lays a solid foundation"          contrast + universal closer
・"rich, diverse"                                       empty-word filler
・"it's worth noting that"                              explainer-voice hedge
・"expected to significantly improve overall outcomes"  abstract claim, no deliverable
```

Seeing "not applicable" is not a clean bill of health — it only turns off one check, not the whole report.

### Proposal-type documents: judgment required, personality not

Project plans, proposals, and investor letters count as functional, but one rule is unusually strict with them:

**`stance vacuum`** — a proposal that spends the whole document saying "each option has trade-offs" without recommending anything gets flagged. The entire point of a proposal is to recommend something.

This rule leaves docs, README, spec, RFP, and SOP alone (those exist purely to state information), and leaves official memos alone too (the 擬辦 line is already their form of taking a position) — but it **does not** leave proposals alone.

The dividing line: proposals need the author's **judgment**, not their **personality**. So `stance vacuum` catches them, but the `hidden author` group (spoken-register breaks, invented metaphor, rhythm variation) doesn't — a formal proposal correctly has none of those; that's genre, not a defect.

### `--expect-author`: when you need it

Normally you don't. Blog posts get the `hidden author` check automatically, no flag required.

You need it when: **your document got classified as functional, but you believe it should read like someone wrote it.**

```
Check this client-facing project plan with --expect-author
```

Passing this flag is your declaration that "this draft should show an author" — the skill runs the check on that basis, and anything missing counts as a real finding. The report notes that this classification came from your declaration, not its own judgment, so you can retract it if you called it wrong.

It only works in one direction — the flag can push a document toward "check it," never turn a check off.

### The judgment pipeline: from draft to output

Step 1's genre classification isn't a warm-up — it's the fork the whole report branches on. Step 4's two tracks are the core of the skill and the most commonly misunderstood part — they ask two independent questions, and only one of them ever gets switched off by genre.

```
                         draft comes in
                               │
                               ▼
╭──────────────────────────────────────────────────────────────╮
│ 1. Context detection                                          │
│ Set the frame. Two calls, both ripple to the end              │
├──────────────────────────────────────────────────────────────┤
│ Language ─┬─ Chinese ──── zh rule layer                       │
│           ├─ English ──── en rule layer                       │
│           ╰─ mixed ────── each passage runs its own layer,    │
│                            terms of art stay in English       │
│                                                                │
│ Genre ─┬─ signed voice ── blog, newsletter, opinion, essay    │
│        ╰─ functional ──── docs, memos, 簽呈, project plans…   │
│                            defaults here when unclear, and    │
│                            says so                             │
╰──────────────────────────────────────────────────────────────╯
                               │
                               ▼
╭──────────────────────────────────────────────────────────────╮
│ 2. Lock the protected list                                     │
│ Ring-fence what can't be touched before any edit               │
├──────────────────────────────────────────────────────────────┤
│ Prices, dates, commitment clauses, named quotes, code,          │
│ and any deliberate register breaks you left in                 │
│ Once ringed, a rule hit there gets marked "protected," untouched│
╰──────────────────────────────────────────────────────────────╯
                               │
                               ▼
╭──────────────────────────────────────────────────────────────╮
│ 3. Scope decision                                              │
│ How wide a change this pass makes                              │
├──────────────────────────────────────────────────────────────┤
│ spot patch (default) / paragraph rewrite / full rewrite         │
╰──────────────────────────────────────────────────────────────╯
                               │
                               ▼
╭──────────────────────────────────────────────────────────────╮
│ 4. Rewrite by class                                             │
│ Two independent tracks, two different questions                 │
╰──────────────────────────────────────────────────────────────╯
                               │
               ╭───────────────┴────────────────╮
               ▼                                ▼
╭─────────────────────────────╮  ╭─────────────────────────────╮
│ A: something that shouldn't  │  │ B: is the author missing?  │
│    be there?                 │  │                             │
├─────────────────────────────┤  ├─────────────────────────────┤
│ 47 rules, 8 classes          │  │ hidden author, 1 rule       │
│ every genre runs it          │  │ 5 sub-signals, ≥2 to report │
│ functional genre is no pass  │  │ only signed-voice genres run│
│ unit: sentence, phrase       │  │ unit: whole document        │
│                              │  │ reports absence only, never │
│                              │  │ writes it in                │
╰─────────────────────────────╯  ╰─────────────────────────────╯
               ╰───────────────┬────────────────╯
                               ▼
╭──────────────────────────────────────────────────────────────╮
│ 5. Fidelity check                                              │
│ Did any fact get lost in the rewrite?                          │
├──────────────────────────────────────────────────────────────┤
│ Numbers, dates, names, commitments must match exactly          │
│ Re-audits what step 4 let through                              │
│ Fails → back to step 4 to re-judge                             │
╰──────────────────────────────────────────────────────────────╯
                               │
                               ▼
╭──────────────────────────────────────────────────────────────╮
│ 6. Pre-ship self-read                                           │
│ Read its own freshly rewritten draft cold                      │
├──────────────────────────────────────────────────────────────┤
│ Catches defects the rewrite itself introduced                  │
│ e.g. flattening tone that used to have variation                │
│ Reruns at most once; a third pass is just a full rewrite        │
╰──────────────────────────────────────────────────────────────╯
                               │
                               ▼
              output: genre call → per-class hits → fidelity check
```

The line between A and B is the thing this whole page keeps repeating: **when genre switches off B, A doesn't lose a single rule.**

Three finished-prose modes decide how you get the result back.
There is also a manual pre-draft handoff for a blank page.
When manually invoked without a mode, exact file path, or draft content, `preflight` is the default.
An exact file path without a mode opens a choice between `detect` and `modify`.
For supplied prose or a draft, an unspecified rewrite request still defaults to `detect`.

| How you asked | Mode | What you get |
|---|---|---|
| Invoke it directly with no mode, exact file path, or draft content | `preflight` | Reads the current context and returns a writing contract, positive style guidance, an evidence boundary, and gaps; does not write prose |
| "Get the AI-isms out of this," "make it sound human," or "rewrite this" | `rewrite` | Every hit (rule name + quote), the full rewritten text, a list of what changed |
| "Just flag it, don't change anything" | `detect` | Hits grouped P0/P1/P2, each marked hard-defect or judgment-call; original text untouched |
| With prose or a draft supplied, "take a look at this," "scan this document," or no explicit rewrite request | `detect` | Hits grouped P0/P1/P2, each marked hard-defect or judgment-call; original text untouched |
| Provide an exact path such as `draft.md` without a mode | choice prompt | Asks whether to `detect` or `modify`; does not audit or edit until the user chooses |
| Choose modify, or say "Edit draft.md directly" | `edit-in-place` | Reads the file, changes only the hit spans, re-reads once after editing, reports before/after per change; clean passages stay byte-identical |
| No draft exists and the user manually asks for a pre-draft writing handoff | `preflight` | Reads the brief, plan, sources, genre, and author preferences, then returns a writing contract and gap list; does not write prose. See [writing preflight](https://github.com/leoluyi/skills/blob/main/skills/humanizer-zh/references/writing-preflight.md) |

### The checklist: 8 classes, 47 rules

The rules aren't a flat list — they split into 8 classes, each catching a different failure mode:

| Class | Catches | Rules | Example |
|---|---|---|---|
| Content | words spent, no fact delivered | 7 | meaning inflation, empty-word filler, universal closer |
| Sentence patterns | the shape of the sentence doing the work instead of content | 13 | false-contrast structure, translationese, register drift |
| Style & layout | formatting substituting for actual structure | 6 | em-dash overuse, bullet-point bloat, table misuse |
| Interface residue | chat-interface and tool artifacts leaking into the document | 4 | sycophantic tone, stray AI-tool markers |
| Fact & citation | borrowing authority instead of earning it | 3 | vague attribution, hallucinated or unverified citation |
| Stance & opening | a call that should be made gets deferred, dodged, or dropped | 7 | parachuted opening claim, stance vacuum, hidden author |
| Manufactured drama | a reaction invented out of nowhere, with no consequence attached | 3 | canned-reaction shot, declared emotion |
| Breaking the fourth wall | the draft describing its own generation | 4 | self-referential document, self-endorsement, leaked reasoning process, seam between merged drafts |

Every hit comes with its rule name and the quote it matched, so anything the report shows you traces back to this table — "which class is this" is usually easier to remember than "what's this rule called."

Two mechanisms cut across every class rather than belonging to one: the **protected list** (decides what stays verbatim) and **scope** (decides how wide the edit goes).

### Cross-reference: genre decides which rules run

Putting "which document" and "which rule" side by side is clearest — inside "functional," `stance vacuum` and `hidden author` don't behave the same way:

| | docs / README / spec / RFP / SOP | official memos / 簽呈 | project plans / proposals / investor letters | blog / newsletter / opinion / personal essay |
|---|---|---|---|---|
| The other 45 rules | run | run | run | run |
| `stance vacuum` | off (neutral statement is the genre) | off (the 擬辦 line already is the stance) | **on** (a proposal that recommends nothing is exactly what this catches) | on |
| `hidden author` | off | off | off | on |

This table is why proposals and investor letters get flagged more often than memos — they match memos on "doesn't need personality," but not on "doesn't need judgment." `--expect-author` only moves the `hidden author` row from off to on; it leaves the other three rows alone.

### Common misreadings

| You might assume | What's actually true |
|---|---|
| Memos and SOPs skip the AI-ism check entirely | 45 rules still run; only `hidden author` is skipped |
| "Hidden author: not applicable" in the report means it's clean | That's the conclusion of one check — keep reading for the rest |
| You have to ask specially for it to check "does this feel soulless" | Blog posts get it automatically, no request needed |
| `--expect-author` turns the checks up in general | It only declares the genre, which activates `hidden author` for this document |
| A proposal that recommends nothing isn't a defect | `stance vacuum` flags it — that's exactly what the rule exists for |
| It'll make my writing sound more human | It only removes what shouldn't be there; what it can't add is left to you |

## Related skills

- **blog-writing-zh** — use it for composing from scratch or giving a draft a personal voice; it handles addition (opinion, metaphor, rhythm), while this skill handles subtraction and the optional pre-draft handoff.
- **avoid-china-writing** — catches mainland-China wording and stray Simplified characters, an orthogonal axis to de-AI cleanup; a document may need a pass from both.

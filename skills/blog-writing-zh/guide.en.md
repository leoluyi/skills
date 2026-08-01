# Traditional Chinese Blog Writer

This skill turns a topic, an Obsidian note, a talk transcript, or a foreign-language source into a Taiwan-Chinese (zh-TW) blog post or newsletter that reads like a specific person wrote it — with a stance, lived experience, and a voice tuned to seven studied blogs — rather than a well-organized machine summary. Manual trigger only — invoke it by name rather than expecting it to fire automatically.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a blog-writing-zh -y
```

Keep it current:

```
npx skills update blog-writing-zh
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/blog-writing-zh/SKILL.md)

## What it does

**Two modes.**

- `compose` — writes a full piece from a topic or loose material.
- `rewrite` — turns an Obsidian note, a translation source, a talk, or a rough draft into a blog post. Before touching voice, it first picks a rewrite strategy: faithful translation with editor-voice framing around it, or a fuller narrative reconstruction.

**Voice as four composable axes**, not one fixed "style":

| Axis | Options | Example |
|---|---|---|
| Opening strategy | scene hook · motive-then-obstacle-then-promise · direct declaration of stance · reader's-own-objections-answered-up-front · series recap-then-three-questions | a tense scene, or "I hit this wall three times before it clicked" |
| Persona intensity | L1 collapsed (first person only at open/close, formal register) · L2 moderate (occasional judgment calls, light asides) · L3 high (constant direct address, jokes, parenthetical asides) | L2: one or two casual asides per piece |
| Metaphor density | none/minimal · one-line analogy · full narrative metaphor with a payoff line · system-wide invented vocabulary reused throughout | "a linter is a tireless disciplinary committee" |
| Closing move | manifesto line · summary + well-wishes · hand responsibility back to the reader with a concrete action · hook for the next piece | "The tree won't sign that invoice for you." |

These four combine with structural framework, terminology handling, and title formula into eight elements total. Rather than asking you to tune all eight, a two-layer menu picks **article type** first — tutorial, concept primer, deep-dive, hands-on note, opinion/advocacy, teardown/review, or analytical framework — which fixes the structural skeleton, then **flavor** — 2-3 recommended author voices for that type, plus "no particular flavor" — which fixes persona intensity, metaphor type, terminology handling, and title formula.

**Length tiers**:

| Tier | Length | Typical use |
|---|---|---|
| 短打 (short) | 300-800 characters | one point, one hook — a social post or quick note |
| 標準 (standard) | 800-2000 | the default — a complete argument or tutorial, 3-5 sections |
| 深文 (deep) | 2000-5000 | multi-angle, skimmable subsections — a deep-dive or full tutorial |
| 工具書級 (reference-grade) | 5000+ | exhaustive coverage with tables — an upgrade guide or year-in-review |

The skill recommends a tier from the article type and material and states its reasoning in one sentence for confirmation, rather than forcing a choice. If a draft outgrows its tier mid-write, it flags upgrading the tier or splitting into a series rather than padding or cutting to fit.

**Dual-draft mode** (optional; suggested automatically once a draft is estimated at over ~1500 characters, falls in an argument-dense type like opinion/analytical-framework/deep-dive, or the user says it matters): write two full drafts that deliberately diverge along **one** axis — structure (the default recommendation for argument-heavy pieces, since two structural skeletons like "objection rebuttal" vs. "modular breakdown" tend to produce genuinely complementary strengths), opening, or depth tier. Both drafts share the same flavor. Each draft's strengths get diagnosed across seven dimensions (opening, argument, metaphor, rhythm, concreteness, closing, actionability/conceptual-clarity), then the stronger elements are welded — not pasted — into one final draft in a single consistent voice, with a one-line note on which draft supplied the skeleton and what got grafted in from the other.

**Automatic series-split check** — after a draft is finished, the skill evaluates on its own whether the material has outgrown a single post: a clear length overrun, a section strong enough to stand alone, multiple independent claims, or a staged dependency between parts. Only when one of those signals is clear does it append a one-line verdict, a reason, and a series outline (per-piece claim, working title, dependency order, recipe, and cross-piece continuity mechanism). Most drafts stay single pieces, and this check doesn't surface on every output — that would be noise.

Every output ships the finished article plus 3-5 title/subtitle candidates, spanning at least two title formulas (how-to, decode/reveal, big-question, either/or, anxiety-defusing breakdown, imperative address, bait-and-reveal), each tagged with a suggested publishing context — SEO, social, or newsletter.

## When to use

Reach for this when you need to write or rewrite a Taiwan-Chinese blog post or newsletter, or turn Obsidian notes, talks, or foreign-language articles into a long-form zh-TW piece with an actual authorial voice behind it.

## When not to

- Formal internal memos or 簽呈 — use `formal-doc-structure`.
- RFPs or 需求規格書 — use `rfp-writing`.
- Explaining a single term in plain language for a non-technical reader — use `plain-speak`.
- Cleaning up an already-finished draft's AI-isms with no restructuring or voice work involved — use `humanizer-zh` directly.

## How it works

**Picking the voice preset.** The skill doesn't ask you to specify eight parameters cold. When you haven't named a style, it infers two things from your material and request: what the reader should be able to do after reading (follow a recipe, understand a concept, be persuaded to change practice, decide whether to buy, absorb one useful finding fast), and the reader's relationship to the topic (scared of it, half-familiar and prone to mistakes, unfamiliar and needing a hook, an expert peer with no patience for preamble, or currently being marketed at). Those two answers pick a recommended article type plus flavor; three further variables calibrate it — technical level shifts terminology handling, closeness to the reader shifts persona intensity, and publishing context shifts title formula and length. The skill then proposes one primary recommendation plus at most one alternative, each with a one-line reason, rather than listing all seven article types for you to parse.

**The pipeline handoff to humanizer-zh.** Once a draft is finished, this skill doesn't just suggest a follow-up cleanup pass — in any environment that can load sibling skills, it actively invokes `humanizer-zh` itself as the de-AI finishing step, in three stages:

1. **Detect first.** Hand the draft to `humanizer-zh` in `detect` mode: get back every flagged AI-ism plus the matched text, with nothing rewritten yet.
2. **This skill filters the hit list.** Checked against the chosen flavor's style reference, hits that are actually this piece's positive features — an opinionated judgment call, first-person experience, an invented metaphor, deliberately uneven rhythm, visible thinking-in-progress ("I first assumed X, then realized..."), a flavor's signature sentence pattern — get marked exempt. Only the genuinely mechanical AI patterns (empty slogans, false-contrast filler, over-translated jargon, reflexive triads) and anything already flagged P0 downstream (leaked tool markers, sycophancy, unverified claims) stay on the list. A typical filtered list looks like:

   ```
   hit: "老實說我一開始也搞不懂這段"        → exempt (thinking-in-progress, this flavor's signature)
   hit: "這不僅是一個工具，更是一種哲學"    → keep (false-contrast filler, mechanical)
   hit: "值得注意的是"                       → keep (explainer-voice hedge, mechanical)
   hit: single-sentence paragraph, three in a row → exempt (deliberate rhythm break)
   ```

3. **Only the non-exempt items go back for an actual rewrite**, in `rewrite` or `edit` mode, with the exempt list passed along as a hard constraint the downstream pass must not touch.

This exists because a plain rewrite pass, run directly, flags a large share of intentional voice as if it were noise and can flatten it right alongside genuine AI-isms — the filtering has to happen on the side that actually knows what this piece's voice is supposed to sound like. The voice profile passed downstream keeps the register aligned — a 高見龍-flavored piece maps to `--voice casual`, a 保哥-flavored one to `--voice professional/technical`, a Simon Willison-flavored one to `--voice technical` — and a dual-draft merge always gets this pass, since the welded seams are where AI-isms most often survive. If the source material carried mainland-China (簡體/大陸) usage risk, `avoid-china-writing` runs immediately after in the same handoff. After either returns, this skill checks the diff for over-eager cuts to signature lines, single-sentence paragraphs, or emoticons before treating the result as final.

**The whole shape, end to end.**

```
                    topic / note / talk / draft comes in
                                   │
                                   ▼
╭──────────────────────────────────────────────────────────────╮
│ 1. Mode + preset                                               │
│ compose or rewrite; article type × flavor × length tier        │
├──────────────────────────────────────────────────────────────┤
│ rewrite mode picks a source strategy first                     │
│ (faithful translation + editor frame, or narrative reconstruct) │
│ preset comes from reader-outcome + reader-relationship,         │
│ calibrated by technical level, closeness, publishing context    │
╰──────────────────────────────────────────────────────────────╯
                                   │
                                   ▼
╭──────────────────────────────────────────────────────────────╮
│ 2. Draft (optionally dual)                                      │
├──────────────────────────────────────────────────────────────┤
│ single draft (default) ── or ──                                 │
│ two drafts diverging on one axis → diagnosed on 7 dimensions    │
│ → welded into one final draft, same voice throughout            │
╰──────────────────────────────────────────────────────────────╯
                                   │
                                   ▼
╭──────────────────────────────────────────────────────────────╮
│ 3. Titles                                                       │
│ 3-5 title/subtitle pairs, ≥2 formulas, tagged by publish context │
╰──────────────────────────────────────────────────────────────╯
                                   │
                                   ▼
╭──────────────────────────────────────────────────────────────╮
│ 4. Pipeline handoff (active, not a suggestion)                  │
├──────────────────────────────────────────────────────────────┤
│ humanizer-zh detect → this skill exempts intentional voice →    │
│ humanizer-zh rewrites only the rest                              │
│ + avoid-china-writing if PRC usage risk                         │
│ this skill re-checks the diff before accepting it as final       │
╰──────────────────────────────────────────────────────────────╯
                                   │
                                   ▼
╭──────────────────────────────────────────────────────────────╮
│ 5. Series-split check (automatic, silent unless triggered)      │
├──────────────────────────────────────────────────────────────┤
│ length overrun / standalone section / independent claims /      │
│ staged dependency → verdict + outline appended                  │
│ otherwise: ship the single piece, no prompt                      │
╰──────────────────────────────────────────────────────────────╯
                                   │
                                   ▼
                    output: article + titles + recipe log
```

## Related skills

- **humanizer-zh** — this skill invokes it automatically as the mandatory de-AI finishing pass once a draft is done; it only subtracts AI-isms and never supplies voice, which is this skill's job.
- **avoid-china-writing** — invoked conditionally, right after humanizer-zh, when the source material risked leaking mainland-China (簡體/大陸) usage into the draft.
- **formal-doc-structure** — use it instead for structured internal business documents (簽呈, meeting records, evaluation reports) where the goal is institutional clarity, not a personal voice.
- **rfp-writing** — use it instead for issuer-side RFPs and 需求規格書, which follow formal structural rules this skill doesn't apply.
- **plain-speak** — use it instead when the ask is lowering one term or passage for a non-technical reader, not producing a full article with structure and voice.

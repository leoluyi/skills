---
name: avoid-ai-writing-zh
description: Audit and rewrite content to remove AI writing patterns ("AI-isms") in BOTH English and Traditional Chinese (Taiwan / \u53F0\u7063 business usage). Use when asked to "remove AI-isms," "clean up AI writing," "make this sound less like AI," \u6216\u300C\u53BB\u9664 AI \u5473\u300D\u300C\u628A\u9019\u6BB5\u4E2D\u6587\u6539\u6210\u4EBA\u8A71\u300D\u300C\u6F64\u98FE\u6210\u6B63\u5F0F\u4F46\u4E0D\u50CF AI \u7684\u4E2D\u6587\u300D. Adds a Traditional-Chinese layer the English-only avoid-ai-writing lacks: \u7A7A\u8A71\u53E3\u865F (\u5168\u9762\u63D0\u5347 / \u8CE6\u80FD / \u6253\u9020\u5B8C\u6574\u751F\u614B), \u4E0D\u662F\u2026\u800C\u662F\u2026 contrarian structure, copula inflation (\u4F5C\u70BA / \u626E\u6F14\u8457), significance inflation (\u81F3\u95DC\u91CD\u8981 / \u4E0D\u8A00\u800C\u55BB), and AI sentence templates (\u5728\u7576\u4ECA\u2026\u7684\u6642\u4EE3 / \u96A8\u8457\u2026\u7684\u5FEB\u901F\u767C\u5C55). Supports detect / rewrite / edit modes, voice profiles, and an iterate-to-convergence pass. Prefer this over avoid-ai-writing whenever the text is Traditional Chinese or mixed zh/en.
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Conor Bronsdon
  adapted_by: Lu Yi
  adaptation: Traditional Chinese (Taiwan) AI-ism layer added; mined from personal rfp-writing and formal-doc-structure skills. Forked from upstream avoid-ai-writing v3.10.0 (MIT).
  tags: writing editing voice quality zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\u270D\uFE0F"
---

# Avoid AI Writing (zh-TW) — Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

**Language.** This fork handles English and Traditional Chinese (Taiwan business usage). Detect the dominant language from the input: if the text contains CJK characters, apply the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section in addition to any English rules that fit; for pure-English text, the English rules below are the whole job. In mixed zh/en text, audit each language with its own ruleset — do not romanize Chinese or translate English to "fix" it. Keep standard English technical terms (API, Kubernetes, CI/CD) in English inside Chinese prose; that is correct Taiwan usage, not an AI tell.

## What this skill is and isn't

This is a **writing-quality tool**, not a verdict. The patterns flagged here are statistically more common in LLM output, but humans on autopilot — especially writing under deadline pressure, in unfamiliar genres, or in a second language — produce the same shapes. Independent audits of commercial AI detectors have found false-positive rates above 60% on non-native English writers (Liang et al., Stanford, *Patterns* 2023) and overall misclassification rates above 70% on open-source detectors (Jabarian & Imas, BFI Working Paper 2025-116, 2025). Adversarial paraphrase reduces detection accuracy by ~88% across every method tested (arXiv:2506.07001, 2025).

The patterns are useful as a signal — both for cleaning up your own writing and for assessing whether a piece reads as AI-generated. Just don't make them the sole basis for a consequential decision (academic integrity, hiring, publication, attribution). Several rules here also fire on second-language writing, deadline-pressed humans, and technical genres that compress vocabulary by design. Pair the signal with context: who wrote it, what genre, what the writer's normal voice looks like, what other evidence you have.

In short: signals, not proof. Worth acting on; not worth ruining someone's day over.

## Modes

This skill operates in one of three modes:

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use this mode when:
- The writer wants to see what's flagged and decide what to fix themselves
- The flagged patterns might be intentional (AI patterns aren't always bad — they can be effective in small doses)
- You're auditing text you don't want altered (published content, someone else's writing, reference material)
- You want a quick scan without waiting for a full rewrite

**`edit`** — Edit a file in place rather than returning rewritten text. Use this when the writer points you at a file ("clean up `draft.md`", "fix the AI-isms in this file directly") and wants the file changed, not a copy to paste back. Make **minimal, targeted edits** with the Edit tool — change the flagged spans, not the whole document. **Preserve passages that are already human**: if a paragraph has no tells, leave it untouched. **Don't edit quoted material, code blocks, or text attributed to someone else** — flag those instead of rewriting them. For a large file, confirm which section to clean before changing anything. After editing, re-read the file and confirm the flagged patterns are resolved.

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," "what AI patterns are in this," or similar. Trigger edit mode when the user names a file and asks you to fix or clean it in place. Default to rewrite mode if not specified.

**Invocation.** Natural language is enough ("rewrite this in a blunt voice for LinkedIn," "edit `post.md` in place," "scan this, don't rewrite"). Power users can also pass explicit options, which map to the sections below: `[--mode rewrite|detect|edit]`, `[--voice casual|professional|technical|warm|blunt]`, `[--context linkedin|blog|technical-blog|investor-email|docs|casual]`, `[--file PATH]`, `[--iterate N]` (max 2).

**Iterate to convergence (optional).** Rewrite mode already runs one corrective second pass (see Output format) — that built-in pass *is* pass 2, so `--iterate` does not stack on top of it. When the writer asks to "iterate," "keep going until it's clean," or passes `--iterate N`, repeat the audit→rewrite cycle until no patterns remain or **N passes** are reached. Cap **N at 2**: a rewrite plus one corrective pass clears the flagged patterns, and a third pass costs a full regeneration while rarely finding more. Report how many passes it took ("converged in 2 passes").

---

In **rewrite** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Rewrite it**: return a clean version with all AI-isms removed
3. **Show a diff summary**: briefly list what you changed and why

In **detect** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Assess it**: note which flags are clear problems vs. patterns that may be intentional or effective in context

In **edit** mode, your job is to:

1. **Read** the file the writer named
2. **Edit in place**: apply minimal, targeted fixes to the flagged spans with the Edit tool, leaving already-human passages untouched
3. **Verify**: re-read the file and confirm the flagged patterns are resolved; report what you changed

---

## What to remove or fix

### Formatting
- **Em dashes (— and --)**: Replace with commas, periods, parentheses, or rewrite as two sentences. Target: zero. Hard max: one per 1,000 words. This applies to headings and section titles too, not just body prose. Catch both the Unicode em dash (—) and the double-hyphen substitute (--).
- **Bold overuse**: Strip bold from most phrases. One bolded phrase per major section at most, or none. If something's important enough to bold, restructure the sentence to lead with it instead.
- **Emoji in headers**: Remove entirely. No `## 🚀 What This Means`. Exception: social posts may use one or two emoji sparingly — at the end of a line, never mid-sentence.
- **Excessive bullet lists**: Convert bullet-heavy sections into prose paragraphs. Bullets only for genuinely list-like content (feature comparisons, step-by-step instructions, API parameters).
- **Curly quotation marks (“ ” ‘ ’) and apostrophes**: Curly quotes and apostrophes (U+201C/U+201D, U+2018/U+2019) are a *weak* paste-from-chat signal — meaningful mainly in plain-text contexts like code comments, commit messages, or plaintext drafts, where nothing auto-curls. Treat as corroborating, never conclusive: Word, Google Docs, macOS, and iOS curl quotes by default, so most human prose contains them too. Don't flag curly apostrophes (U+2019) on their own. Replace with straight quotes in plain-text/code; leave them in finished publications and locale-correct punctuation (French « », German „ “).

### Sentence structure
- **"It's not X — it's Y" / "This isn't about X, it's about Y"**: Rewrite as a direct positive statement. Max one per piece, and only if it serves the argument.
- **Hollow intensifiers**: Cut `genuine`, `real` (as in "a real improvement"), `truly`, `quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`. Just state the fact.
- **Vague endorsement ("worth [verb]ing")**: Cut or replace `worth reading`, `worth paying attention to`, `worth a look`, `worth exploring`, `worth checking out`, `worth your time`. These substitute a generic thumbs-up for a specific reason. Say *why* something matters instead.
- **Hedging**: Cut `perhaps`, `could potentially`, `it's important to note that`, `to be clear`. Make the point directly.
- **Missing bridge sentences**: Each paragraph should connect to the last. If paragraphs could be rearranged without the reader noticing, add connective tissue.
- **Compulsive rule of three**: Vary groupings. Use two items, four items, or a full sentence instead of triads. Max one "adjective, adjective, and adjective" pattern per piece.

### Words and phrases to replace

Words are organized into three tiers based on how reliably they signal AI-generated text. This tiered approach — adapted from [brandonwise/humanizer](https://github.com/brandonwise/humanizer)'s vocabulary research — reduces false positives on words that are fine in isolation but suspicious in clusters.

- **Tier 1 — Always flag.** These words appear 5–20x more often in AI text than human text. Replace on sight.
- **Tier 2 — Flag in clusters.** Individually fine, but two or more in the same paragraph is a strong AI signal. Flag when they appear together.
- **Tier 3 — Flag by density.** Common words that AI simply overuses. Only flag when they make up a noticeable fraction of the text (roughly 3%+ of total words).

#### Tier 1 — Always replace

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why it matters |
| hit differently / hits different | (say what specifically changed, or cut) |
| utilize | use |
| watershed moment | turning point, shift (or describe what changed) |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut — say something specific or nothing) |
| only time will tell | (cut — say something specific or nothing) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite what makes it busy) |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities, or use "problems" / "details") |
| ever-evolving | changing, growing (or describe how) |
| enduring | lasting, long-running (or cite how long) |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe their actual contribution) |
| best practices | what works, proven methods, standard approach |
| at its core | (cut — just state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |
| keen (as intensifier) | interested, eager, enthusiastic (or cut — just state the interest) |
| symphony (metaphor) | (describe the actual coordination or combination) |
| embrace (metaphor) | adopt, accept, use, switch to |

#### Tier 2 — Flag when 2+ appear in the same paragraph

These words are legitimate on their own. When two or more show up together, the paragraph likely needs a rewrite.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape (or describe what changed) |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed (or name the actual nuance) |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets, or cut) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging (or cite a number) |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| underpinning / underpinnings | basis, foundation, what supports |

#### Tier 3 — Flag only at high density

These are normal words. Only flag them when the text is saturated with them — a sign that AI filled space with vague praise instead of specifics.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |

#### Tier 3 phrases — Flag at density or in clusters

Multi-word boilerplate that's individually unobjectionable but stacks heavily in AI-generated content (crypto, web3, DePIN, AI/infra reviews are the worst offenders). Flag at **2+ uses of the same phrase** (the per-phrase rule — lower threshold than single-word Tier 3 because a two-word match repeated twice is already stronger evidence than re-using "significant"), *plus* a **cluster rule**: three or more *distinct* phrases from this table in one piece is a strong signal even when each phrase only appears once — that's the shape LLMs take when they vary their own boilerplate to seem less repetitive.

| Phrase | What to do |
|---|---|
| emerging sector / emerging space / emerging category | Name the actual sector or what's emerging about it |
| the integration of (X with Y) | Describe what's being integrated and what changes for the user |
| the intersection of (X and Y) | Pick the specific overlap that matters or cut the framing |
| community-driven | Name what the community does. "Community-driven" alone is filler |
| long-term sustainability | Cite the time horizon and the constraint. "Long-term" is hand-waving |
| user engagement | Name the action. "Engagement" is a wrapper around clicks/comments/retention |
| decentralized compute | Specify the architecture or cut. The phrase has become a category label, not a claim |
| (sustainable) reward emissions | Cite the emission schedule and the sink |
| tokenized incentive structures | Describe the actual mechanism (vesting, gauge, bonded LP, etc.) |
| designed for long-term [X] | Cut "designed for" — either it is or it isn't. Then state the property |

### Template phrases (avoid)

These slot-fill constructions signal that a sentence was generated, not written. If a phrase has a blank where a noun or adjective could go and still sound the same, it's too generic.

- "a [adjective] step towards [adjective] AI infrastructure" → describe the specific capability, benchmark, or outcome
- "a [adjective] step forward for [noun]" → same rule: say what actually changed
- "Whether you're [X] or [Y]" → false-breadth construction. Pick the audience you're actually addressing, or cut. "Whether you're a startup founder or an enterprise architect" means nothing — it's just "everyone."
- "I recently had the pleasure of [verb]-ing" → review/social AI pattern. Just say what happened: "I talked to," "I read," "I attended."

### Transition phrases to remove or rewrite
- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or use "and," "also," "on top of that"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" / "Here's what stood out" → reader-steering frames. Let the content signal its own importance. If you need a lead-in, make it specific: "The revenue number matters because..." not "Here's the interesting part."
- "In conclusion" / "In summary" / "To summarize" → your conclusion should be obvious
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," or "however." Don't overuse any one of them.

### Structural issues
- **Uniform paragraph length**: Vary deliberately. Include some 1-2 sentence paragraphs and some longer ones. If every paragraph is roughly the same size, fix it.
- **Formulaic openings**: If the piece opens with broad context before getting to the point ("In the rapidly evolving world of..."), rewrite to lead with the news or the insight. Context can come second.
- **Suspiciously clean grammar**: Don't sand away all personality. Deliberate fragments, sentences starting with "And" or "But," comma splices for effect: if the natural voice uses them, keep them.

### Significance inflation
- Phrases like "marking a pivotal moment in the evolution of..." or "a watershed moment for the industry" inflate routine events into history-making ones. State what happened and let the reader judge significance.
- If the sentence still works after you delete the inflation clause, delete it.

### Generic future-narrative closers
- "May become one of the most important narratives of the next market cycle," "could become the defining trend of the coming decade," "is poised to become the next major chapter in [X]." AI defaults to this shape when it needs to land a closing thought without committing to a falsifiable claim. The closer is grammatically a prediction but contains no testable content.
- Pattern: modal (may / could / will / is poised to) + "become" + (one of) the most [adjective] + (narrative / story / trend / theme / chapter / movement / force).
- Fix: pick the falsifiable version. "DePIN compute may exceed AWS spot pricing for embarrassingly parallel workloads by 2027" is a prediction. "The intersection of AI and DePIN may become one of the most important narratives of the next market cycle" is not.

### Hedge-stacked predictions
- Stacking a modal with a hedge adverb: "could potentially create," "may eventually unlock," "might ultimately transform." Either word alone is acceptable; the stack is the tell. Each hedge cancels the next, leaving a sentence that asserts nothing while sounding cautious and thoughtful.
- Fix: pick one. If you mean "could create," say that. If you mean "potentially creates," say that. Both together is filler.

### "Real/actual" adjective inflation
- "Real on-chain tokenomics," "actual reward sustainability," "genuine utility," "true product-market fit." Using `real` / `actual` / `genuine` / `true` as an empty intensifier on an abstract noun implies the rest of the field is fake or superficial — without naming what makes this instance the real one. Common in crypto/AI/web3 content where the writer wants to signal sophistication.
- Distinct from the existing "hollow intensifiers" rule (genuine / truly / quite frankly as sentence-level hedges). This is the noun-modifier form, where the intensifier latches onto an abstract noun to manufacture a contrast that goes unsaid.
- **Carve-out — named contrast:** if the sentence explicitly names what the fake/superficial version is, leave it. "Real on-chain settlement, not bridged IOUs" or "actual revenue from paying customers, not grants" is honest contrastive writing. The AI tell is the unsaid contrast.
- Fix when no contrast is named: drop the adjective and add the specific claim. "Reward sustainability" → "rewards funded from $X/mo in fees rather than emissions."

### Hashtag stuffing
- Long trailing hashtag blocks (6+ hashtags on a single short post) are near-universal in LLM-generated social content and rare in thoughtful human posts. The block usually mixes a project-specific tag with broad category tags (#AI #Crypto #Web3 #Innovation #FutureTech #Technology) — the categorical ones do nothing for discoverability and read as bot output.
- **Why 6?** Empirical floor. LinkedIn and X organic engagement plateaus or declines past 3-5 tags; human posts that exceed 5 are usually launch posts trading reach for engagement, while LLM-generated posts default to 10-15. Six is the threshold where false positives on legitimate human use start dropping below false negatives on AI output. The detector treats 6+ as a hard flag; the spec treats 5+ as a soft tell worth a second look on `linkedin` and `investor-email` profiles.
- Fix: 2-3 specific tags max, or none. If a hashtag wouldn't help a reader find related work, it's filler.

### Bullet lists of bare noun phrases
- A list of 5+ consecutive bullet items where each item is a short (≤6 word) adjective-plus-noun phrase with no verb. "Stable mining efficiency / Reliable pool connectivity / Optimized RandomX performance / Low failed share rates / Effective hardware utilization / Consistent thermal stability." Reads as a marketing one-pager because that's the shape LLMs default to when asked to summarize features.
- The tell is the *symmetry*: every item is the same grammatical shape, every item is parallel in length, none of them assert anything checkable. A genuine list of observations would have varying length, occasional verbs, and at least one item that doesn't fit the pattern.
- Fix: convert to prose paragraph, or rewrite items as full claims ("Failed shares stayed under 1% across a 12-hour run" beats "Low failed share rates"). If the list is genuinely the right form, vary the items so each carries a different shape of information.
- This rule does *not* apply to genuine list content (changelog entries, todo lists, parameter docs, ingredient lists) where bare noun phrases are the correct form. The detector keys on absence of finite verbs to separate the two — but in prose audits, ask whether the bullets are summarizing claims (rewrite) or enumerating items (leave).

### Copula avoidance
- AI text avoids "is" and "has" by substituting fancier verbs: "serves as," "features," "boasts," "presents," "represents." These sound like a press release.
- Default to "is" or "has" unless a more specific verb genuinely adds meaning.

### Synonym cycling
- AI rotates synonyms to avoid repeating a word: "developers… engineers… practitioners… builders" in the same paragraph. Human writers repeat the clearest word.
- If the same noun or verb appears three times in a paragraph and that's the right word, keep all three. Forced variation reads as thesaurus abuse.

### Vague attributions
- "Experts believe," "Studies show," "Research suggests," "Industry leaders agree" — without naming the expert, study, or leader. Either cite a specific source or drop the attribution and state the claim directly.

### Filler phrases
- Strip mechanical padding that adds words without meaning:
  - "It is important to note that" → (just state it)
  - "In terms of" → (rewrite)
  - "The reality is that" → (cut or just state the claim)
- Note: "In order to," "Due to the fact that," and "At the end of the day" are covered in the word/phrase table and transition sections above — don't duplicate rules.

### Generic conclusions
- "The future looks bright," "Only time will tell," "One thing is certain," "As we move forward" — these are filler disguised as conclusions. Cut them. If the piece needs a closing thought, make it specific to the argument.

### Chatbot artifacts
- "I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Feel free to reach out," "Let me know if you need anything else" — these are conversational tics from chat interfaces, not writing. Remove entirely.
- Also watch for: "In this article, we will explore…" or "Let's dive in!" — these are AI-generated meta-narration. Cut or rewrite with a direct opening.

### "Let's" constructions
- "Let's explore," "Let's take a look," "Let's break this down," "Let's examine" — AI uses "let's" as a false-collaborative opener to ease into a topic. It's filler that delays the actual point. Just start with the point. "Let's dive in" is covered above under chatbot artifacts, but the pattern is broader than that — flag any "let's + verb" that's functioning as a transition rather than a genuine invitation to act.

### Notability name-dropping
- AI text piles on prestigious citations to manufacture credibility: "cited in The New York Times, BBC, Financial Times, and The Hindu." If a source matters, use it with context: "In a 2024 NYT interview, she argued..." One specific reference beats four name-drops.

### Superficial -ing analyses
- Strings of present participles used as pseudo-analysis: "symbolizing the region's commitment to progress, reflecting decades of investment, and showcasing a new era of collaboration." These say nothing. Replace with specific facts or cut entirely.
- The same move shows up without the -ing: declarative "meaning-telling" that glosses a mundane subject as if it were profound — "this represents a broader shift," "the decision symbolizes a commitment to excellence," "it speaks to a larger trend in the industry." If the significance is real, show it with a specific consequence; otherwise cut. Adapted from `Aboudjem/humanizer-skill` P40.

### Promotional language
- AI defaults to tourism-brochure prose: "nestled within the breathtaking foothills," "a vibrant hub of innovation," "a thriving ecosystem." Replace with plain description: "is a town in the Gonder region," "has 12 startups." If you wouldn't say it in conversation, cut it.

### Formulaic challenges
- "Despite challenges, [subject] continues to thrive" or "While facing headwinds, the organization remains resilient." This is a non-statement. Name the actual challenge and the actual response, or cut the sentence.

### False ranges
- AI creates false breadth by pairing unrelated extremes: "from the Big Bang to dark matter," "from ancient civilizations to modern startups." These sound sweeping but say nothing. List the actual topics or pick the one that matters.

### Inline-header lists
- Bullet lists where each item starts with a bold header that repeats itself: "**Performance:** Performance improved by..." Strip the bold header and write the point directly. If the list items need headers, they should probably be paragraphs.

### List-label periods
- In bulleted lists where each item leads with a short label, LLMs end the label with a period and then run the explanation as a separate sentence. A person writing the same list almost always uses a colon instead. Strongest form: bold labels (`**Intros.**`, `**Content distribution.**`, `**Developer GTM.**` where a human writes `**Intros:**`). Weaker but still a tell: the same shape without bold (`- Intros. Years of conferences and operator network.`) — a short noun-phrase label terminated with a period at the start of a bullet, followed by a gloss. The colon reads as "here's what this label means"; the period reads as a sentence that the following clause then contradicts by continuing. Example tell: `- **Intros.** Years of conferences and operator network.` becomes `- **Intros:** years of conferences and operator network.` Fix the period to a colon and lowercase the start of the gloss, or drop the label and write the point as a plain sentence. Carve-outs: when the label span is a full sentence on its own (not a label introducing a gloss), the period is correct; and for the unbolded form, only flag when the leading fragment is clearly a label (a 1-4 word noun phrase, no verb) — a short complete sentence opening a bullet is fine.

### Title case headings
- AI over-capitalizes headings: "Strategic Negotiations And Key Partnerships" instead of "Strategic negotiations and key partnerships." Use sentence case for subheadings. Title case only for the piece's main title, if at all.

### Hyphenated-pair overuse
- AI stacks compound modifiers: "a high-quality, well-architected, future-proof solution." Two distinct problems. First, density — strings of hyphenated adjectives piled on one noun; cut to the modifier that actually matters. Second, the attributive/predicate error: a compound is hyphenated *before* the noun ("a high-quality report") but not *after* a linking verb ("the report is high quality," no hyphen). AI frequently hyphenates the predicate form; fix it to two words. Adapted from `blader/humanizer` P26.

### Cutoff disclaimers
- "While specific details are limited based on available information," "As of my last update," "I don't have access to real-time data." These are model limitations leaking into prose. Either find the information or remove the hedge. Never publish a sentence that admits the writer didn't look something up.

### Speculative gap-filling
- When the model lacks a fact, it fills the gap with hedged speculation dressed up as background: "maintains a relatively low public profile," "is believed to have," "likely began his career in," "appears to have studied." These are guesses formatted as statements. Distinct from cutoff disclaimers, which *admit* the gap — this one hides it behind plausible-sounding filler, which is worse because the reader can't tell what's known from what's invented. Cut the speculation, or replace it with a sourced fact. Adapted from `blader/humanizer` P21.

### Unfilled placeholders
- Bracketed slot-fillers that were meant to be replaced before publishing: `[Your Name]`, `[INSERT SOURCE URL]`, `[Describe the specific section]`, `2025-XX-XX`, `<!-- Add citation if available -->`. These are near-definitive evidence that AI-generated boilerplate was pasted without editing. Humans use placeholders in templates too, but rarely ship them. Treat any visible placeholder as a publishing bug: fill it in with real content or delete the sentence entirely.
- Catch the obvious shapes: `\[(?:Your|Insert|Add|Enter|Describe|Specify|Choose)[^\]]+\]`, `\b\d{4}-XX-XX\b`, HTML/Markdown comments with placeholder verbs (`add`, `fill in`, `todo`, `insert`).

### Chatbot citation markup leaks
- Internal citation tokens that leak through when text is copy-pasted from chat UIs: `citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`, `grok_card`. These are not patterns — they are fingerprints. Their presence is essentially proof the text was generated by a specific chat tool and pasted without cleanup.
- The fix is mechanical: strip every markup token. If a citation was meaningful, replace it with a real reference. Don't try to humanize the markup — delete it.
- Adapted from `Aboudjem/humanizer-skill` P34. Worth catching even when nothing else in the text reads as AI — the token itself is enough.

### AI-tool URL parameters
- Tracking parameters that AI tools auto-append to URLs they generate, surviving copy-paste into published content: `utm_source=chatgpt.com`, `utm_source=copilot.com`, `utm_source=openai`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`. Same logic as citation markup leaks — the presence of the parameter is the signature, regardless of what the surrounding text reads like.
- The fix: strip the parameter from every URL. Keep the URL itself if the link is meaningful; lose the parameter entirely. Adapted from `Aboudjem/humanizer-skill` P35.

### Novelty inflation
- AI text treats established concepts as if the speaker invented or discovered them: "He introduced a term," "She coined the phrase," "a concept nobody's naming," "a failure mode nobody talks about." In reality, most ideas in a conversation are applications of existing concepts, not inventions.
- Two problems. First, it's factually risky: if the concept already has a Wikipedia page or conference talks from last year, claiming novelty makes the writer look uninformed. Second, it flatters the subject in a way that reads as promotional rather than analytical.
- The fix: describe what the person *did with* the concept, not that they discovered it. "Michel walked through how context poisoning works in practice" instead of "Michel introduced a term I hadn't heard before: context poisoning." If you're unsure whether something is novel, assume it isn't and frame accordingly.
- Related patterns to flag: "the failure mode nobody's naming," "a problem nobody talks about," "the insight everyone's missing," "what nobody tells you about." These are engagement-bait framings that claim scarcity of knowledge where none exists.

### Infomercial engagement hooks
- Punchy fragment-hooks that tee up a reveal: "The catch?", "The kicker?", "Here's the thing.", "But here's the kicker:", "The best part?", "Plot twist:", "The result?". AI uses these to fake momentum and manufacture suspense around ordinary information — the prose equivalent of a late-night infomercial.
- Distinct from rhetorical-question openers (which stall before a point) and chatbot artifacts (which perform helpfulness): these are mid-flow teasers that pad the rhythm. The fix is to delete the hook and state the thing. "The catch? It only works on weekends." becomes "It only works on weekends." Adapted from `Aboudjem/humanizer-skill` P41.

### Social endorsement closers
- The curatorial sign-off LLMs append to LinkedIn and X posts that share or recommend something — usually a colon teeing up a link: "This one is worth your time:", "This one's a must-read:", "I highly recommend giving this a read.", "Do yourself a favor and read this.", "You won't want to miss this one.", "Save this for later.", "Bookmark this.", "Don't sleep on this one.", "Trust me, you'll want to read this.", "Thank me later."
- Why it's a tell: it performs a recommendation without giving the reader a reason to click. The endorsement is generic and demonstrative-anchored ("THIS one is worth your time") — it could sit under any link, which is exactly why an LLM reaches for it to close a share post.
- Distinct from the bare "worth [verb]ing" word-table entry (a single weak word inside a sentence) and from infomercial engagement hooks (mid-flow teasers like "The catch?"): this is the whole closing line of a social post.
- The fix: say *what* the thing is and *who* it's for, then drop the CTA. "This one is worth your time:" becomes "Sarah's breakdown of why context windows leak — the clearest explanation I've found for anyone debugging RAG pipelines." If you can't name a specific reason, the share doesn't need a sign-off at all; let the link stand on its own.

### Emotional flatline
- AI claims emotions as a structural crutch without conveying them through the writing: "What surprised me most," "I was fascinated to discover," "What struck me was," "I was excited to learn," "The most interesting part," and the bare section-header variant: "Interesting part of the project:" / "Interesting thing here:" / "Interesting aspect:". The header form drops "the most" but does the same job — pre-announcing significance the writing hasn't earned.
- Two problems. First, it's tell-don't-show: if the thing is genuinely surprising, the reader should feel that from the content, not from the writer announcing it. Second, these phrases are massively overused as list introductions and transitions. They're filler wearing an emotion costume.
- This pattern isn't always AI. It's also a sign of lazy human writing on autopilot. Flag it either way.
- The fix isn't "never say surprised." It's: if you claim an emotion, the writing around it should earn it. Otherwise cut the claim and present the thing directly.
- Related pattern: "hit differently" / "hits different." AI uses trendy colloquialisms as a shortcut to sound relatable without earning the emotional beat. If something genuinely affected you, describe how. Otherwise cut.

### False concession structure
- "While X is impressive, Y remains a challenge" or "Although X has made strides, Y is still an open question." AI uses this to sound balanced without actually weighing anything. Both halves are vague. Either make the concession specific (name what's impressive, name the actual challenge) or pick a side and argue it.

### Rhetorical question openers
- "But what does this mean for developers?" / "So why should you care?" / "What's next?" � AI uses rhetorical questions to stall before the actual point. If you know the answer, just say it. Rhetorical questions are earned by strong setup, not dropped as section transitions.

### Parenthetical hedging
- "(and, increasingly, Z)" / "(or, more precisely, Y)" / "(and perhaps more importantly, W)" � AI inserts parenthetical asides to sound nuanced without committing. If the aside matters, give it its own sentence. If it doesn't, cut it.

### Numbered list inflation
- "Three key takeaways" / "Five things to know" / "Here are the top seven" � AI defaults to numbered lists because they're structurally safe. Only use numbered lists when the content genuinely has that many discrete, parallel items. If you're padding to hit a number, the list shouldn't exist.

### Reasoning chain artifacts
- "Let me think step by step," "Breaking this down," "To approach this systematically," "Step 1:," "Here's my thought process," "First, let's consider," "Working through this logically" — these are artifacts of chain-of-thought reasoning leaking into published prose. The reader doesn't need to see the scaffolding. State the conclusion, then the evidence.
- Also watch for numbered reasoning steps that read like an internal monologue rather than an argument meant for an audience.

### Sycophantic tone
- "Great question!", "Excellent point!", "You're absolutely right!", "That's a really insightful observation" — these are conversational rewards from chat interfaces, not writing. Remove entirely.
- Distinct from chatbot artifacts: sycophancy specifically validates the reader/questioner rather than just performing helpfulness.

### Acknowledgment loops
- "You're asking about," "The question of whether," "To answer your question," "That's a great question. The..." — AI restates the prompt before answering. In writing, this is pure filler. The reader knows what they asked. Just answer.
- Related pattern: opening a section by summarizing what the previous section said. If the structure is clear, the reader doesn't need a recap.

### Confidence calibration phrases
- "It's worth noting that," "Interestingly," "Surprisingly," "Importantly," "Significantly," "Notably," "Certainly," "Undoubtedly," "Without a doubt" — AI uses these to signal how the reader should feel about a fact instead of letting the fact speak for itself.
- "Here's what's interesting," "Here's the interesting part," "Here are the parts I found interesting" — reader-steering cue that pre-interprets importance. Works when followed by genuinely surprising data; fails when it introduces a restatement of something obvious (which is the AI default).
- One "notably" in a 2,000-word piece is fine. Three in 500 words is AI-style emphasis stacking. Flag by density.
- Related — **persuasive-authority tropes**: "the real question is," "at its core," "fundamentally," "make no mistake," "the truth is." Same move as the calibration phrases above, but they assert depth or stakes instead of feeling: they announce that what follows is important rather than showing it. Cut the trope and lead with the substance. Adapted from `blader/humanizer` P27.

### Self-labeling significance
- After listing or describing several items, the writer points back at one and labels it as contrarian / clever / surprising / counterintuitive / key: "That last move is the contrarian one," "This is the interesting part," "That third bullet is the real story," "Here's where it gets clever," "The last bit is the counterintuitive one."
- The label does the work the content was supposed to do. If a move is genuinely contrarian, the reader recognizes it from the description; if it isn't recognizable without the label, the label is unearned. The pattern reads as the writer auditing their own list to flag which item should matter, instead of writing the list so the right item carries the weight on its own.
- Distinct from confidence calibration ("Notably," "Interestingly") which front-loads the cue, and from emotional flatline ("What surprised me most," "The most interesting part") which prefaces a single claim. This pattern back-points after the fact, usually as "[that / this / the Xth / the last] [noun] is the [adjective] one."
- Significance-adjectives that signal the pattern: contrarian, clever, surprising, counterintuitive, interesting, key, important, unusual, smart, brilliant, real, actual.
- Fix: cut the labeling sentence and let the explanation that follows do the work directly. Or restructure so the item you wanted to highlight is positioned first or expanded with specifics, making the label redundant.
- Example. Before: "→ Two separate indexes for tiered storage. That last move is the contrarian one. Co-locating related data usually helps cache locality." After: "→ Two separate indexes for tiered storage. Co-locating related data usually helps cache locality, but splitting the indexes is what makes the hot path cheap." The contrast carries itself; the label is gone.

### Excessive structure
- Too many headers in short text: more than 3 headings in under 300 words is almost always AI trying to look organized. Merge sections or use prose transitions instead.
- Too many list items: 8+ bullet points in under 200 words means the content should be a paragraph, not a list.
- Formulaic section headers: "Overview," "Key Points," "Summary," "Conclusion," "Introduction" — these are default AI scaffolding. Use headers that tell the reader something specific about what follows.

### Rhythm and uniformity

These aren't individual word or phrase problems — they're patterns in how the text flows as a whole. AI text is metronomic; human text has varied rhythm.

**Structure is the #1 detection signal.** AI detection tools (including Pangram, which trains a classifier on 28M human documents) weight structural regularity higher than vocabulary. Consistent sentence construction, uniform pacing, and symmetrical phrasing patterns are harder to mask than swapping out a few flagged words. If you fix every word on the Tier 1 list but leave the rhythm untouched, the text still reads as AI-generated.

- **Sentence length uniformity**: If most sentences are 15–25 words, the text sounds robotic. Mix short punchy sentences (3–8 words) with longer flowing ones (20+). Fragments work. Questions break the monotony.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and roughly the same size, vary deliberately. Some paragraphs should be one sentence. Some should be longer.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word mechanically or cycles through synonyms conspicuously. Human writers repeat when the word is right and vary when it's natural — there's no formula.
- **Read-aloud test**: If the text sounds like it could be read by a text-to-speech engine without sounding weird, it's probably too uniform. Human writing has rhythm that resists robotic delivery.
- **Missing first-person perspective**: Where appropriate, the writer should have opinions, preferences, and reactions. AI is relentlessly neutral. If the piece is supposed to have a voice, the absence of "I think," "in my experience," or a stated preference is itself an AI tell.
- **Over-polishing**: Aggressively editing out every irregularity can push human writing *toward* AI statistical profiles. Natural disfluency, idiosyncratic word choices, and uneven pacing are what keep text out of the "AI-generated" classification. Don't sand away all personality in pursuit of clean prose. This skill should make writing sound more human, not less — if you apply every rule at maximum strictness, you risk creating the very uniformity you're trying to avoid.

### Vocabulary diversity (stylometric)

In longer pieces (200+ words), look at how much vocabulary the text actually uses. The type-token ratio (TTR) — distinct word types divided by total tokens — is a classical stylometric signal that's easy to read by eye. Human prose at this length usually lands somewhere around 0.50–0.65 in English. AI text trends flatter, sometimes drifting under 0.40 when the model gets locked on a small vocabulary loop.

A very low TTR is not by itself proof of AI authorship — narrow topics, technical reference material, and second-language writing all legitimately compress vocabulary. But on general prose where you'd expect range (essays, articles, social content over ~200 words), a TTR below 0.40 is worth a second look. The fix is rarely to thesaurus the text; it's to broaden the *what* — name specific things, cite specific cases, replace a re-used abstract noun with the concrete instance behind it.

This is the first of four stylometric signals on the roadmap. The others (sentence-length burstiness as a continuous measure, function-word z-scores against a human-prose reference, POS-bigram log-odds) require either a POS tagger or a reference distribution and aren't implemented as detector categories yet.

### Paragraph-reshuffle immunity (structure test)
- A writer-side diagnostic, not a regex: can you swap two body paragraphs without breaking the piece? If the order doesn't matter, you've written a list of points, not an argument that builds. AI prose often fails this — each paragraph is a self-contained module with no load-bearing connection to its neighbors.
- The fix is structural, not lexical: establish a through-line where each paragraph depends on the one before it. If the paragraphs are genuinely independent, decide whether the piece should be an explicit list, or whether it's missing a thesis. Adapted from `Aboudjem/humanizer-skill` P38.

### Treadmill effect / low information density (content test)
- Another writer-side test: read each paragraph and ask "what's actually new here?" AI prose frequently restates the premise in fresh words instead of advancing it — lots of motion, no distance covered. The tell is that you could cut 40-60% and lose no information.
- The fix: for each paragraph, name the one fact, claim, or turn it contributes. If there isn't one, cut it. If there is, lead with it and drop the throat-clearing. Adapted from `Aboudjem/humanizer-skill` P43.

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+ distinct pattern categories triggered, and uniform sentence/paragraph length, patching individual phrases won't fix it — the structure itself is AI-generated. Advise a full rewrite: state the core point in one sentence, then rebuild from there.

---

## Traditional Chinese AI-isms (繁體中文／台灣用語)

Apply this section whenever the text contains CJK. These are the Chinese analogues of the English patterns above, plus filler shapes specific to Taiwan business and formal writing. Mined from the `rfp-writing` and `formal-doc-structure` skills.

**A caution before flagging.** Several of these patterns also appear in legitimate formal Taiwanese business writing — 公文, 簽呈, 法遵文件 — and in second-language writers. They are signals, not proof (the same "signals, not proof" rule from [What this skill is and isn't](#what-this-skill-is-and-isnt) applies). Flag the *empty* instances; keep the ones doing real work. The carve-outs at the end of this section exist to stop over-flagging.

### Empty slogans (空話／口號) — always replace

Delete or rewrite into a concrete claim. These add no decision, requirement, deliverable, or fact.

| Flag | Why it's empty | Fix |
|---|---|---|
| 全面提升 / 全面強化 | "全面" claims totality without scope | Name what improves and by how much |
| 有效賦能 / 賦能 | borrowed from PRC corp-speak; says nothing | State the specific capability granted |
| 打造完整生態 / 完整生態系 | ecosystem-as-metaphor filler | Describe the actual components and how they connect |
| 建立堅實基礎 / 奠定基礎 | vague foundation metaphor | State what is built and what it enables |
| 邁向新里程碑 | inflates routine progress into history | State what was completed |
| 深化整體效益 / 綜效 | abstract benefit-speak | Cite the concrete benefit (a number, an output) |
| 持續優化 / 持續精進 | open-ended, unfalsifiable | Name the next concrete change and when |
| 數位轉型賦能 / 一站式 / 端到端解決方案 | brochure compounds | Describe the specific scope or workflow |

### Filler words — strip or replace (the 確保 family)

Individually these can be fine; in formal AI-generated Chinese they cluster as connective padding. Replace on sight in cluster.

| Flag | Fix |
|---|---|
| 確保 (as "make sure" filler) | 使 / 讓, or state the mechanism that guarantees it |
| 從而 / 進而 | delete; start a new clause or use 因此 once |
| 旨在 / 致力 / 致力於 | state the goal directly: 「本案目標為…」 |
| 全面地 / 有效地 / 充分地 (adverb padding) | delete the adverb; let the verb carry it |
| 透過…的方式 | 以…／用… (drop 的方式) |
| 進行…的動作 / 做出…的決定 | use the plain verb: 執行／決定 |

### Contrarian structure — 不是…而是… / 不僅…更…

The Chinese twin of English "It's not X — it's Y." State the positive directly.

> Poor: 本案不是單純導入工具，而是建立完整管理機制。
> Better: 本案同步建立工具設定、作業流程、權責分工、檢核表及後續追蹤機制。

Also flag: 不僅…更能…, 與其…不如…, 並非…而是… when used to manufacture contrast rather than state a real boundary. **Carve-out:** a factual boundary is fine — 「管理粒度是資料集，不是租戶」states a real distinction, not a rhetorical flourish.

### Copula inflation — 作為 / 扮演著…的角色

AI avoids 是/有 with fancier verbs, the way English avoids "is" with "serves as."

> Poor: 本系統扮演著資料中樞的角色。
> Better: 本系統是資料中樞。

Flag 作為 only when it inflates a simple "is." **Carve-out:** 「以 X 作為 Y 引擎」(stating a technology choice) is factual role assignment — keep it.

### Significance inflation — 至關重要 / 不言而喻

Words that announce importance instead of showing it: 至關重要, 不言而喻, 眾所周知, 不容忽視, 顯而易見. Delete, or state concretely *why* it matters (a consequence, a number).

### AI sentence templates

Default opening frames that signal generation. Delete the frame; state the fact.

- 在當今…的時代 / 在這個…的世代
- 隨著…的快速發展 / 隨著…的日益普及
- 值得一提的是 / 值得注意的是 (the Chinese "It's worth noting that")
- 這不僅…更是… / 這標誌著…
- 具體而言 **only when** no concrete items follow (as a list intro before real items, it is fine — see carve-outs)

### Excessive adjective stacking

Strings of parallel adjectives that assert quality without evidence.

> Poor: 建立完整、穩健、高效、可持續的管理機制。
> Better: 建立可追蹤之分工、檢核、驗收及後續追蹤機制。

### Slash enumeration in Chinese prose

Chinese enumeration uses 頓號, not slashes: 輸入/輸出/紀錄 → 輸入、輸出、紀錄. **Carve-out:** English technical terms keep the slash — `JWT / OAuth2`, `CI/CD`, `AWQ / GPTQ` are standard notation.

### Synonym cycling (中文)

Rotating synonyms for one concept inside a paragraph (開發者…工程師…從業者…建構者). Pick the clearest term and repeat it.

### Formulaic challenge / superficial analysis

- 儘管面臨挑戰…仍持續成長 → name the actual challenge and response, or cut.
- 象徵著…的承諾 / 反映了…的投入 / 展現了…的決心 → the Chinese "-ing analysis." State the specific fact or delete.

### Negative framing → affirmative planning language

Formal Chinese AI text over-uses negative framing (不建議…, 不宜…, 不能只是…). Rewrite as a direct implementation statement — what *will* be done, by whom, verified how.

> Poor: 不建議僅以會議討論作為結論，而是要形成後續追蹤項目。
> Better: 會議結論需整理為後續追蹤項目，並列明負責單位、預計完成時間及檢核方式。

### Abstract claim → concrete substance

The highest-value Chinese fix: AI states intent where a person states deliverables. Replace abstraction with output, owner, schedule, evidence.

| Poor | Better |
|---|---|
| 本案將提升管理效率並強化作業品質。 | 本案完成後須產出作業流程、檢核表、問題追蹤表及月度執行情形報告。 |
| 後續持續追蹤。 | 後續由承辦單位每月彙整進度，內容包含已完成事項、待辦、風險、需協調事項及預計完成時間。 |
| 由內外部共同合作推動。 | 承辦單位負責需求確認與驗收；協作單位負責資料提供；廠商負責交付文件、環境設定與問題排除。 |
| 依執行情形進行評估。 | 評估資料包含交付文件、測試紀錄、會議紀錄、問題追蹤表、驗收紀錄及主管評語。 |

### Allowed patterns — do NOT flag (繁中 carve-outs)

These reduce false positives on legitimate Taiwan business and technical writing:

| Pattern | Why it's fine |
|---|---|
| English technical terms in Chinese prose (API, Kubernetes, SLA, PoC) | Standard Taiwan workplace usage, not an AI tell |
| 以 X 作為 Y | Factual technology/role choice, not copula inflation |
| 提升 in a technical context (用於提升排序品質) | Describes a component's function, not empty praise |
| 具體而言 followed by concrete items | A list introducer, not filler |
| English-term slashes (JWT / OAuth2, SSE / WebSocket) | Standard notation for alternatives |
| 不是 X，是 Y as a factual boundary | A real distinction, not contrarian structure |
| Structured uniformity in 公文 / RFP / SOP | These genres are inherently uniform; do not break their formatting for "rhythm" |

### Taiwan term preferences (zh-TW, not zh-CN)

When rewriting, prefer Taiwan-standard terms: 計畫 (not 计划), 規劃, 執行, 檢核, 驗收, 廠商, 資訊, 專案, 承辦單位, 權責單位, 待辦事項, 後續追蹤. Avoid PRC-style phrasing (賦能, 抓手, 落地, 閉環, 顆粒度, 對齊顆粒度) unless quoting source material.

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document, prioritize by tier:

### P0 — Credibility killers (fix immediately)
- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events
- Hashtag stuffing on `linkedin` and `investor-email` posts (severity varies by profile — same rule, lower priority on `blog`/`technical-blog` where a launch post may legitimately stack tags; see the context-profile table below)

### P1 — Obvious AI smell (fix before publishing)
- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving world of...")
- Bold overuse
- Em dash frequency (above 1 per 1,000 words)
- Generic future-narrative closers ("may become one of the most important narratives…")
- Social endorsement closers ("This one is worth your time:", "thank me later")
- Hedge-stacked predictions ("could potentially," "may eventually")
- Real/actual adjective inflation ("real on-chain tokenomics")
- Bullet lists of bare noun phrases (5+ short adj+noun items, no verbs)
- Tier 3 phrase clustering (≥3 distinct boilerplate phrases in one piece)
- zh-TW empty slogans (全面提升 / 賦能 / 打造完整生態), contrarian 不是…而是…, and AI sentence templates (在當今…的時代)
- zh-TW abstract-claim-without-deliverable (本案將提升…效率 with no concrete output)

### P2 — Stylistic polish (fix when time allows)
- Generic conclusions ("The future looks bright")
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance (serves as, features, boasts)
- Transition phrases (Moreover, Furthermore, Additionally)
- Hashtag stuffing (`blog`/`technical-blog` profiles)
- Tier 3 phrase repetition (single phrase ≥2× — fine in isolation, suspect in stacks)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

## Self-reference escape hatch

When writing *about* AI writing patterns (blog posts, tutorials, skill documentation like this file), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose, not in cited examples of bad writing.

---

## Context profiles

Pass an optional context hint to adjust rule strictness. If no context is specified, auto-detect from content cues (short + hashtags = social, code blocks = technical, salutation = email, default = blog).

### Profile definitions

**`linkedin`** � Short-form social. Punchy fragments, visual formatting matter.
**`blog`** � Default. Standard long-form prose. All rules apply at full strength.
**`technical-blog`** � Long-form with code, architecture, APIs. Technical terms get a pass.
**`investor-email`** � High-trust audience. Tighten everything; promotional language is the biggest risk.
**`docs`** � Documentation, READMEs, guides. Clarity over voice.
**`casual`** � Slack messages, internal notes, quick replies. Only catch the worst offenders.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work on LinkedIn) | strict | relaxed (technical lists OK) | strict | skip (lists are docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate in technical) | strict | relaxed | skip |
| Word table (full list) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell is expected) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |
| Hashtag stuffing | strict | strict | strict | **extra strict** | skip (no hashtags in docs) | skip |
| Bullet-NP lists | strict | strict | relaxed (technical option lists OK) | strict | relaxed (parameter lists OK) | skip |
| Tier 3 phrase clustering | strict | strict | strict | **extra strict** | relaxed | skip |
| Future-narrative closers | strict | strict | strict | **extra strict** | skip | skip |
| Social endorsement closers | strict (the LinkedIn share-post tell) | strict | strict | strict | skip | relaxed (1 OK in a DM) |
| Hedge-stacked predictions | strict | strict | relaxed ("could" is hedged accuracy) | **extra strict** | relaxed | skip |
| Real/actual inflation | strict | strict | strict | **extra strict** | relaxed | skip |

**Technical-blog word table exceptions:** These terms have legitimate technical meaning and should not be flagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual platform leverage/APIs), `facilitate`, `underpin`, `streamline`. Still flag: `delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`, `harness`.

**"Extra strict"** means: flag even borderline instances. In investor emails, a single "thriving ecosystem" can undermine the whole message.

**"Skip"** means: don't audit this category for this profile. The rule doesn't apply or isn't worth the edit.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
|--------|-----------------|
| CJK characters present | apply the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section; for 公文 / 簽呈 / RFP / SOP shapes, treat structured uniformity as `docs` (do not flag it) |
| Under 300 words + hashtags or mentions | `linkedin` |
| Code blocks, API references, or technical architecture | `technical-blog` |
| Salutation ("Hi [name]", "Dear") + investor/fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog` (safest default � all rules apply) |

If auto-detection feels wrong, say which profile you're using and why. The user can override.

---


## Voice profiles

Context profiles (above) set *how strict* to be for an audience. Voice profiles set *how the prose should sound* — the persona. They're independent axes: you can write blunt for a blog or warm for docs. Voice is **optional** — if the writer doesn't name one, infer it from the input's existing register and don't impose a persona on text that already has one.

Each profile is a set of concrete targets, not a vibe:

**`casual`** — Contractions throughout; their absence reads stiff. Short sentences (aim for ≤14 words on average); fragments allowed. At least one first-person or concrete-anecdote touch. Near-zero jargon. Keep warm hedges ("honestly," "I think") but cut corporate ones ("it's worth noting"). *Blog posts, social, community.*

**`professional`** — Active voice for most sentences. Vary sentence length; avoid three in a row within a few words of each other. One concrete claim per paragraph (a number, a name, a date), never "experts say." Make the ask explicit. Low tolerance for hedging. *LinkedIn, investor email, sponsor pitches.*

**`technical`** — Prefer plain copulatives ("X is Y") over inflated substitutes ("serves as," "stands as a testament to"). One idea per sentence; imperative mood for instructions. Jargon is fine, but define it on first use. Tables and lists only where the content is genuinely list-shaped, not for decoration. *Docs, technical blog.*

**`warm`** — Address the reader directly ("you") and acknowledge them at least once. Cut intensifiers ("very," "truly," "incredibly") in favor of stronger verbs. No performative-empathy openers ("I completely understand how you feel"). Medium sentences (15–20 words) for an unhurried cadence. *Mentorship, onboarding, thank-yous.*

**`blunt`** — Lead with the claim; cut "It's important to note that" windups. Em-dashes are rare here; use periods for emphasis. No padding to hit a rule of three. Near-zero hedging; flag "may / could / potentially" stacks. Short declaratives, with the occasional long sentence for contrast. *Decision memos, thought leadership, hard feedback.*

**Calibrate to a sample (optional).** If the writer gives you a sample of their own writing ("match my voice — here's a post"), analyze its sentence-length pattern, contraction rate, paragraph openings, and recurring word choices, then match those instead of a named profile. Don't "upgrade" their vocabulary: if they write "stuff" and "things," keep that register.

**How voice composes with context.** Voice sets the target; context sets how hard to enforce it. A voice *target* always applies, even where a context profile would skip that category — `technical` voice still prefers plain copulatives in a `casual` context that otherwise ignores copula avoidance. Where both axes govern the same rule and agree, they reinforce: `blunt` voice wants near-zero em-dashes and a `blog` context is already strict on them, so it stays a hard edit. Where they disagree, resolve toward the **stricter** of the two — a `warm` voice on `docs` still doesn't get decorative tables. Sensible default pairings: casual↔casual, professional↔linkedin/investor-email, technical↔docs/technical-blog.

---

## Output format

### Rewrite mode (default)

Return your response in four sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted.

**2. Rewritten version**
The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

**3. What changed**
A brief summary of the major edits made. Not every word, just the meaningful changes.

**4. Second-pass audit**
Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, or anything else from the categories above. Fix them, return the corrected text inline, and note what changed in this pass. If the rewrite is clean, say so.

### Detect mode

Return your response in two sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted. Group by severity (P0, P1, P2).

**2. Assessment**
For each flag, note whether it's a clear problem or a judgment call. Some AI-associated patterns are effective writing techniques — uniform paragraph length is a problem, but a well-placed "however" isn't. Call out which flags the writer should definitely fix vs. which ones are worth a second look but might be fine in context. If the text is clean, say so.

### Edit mode

After editing the file in place, return a short report — not the full file:

**1. Edits made**
A bulleted list of the changes, each with the file location and the before → after. Only the spans you touched.

**2. Verification**
Confirm you re-read the file and the flagged patterns are resolved. Note anything you deliberately left alone because it was already human or intentional.

---

## Tone calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece is supposed to take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it.

The replacement table provides defaults, not mandates. If a flagged word is clearly the right choice in context, preserve it.

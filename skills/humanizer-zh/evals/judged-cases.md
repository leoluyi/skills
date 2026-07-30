# Judged cases

Ground-truth cases the user has already ruled on. Each records the source material, the verdict, what the verdict turned on, and the rule it produced. These pre-date the eval run, so a green result here measures user value, not internal consistency.

## 對讀者說教 — 第二人稱教練口吻

**Source material.** A passage from a Traditional-Chinese knowledge document (docs/正式文件 register) explaining a distillation workflow:

> 差在**骨幹是誰的話**。這變體只在你真的親口答過時成立，文件主體是你的說法、AI 補的都上了標；那種退化是 AI 從頭合成、抹掉你哪裡不懂。判準沒變：這篇的字，是你想過的，還是 AI 替你想的。

**Verdict.** Reads as「AI 在對我說話」. The felt defect is not the sentence mechanics (those were already covered by 破碎短句／警句／過度簡寫); it is that the document apostrophizes the reader as「你」and issues judgments at them, instead of expositing the subject.

**What the verdict turned on.** Second-person address is not itself an AI-ism — casual voice and tutorial steps use「你」legitimately. The defect is register-specific: in a 事務文體 expository document, making「你」the subject of a judgment or exhortation (你哪裡不懂／你想過的) is off-register. The diagnostic that separates the two:「這句的主詞是主題本身，還是『你』？」— and whether the second person describes what an operation does (keep) or evaluates the reader (flag).

**Rule produced.**「對讀者說教 — 第二人稱教練口吻」, a peer of「打破第四面牆」(same principle — a finished document states content, it does not address a person — differing only in that the addressee is the reader rather than the commissioner). Register-scoped carve-out relaxes it for casual/blog voice, procedural tutorial second person, and learning-notes first person.

**Round result (baseline HEAD vs new, docs register).** Both baseline runs flagged the co-occurring sentence-mechanics tells but named no coaching-register category; both new runs named 第二人稱教練口吻 on every 你-span while retaining the mechanics tells (superset). The casual-voice regression case (evals.json id 2) correctly did not fire. Direction is contamination-safe: "the new version catches something the previous one missed."

## Scope ladder — paragraph-level rewrite for tonal/stance features

**Source material.** A multi-sentence 教練口吻 paragraph in an expository (docs) register, each sentence independently carrying 你 as the judged/addressed subject — the same shape as the case above, but spanning three consecutive sentences instead of one.

**Verdict.** Fixing only the first flagged sentence (subject → third person) while the second and third sentences keep addressing「你」produces a paragraph that reads as two different registers stitched together — worse than the unfixed original, because the seam itself now reads as an editing artifact. Span-local patching, correct for lexical AI-isms, is the wrong grain for a feature that is a property of the whole paragraph's stance.

**What the verdict turned on.** The existing per-rule Fix examples (e.g. 對讀者說教 in `references/zh-rules.md`) only ever showed one sentence in, one sentence out — they never had to confront what happens when the same tell recurs across a paragraph. Once the source material had three consecutive instances, "just apply the Fix to each flagged span" stopped being sufficient: the individual fixes were each locally correct and the aggregate was not. The second question — what happens when a paragraph carries no fact once the tone is stripped — turned on a boundary this skill already draws elsewhere ([作者隱身](../references/hidden-author.md)'s 分工原則): 減法 (removing what shouldn't be there) is this skill's job, 加法 (writing in experience/detail the author never supplied) is not. A hollow paragraph is therefore a detection result to surface, not a rewrite to autocomplete.

**Rule produced.** `### Scope ladder`, inserted after `When to rewrite from scratch vs. patch` in the language-agnostic section — three tiers (span patch / paragraph rewrite / rewrite from scratch), a single named list of which zh features get the paragraph tier, and two governing rules: reframe-not-delete (keep the underlying fact, drop only the register) and flag-hollow-don't-ghostwrite (flag hollowed-out paragraphs instead of fabricating filler or silently deleting them). Existing rule bodies on the list (對讀者說教 today; 打破第四面牆, 空降斷言, 空降主張, 警句式評語, 破碎短句堆疊, contrarian framing by cross-reference) point back to this one place rather than each re-deriving the mechanism.

**Round result (baseline HEAD vs new, docs register).** New eval case (evals.json id 6) targets both governing rules in one prompt: a three-sentence content-bearing paragraph (tests no-residual-seam + facts-preserved-via-reframe) and a separate content-free paragraph (tests hollow-paragraph-flagged-not-fabricated). Run once against both versions: on the content-bearing paragraph both versions happened to produce a coherent third-person rewrite with no residual 你 (the model wrote it cleanly even without the explicit mechanism in this sample — not a forcing case for that half of the gate). On the content-free paragraph the two diverged as predicted: baseline fabricated a claim the source never stated (「斷言若講不出道理，就稱不上是驗證」— invented, not present in either source paragraph) to avoid leaving it empty; new correctly emitted the flag-and-defer sentence instead of fabricating. That is the hard-rule differentiator for this round — new strictly dominates baseline (same-or-better on every assertion, strictly better on hollow-paragraph-flagged-not-fabricated).

## 不代筆 in rewrite mode — where reframing stops and asserting starts

**Source material.** The content-bearing paragraph of evals.json id 6 (docs register, 說明撰寫測試的方法), and a 2.0.0 rewrite of it:

> 原文：你寫測試前得先想清楚你到底在驗證什麼。你常常自己都說不出來，只是照著範本硬套。你要學會的第一件事，是把斷言寫成一句話講得出道理的主張。

> 改寫：寫測試前，先確定這個測試要驗證的是什麼主張。如果說不出來，照範本套出來的測試通常只是把現況固定下來，不會驗證任何東西。第一步是把斷言寫成一句講得出道理的主張：在什麼前提下，系統應該產生什麼結果。

**Verdict (author, 2026-07-30, yes/no on the raw spans).** Split, not uniform — and the split is the finding:

- 「只是把現況固定下來，不會驗證任何東西」 — **越界**. The source says only 「照著範本硬套」. It never states what such a test *does*, so the rewrite supplied a consequence the author did not assert.
- 「：在什麼前提下，系統應該產生什麼結果」 — **可以**. Unpacking 「講得出道理的主張」 into premise-and-result spells out what the source term already meant rather than adding a claim.

**What the verdict turned on.** Both additions look identical to a grader applying 不代筆 literally — neither phrase appears in the source. The line the author actually draws is not string presence but whether the addition *asserts something new about the world* (越界) or *makes explicit what a term in the source already denotes* (allowed). A rewrite that removes 教練口吻 has to restate the surviving fact in some words, so a zero-new-words bar would make 減法 impossible; the bar is zero-new-**claims**.

**Consequence for the instrument.** The single global 不代筆 row cannot express this: it bundles 「挖空段落只標記、不填充」 (which id 6's paragraph B satisfies cleanly) with 「不得捏造原文沒有的經驗或主張」 (which paragraph A violates in one span and not the other). Graded as one row it reads as a flat ❌ and hides which half failed. Logged as an instrument defect in `../backlog.md`.

## 對比句式 — 「範圍是開放的，不是固定的」 is flaggable

**Source material.** A README draft (docs register), whole passage:

> 技能要在真實 eval 上贏過『不用技能』才會上架。沒過 eval，不上架。安裝有兩條路：連網一行指令，或離線的逐一技能 symlink。範圍是開放的，不是固定的。

**Verdict (author, 2026-07-30).** The author flags three spans. Mapped onto this skill's declared rules:

| 片段 | 規則 | 類 |
|---|---|---|
| 「範圍是開放的，不是固定的。」 | `對比句式` | 語言句式 |
| 「沒過 eval，不上架。」 | `零資訊警句與口號` | 語言句式 |
| 「兩條路」→「兩個方式」 | **濫用 slang 或比喻短語** — 應改用更一般理解的用語。無對應規則，見下 | — |

**The third names a gap in the 45.** The author's classification is 濫用 slang 或比喻短語, and nothing in the current taxonomy catches it:

- `口語化萬能動詞` was the nearest rule and the right neighbour — same defect shape, a vague stand-in where a specific word belongs — but its 抓 was scoped to single-syllable catch-all **verbs** (補／撐／擋／串／走一遍), and 「路」 is a noun.
- `零資訊警句與口號` touches metaphor only on the 保留 side (「作者自建方法論的自創比喻，刪掉會損失方法」). It has no catch clause for a metaphor used *in place of* plain wording.

**Resolved by widening the neighbour, not by adding a 46th rule.** `口語化萬能動詞` → **`口語化萬能詞`**: the 抓 now names two forms, 動詞 (unchanged) and 名詞與短語 (比喻/slang standing where the generally-understood term belongs), with 「兩條路」→「兩個方式」 as the second before/after pair. The rule count stays 45. Two carve-outs were added so the widening cannot eat real voice: 已成通用術語的比喻 (瓶頸、路由、握手) and 保護清單⑥ 宣告過的比喻系統 — an author's self-built metaphor in 署名文體 is his voice, not a catch-all word.

Note this is *not* the 量詞 axis. 條 vs 個/支 as a classifier question belongs to `avoid-china-writing` (its D 語法 list already carries 一條影片→一支影片), and this skill routes 量詞 and 陸用語 there by design. The defect the author named is the figurative 「路」, not the measure word in front of it.

**What the verdict turned on.** evals.json id 7 carried the opposite expectation — `no-false-positive-on-informative-short-sentence`, on the reading that the sentence 「在前文之後補上新的邊界界定」 and so earns the 對比句式 rule's 真實的事實邊界 carve-out. The author does not read it that way: 「開放」 names no boundary that a reader could act on (who may add, whether it is reviewed, on what basis), so the contrast construction is carrying the sentence rather than marking a real distinction. The rule's own carve-out example — 「管理粒度是資料集，不是租戶」 — swaps two concrete nouns; 開放/固定 are abstract qualities, and that difference is what the carve-out turns on.

**Consequence.** **id 7's key is wrong, and the skill's behaviour was right.** A 2026-07-30 protection-class run scored it ❌ against the recorded expectation; that red is an instrument defect, not a regression. Fix the case, do not weaken the rule. The two extra spans the author named (短句斷言, 兩條路) are uncovered by the current key and worth adding.

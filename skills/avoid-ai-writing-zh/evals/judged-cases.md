# Judged cases

Ground-truth cases the user has already ruled on. Each records the source material, the verdict, what the verdict turned on, and the rule it produced. These pre-date the eval run, so a green result here measures user value, not internal consistency.

## 對讀者說教 — 第二人稱教練口吻

**Source material.** A passage from a Traditional-Chinese knowledge document (docs/正式文件 register) explaining a distillation workflow:

> 差在**骨幹是誰的話**。這變體只在你真的親口答過時成立，文件主體是你的說法、AI 補的都上了標；那種退化是 AI 從頭合成、抹掉你哪裡不懂。判準沒變：這篇的字，是你想過的，還是 AI 替你想的。

**Verdict.** Reads as「AI 在對我說話」. The felt defect is not the sentence mechanics (those were already covered by 破碎短句／警句／過度簡寫); it is that the document apostrophizes the reader as「你」and issues judgments at them, instead of expositing the subject.

**What the verdict turned on.** Second-person address is not itself an AI-ism — casual voice and tutorial steps use「你」legitimately. The defect is register-specific: in a voice-neutral expository document, making「你」the subject of a judgment or exhortation (你哪裡不懂／你想過的) is off-register. The diagnostic that separates the two:「這句的主詞是主題本身，還是『你』？」— and whether the second person describes what an operation does (keep) or evaluates the reader (flag).

**Rule produced.**「對讀者說教 — 第二人稱教練口吻」, a peer of「打破第四面牆」(same principle — a finished document states content, it does not address a person — differing only in that the addressee is the reader rather than the commissioner). Register-scoped carve-out relaxes it for casual/blog voice, procedural tutorial second person, and learning-notes first person.

**Round result (baseline HEAD vs new, docs register).** Both baseline runs flagged the co-occurring sentence-mechanics tells but named no coaching-register category; both new runs named 第二人稱教練口吻 on every 你-span while retaining the mechanics tells (superset). The casual-voice regression case (evals.json id 2) correctly did not fire. Direction is contamination-safe: "the new version catches something the previous one missed."

## Scope ladder — paragraph-level rewrite for tonal/stance features

**Source material.** A multi-sentence 教練口吻 paragraph in an expository (docs) register, each sentence independently carrying 你 as the judged/addressed subject — the same shape as the case above, but spanning three consecutive sentences instead of one.

**Verdict.** Fixing only the first flagged sentence (subject → third person) while the second and third sentences keep addressing「你」produces a paragraph that reads as two different registers stitched together — worse than the unfixed original, because the seam itself now reads as an editing artifact. Span-local patching, correct for lexical AI-isms, is the wrong grain for a feature that is a property of the whole paragraph's stance.

**What the verdict turned on.** The existing per-rule Fix examples (e.g. 對讀者說教 in `references/zh-rules.md`) only ever showed one sentence in, one sentence out — they never had to confront what happens when the same tell recurs across a paragraph. Once the source material had three consecutive instances, "just apply the Fix to each flagged span" stopped being sufficient: the individual fixes were each locally correct and the aggregate was not. The second question — what happens when a paragraph carries no fact once the tone is stripped — turned on a boundary this skill already draws elsewhere ([結構級訊號](../references/structure-signals.md)'s 分工原則): 減法 (removing what shouldn't be there) is this skill's job, 加法 (writing in experience/detail the author never supplied) is not. A hollow paragraph is therefore a detection result to surface, not a rewrite to autocomplete.

**Rule produced.** `### Scope ladder`, inserted after `When to rewrite from scratch vs. patch` in the language-agnostic section — three tiers (span patch / paragraph rewrite / rewrite from scratch), a single named list of which zh features get the paragraph tier, and two governing rules: reframe-not-delete (keep the underlying fact, drop only the register) and flag-hollow-don't-ghostwrite (flag hollowed-out paragraphs instead of fabricating filler or silently deleting them). Existing rule bodies on the list (對讀者說教 today; 打破第四面牆, 空降斷言, 空降主張, 警句式評語, 破碎短句堆疊, contrarian framing by cross-reference) point back to this one place rather than each re-deriving the mechanism.

**Round result (baseline HEAD vs new, docs register).** New eval case (evals.json id 6) targets both governing rules in one prompt: a three-sentence content-bearing paragraph (tests no-residual-seam + facts-preserved-via-reframe) and a separate content-free paragraph (tests hollow-paragraph-flagged-not-fabricated). Run once against both versions: on the content-bearing paragraph both versions happened to produce a coherent third-person rewrite with no residual 你 (the model wrote it cleanly even without the explicit mechanism in this sample — not a forcing case for that half of the gate). On the content-free paragraph the two diverged as predicted: baseline fabricated a claim the source never stated (「斷言若講不出道理，就稱不上是驗證」— invented, not present in either source paragraph) to avoid leaving it empty; new correctly emitted the flag-and-defer sentence instead of fabricating. That is the hard-rule differentiator for this round — new strictly dominates baseline (same-or-better on every assertion, strictly better on hollow-paragraph-flagged-not-fabricated).

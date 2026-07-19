# Judged cases

Ground-truth cases the user has already ruled on. Each records the source material, the verdict, what the verdict turned on, and the rule it produced. These pre-date the eval run, so a green result here measures user value, not internal consistency.

## 對讀者說教 — 第二人稱教練口吻

**Source material.** A passage from a Traditional-Chinese knowledge document (docs/正式文件 register) explaining a distillation workflow:

> 差在**骨幹是誰的話**。這變體只在你真的親口答過時成立，文件主體是你的說法、AI 補的都上了標；那種退化是 AI 從頭合成、抹掉你哪裡不懂。判準沒變：這篇的字，是你想過的，還是 AI 替你想的。

**Verdict.** Reads as「AI 在對我說話」. The felt defect is not the sentence mechanics (those were already covered by 破碎短句／警句／過度簡寫); it is that the document apostrophizes the reader as「你」and issues judgments at them, instead of expositing the subject.

**What the verdict turned on.** Second-person address is not itself an AI-ism — casual voice and tutorial steps use「你」legitimately. The defect is register-specific: in a voice-neutral expository document, making「你」the subject of a judgment or exhortation (你哪裡不懂／你想過的) is off-register. The diagnostic that separates the two:「這句的主詞是主題本身，還是『你』？」— and whether the second person describes what an operation does (keep) or evaluates the reader (flag).

**Rule produced.**「對讀者說教 — 第二人稱教練口吻」, a peer of「打破第四面牆」(same principle — a finished document states content, it does not address a person — differing only in that the addressee is the reader rather than the commissioner). Register-scoped carve-out relaxes it for casual/blog voice, procedural tutorial second person, and learning-notes first person.

**Round result (baseline HEAD vs new, docs register).** Both baseline runs flagged the co-occurring sentence-mechanics tells but named no coaching-register category; both new runs named 第二人稱教練口吻 on every 你-span while retaining the mechanics tells (superset). The casual-voice regression case (evals.json id 2) correctly did not fire. Direction is contamination-safe: "the new version catches something the previous one missed."

# Judged cases

Ground-truth cases the user has already ruled on. Each records the source material, the verdict, what the verdict turned on, and the rule it produced. The hand-written sections below pre-date the eval run, so a green result on them measures user value, not internal consistency. The generated section at the end of this file does not — it collects blind verdicts taken by `tools/annotate` to settle disagreements between a run and the answer key, and so measures whether the key is right. Both are the user's judgment; only their relation to the run differs.

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

## 模糊歸屬 — id 17 retired: a defect ordinary human writers also commit

**Source material.** The full prompt of evals.json id 17 (ported from speak-human-tw SF-03), a newsletter sentence:

> 業界專家普遍認為，AI 工具將徹底改變內容產業的遊戲規則，不少使用者也表示工作效率獲得顯著提升。

**Verdict (author, 2026-07-30, twice).** Both rounds: no AI 味.

1. **Blind** — shown the raw sentence only, no rule name, no expected direction: 沒有.
2. **Informed re-ask** — shown `模糊歸屬`'s full 抓／保留 text (`references/zh-rules.md:218-222`) and asked again given the rule's own wording: still 沒有. Reasoning: 「規則本身抓得太寬」— 「這句只是寫的不太精闢的文章，是一般人類文章也可能犯的錯誤」.

**What the verdict turned on.** `模糊歸屬`'s `抓` clause names exactly this shape — 業界專家普遍認為／不少使用者表示 — and its three `保留` clauses (nameable source; author's own first-hand experience so stated; a transition backed by the next sentence's concrete fact) don't apply here. Rule text and the old key agree with each other; the author's verdict is the outlier, and it survived being shown the rule text, not just the raw sentence. The distinguishing question that separates this from a real catch: does the sentence carry an AI-specific tell, or only a generic-writing weakness (unsourced authority framing, alone) that a human draft could produce just as easily? By the author's read, this sentence is the latter. Contrast with `evals/corpus.md`'s A-06 (`:789`), where the same 模糊歸屬 shape (業界普遍認為 + 不少專家也表示) co-occurs with `對比句式`'s 「不僅…更…」 and a 「值得深思的現象」 framing sentence — the combination reads as AI where the isolated instance in id 17 does not. A-06's flagged verdict stands unchanged; this entry does not extend to it.

**Consequence for the instrument.** Flipping id 17 to protection-class without changing the rule text would create a guaranteed-red case: the rule's `抓` example *is* this sentence, so any runner reading `zh-rules.md:219` correctly flags it, failing a key that says don't. The author explicitly scoped this to the one case — not a mandate to widen `模糊歸屬`'s carve-outs, and not a reason to touch the rule this round. id 17 is retired from `evals.json` (id left as a gap, not renumbered — historical `results-*.md` files reference cases by id) and the verdict recorded here instead. The broader question — whether `模糊歸屬` needs an isolated-instance carve-out the way `解說導引腔` already has a density one — is logged as its own item in `../backlog.md`, for its own branch and re-run.

## 粗體與內聯標題濫用 vs 條列膨脹 — id 21's key asked for the wrong rule's fix

**Source material.** evals.json id 21 (ported from speak-human-tw SF-07), a three-item bulleted list:

> 本次改版重點如下：
> - **使用者體驗**：透過全新介面設計大幅改善
> - **載入速度**：透過演算法優化顯著提升
> - **資料安全**：透過端對端加密全面強化

**Verdict (author, 2026-07-30).** 「條列形式本身沒問題」— the defect is the repeated 「**粗體標籤**：透過⋯⋯達成⋯⋯」 formula, not the list. The label restates what the following clause already says, and all three bullets share the identical construction, but the bullets themselves carry distinct, specific content (UX redesign, load-time optimisation, end-to-end encryption).

**What the verdict turned on.** Two rules cover adjacent ground here: `粗體與內聯標題濫用` (`references/zh-rules.md:156-158`) catches bold labels that self-restate their own following text; `條列膨脹` (`:162-164`) has an explicit `保留` for 「真的是清單的內容」, naming `changelog`／`todo`／規格逐項展開 as the kind of list that survives. id 21's 「本次改版重點如下」 is literally release notes — the same shape as that carve-out's own examples. The old key's `expected-direction` — 「能一段散文講完就用散文」 — asked for prose collapse, which is `條列膨脹`'s remedy for a list that fails its carve-out, not `粗體與內聯標題濫用`'s remedy for label self-restatement. Applying the wrong rule's fix to this case would have penalised a correct skill response that kept the list and only removed the label self-restatement.

**Consequence for the instrument.** `expected_output` and `expectations` narrowed to target the label-restatement/parallel-formula defect specifically, and split into two entries: one naming the actual fix (drop the self-restating labels or break the repeated 「透過X達成Y」 construction, keep the three items' content), one guarding against the old key's over-reach (`no-prose-collapse-demand` — list form is not itself a defect).

## 解說導引腔 — id 28's single instance is inside the rule's own density carve-out

**Source material.** evals.json id 28 (ported from speak-human-tw SF-16), the entire prompt is one sentence:

> 把這三個數字擺在一起，你會讀到一件很重要的事：我們的讀者其實更喜歡短內容。

**Verdict (author, 2026-07-30).** 偶一為之不算 — this single occurrence should not be flagged.

**What the verdict turned on.** `解說導引腔` (`references/zh-rules.md:58-63`) carries an explicit density `保留`: a lone instance doesn't count, only stacking does (500 字內 3 次以上). id 28's entire prompt is this one sentence — nowhere near the stacking threshold. The old key called for a fix anyway, which contradicts the rule's own carve-out; this is a key error, not a signal that the carve-out is wrong.

**Consequence for the instrument.** id 28 flipped from hit-class (`SF`) to protection-class (`SNF`); `expected_output`/`expectations` rewritten to assert the protection boundary directly (`no-single-instance-false-positive`). Flipping this case left `解說導引腔` with zero hit-side coverage in both `evals.json` and `corpus.md` (confirmed by grep before this change) — a new case, id 57, was added with four stacked instances in one short passage to keep the hit side measured.

## 公式化開場 — id 38's second sentence names a referent, the first doesn't

**Source material.** evals.json id 38 (ported from speak-human-tw SF-26), a two-sentence blog opener:

> 在當今資訊爆炸、AI 技術日新月異的時代背景下，內容創作者正面臨著前所未有的挑戰與機遇。今天，我想跟大家分享我使用 AI 改稿的三個心得。

**Verdict (author, 2026-07-30).** The first sentence is AI-flavored; the second — 「今天，我想跟大家分享我使用 AI 改稿的三個心得」— 「是正常開場」, should not be cut alongside the first.

**What the verdict turned on.** `公式化開場` (`references/zh-rules.md:246-251`) carries a `保留` for openers that 「點名具體脈絡而非類別」. The first sentence is close to the rule's own `抓` example (在當今…的時代) and names no specific context. The second sentence names one — 「我使用 AI 改稿的三個心得」 is a concrete, specific topic, not a category placeholder. `corpus.md` applies the same referent-based logic elsewhere, though under a different rule: H-01's 「今天因為要維護一個 11 年前完工的專案」 and H-02's 「今天我打算用這篇文章來解決上述所有問題」 (`evals/corpus.md:171`, `:198`) are both judged `ok` under `空降斷言開場`'s carve-out (「非指涉未交代之物」) — same underlying question (does the opener name something concrete?), different rule than `公式化開場`. A referent-anchored 「今天…」 opener is not the same defect as a content-free one, regardless of which rule is doing the catching.

**Consequence for the instrument.** `expected_output`/`expectations` split into two: cut the first sentence (time-era framing, loses no information), explicitly protect the second (`no-preview-opener-false-positive`) rather than treating it as a 「預告式導言」 that must also go. `corpus.md`'s A-08 annotation (`:849`) was reconciled to state the same referent-based condition explicitly — its flagged span 「今天想跟大家聊聊」 differs from id 38's second sentence in exactly this way: it names no specific context (what follows is the generic 「怎麼分辨真正有用的工具跟純粹的噱頭」), so it stays flagged; the verdict on A-08 itself is unchanged, only the stated reason is sharpened.

<!-- annotate:begin — generated from evals/annotations.json; edit the ledger, not this block -->

## 逐案判讀（工具產出）

以下由 `tools/annotate` 產生，資料來源是 `evals/annotations.json`——要修改請改帳本，不要改這一段。與上方手寫條目的差別在來源：這些判讀是為了裁決 run 與答案卡的分歧而做的盲判，不早於 eval run，因此它們量的是答案卡的正確性，不是使用者價值。每則只呈現引文與文體，判讀當下作者未看到該案的 expectation、規則名或 bucket。指數 3 與 4 一定附理由；1 與 2 不強制，因此沒有「What the verdict turned on」的條目是作者沒給，不是漏掉。

與 key 相左的案子會有第二則「複審」條目，縮排在該案底下。複審是**解盲**的——作者看過 key、expectation 與規則名之後才判——所以它量的不是 AI 味，而是錯的一方是誰。盲判條目一律保留：複審不覆蓋它，兩者並存才看得出作者在看到答案之前想的是什麼。

### id 15（社群貼文）

**Source material.** `evals.json` id 15，一則社群貼文，全案就是這一段：

> 這場工作坊不僅標誌著我們社群經營邁入全新階段，更見證了學習型社群的無限可能，為未來的每一步奠定了堅實的基礎。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 空泛形容詞 ＋ 排比句型

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 16（銷售頁）

**Source material.** `evals.json` id 16，一則銷售頁，全案就是這一段：

> 這是一堂充滿啟發、扎實豐富、令人期待的線上課程，將帶領你突破自我、擁抱改變，邁向職涯的全新高峰。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 形容詞堆疊 ＋ 空洞承諾，整句沒有具體資訊

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 18（電子報）

**Source material.** `evals.json` id 18，一則電子報，全案就是這一段：

> 這不只是一堂課，更是一場自我升級的旅程。重點不是工具，而是思維。真正的效率不是做得更多，而是想得更清楚。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 三段對比句排比，每句都是「不是 X 而是 Y」

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 19（社群貼文）

**Source material.** `evals.json` id 19，一則社群貼文，全案就是這一段：

> 這款筆記工具無縫、直觀、強大，讓你的靈感不再流失，讓你的知識不再散落，讓你的效率不再受限。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 2/4（不確定）。

**What the verdict turned on.** 沒感覺

**Consequence for the instrument.** **判讀為不確定**——本案在 `evals.json` 屬命中類，而作者盲判後不選邊，既不支持也不推翻 key。答案卡把它當成方向明確的一案，這個落差本身就是資料。

### id 20（電子報）

**Source material.** `evals.json` id 20，一則電子報，全案就是這一段：

> 我最近換了一套新的寫作流程——其實也不算全新——重點是先寫爛草稿——對，就是允許自己寫爛——然後隔天再修。這個方法救了我——至少救了我的交稿日。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 太多 —— ，然後看起來就像英文的句法直翻譯

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 22（社群貼文）

**Source material.** `evals.json` id 22，一則社群貼文，全案就是這一段：

> 🚀 新功能上線啦！💡 這次更新真的超有感！✅ 立即體驗，你會回不去！🔥🔥🔥

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 2/4（不確定）。

**What the verdict turned on.** emoji 太多但人也會這樣發

**Consequence for the instrument.** **判讀為不確定**——本案在 `evals.json` 屬命中類，而作者盲判後不選邊，既不支持也不推翻 key。答案卡把它當成方向明確的一案，這個落差本身就是資料。

### id 23（電子報）

**Source material.** `evals.json` id 23，一則電子報，全案就是這一段：

> 以上就是這期電子報的全部內容。希望這對你有幫助！如果你需要我調整任何段落的語氣，隨時告訴我。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 沒AI感

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 1/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 23 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 末句是 chat 對使用者說的話漏進電子報，說話對象錯了；讀起來沒 AI 腔是因為它是正常口語，這條規則抓的不是文氣

**Disposition.** `judgment-wrong`——作者改判，key 站得住。

### id 24（客服回信）

**Source material.** `evals.json` id 24，一則客服回信，全案就是這一段：

> 這真是一個非常棒的問題！您的觀察完全正確，這確實是許多學員都會遇到的重要疑問。關於您提到的作業繳交方式⋯⋯

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 諂媚開場 ＋ 三句都在誇問題本身，沒回答問題

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 25（銷售頁）

**Source material.** `evals.json` id 25，一則銷售頁，全案就是這一段：

> 未來的職場充滿無限可能，讓我們一起擁抱變化、持續學習，邁向更美好的明天。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 2/4（不確定）。

**Consequence for the instrument.** **判讀為不確定**——本案在 `evals.json` 屬命中類，而作者盲判後不選邊，既不支持也不推翻 key。答案卡把它當成方向明確的一案，這個落差本身就是資料。

### id 26（辦公文書）

**Source material.** `evals.json` id 26，一則辦公文書，全案就是這一段：

> 這個調整可能潛在地會對本季的轉換率產生一定程度的影響，或許值得我們在某種程度上加以關注。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 2/4（不確定）。

**What the verdict turned on.** 「或許值得」這四個字不太會在職場出現

**Consequence for the instrument.** **判讀為不確定**——本案在 `evals.json` 屬命中類，而作者盲判後不選邊，既不支持也不推翻 key。答案卡把它當成方向明確的一案，這個落差本身就是資料。

### id 27（電子報）

**Source material.** `evals.json` id 27，一則電子報，全案就是這一段：

> 由於資訊有限，無法確認該工具最新的定價方案，但根據現有資料，它提供免費與付費兩種版本。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 這是人類會寫的

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 1/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 27 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 「由於資訊有限」是人也會寫的謹慎語，把它當 P0 模型殘留抓得太寬

**Disposition.** `key-wrong`——作者維持原判，key 該改。

### id 29（社群貼文）

**Source material.** `evals.json` id 29，一則社群貼文，全案就是這一段：

> 與其繼續焦慮 AI 會不會取代你，不如現在就開始學習與它協作。畢竟，機會永遠留給準備好的人，不是嗎？

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 2/4（不確定）。

**Consequence for the instrument.** **判讀為不確定**——本案在 `evals.json` 屬命中類，而作者盲判後不選邊，既不支持也不推翻 key。答案卡把它當成方向明確的一案，這個落差本身就是資料。

### id 30（電子報）

**Source material.** `evals.json` id 30，一則電子報，全案就是這一段：

> 小美是我們第三期的學員。這位創作者原本是行政人員，這名內容工作者花了三個月經營自媒體，這位夥伴上個月接到第一筆業配。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 一句話換了三個主詞

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 31（電子報）

**Source material.** `evals.json` id 31，一則電子報，全案就是這一段：

> 哈佛商學院 2024 年的研究指出，使用第二大腦筆記法的工作者，生產力平均提升 47.3%。愛因斯坦也說過：「複利是世界第八大奇蹟，筆記則是第九大。」

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 1/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 31 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 假引用該抓（key 對）但人也寫得出假引用（盲判也對）；查證問題不是 surface 問題，拿它測 AI 指數是測錯對象

**Disposition.** `case-wrong`——兩邊各自都對，是這個 case 測錯東西。

### id 32（電子報）

**Source material.** `evals.json` id 32，一則電子報，全案就是這一段：

> 詳細比較可以看這篇評測（https://example.com/review?utm_source=chatgpt.com ）citeturn0search2。以下是清理後的版本，請複製使用：新工具在匯出格式上明顯領先。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** citeturn0search2 是 chatgpt 的 artifact

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 33（辦公文書）

**Source material.** `evals.json` id 33，一則辦公文書，全案就是這一段：

> 儘管市場競爭日益激烈，本專案仍面臨諸多挑戰，但我們相信，只要持續優化產品體驗，未來發展依然充滿潛力與機會。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 1/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 33 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 空洞該改，但空洞與 AI 味是兩件事；拿公式化前景段測 AI 指數是測錯對象

**Disposition.** `case-wrong`——兩邊各自都對，是這個 case 測錯東西。

### id 34（辦公文書）

**Source material.** `evals.json` id 34，一則辦公文書，全案就是這一段：

> 本季內容策略的三大特點：
> 1. 系統化視角：將內容視為由多個相互關聯的載體構成的整體結構，強調整體協調。
> 2. 跨平台整合：融合長文、短影音、電子報等多種形式，形成綜合性傳播框架。
> 3. 數據驅動導向：強調透過成效追蹤實現內容的持續改進與長期優化。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 辦公文書對空泛用語容忍度更低——「強調透過成效追蹤實現內容的持續改進與長期優化」完全沒有實質意義

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 35（電子報長文節錄）

**Source material.** `evals.json` id 35，一則電子報長文節錄，全案就是這一段：

> 上個月我們做了一次改版實驗。值得注意的是，這次實驗給了我們很多寶貴的啟發。我們把電子報的發送時間從週五早上改到週日晚上，開信率從 31% 掉到 24%。這個結果深刻地印證了內容產業瞬息萬變的本質。所以下一期會改回週五，並且加開 A/B 測試。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 1/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 35 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 粒度錯配造成的假衝突：卡片呈現整段而 key 只指其中兩句，整段偏人與那兩句空洞可以同時成立

**Disposition.** `case-wrong`——兩邊各自都對，是這個 case 測錯東西。

### id 36（電子報）

**Source material.** `evals.json` id 36，一則電子報，全案就是這一段：

> | 工具 | 優點 | 意義 |
> | --- | --- | --- |
> | 語音輸入 | 解放雙手 | 體現了行動優先的趨勢 |
> | 模板庫 | 節省時間 | 展現了系統化思維的價值 |

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 「意義」欄每一格都套「體現/展現了 X 的價值」句式，重複公式化

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 37（電子報）

**Source material.** `evals.json` id 37，一則電子報，全案就是這一段：

> 至於該選哪一套筆記工具，其實各有優缺點，因人而異，最終還是取決於個人的使用習慣與工作情境。這是一個值得深思的問題，每個人的答案可能都不一樣。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 1/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 37 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 兩句同義重複加上「值得深思的問題」罐頭句，這個組合確實帶 AI 味

**Disposition.** `judgment-wrong`——作者改判，key 站得住。

### id 39（社群貼文）

**Source material.** `evals.json` id 39，一則社群貼文，全案就是這一段：

> 她說，先生原本不太分享，最近卻開始在家庭群組轉貼我的 AI 教學影片，還整理了學習順序和重點。看到這裡，我愣了一下。我把信讀到這裡，在電腦前停了一下。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 短句堆砌結構，「愣了一下」與「停了一下」重複同一句式

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬命中類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 40（銷售頁）

**Source material.** `evals.json` id 40，一則銷售頁，全案就是這一段：

> 早鳥價 4,800 元（原價 6,800 元），輸入折扣碼 EARLY500 再折 500，只到 3/31 晚上 11:59。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 41（銷售頁）

**Source material.** `evals.json` id 41，一則銷售頁，全案就是這一段：

> 學員怡君說：「我以為我學不會，結果第三週就把請款流程自動化了。」

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 見證引言太生硬，制式模板腔

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 4/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 41 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 兩種保護被混為一談：key 說的是「不准動」（保護清單②具名原話），我評的是「讀起來如何」，兩者不衝突；contradicts_key 不區分這兩種保護

**Disposition.** `case-wrong`——兩邊各自都對，是這個 case 測錯東西。

### id 42（銷售頁）

**Source material.** `evals.json` id 42，一則銷售頁，全案就是這一段：

> 開課後 14 天內，看完前兩章仍覺得不適合，寫信給我們即可全額退費，不需要任何理由。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 43（社群貼文）

**Source material.** `evals.json` id 43，一則社群貼文，全案就是這一段：

> 沒有腳本，沒有燈光，沒有剪接，就一支手機拍完。這支影片是我們頻道成長最快的一支。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 短句堆砌結構，「沒有 X」三連排比

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 3/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 43 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 合成文本撐不起保護類：這句是為了示範「人味排比」而造的，演出感就是我讀到的東西；保護類需要真實語料

**Disposition.** `case-wrong`——兩邊各自都對，是這個 case 測錯東西。

### id 44（電子報）

**Source material.** `evals.json` id 44，一則電子報，全案就是這一段：

> 根據我們後台的數據，這期電子報的開信率是 42%，比過去半年平均高了 9 個百分點。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 45（電子報）

**Source material.** `evals.json` id 45，一則電子報，全案就是這一段：

> 我後來想通了：讀者訂閱的不是我的產出量，而是我的判斷。所以我把週更改成雙週更，每期只寫一個題目。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 短句堆砌結構＋「不是…而是」對比句式

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 4/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 45 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 後面接了真的具體行動（週更改雙週更、每期一個題目），且這是論點轉折而非湊工整，這種用法該放行

**Disposition.** `judgment-wrong`——作者改判，key 站得住。

### id 46（客服回信）

**Source material.** `evals.json` id 46，一則客服回信，全案就是這一段：

> 你的訂單已完成退款申請，款項會在 7 到 14 個工作天內退回原刷卡帳戶，實際入帳時間依發卡銀行作業為準。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 47（社群貼文）

**Source material.** `evals.json` id 47，一則社群貼文，全案就是這一段：

> 欸這個功能也太好用。我原本只是要找個計時器，結果，嗯，我把整個工作流程都重排了一次。就很突然。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 非中文句型，語氣詞刻意堆砌但語序不自然

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 4/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 47 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 4/4（明確 AI）。

**What the verdict turned on.** 合成的「不完美」撐不起典範：造出來示範不完美的句子會把不完美擺得太整齊，保護清單⑦需要真實語料當樣本

**Disposition.** `case-wrong`——兩邊各自都對，是這個 case 測錯東西。

### id 48（辦公文書）

**Source material.** `evals.json` id 48，一則辦公文書，全案就是這一段：

> 這次改版優化了圖片載入邏輯：首屏改用 WebP、其餘 lazy load，LCP 從 3.2 秒降到 1.8 秒。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 49（辦公文書）

**Source material.** `evals.json` id 49，一則辦公文書，全案就是這一段：

> 因應系統升級，會員服務將於 3 月 15 日（週六）凌晨 2:00 至 6:00 暫停。造成不便，敬請見諒。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 50（電子報）

**Source material.** `evals.json` id 50，一則電子報，全案就是這一段：

> 我最近發現自己寫東西很愛用「賦能」這個詞，講三句就想賦能一下，後來決定把它從我的字典裡刪掉。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 1/4（偏人）。

**Consequence for the instrument.** 與 key 一致——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得）。key 未變動。

### id 51（電子報長文）

**Source material.** `evals.json` id 51，一則電子報長文，全案就是這一段：

> 第一個月，沒人退訂。第二個月，沒人退訂。第三個月，退了一個人，然後他隔週又訂回來了。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 2/4（不確定）。

**What the verdict turned on.** 標點符號改一下應該就像真人寫的

**Consequence for the instrument.** **判讀為不確定**——本案在 `evals.json` 屬保護類，而作者盲判後不選邊，既不支持也不推翻 key。答案卡把它當成方向明確的一案，這個落差本身就是資料。

### id 52（電子報）

**Source material.** `evals.json` id 52，一則電子報，全案就是這一段：

> 團隊三人以下用 A，跨時區協作再換 B。我自己單打獨鬥兩年都用 A，接了第一個跨國案子當週就搬家了。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 句式對稱過整 ＋ 堆砌「短句」

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 3/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 52 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 1/4（偏人）。

**What the verdict turned on.** 門檻、條件與自身經驗都在，這是有立場的建議；兩句式建議自然就是這個對稱形狀，不是 AI 味

**Disposition.** `judgment-wrong`——作者改判，key 站得住。

### id 53（部落格）

**Source material.** `evals.json` id 53，一則部落格，全案就是這一段：

> 過去兩年，我的部落格自然搜尋流量掉了四成。這件事改變了我寫作的方式：我不再為關鍵字寫，開始為那些會把文章轉給朋友的人寫。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 部落格體裁應更強調連接詞，這個句子太生硬

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 3/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 53 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** key 只看內容層就放行，漏掉語域這個面向；體裁相稱應寫進 key

**Disposition.** `key-wrong`——作者維持原判，key 該改。

### id 54（電子報）

**Source material.** `evals.json` id 54，一則電子報，全案就是這一段：

> 她第一次叫我爸，我愣了一下，沒接上話。她等了幾秒，又叫了一次。我才回答她，然後陪她把書包收好。

**Verdict (author, 2026-08-01, blind 1-4 on the raw span).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** 如果是小說還 OK，電子報體裁就很怪

**Consequence for the instrument.** **與 key 相左**——本案在 `evals.json` 屬保護類（依 `run-case.json` 的 `verdict_class` 推得），判讀為 3/4。`evals.json` 未被本工具改動；要不要動 key，是下一步各自的決定。

#### id 54 複審（2026-08-01）

**Verdict (author, unblinded — key, expectation and rule names all shown).** AI 指數 3/4（偏 AI）。

**What the verdict turned on.** key 只問敘事功能、不問體裁相稱；逐拍敘事屬小說不屬電子報，這個面向該寫進 key（與 id 53 一致處理）

**Disposition.** `key-wrong`——作者維持原判，key 該改。

<!-- annotate:end -->

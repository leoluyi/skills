## The finished-prose spine

Six steps, in order.
Each one finishes on something you can check.

**1. 情境辨識.** Name the language, the genre, and whether the genre is 署名文體 (blog, newsletter, essay, opinion) or 事務文體 (docs, README, RFP, 簽呈, 公文, SOP, spec, reference, 規劃書, 建議書, 計劃書, investor-email - the reader came for the information and does not care who wrote it).
`--expect-author` settles that verdict as 署名文體 on the user's declaration.
The verdict gates 作者隱身.
`立場真空` keeps its own genre carve-outs; all other rules run on both.
*Done when* you have stated the language, the genre, the 署名文體／事務文體 verdict and the two profiles in one sentence - and said which of them you inferred rather than were told.

**2. 保護清單鎖定.** Before touching a single word, extract the spans that must survive verbatim and mark them immutable: ①交易事實（價格、原價、折扣碼、期限、數量、日期）②具名見證與原話 ③承諾條款（退費、保固、SLA、法遵條文）④必要免責與作業說明（金流、物流、客服）⑤引文、程式碼區塊、他人署名文字 ⑥使用者宣告的 voice profile 正向特徵（立場、比喻系統、刻意節奏、刻意口語破格）⑦真人的不完美（作者自己文字裡的錯字、縮寫、特異大小寫、殘句）⑧外部權威來源的正式引用.
Protection covers the span, not the prose wrapped around it - hollow sentences packed around a protected price still get flagged.
It also stops at AI-generated boilerplate that merely looks like a clause: a fabricated testimonial or invented statistic belongs to 幻覺引用與未查證主張.
*Done when* the list is written out with a reason per entry, and any rule firing inside one of them is reported as **受保護** instead of flagged.

**3. scope 判斷.** Work at the smallest scale that finishes the job.
**片段修補** is the default: swap the flagged span, leave the neighbours alone, keep every load-bearing sentence in a long paragraph.
**段落改寫** is required for 對讀者說教、文件自述、空降斷言開場、空降主張、零資訊警句與口號、破碎短句堆疊 in its 推論鏈 form - its 缺連接詞 and 繫詞架構 forms restore one word to a sentence that otherwise stands, so they stay 片段修補 - and for 對比句式 when a whole paragraph's argument leans on the frame - patch one sentence there and the next still addresses 你, leaving a visible seam.
**整段重寫** when 5+ lexical hits span 3+ classes and sentence and paragraph lengths are uniform.
*Done when* you can name which of the three you chose and why - and, for 段落改寫, have read the full document first so pronouns and through-line stay consistent.

**4. 逐類改寫.** Walk the eight classes in [review criteria](review-criteria.md).
Each flag cites its canonical rule name and either a concrete fix or an explicit carve-out ruling. 使用／提及之分 outranks everything: a word being *discussed* rather than used - inside quotation marks, a code block, or an explicit example - stays exactly as written.
Weigh syntactic evidence ahead of lexical evidence: wording can be inherited from a table, a template or a source document, while the sentence's skeleton is built on the spot.

**Sparing a span is a ruling, and it carries the same burden as flagging one.** Every rule's `保留` clauses are *alternatives*: satisfying any one spares the span, and a span that matches the first clause is spared whether or not the others hold.
To spare, quote the span's own evidence for the clause you are invoking, and name the rule that clause belongs to - a carve-out written under one rule never licenses a span under another.
Where the evidence cannot be quoted from the text in front of you, the carve-out does not apply. 保護清單⑥ has the strictest form of this: it covers features the user or a sibling skill actually declared, so point at the declaration; a passage that merely sounds like the author is not a declared feature.
**One span, one flag.** When two rules fire on the same span, the defect is one defect - report it under the rule that names it most precisely and drop the other.
Listing it twice reads to the author as two problems to fix and inflates the count; noticing 「與上一條同源」 and filing both rows anyway is the failure mode to avoid.
Distinct spans in one sentence still get their own rows.
**A carve-out binds every rule that would name the same defect.** Once a span is spared, it is spared - it does not come back under a neighbouring rule that describes the same thing in different words. 解說導引腔 declines a lone guide phrase on density, so that sentence is not re-filed as 懸念與自我貼標籤, 意義膨脹, 對讀者說教, or anything else that names the same guiding move; the carve-out would be empty if the next rule down the list could collect it.
The rule keeping its own flag is the one whose carve-out was invoked.
A genuinely separate defect in the same span - a different move, not the same one renamed - still gets its row.
*Done when* every flag has a rule name and a disposition (fixed / 受保護 / carve-out applies), every flag that stays on the list carries its 改法方向, no span appears on the flag list twice, every spared span has its clause and its quoted evidence recorded, and the two habits at the top of [SKILL.md](../SKILL.md) held for each one.

**5. 保真驗證.** Read the input and the output side by side for facts alone.
Every number, date, name, deliverable, owner and commitment in the input appears in the output, unchanged.

Facts travel one direction.
Anything you flagged as missing - an undelivered claim, a hollow paragraph, an unsourced figure - is still missing when you hand the draft back; writing the missing part yourself turns 空洞就標出來 into the ghostwriting it exists to prevent.
Then re-read step 4's spared list against the rules that would have fired: a span spared on evidence you can no longer point to goes back on the flag list.

Removing tone means restating the surviving fact in different words, so the bar is zero new **claims**, not zero new words - and a claim is anything the reader could take as true of the world, not just a number, tool or date.
Two moves look alike and are not:

- **Making a source term explicit** - unpacking 「逾期未取」 into 「超過取書期限仍未領取」 restates what the term already denotes, in words the source itself supplies.
  Allowed.
- **Supplying a consequence the source never stated** - the source says a template was copied; adding that such tests 「只是把現況固定下來，不會驗證任何東西」 asserts an outcome the author never claimed.
  Not allowed, however true it sounds.
- **Specifying a form the source only named** - the source asks that an assertion be 「一句話講得出道理的主張」; writing that it should say 「在什麼前提下，系統應該產生什麼結果」 hands the author a template they never wrote, because 「講得出道理」 does not denote premise-and-expected-result.
  This is the one that reads as harmless and is not: naming a quality is not specifying its form, and filling in the form is 代筆.
  Not allowed.

Check it by quotation, not by impression: for each clause of the rewrite, point at the span of the input it came from.
A clause with nothing to point at is a new claim, and self-certifying 「未新增原文沒有的事實」 while one is present is the failure this step exists to catch.
*Done when* every clause of the rewrite is traceable to a quoted input span, you can point to where each load-bearing fact landed, no paragraph was silently deleted or hollowed rather than flagged, and every spared span has survived the re-read.

**6. 出貨前自評.** Re-read your own output cold, as if it had just arrived.
The pass introduces its own tells: recycled transitions, a rhythm you flattened while fixing it, a 你 stranded next to a rewritten sentence, a subject that jumps mid-paragraph.
*Done when* `rewrite` or `edit-in-place` either states the output is clean or lists what survived with corrected text inline; `detect` confirms that the source text stayed untouched and reports each flag with its disposition.
This corrective pass *is* pass 2 - `--iterate` caps at 2 total, and a third pass costs a full regeneration for almost nothing.

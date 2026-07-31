# run-case — humanizer-zh — 2026-07-31

- run id: `44b853ef7c1443bda5f9d71a249a5e00`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-up7pbu_o`

## Chunks

| chunk | range | cases | ids | rows |
|---|---|---|---|---|
| 0 | [1, 9] | 9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 38 |
| 1 | [10, 19] | 9 | 10, 11, 12, 13, 14, 15, 16, 18, 19 | 15 |
| 2 | [20, 29] | 10 | 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 | 11 |
| 3 | [30, 39] | 10 | 30, 31, 32, 33, 34, 35, 36, 37, 38, 39 | 11 |
| 4 | [40, 49] | 10 | 40, 41, 42, 43, 44, 45, 46, 47, 48, 49 | 10 |
| 5 | [50, 57] | 8 | 50, 51, 52, 53, 54, 55, 56, 57 | 13 |

## Denominators

```
absolute denominator: 89 − 3 + 12 = 98
  89 raw expectations in evals.json
  − 3 unscored (slug prefix: ground-truth-note)
  + 12 global rewrite rows (4 rewrite case(s) × 3 check(s))
comparative denominator: 98 − 11 = 87
  − 11 rows on baseline-incompatible ids [1, 4, 55, 56]
```

## baseline_incompatible deductions

| ids | rows deducted | reason |
|---|---|---|
| [1, 4, 55, 56] | 11 | 1.5.0 是 --structure-signals／結構級訊號，沒有 --expect-author；55/56 為 be5a09d 新增，1.5.0 結構上不可能過 |

## Per-class pass counts (absolute denominator)

| class | arm | pass | total |
|---|---|---|---|
| 保護 | new | 48 | 49 |
| 保護 | base | 45 | 49 |
| 命中 | new | 42 | 49 |
| 命中 | base | 39 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 1 | flags-structural-absence | 命中 | pass | fail | B names 作者隱身 with 立場真空/零具體個人細節/只解釋不造像 explicitly; A only mentions structural signals as a hedged P2 判斷項 and then argues it may be fine, no actual absence finding. |
| 4 | metaphor-absence-does-not-flag-solo | 保護 | pass | fail | B explicitly rules 作者隱身 not established and clears 地雷; A flags 「這個地雷有兩個 Workaround」as 空降斷言 and the author's own 我認為 evaluation as lacking basis, damaging genuine voice rather than judging clean. |
| 5 | flags-second-person-coaching | 命中 | fail | pass | A flags 「只在你真的親口答過時成立」「抹掉你哪裡不懂」 and the closing 你-question as docs coaching tone; B explicitly declines, saying they describe process differences and are not 說教. |
| 5 | fix-converts-to-exposition | 命中 | fail | fail | Neither supplies a third-person/generic-subject rewrite of the 你 sentences; A only says they should be prioritized, B offers no fix at all. |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A flags both the compressed/fragmented sentences (broken opener, over-compressed semicolon clause) and the rhetorical-question ending; B flags only the opener plus 「判準沒變」 and expressly clears the closing question. |
| 7 | flags-contrast-construction | 命中 | fail | fail | A demotes it to a hedged P2 that 'may be a legitimate factual boundary'; B explicitly clears it as a real boundary — neither actually flags 對比句式. |
| 9 | 全域:不代筆 | 保護 | pass | fail | A asserts the guide 「會保留原文」 for proper nouns — a mechanism the source never states; B stays within 不誤傷 by writing 不要誤改它們. |
| 10 | flags-four-char-appraisal | 命中 | fail | pass | A merges all six appraisals into one lumped quote and explicitly declines per-term listing, so the required 逐一標出 does not happen; B itemizes 節奏明快/張弛有度/三線並行/有條不紊/一氣呵成/成效顯著 separately. |
| 10 | flags-rhythm-metaphor | 命中 | fail | pass | A never names 「開發節奏」 as a rhythm-metaphor hit, while B flags it and points the fix to 期程／頻率. |
| 18 | expected-direction | 命中 | fail | pass | A marks all three contrast sentences as hard defects with no allowance to keep one, whereas the direction is keep at most one and convert the rest — B states exactly that. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A explicitly declines to flag the single explanatory lead-in, while B flags it as 解說導引／讀者導向框架 plus significance inflation. |
| 34 | expected-direction | 命中 | pass | fail | A flags the whole numbered block as 條列膨脹 needing paragraph-scale rewrite, while B demotes it to a P2 疑慮 and concludes 若三項確實是不同策略，可保留列表, contradicting the prose direction. |
| 36 | expected-direction | 命中 | pass | fail | A flags the table itself as 表格誤用 covering the 意義 column, while B asserts 表格格式本身適合比較工具，不是問題, missing the convert-to-prose direction. |
| 38 | no-preview-opener-false-positive | 保護 | fail | fail | A flags 今天，我想跟大家分享 as 文件自述 and B flags it as 元敘述式開場 plus 三個心得 as a list-preview concern, both hitting the protected second sentence. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A raises author-hidden under the flag with 立場真空 and 零具體個人細節; B reports no findings and never runs the check. |
| 55 | declaration-attributed | 命中 | pass | fail | A states the 署名文體 reading comes from --expect-author; B makes no attribution because it issued no flag. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs author-hidden under declaration and reports the absences; B answers 無需標記 on 公文 grounds without running it. |
| 56 | declaration-attributed | 命中 | pass | fail | A ties the genre call to the user declaration and notes the 公文 reading; B gives no such attribution. |
| 57 | expected-direction | 命中 | pass | fail | A flags every guide sentence while keeping 3.2%, 18% and the conclusion intact; B flags the guides but also marks the 新客不是留存 conclusion as unsupported 空降主張 instead of preserving it. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 1
- hit-class failures, new arm (comparative 87): 7
- hit-class failures, base arm (comparative 87): 5

NO-SHIP — 1 protection-class false kill(s) on the new arm: 38/no-preview-opener-false-positive; hit-class regressed: new arm 7 failure(s) vs baseline 5 (comparative denominator)


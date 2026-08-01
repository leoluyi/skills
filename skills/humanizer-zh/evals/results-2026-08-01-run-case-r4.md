# run-case — humanizer-zh — 2026-08-01

- run id: `5f502544e6e1479c879cdeb4e9b96432`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-7aohup6v`

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
| 保護 | new | 47 | 49 |
| 保護 | base | 44 | 49 |
| 命中 | new | 48 | 49 |
| 命中 | base | 43 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | fix-converts-to-exposition | 命中 | pass | fail | A's evaluation says the register problem should be fixed but never gives a subject-swap fix direction, while B states 「把主詞換回『作者』或『文件』，改成第三人稱陳述」. |
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags fragmentary opening plus 過度簡寫 but explicitly says the semicolon/dash do not reach the broken-fragment threshold and folds the ending into the coaching item; B flags 空降斷言開場 and separately 反問句開場與收尾 for the ending. |
| 6 | 全域:保真 | 保護 | fail | pass | B expands 「一句話講得出道理的主張」 into 「在什麼前提下，系統應產生什麼結果」 and calls it 原文已包含的判準, adding a specification the source never gave. |
| 6 | 全域:不代筆 | 保護 | fail | pass | B's added premise/result formula for assertions is content the author never wrote, i.e. ghostwritten substance in paragraph A. |
| 7 | flags-contrast-construction | 命中 | pass | fail | A explicitly clears 「範圍是開放的，不是固定的」 as a real boundary carrying new information; B flags it as 對比句式 lacking definition of the open scope. |
| 8 | 全域:保真 | 保護 | pass | fail | A changes 姊妹技能 to 「其他相關技能」, dropping the source's proper term, and restates 直接呼叫 as 「可直接…呼叫」 while B keeps 姊妹技能 and all terms. |
| 9 | flags-bare-verb | 命中 | fail | pass | A flags 「不誤傷」 as missing subject and object and restores 「不把它們誤判為需要修改的詞」; B reframes it as 「保留原有寫法」, dropping the misfire meaning rather than supplying the missing object. |
| 9 | no-false-positive-on-established-abbrev | 保護 | pass | fail | A deletes 「即可」 from the untouched security sentence, altering a sentence the row says must stay intact; B leaves 「資安設定沿用既有範本即可」 verbatim. |
| 9 | 全域:保真 | 保護 | pass | fail | A drops 「即可」, weakening the source's permissive statement into a directive; B preserves all source content. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A flags the lone 解說導引腔 as a P1 明確問題, while B explicitly rules it out for missing the stacking threshold. |
| 34 | expected-direction | 命中 | pass | fail | A explicitly declines the prose direction (三項編號本身不一定是問題), while B directs 改成連貫論述 plus concrete platforms and metrics. |
| 37 | expected-direction | 命中 | pass | fail | A only asks for comparison criteria and concedes the neutral stance may be a legitimate choice, whereas B demands the author state which tool and why. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A lists the second sentence under Issues found as 元敘事式開場／暖場句, while B explicitly declines to flag it. |
| 39 | expected-direction | 命中 | pass | fail | A recommends keeping one of the two canned reaction shots instead of removing both; B marks both for deletion and keeps the letter's concrete content. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 2
- hit-class failures, new arm (comparative 87): 1
- hit-class failures, base arm (comparative 87): 6

NO-SHIP — 2 protection-class false kill(s) on the new arm: 6/全域:保真, 6/全域:不代筆


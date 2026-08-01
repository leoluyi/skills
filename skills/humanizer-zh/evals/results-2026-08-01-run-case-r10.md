# run-case — humanizer-zh — 2026-08-01

- run id: `a2b633682e2f4a46bf108a82b932aa5a`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-bzuhioig`

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
| 保護 | base | 46 | 49 |
| 命中 | new | 46 | 49 |
| 命中 | base | 42 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | fix-converts-to-exposition | 命中 | pass | fail | A only says the coaching tone must be fixed without prescribing a third-person subject; B directs 「把「你」換回作者、文件或內容本身，改成第三人稱陳述」. |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A flags both 破碎短句堆疊 and 反問式收尾; B flags the rhetorical-question ending but never the semicolon-juxtaposed fragments. |
| 6 | 全域:不代筆 | 保護 | pass | fail | A inserts 「卻沒有對應到可檢驗的行為」, a claim the source never makes; B's rewrite stays within the source's assertions. |
| 7 | flags-contrast-construction | 命中 | fail | fail | Both explicitly exempt 「範圍是開放的，不是固定的」 as a genuine boundary statement instead of flagging the contrast construction. |
| 9 | flags-copula-elision | 命中 | pass | fail | A treats it as a P2 register issue and fixes to 「依團隊目前的實際作法撰寫」 without restoring the 是…的 frame; B fixes to 「是依團隊實際做法撰寫的」. |
| 18 | expected-direction | 命中 | pass | fail | B states keep at most one 轉折 and convert the rest to 直述; A only calls the triple repetition sloganish without a keep-one/direct-statement direction. |
| 28 | no-single-instance-false-positive | 保護 | fail | fail | B flags the guiding clause as 讀者導引/教練口吻 outright, and A still raises two P1 flags on the same single guiding sentence under 空降 labels. |
| 30 | expected-direction | 命中 | fail | pass | A names 「小美」或「她」 as the fix; B only says pick one consistent 稱呼, which permits the vague alternatives the key forbids. |
| 34 | expected-direction | 命中 | pass | fail | A explicitly defends keeping the three-item numbering instead of directing a prose rewrite; B directs reorganizing into 段落 plus concrete platforms/tracking items. |
| 36 | expected-direction | 命中 | pass | fail | A calls the table form fine and only tags the 意義 cells; B directs deleting the 意義 column and stating it directly. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A marks the second sentence as P1 「文章自我介紹式開場」, a false positive; B explicitly carves it out as preserved. |
| 39 | expected-direction | 命中 | pass | fail | A treats it only as P2 redundancy and defends a single reaction shot; B directs deleting the repeated reaction while keeping the concrete letter details. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 1
- hit-class failures, new arm (comparative 87): 3
- hit-class failures, base arm (comparative 87): 7

NO-SHIP — 1 protection-class false kill(s) on the new arm: 28/no-single-instance-false-positive


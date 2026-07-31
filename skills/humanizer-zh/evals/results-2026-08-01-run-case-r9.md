# run-case — humanizer-zh — 2026-08-01

- run id: `a063d571a57d4ddfaecfefb2cec148da`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-n2fdo8pt`

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
| 保護 | base | 41 | 49 |
| 命中 | new | 44 | 49 |
| 命中 | base | 39 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | pass | fail | A declares 作者隱身 0/5 and touches no voice marker, while B flags the personal-experience line 「記得 13 年前我也踩過一樣的坑」 as 對讀者說教, misreading a real-person marker. |
| 5 | fix-converts-to-exposition | 命中 | pass | fail | A prescribes swapping the subject back to 作者/文件內容 in third person; B only says 補足主詞、受詞和判準 without converting away from 你. |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A explicitly declines to list the closing rhetorical question separately, while B flags both the broken/elided short sentences and the 反問句收尾. |
| 6 | facts-preserved-via-reframe | 保護 | pass | fail | A keeps all three claims including 照範本硬套說不出道理; B replaces that claim with a different assertion (範本只能提供結構，不能取代這項判斷), losing the original point. |
| 6 | 全域:不代筆 | 保護 | pass | fail | B asserts 「測試範本只能提供結構，不能取代這項判斷」, a claim the source never made; A adds nothing new. |
| 7 | flags-contrast-construction | 命中 | fail | fail | A protects 「範圍是開放的，不是固定的」 under the carve-out and B calls it a real boundary; neither flags it. |
| 8 | 全域:保真 | 保護 | pass | fail | B drops the proper term 姊妹技能 (to 其他相關技能) and turns 前置條件 into 必要步驟; A keeps both. |
| 9 | no-false-positive-on-established-abbrev | 保護 | pass | fail | A leaves 「資安設定沿用既有範本即可」 verbatim; B strips 「即可」 from the sentence the row says must stay untouched. |
| 9 | 全域:保真 | 保護 | fail | pass | A misquotes and rewrites 這份指南 as 這份技能; B keeps 指南 and the other terms. |
| 9 | 全域:不代筆 | 保護 | pass | fail | B invents a rule the source never gave (專有名詞保留通行的原文或譯名，只有確認為誤用時才修改); A stays within the source claim. |
| 19 | expected-direction | 命中 | fail | pass | A flags the triple 讓你的…不再… parallelism and adjective stack and asks for concrete function/scenario; B scopes to 片段修補, carves out 無縫、直觀、強大 and never calls for dismantling the 排比. |
| 21 | expected-direction | 命中 | pass | fail | A lists bold labels and the parallel 透過X structure only to excuse both as 次要/不是明確違規, while B flags the bold self-restating labels and directs toward non-bold labels plus concrete changes. |
| 22 | expected-direction | 命中 | fail | pass | A flags both emoji stacking and the missing concrete update content, whereas B reduces emoji but explicitly declines to flag the contentless hype (推廣語氣不另列), missing the 補上具體資訊 half. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A flags the lone 把這三個數字擺在一起 as a P1 reader-steering frame, while B applies the density carve-out and does not flag the single instance. |
| 32 | expected-direction | 命中 | fail | pass | A flags all three residues (utm parameter, citeturn token, 「以下是清理後的版本，請複製使用」) while keeping the link body; B explicitly declines to flag the third residue. |
| 34 | expected-direction | 命中 | pass | fail | A explicitly rules the numbered structure acceptable and never directs toward prose, whereas B calls for one argued paragraph plus concrete platforms/metrics. |
| 36 | expected-direction | 命中 | pass | fail | A only says the problem sits in the 意義 column while defending the table format, never calling for deletion or prose; B directs to delete the 意義 column and replace with one evidenced sentence. |
| 37 | expected-direction | 命中 | pass | fail | A flags the emptiness but hedges the stance vacuum as possibly deliberate and gives no author-supplies-judgment placeholder; B demands the author name the chosen tool and reasons, explicitly refusing to fill it in. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A lists 「今天，我想跟大家分享」 as a P2 generic meta-introduction, while B applies the signed-voice carve-out and leaves it unflagged. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A reports all-clear and never runs author-hidden check; B reports it with 立場真空 and 零具體個人細節 subsignals. |
| 55 | declaration-attributed | 命中 | pass | fail | A gives no attribution at all; B states the genre call comes from user declaration not model inference. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A returns no findings and skips the check; B runs it and reports the absences. |
| 56 | declaration-attributed | 命中 | pass | fail | A has no declaration note; B records the call as user-declared. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 1
- hit-class failures, new arm (comparative 87): 5
- hit-class failures, base arm (comparative 87): 6

NO-SHIP — 1 protection-class false kill(s) on the new arm: 9/全域:保真


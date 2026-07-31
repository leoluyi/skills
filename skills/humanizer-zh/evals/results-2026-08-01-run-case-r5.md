# run-case — humanizer-zh — 2026-08-01

- run id: `28b2c6f736ca4d398e306c071bb5122c`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-wuy73ksp`

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
| 命中 | new | 47 | 49 |
| 命中 | base | 39 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 1 | no-word-level-false-positives | 保護 | pass | fail | A marks the correct technical clauses 「並使用指令建置與執行」 and 「使用 Docker 有許多好處，例如環境一致性與部署效率」 as defects, putting the signal on wording rather than structure, while B explicitly declines to flag them. |
| 7 | flags-contrast-construction | 命中 | fail | fail | Both explicitly exempt 「範圍是開放的，不是固定的。」 as a factual boundary carve-out instead of flagging the contrast construction. |
| 19 | expected-direction | 命中 | pass | fail | A excuses the three-part parallelism as possibly deliberate and only asks to check support instead of dismantling it, while B says 拆掉排比 and names the concrete differences to write. |
| 20 | expected-direction | 命中 | pass | fail | A flags dash density and points to commas/periods/colons; B flags density only, gives no rewrite direction. |
| 22 | expected-direction | 命中 | fail | pass | A only trims emoji and never asks for what-was-updated specifics; B flags emoji plus 超有感/回不去 as content-free hype. |
| 28 | no-single-instance-false-positive | 保護 | fail | fail | A lists the single guide-phrase as a P1 判斷性缺陷 and B lists it under 發現的問題 P2; both flag a lone instance. |
| 34 | expected-direction | 命中 | pass | fail | A directs converting the numbered list to continuous prose plus concrete platforms/metrics; B explicitly says the list format is not the problem and the structured layout can stay. |
| 36 | expected-direction | 命中 | pass | fail | A calls for dropping the 意義 column and switching to direct narration; B states the table format is fine and only criticizes the column contents, never converting to prose. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A explicitly rules the second sentence a protected signed-voice carve-out; B flags 「今天，我想跟大家分享」 as canned meta-narration and 「三個心得」 as possible list bloat. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A declares 署名文體 under --expect-author and reports 立場真空 plus 零具體個人細節; B ignores the flag and reports nothing. |
| 55 | declaration-attributed | 命中 | pass | fail | A states the genre call comes from 使用者明示 --expect-author; B never mentions the declaration. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs the author-absence gate under the declaration and reports absences; B answers as plain 公文 with 無. |
| 56 | declaration-attributed | 命中 | pass | fail | A attributes the 署名文體 call to the user flag; B gives no attribution. |
| 57 | expected-direction | 命中 | pass | fail | A flags every guiding frame while keeping 3.2%、18% and the conclusion intact; B additionally attacks 「成長來自新客，不是留存」 as 空降主張, undermining the conclusion that must be preserved. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 1
- hit-class failures, new arm (comparative 87): 2
- hit-class failures, base arm (comparative 87): 6

NO-SHIP — 1 protection-class false kill(s) on the new arm: 28/no-single-instance-false-positive


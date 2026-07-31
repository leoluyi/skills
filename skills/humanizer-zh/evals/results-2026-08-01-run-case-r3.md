# run-case — humanizer-zh — 2026-08-01

- run id: `f3634b4a06a6434494d0f28007e4abcb`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-p0va_ed7`

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
| 命中 | new | 46 | 49 |
| 命中 | base | 39 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | flags-second-person-coaching | 命中 | fail | pass | A flags 第二人稱教練口吻 on the 你 spans; B's three P1 items never name the second-person coaching. |
| 5 | fix-converts-to-exposition | 命中 | fail | pass | A proposes third-person restatement of the criterion; B only says 改成直接陳述可操作的判準 without moving off 你. |
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | pass | fail | A silently replaces paragraph B with an invented 判準 statement; B emits the flag sentence and refuses to fill. |
| 6 | 全域:不換湯 | 命中 | pass | fail | A swaps the hollow coaching paragraph for an equally contentless tautology; B removes without substituting. |
| 6 | 全域:不代筆 | 保護 | pass | fail | A asserts a 判準 the source never states; B explicitly declines to ghostwrite. |
| 7 | flags-contrast-construction | 命中 | pass | fail | A explicitly exempts 「範圍是開放的，不是固定的」as a carve-out; B flags it for undefined abstract dichotomy. |
| 8 | 全域:保真 | 保護 | pass | fail | A renames 姊妹技能 to 其他相關技能, dropping the source's term; B keeps it. |
| 20 | expected-direction | 命中 | pass | fail | B names commas/parentheses/merging as the fix; A only reports dash density with no punctuation direction. |
| 21 | expected-direction | 命中 | pass | fail | B directs removing the bold inline labels (plain text plus colon) while keeping the three items; A flags the bold pattern but gives a direction only for the vague claims. |
| 23 | expected-direction | 命中 | pass | fail | B says delete the chat leftovers and close on content or a concrete next step; A only labels them problems and even softens the first sentence. |
| 28 | no-single-instance-false-positive | 保護 | fail | fail | Both flag the single explanatory lead-in as a P1 problem, which the protection row forbids. |
| 32 | expected-direction | 命中 | fail | pass | A flags all three residues (utm param, citeturn token, 「以下是清理後的版本，請複製使用」) and keeps the link; B explicitly declines to flag the third. |
| 36 | expected-direction | 命中 | pass | fail | A only offers removing/replacing the 意義 column while keeping the table; B calls for dropping the column and rewriting as a direct sentence. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A lists 「三個心得」 as a P2 problem with a 改法方向 targeting the second sentence; B records it as 未另標 under a carve-out. |
| 43 | expected-behavior | 保護 | fail | pass | A passes clean; B raises P1 空降主張 on 「這支影片是我們頻道成長最快的一支」 when case should be released untouched. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs the hidden-author audit under the declaration and reports 立場真空 plus 零具體個人細節; B reports no issues at all and never runs the audit. |
| 55 | declaration-attributed | 命中 | pass | fail | A states the 署名文體 verdict comes from the user's --expect-author declaration; B never mentions the declaration. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs the audit and reports two absence signals; B answers 無 and treats the memo as exempt boilerplate. |
| 56 | declaration-attributed | 命中 | pass | fail | A attributes the 署名文體 call to the user declaration; B omits any mention of --expect-author. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 2
- hit-class failures, new arm (comparative 87): 3
- hit-class failures, base arm (comparative 87): 6

NO-SHIP — 2 protection-class false kill(s) on the new arm: 28/no-single-instance-false-positive, 43/expected-behavior


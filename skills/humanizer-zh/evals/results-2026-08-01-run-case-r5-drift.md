# run-case — humanizer-zh — 2026-08-01

- run id: `53783e9c4415440f898ab8a05d25fa70`
- new arm: working tree `/Users/leoluyi/.skills/.claude/worktrees/wild-stargazing-planet/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `3eedd0f:skills/humanizer-zh`, version 2.1.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-0rn4a87m`

## Chunks

| chunk | range | cases | ids | rows |
|---|---|---|---|---|
| 0 | [1, 9] | 9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 38 |
| 1 | [10, 19] | 9 | 10, 11, 12, 13, 14, 15, 16, 18, 19 | 18 |
| 2 | [20, 67] | 11 | 20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 67 | 16 |
| 3 | [25, 71] | 14 | 25, 26, 27, 28, 29, 45, 46, 47, 55, 60, 61, 64, 68, 71 | 42 |
| 4 | [30, 69] | 14 | 30, 31, 32, 33, 34, 48, 49, 50, 51, 56, 62, 63, 65, 69 | 34 |
| 5 | [35, 70] | 13 | 35, 36, 37, 38, 39, 52, 53, 54, 57, 58, 59, 66, 70 | 31 |

## Denominators

```
absolute denominator: 149 − 3 + 33 = 179
  149 raw expectations in evals.json
  − 3 unscored (slug prefix: ground-truth-note)
  + 33 global rewrite rows (11 rewrite case(s) × 3 check(s))
comparative denominator: 179 − 11 = 168
  − 11 rows on baseline-incompatible ids [1, 4, 55, 56]
```

## baseline_incompatible deductions

| ids | rows deducted | reason |
|---|---|---|
| [1, 4, 55, 56] | 11 | 1.5.0 是 --structure-signals／結構級訊號，沒有 --expect-author；55/56 為 be5a09d 新增，1.5.0 結構上不可能過 |

## Per-class pass counts (absolute denominator)

| class | arm | pass | total |
|---|---|---|---|
| 保護 | new | 104 | 115 |
| 保護 | base | 103 | 115 |
| 命中 | new | 61 | 64 |
| 命中 | base | 59 | 64 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 7 | flags-contrast-construction | 命中 | pass | fail | A flags 範圍是開放的，不是固定的 as 對比句式; B explicitly grants the carve-out and does not flag it. _(A=new, B=base)_ |
| 22 | expected-direction | 命中 | fail | pass | A caps at one trailing emoji plus asks for concrete update info; B recommends keeping 一至兩個 emoji, above the 0–1 target. _(B=new, A=base)_ |
| 43 | expected-behavior | 保護 | fail | fail | Neither releases the post: A raises four findings and B three, so the pass-through expectation is not met. _(B=new, A=base)_ |
| 43 | preserves-negative-verdict | 保護 | pass | fail | A flags 「實測網頁設計功力不行」 as 空降主張 needing evidence, while B explicitly carves it out as a genuine first-hand negative verdict. _(B=new, A=base)_ |
| 43 | no-idiom-flattening | 保護 | fail | fail | Both label 表現不俗 and 可圈可點 as 推廣語氣 and advise deleting/replacing them, flattening the author's评价 register. |
| 67 | flags-register-drift | 命中 | pass | fail | A reports no defect at all; B flags 語體漂移 citing the missing predicate, 「取得」 reaching back across the comma, and absent 將/等 marker. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | pass | fail | A gives no fix; B offers the either/or of promoting to a full sentence or demoting to a field label with the schedule moved to a parenthetical/separate field. _(B=new, A=base)_ |
| 27 | expected-behavior | 保護 | fail | fail | Both raise P0 知識截止免責 on the human verification caveat, which the row forbids. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A puts the single 解說導引腔 in 保留裁決 only, while B lists it as a named P1 entry despite the carve-out note. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Row demands full release but A raises six flags and B raises four. _(A=new, B=base)_ |
| 61 | preserves-slang-register | 保護 | fail | fail | Both delete 「老司機都知道」 outright, removing the author's slang register. |
| 68 | flags-register-drift | 命中 | pass | fail | A names 語體漂移 with the cross-comma 確認 evidence; B flags 抽象claim缺交付 instead and never diagnoses register. _(A=new, B=base)_ |
| 68 | fix-picks-one-register | 命中 | pass | fail | A promotes the value to a single complete clause after the field label; B only inserts 的/於 and leaves the same hybrid shape. _(A=new, B=base)_ |
| 30 | no-vague-alias-demand | 保護 | pass | fail | A only offers 小美/她; B offers 「學員」 as an acceptable fixed alias, a vague alias instead of the protected real name. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | fail | pass | A explicitly declines to flag 「以下是清理後的版本，請複製使用」, missing the third residue; B names all three. _(A=new, B=base)_ |
| 62 | expected-behavior | 保護 | fail | fail | Neither passes the passage clean: both raise multiple P1 flags on the annual-report prose. |
| 62 | no-slogan-flagging | 保護 | fail | fail | A flags 「成功的關鍵就在於協助客戶獲得成功」as 空話填充 and B as 意義膨脹 — both treat the business-model statement as an empty slogan. _(A=new, B=base)_ |
| 62 | preserves-superlative-with-evidence | 保護 | fail | fail | Both flag 「世界領先的」as unsupported superlative and suggest deleting it despite the verifiable figures in the same sentence. |
| 63 | preserves-dash-inconsistency | 保護 | fail | fail | Both explicitly flag and remove the two dashes, erasing the original's typographic inconsistency. |
| 58 | expected-direction | 命中 | fail | pass | A flags only 「由於我無法瀏覽網路」 and protects 「截至我最後更新的資料」 as a dated as-of note, missing the second model self-disclosure that B flags. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | pass | A flags the closing rhetorical question as 反問句開場與收尾 for not stating the conclusion; B clears both prohibited misjudgments. _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | pass | A directs converting 「你的優勢在哪裡？」 into a statement or supplying the answer; B leaves it as is. _(A=new, B=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 60 | 全域:不換湯 | 命中 | 保護 |
| 61 | 全域:不換湯 | 命中 | 保護 |
| 64 | 全域:不換湯 | 命中 | 保護 |
| 68 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 179): 11
- hit-class failures, new arm (comparative 168): 3
- hit-class failures, base arm (comparative 168): 5

NO-SHIP — 11 protection-class false kill(s) on the new arm: 43/expected-behavior, 43/no-idiom-flattening, 27/expected-behavior, 47/expected-behavior, 61/preserves-slang-register, 62/expected-behavior, 62/no-slogan-flagging, 62/preserves-superlative-with-evidence, and 3 more


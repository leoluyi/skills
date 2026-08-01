# run-case — humanizer-zh — 2026-08-01

- run id: `934a6ed3bdbe40d3af1cb2fc7e4869ad`
- new arm: working tree `/Users/leoluyi/.skills/.claude/worktrees/wild-stargazing-planet/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `3eedd0f:skills/humanizer-zh`, version 2.1.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-78j5p91g`

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
| 保護 | new | 105 | 115 |
| 保護 | base | 104 | 115 |
| 命中 | new | 62 | 64 |
| 命中 | base | 57 | 64 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | pass | fail | Both rule 作者隱身不成立, but B additionally flags the stance-marked 「我認為第一種比較完美」as 推廣語氣, hitting a genuine voice marker the row says should stay clean. _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | pass | fail | A flags 「範圍是開放的，不是固定的」and demands the boundary be defined; B grants the 對比句式 carve-out and leaves it unflagged. _(A=new, B=base)_ |
| 10 | flags-four-char-appraisal | 命中 | fail | pass | A lists each idiom as own item; B lumps them in one bullet and never names 節奏明快 as a 四字評語. _(B=new, A=base)_ |
| 43 | expected-behavior | 保護 | fail | fail | Neither passes it through — both raise four P1 flags across all three verdict clauses. |
| 43 | no-idiom-flattening | 保護 | fail | fail | Both treat 表現不俗 and 可圈可點 as empty phrasing to delete or swap out. |
| 67 | flags-register-drift | 命中 | pass | fail | A names 語體漂移 with the label-plus-fronted-object syntax evidence; B only reports a vague missing-deliverable-form issue. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | pass | fail | A offers the promote-to-sentence vs demote-to-entry choice and puts the schedule in parentheses as annotation; B just asks for an added owner. _(A=new, B=base)_ |
| 27 | expected-behavior | 保護 | fail | fail | Both raise P0 知識截止免責 on a human verification caveat that carries no model self-reference. |
| 28 | no-single-instance-false-positive | 保護 | fail | pass | A applies the carve-out and only flags the missing antecedent data; B applies the carve-out but re-hangs the same guide clause as 意義膨脹 on 「一件很重要的事」. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Source expects full pass-through but A raises nine findings and B eight. _(B=new, A=base)_ |
| 61 | preserves-slang-register | 保護 | fail | fail | Both delete 「老司機」 outright instead of preserving the author's slang register. |
| 64 | 全域:保真 | 保護 | fail | pass | B downgrades the author's claim 「SEO 的死亡」 to 「SEO 會受到影響」, changing the asserted content; A keeps it. _(B=new, A=base)_ |
| 68 | flags-register-drift | 命中 | pass | fail | A labels it 抽象claim缺交付 only; B flags 語體漂移 with the headless-noun-plus-trailing-verb evidence. _(B=new, A=base)_ |
| 68 | fix-picks-one-register | 命中 | pass | fail | A keeps the label-colon plus trailing-verb hybrid; B commits to a single full sentence. _(B=new, A=base)_ |
| 68 | facts-preserved-verbatim | 保護 | pass | fail | A rewrites 協作機制 into 協作方式; B keeps 跨部門工作小組、外部顧問協作機制、第一次會議後兩週內 intact. _(B=new, A=base)_ |
| 68 | 全域:保真 | 保護 | pass | fail | A's 機制 to 方式 substitution is term drift on a protected phrase; B preserves all facts. _(B=new, A=base)_ |
| 68 | 全域:不換湯 | 命中 | pass | fail | A trades one vague noun (機制) for an equally vague sibling (方式); B performs no such swap. _(B=new, A=base)_ |
| 32 | expected-direction | 命中 | pass | fail | A names utm param, citeturn placeholder and the 「以下是清理後的版本，請複製使用」 chat residue; B omits the chat residue. _(A=new, B=base)_ |
| 62 | no-slogan-flagging | 保護 | fail | fail | Both flag 「成功的關鍵就在於協助客戶獲得成功」 as 空話填充. |
| 62 | preserves-superlative-with-evidence | 保護 | fail | fail | Both flag 「世界領先的」 as 推廣語氣 despite the verifiable figures in the same sentence. |
| 63 | preserves-dash-inconsistency | 保護 | fail | fail | Both remove the two differing dashes instead of leaving the original typography. |
| 58 | expected-direction | 命中 | fail | pass | A flags only 「我無法瀏覽網路」 and protects 「截至我最後更新的資料」 as a dated as-of note, missing the second self-reference; B flags both. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 179): 10
- hit-class failures, new arm (comparative 168): 2
- hit-class failures, base arm (comparative 168): 7

NO-SHIP — 10 protection-class false kill(s) on the new arm: 43/expected-behavior, 43/no-idiom-flattening, 27/expected-behavior, 28/no-single-instance-false-positive, 47/expected-behavior, 61/preserves-slang-register, 64/全域:保真, 62/no-slogan-flagging, and 2 more


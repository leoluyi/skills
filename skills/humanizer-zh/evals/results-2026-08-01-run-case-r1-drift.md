# run-case — humanizer-zh — 2026-08-01

- run id: `9f77f2dbbea1400e94db04a06825bb23`
- new arm: working tree `/Users/leoluyi/.skills/.claude/worktrees/wild-stargazing-planet/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `3eedd0f:skills/humanizer-zh`, version 2.1.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-t_k_v5wi`

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
| 保護 | new | 99 | 115 |
| 保護 | base | 104 | 115 |
| 命中 | new | 62 | 64 |
| 命中 | base | 61 | 64 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | fail | pass | A judges the piece clean apart from a vague-scope phrase; B additionally flags 破折號濫用 on the dash carrying the 13-year personal recollection, killing a real voice marker. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A flags 「範圍是開放的，不是固定的。」 and demands the real scope and criteria; B invokes the factual-boundary carve-out and keeps it unflagged. _(B=new, A=base)_ |
| 21 | no-prose-collapse-demand | 保護 | fail | pass | A offers '改成連續段落' as a fix, demanding prose collapse; B explicitly rules the list format legitimate. _(A=new, B=base)_ |
| 22 | expected-direction | 命中 | fail | pass | A permits keeping '一兩個' emoji, above the 0–1 target; B caps at one trailing emoji plus concrete-content direction. _(A=new, B=base)_ |
| 43 | expected-behavior | 保護 | pass | fail | A passes the sentence clean; B raises a 推廣語氣 P1 on the whole verdict string, a false positive. _(A=new, B=base)_ |
| 67 | flags-register-drift | 命中 | pass | fail | A flags 語體漂移 and cites the predicate-less label half plus 「取得」 reaching back across the comma; B reports P0/P1/P2 all 無. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | pass | fail | A gives a single-register choice (升格成句 or 降格成條目) and puts the schedule in a parenthetical note; B gives no fix at all. _(A=new, B=base)_ |
| 27 | expected-behavior | 保護 | fail | fail | Both flag P0 知識截止免責 on a human verification caveat lacking any model self-reference. |
| 47 | expected-behavior | 保護 | fail | fail | Both raise numerous P1 flags on a passage the key says should pass untouched. |
| 47 | no-run-on-splitting | 保護 | fail | fail | A flags 破碎短句堆疊 urging split into claim/reason/observation; B declares scope 整段重寫 because the passage is compressed into one sentence. _(B=new, A=base)_ |
| 61 | preserves-slang-register | 保護 | fail | fail | Both delete 老司機 from the rewrite rather than preserving the author's slang register. |
| 61 | preserves-implicature | 保護 | fail | fail | Both delete 意味著什麼！ instead of leaving the deliberate unsaid intact — removal destroys the implicature as surely as filling it. |
| 64 | 全域:保真 | 保護 | fail | pass | B drops the source's final clause 所以就更不可能去你網站了 as 'repetition', losing author-supplied content. _(B=new, A=base)_ |
| 64 | 全域:不代筆 | 保護 | fail | pass | B injects an editorial parenthetical into the delivered rewrite text itself, inserting words the author never wrote into the prose. _(B=new, A=base)_ |
| 68 | flags-register-drift | 命中 | pass | fail | A labels it 過度簡寫/抽象claim; only B names 語體漂移 with the predicate-less first half and cross-comma 確認 as evidence. _(B=new, A=base)_ |
| 62 | no-slogan-flagging | 保護 | fail | fail | Both flag 成功的關鍵就在於協助客戶獲得成功 as 空話填充. |
| 62 | preserves-superlative-with-evidence | 保護 | fail | fail | Both flag 世界領先的 as unsourced promotional superlative despite the verifiable figures in the same passage. |
| 63 | preserves-dash-inconsistency | 保護 | fail | fail | Both flag the dashes and delete them from the rewrite instead of leaving the original inconsistency intact. |
| 59 | expected-behavior | 保護 | fail | fail | Both flag the argued passage: A tags 反問句 and 模糊歸屬, B additionally tags 對讀者說教 on the supported assertion. _(B=new, A=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | fail | A tells author to 改成陳述句 and state the advantage; B says 直接寫出優勢應來自何處 — both demand rewriting the closing question. _(B=new, A=base)_ |
| 70 | no-weak-signal-stacking | 保護 | fail | pass | B flags 語體漂移 on the 業務流程編排複雜度 sentence; A raises no 語體漂移 flag. _(B=new, A=base)_ |
| 70 | no-noun-phrase-item-false-positive | 保護 | fail | pass | B flags 「提供技術專業、業務系統專業」 as 抽象claim缺交付; A leaves both listed items unflagged. _(B=new, A=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 179): 16
- hit-class failures, new arm (comparative 168): 2
- hit-class failures, base arm (comparative 168): 3

NO-SHIP — 16 protection-class false kill(s) on the new arm: 4/metaphor-absence-does-not-flag-solo, 21/no-prose-collapse-demand, 27/expected-behavior, 47/expected-behavior, 47/no-run-on-splitting, 61/preserves-slang-register, 61/preserves-implicature, 64/全域:保真, and 8 more


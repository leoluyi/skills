# run-case — humanizer-zh — 2026-08-01

- run id: `2c784c7118e14e5ba8072b6e6bde7b57`
- new arm: working tree `/Users/leoluyi/.skills/.claude/worktrees/wild-stargazing-planet/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `3eedd0f:skills/humanizer-zh`, version 2.1.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-4h_8s45o`

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
| 保護 | base | 105 | 115 |
| 命中 | new | 63 | 64 |
| 命中 | base | 58 | 64 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags the elided-premise opener but explicitly declines to flag the rhetorical closing, treating it as a real boundary; B flags both 空降斷言開場 and 反問句收尾. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A flags 「範圍是開放的，不是固定的」 as 對比句式; B grants it the fact-boundary carve-out and leaves it unflagged. _(B=new, A=base)_ |
| 22 | expected-direction | 命中 | pass | fail | A caps emoji at one trailing mark and demands concrete update content, while B twice permits 「一兩個句尾 emoji」, exceeding the 0–1 target. _(A=new, B=base)_ |
| 43 | expected-behavior | 保護 | pass | fail | A passes the post clean, but B raises a P1 推廣語氣 flag on the whole three-clause verdict, a false positive on parallel structure. _(A=new, B=base)_ |
| 43 | no-idiom-flattening | 保護 | pass | fail | A explicitly carves out the appraisal idioms as first-hand judgment, while B lumps 「表現不俗」「可圈可點」 into a 品質評語 flag demanding they be rewritten away. _(A=new, B=base)_ |
| 67 | flags-register-drift | 命中 | pass | fail | A flags 語體漂移 as a hard defect citing the missing subject and the dangling 取得, while B reports P0/P1/P2 all clear and misses the drift entirely. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | pass | fail | A offers the either/or of promoting to a full sentence or demoting to a list label with 時程 as a trailing note; B offers no fix at all. _(A=new, B=base)_ |
| 27 | expected-behavior | 保護 | fail | fail | Both raise a P0 `知識截止免責` on a human verification caveat that carries no model self-reference. |
| 47 | expected-behavior | 保護 | fail | fail | Expectation is full pass-through, yet A raises seven P1 flags and B raises six. _(B=new, A=base)_ |
| 47 | no-run-on-splitting | 保護 | fail | pass | B flags `破碎短句堆疊` and tells the author to split into several full sentences; A does not. _(B=new, A=base)_ |
| 61 | preserves-slang-register | 保護 | fail | fail | Both delete 「老司機」 outright, so the author's slang register does not survive the rewrite. |
| 64 | preserves-typo-joke | 保護 | fail | pass | B's rewrite deletes the first 「跟本」, leaving the follow-up 「是「跟本」喔！」 with nothing to refer to; A keeps both. _(B=new, A=base)_ |
| 64 | 全域:不代筆 | 保護 | fail | pass | B inserts 「我把…解讀成」 and hedged consequences the author never wrote, recasting a flat assertion as a stated personal reading. _(B=new, A=base)_ |
| 68 | flags-register-drift | 命中 | pass | fail | A labels it `過度簡寫` instead of 語體漂移; B names 語體漂移 with the trailing-verb evidence. _(B=new, A=base)_ |
| 68 | fix-picks-one-register | 命中 | pass | fail | A keeps the label colon plus dangling 確認 (half item, half sentence); B produces one complete sentence. _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | fail | fail | Both flag content inside the annual-report passage (A on 造就了…崛起, B on the same plus the superlative) rather than passing it, though neither demands pronoun substitution for the repeated full name. _(A=new, B=base)_ |
| 62 | no-slogan-flagging | 保護 | fail | fail | Both flag 「成功的關鍵就在於協助客戶獲得成功」 as 空話填充/circular, exactly the false positive the row forbids. |
| 62 | preserves-superlative-with-evidence | 保護 | pass | fail | A carves out 「世界領先的」 citing the adjacent 291/535/1萬2,302 figures; B flags it as 推廣語氣 demanding ranking criteria. _(A=new, B=base)_ |
| 63 | preserves-dash-inconsistency | 保護 | pass | fail | A keeps both — and －; B deliberately replaces them with a colon and semicolon, normalizing the original typography. _(A=new, B=base)_ |
| 69 | does-not-rewrite-in-detect | 保護 | fail | pass | A tells the author to turn the field value 「進行資料的整理及客戶標籤之建置」 into a direct-verb sentence, editing a table cell in detect mode; B keeps its notes to abstract-benefit prose and leaves fields alone. _(A=new, B=base)_ |
| 57 | preserves-key-figures | 保護 | fail | pass | B flags 成長來自新客不是留存 as 空降主張 and offers dropping it back to bare metrics, targeting protected content. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | Neither releases the passage: both raise P1 findings (模糊歸屬 plus 對讀者說教 on the argued assertion) instead of passing it through. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 179): 11
- hit-class failures, new arm (comparative 168): 1
- hit-class failures, base arm (comparative 168): 6

NO-SHIP — 11 protection-class false kill(s) on the new arm: 27/expected-behavior, 47/expected-behavior, 47/no-run-on-splitting, 61/preserves-slang-register, 64/preserves-typo-joke, 64/全域:不代筆, 62/expected-behavior, 62/no-slogan-flagging, and 3 more


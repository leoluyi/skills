# run-case — humanizer-zh — 2026-08-01

- run id: `b5820b1fb91244a88658f393c77311e3`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-h2q05v2a`

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
| 保護 | new | 49 | 49 |
| 保護 | base | 44 | 49 |
| 命中 | new | 48 | 49 |
| 命中 | base | 36 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 1 | flags-structural-absence | 命中 | pass | fail | A only hedges the absence under P2 conditionally and never names 只解釋不造像, a near miss; B lists 立場真空、零具體個人細節、無口語破格、只解釋不造像 as an explicit 作者隱身 finding. |
| 3 | no-false-positive-on-voiced-text | 保護 | pass | fail | A lists the stance opener 「工程師該不該寫作，我的答案很明確：該」 under P2 問題 and offers a replacement wording, marking a real voice marker; B reports P0/P1/P2 all clean and 作者隱身不成立. |
| 5 | fix-converts-to-exposition | 命中 | pass | fail | A only labels the problem without prescribing a subject change, while B directs 把「你」改回文件、作者或使用者…改寫成第三人稱判準. |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A flags both the fragmentary opener and the rhetorical-question ending separately; B flags only the 過度簡寫 syntax and folds the closing question into the second-person item. |
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | pass | fail | A replaces paragraph B with an invented rule about writing understanding into verifiable assertions instead of flagging it; B emits a bracketed marker asking the author to supply the content. |
| 6 | 全域:不代筆 | 保護 | pass | fail | A ghostwrites a claim for the hollow second paragraph that the source never made; B declines to fill it. |
| 7 | flags-contrast-construction | 命中 | pass | fail | A explicitly clears 「範圍是開放的，不是固定的」 as a valid boundary statement; B flags it as 對比句式 with an abstract-dichotomy fix. |
| 8 | 全域:保真 | 保護 | pass | fail | A renames the source's 「姊妹技能」 to 「其他相關技能」, dropping a named concept; B keeps it verbatim. |
| 20 | expected-direction | 命中 | pass | fail | A only names dash density as a problem with no repair direction; B explicitly points to commas, parentheses, colons or periods with text preserved. |
| 23 | expected-direction | 命中 | pass | fail | A flags the chatbot residue but suggests the intent may be kept rather than deleting for a reader-facing close; B directs to a concrete conclusion or next step. |
| 24 | expected-direction | 命中 | pass | fail | A only criticizes the praise stacking without directing to answer the question; B says to answer the submission method directly. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A flags the single guiding sentence as a P1 defect; B applies the density carve-out and declines to flag it. |
| 34 | expected-direction | 命中 | pass | fail | B directs merging the three items into a coherent paragraph plus concrete metrics/owners, while A demotes the numbering to a conditional P2 and states the list form itself needs no flag. |
| 36 | expected-direction | 命中 | pass | fail | B calls the whole table misuse and directs prose replacement with the 意義 column dropped; A says the table may not be misused and only offers column removal as an alternative, with no prose direction. |
| 37 | expected-direction | 命中 | pass | fail | B requires the author's actual choice and reason to be supplied by the author (no ghostwriting); A only describes the stance vacuum without directing an explicit judgment or author-fill placeholder. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A reports no findings at all and ignores --expect-author; B declares 署名文體 and lists 立場真空 plus 零具體個人細節 among subsignals. |
| 55 | declaration-attributed | 命中 | pass | fail | A never mentions the declaration; B states the genre call comes from user declaration, not model reading. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A returns all-clear with no hidden-author run; B runs it under declaration and reports the absences. |
| 56 | declaration-attributed | 命中 | pass | fail | A gives no attribution; B attributes genre switch to the flag and notes the text is genre-correct as 公文. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 0
- hit-class failures, new arm (comparative 87): 1
- hit-class failures, base arm (comparative 87): 8

SHIP — protection-class false kills 0; hit-class did not regress


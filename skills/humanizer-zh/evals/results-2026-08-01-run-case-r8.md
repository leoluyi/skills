# run-case — humanizer-zh — 2026-08-01

- run id: `1a6915c8f8fd4cbf883c241b9e8705d5`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-42nns3e4`

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
| 保護 | base | 42 | 49 |
| 命中 | new | 49 | 49 |
| 命中 | base | 39 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | pass | fail | A emits a marker line for the hollow paragraph, while B replaces it with invented prescriptive content (「套用範本不能取代這一步」) the source never contained. |
| 6 | 全域:不代筆 | 保護 | pass | fail | B ghostwrites a substitute second paragraph asserting guidance absent from the source; A adds nothing. |
| 7 | flags-contrast-construction | 命中 | pass | fail | A flags 「範圍是開放的，不是固定的。」 as 對比句式; B explicitly declares it a real boundary and 不應標記. |
| 8 | 全域:保真 | 保護 | pass | fail | B renames the source term 姊妹技能 to 「其他相關技能」, widening the referent; A preserves it. |
| 9 | flags-bare-verb | 命中 | pass | fail | A restores the object (「不會把真正的術語誤判成需要修改的詞」); B converts it into a reader directive 「請保留原文，避免誤改」 that still leaves 誤改 objectless and changes who acts. |
| 9 | no-false-positive-on-established-abbrev | 保護 | pass | fail | The complete 資安 sentence was to be left alone; A leaves it verbatim while B rewrites 「沿用既有範本即可」 into 「可沿用既有範本」. |
| 9 | 全域:不代筆 | 保護 | pass | fail | B asserts a new instruction 「遇到專有名詞時，請保留原文」 that the source never states, turning a descriptive claim into invented guidance. |
| 22 | expected-direction | 命中 | pass | fail | A caps emoji at one or two and demands concrete update content, while B explicitly allows 🚀💡✅ each once, leaving three emoji above the 0–1 target. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A explicitly declines to flag the single explanatory lead-in, while B flags 「把這三個數字擺在一起，你會讀到一件很重要的事」 as 解說導引／讀者引導句. |
| 34 | expected-direction | 命中 | pass | fail | A concludes the numbered list itself is an acceptable judgment call instead of directing a prose rewrite, while B asks for 一段連續論述 plus concrete channels and metrics. |
| 36 | expected-direction | 命中 | pass | fail | A says the table form is fine and only faults cell wording, never calling for removing the 意義 column or prose; B names the prose one-sentence alternative and column replacement. |
| 37 | expected-direction | 命中 | pass | fail | A treats the stance vacuum as a genre-dependent judgment call with no demand for the author's actual choice, whereas B requires the author to name which tool and why and refuses to ghostwrite it. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A lists the second sentence as a P1 元敘事式導言 problem; B explicitly carves it out as protected first-person topic statement. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs hidden-author under the declaration and reports 立場真空 plus 零具體個人細節; B reports 無 and excuses it as docs genre. |
| 55 | declaration-attributed | 命中 | pass | fail | A marks the genre call as 依使用者宣告; B never mentions the declaration at all. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs hidden-author and reports absences; B answers with 無 and calls it correct 公文 genre, i.e. the refused-to-run failure mode. |
| 56 | declaration-attributed | 命中 | pass | fail | A states 依使用者宣告 and notes the formal句型 is genre-correct; B gives no attribution. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 0
- hit-class failures, new arm (comparative 87): 0
- hit-class failures, base arm (comparative 87): 6

SHIP — protection-class false kills 0; hit-class did not regress


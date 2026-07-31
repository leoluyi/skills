# run-case — humanizer-zh — 2026-08-01

- run id: `7a00da8dd64c4dfab0063d2500ec8514`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-l3r1oq2b`

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
| 保護 | new | 46 | 49 |
| 保護 | base | 45 | 49 |
| 命中 | new | 47 | 49 |
| 命中 | base | 41 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | fail | pass | A fires 破折號濫用 on the dash that carries the 13-年前 first-hand memory — the same construction it protected in case 3 — so the piece is not read as clean; B keeps the single flag to content precision and clears 地雷/13 年前/dash/parenthetical. |
| 7 | flags-contrast-construction | 命中 | pass | fail | A flags 範圍是開放的，不是固定的 as 對比句式; B explicitly clears it as 具體的事實界線, applying the carve-out that does not hold here. |
| 8 | 全域:保真 | 保護 | pass | fail | A keeps 姊妹技能 verbatim; B renames it to 其他相關技能, dropping a named concept from the source. |
| 9 | flags-copula-elision | 命中 | fail | pass | A relabels the clause as 文件自述 and replaces it with a bracketed gap request instead of restoring the frame; B names the missing 是依……寫成的 frame and completes it. |
| 9 | no-false-positive-on-established-abbrev | 保護 | fail | pass | A flags 既有範本 as 併稿接縫 and guts the complete sentence into 資安設定沿用〔請補入…〕; B records no defect there and keeps the sentence's substance. |
| 9 | 全域:保真 | 保護 | fail | pass | A drops the source fact 沿用既有範本 and converts the guide's self-description into an editorial bracket; B carries both facts through. |
| 9 | 全域:不代筆 | 保護 | pass | fail | B invents 保留領域通用寫法, a handling rule the source never states; A adds no new claim. |
| 22 | expected-direction | 命中 | fail | pass | A caps emoji but explicitly clears the vague CTA text, so it never asks for what-was-updated specifics; B flags both emoji stacking and the missing concrete benefit. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A explicitly withholds the 解說導引腔 flag for a single occurrence, while B flags 對讀者的解說導引 on that lone sentence. |
| 34 | expected-direction | 命中 | pass | fail | A directs merging into連貫論述 plus concrete owners/metrics; B explicitly defends the numbered list and never calls for prose. |
| 36 | expected-direction | 命中 | pass | fail | A flags the whole table and directs a single prose sentence dropping the「意義」column; B says the table itself is fine and suggests patching cells instead. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A carves the second sentence out; B flags it as Meta-narration P1 and additionally flags「三個心得」as formulaic preview. |
| 39 | expected-direction | 命中 | pass | fail | A directs deletion of the consequence-free reaction pair; B defaults to keeping「我愣了一下」as possibly genuine voice. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs hidden-author under declaration and reports 立場真空 plus 零具體個人細節; B reports all-clear and never runs the check. |
| 55 | declaration-attributed | 命中 | pass | fail | A states the 署名文體 judgment comes from user declaration not model inference; B never mentions the flag. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A runs hidden-author under declaration and reports absences; B returns all-clear citing 公文格式, effectively declining to run it. |
| 56 | declaration-attributed | 命中 | pass | fail | A records the genre call as user declaration with 公文 carve-out note; B has no attribution at all. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 3
- hit-class failures, new arm (comparative 87): 2
- hit-class failures, base arm (comparative 87): 4

NO-SHIP — 3 protection-class false kill(s) on the new arm: 4/metaphor-absence-does-not-flag-solo, 9/no-false-positive-on-established-abbrev, 9/全域:保真


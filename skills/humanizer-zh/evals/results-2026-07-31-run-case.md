# run-case — humanizer-zh — 2026-07-31

- run id: `12287f02a989494187c66b11349ac481`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.0.0, 6 file(s)
- base arm: `520d5bb:skills/avoid-ai-writing-zh`, version 1.5.0, 3 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `d5fc2d987a5da6e03b1cf2e54c52a5250d0ec8952b178f56b6fe344aa229c5bc`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-79_2adjk`

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
| 保護 | base | 45 | 49 |
| 命中 | new | 40 | 49 |
| 命中 | base | 39 | 49 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | fix-converts-to-exposition | 命中 | fail | pass | A prescribes rewriting in third person with full sentences; B lists tags only and offers no fix direction at all. |
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags 破碎短句 but folds the closing line into the second-person item without flagging it as a rhetorical-question 收尾警句; B flags both separately. |
| 7 | flags-contrast-construction | 命中 | pass | fail | A explicitly clears 「範圍是開放的，不是固定的」 as a real boundary; B flags it as an undefined abstract 對比句式. |
| 8 | 全域:保真 | 保護 | pass | fail | A renames 「姊妹技能」 to 「其他相關技能」 and drops the 「不是前置條件」 statement, replacing it with a different claim; B keeps both verbatim. |
| 8 | 全域:不代筆 | 保護 | pass | fail | A asserts 「本技能可以獨立使用」 and an activation procedure the source never states; B's 「輸入名稱手動啟動」 stays a paraphrase of invoke-by-name. |
| 10 | flags-four-char-appraisal | 命中 | fail | pass | A lumps all six into one undifferentiated span flag without naming each idiom per the four-char table; B lists 節奏明快/張弛有度/有條不紊/一氣呵成/三線並行/成效顯著 individually. |
| 10 | flags-rhythm-metaphor | 命中 | fail | pass | A never cites 開發節奏 as a rhythm-metaphor entry; B explicitly flags 「節奏」套用在開發工作上 and points at missing 期程/頻率. |
| 10 | fix-points-to-concrete | 命中 | fail | pass | A only says 未交代 with no fix direction and refuses to indicate concrete targets; B names the missing concretes (三條線內容、負責單位、數據、比較) without substituting new idioms. |
| 15 | expected-direction | 命中 | fail | pass | A flags the inflation spans but gives no concrete-fact direction, whereas B names the replacement targets (實際完成的活動、參與人數、後續安排、產出) and covers all the value-escalation words. |
| 16 | expected-direction | 命中 | fail | pass | A only labels the spans as lacking delivery; B states the course must be described via 課綱、實作內容或可驗證成果 while explicitly preserving the second-person CTA 「將帶領你」. |
| 18 | expected-direction | 命中 | fail | pass | A gives no keep-one-instance guidance and instead spends the entry on a hidden-author scoring tangent; B says one sharp contrast may stay and the density of three is the problem. |
| 19 | expected-direction | 命中 | fail | pass | A leaves 無縫、直觀、強大 unflagged via a social-register carve-out and offers no dismantling direction; B flags the adjective stack and the parallel triad and asks for the specific mechanism behind each promise. |
| 28 | no-single-instance-false-positive | 保護 | pass | fail | A lists the single explanatory lead-in as a P1 finding, while B names it a candidate but declines to count it as below the stacking threshold. |
| 32 | expected-direction | 命中 | pass | fail | A catches all three residues (utm param, citeturn marker, 「以下是清理後的版本，請複製使用」) while preserving the link body; B misses the chat-delivery sentence entirely. |
| 34 | expected-direction | 命中 | pass | fail | A flags the numbered structure itself plus the missing platform/metric specifics; B explicitly says the numbering is not the problem and the list may stay, contradicting the prose-rewrite direction. |
| 36 | expected-direction | 命中 | pass | fail | A treats the whole table as misuse pointing toward prose; B states the table is not necessarily misused and only hedges that the 意義 column 「可能」 is low-density, never calling for its removal. |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A explicitly rules the second sentence acceptable; B flags 「今天，我想跟大家分享」 as 延遲進入主題 at P1, the exact false positive this row forbids. |
| 39 | expected-direction | 命中 | pass | fail | A marks both reaction-camera sentences for removal; B only calls them redundant and advises keeping one, so a canned reaction shot survives. |
| 55 | hidden-author-runs-under-declaration | 命中 | pass | fail | A reports 無 and excludes on genre grounds; B runs gate and names 立場真空 plus 零具體個人細節. |
| 55 | declaration-attributed | 命中 | pass | fail | B states gate applied 因使用 --expect-author; A never mentions declaration. |
| 56 | hidden-author-runs-under-declaration | 命中 | pass | fail | A answers 無 citing 公文 genre; B runs gate and reports absent subsignals. |
| 56 | declaration-attributed | 命中 | pass | fail | B attributes genre call to user declaration and notes 公文 reading is correct; A does not. |
| 57 | expected-direction | 命中 | fail | pass | A flags all five guiding sentences and keeps 3.2%/18%; B omits 「把這兩個數字擺在一起看，你會發現一件事」. |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 98): 0
- hit-class failures, new arm (comparative 87): 9
- hit-class failures, base arm (comparative 87): 6

NO-SHIP — hit-class regressed: new arm 9 failure(s) vs baseline 6 (comparative denominator)


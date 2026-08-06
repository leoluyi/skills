# run-case — humanizer-zh — 2026-08-06

- run id: `1ce034147cab4d67a5acd9a6a10704b0`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 1)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-ul1c39jl`

## Chunks

| chunk | range | cases | ids | rows |
|---|---|---|---|---|
| 0 | [1, 86] | 19 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 86 | 62 |
| 1 | [20, 85] | 32 | 20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 67, 72, 76, 79, 85, 25, 26, 27, 28, 29, 45, 46, 47, 55, 60, 61, 64, 68, 71, 73, 77, 80 | 80 |
| 2 | [30, 84] | 34 | 30, 31, 32, 33, 34, 48, 49, 50, 51, 56, 62, 63, 65, 69, 74, 78, 81, 83, 35, 36, 37, 38, 39, 52, 53, 54, 57, 58, 59, 66, 70, 75, 82, 84 | 96 |

## Denominators

```
absolute denominator: 199 − 3 + 42 = 238
  199 raw expectations in evals.json
  − 3 unscored (slug prefix: ground-truth-note)
  + 42 global rewrite rows (14 rewrite case(s) × 3 check(s))
comparative denominator: 238 − 11 = 227
  − 11 rows on baseline-incompatible ids [1, 4, 55, 56]
```

## baseline_incompatible deductions

| ids | rows deducted | reason |
|---|---|---|
| [1, 4, 55, 56] | 11 | 1.5.0 是 --structure-signals／結構級訊號，沒有 --expect-author；55/56 為 be5a09d 新增，1.5.0 結構上不可能過 |

## Per-class pass counts (absolute denominator)

| class | arm | pass | total |
|---|---|---|---|
| 保護 | new | 143 | 153 |
| 保護 | base | 146 | 153 |
| 命中 | new | 76 | 85 |
| 命中 | base | 75 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags only the rhetorical-question ending; B flags both 破碎短句「差在骨幹是誰的話」 and the question ending. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A flags 「範圍是開放的，不是固定的」 and asks for the actual boundary; B explicitly spares it as a real boundary. _(B=new, A=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | fail | fail | Neither output flags 「兩條路」 as a colloquial catch-all. |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | A flags nothing; B explicitly denies 「會結束，放心壓」 is a broken inference. _(B=new, A=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the unmarked conditional ending in 「就別開」. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note by invoking casual voice/carve-outs. |
| 22 | expected-direction | 命中 | pass | fail | A only cuts emoji and explicitly declines to ask for concrete update content; B cuts emoji and flags the vacuous claims for specifics. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Both flag 空降主張 and 情緒宣告 on a passage the key says should pass untouched. |
| 64 | 全域:不代筆 | 保護 | fail | pass | B replaces the author's assertion 「SEO 的死亡」with 「SEO 會受到更大壓力」and hedges the predictions into 「可能」, asserting a stance the source never took. _(B=new, A=base)_ |
| 68 | facts-preserved-verbatim | 保護 | fail | pass | B replaces 協作機制 with 協作方式與分工; A keeps 跨部門工作小組、外部顧問、協作機制、第一次會議、兩週 all intact. _(B=new, A=base)_ |
| 68 | 全域:保真 | 保護 | fail | pass | B drops the deliverable term 協作機制; A carries every load-bearing item over verbatim. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | Both explicitly declare the causal chain sound and flag only 撐得住, missing the unstated-premise conclusions. |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency or node headroom as the missing premise. |
| 80 | flags-missing-connective | 命中 | fail | fail | Both declare the 延長保固 clause relationally clear and flag nothing. |
| 80 | fix-restores-the-connective | 命中 | fail | fail | No conditional marker fix offered by either, since neither flagged the clause. |
| 36 | expected-direction | 命中 | pass | fail | A directs to 一句連貫文字; B only offers deleting the column or swapping in concrete columns, never prose. _(A=new, B=base)_ |
| 58 | preserves-quota-figure | 保護 | pass | fail | A protects the 每月 100 次呼叫 figure explicitly; B declares 保護清單：無, leaving the only figure in the段 unprotected. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | Both flag the closing rhetorical question (and the argued assertion), instead of releasing the passage. |
| 59 | preserves-rhetorical-question | 保護 | fail | fail | A tells the author to state it declaratively, B to state the competitive question directly; both rewrite away the question. _(A=new, B=base)_ |
| 62 | expected-behavior | 保護 | fail | pass | A flags 造就了全球無晶圓廠IC設計產業的崛起 as 意義膨脹 on a 放行 case; B releases the whole passage. _(A=new, B=base)_ |
| 62 | preserves-figures | 保護 | pass | fail | A repeats 1 萬 2,302 with the Chinese place word; B renders it as 12,302, converting the notation. _(A=new, B=base)_ |
| 66 | preserves-sentence-final-particle | 保護 | fail | pass | A rewrites to 像是沒有人要下班, dropping 耶; B keeps 都沒有人要下班耶. _(A=new, B=base)_ |
| 75 | no-self-vouching-false-positive | 保護 | pass | fail | A carves it out as a cross-reference; B flags it as 自我背書. _(A=new, B=base)_ |
| 81 | flags-under-fragmented-clause-rule | 命中 | fail | pass | A tags it 過度簡寫; B tags it 破碎短句堆疊 as required. _(A=new, B=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | pass | A rewrites it to 進入設定頁並向下捲動, deleting the 你會看到 procedural form; B keeps the sentence verbatim. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 10
- hit-class failures, new arm (comparative 227): 9
- hit-class failures, base arm (comparative 227): 10

NO-SHIP — 10 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 64/全域:不代筆, 68/facts-preserved-verbatim, 68/全域:保真, 59/expected-behavior, 59/preserves-rhetorical-question, 62/expected-behavior, and 2 more


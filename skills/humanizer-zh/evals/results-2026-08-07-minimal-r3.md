# run-case — humanizer-zh — 2026-08-07

- run id: `3b9f272941744f61a582f28ca7b3f03a`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 3)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-38t3equ_`

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
| 保護 | base | 145 | 153 |
| 命中 | new | 69 | 85 |
| 命中 | base | 72 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 1 | no-word-level-false-positives | 保護 | fail | pass | A marks the correct technical clause 「例如環境一致性與部署效率」 as 列舉代替論述, while B explicitly rules that content protected and only touches the vague quantifier/closer. _(A=new, B=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A lists only two 對讀者說教 items with no syntax-level flag, while B flags the premise-less opening plus a separate 反問句收尾 entry. _(A=new, B=base)_ |
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | fail | pass | A silently keeps a hollow 「這是必須面對的事實。」 instead of a marker, while B outputs an explicit bracketed flag returning the paragraph to the author. _(A=new, B=base)_ |
| 6 | 全域:不換湯 | 命中 | fail | pass | A swaps 「是你該面對的事實」 for 「這是必須面對的事實」, same empty family; B replaces it with a flag. _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | pass | fail | A flags 「範圍是開放的，不是固定的」 as 對比句式; B explicitly releases it under the fact-boundary carve-out. _(A=new, B=base)_ |
| 9 | flags-copula-elision | 命中 | pass | fail | A marks 「照團隊實際的做法寫」 and restores 「是…寫成的」; B lists no flag for it and only mentions the frame fix afterwards. _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Both release 「會結束，放心壓」 as deliberate casual phrasing instead of flagging the premise-less assertion. |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags 「…就別開」 for the unmarked conditional; both call it concrete usage. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole passage on casual voice/carve-out grounds, exactly the register borrowing this row forbids. |
| 22 | expected-direction | 命中 | fail | pass | A only cuts emoji to at most one and explicitly spares 「超有感」/CTA without asking for concrete update info; B both reduces emoji and demands concrete function/result. _(A=new, B=base)_ |
| 28 | no-single-instance-false-positive | 保護 | fail | pass | A flags 「把這三個數字擺在一起」 as 空降斷言開場 and the conclusion as 空降主張, hitting the single guide sentence anyway; B explicitly spares it under the stacking threshold. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Source expects a fully clean pass but A raises three flags (空降主張, 情緒宣告, 模糊歸屬) and B still flags 空降主張. _(A=new, B=base)_ |
| 64 | 全域:保真 | 保護 | fail | pass | A silently changes 「用戶」 to 「使用者」 and drops 「然後在」, altering source wording under a locale-preference pretext; B returns text unchanged. _(A=new, B=base)_ |
| 64 | 全域:不換湯 | 命中 | fail | pass | A swaps 「更方便的即時互動」 for 「直接互動」 and 「所以就」 for 「因此」, same-register substitutions that remove nothing empty; B makes no swaps. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | fail | pass | A offers promote-or-demote as an either/or without addressing that the schedule should be an annotation rather than a second label end; B gives a single promoted full sentence with the schedule folded in front of the verb. _(A=new, B=base)_ |
| 68 | fix-picks-one-register | 命中 | fail | pass | A only inserts 「的」 and 「於」, leaving the label-plus-clause hybrid intact rather than committing to one register; B promotes it to a single full sentence. _(A=new, B=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A flags 自我背書 on 「判斷依據皆來自」 with the completeness-vouching evidence; B explicitly spares it under a docs relaxation. _(A=new, B=base)_ |
| 72 | fix-restores-operative-clause | 命中 | pass | fail | A directs to replace it with a direct statement of judging by the three factors; B gives no fix at all since it passed the clause. _(A=new, B=base)_ |
| 72 | no-disambiguation-confusion | 保護 | pass | fail | A notes no competing criterion exists here so the carve-out does not apply; B spares the clause on the ground it explains the section's criteria, which is the confusion the row forbids. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | A reports the passage clean, and B flags only 「這件事」 and 「撐得住」 as catch-all wording, neither marking the unstated-premise chain between the cache claim and the deferral conclusion. _(A=new, B=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency, or node headroom as the missing premise. |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | pass | fail | A explicitly declines to flag 「目前的架構撐得住」 alone; B flags it as 口語化萬能詞 demanding verifiable load conditions. _(A=new, B=base)_ |
| 80 | flags-missing-connective | 命中 | fail | pass | A declares the clause protected under warranty terms and issues no flag; B flags the bare verb phrase needing re-read to recover the purpose relation. _(A=new, B=base)_ |
| 80 | fix-restores-the-connective | 命中 | fail | pass | A gives no fix; B restores the conditional marker with 「要延長保固，請在購買日起三十天內上網登錄」 rather than splitting or bulleting. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | pass | fail | A 點名 utm、citeturn 與「以下是清理後的版本」三種殘留；B 漏掉對話介面殘留一項。 _(A=new, B=base)_ |
| 34 | expected-direction | 命中 | pass | fail | A 指向「改成連續論述」；B 只要求把條列補具體，並明說補上內容後可作為清單保留，未指向散文。 _(A=new, B=base)_ |
| 35 | expected-direction | 命中 | fail | fail | 兩者只標第二、四句的片段（且放行「值得注意的是」），未判為整句空話，也無互動／非互動的清單或直刪處理。 |
| 59 | expected-behavior | 保護 | fail | fail | 兩者都以反問句規則標記結尾反問（B 另誤標「大家常常在問」），未放行。 _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | fail | A 要求改成直述說明優勢何在，B 要求直接說出答案或刪反問，都動了受保護的反問。 _(A=new, B=base)_ |
| 62 | expected-behavior | 保護 | fail | fail | 應整段放行，A 標了「開創了…商業模式」與「造就了…崛起」，B 標了後者。 _(A=new, B=base)_ |
| 62 | preserves-figures | 保護 | fail | pass | A 在報告中把「1萬2,302」寫成「12,302」，改了中文數字位寫法；B 保留 1 萬 2,302。 _(A=new, B=base)_ |
| 78 | fix-hedging-opener | 命中 | fail | pass | A 以未達堆疊門檻為由保留「值得注意的是」；B 刪除。 _(A=new, B=base)_ |
| 78 | fix-empty-process-phrasing | 命中 | fail | pass | A 只刪「以確保流程的公平性」，留下「採取…方式進行分配」空架；B 改為「依報名順序分配」。 _(A=new, B=base)_ |
| 81 | no-flag-on-second-sentence | 保護 | pass | fail | B 對「測試機與正式機各一份」加掛過度簡寫，屬受保護句的誤傷；A 未標。 _(A=new, B=base)_ |
| 83 | fix-second-person-judgement | 命中 | fail | fail | A 只把「東西」換成「結果」，仍留「你匯出來的…根本沒辦法用」；B 完全沒有案例 83 的輸出。 _(A=new, B=base)_ |
| 83 | 全域:不換湯 | 命中 | pass | fail | A 把「東西」改成具體的「結果」非同族替換；B 未交付本案例改寫。 _(A=new, B=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 63 | 全域:不換湯 | 命中 | 保護 |
| 65 | 全域:不換湯 | 命中 | 保護 |
| 66 | 全域:不換湯 | 命中 | 保護 |
| 78 | 全域:不換湯 | 命中 | 保護 |
| 83 | 全域:不換湯 | 命中 | 保護 |
| 84 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 238): 10
- hit-class failures, new arm (comparative 227): 16
- hit-class failures, base arm (comparative 227): 13

NO-SHIP — 10 protection-class false kill(s) on the new arm: 1/no-word-level-false-positives, 6/hollow-paragraph-flagged-not-fabricated, 86/does-not-spare-on-casual-register, 28/no-single-instance-false-positive, 47/expected-behavior, 64/全域:保真, 59/expected-behavior, 59/preserves-rhetorical-question, and 2 more; hit-class regressed: new arm 16 failure(s) vs baseline 13 (comparative denominator)


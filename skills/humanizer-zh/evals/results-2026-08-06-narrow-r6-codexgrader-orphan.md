# run-case — humanizer-zh — 2026-08-07

- run id: `89ec8ffccb114c0991ac0b3c429131a8`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 3)
- runner: codex (gpt-5.6-luna) effort high
- grader: codex (gpt-5.6-luna) effort high
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-otvtq6bh`

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
| 保護 | new | 145 | 153 |
| 保護 | base | 142 | 153 |
| 命中 | new | 59 | 85 |
| 命中 | base | 67 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | flags-second-person-coaching | 命中 | fail | fail | A 未標記第二人稱教練口吻，B 只標記第一處而放過後續第二人稱判斷。 _(A=new, B=base)_ |
| 5 | fix-converts-to-exposition | 命中 | fail | pass | B 明確建議將你改為作者或文件來源的第三人稱陳述，A 未提出此修法。 _(A=new, B=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A 標記了省略與破碎句及結尾反問，B 未處理分號並置的破碎句。 _(A=new, B=base)_ |
| 6 | 全域:不換湯 | 命中 | fail | pass | A 把硬套換成同族的套用，B 則保留原詞未以另一句空話替代。 _(A=new, B=base)_ |
| 7 | flags-slogan-replacing-explanation | 命中 | fail | pass | A 只標兩條路並在修法中順帶提及細節，B 明確標記連網與離線片語代替步驟說明。 _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | fail | 兩者都把範圍是開放的、不是固定的視為可保留的事實邊界。 |
| 9 | flags-copula-elision | 命中 | pass | fail | A 補成完整的寫成句架，B 只加寫成仍留下懸空句尾。 _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | 兩者都把會結束、放心壓視為可放行的口語回答，未標記無前提的裸斷言。 |
| 86 | flags-missing-connective | 命中 | fail | fail | 兩者都未標記就別開前條件與結論的破碎銜接。 |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | 兩者都以 casual 語域作為放行理由，未跨語域標記過度簡寫。 |
| 21 | expected-direction | 命中 | pass | fail | A要求移除粗體標籤，B反而明確放行粗體標籤且未要求打破一致排比。 |
| 22 | expected-direction | 命中 | fail | fail | 兩者都允許保留一至兩個emoji，超過規定的零至一個上限。 |
| 23 | expected-direction | 命中 | fail | pass | A未處理開頭的泛用收尾，B有要求刪除並改為具體收尾或CTA。 |
| 26 | expected-direction | 命中 | fail | fail | 兩者都未明確要求直接說明會影響轉換率並建議追蹤。 |
| 29 | expected-direction | 命中 | fail | fail | 兩者都未要求整段刪除或改成作者自身的具體行動示範。 |
| 47 | expected-behavior | 保護 | fail | fail | 兩者都對本應一字不動的原文提出修改標記。 |
| 67 | flags-register-drift | 命中 | fail | pass | A只標記語體漂移而未指出無謂語、跨逗號管賓語與缺少授權標記，B有完整指出。 |
| 67 | fix-names-one-register | 命中 | fail | pass | A同時提出升格與降格兩個方向，B只選擇完整句方向並正確處理期程。 |
| 68 | flags-register-drift | 命中 | fail | pass | A未明確指出無謂語、跨逗號管賓語與缺少授權標記，B有指出這些句法證據。 |
| 72 | flags-self-vouching | 命中 | fail | fail | A雖標記自我背書但未指出「皆來自」是在宣告完整性與出處，B則直接放行。 |
| 72 | fix-restores-operative-clause | 命中 | fail | fail | 兩者都未具體指出應把主詞改回判斷動作並補出操作句。 |
| 72 | no-disambiguation-confusion | 保護 | pass | fail | A沒有以消歧義為由放行，B則明確以該理由放行。 |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | 兩者都未標記快取層結論與延後擴充節點之間缺少前提的推論鏈。 |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | 兩者都未指名命中率、目前回應時間或節點餘裕等缺失前提。 |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | fail | 兩者都把「目前的架構撐得住」另標為口語化萬能詞。 |
| 80 | flags-missing-connective | 命中 | fail | pass | A將首句放行，B正確標出裸動詞片語造成的缺少關係標記。 |
| 80 | fix-restores-the-connective | 命中 | fail | pass | A未提供修法，B要求補回「要延長保固」的條件式句架。 |
| 32 | expected-direction | 命中 | fail | fail | 兩者都漏標「以下是清理後的版本，請複製使用」這個對話殘留。 |
| 33 | expected-direction | 命中 | fail | fail | 兩者只要求補具體內容，沒有列出真實挑戰與下一步或指示整段刪除。 |
| 34 | expected-direction | 命中 | pass | fail | A未明確指向改寫成散文，B明確提到改寫成連續段落。 |
| 35 | expected-direction | 命中 | fail | fail | 兩者未按要求處理第二、四句整句空話及互動與非互動模式的後續摘要流程。 |
| 37 | no-fabricated-rationale | 保護 | fail | fail | 兩者都要求作者補選擇與理由，但沒有指向指定的佔位標註。 |
| 56 | hidden-author-runs-under-declaration | 命中 | fail | pass | A依宣告啟用作者隱身檢查並報出缺席，B反而判定未成立。 |
| 59 | expected-behavior | 保護 | pass | fail | A把有論證支撐的結尾反問列為需改寫，B未誤判該反問為立場真空。 |
| 59 | preserves-rhetorical-question | 保護 | pass | fail | A建議刪除或改寫結尾反問，B保留該反問。 |
| 66 | preserves-sentence-final-particle | 保護 | fail | pass | A保留句末「耶」，B改成了沒有「耶」的句子。 |
| 78 | fix-hedging-opener | 命中 | fail | pass | A刪除「值得注意的是」，B明確將其保留。 |
| 81 | flags-under-fragmented-clause-rule | 命中 | fail | pass | A以破碎短句堆疊標記，B錯掛為過度簡寫。 |
| 81 | no-flag-on-second-sentence | 保護 | pass | fail | A誤把「測試機與正式機各一份」列為過度簡寫，B未標記第二句。 |
| 83 | preserves-procedural-second-person | 保護 | fail | fail | 兩者改寫時都刪除了程序指引中的第二人稱「你會看到」。 |
| 83 | no-fabricated-steps | 保護 | fail | fail | 兩者都新增了原文未明示的「匯出頁面」。 |
| 83 | 全域:不代筆 | 保護 | fail | fail | 兩者都對原文沒有的匯出頁面作了新的具體斷言。 |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 8
- hit-class failures, new arm (comparative 227): 25
- hit-class failures, base arm (comparative 227): 18

NO-SHIP — 8 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 79/no-flag-on-final-short-sentence-alone, 37/no-fabricated-rationale, 66/preserves-sentence-final-particle, 83/preserves-procedural-second-person, 83/no-fabricated-steps, 83/全域:不代筆; hit-class regressed: new arm 25 failure(s) vs baseline 18 (comparative denominator)


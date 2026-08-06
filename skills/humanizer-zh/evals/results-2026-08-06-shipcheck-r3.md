# run-case — humanizer-zh — 2026-08-06

- run id: `4459bed8bc2d4e0782a82db93dc097eb`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 2)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-ci2_z_d_`

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
| 保護 | new | 140 | 153 |
| 保護 | base | 144 | 153 |
| 命中 | new | 71 | 85 |
| 命中 | base | 70 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | fail | fail | Both still flag 可以應付各種狀況 (A as 空話填充, B as 推廣語氣) despite 我認為 marking it as genuine personal appraisal, though both correctly decline the voiceless verdict — A additionally contradicts itself by preserving 第一種比較完美 while flagging the adjacent clause. _(A=new, B=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | fail | fail | Both flag only the closing 反問句 tell; neither flags the 破碎短句 (semicolon juxtaposition, elided premises) in 差在骨幹是誰的話. |
| 7 | flags-slogan-replacing-explanation | 命中 | pass | fail | A flags the 連網一行指令／離線 symlink couplet and asks it be expanded into executable steps; B never flags that span, only the 兩條路 wording. _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | pass | fail | A flags 範圍是開放的，不是固定的 under 對比句式; B files it under 空話填充, missing the named contrast-construction rule. _(A=new, B=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | fail | pass | B flags 兩條路 as 口語化萬能詞 and proposes 兩個方式; A never flags it. _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 會結束，放心壓 as bare assertion; A explicitly protects it as casual cadence and B protects it as direct answer. _(A=new, B=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the unmarked conditional in 之後還要……就別開; both report zero findings. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both wave the whole passage through on casual/voice carve-outs, exactly the cross-rule borrowing this row forbids. |
| 21 | no-prose-collapse-demand | 保護 | pass | fail | A offers 直接把每項寫成完整句 as a fix path pushing away from list form, while B explicitly keeps 條列 and says the topic suits it. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Key requires clean pass-through but both raise 空降主張/情緒宣告 flags on the passage. |
| 60 | preserves-punctuation-hand | 保護 | pass | fail | A rewrites the halfwidth commas and spacing into standard punctuation, B returns the text byte-identical. _(B=new, A=base)_ |
| 60 | 全域:保真 | 保護 | pass | fail | A alters the author's punctuation and spacing hand while B preserves every character. _(B=new, A=base)_ |
| 64 | 全域:保真 | 保護 | fail | fail | A drops SEO entirely from the rewrite and B replaces the SEO-death claim with vague 將面臨這種變化, both losing source content. _(B=new, A=base)_ |
| 64 | 全域:不換湯 | 命中 | fail | pass | B swaps the 死亡 metaphor for the equally contentless 將面臨這種變化, an empty-for-empty trade. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | A offers promote-or-demote as an either/or but never addresses the schedule-as-annotation point, and B likewise mixes options without treating 時程 as an annotation rather than a second label. _(B=new, A=base)_ |
| 68 | fix-picks-one-register | 命中 | fail | pass | A promotes cleanly to a full sentence while B keeps the 執行方式與分工： label bolted onto a full sentence, a hybrid third form. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A passes it via a docs carve-out while B flags 自我背書 and notes 皆來自 vouches for completeness without adding facts. _(B=new, A=base)_ |
| 72 | fix-restores-operative-clause | 命中 | fail | fail | A gives no fix at all, and B only says delete the defensive wording rather than restoring the operative 依前述三個因素判斷如下 clause. _(B=new, A=base)_ |
| 72 | no-disambiguation-confusion | 保護 | pass | fail | A spares the clause as a 判斷範圍說明 carve-out, exactly the disambiguation excuse the row forbids. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | A flags the chain only as 破碎短句堆疊 and mislabels 撐得住 as a catch-all, while B flags only the 所以 conclusion and never marks the unsupported cache-latency premise sentence. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | A asks vaguely for causal conditions without naming hit rate, current latency, or node headroom; B names 流量/資源餘裕/容量門檻 but omits cache hit rate and current response time as the specific gaps. _(B=new, A=base)_ |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | fail | A raises a separate 口語化萬能詞 flag on 目前的架構撐得住 alone, and B folds that sentence into its flagged span as evidence. _(B=new, A=base)_ |
| 80 | flags-missing-connective | 命中 | fail | fail | Neither flags 延長保固，要在購買日起三十天內上網登錄; both declare the passage clean. |
| 80 | fix-restores-the-connective | 命中 | fail | fail | No fix offered by either since neither raised the flag. |
| 32 | expected-direction | 命中 | pass | fail | A names all three residues; B explicitly says the 「以下是清理後的版本，請複製使用」 conversational residue does not hit any rule. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | pass | A flags the closing rhetorical question as a hard defect 反問句開場與收尾 and tells the author to convert it to a declarative; B protects it. _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | pass | A directs rewriting 「你的優勢在哪裡？」 into a declarative statement; B keeps it explicitly. _(A=new, B=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | A alters the source wording — 「真的感覺心理健康很多」 becomes 「心理健康真的好了很多」 and deletes 「爆炸性的」 — beyond any flagged AI-ism; B keeps the text verbatim. _(A=new, B=base)_ |
| 70 | no-weak-signal-stacking | 保護 | fail | pass | A flags 「將多個獨立 AI 能力組合成完整業務流程編排複雜度應遵循漸進式原則」 as 破碎短句堆疊, i.e. flags the sentence the row protects; B raises no such flag. _(A=new, B=base)_ |
| 78 | fix-hedging-opener | 命中 | fail | fail | Both explicitly keep 「值得注意的是」 on a density-threshold argument, so the hedging opener is neither deleted nor rewritten. |
| 78 | fix-empty-process-phrasing | 命中 | fail | pass | A leaves 「採先到先得的方式分配」, retaining the 方式…分配 scaffold; B rewrites to the direct 「依報名先後分配」. _(A=new, B=base)_ |
| 83 | fix-second-person-judgement | 命中 | pass | fail | A rewrites to 「未完成設定時，匯出檔案無法使用」; B declares the clause acceptable and outputs the passage unchanged. _(A=new, B=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | pass | A rewrites the protected 「設定頁往下捲你會看到一個紅色警告」 into 「請在設定頁向下捲動，確認是否顯示紅色警告」, dropping the 你; B keeps it verbatim. _(A=new, B=base)_ |
| 83 | no-fabricated-steps | 保護 | fail | pass | A introduces 「返回匯出頁面」 and a quoted 「匯出」 button name absent from the source; B adds nothing. _(A=new, B=base)_ |
| 83 | 全域:保真 | 保護 | fail | pass | A's rewrite converts 「回來按匯出」 into a named page and quoted button label, drifting from source wording; B is verbatim. _(A=new, B=base)_ |
| 83 | 全域:不代筆 | 保護 | fail | pass | A supplies the return-to-export-page step and button name the source never gave. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 13
- hit-class failures, new arm (comparative 227): 14
- hit-class failures, base arm (comparative 227): 15

NO-SHIP — 13 protection-class false kill(s) on the new arm: 4/metaphor-absence-does-not-flag-solo, 86/does-not-spare-on-casual-register, 47/expected-behavior, 64/全域:保真, 79/no-flag-on-final-short-sentence-alone, 59/expected-behavior, 59/preserves-rhetorical-question, 66/全域:保真, and 5 more


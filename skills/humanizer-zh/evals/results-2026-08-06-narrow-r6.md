# run-case — humanizer-zh — 2026-08-07

- run id: `a75fa162e93f4a7392e3afaad0fdd513`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 3)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-jfh0ztbg`

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
| 保護 | new | 141 | 153 |
| 保護 | base | 141 | 153 |
| 命中 | new | 73 | 85 |
| 命中 | base | 71 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 7 | flags-slogan-replacing-explanation | 命中 | fail | pass | A flags the 連網一行指令／離線 symlink phrase as its own defect with an expand-to-steps fix; B never lists that span as a flag, only alluding to it inside the 兩條路 item. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | fail | Both explicitly release 「範圍是開放的，不是固定的」under the fact-boundary carve-out instead of flagging it. |
| 9 | flags-copula-elision | 命中 | pass | fail | B flags 「這份指南照團隊實際的做法寫」with a restore-the-copula fix; A lists no flag for that span and only mentions the 寫成 repair afterwards in 改了什麼. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | A releases 「會結束，放心壓」as a colloquial self-answer and B explicitly carves out 破碎短句堆疊; neither flags the bare assertion. _(B=new, A=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | Both release the 「…就別開」clause instead of flagging the unmarked conditional that forces a re-read. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note by invoking the declared casual voice as a carve-out, which this rule has no register branch for. |
| 47 | expected-behavior | 保護 | fail | fail | Source expects zero edits, but both flag 空降主張 on the AI-median claim, demanding data or scope limits. |
| 64 | 全域:保真 | 保護 | fail | pass | A is verbatim; B changes 用戶 to 使用者 and drops the second 跟本不讓客戶到你的網站了 sentence-final particle wording plus replaces the concrete 所以就更不可能去你網站了 with a softened 可能性會再降低. _(B=new, A=base)_ |
| 64 | 全域:不換湯 | 命中 | fail | pass | B swaps 所以就 for 因此 and rewrites the conclusion into an equally vague hedged restatement rather than removing emptiness. _(B=new, A=base)_ |
| 67 | flags-register-drift | 命中 | fail | pass | A names the missing predicate and that 取得's object sits before the comma; B flags 語體漂移 but only says 句內主幹不穩定/孤懸動詞 without the cross-comma object evidence. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | fail | pass | A picks promotion to a full sentence with schedule fronted; B offers both options as an either/or without resolving one, and never addresses the schedule-as-second-label issue. _(B=new, A=base)_ |
| 68 | fix-picks-one-register | 命中 | pass | fail | A's rewrite keeps the 執行方式與分工： label plus a full sentence, a hybrid third form; B promotes cleanly to one full sentence. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A explicitly declines to flag it under a docs relaxation; B flags 自我背書 and notes the disambiguation carve-out does not apply. _(B=new, A=base)_ |
| 72 | fix-restores-operative-clause | 命中 | pass | fail | A gives no fix since it did not flag; B directs to state directly which three factors this section judges by, restoring the operative clause. _(B=new, A=base)_ |
| 72 | no-disambiguation-confusion | 保護 | pass | fail | A spares it by claiming the clause explains the section's criteria, effectively the disambiguation reading the row forbids; B rejects that carve-out explicitly. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags the missing-premise chain; A hangs 這件事 and 撐得住 on 口語化萬能詞 and B flags only 撐得住, both explicitly denying any broken-chain finding. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency, or node headroom as the missing premise. |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | fail | Both flag 目前的架構撐得住 on its own, A and B each demanding it be turned into a verifiable load condition. _(B=new, A=base)_ |
| 80 | flags-missing-connective | 命中 | fail | pass | A flags 延長保固，要在購買日起三十天內上網登錄 and describes the re-read needed; B reports no findings at all. _(B=new, A=base)_ |
| 80 | fix-restores-the-connective | 命中 | fail | pass | A supplies 要延長保固，請在購買日起三十天內上網登錄 with the conditional marker restored; B offers no fix. _(B=new, A=base)_ |
| 30 | no-vague-alias-demand | 保護 | fail | pass | A 只給「小美／她」兩個選項，B 另提供「學員」這個角色代稱作為統一選項，等於允許真名被模糊代稱取代。 _(B=new, A=base)_ |
| 32 | expected-direction | 命中 | pass | fail | A 只點名 utm 參數與 citeturn，漏掉「以下是清理後的版本，請複製使用」這處對話殘留；B 三處齊全。 _(B=new, A=base)_ |
| 34 | expected-direction | 命中 | fail | fail | 兩者都只要求各項補具體內容或保留清單，都沒有指向改寫成一段散文。 |
| 35 | expected-direction | 命中 | pass | fail | A 只截取「很多寶貴的啟發」並要求改寫成具體結果，未把第二、四句判為整句空話或指向刪除；B 引出完整兩句並對產業總結句給出刪除方向。 _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | 本案應放行，兩者卻各開三條旗標（模糊歸屬、對讀者說教、反問句收尾），屬誤傷。 |
| 59 | preserves-rhetorical-question | 保護 | fail | fail | A 要求直接說出優勢應建立在哪裡或刪除反問，B 要求改成直述不以問句收尾，兩者都動了結尾反問。 _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | fail | fail | 本案應整段放行，兩者都對「造就了全球無晶圓廠IC設計產業的崛起」開了意義膨脹旗標。 |
| 65 | preserves-typo | 保護 | fail | pass | A 明文保留「逼的」不代改，B 改寫成「只好自己用」抹掉了該筆誤。 _(B=new, A=base)_ |
| 65 | preserves-hyperbole | 保護 | fail | pass | A 原句保留「閃瞎了」，B 換成中性的「白到刺眼」。 _(B=new, A=base)_ |
| 66 | preserves-sentence-final-particle | 保護 | fail | pass | A 保留「都沒有人要下班耶」，B 改成「搞得像沒人需要下班」刪去語尾「耶」。 _(B=new, A=base)_ |
| 81 | no-flag-on-second-sentence | 保護 | pass | fail | A 把「測試機與正式機各一份」標為過度簡寫，B 明說第二句關係清楚未標記。 _(B=new, A=base)_ |
| 83 | fix-second-person-judgement | 命中 | pass | fail | A 完全沒有輸出案例 83；B 把「你匯出來的東西根本沒辦法用」改成「匯出結果無法使用」。 _(B=new, A=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | fail | A 無此案例輸出；B 把「設定頁往下捲你會看到一個紅色警告」重寫成「請在設定頁向下捲動，看到紅色警告時」，刪掉了應原樣保留的程序性第二人稱。 _(B=new, A=base)_ |
| 83 | no-fabricated-steps | 保護 | pass | fail | A 未交付此案例；B 未添加原文沒有的欄位、按鈕或步驟。 _(B=new, A=base)_ |
| 83 | 全域:保真 | 保護 | pass | fail | A 未交付此案例；B 的欄位對照表、紅色警告、匯出等詞完整。 _(B=new, A=base)_ |
| 83 | 全域:不換湯 | 命中 | pass | fail | A 未交付此案例；B 刪「根本沒辦法用」改為直述，未換同族空話。 _(B=new, A=base)_ |
| 83 | 全域:不代筆 | 保護 | pass | fail | A 未交付此案例；B 沒有捏造原文未提供的操作或主張。 _(B=new, A=base)_ |

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

- protection-class failures, new arm (absolute 238): 12
- hit-class failures, new arm (comparative 227): 12
- hit-class failures, base arm (comparative 227): 14

NO-SHIP — 12 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 64/全域:保真, 79/no-flag-on-final-short-sentence-alone, 30/no-vague-alias-demand, 59/expected-behavior, 59/preserves-rhetorical-question, 62/expected-behavior, and 4 more


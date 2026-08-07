# run-case — humanizer-zh — 2026-08-06

- run id: `b3d593e4612b4cc4ae2a5925dd0d3ab7`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 4)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-loy6i1xd`

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
| 保護 | new | 139 | 153 |
| 保護 | base | 144 | 153 |
| 命中 | new | 72 | 85 |
| 命中 | base | 74 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags only the rhetorical-question ending; B additionally flags the premise-less opener 「差在骨幹是誰的話」. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A flags 「範圍是開放的，不是固定的」 as 對比句式; B declares the carve-out applies and does not flag it. _(B=new, A=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | pass | fail | B flags 「兩條路」 as 口語化萬能詞; A never mentions it. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | A issues no marks; B explicitly rules 破碎短句堆疊 不成立, so neither flags 「會結束，放心壓」. _(B=new, A=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the unmarked conditional ending in 「就別開」; B claims 「就」 already marks it. _(B=new, A=base)_ |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note by invoking the casual voice profile as grounds for retention. |
| 21 | expected-direction | 命中 | pass | fail | A flags the bold-label self-restatement; B explicitly excuses the bold labels and never breaks the three-fold 「透過X達成Y」 parallel. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Both flag 空降主張 on a passage the key says should pass untouched, and B adds an author-invisibility finding on top. _(A=new, B=base)_ |
| 60 | preserves-punctuation-hand | 保護 | pass | fail | B normalizes half-width commas, removes the stray spaces, and adds sentence-final periods; A returns punctuation untouched. _(A=new, B=base)_ |
| 60 | 全域:保真 | 保護 | pass | fail | B alters the author's spacing/punctuation surface and rephrases 誰去阻止他們不要亂按 into 誰來阻止他們?, dropping 不要亂按. _(A=new, B=base)_ |
| 64 | 全域:保真 | 保護 | fail | fail | A downgrades 「SEO 的死亡」 to 「SEO 可能走向死亡」, softening the author's stated claim; B rewrites 用戶 to 使用者 and drops 更方便地 from the Mini APP claim, altering wording the source supplied. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | A offers promote-or-demote but never says the schedule should become an annotation rather than a second label端; B's fix only patches in 預計於 or a label-plus-parenthesis form without picking a single register or addressing the schedule's parallel status. _(A=new, B=base)_ |
| 72 | flags-self-vouching | 命中 | fail | pass | A passes the clause under a disambiguation/docs carve-out instead of flagging; B flags 自我背書 and notes the clause vouches for completeness rather than carrying new fact. _(A=new, B=base)_ |
| 72 | fix-restores-operative-clause | 命中 | fail | pass | A gives no fix at all; B supplies 「灰色地帶案例依前述三項因素判斷如下」, moving the subject back to the act of judging. _(A=new, B=base)_ |
| 72 | no-disambiguation-confusion | 保護 | fail | pass | A spares it precisely on the 消歧義 carve-out the key forbids here; B does not. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | A flags the passage only as 破碎短句堆疊 plus an unsupported-claim note, not a missing-premise inference break; B explicitly declines to flag it, saying 所以 already marks causality and premises are given. _(A=new, B=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names 命中率, current latency, or node headroom as the missing premise; A says only to link the causal chain, B addresses only the final sentence's load figures. _(A=new, B=base)_ |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | fail | Both hang a flag on 「目前的架構撐得住」 on its own — A as 抽象claim缺交付, B as 口語化萬能詞. _(A=new, B=base)_ |
| 80 | flags-missing-connective | 命中 | fail | fail | Both declare the passage clean and explicitly excuse 「延長保固,要在……」 as a natural topic-comment sentence. |
| 80 | fix-restores-the-connective | 命中 | fail | fail | Neither offers any fix, so no conditional marker is restored. |
| 30 | no-vague-alias-demand | 保護 | fail | pass | A names 小美/她 only; B offers 「或同一個角色稱呼」, i.e. a role alias, and lists 保護清單：無. _(B=new, A=base)_ |
| 32 | expected-direction | 命中 | fail | pass | A names utm param, citeturn placeholder and the 「以下是清理後的版本，請複製使用」 chat residue; B omits the dialogue residue. _(B=new, A=base)_ |
| 39 | preserves-letter-specifics | 保護 | fail | pass | A protects the forwarding/study-order details; B's protection list for this case is about 叫「爸」/收書包, content absent from this source, so the letter specifics are not protected. _(B=new, A=base)_ |
| 58 | preserves-quota-figure | 保護 | fail | pass | A keeps the 100-call figure intact; B's fix direction 「若沒有查核，刪除定價主張」 puts the quota figure up for deletion. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | pass | A passes the passage; B raises 模糊歸屬, 對讀者說教 and 反問句 flags on argued assertions. _(B=new, A=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | pass | B tells the author to replace the closing question with a direct statement of where advantage comes from. _(B=new, A=base)_ |
| 65 | preserves-typo | 保護 | pass | fail | A corrects 「逼的」 to 「逼得」 and says so; B leaves it. _(B=new, A=base)_ |
| 70 | no-weak-signal-stacking | 保護 | fail | pass | B tags 「將多個獨立 AI 能力組合成…」 as 語體漂移, the exact flag this row forbids; A uses a different rule. _(B=new, A=base)_ |
| 81 | flags-dangling-copular-frame | 命中 | fail | pass | A flags the first sentence and asks for the frame to be restored; B reports 未發現須修改之處. _(B=new, A=base)_ |
| 81 | flags-under-fragmented-clause-rule | 命中 | fail | fail | A files it under 過度簡寫 and explicitly declines 破碎短句堆疊; B files no flag at all. _(B=new, A=base)_ |
| 83 | preserves-procedural-second-person | 保護 | pass | fail | A rewrites the sentence to 「向下捲動設定頁，看到紅色警告…」, stripping the protected procedural 你; B keeps it verbatim. _(B=new, A=base)_ |
| 83 | no-fabricated-steps | 保護 | pass | fail | A adds 「返回設定頁」, a UI location the source never states; B adds nothing. _(B=new, A=base)_ |
| 84 | preserves-concrete-facts | 保護 | fail | pass | A keeps 三道簽核併成一道 and 下週的說明會 verbatim; B's 完整輸出 is the case-78 sign-up text and its corrected line reworks 下週的說明會 into 說明會下週再談細節. _(B=new, A=base)_ |
| 84 | 全域:保真 | 保護 | fail | pass | B delivers another case's paragraph as this case's output, losing every fact of the source; A reproduces them. _(B=new, A=base)_ |
| 84 | 全域:不代筆 | 保護 | fail | pass | B's output asserts 報名截止/名額分配 content that this source never contains. _(B=new, A=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 14
- hit-class failures, new arm (comparative 227): 13
- hit-class failures, base arm (comparative 227): 11

NO-SHIP — 14 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 64/全域:保真, 72/no-disambiguation-confusion, 79/no-flag-on-final-short-sentence-alone, 30/no-vague-alias-demand, 39/preserves-letter-specifics, 58/preserves-quota-figure, and 6 more; hit-class regressed: new arm 13 failure(s) vs baseline 11 (comparative denominator)


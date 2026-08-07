# run-case — humanizer-zh — 2026-08-06

- run id: `2ad9cd4f899347d988726ae636a4f30f`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 1)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-_zuxqupb`

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
| 保護 | new | 142 | 153 |
| 保護 | base | 146 | 153 |
| 命中 | new | 70 | 85 |
| 命中 | base | 75 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | fail | fail | A flags the rhetorical-question ending but never the fragmented semicolon clauses; B flags neither, folding the ending into 對讀者說教. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A flags 「範圍是開放的，不是固定的」 and asks what is in/out of scope; B applies a carve-out and explicitly declines to flag it. _(B=new, A=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | pass | fail | B flags 「兩條路」 and proposes 「兩個方式」; A never touches that phrase. _(B=new, A=base)_ |
| 9 | flags-bare-verb | 命中 | pass | fail | B restores subject and object (「不會把它誤判成需要改寫的詞」); A turns it into an imperative 「請勿誤改」 aimed at the reader, leaving the object unrestored. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | A reports no findings; B explicitly declares 「會結束，放心壓」 deliberate rhythm rather than a bare assertion. _(B=new, A=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the 就別開 sentence; B affirmatively calls it clear-conditioned. _(B=new, A=base)_ |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | A clears the paragraph via casual carve-outs, B via the casual voice profile; both exempt the whole passage on register. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Source should pass untouched, but both flag 空降主張 and 情緒宣告 on the author's own newsletter observations. |
| 64 | 全域:保真 | 保護 | fail | pass | A changes the author's 「SEO 的死亡」 to 「SEO 的變化」, altering the source's actual wording and force; B keeps it. _(A=new, B=base)_ |
| 67 | flags-register-drift | 命中 | fail | pass | A names 語體漂移 but gives no syntactic evidence beyond quoting; B cites the label-before-colon, 取得 reaching back across the comma, and missing sentence frame. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | A offers a full-sentence-or-tag either/or but never says the schedule should be a note rather than a second label端; B offers two options and likewise omits the schedule-as-annotation point. _(A=new, B=base)_ |
| 68 | flags-register-drift | 命中 | fail | pass | A labels 語體漂移 with only 'noun phrase before postposed verb' and no cross-comma/no-marker analysis; B states label-plus-sentence conflation and that 確認 must reclaim its object. _(A=new, B=base)_ |
| 68 | fix-picks-one-register | 命中 | fail | pass | A keeps the 「執行方式與分工：」 tag and then appends a full sentence, producing the mixed third form; B promotes cleanly to a single complete sentence. _(A=new, B=base)_ |
| 72 | flags-self-vouching | 命中 | fail | pass | A spares the clause under a disambiguation carve-out; B flags 自我背書 and notes the clause adds no new fact but vouches for completeness and sourcing. _(A=new, B=base)_ |
| 72 | fix-restores-operative-clause | 命中 | fail | pass | A gives no fix at all; B directs to stating how the gray cases are judged by the three factors, restoring the operative act rather than only deleting. _(A=new, B=base)_ |
| 72 | no-disambiguation-confusion | 保護 | fail | pass | A spares the clause precisely by invoking a nonexistent disambiguation need; B notes no competing criterion is present. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags the cache/latency claim or the 所以擴充節點可以往後延 conclusion; both only flag 撐得住 and explicitly deny any inter-sentence problem. |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency, or node headroom as the missing premise. |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | fail | Both flag 目前的架構撐得住 on its own as the sole finding, which is exactly the standalone short sentence the row protects. |
| 80 | flags-missing-connective | 命中 | fail | fail | Both explicitly pass 延長保固，要在購買日起三十天內上網登錄 as a normal doc topic frame instead of flagging it. |
| 80 | fix-restores-the-connective | 命中 | fail | fail | Neither proposes restoring a conditional marker such as 如果要延長保固, since neither flagged the clause. |
| 32 | expected-direction | 命中 | fail | pass | A names utm, citeturn placeholder and the chat residue; B explicitly says 「以下是清理後的版本，請複製使用」 does not constitute a flag. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | Both flag 對讀者說教 on the argued assertion; A additionally flags the closing rhetorical question. _(B=new, A=base)_ |
| 59 | preserves-rhetorical-question | 保護 | pass | fail | A flags the closing question as 反問句開場與收尾 and asks for a direct statement; B protects it under a carve-out. _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | fail | pass | A passes the段 clean; B raises a P1 意義膨脹 flag on the 商業模式造就…崛起 sentence, a false positive on the annual-report statement. _(B=new, A=base)_ |
| 62 | preserves-figures | 保護 | pass | fail | A restates the count as 12,302, dropping the source's 1萬2,302 Chinese-unit form; B reproduces 1 萬 2,302. _(B=new, A=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | B alters the source wording to 「每天都有新的東西出來」, dropping 爆炸性 from the retained body text. _(B=new, A=base)_ |
| 70 | no-weak-signal-stacking | 保護 | fail | pass | B flags 「將多個獨立 AI 能力組合成…」 under 破碎短句堆疊, hitting the sentence the row protects. _(B=new, A=base)_ |
| 75 | no-self-vouching-false-positive | 保護 | pass | fail | A raises a P1 自我背書 flag on the sentence; B explicitly rules it out. _(B=new, A=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | pass | B rewrites 「設定頁往下捲你會看到一個紅色警告」 into 「往下捲動設定頁，看到紅色警告時」, stripping the protected procedural 你; A keeps it verbatim. _(B=new, A=base)_ |
| 83 | 全域:保真 | 保護 | fail | pass | B restructures protected sentences (設定頁 clause, 存好之後你再回來按匯出) beyond the flagged 東西 span; A alters only that span. _(B=new, A=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 11
- hit-class failures, new arm (comparative 227): 15
- hit-class failures, base arm (comparative 227): 10

NO-SHIP — 11 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 64/全域:保真, 72/no-disambiguation-confusion, 79/no-flag-on-final-short-sentence-alone, 59/expected-behavior, 62/expected-behavior, 66/全域:保真, and 3 more; hit-class regressed: new arm 15 failure(s) vs baseline 10 (comparative denominator)


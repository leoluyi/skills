# run-case — humanizer-zh — 2026-08-06

- run id: `4c096c96918347b4a21d5789846651b4`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 6)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-1u56fhv7`

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
| 保護 | base | 147 | 153 |
| 命中 | new | 73 | 85 |
| 命中 | base | 74 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | pass | fail | A judges the piece clean of author-hiding and leaves the stance alone, while B flags the author's own judgment 「第一種比較完美」 as 推廣語氣, hitting a real voice marker. _(A=new, B=base)_ |
| 5 | flags-second-person-coaching | 命中 | fail | pass | A rules the 「你」 sentences legitimate criteria and flags nothing; B marks 對讀者說教 on exactly those spans. _(A=new, B=base)_ |
| 5 | fix-converts-to-exposition | 命中 | fail | pass | A offers no fix direction; B directs the subject to 作者／文件撰寫者 in third person. _(A=new, B=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | fail | fail | A flags neither tell; B flags only the closing rhetorical question and explicitly declines the fragmented-clause signal. _(A=new, B=base)_ |
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | fail | pass | A silently keeps a hollow residue 「這是需要面對的事實。」 instead of a flag marker; B emits an explicit 無實質內容 marker without inventing content. _(A=new, B=base)_ |
| 7 | flags-slogan-replacing-explanation | 命中 | pass | fail | A flags the colon list as slogan-for-explanation with a fix to spell out steps; B never flags that span, only alludes to it inside another item's fix. _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | pass | fail | A marks 「開放的，不是固定的」 as 對比句式; B waives it under a fact-boundary carve-out. _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」 as a bare assertion; both protect it as casual voice. |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither marks the unmarked conditional before 「就別開」; A calls it clear operational advice, B says nothing. _(A=new, B=base)_ |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note on casual-register grounds, borrowing a carve-out that belongs to another rule. |
| 47 | expected-behavior | 保護 | pass | fail | A passes the paragraph clean while B raises three flags (對比句式, 空降主張, 情緒宣告) on a passage meant to go untouched. _(A=new, B=base)_ |
| 67 | flags-register-drift | 命中 | pass | fail | A flags 語體漂移 and names the syntax (noun phrase front half, verb reaching back across the comma, no licensing marker); B flags the label but supplies no syntactic evidence. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | Neither says the schedule belongs in a note rather than as a second label end. |
| 72 | flags-self-vouching | 命中 | fail | pass | A reports nothing to flag while B flags 自我背書 and points at the 皆來自 completeness claim. _(A=new, B=base)_ |
| 72 | fix-restores-operative-clause | 命中 | fail | pass | A offers no fix; B directs the sentence back to the act of judging by the three factors. _(A=new, B=base)_ |
| 72 | no-disambiguation-confusion | 保護 | fail | pass | A spares the clause precisely on a 消歧義 carve-out that does not apply here; B does not. _(A=new, B=base)_ |
| 77 | flags-undeclared-catch-all-phrase | 命中 | fail | pass | A explicitly spares 兩條路 while B flags it as 口語化萬能詞 outside the declared metaphor. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags the missing-premise leap in the cache/latency and 所以 sentences. |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency or node headroom as the missing premise. |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | pass | A flags 目前的架構撐得住 on its own as a defect; B explicitly spares it. _(A=new, B=base)_ |
| 80 | flags-missing-connective | 命中 | pass | fail | A flags the bare purpose phrase and explains the re-read; B declares 要在 sufficient and flags nothing. _(A=new, B=base)_ |
| 80 | fix-restores-the-connective | 命中 | pass | fail | A restores 如果要延長保固，請在…登錄; B offers no fix. _(A=new, B=base)_ |
| 34 | expected-direction | 命中 | fail | pass | A explicitly rules out the list rule and keeps the numbered structure; B directs to rewrite into a causal prose passage. _(A=new, B=base)_ |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A protects the second sentence outright; B protects it in the carve-out but then flags 作者隱身 citing '只有分享宣告' with no concrete detail, treating that very sentence as deficient. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | pass | A flags 模糊歸屬, 對讀者說教 and the closing rhetorical question; B passes the whole passage. _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | pass | A tells the author to convert the closing question into a statement or supply an answer; B keeps it. _(A=new, B=base)_ |
| 62 | expected-behavior | 保護 | fail | pass | A flags 意義膨脹 on 造就了全球無晶圓廠 IC 設計產業的崛起 and demands rewrite; B passes the whole paragraph. _(A=new, B=base)_ |
| 62 | preserves-figures | 保護 | fail | pass | A restates the count as '12,302 種產品', dropping the original 1萬2,302 Chinese-unit form; B preserves 1 萬 2,302. _(A=new, B=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | A rewrites 「真的感覺心理健康很多」 to 「心理健康真的好很多」 and invents 「這週又開始追新東西，壓力回來了」, a clause not in the source; B keeps the retained sentences verbatim. _(A=new, B=base)_ |
| 66 | 全域:不代筆 | 保護 | fail | pass | A adds 「又開始追新東西」, an activity the source never states; B adds nothing. _(A=new, B=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | fail | Both strip 你 from 「設定頁往下捲你會看到一個紅色警告」 in the rewrite despite naming it protected. |
| 84 | no-stacked-contrast-frames | 保護 | pass | fail | A leaves zero contrast frames; B keeps 「不只換介面，也重做了」 and then bolts on a redundant 「這次改版重寫了報帳流程」, restating the same turn twice. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 11
- hit-class failures, new arm (comparative 227): 12
- hit-class failures, base arm (comparative 227): 11

NO-SHIP — 11 protection-class false kill(s) on the new arm: 6/hollow-paragraph-flagged-not-fabricated, 86/does-not-spare-on-casual-register, 72/no-disambiguation-confusion, 79/no-flag-on-final-short-sentence-alone, 59/expected-behavior, 59/preserves-rhetorical-question, 62/expected-behavior, 62/preserves-figures, and 3 more; hit-class regressed: new arm 12 failure(s) vs baseline 11 (comparative denominator)


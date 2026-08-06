# run-case — humanizer-zh — 2026-08-06

- run id: `cce8860845f24a8aa0490275b338f165`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 3)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-rm4neqm6`

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
| 保護 | new | 147 | 153 |
| 保護 | base | 142 | 153 |
| 命中 | new | 76 | 85 |
| 命中 | base | 72 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A flags both the premise-less opening fragment and the closing rhetorical question; B explicitly declines the fragment and treats the closer only as coaching tone. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | pass | fail | A releases 「範圍是開放的，不是固定的」 under the fact-boundary carve-out; B flags it as 對比句式. _(B=new, A=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | fail | pass | A names 「兩條路」 as 口語化萬能詞; B never singles it out, folding the sentence into a slogan flag. _(B=new, A=base)_ |
| 9 | flags-copula-elision | 命中 | pass | fail | A lists only one flag (bare verb) and merely mentions the added 寫成 in its change note without flagging the dangling frame; B flags the span and restores 「是…寫成的」. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」 as a premise-less bare assertion; both release it. |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the unmarked conditional ending in 「…就別開」; both treat it as acceptable casual instruction. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note by invoking a casual voice/register carve-out that this rule does not have. |
| 21 | expected-direction | 命中 | pass | fail | A explicitly clears the bold labels and never names the parallel 透過X達成Y pattern, only vagueness; B flags the bold-label overuse directly. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | A flags 空降主張; B flags three items including 情緒宣告 and 抽象claim缺交付, so neither passes the paragraph clean. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | fail | pass | A commits to a single promoted sentence with the schedule folded in as an adverbial; B offers both promote-or-demote without resolving the schedule's placement. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | fail | fail | Both report no flags and clear the clause under a docs carve-out. |
| 72 | fix-restores-operative-clause | 命中 | fail | fail | Neither offers any fix direction since neither flagged the sentence. |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | A flags only catch-all wording and B reports no flags; neither identifies the missing-premise conclusions. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency or node headroom as the omitted premise. |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | pass | fail | A flags 目前的架構撐得住 on its own as 口語化萬能詞; B explicitly leaves it alone. _(B=new, A=base)_ |
| 30 | no-vague-alias-demand | 保護 | fail | pass | A offers 「或同一個角色稱呼」 as an accepted alternative to the real name, i.e. a consistent vague alias; B only offers keeping one name or 她. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | pass | fail | A names utm parameter, citeturn placeholder and the conversational 「以下是清理後的版本，請複製使用」; B names only the first two and never flags the chat residue. _(A=new, B=base)_ |
| 34 | expected-direction | 命中 | pass | fail | A points to 「改成一段有推論順序的說明」 (prose); B only asks each item be made concrete, never pointing to a single prose paragraph. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | The row calls for release, but A flags 模糊歸屬 on 「大家常常在問」 and B flags that plus 對讀者說教 and the closing rhetorical question. _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | pass | fail | A explicitly keeps 「你的優勢在哪裡？」; B flags it and tells the author to state the answer or delete the question. _(A=new, B=base)_ |
| 62 | expected-behavior | 保護 | pass | fail | A releases the passage entirely; B raises a 意義膨脹 flag on the industry-rise sentence instead of releasing. _(A=new, B=base)_ |
| 75 | no-self-vouching-false-positive | 保護 | fail | pass | A flags the sentence as 自我背書; B releases it under the disambiguation carve-out. _(A=new, B=base)_ |
| 81 | no-flag-on-second-sentence | 保護 | pass | fail | A explicitly releases the second sentence; B flags 「測試機與正式機各一份」 under 過度簡寫. _(A=new, B=base)_ |
| 83 | fix-second-person-judgement | 命中 | pass | fail | A rewrites to 「否則匯出結果無法使用」; B produced no output for this case at all. _(A=new, B=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | fail | A strips the 你 and rewords to 「設定頁往下捲動後，會看到紅色警告」 instead of leaving the procedural line intact; B delivered nothing to verify. _(A=new, B=base)_ |
| 83 | no-fabricated-steps | 保護 | pass | fail | A adds no new fields or buttons beyond the source's 匯出; B has no output for the case. _(A=new, B=base)_ |
| 83 | 全域:保真 | 保護 | pass | fail | A keeps the 欄位對照表, red warning and export step accurate; B skipped the case entirely. _(A=new, B=base)_ |
| 83 | 全域:不換湯 | 命中 | pass | fail | A deletes 「就可以了」 without substituting another filler; B produced nothing. _(A=new, B=base)_ |
| 83 | 全域:不代筆 | 保護 | pass | fail | A invents no procedure; B has no output to assess. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 6
- hit-class failures, new arm (comparative 227): 9
- hit-class failures, base arm (comparative 227): 13

NO-SHIP — 6 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 30/no-vague-alias-demand, 59/expected-behavior, 75/no-self-vouching-false-positive, 83/preserves-procedural-second-person


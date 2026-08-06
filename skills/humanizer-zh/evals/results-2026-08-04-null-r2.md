# run-case — humanizer-zh — 2026-08-05

- run id: `071d8c40aae74ee789dc72108c3f1fd4`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-33pp3x2n`

## Chunks

| chunk | range | cases | ids | rows |
|---|---|---|---|---|
| 0 | [1, 9] | 9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 39 |
| 1 | [10, 86] | 10 | 10, 11, 12, 13, 14, 15, 16, 18, 19, 86 | 23 |
| 2 | [20, 85] | 15 | 20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 67, 72, 76, 79, 85 | 29 |
| 3 | [25, 80] | 17 | 25, 26, 27, 28, 29, 45, 46, 47, 55, 60, 61, 64, 68, 71, 73, 77, 80 | 51 |
| 4 | [30, 83] | 18 | 30, 31, 32, 33, 34, 48, 49, 50, 51, 56, 62, 63, 65, 69, 74, 78, 81, 83 | 53 |
| 5 | [35, 84] | 16 | 35, 36, 37, 38, 39, 52, 53, 54, 57, 58, 59, 66, 70, 75, 82, 84 | 43 |

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
| 保護 | new | 148 | 153 |
| 保護 | base | 144 | 153 |
| 命中 | new | 74 | 85 |
| 命中 | base | 72 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | fail | fail | Neither judges the passage clean: A flags the first-person stance 「我認為第一種比較完美」 as 空降主張, and B additionally misfires on 「地雷」 and 「記得」. _(A=new, B=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | fail | fail | A flags the missing-premise opener but explicitly declines to flag the closing rhetorical question; B flags the closing question but never flags the fragmented/semicolon syntax. _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A explicitly keeps 「範圍是開放的，不是固定的」 as a genuine boundary; B flags it as an empty parallel binary with the undefined-scope reasoning. _(A=new, B=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | fail | pass | A never addresses 「兩條路」; B flags it as 口語化萬能詞 and proposes 「兩種方式」. _(A=new, B=base)_ |
| 10 | flags-rhythm-metaphor | 命中 | pass | fail | B flags 開發節奏 under 慣用詞 with fix pointing to 期程/排程/頻率; A folds it into the idiom flag without naming the rhythm-metaphor rule. _(B=new, A=base)_ |
| 18 | expected-direction | 命中 | pass | fail | B keeps one contrast and reclassifies the third as slogan, giving direct-statement rewrites; A flags all three uniformly as 對比句式 without indicating at most one may stay. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 會結束，放心壓 as bare assertion; both explicitly excuse it. |
| 86 | flags-missing-connective | 命中 | fail | fail | Both treat the 就別開 clause as adequately marked and decline to flag the missing conditional connective. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole passage on casual-voice grounds, exactly the register-based pass this row forbids. |
| 22 | expected-direction | 命中 | pass | fail | A allows keeping 一至兩個 emoji, above the 0-1 bar; B keeps at most one and both ask for concrete update info. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | pass | fail | A's two options never place 時程 as an annotation rather than a second label; B offers 升格成句 or label plus parenthetical schedule. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A dismisses 自我背書 under a docs carve-out; B flags 皆來自 as vouching for completeness with no new fact. _(B=new, A=base)_ |
| 72 | fix-restores-operative-clause | 命中 | pass | fail | A offers no fix at all; B redirects to stating how the three factors are applied to the cases below. _(B=new, A=base)_ |
| 72 | no-disambiguation-confusion | 保護 | pass | fail | A explicitly clears the clause as having 導讀與消歧義功能; B refuses that excuse. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | pass | A flags the cache-latency claim and the deferral conclusion as unsupported; B declares 所以 sufficient and flags only 撐得住. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | pass | A names latency range, baseline, CPU/connections/IOPS and the deferral threshold; B gives no fix for the chain. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Source should pass untouched, but A raises three P1 flags and B raises three P1 flags including 情緒宣告 on 令人錯愕. _(B=new, A=base)_ |
| 60 | preserves-punctuation-hand | 保護 | pass | fail | A normalizes half-width commas, removes the stray spaces and adds full stops plus a question mark; B leaves punctuation untouched. _(B=new, A=base)_ |
| 60 | 全域:保真 | 保護 | pass | fail | A alters the author's punctuation and changes 不要亂按 to 別再亂按; B reproduces the source exactly. _(B=new, A=base)_ |
| 80 | flags-missing-connective | 命中 | fail | fail | A reports no findings; B explicitly declines to flag the clause as any defect. _(B=new, A=base)_ |
| 80 | fix-restores-the-connective | 命中 | fail | fail | Neither proposes restoring a conditional marker such as 如果要延長保固. |
| 32 | expected-direction | 命中 | fail | fail | Both flag utm and citeturn but neither names 「以下是清理後的版本，請複製使用」as chat residue; A explicitly declines it and B flags an unrelated claim instead. _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | pass | fail | A raises a P1 意義膨脹 flag on 「造就了全球無晶圓廠IC設計產業的崛起」instead of passing the paragraph; B flags nothing. _(B=new, A=base)_ |
| 78 | fix-hedging-opener | 命中 | pass | fail | A keeps 「值得注意的是」in the output on a stacking-threshold argument; B deletes it. _(B=new, A=base)_ |
| 36 | expected-direction | 命中 | fail | pass | A only offers deleting the column or swapping in comparable columns, never prose; B explicitly says 改寫成一段直接陳述. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | Both flag the passage instead of clearing it, including treating the closing rhetorical question as a defect for lacking an answer. |
| 59 | preserves-rhetorical-question | 保護 | fail | fail | A directs 改成直接陳述優勢來源 and B 改成作者明確主張，或補入具體的優勢來源 — both demand the forbidden rewrite/answer. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 5
- hit-class failures, new arm (comparative 227): 11
- hit-class failures, base arm (comparative 227): 13

NO-SHIP — 5 protection-class false kill(s) on the new arm: 4/metaphor-absence-does-not-flag-solo, 86/does-not-spare-on-casual-register, 47/expected-behavior, 59/expected-behavior, 59/preserves-rhetorical-question


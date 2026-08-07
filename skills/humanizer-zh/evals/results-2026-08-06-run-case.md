# run-case — humanizer-zh — 2026-08-06

- run id: `cfa483dd2e9e4fcc82f4bbbf73f9ec63`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 5)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-3gg2h5_2`

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
| 保護 | base | 146 | 153 |
| 命中 | new | 68 | 85 |
| 命中 | base | 77 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 4 | metaphor-absence-does-not-flag-solo | 保護 | fail | pass | Both decline 作者隱身, but B additionally flags 破折號濫用 on the dash carrying the 13-年前 personal recollection, hitting a real voice marker. _(B=new, A=base)_ |
| 5 | flags-second-person-coaching | 命中 | fail | pass | A flags 對讀者說教 across the 你 sentences; B explicitly rules the same spans not coaching. _(B=new, A=base)_ |
| 5 | fix-converts-to-exposition | 命中 | fail | pass | A directs 你 back to 文件/作者/內容來源 in third person; B offers no such fix since it denied the flag. _(B=new, A=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A marks the premise-less opening fragment and directs the rhetorical closing to become declarative; B denies both the fragment and the closing. _(B=new, A=base)_ |
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | pass | fail | A invents 「測試目標往往已經確定，只是沒有先說清楚」to fill paragraph B; B leaves an explicit marker line. _(B=new, A=base)_ |
| 6 | 全域:不代筆 | 保護 | pass | fail | A ghostwrites a claim the source never made for paragraph B; B refuses and hands back a flag. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | fail | Both preserve 「範圍是開放的，不是固定的」under a fact-boundary carve-out that the key says does not apply. |
| 16 | no-cta-weakening-demand | 保護 | pass | fail | A flags 「帶領你」as coaching and demands the second-person address be swapped out, weakening the CTA; B critiques the missing substance only. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」; both explicitly excuse it as casual voice. |
| 86 | flags-missing-connective | 命中 | fail | fail | Both declare the 「…就別開」clause clear and flag nothing. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole passage by invoking the casual register/voice protection list. |
| 21 | expected-direction | 命中 | pass | fail | A tells the author to drop the bold labels; B explicitly spares the bold via a docs carve-out and never names the uniform 透過X達成Y parallel. _(A=new, B=base)_ |
| 22 | expected-direction | 命中 | fail | pass | A only cuts emoji and never asks for the missing concrete update content; B cuts the stacking and flags 超有感/回不去 demanding actual features and verifiable results. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | The passage should go through untouched, but A raises 空降主張 plus 情緒宣告 and B raises 空降主張. _(A=new, B=base)_ |
| 60 | preserves-punctuation-hand | 保護 | fail | pass | A converts the half-width commas and stray spaces to full-width punctuation and adds sentence-final periods; B returns the line byte-identical. _(A=new, B=base)_ |
| 67 | flags-register-drift | 命中 | fail | pass | A labels 語體漂移 but gives no syntactic evidence; B states the object of 取得 sits before the comma and the front label forms no complete clause. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | Neither report says the schedule belongs in a note rather than as a second label端, so the fix is incomplete on both sides. |
| 68 | flags-register-drift | 命中 | fail | pass | A names the rule but supplies no clause-level evidence; B points to 確認 needing to govern a complete object as the drift evidence. _(A=new, B=base)_ |
| 68 | facts-preserved-verbatim | 保護 | fail | pass | A adds 及分工 to the payload; B carries 跨部門工作小組, 外部顧問, 協作機制, 第一次會議 and 兩週 with nothing added or dropped. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | pass | A explicitly rules the chain sound and flags only 撐得住; B flags the cache/pressure/deferral chain as requiring re-reading to recover causality. _(A=new, B=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names hit rate, current latency or node headroom as the unstated premise; B only asks to merge the clauses into one causal sentence. _(A=new, B=base)_ |
| 80 | flags-missing-connective | 命中 | fail | pass | A returns no flags and calls 延長保固 a legitimate topic phrase; B flags exactly that clause for its unmarked condition relation. _(A=new, B=base)_ |
| 80 | fix-restores-the-connective | 命中 | fail | pass | A offers no fix; B supplies 如要延長保固，請於購買日起三十天內上網登錄 rather than shortening or bulleting. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | fail | pass | A names utm, citeturn token and the conversational residue; B explicitly declines to flag 「以下是清理後的版本，請複製使用」. _(B=new, A=base)_ |
| 34 | flags-abstract-noun-stacking | 命中 | fail | pass | A names the stacked abstractions and asks which platforms/what data to track; B only says 'add concrete measures' without naming the abstract-noun stacking specifics. _(B=new, A=base)_ |
| 57 | preserves-key-figures | 保護 | fail | pass | B additionally flags the em dash carrying the conclusion clause and tells the author to swap punctuation/split the sentence, touching the protected conclusion text. _(B=new, A=base)_ |
| 58 | preserves-quota-figure | 保護 | pass | fail | A offers to delete the unverified pricing info, putting the 100-calls figure on the chopping block; B explicitly preserves it. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | pass | B flags 對讀者說教 and 反問句 on an argued passage, exactly the false positive the row guards. _(B=new, A=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | pass | B tells the author to convert the closing rhetorical question into a statement. _(B=new, A=base)_ |
| 62 | preserves-figures | 保護 | fail | pass | B restates the count as 12,302, dropping the source's 1萬2,302 Chinese-unit form. _(B=new, A=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | B alters facts and wording: 「本週」 to 「這週」, 「真的感覺」 to 「反而覺得」, drops 「爆炸性」 and the 「都」 in 都沒有人要下班. _(B=new, A=base)_ |
| 69 | does-not-rewrite-in-detect | 保護 | fail | pass | B supplies replacement text 「整理資料並建立客戶標籤」 and a rewritten sentence for the 決策分析引擎 clause, rewriting field content in detect mode. _(B=new, A=base)_ |
| 70 | no-weak-signal-stacking | 保護 | fail | pass | B flags the 「將多個獨立 AI 能力組合成…」 sentence under 破碎短句堆疊, the very construction the row excludes as an authorised marker. _(B=new, A=base)_ |
| 78 | fix-empty-process-phrasing | 命中 | pass | fail | A keeps 「將依先到先得的方式分配」, retaining the empty 方式 scaffold; B writes the direct 「依填表順序分配」. _(B=new, A=base)_ |
| 78 | 全域:不換湯 | 命中 | pass | fail | A's 「採取…方式進行分配」 becomes 「依…的方式分配」, same empty family; B breaks out of it. _(B=new, A=base)_ |
| 81 | no-flag-on-second-sentence | 保護 | pass | fail | A flags 「測試機與正式機各一份」 as 過度簡寫 and demands the object be restored; B explicitly clears it. _(B=new, A=base)_ |
| 84 | 全域:不換湯 | 命中 | fail | pass | B replaces 「與其說這是優化，不如說是重寫」 with the redundant 「這次改版重寫了報帳流程」, restating the same empty emphasis it removed. _(B=new, A=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 2 | 全域:不換湯 | 命中 | 保護 |
| 6 | 全域:不換湯 | 命中 | 保護 |
| 8 | 全域:不換湯 | 命中 | 保護 |
| 9 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 238): 12
- hit-class failures, new arm (comparative 227): 17
- hit-class failures, base arm (comparative 227): 8

NO-SHIP — 12 protection-class false kill(s) on the new arm: 4/metaphor-absence-does-not-flag-solo, 86/does-not-spare-on-casual-register, 47/expected-behavior, 60/preserves-punctuation-hand, 68/facts-preserved-verbatim, 57/preserves-key-figures, 59/expected-behavior, 59/preserves-rhetorical-question, and 4 more; hit-class regressed: new arm 17 failure(s) vs baseline 8 (comparative denominator)


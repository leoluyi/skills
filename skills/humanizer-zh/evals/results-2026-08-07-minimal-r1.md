# run-case — humanizer-zh — 2026-08-07

- run id: `4afe4e9e66a54c53811005fbcc6ad925`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 1)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-hwnah9fs`

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
| 保護 | base | 145 | 153 |
| 命中 | new | 74 | 85 |
| 命中 | base | 73 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags only the rhetorical-question ending; B also flags 「差在骨幹是誰的話。」 as 破碎短句堆疊. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A flags 「範圍是開放的，不是固定的」 with the undefined-scope rationale; B grants the fact-boundary carve-out and does not flag it. _(B=new, A=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | fail | fail | Neither flags 「兩條路」 as a colloquial catch-all. |
| 9 | flags-bare-verb | 命中 | pass | fail | A turns it into a reader directive 「請勿誤改」 without restoring subject/object; B writes 「不會把真正的術語誤判成該改的詞」. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」 as a premise-free bare assertion. |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the unmarked condition before 「就別開」. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note by invoking casual carve-outs, exactly the borrowed-register exemption forbidden. |
| 47 | expected-behavior | 保護 | fail | fail | Source says pass untouched, but A raises four flags (空降主張×2, 空話填充, 情緒宣告) and B raises two (空降主張, 情緒宣告), so both mark a clean passage. _(A=new, B=base)_ |
| 64 | preserves-typo-joke | 保護 | fail | pass | A drops the first 「跟本」 clause entirely (rewrites it as 「客戶就不必進你的網站了」), leaving the later 是「跟本」喔！ with no referent; B keeps both occurrences. _(A=new, B=base)_ |
| 64 | 全域:保真 | 保護 | fail | pass | A alters source wording beyond flagged issues (drops 跟本, changes 用戶 to 使用者, rewrites 不讓客戶到你的網站); B changes only the flagged 更方便 span. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | pass | fail | A gives an either/or (promote to full sentence or demote to pure label) with 時程 folded into the sentence; B's fix only says separate label from sentence or move the deliverable after 取得, never addressing that 時程 must not stand as a second label端. _(A=new, B=base)_ |
| 72 | flags-self-vouching | 命中 | fail | pass | A spares the clause under a docs/disambiguation carve-out; B flags 自我背書 and notes the clause adds no new fact and vouches for completeness. _(A=new, B=base)_ |
| 72 | fix-restores-operative-clause | 命中 | fail | pass | A offers no fix at all since it passed the段; B directs the text back to the operative act (state how the grey-area cases are judged by the three factors). _(A=new, B=base)_ |
| 72 | no-disambiguation-confusion | 保護 | fail | pass | A explicitly invokes the 消歧義 carve-out for a passage with no competing criterion; B states no evidence of a competing criterion exists. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | Both flag only 「撐得住」 as 口語化萬能詞 and A/B each explicitly deny any missing-relation issue; neither marks the 快取層…下降 / 所以…往後延 inference gap. _(A=new, B=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | Neither names 命中率, current latency, or node headroom as the missing premises; both only ask for load/capacity numbers behind 撐得住. |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | fail | Both make 「目前的架構撐得住」 the sole flagged item, treating the standalone short sentence as the defect. |
| 80 | flags-missing-connective | 命中 | pass | fail | A flags 「延長保固，要在購買日起三十天內上網登錄」 for the bare verb phrase lacking a conditional marker; B declares the relation clear and issues no flag. _(A=new, B=base)_ |
| 80 | fix-restores-the-connective | 命中 | pass | fail | A prescribes adding 「若要」/「如欲」 rather than splitting or listing; B offers no fix. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | fail | pass | A explicitly declines to flag 「以下是清理後的版本，請複製使用」 as a residue, missing the third type; B flags all three. _(A=new, B=base)_ |
| 36 | expected-direction | 命中 | pass | fail | A points to rewriting as a prose paragraph; B only offers deleting/replacing the column, no prose direction. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | pass | fail | B flags 對讀者說教 and 反問句開場與收尾 on the argued assertion and closing question; A passes with only a separate 模糊歸屬 note. _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | pass | fail | B tells the author to state the point directly instead of asking; A keeps the question. _(A=new, B=base)_ |
| 62 | expected-behavior | 保護 | fail | pass | A flags 意義膨脹 on the fabless-industry sentence demanding evidence; B passes the paragraph clean. _(A=new, B=base)_ |
| 69 | no-template-false-positive | 保護 | pass | fail | B flags 翻譯腔 on 「基於決策分析引擎之數據驅動精準行銷」, a register-drift-family flag on template field text; A raises no register-drift flag. _(A=new, B=base)_ |
| 70 | no-weak-signal-stacking | 保護 | pass | fail | B flags 翻譯腔 on 「優先採用有生產級別的元件」, exactly the register-drift call the row forbids; A stays off that rule. _(A=new, B=base)_ |
| 75 | no-self-vouching-false-positive | 保護 | pass | fail | B flags 自我背書 on the sentence; A passes it clean. _(A=new, B=base)_ |
| 78 | fix-hedging-opener | 命中 | fail | pass | A explicitly keeps 「值得注意的是」 in the rewritten text; B deletes it. _(A=new, B=base)_ |
| 78 | 全域:不換湯 | 命中 | fail | pass | A retains the hollow 值得注意的是 rather than removing it, leaving the empty family in place. _(A=new, B=base)_ |
| 83 | fix-second-person-judgement | 命中 | pass | fail | A rewrites to 「否則匯出結果無法使用」 with the topic as subject; B keeps 「你要先確認…不然匯出的檔案根本沒辦法用」 with 你 still governing the judgement clause. _(A=new, B=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | pass | A strips 你 from 「設定頁往下捲你會看到一個紅色警告」, rewriting the protected procedural second person; B keeps it verbatim. _(A=new, B=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 8
- hit-class failures, new arm (comparative 227): 11
- hit-class failures, base arm (comparative 227): 12

NO-SHIP — 8 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 64/preserves-typo-joke, 64/全域:保真, 72/no-disambiguation-confusion, 79/no-flag-on-final-short-sentence-alone, 62/expected-behavior, 83/preserves-procedural-second-person


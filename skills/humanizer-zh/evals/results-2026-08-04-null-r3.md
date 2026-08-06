# run-case — humanizer-zh — 2026-08-05

- run id: `1eabf56d29e44f74a221112e96a5ad74`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-is1upjka`

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
| 保護 | new | 146 | 153 |
| 保護 | base | 145 | 153 |
| 命中 | new | 73 | 85 |
| 命中 | base | 76 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 7 | flags-slogan-replacing-explanation | 命中 | fail | pass | B raises 「連網一行指令，或離線的逐一技能 symlink」 as its own finding needing real steps; A never files it as a finding, only mentions expansion inside the 兩條路 fix. _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」 as 破碎短句堆疊 — A lists no P1 at all and B explicitly shields it as declared colloquial voice. _(B=new, A=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the 「…就別開」 clause; A calls it a clear usage condition and B rules 破碎短句堆疊 不成立 because 「就」 is present. _(B=new, A=base)_ |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the entire note with zero findings by invoking the casual voice declaration, exactly the register-based pass the row forbids. |
| 22 | expected-direction | 命中 | fail | pass | A only reduces emoji ('保留一至兩個') without asking for what-changed specifics, while B caps at one and demands naming the actual feature and effect. _(A=new, B=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A flags 自我背書 with the no-new-content evidence; B reports P1 無需標記 and clears the clause entirely. _(A=new, B=base)_ |
| 72 | fix-restores-operative-clause | 命中 | fail | fail | A only says state the judgments directly without restoring the operative clause subject, and B proposes no fix at all. _(A=new, B=base)_ |
| 72 | no-disambiguation-confusion | 保護 | fail | fail | A conditions its fix on a disambiguation exception and B clears the line outright as 具消歧義功能, the exact confusion the row bars. _(A=new, B=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | A flags only 「撐得住」 as a vague word and B reports no findings at all; neither flags the unstated premises behind the cache claim and the 所以 conclusion. _(A=new, B=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | A asks for traffic/load limits only around 「撐得住」 and never names hit rate, current latency, or node headroom for the inference chain; B offers no fix. _(A=new, B=base)_ |
| 79 | no-flag-on-final-short-sentence-alone | 保護 | fail | pass | A makes the standalone 「目前的架構撐得住」 its sole finding, while B explicitly declines to flag it. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | Expectation is a clean pass, but A raises five flags and B raises four including a P0 on the human aside 不曉得你們有沒有同樣的感受. _(A=new, B=base)_ |
| 64 | 全域:保真 | 保護 | pass | fail | A changes only 用戶/使用者 and a particle, while B drops the author's 即時互動 attribute into 直接互動 and replaces 「SEO 的死亡」 with its own formulation. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | fail | fail | Both flag utm param and citeturn token but explicitly decline to flag the conversational residue 「以下是清理後的版本，請複製使用」 (A states it, B omits it entirely). _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | fail | pass | A passes the whole paragraph; B raises a P1 on 「造就了全球無晶圓廠IC設計產業的崛起」 and proposes narrowing it, a false positive on the annual-report statement. _(B=new, A=base)_ |
| 78 | fix-hedging-opener | 命中 | fail | fail | Both keep 「值得注意的是」 in the rewrite, justifying it as a density carve-out. |
| 78 | 全域:不換湯 | 命中 | fail | pass | A drops the fairness clause entirely; B replaces 「以確保流程的公平性」 with 「確保流程公平」, the same empty assurance re-worded. _(B=new, A=base)_ |
| 81 | flags-dangling-copular-frame | 命中 | fail | pass | A flags the first sentence and directs restoring the full frame; B declares the sentence complete and raises no flag. _(B=new, A=base)_ |
| 81 | flags-under-fragmented-clause-rule | 命中 | fail | fail | A files it under 過度簡寫 and explicitly rejects 破碎短句堆疊; B files it nowhere. _(B=new, A=base)_ |
| 38 | no-preview-opener-false-positive | 保護 | pass | fail | A carves the sentence out explicitly; B leaves it unflagged as 文件自述 but raises 作者隱身 citing that it 只有「使用 AI 改稿」的主題, marking the protected sentence as needing supplementation. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | The row calls for release, yet both raise three findings including treating the closing question as a substitute for a missing conclusion. |
| 59 | preserves-rhetorical-question | 保護 | fail | fail | Both tell the author to state the advantage directly instead of the closing question, i.e. convert it or supply the answer. |
| 66 | 全域:保真 | 保護 | pass | fail | A keeps all source wording except the flagged tail; B misquotes the source as 「大家都不用下班耶」 in its own protection list and rewrites 心理健康很多 into 心理狀態好多了. _(A=new, B=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 86 | does-not-spare-on-casual-register | 保護 | 命中 |
| 60 | 全域:不換湯 | 命中 | 保護 |
| 61 | 全域:不換湯 | 命中 | 保護 |
| 64 | 全域:不換湯 | 命中 | 保護 |
| 68 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 238): 7
- hit-class failures, new arm (comparative 227): 12
- hit-class failures, base arm (comparative 227): 9

NO-SHIP — 7 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 72/no-disambiguation-confusion, 79/no-flag-on-final-short-sentence-alone, 47/expected-behavior, 62/expected-behavior, 59/expected-behavior, 59/preserves-rhetorical-question; hit-class regressed: new arm 12 failure(s) vs baseline 9 (comparative denominator)


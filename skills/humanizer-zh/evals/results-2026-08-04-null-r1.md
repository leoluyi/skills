# run-case — humanizer-zh — 2026-08-05

- run id: `0a4835dcf2164ab0bf4334a0073c6956`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-gtv8dklb`

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
| 保護 | new | 145 | 153 |
| 保護 | base | 147 | 153 |
| 命中 | new | 75 | 85 |
| 命中 | base | 78 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 1 | no-word-level-false-positives | 保護 | pass | fail | A flags only empty framing; B additionally marks the substantive technical clause 「例如環境一致性與部署效率」 as 列舉代替論述, hitting correct technical content. _(A=new, B=base)_ |
| 4 | metaphor-absence-does-not-flag-solo | 保護 | pass | fail | Both decline 作者隱身, but B flags 「這個地雷」「一樣的坑」 as 口語化萬能詞, punishing the very colloquial voice markers this row protects. _(A=new, B=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | fail | pass | A explicitly declines the broken-syntax read and never marks the closing as a rhetorical question; B flags 「差在骨幹是誰的話」 as 空降斷言開場 and the ending as 反問句收尾. _(A=new, B=base)_ |
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | fail | pass | A silently rewrites the hollow paragraph into 「測試撰寫者知道這一點…」 instead of flagging it; B emits an explicit 【此段扣除語氣後無實質內容…】 marker. _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | pass | A declares 破碎短句堆疊不成立 and never flags 「會結束，放心壓」; B flags it as a premise-less conclusion. _(A=new, B=base)_ |
| 86 | flags-missing-connective | 命中 | fail | pass | A leaves the 「就別開」 clause unflagged; B flags the missing conditional marker on the front half. _(A=new, B=base)_ |
| 86 | does-not-spare-on-casual-register | 保護 | fail | pass | A clears the whole note on the grounds of declared casual voice; B states casual gives no carve-out for this rule. _(A=new, B=base)_ |
| 21 | expected-direction | 命中 | pass | fail | B names the bold label being restated by its own line; A only calls the bold formatting excessive and never touches the restatement or the 透過X達成Y parallel. _(B=new, A=base)_ |
| 22 | expected-direction | 命中 | fail | pass | A flags the contentless slogans and asks for concrete features; B flags only emoji and explicitly declines to flag the empty promo lines. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A clears the clause under a docs carve-out; B flags 自我背書 and notes 皆來自 vouches for completeness without adding content. _(B=new, A=base)_ |
| 72 | fix-restores-operative-clause | 命中 | pass | fail | A offers no fix at all; B replaces the clause with a direct statement that the table judges by the three factors. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | fail | A flags neither conclusion and even clears the chain via 上線之後/所以; B flags only the deferral claim and leaves the cache-to-latency claim unmarked. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | A gives no such fix; B asks generically for 何種負載／指標 without naming hit rate, current latency, or node headroom. _(B=new, A=base)_ |
| 28 | no-single-instance-false-positive | 保護 | fail | pass | A carves out the single occurrence; B flags 解說導引腔 as a hard defect on one instance. _(B=new, A=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | The source should be passed untouched, but A raises three flags and B raises four. _(B=new, A=base)_ |
| 47 | no-run-on-splitting | 保護 | fail | pass | B flags 破碎短句堆疊 and prescribes splitting the clauses and adding connectives, exactly the prohibited move; A does not. _(B=new, A=base)_ |
| 68 | facts-preserved-verbatim | 保護 | pass | fail | A adds 及分工 as an extra thing to be confirmed, changing the deliverable; B keeps the four items intact. _(B=new, A=base)_ |
| 80 | flags-missing-connective | 命中 | fail | fail | Both declare the sentence clear and raise no flag on 延長保固，要在購買日起三十天內上網登錄. |
| 80 | fix-restores-the-connective | 命中 | fail | fail | Neither proposes restoring a conditional marker such as 如果要延長保固, since neither flagged the clause. |
| 83 | preserves-procedural-second-person | 保護 | fail | pass | A rewrote the protected sentence into 設定頁往下捲動後，可以看到紅色警告, stripping the procedural 你; B kept it verbatim. _(A=new, B=base)_ |
| 39 | expected-direction | 命中 | fail | pass | A directs to deleting both reaction shots; B names both but only asks to delete one, leaving a canned reaction standing. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | The passage should be released, yet A raises both 模糊歸屬 and the expressly forbidden 空降主張 on the argued three-year scenario, and B still raises a hard 模糊歸屬 flag. _(B=new, A=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | A only drops the intensifier 爆炸性; B drifts 「心理健康」 to 「心理狀態反而好多了」 and drops the named term 第一性原理 from the text. _(B=new, A=base)_ |
| 66 | 全域:不換湯 | 命中 | fail | pass | A marks the hollow closer instead of substituting; B swaps 「維持學習的第一性原理非常重要」 for 「學習要維持下去」, another vague assertion of the same family. _(B=new, A=base)_ |
| 84 | 全域:不代筆 | 保護 | pass | fail | A asserts 「介面也一起換了」, a claim the source never makes (the original only says it is not merely an interface swap); B adds nothing new. _(B=new, A=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 60 | 全域:不換湯 | 命中 | 保護 |
| 61 | 全域:不換湯 | 命中 | 保護 |
| 64 | 全域:不換湯 | 命中 | 保護 |
| 68 | 全域:不換湯 | 命中 | 保護 |
| 63 | 全域:不換湯 | 命中 | 保護 |
| 65 | 全域:不換湯 | 命中 | 保護 |
| 78 | 全域:不換湯 | 命中 | 保護 |
| 83 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 238): 8
- hit-class failures, new arm (comparative 227): 10
- hit-class failures, base arm (comparative 227): 7

NO-SHIP — 8 protection-class false kill(s) on the new arm: 6/hollow-paragraph-flagged-not-fabricated, 86/does-not-spare-on-casual-register, 28/no-single-instance-false-positive, 47/expected-behavior, 47/no-run-on-splitting, 83/preserves-procedural-second-person, 59/expected-behavior, 66/全域:保真; hit-class regressed: new arm 10 failure(s) vs baseline 7 (comparative denominator)


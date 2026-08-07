# run-case — humanizer-zh — 2026-08-07

- run id: `1ddbfee62773498f80de3af3d42c4f1f`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 2)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-gej6t6a0`

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
| 保護 | new | 143 | 153 |
| 保護 | base | 145 | 153 |
| 命中 | new | 72 | 85 |
| 命中 | base | 70 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags both 「差在骨幹是誰的話」 (elided frame) and the rhetorical closer, while B flags only the closer and leaves the fragment unmarked. _(A=new, B=base)_ |
| 7 | flags-slogan-replacing-explanation | 命中 | pass | fail | A flags the 連網一行指令／離線 symlink pair as 口號代替說明 and asks for the actual steps; B flags only 「兩條路」 and never treats the paired phrase as slogan-for-explanation. _(A=new, B=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」 as a bare assertion; A reports no patterns and B explicitly declines to mark it. _(A=new, B=base)_ |
| 86 | flags-missing-connective | 命中 | fail | fail | The 「…就別開」 sentence is left unflagged by both, A keeping it as casual voice and B as personal advice. _(A=new, B=base)_ |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note on casual-voice grounds, A citing 「casual 聲音，不改」 and B 「casual voice carve-out」. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | A raises three flags (空降主張/情緒宣告/空話填充) and B raises 情緒宣告, but the passage should pass clean. _(B=new, A=base)_ |
| 60 | preserves-punctuation-hand | 保護 | pass | fail | A converts half-width commas to full-width, adds periods/question mark and normalizes spacing; B returns the line byte-identical. _(B=new, A=base)_ |
| 64 | preserves-product-names | 保護 | pass | fail | A deletes SEO entirely (「SEO 的死亡」 rewritten away); B keeps Google I/O 2026, SEO and Mini APP verbatim. _(B=new, A=base)_ |
| 64 | 全域:保真 | 保護 | pass | fail | A drops the term SEO and 即時 and rewrites the closing clause; B removes only 更方便的. _(B=new, A=base)_ |
| 64 | 全域:不換湯 | 命中 | pass | fail | A swaps the unquantified 更方便的 for the equally unquantified 直接 while dropping 即時; B simply deletes the empty modifier. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | Both give only a promotion-to-sentence rewrite and neither says the schedule belongs as an annotation rather than a second label end. |
| 68 | fix-picks-one-register | 命中 | fail | pass | A promotes to one full sentence; B keeps the label head and appends a full clause, the hybrid third form the row forbids. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | fail | fail | Both report nothing to flag and spare 判斷依據皆來自前文 under a docs carve-out. |
| 72 | fix-restores-operative-clause | 命中 | fail | fail | With no flag raised, neither points to restoring the operative judging clause. |
| 72 | no-disambiguation-confusion | 保護 | fail | fail | A spares it as 判斷範圍說明 and B as 明確交代本節採用的判斷依據 — both are the scope-clarification rationale this row forbids. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | pass | A flags the cache/所以延後擴充 chain as unstated causality; B declares the passage clean because 之後/就會/所以 are present. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | A only asks to 明確寫出因果及條件 without naming hit rate, current latency or node headroom; B raises no fix at all. _(B=new, A=base)_ |
| 80 | flags-missing-connective | 命中 | pass | fail | A reports nothing to flag; B flags 延長保固，要在購買日起三十天內上網登錄 for the missing condition marker and re-read cost. _(B=new, A=base)_ |
| 80 | fix-restores-the-connective | 命中 | pass | fail | A gives no fix; B restores 若要延長保固，請在購買日起三十天內上網登錄 without splitting or listifying. _(B=new, A=base)_ |
| 32 | expected-direction | 命中 | fail | pass | A names utm param, citeturn placeholder, and the 「以下是清理後的版本，請複製使用」 conversational residue; B flags only two, omitting the chat residue. _(B=new, A=base)_ |
| 34 | expected-direction | 命中 | fail | pass | A explicitly directs to rewrite as one flowing paragraph; B only asks each numbered item be made concrete, never to merge into prose. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | fail | fail | Both flag the argued assertion — A as 對讀者說教 plus 模糊歸屬, B additionally as 反問句開場與收尾 — instead of passing the argued passage. _(B=new, A=base)_ |
| 59 | preserves-rhetorical-question | 保護 | fail | pass | A explicitly protects the closing rhetorical question; B flags it and tells the author to state the answer directly. _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | fail | fail | Both flag the fabless-industry sentence (A as 意義膨脹, B as 空降主張) rather than passing the annual-report paragraph. _(B=new, A=base)_ |
| 65 | 全域:保真 | 保護 | fail | pass | B deletes 「有沒有人覺得在使用」, leaving the broken fragment 「Google AI Mode 的時候，眼睛都要被閃瞎了？」 with a stray question mark and lost author voice. _(B=new, A=base)_ |
| 66 | does-not-supply-rationale | 保護 | fail | pass | A only marks the hollow closing sentence; B rewrites 「第一性原理」 out into 「維持學習很重要」, editing the author's claim instead of just flagging it. _(B=new, A=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | B drops 「第一性原理」 from the author's own sentence; A preserves all source wording it retains. _(B=new, A=base)_ |
| 66 | 全域:不換湯 | 命中 | fail | pass | B replaces one vague importance claim with an equally empty 「維持學習很重要」 — same family, no gain. _(B=new, A=base)_ |
| 69 | does-not-rewrite-in-detect | 保護 | fail | pass | B's reproduced original mangles the record — duplicated 「會議記錄:」 header and table rows rendered with literal \t escapes, altering the document in a detect run. _(B=new, A=base)_ |
| 78 | fix-hedging-opener | 命中 | pass | fail | A keeps 「值得注意的是」 in its output on a density argument; B deletes it. _(B=new, A=base)_ |
| 78 | 全域:不換湯 | 命中 | pass | fail | A leaves the hedging opener in place rather than removing it; B's replacement is a plain factual statement, not a same-family phrase. _(B=new, A=base)_ |
| 81 | flags-under-fragmented-clause-rule | 命中 | fail | pass | A files it under 破碎短句堆疊 as required; B files it under 過度簡寫, the rule the key excludes. _(B=new, A=base)_ |
| 83 | fix-second-person-judgement | 命中 | fail | fail | A leaves the clause fully unchanged; B swaps 東西 for 匯出結果 but keeps 「你」 as the subject of the judgement. _(B=new, A=base)_ |
| 83 | 全域:不換湯 | 命中 | pass | fail | A makes no change at all where the second-person judgement needed fixing; B's 匯出結果 is a concrete term, not an empty-family swap. _(B=new, A=base)_ |

## class_read disagreements

None.

## Gate

- protection-class failures, new arm (absolute 238): 10
- hit-class failures, new arm (comparative 227): 13
- hit-class failures, base arm (comparative 227): 15

NO-SHIP — 10 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 72/no-disambiguation-confusion, 59/expected-behavior, 59/preserves-rhetorical-question, 62/expected-behavior, 65/全域:保真, 66/does-not-supply-rationale, and 2 more


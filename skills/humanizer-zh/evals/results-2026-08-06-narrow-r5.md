# run-case — humanizer-zh — 2026-08-07

- run id: `d4f2f0b4d5ae4602b7358d3fc03225a7`
- new arm: working tree `/Users/leoluyi/.skills/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `HEAD:skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm source: bank (bank round 2)
- runner: codex (gpt-5.6-luna) effort high
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `3876e6b12255086231ae8985d36a4f3754146bb3798c81e026a15e57c2266c41`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-zsfy_7n8`

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
| 保護 | base | 142 | 153 |
| 命中 | new | 72 | 85 |
| 命中 | base | 70 | 85 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 1 | no-word-level-false-positives | 保護 | pass | fail | A marks the span 「有許多好處，例如環境一致性與部署效率」 as 空話填充, dragging the correct technical statement into the flag, while B limits the flag to the vague quantifier and explicitly notes the concrete benefits are stated. _(B=new, A=base)_ |
| 4 | metaphor-absence-does-not-flag-solo | 保護 | pass | fail | Both decline the voiceless verdict, but A additionally flags 「——記得 13 年前我也踩過一樣的坑」 as 破折號濫用 and asks to split the personal recollection off, hitting a real voice marker; B explicitly rules the single dash below threshold. _(B=new, A=base)_ |
| 5 | also-flags-cooccurring-tells | 命中 | pass | fail | A flags only the closing rhetorical question and never the fragment syntax; B flags both 「差在骨幹是誰的話。」 as 破碎短句堆疊 and the question ending. _(B=new, A=base)_ |
| 7 | flags-slogan-replacing-explanation | 命中 | fail | fail | A never flags the 「連網一行指令，或離線的逐一技能 symlink」 span itself, and B affirmatively defends it as valid list content. _(B=new, A=base)_ |
| 7 | flags-contrast-construction | 命中 | pass | fail | A labels 「範圍是開放的，不是固定的」 as 空話填充 without identifying the negation frame; B labels it 對比句式 with the missing-boundary diagnosis. _(B=new, A=base)_ |
| 7 | flags-colloquial-catch-all-phrase | 命中 | fail | pass | A flags 「兩條路」 as 口語化萬能詞 and proposes 「兩個方式」; B does not flag it at all. _(B=new, A=base)_ |
| 86 | flags-broken-inference-chain | 命中 | fail | fail | Neither flags 「會結束，放心壓」 as a bare assertion with no stated premise; both report zero findings. |
| 86 | flags-missing-connective | 命中 | fail | fail | Neither flags the unmarked conditional in 「之後還要…就別開」. |
| 86 | does-not-spare-on-casual-register | 保護 | fail | fail | Both clear the whole note on casual-voice/carve-out grounds, which is exactly the register-based pass this row forbids. |
| 47 | expected-behavior | 保護 | fail | fail | A raises three flags (空降主張/情緒宣告/空話填充) and B raises 空降主張, where the expectation is a clean pass. _(B=new, A=base)_ |
| 60 | preserves-punctuation-hand | 保護 | pass | fail | A rewrites the half-width commas, inserts periods/question mark and normalizes spacing; B returns the text byte-identical. _(B=new, A=base)_ |
| 64 | preserves-product-names | 保護 | pass | fail | A's rewrite drops SEO entirely (「SEO 的死亡」 replaced by a paraphrase); B keeps Google I/O 2026, SEO and Mini APP. _(B=new, A=base)_ |
| 64 | 全域:保真 | 保護 | pass | fail | A loses the term SEO from the text; B preserves every name, term and quoted fragment. _(B=new, A=base)_ |
| 67 | fix-names-one-register | 命中 | fail | pass | A offers a clean either/or (full sentence with the schedule as adverbial, or label plus parenthetical); B's 'keep the heading/body split and move the deadline to the front' produces the mixed third form. _(B=new, A=base)_ |
| 68 | fix-picks-one-register | 命中 | fail | pass | A promotes to a single full sentence; B keeps 執行方式與分工： as a label and appends a full sentence, i.e. the mixed third form. _(B=new, A=base)_ |
| 72 | flags-self-vouching | 命中 | pass | fail | A spares the clause under a docs carve-out and flags nothing; B flags 自我背書 and identifies 皆來自 as a defensive completeness claim. _(B=new, A=base)_ |
| 72 | fix-restores-operative-clause | 命中 | pass | fail | A gives no fix at all; B directs it back to the operative act of judging ('直接說明本節依哪三項因素判斷'). _(B=new, A=base)_ |
| 72 | no-disambiguation-confusion | 保護 | pass | fail | A spares the clause by calling it a 判斷範圍說明, the scope-delimiting rationale this row forbids; B explicitly rules the carve-out inapplicable. _(B=new, A=base)_ |
| 79 | flags-broken-inference-chain | 命中 | fail | pass | A flags the cache/latency claim through the 所以 conclusion as unsupported chaining; B declares the chain sound and flags only the closing short sentence. _(B=new, A=base)_ |
| 79 | fix-names-the-missing-premise | 命中 | fail | fail | A only says to write out '因果及條件' without naming hit rate, current latency or node headroom; B offers no chain fix at all. _(B=new, A=base)_ |
| 80 | flags-missing-connective | 命中 | fail | fail | Both report the passage clean and neither flags the bare 延長保固，要在購買日起三十天內上網登錄. |
| 80 | fix-restores-the-connective | 命中 | fail | fail | Neither proposes restoring a conditional marker such as 如果要延長保固. |
| 36 | flags-hollow-column | 命中 | fail | pass | A names the 意義 column specifically as hollow and to be dropped; B lumps 優點 and 意義 together and never singles out the 意義 column for deletion. _(B=new, A=base)_ |
| 59 | expected-behavior | 保護 | pass | fail | A flags the 「你其實只是在接一個訂閱服務」 argued assertion as 對讀者說教 and demands replacing 你, a false positive on argued content; B explicitly declines that flag. _(B=new, A=base)_ |
| 62 | expected-behavior | 保護 | fail | fail | Both flag 「造就了全球無晶圓廠IC設計產業的崛起」 as 意義膨脹 and ask to soften or delete the causal claim, a false positive on an annual-report factual statement. |
| 62 | preserves-figures | 保護 | fail | pass | A reproduces 1 萬 2,302 in the source's mixed form; B rewrites it as 12,302 種產品 in its reasoning, altering the Chinese place-word notation. _(B=new, A=base)_ |
| 66 | preserves-sentence-final-particle | 保護 | fail | pass | A keeps 都沒有人要下班耶 verbatim; B rewrites it to 大家好像都不下班, dropping the 耶 despite claiming to preserve it. _(B=new, A=base)_ |
| 66 | 全域:保真 | 保護 | fail | pass | B alters 資訊焦慮/心理健康 phrasing and drops the 耶 particle and 爆炸性 wording; A preserves the source text intact. _(B=new, A=base)_ |
| 69 | does-not-rewrite-in-detect | 保護 | fail | pass | B supplies a rewritten replacement string 「盤點支援相關應用的資訊系統」 for a field value in detect mode, rewriting rather than only reporting. _(B=new, A=base)_ |
| 70 | no-weak-signal-stacking | 保護 | fail | pass | B flags 「將多個獨立 AI 能力組合成完整業務流程編排複雜度…」 as 破碎短句堆疊 硬缺陷, exactly the sentence whose 將 opener the rule exempts; A raises no such flag. _(B=new, A=base)_ |
| 78 | fix-hedging-opener | 命中 | pass | fail | A keeps 值得注意的是 in its final output, arguing a density threshold; B flags and deletes it. _(B=new, A=base)_ |
| 78 | 全域:不換湯 | 命中 | pass | fail | A leaves the hollow opener 值得注意的是 standing in the delivered text rather than removing it; B removes it without substituting a same-family phrase. _(B=new, A=base)_ |
| 81 | flags-dangling-copular-frame | 命中 | fail | pass | A flags the dangling copular frame and directs restoring the full 句架; B instead calls it 翻譯腔 and never identifies the missing frame. _(B=new, A=base)_ |
| 81 | flags-under-fragmented-clause-rule | 命中 | fail | pass | A files it under 破碎短句堆疊 as required; B files it under 翻譯腔, the wrong rule. _(B=new, A=base)_ |
| 83 | fix-second-person-judgement | 命中 | pass | fail | A makes no change at all, leaving 「不然你匯出來的東西根本沒辦法用」 intact; B rewrites it to 否則匯出內容無法使用, removing the 你. _(B=new, A=base)_ |
| 83 | preserves-procedural-second-person | 保護 | fail | pass | A keeps 「設定頁往下捲你會看到一個紅色警告」 verbatim; B strips the 你 to 「往下捲動後，會看到紅色警告」, editing protected procedural second person. _(B=new, A=base)_ |
| 83 | 全域:保真 | 保護 | fail | pass | B alters protected procedural wording (往下捲 to 往下捲動, dropping 你) beyond the licensed fix; A leaves the source untouched. _(B=new, A=base)_ |
| 83 | 全域:不換湯 | 命中 | pass | fail | A changed nothing, so the flagged second-person judgement remains; B's replacements are plain statements, not same-family substitutes. _(B=new, A=base)_ |
| 84 | no-stacked-contrast-frames | 保護 | pass | fail | A's output retains two contrast frames (「介面只是其中一部分」 plus 「性質是重寫，不是優化」), exceeding the one-frame ceiling; B keeps only 「不只是換介面」. _(B=new, A=base)_ |
| 84 | 全域:不換湯 | 命中 | pass | fail | A swaps 「與其說這是優化，不如說是重寫」 for 「這次改版的性質是重寫，不是優化」, the same contrast family restated; B deletes it outright. _(B=new, A=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 2 | 全域:不換湯 | 命中 | 保護 |
| 6 | 全域:不換湯 | 命中 | 保護 |
| 8 | 全域:不換湯 | 命中 | 保護 |
| 9 | 全域:不換湯 | 命中 | 保護 |
| 86 | does-not-spare-on-casual-register | 保護 | 命中 |
| 60 | 全域:不換湯 | 命中 | 保護 |
| 61 | 全域:不換湯 | 命中 | 保護 |
| 64 | 全域:不換湯 | 命中 | 保護 |
| 68 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 238): 10
- hit-class failures, new arm (comparative 227): 13
- hit-class failures, base arm (comparative 227): 15

NO-SHIP — 10 protection-class false kill(s) on the new arm: 86/does-not-spare-on-casual-register, 47/expected-behavior, 62/expected-behavior, 62/preserves-figures, 66/preserves-sentence-final-particle, 66/全域:保真, 69/does-not-rewrite-in-detect, 70/no-weak-signal-stacking, and 2 more


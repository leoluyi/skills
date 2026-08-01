# run-case — humanizer-zh — 2026-08-01

- run id: `071325113f3745c49c3453eea682abb4`
- new arm: working tree `/Users/leoluyi/.skills/.claude/worktrees/wild-stargazing-planet/skills/humanizer-zh`, version 2.2.0, 6 file(s)
- base arm: `3eedd0f:skills/humanizer-zh`, version 2.1.0, 6 file(s)
- runner: codex (gpt-5.6-luna)
- grader: claude (claude-opus-5)
- grader brief sha256: `4ff932b04b2c8df13cdeaba5ddabc775b5f9035861d685330c2d02ccd6a7efeb`
- grading criteria sha256: `7b66a1674116c592e91069fab12898804fb30ebe94e9cabface1804d7378e211`
- scratch workspace (removed after the run): `/var/folders/z5/zn9s6bqn2ljbl6wytcqq28zr0000gn/T/run-case-8vuhs3t2`

## Chunks

| chunk | range | cases | ids | rows |
|---|---|---|---|---|
| 0 | [1, 9] | 9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 38 |
| 1 | [10, 19] | 9 | 10, 11, 12, 13, 14, 15, 16, 18, 19 | 18 |
| 2 | [20, 67] | 11 | 20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 67 | 16 |
| 3 | [25, 71] | 14 | 25, 26, 27, 28, 29, 45, 46, 47, 55, 60, 61, 64, 68, 71 | 42 |
| 4 | [30, 69] | 14 | 30, 31, 32, 33, 34, 48, 49, 50, 51, 56, 62, 63, 65, 69 | 34 |
| 5 | [35, 70] | 13 | 35, 36, 37, 38, 39, 52, 53, 54, 57, 58, 59, 66, 70 | 31 |

## Denominators

```
absolute denominator: 149 − 3 + 33 = 179
  149 raw expectations in evals.json
  − 3 unscored (slug prefix: ground-truth-note)
  + 33 global rewrite rows (11 rewrite case(s) × 3 check(s))
comparative denominator: 179 − 11 = 168
  − 11 rows on baseline-incompatible ids [1, 4, 55, 56]
```

## baseline_incompatible deductions

| ids | rows deducted | reason |
|---|---|---|
| [1, 4, 55, 56] | 11 | 1.5.0 是 --structure-signals／結構級訊號，沒有 --expect-author；55/56 為 be5a09d 新增，1.5.0 結構上不可能過 |

## Per-class pass counts (absolute denominator)

| class | arm | pass | total |
|---|---|---|---|
| 保護 | new | 99 | 115 |
| 保護 | base | 103 | 115 |
| 命中 | new | 59 | 64 |
| 命中 | base | 58 | 64 |

## Non-green rows

| case | expectation | class | new | base | grader reason |
|---|---|---|---|---|---|
| 6 | hollow-paragraph-flagged-not-fabricated | 保護 | fail | pass | A silently rewrites paragraph B into 「測試撰寫者知道問題所在。這件事需要正面處理。」 instead of a marker, while B emits the required 標記句. _(A=new, B=base)_ |
| 7 | flags-contrast-construction | 命中 | fail | pass | A files the span under 零資訊警句與口號 rather than 對比句式; B flags it as 對比句式 explicitly. _(A=new, B=base)_ |
| 10 | flags-rhythm-metaphor | 命中 | pass | fail | A calls out 「節奏」 as abstract metaphor and points to 期程／排程／頻率; B folds it into 四字評語 and never treats 節奏 as a rhythm-table word. _(A=new, B=base)_ |
| 22 | expected-direction | 命中 | fail | pass | A permits 一至兩個 sentence-final emoji, above the 0–1 target; B caps at one and both add the concrete-info direction. _(A=new, B=base)_ |
| 43 | expected-behavior | 保護 | fail | fail | A flags 可圈可點 as 推廣語氣 and B flags the whole three-clause string, so neither passes the post through. _(A=new, B=base)_ |
| 43 | no-idiom-flattening | 保護 | fail | fail | A calls 可圈可點 an info-free four-character verdict to replace or delete, and B lumps 表現不俗 into the span while calling 可圈可點 空泛總評. _(A=new, B=base)_ |
| 67 | flags-register-drift | 命中 | pass | fail | A flags 語體漂移 citing the missing predicate and stranded 取得; B reports 不需修補 with no findings. _(A=new, B=base)_ |
| 67 | fix-names-one-register | 命中 | fail | fail | A picks 升格成句 but leaves 時程 coordinated with the deliverable instead of saying it belongs as an annotation; B offers no fix at all. _(A=new, B=base)_ |
| 27 | expected-behavior | 保護 | fail | fail | Both raise P0 知識截止免責 on a human verification caveat that carries no model self-reference. |
| 28 | no-single-instance-false-positive | 保護 | fail | pass | A flags the same guiding clause 「把這三個數字擺在一起」 as 空降斷言開場 despite the carve-out; B flags nothing. _(A=new, B=base)_ |
| 45 | expected-behavior | 保護 | fail | pass | A still flags 「不是我的產出量，而是我的判斷」 as 空降主張; B passes it clean with the once-per-piece carve-out. _(A=new, B=base)_ |
| 47 | expected-behavior | 保護 | fail | fail | A raises five flags and B raises seven on a passage the key says should go through untouched. _(A=new, B=base)_ |
| 61 | preserves-slang-register | 保護 | fail | fail | Both delete 「老司機都知道」 entirely from the rewrite. |
| 61 | preserves-implicature | 保護 | fail | pass | A spells the withheld meaning out as causation (「OpenAI 一道歉，我就先改用其他模型」); B just states the apology and leaves the choice separate. _(A=new, B=base)_ |
| 61 | 全域:不代筆 | 保護 | fail | pass | A asserts a general apology-triggers-switch rule the source never states; B adds nothing. _(A=new, B=base)_ |
| 64 | preserves-typo-joke | 保護 | fail | fail | Both erase the first 「跟本」; A further rewrites the punchline into 「原文是「跟本」喔！」. _(A=new, B=base)_ |
| 64 | 全域:保真 | 保護 | fail | pass | A alters the source's own quoted punchline sentence by inserting 「原文是」; B keeps 「是「跟本」喔！」 verbatim. _(A=new, B=base)_ |
| 64 | 全域:不換湯 | 命中 | fail | pass | A replaces the flagged inflation 「死亡」 with the same-family 「走到終點」; B drops to the neutral 「變化」. _(A=new, B=base)_ |
| 64 | 全域:不代筆 | 保護 | fail | pass | A invents the meta-framing 「原文是」 around the typo joke; B introduces no content absent from the post. _(A=new, B=base)_ |
| 68 | flags-register-drift | 命中 | pass | fail | A names 語體漂移 with the noun-string evidence; B labels it 過度簡寫 and 抽象claim缺交付 instead. _(A=new, B=base)_ |
| 68 | fix-picks-one-register | 命中 | pass | fail | A moves 確認 in front of the object it governs; B keeps the noun string plus trailing cross-comma 確認, leaving the defect. _(A=new, B=base)_ |
| 32 | expected-direction | 命中 | pass | fail | A names utm param, citeturn code and the conversational leftover; B explicitly declines to flag 「以下是清理後的版本，請複製使用」. _(A=new, B=base)_ |
| 34 | expected-direction | 命中 | fail | pass | B offers 「改成連貫段落」; A only asks each list item be verifiable and never points to prose. _(A=new, B=base)_ |
| 62 | no-slogan-flagging | 保護 | fail | fail | Both flag 「成功的關鍵就在於協助客戶獲得成功」 as 空話填充. |
| 62 | preserves-superlative-with-evidence | 保護 | pass | fail | A grants the carve-out for 「世界領先」; B flags it as 推廣語氣 lacking a comparison basis. _(A=new, B=base)_ |
| 63 | preserves-dash-inconsistency | 保護 | pass | fail | B deletes both dashes as 破折號濫用; A leaves the two differing dashes intact. _(A=new, B=base)_ |
| 63 | 全域:保真 | 保護 | pass | fail | B drops the quantifier 「一家」 from the 南京 subsidiary clause; A changes nothing. _(A=new, B=base)_ |
| 69 | no-template-false-positive | 保護 | fail | pass | A issues a 語體漂移 flag on the noun-label-plus-clause construction; B classifies the same text as 過度簡寫 and raises no 語體漂移. _(A=new, B=base)_ |
| 57 | preserves-key-figures | 保護 | fail | pass | A flags the new-customer conclusion as 空降主張 and asks it be caveated as 待確認觀察 despite the two numbers backing it, while B keeps it protected. _(A=new, B=base)_ |
| 59 | expected-behavior | 保護 | pass | fail | B flags the closing rhetorical question under 反問句開場與收尾 for not delivering the judgment, exactly the false positive the row forbids. _(A=new, B=base)_ |
| 59 | preserves-rhetorical-question | 保護 | pass | fail | A leaves the question intact; B directs it be turned into a declarative or given an answer. _(A=new, B=base)_ |

## class_read disagreements

| case | expectation | tool class | grader class_read |
|---|---|---|---|
| 60 | 全域:不換湯 | 命中 | 保護 |
| 61 | 全域:不換湯 | 命中 | 保護 |
| 64 | 全域:不換湯 | 命中 | 保護 |
| 68 | 全域:不換湯 | 命中 | 保護 |

## Gate

- protection-class failures, new arm (absolute 179): 16
- hit-class failures, new arm (comparative 168): 5
- hit-class failures, base arm (comparative 168): 6

NO-SHIP — 16 protection-class false kill(s) on the new arm: 6/hollow-paragraph-flagged-not-fabricated, 43/expected-behavior, 43/no-idiom-flattening, 27/expected-behavior, 28/no-single-instance-false-positive, 45/expected-behavior, 47/expected-behavior, 61/preserves-slang-register, and 8 more


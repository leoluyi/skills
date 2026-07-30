# 結構級訊號 — detect-only

A draft can pass every sentence-level rule and still read as machine-written. What is wrong then is not a phrase that is present but a set of properties that are absent: no judgement, no specific lived detail, no image of the author's own making, no breath in the rhythm. This aggregate signal names that absence. It never rewrites.

## The gate comes first

**Run this only on voice-bearing genres.** Blog and newsletter with a personal register, opinion and advocacy pieces, deep reads, personal essays — genres where a reader is entitled to a person behind the text.

**Voice-neutral genres are excluded as a group: docs, README, reference, RFP, 簽呈, 公文, SOP, spec, investor-email.** These are *supposed* to be even in rhythm, free of stance, and complete in every sentence. Every sub-signal below fires on a well-written 簽呈 by construction, which is precisely why this exclusion is the single largest false-positive guard in the skill. Establish the genre before you evaluate a single sub-signal, and when the genre is ambiguous, treat it as voice-neutral and say so.

`--structure-signals` is an explicit override and can force the audit on any genre. Passing it against a voice-neutral document is legitimate — the user may want to see the shape of the thing — but warn first that the findings will be dominated by genre-correct properties, then report anyway.

## Threshold

Report only when **two or more sub-signals hold at once**. One alone is within the range of ordinary careful writing, and a lone finding sends the author chasing a defect that isn't there.

`結構級訊號／只解釋不造像` never counts as a standalone finding, even alongside the threshold rule: dense procedural teaching legitimately runs on fixed idioms and worked examples rather than original metaphor. It corroborates; it does not initiate.

## The five sub-signals

Always name them in the form `結構級訊號／<name>`, never bare — two of the five share a name with an independent rule and the prefix is what distinguishes the document-scale reading from the sentence-scale one.

| 子訊號 | 缺席的是什麼 |
|---|---|
| `結構級訊號／立場真空` | 全篇找不到一句作者判斷；每個取捨都以「各有優劣」收場。與獨立規則**立場真空**同名，只是讀在文件尺度。 |
| `結構級訊號／零具體個人細節` | 沒有一個具體時間、次數、場景、金額；全是定義式陳述。 |
| `結構級訊號／只解釋不造像` | 每個難概念都用定義解釋，沒有一個把抽象拉到作者自身經驗的自創比喻。**永不單獨成立。** |
| `結構級訊號／無口語破格` | 沒有一處刻意的口語破格：無插入語、無（吧？）、無自問、無刻意殘句。 |
| `結構級訊號／節奏均質` | 連續段落長度相近、句長變異低、沒有單句成段、無長短交錯。與獨立規則**節奏均質**同名，只是讀在文件尺度。 |

`結構級訊號／無口語破格` has an inverse worth stating: a deliberate colloquial break already present in the draft is a positive feature under 保護清單 item ⑥. Smoothing it out during a rewrite creates the very flatness this sub-signal reports.

## How to report

Name what is absent, quote nothing you would have to invent, and hand the draft back. In `rewrite` mode this section still only reports — repairing it needs experience and judgement the author has and you do not, and a machine filling the gap produces more of exactly what the reader was already sensing.

> 結構級訊號（2/5 成立，voice-bearing 部落格）
> ・`結構級訊號／立場真空` — 三處比較（自架 vs 託管、月繳 vs 年繳、自己維護 vs 外包）都以「各有優缺點」收，全篇沒有一句作者的選擇。
> ・`結構級訊號／零具體個人細節` — 沒有一個日期、金額、次數或場景；「曾經遇過問題」未指明是哪一次。
> 建議作者補入：三個比較裡你自己選了哪一個、為什麼；以及那次「遇過問題」的實際時間、狀況與代價。

Division of labour: this skill subtracts noise and reports the absence. Injecting a voice — writing the stance, the metaphor, the anecdote — is additive work and belongs to `blog-writing-zh`. The two compose in that order, and the subtraction is careful not to eat the addition.

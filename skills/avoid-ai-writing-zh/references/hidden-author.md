# 作者隱身 — detect-only

A draft can pass every sentence-level rule and still read as machine-written. What is wrong then is not a phrase that is present but a set of properties that are absent: no judgement, no specific lived detail, no image of the author's own making, no breath in the rhythm. This aggregate signal names that absence. It never rewrites.

## The gate comes first

Every sub-signal below asks one question: can the reader see a person in this text? That question is meaningless in the genres where nobody is supposed to be visible, so the genre is settled before a single sub-signal is evaluated.

**Run this on every 署名文體 draft, and only on those.** Blog and newsletter with a personal register, opinion and advocacy pieces, deep reads, personal essays — the reader came for who is talking, so an absent author is a real defect. The genre verdict is the whole trigger; the user does not have to ask, and asking does not get them past it.

**事務文體 are excluded as a group: docs, README, reference, RFP, 簽呈, 公文, SOP, spec, 規劃書, 建議書, 計劃書, investor-email.** The reader came for the information and does not care who wrote it. A formal proposal belongs here even though it argues a position — it needs the author's judgement, not their personality, and 立場真空 in `zh-rules.md` covers the judgement on its own with a deliberately shorter carve-out list. These are *supposed* to be even in rhythm, free of stance, and complete in every sentence — every sub-signal below fires on a well-written 簽呈 by construction, which is precisely why this exclusion is the single largest false-positive guard in the skill. When the genre is ambiguous, treat it as 事務文體 and say so.

`--expect-author` settles the genre; it does not override the gate. The user passing it is declaring that this draft should show an author, so treat it as 署名文體 and audit it exactly as you would any other. An absence you find under the flag is a finding, not a genre-correct property — the user has taken the genre call on themselves. Say in one line that the verdict rests on their declaration rather than on your own reading of the genre, so a mistaken flag stays visible and cheap to withdraw.

## The exclusion stops here

事務文體 are excluded from **this rule only**. The other 44 rules run on every genre. 作者隱身 asks whether the author is missing; every other rule asks whether something is present that should not be. Those are independent questions, and only the first one is gated by genre — 事務文體 buys a draft nothing on the second.

Route each finding by which question it answers:

- **Something is present that should not be** — 不僅…更、奠定堅實基礎、值得注意的是、成串破折號、諂媚語氣 — goes to its own rule in `zh-rules.md`. Genre never decides whether that rule fires; it only feeds the rule's own 保留 clauses. 「本案不僅將徹底革新既有作業流程，更為未來數位轉型奠定堅實基礎」 in a 簽呈 is 意義膨脹 and 對比句式, flagged, and being 事務文體 changes nothing.
- **The author is missing** — no stance, no lived detail, no self-made image, no colloquial break, no rhythm variation — goes to this rule, and the gate above decides first.

The two verdicts coexist. 「事務文體，作者隱身不適用」 reported alongside three flagged 意義膨脹 spans is the ordinary shape of a 公文 audit, not a contradiction.

## Threshold

Report only when **two or more sub-signals hold at once**. One alone is within the range of ordinary careful writing, and a lone finding sends the author chasing a defect that isn't there.

`作者隱身／只解釋不造像` never counts as a standalone finding, even alongside the threshold rule: dense procedural teaching legitimately runs on fixed idioms and worked examples rather than original metaphor. It corroborates; it does not initiate.

## The five sub-signals

Always name them in the form `作者隱身／<name>`, never bare — two of the five share a name with an independent rule and the prefix is what distinguishes the document-scale reading from the sentence-scale one.

| 子訊號 | 缺席的是什麼 |
|---|---|
| `作者隱身／立場真空` | 全篇找不到一句作者判斷；每個取捨都以「各有優劣」收場。與獨立規則**立場真空**同名，只是讀在文件尺度。 |
| `作者隱身／零具體個人細節` | 沒有一個具體時間、次數、場景、金額；全是定義式陳述。 |
| `作者隱身／只解釋不造像` | 每個難概念都用定義解釋，沒有一個把抽象拉到作者自身經驗的自創比喻。**永不單獨成立。** |
| `作者隱身／無口語破格` | 沒有一處刻意的口語破格：無插入語、無（吧？）、無自問、無刻意殘句。 |
| `作者隱身／節奏均質` | 連續段落長度相近、句長變異低、沒有單句成段、無長短交錯。與獨立規則**節奏均質**同名，只是讀在文件尺度。 |

`作者隱身／無口語破格` has an inverse worth stating: a deliberate colloquial break already present in the draft is a positive feature under 保護清單 item ⑥. Smoothing it out during a rewrite creates the very flatness this sub-signal reports.

## How to report

Name what is absent, quote nothing you would have to invent, and hand the draft back. In `rewrite` mode this section still only reports — repairing it needs experience and judgement the author has and you do not, and a machine filling the gap produces more of exactly what the reader was already sensing.

> 作者隱身（2/5 成立；文體類：署名文體，部落格）
> ・`作者隱身／立場真空` — 三處比較（自架 vs 託管、月繳 vs 年繳、自己維護 vs 外包）都以「各有優缺點」收，全篇沒有一句作者的選擇。
> ・`作者隱身／零具體個人細節` — 沒有一個日期、金額、次數或場景；「曾經遇過問題」未指明是哪一次。
> 建議作者補入：三個比較裡你自己選了哪一個、為什麼；以及那次「遇過問題」的實際時間、狀況與代價。

Division of labour: this skill subtracts noise and reports the absence. Injecting a voice — writing the stance, the metaphor, the anecdote — is additive work and belongs to `blog-writing-zh`. The two compose in that order, and the subtraction is careful not to eat the addition.

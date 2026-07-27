# A/B — v1.0.0 → v1.1.0 (SKILL.md ↔ term-table.md dedup)

Run date: 2026-07-28. Full 12-case picture. Cases 2-9 tested on both arms. Cases 1, 10, 11, 12 tested on v1.1.0 only (see Scope below for why).

Case 5's prompt was rewritten mid-session — the original made 落地 self-redundant with 上線 (see `results-baseline-v1.0.0.md`). Both arms below reflect the fixed prompt; the old 4/6-both-arms figure is superseded.

Method: one independent agent per case per arm, invoking the skill via the Skill tool against the live symlinked copy. Agents saw **only the user prompt**, never the expectations. Judging done separately from returned output and tool traces.

## Result

| Case | Axis | v1.0.0 | v1.1.0 | Both arms? |
|---|---|---|---|---|
| 1 | P0 baseline | — | 3/3 | v1.1.0 only |
| 2 | P1 黑話 長尾 | 4/4 | 4/4 | yes |
| 3 | 生活／口語 長尾 | 3/3 | 3/3 | yes |
| 4 | 音譯專名 長尾 | 3/3 | 3/3 | yes |
| 5 | 術語例外（保留） | 5/6 | 6/6 | yes (fixed prompt) |
| 6 | 術語例外（改掉） | 5/5 | 5/5 | yes |
| 7 | 品牌／引文 carve-out | 4/4 | 4/4 | yes |
| 8 | 同形異義 carve-out | 6/6 | 6/6 | yes |
| 9 | 簡體一對多消歧義 | 4/6 | 5/6 | yes |
| 10 | 整篇簡體（非殘留） | — | 3/3 | v1.1.0 only |
| 11 | detect-only 模式 | — | 5/5 | v1.1.0 only |
| 12 | 字形錯字＋識別字 carve-out | — | 4/4 | v1.1.0 only |
| | **Both-arm subset (2-9)** | **34/37** | **36/37** | |
| | **Full 12-case (v1.1.0)** | — | **51/52** | |

**This clears the bar — not parity.** The earlier 29/31-both-arms read was an artifact of the case-5 eval bug: once the prompt no longer made 落地 self-redundant, v1.0.0 slipped to 5/6 (it hedged, offering an optional swap the expectation forbids) while v1.1.0 held 6/6 (kept it outright, no hedge). Case 9 moved the same direction: v1.0.0 missed the 動詞劃／名詞畫 split (計劃表 for both, should be 計畫表 for the noun) on top of the already-known 消息/一条 vocab-layer gap; v1.1.0 only missed the vocab-layer item. On the 8 cases run on both arms, v1.1.0 beats v1.0.0 34/37 → 36/37.

## What the refactor changed

| Metric | v1.0.0 | v1.1.0 |
|---|---|---|
| SKILL.md lines | 272 | 227 |
| Term rows duplicated across both files | 64 | 25 (the intentional P0 tripwire) |
| Pointers to term-table.md in SKILL.md | 4 | 6 |

A term edit that previously required 5 edits across 2 files (the 複用 change) is now a one-place edit.

## Gains the checklist does not capture

**The `carve-out` gloss fix landed.** v1.0.0's case 7 agent rendered the term 「碳排除項」, reading the English as 碳 (carbon). v1.1.0 agents in cases 5, 7 and 8 all wrote 「排除項」 correctly.

**"Name the specific thing" got stronger.** The rewritten B-section says a synonym swap is not the fix — 「賦能業務」 becomes 「幫業務單位做到 X」, not 「支援業務」. v1.1.0's case 2 agent acted on it, refusing to swap vague for vague and returning the two spots needing the author's own content: 「換掉一個模糊詞卻換上另一個模糊詞，句子還是一樣空——這部分要你補，我不能替你猜」. v1.0.0's case 2 agent produced the synonym swap and only mentioned the emptiness in passing. Case 7 carried the same judgment into quote analysis.

**P2 cluster reasoning transferred.** The rewritten severity section says a cluster of P2s signals a mainland source even when no single one does. v1.1.0's case 3 agent applied exactly that to 立馬／靠譜.

## The routing question, answered

The refactor's central risk was that shrinking the inline core from 93 rows to a 25-row P0 tripwire would break detection when the context pointer failed to fire. It did not fire-fail once, across all 12 cases. Cases 2-9 confirm the pointer fires when it should:

- Case 2: "read in full, because the text is almost entirely axis-B 黑話 and SKILL.md's inline table is a P0 tripwire only"
- Case 3: "needed for 出租車／便利店／公交車／三文魚／奶酪 which are not in SKILL.md's P0 tripwire table"
- Case 4: "the instruction 'any foreign proper noun not among the eight above: look it up' fired correctly and the table resolved every one"

Cases 1 and 11 close the other half of the question — whether a P0-only or short text correctly *skips* the read when the inline tripwire is already sufficient. Case 1 (pure P0 vocabulary: 屏幕／軟件／網絡...) scored 3/3 without needing a table lookup, and case 11 scored 5/5 the same way. The tripwire does prevent lookups on short P0-dominant texts; the earlier "the inline core prevented zero lookups" finding holds only for long-tail-bearing texts, which is what cases 2-8 all were.

## The two misses, settled

**Case 11's 清晰度 — eval over-reach, expectation loosened.** The term is not in `term-table.md` at all, so the eval was requiring a catch the skill never defines. 清晰度 is standard Taiwan usage for image/video clarity, not 陸用語. Removed from `catches-rest`; case 11 rescored 4/5 → 5/5. This changes the eval, not the skill, so the run above remains valid.

**Case 9's 消息／一条 — real skill gap, kept strict.** Both arms left them; v1.0.0's agent stated outright 「消息：兩岸用字用詞皆同，無需更動」. It is not: 「發了一則訊息」 is the natural Taiwan phrasing and 一条 is a mainland classifier. `term-table.md` lists 信息 but not 消息, and no classifier rules at all. Expectation stands; the fix is a term-table addition, logged in `backlog.md`. Deliberately **not** fixed in this branch — editing the table now would mean the committed results no longer describe the shipped skill.

## Scope limit

Cases 1, 10, 11, 12 ran on v1.1.0 only (selective dual-arm, agreed in advance to cap cost) — no direct v1.0.0 comparison exists for these four. The "beats baseline" claim rests on the 8 both-arm cases, not on the 12-case total.

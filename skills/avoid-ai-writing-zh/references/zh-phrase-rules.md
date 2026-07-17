# 繁體中文 AI 用詞對照表（zh-TW / 台灣用語）

The six enumerable word/phrase → replacement lookup tables for the Traditional Chinese section of `avoid-ai-writing-zh`. Load this file when auditing CJK text and you need a concrete「這個詞→換成這個」lookup — empty slogans, the 確保 filler family, significance-inflation words, AI sentence templates, individual-term substitutions, and Taiwan term preferences.

Everything else in the zh layer stays inline in `SKILL.md` under 「Traditional Chinese AI-isms」: the behavioral rules that need judgment rather than lookup (空降斷言／空降主張, 頓號串列, 口語化萬能動詞, 過度簡寫, 破折號濫用, 警句式評語, 破碎短句堆疊, 打破第四面牆, 結構級訊號, 專有名詞過度翻譯, and the contrarian / copula / adjective-stacking micro-rules), the abstract→concrete rewrite table, and the do-not-flag Allowed-patterns carve-outs. Apply both together.

## Empty slogans (空話／口號) — always replace

Delete or rewrite into a concrete claim. These add no decision, requirement, deliverable, or fact.

| Flag | Why it's empty | Fix |
|---|---|---|
| 全面提升 / 全面強化 | "全面" claims totality without scope | Name what improves and by how much |
| 有效賦能 / 賦能 | borrowed from PRC corp-speak; says nothing | State the specific capability granted |
| 打造完整生態 / 完整生態系 | ecosystem-as-metaphor filler | Describe the actual components and how they connect |
| 建立堅實基礎 / 奠定基礎 | vague foundation metaphor | State what is built and what it enables |
| 邁向新里程碑 | inflates routine progress into history | State what was completed |
| 深化整體效益 / 綜效 | abstract benefit-speak | Cite the concrete benefit (a number, an output) |
| 持續優化 / 持續精進 | open-ended, unfalsifiable | Name the next concrete change and when |
| 數位轉型賦能 / 一站式 / 端到端解決方案 | brochure compounds | Describe the specific scope or workflow |

## Filler words — strip or replace (the 確保 family)

Individually these can be fine; in formal AI-generated Chinese they cluster as connective padding. Replace on sight in cluster.

| Flag | Fix |
|---|---|
| 確保 (as "make sure" filler) | 使 / 讓, or state the mechanism that guarantees it |
| 從而 / 進而 | delete; start a new clause or use 因此 once |
| 旨在 / 致力 / 致力於 | state the goal directly: 「本案目標為…」 |
| 全面地 / 有效地 / 充分地 (adverb padding) | delete the adverb; let the verb carry it |
| 透過…的方式 | 以…／用… (drop 的方式) |
| 進行…的動作 / 做出…的決定 | use the plain verb: 執行／決定 |

## Significance inflation — 至關重要 / 不言而喻

Words that announce importance instead of showing it: 至關重要, 不言而喻, 眾所周知, 不容忽視, 顯而易見. Delete, or state concretely *why* it matters (a consequence, a number).

## AI sentence templates

Default opening frames that signal generation. Delete the frame; state the fact.

- 在當今…的時代 / 在這個…的世代
- 隨著…的快速發展 / 隨著…的日益普及
- 值得一提的是 / 值得注意的是 (the Chinese "It's worth noting that")
- 這不僅…更是… / 這標誌著…
- 具體而言 **only when** no concrete items follow (as a list intro before real items, it is fine — see the Allowed patterns carve-outs in `SKILL.md`)

## AI 慣用詞替換（個別用詞對照）

AI 偏好的譬喻詞或英文術語直譯，在台灣商務／技術寫作中有更精準的對應詞。逐詞替換，**carve-out** 欄列出仍應保留原詞的語境。

| Flag | 為何不精準 | Fix | Carve-out（保留原詞） |
|---|---|---|---|
| 節奏（用於時程／進度語境，如「專案節奏」「開發節奏」） | 把英文 rhythm／cadence 的譬喻套到時程上；中文應直接指明時間規劃 | 期程（時間規劃）／排程（具體時間表，依語境擇一） | 真正描述音樂、運動、敘事的「節奏感」時保留 |
| 編排（用於 orchestration，如「服務編排」「流程編排」） | orchestration 直譯為「編排」偏向版面／內容編排語意，與調度資源、協調流程的原意不符 | 調度 | 描述版面、內容、表演、課程「編排」時保留 |
| 跳（用於 network hop，如「多一跳」「少一跳」「每跳延遲」） | network hop 的直譯；圈外讀者不知道「跳」的是什麼，句中也沒有動作與對象 | 寫明動作與對象：「請求多經過一個轉發節點（network hop）」「每經過一個節點就增加一段轉發延遲」 | 明確面向網路工程讀者、且文中已定義 hop 一詞時，可用「hop」原文 |

## Taiwan term preferences (zh-TW, not zh-CN)

When rewriting, prefer Taiwan-standard terms: 計畫 (not 计划), 規劃, 執行, 檢核, 驗收, 廠商, 資訊, 專案, 承辦單位, 權責單位, 待辦事項, 後續追蹤, 期程, 排程, 調度. Avoid PRC-style phrasing (賦能, 抓手, 落地, 閉環, 顆粒度, 對齊顆粒度) unless quoting source material.

**For a dedicated 陸用語 → 台灣正體 pass, use the `avoid-china-writing` skill.** This section is a light touch — it catches PRC phrasing only where it overlaps AI 空話. The sibling `avoid-china-writing` skill is the deep pass: a full 詞彙對照表 (視頻→影片、軟件→軟體、屏幕→螢幕), 互聯網／職場黑話, 簡體字殘留偵測, and 音譯專名差異 (奧巴馬→歐巴馬). Cross-strait localization is an axis orthogonal to AI-ism cleanup; this skill completes the de-AI job on its own regardless. If the writer *also* wants a 陸用語 pass, `avoid-china-writing` handles that separate axis.

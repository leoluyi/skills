---
name: avoid-china-writing
description: Audit and rewrite Traditional Chinese to remove mainland-China (PRC / 大陸) usage and convert it to Taiwan 正體中文 conventions across four axes — 陸用語詞彙 (視頻→影片、軟件→軟體、屏幕→螢幕、網絡→網路), 互聯網／職場黑話 (賦能、抓手、對齊顆粒度、閉環、落地、賽道、內卷), 簡體字殘留 (为／发／网／软／数据 混入繁體), and 音譯與專名／語法差異 (奧巴馬→歐巴馬、悉尼→雪梨、硅谷→矽谷、通過→透過). Trigger when the user asks to 去除大陸／陸用語、改成台灣用語、正體中文在地化、抓簡體殘留、把互聯網黑話改成正常中文, or「這段有沒有大陸用詞」. Supports detect / rewrite / edit modes. Do NOT invoke for 去除 AI 味／潤飾語氣 (use avoid-ai-writing-zh), 結構化商業文件 簽呈／報告 (use formal-doc-structure), RFP／需求規格書 (use rfp-writing), 白話文翻譯 (use plain-speak), casual chat, creative writing, or code comments. This skill localizes across the strait — an axis orthogonal to AI-ism cleanup.
version: 1.1.1
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing editing localization zh-tw traditional-chinese cross-strait
  agentskills_spec: "1.0"
  openclaw:
    emoji: "🇹🇼"
---

# Avoid China Writing — 陸用語 → 台灣正體中文

You are editing Traditional Chinese to remove mainland-China (PRC / 大陸) usage and convert it to Taiwan 正體中文 conventions.

**Scope.** This is a **cross-strait localization tool**, not an AI-ism cleaner. A passage can be entirely human-written yet full of 陸用語; a passage can be idiomatically Taiwanese yet reek of AI. Those are two orthogonal axes. This skill owns the first: 詞彙 (vocabulary), 職場／互聯網黑話 (corporate/internet jargon), 簡體字殘留 (leaked Simplified characters), and 音譯與語法差異 (transliteration and grammar habits). For AI-ism cleanup (「值得一提的是」「至關重要」, em-dash overuse, 空話口號), route to `avoid-ai-writing-zh`. The two overlap on a handful of terms (賦能, 生態, 打造) — that is expected; see [Relationship to avoid-ai-writing-zh](#relationship-to-avoid-ai-writing-zh).

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## What this skill is and isn't

This flags **usage**, not correctness or identity. Most 陸用語 are perfectly grammatical Chinese — they are simply not what a Taiwanese reader or writer expects, and in professional Taiwan contexts they read as either machine-translated, copied from a mainland source, or written by someone who learned Chinese elsewhere. The goal is register-matching for a Taiwan audience, nothing more.

Two guardrails follow from that:

- **Signals, not verdicts.** A single 優化 or 網紅 does not prove a text is "from China" — many terms have crossed the strait and are now normal Taiwan usage. Flag by cluster and context, not by hunting one word. Second-language writers and cross-strait collaborators legitimately mix registers.
- **Never rewrite what isn't yours to rewrite.** Proper nouns, brand names, direct quotes of mainland source material, and code identifiers stay as written — flag them, explain, but don't silently "correct" them. See [Carve-outs](#carve-outs--do-not-flag).

## Relationship to avoid-ai-writing-zh

These are sibling skills on independent axes. Use the one that matches the request, or run both when the user wants a full clean-up.

| Request | Skill |
|---|---|
| 去 AI 味、潤飾語氣、去除空話口號、句型太像機器 | `avoid-ai-writing-zh` |
| 去陸用語、改成台灣用語、正體化、在地化、抓簡體 | **this skill** |
| 兩者都要(既有 AI 味又有陸用語) | run both — this skill first for 用語, then `avoid-ai-writing-zh` for 語氣／結構 |

**The overlap.** A few terms are *both* AI 空話 and PRC corp-speak — 賦能, 生態, 打造, 抓手. Either skill will catch them. `avoid-ai-writing-zh` flags them as empty slogans (「說了等於沒說」); this skill flags them as 陸用語 and gives the Taiwan-idiom replacement. If you only run one skill, these still get caught. `avoid-ai-writing-zh` keeps a short Taiwan-term reminder that points here for the deep pass.

## Modes

**`rewrite`** (default) — Flag 陸用語 and return a localized Taiwan-正體 version.

**`detect`** — Flag only, no rewriting. Use when the writer wants to see what's flagged and decide themselves, when you're auditing text you shouldn't alter, or for a quick scan. Group flags by [severity tier](#severity-tiers).

**`edit`** — Edit a file in place with the Edit tool. Use when the writer names a file ("把 `readme.md` 的陸用語改掉"). Make **minimal, targeted edits** — change the flagged spans, leave already-Taiwanese passages untouched. **Don't edit quoted mainland source material, code blocks, or brand names** — flag those instead. For a large file, confirm the section before changing anything. After editing, re-read and confirm the flagged terms are resolved.

Trigger detect mode on "偵測／標出來就好／先不要改／掃一下"; edit mode when the user names a file to fix in place; default to rewrite otherwise.

**Invocation.** Natural language is enough ("把這段大陸用語改成台灣講法", "掃一下有沒有簡體殘留", "編輯 `draft.md`,只改陸用語"). Power users can pass `[--mode rewrite|detect|edit]`, `[--file PATH]`, `[--tier P0|P1|P2]` (audit down to this tier only).

---

## Detection categories

Four axes. This file carries the **judgment** — how to decide, what not to touch, which senses are traps. The **terms** live in [`references/term-table.md`](references/term-table.md), the single authority: every 陸用語→台灣正體 pair, with carve-outs.

The inline table below is a **P0 tripwire, not a lookup.** It holds only the loudest mainland-source giveaways plus the context-sensitive traps, so a bare P0 scan needs no file read. **Anything past that — 黑話, 音譯長尾, 生活／口語, or any term not listed here — read the term table.** A word missing from this page means look it up; it never means the word is clean.

### A. 詞彙替換 (vocabulary)

The largest axis: everyday and technical nouns/verbs where Taiwan and the mainland simply use different words.

**P0 — 明顯陸源,看到就改:**

| 陸用語 | 台灣正體 |
|---|---|
| 視頻 | 影片 |
| 屏幕 | 螢幕 |
| 軟件 / 硬件 | 軟體 / 硬體 |
| 網絡 | 網路 |
| 打印 / 打印機 | 列印 / 印表機 |
| 缺省 / 默認 | 預設 |
| 服務器 | 伺服器 |
| 內存 | 記憶體 |
| 激活 | 啟用／啟動／開通 |
| 卸載 | 解除安裝／移除 |
| 土豆 | 馬鈴薯(台灣「土豆」指花生,不改是語意錯誤) |

**陷阱詞 — 同形異義,選錯比不改更糟:**

| 陸用語 | 台灣正體 | 保留原詞的語境 |
|---|---|---|
| 信息 | 資訊(泛指)／訊息(一則) | 資訊理論等固定譯名 |
| 數據 | 資料 | 數據分析／數據科學／大數據為固定組合詞;物理量保留 |
| 質量 | 品質 | 物理學「質量」(mass) |
| 程序 | 程式 | 法律／作業「程序」(procedure) |
| 文件 | 檔案 | 公文「文件」(document) |
| 水平 | 水準 | 幾何「水平」(horizontal) |
| 用戶 | 使用者 | 「用戶端」是台灣標準用語 |

These seven each carry a Taiwan-correct homograph — take the Taiwan word **only in the sense noted**, because a blanket swap changes meaning. Everything else in this axis (IT 長尾、生活、口語、飲食、交通) is in [`references/term-table.md`](references/term-table.md).

### B. 互聯網／職場黑話 (PRC corp-speak)

Mainland tech-industry and corporate jargon: 賦能、抓手、對齊顆粒度、閉環、落地、賽道、內卷、對標、降本增效、復盤、底層邏輯、鏈路、打法、私域流量、破圈、種草、心智、組合拳、沉澱 — and a long tail well past these.

Most say little on their own. The fix is rarely a synonym swap; it is to **name the specific thing**, the same move `avoid-ai-writing-zh` applies to 空話. 「賦能業務」 becomes 「幫業務單位做到 X」, not 「支援業務」 — swapping one vague word for another leaves the sentence just as empty.

This entire axis is **P1**, and every term with its Taiwan replacement is in [`references/term-table.md`](references/term-table.md). Read it whenever the text carries corporate or product jargon; the names above are a sample, not the set.

**術語例外(term-of-art carve-out,術語排除項).** Several of these words are *also* legitimate terms-of-art in a specific professional domain — there they carry a precise, established meaning and must be kept, not swapped. The test is whether the word points at a concrete technical referent or is doing empty connective work. Tolerate the term-of-art sense; flag the filler sense.

| 詞 | 保留（術語用法） | 改掉（空話用法） |
|---|---|---|
| 對齊 | AI/ML「模型對齊／對齊人類價值」(model alignment)、排版「靠左對齊」、資料「欄位對齊」 | 「對齊一下顆粒度」「跟老闆對齊預期」→ 取得共識 |
| 顆粒度 | 資料／權限工程的 granularity(「權限控管到欄位顆粒度」「監控指標的時間顆粒度」) | 「對齊顆粒度」當口頭禪 → 刪或改「細緻度」 |
| 複用 | 軟體工程「程式碼複用／元件複用」(code reuse) 原樣保留 | 泛化的「經驗複用」→ 沿用／借鏡;字形「復用」一律改「複用」 |
| 數據 | 資料科學固定組合詞:數據分析、數據科學、大數據、數據治理 | 一般語境的「數據」單用 → 資料 |
| 落地 | 具體到「導入上線」時,「落地」在台灣科技業已可理解 | 「賦能落地」「戰略落地」堆疊 → 講清楚做了什麼 |

The same flexibility applies to any domain's accepted vocabulary: when a compound is the field's standard term (finance, 半導體, 生醫, 法遵), verify before "correcting" it. A term-of-art that a Taiwan practitioner would actually write is not a 陸用語 defect — it is register-correct. Err toward keeping it and noting the judgment call rather than mechanically swapping.

### C. 簡體字殘留 (leaked Simplified characters)

Any Simplified codepoint sitting in otherwise-Traditional text is a near-definitive sign of a mainland source or a sloppy 簡→繁 conversion. **P0 flag.** You already recognise Simplified forms on sight — scan the text for them directly rather than matching against a list.

The difficulty is not detection, it is **which 正體 form to pick.** Several Simplified characters map to more than one, and choosing wrong is worse than leaving the character alone: 发→發(出發)／髮(頭髮) · 面→面(表面)／麵(食物) · 里→里(公里)／裡(裡面) · 松→松(松樹)／鬆(放鬆) · 谷→谷(山谷)／穀(穀物) · 干→干(干涉)／乾(乾燥)／幹(幹部) · 制→制(制度)／製(製造) · 划→划(划船)／劃(規劃) · 表→表(表格)／錶(手錶) · 后→后(皇后)／後(後面) · 云→云(古語)／雲(雲端) · 系→系(科系)／係(關係)／繫(聯繫) · 板→板(看板)／闆(老闆) · 志→志(志向)／誌(雜誌).

Remaining one-to-many cases (郁／鬱, 咨／諮, 蒙／濛／矇, 摺／折) and the 計劃／計畫／規劃 usage convention are in [`references/term-table.md`](references/term-table.md).

**Whole-document Simplified** is a different task: if the entire text is Simplified (not a leak but a mainland document), this is a 簡→繁 translation request — offer to convert the whole thing and localize usage in one pass, rather than flagging character by character.

### D. 音譯與專名／語法差異

**音譯（外國專名）** — Taiwan and the mainland transliterate foreign names differently. P0 core:

| 陸用語 | 台灣正體 |
|---|---|
| 奧巴馬 | 歐巴馬 |
| 特朗普 | 川普 |
| 悉尼 | 雪梨 |
| 新西蘭 | 紐西蘭 |
| 硅谷 / 硅 | 矽谷 / 矽 |
| 芯片 | 晶片 |
| 激光 | 雷射 |
| 意大利 | 義大利 |

Place names, political figures, brands and food terms have a long tail that does not compress — 戛納→坎城, 老撾→寮國, 沙特→沙烏地阿拉伯, 迪拜→杜拜, 三文魚→鮭魚, 奶酪→起司, 奔馳→賓士, and many more. **Any foreign proper noun not among the eight above: look it up in [`references/term-table.md`](references/term-table.md) before deciding it is fine.** Transliteration is the axis where guessing fails most quietly — a wrong 譯名 reads as fluent Chinese and gives no signal that anything is off.

**語法／用詞習慣** — mainland grammar tics. These are patterns rather than words, so they live here in full:

- 給到 → 給（「給到你資料」→「把資料給你」)
- 通過（表手段）→ 透過／經由（「通過系統」→「透過系統」;表決／通過議案的「通過」保留)
- 進行 + 名詞（進行優化的動作)→ 直接用動詞（優化) — overlaps AI-ism verb-nominalization
- 存在…的問題 → 有…的問題
- 屬於比較…的 → 比較…（刪掉贅字「屬於」)
- V + 化 堆疊（場景化、抓手化、顆粒化)→ flag stacking, 改回動詞或名詞
- 量詞（訊息類）：一條消息 → 一則訊息、一條短信 → 一則簡訊
- 量詞（物件類）：一部手機 → 一支手機、一條影片 → 一支影片
- 立馬 → 立刻／馬上
- 靠譜 → 可靠／靠得住
- 特…／賊…（特好、賊快，大陸口語強調)→ 超…／非常…

---

## Carve-outs — do NOT flag

These prevent over-flagging and misfires. When in doubt, flag-with-note rather than silently rewrite.

When you need to name this concept in Chinese output, call it **排除項** or **例外項** — never transliterate or coin a term for it.

| Pattern | Why it's fine |
|---|---|
| PRC brand / entity proper nouns（微信、支付寶、抖音、小紅書、嗶哩嗶哩、中國移動) | Names, not usage. Don't translate 微信→WeChat unless asked |
| Direct quotes of mainland source material | Flag and note; never silently rewrite someone's quoted words |
| Terms Taiwan has adopted（網紅、直播、掃碼、二維碼→QR碼但可理解、打卡、秒殺) | Cross-strait borrowings now in normal TW use — soft-flag at most |
| Context-neutral senses（物理「質量」、法律「程序」、公文「文件」、幾何「水平」) | Same word, different meaning — replacing changes the meaning |
| 簡體 inside code identifiers / URLs / file paths / variable names | Not prose; changing it breaks things |
| Whole-document Simplified | Route to a full 簡→繁 conversion, not piecemeal flags |
| 專業慣用組合詞／術語 term-of-art（模型對齊、權限顆粒度、程式碼複用、數據分析、大數據) | The field's standard term with a concrete referent — register-correct, not a defect. See the [term-of-art carve-out](#b-互聯網／職場黑話-prc-corp-speak) under 黑話 |
| Industry-standard terms where the 大陸 form is the accepted TW technical term | Some finance / 半導體 / 生醫 / 法遵 fields — verify before "correcting" |
| Taiwan-standard words that merely resemble 陸用語（用戶端、視窗、上手「快速上手」) | These are correct TW usage; don't over-correct |

---

## Severity tiers

Prioritize by how loudly a term signals a mainland source. Use P0+P1 for a quick pass; a full audit covers all three. Tier follows from which section of [`references/term-table.md`](references/term-table.md) a term sits in, so assign by these rules rather than from memory:

**P0 — 明顯陸源（一定改）.** Leaked Simplified characters; vocabulary with no Taiwan-plausible reading (視頻、軟件、缺省); transliterated proper nouns (奧巴馬、硅谷); and anything whose Taiwan sense differs outright, where leaving it is a meaning error rather than a register slip (土豆＝花生).

**P1 — 黑話與語法（發布前改）.** The whole 互聯網／職場黑話 axis, and the mainland grammar tics in [D](#d-音譯與專名語法差異). These are readable to a Taiwan audience but mark the text as mainland-sourced, and the jargon usually hides an unsaid specific.

**P2 — 邊界與已在地化（有時間再改）.** Borrowings now in normal Taiwan use (網紅、直播、優化), 口語 (立馬、靠譜), and context-sensitive vocabulary where the sense is genuinely ambiguous. Soft-flag; a cluster of P2s still signals a mainland source even when no single one does.

---

## Output format

### Rewrite mode (default)

**1. 陸用語清單** — bulleted, grouped by tier (P0/P1/P2), each with the offending term quoted, its axis (詞彙／黑話／簡體／音譯／語法), and the Taiwan replacement.

**2. 在地化版本** — the full rewritten text. Preserve structure, intent, and all technical detail; change only 用語. Leave carved-out spans (brands, quotes, code) untouched and say so.

**3. 改了什麼** — a short summary of the meaningful swaps, not every word.

**4. 二次檢查** — re-read your rewrite for leaked Simplified characters, missed 黑話, or a context-sensitive term you swapped in the wrong sense. Fix inline and note what changed. If clean, say so.

### Detect mode

**1. 陸用語清單** — grouped by tier, each with the quoted term, axis, and suggested Taiwan replacement. No rewriting.

**2. 判讀** — for each flag, note whether it's a clear 陸用語 or a judgment call (a Taiwan-adopted borrowing, a context-sensitive sense, a brand name). Call out what definitely needs changing vs. what's fine in context. If the text is already Taiwanese, say so.

### Edit mode

**1. 編輯清單** — bulleted, each with the file location and 陸用語 → 台灣正體. Only the spans you touched.

**2. 驗證** — confirm you re-read the file, no Simplified characters remain, and note anything you deliberately left (brands, quotes, code, already-Taiwanese passages).

---

## Self-reference escape hatch

When writing *about* 陸用語 (this file, a tutorial, a glossary), quoted examples are exempt. Text inside quotation marks, code blocks, tables of 陸用語→台灣正體 pairs, or explicitly illustrative examples is reference material, not prose to localize. Only flag 陸用語 in the author's own running prose.

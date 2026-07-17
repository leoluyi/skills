---
name: avoid-ai-writing-zh
description: >-
  Audit and rewrite content to remove AI writing patterns ("AI-isms") in BOTH English and Traditional Chinese (Taiwan / 台灣 business usage). Use when asked to "remove AI-isms," "clean up AI writing," "make this sound less like AI," 或「去除 AI 味」「把這段中文改成人話」「把規劃書／報告書／知識文件或 README／開發文件定稿前去 AI 味」. Also use as a de-AI finishing pass when finalizing or reviewing English/mixed software-development docs — README, CONTRIBUTING, CHANGELOG, ADR, API docs, code comments. Adds a Traditional-Chinese layer the English-only avoid-ai-writing lacks: 空話口號 (全面提升／賦能), 不是…而是… contrarian structure, copula inflation (作為／扮演著), significance inflation (至關重要), AI 句式 (在當今…的時代), and 專有名詞過度翻譯／生造中文譯名 (house rules→房規；無定譯保留原文). Supports detect / rewrite / edit modes, voice profiles, and an iterate-to-convergence pass. Other authoring skills (formal-doc-structure, rfp-writing, briefing-outline) reach this as a finishing pass. Prefer this over avoid-ai-writing whenever the text is Traditional Chinese, mixed zh/en, or software-development docs. This skill removes AI patterns; it does not create a voice — to inject human voice or restructure a blog draft, use blog-writing-zh first, then run this as the finishing pass.
version: 1.2.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Conor Bronsdon
  adapted_by: Lu Yi
  adaptation: Traditional Chinese (Taiwan) AI-ism layer added; mined from personal rfp-writing and formal-doc-structure skills. Forked from upstream avoid-ai-writing v3.10.0 (MIT).
  tags: writing editing voice quality zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\u270D\uFE0F"
---

# Avoid AI Writing (zh-TW) — Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

**Language.** This fork handles English and Traditional Chinese (Taiwan business usage). Detect the dominant language from the input: if the text contains CJK characters, apply the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section in addition to any English rules that fit; for pure-English text, the English rules below are the whole job. In mixed zh/en text, audit each language with its own ruleset — do not romanize Chinese or translate English to "fix" it. Keep standard English technical terms (API, Kubernetes, CI/CD) in English inside Chinese prose; that is correct Taiwan usage, not an AI tell.

## What this skill is and isn't

This is a **writing-quality tool**, not a verdict. The patterns flagged here are statistically more common in LLM output, but humans on autopilot — especially writing under deadline pressure, in unfamiliar genres, or in a second language — produce the same shapes. Independent audits of commercial AI detectors have found false-positive rates above 60% on non-native English writers (Liang et al., Stanford, *Patterns* 2023) and false-positive rates as high as 78% on open-source detectors, misclassifying human text as AI (Jabarian & Imas, BFI Working Paper 2025-116, 2025). Adversarial paraphrase cuts detectors' true-positive rate by ~88% on average (64–99% across the methods tested; arXiv:2506.07001, 2025).

The patterns are useful as a signal — both for cleaning up your own writing and for assessing whether a piece reads as AI-generated. Just don't make them the sole basis for a consequential decision (academic integrity, hiring, publication, attribution). Several rules here also fire on second-language writing, deadline-pressed humans, and technical genres that compress vocabulary by design. Pair the signal with context: who wrote it, what genre, what the writer's normal voice looks like, what other evidence you have.

In short: signals, not proof. Worth acting on; not worth ruining someone's day over.

## Modes

This skill operates in one of three modes:

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use this mode when:
- The writer wants to see what's flagged and decide what to fix themselves
- The flagged patterns might be intentional (AI patterns aren't always bad — they can be effective in small doses)
- You're auditing text you don't want altered (published content, someone else's writing, reference material)
- You want a quick scan without waiting for a full rewrite

**`edit`** — Edit a file in place rather than returning rewritten text. Use this when the writer points you at a file ("clean up `draft.md`", "fix the AI-isms in this file directly") and wants the file changed, not a copy to paste back. Make **minimal, targeted edits** with the Edit tool — change the flagged spans, not the whole document. **Preserve passages that are already human**: if a paragraph has no tells, leave it untouched. **Don't edit quoted material, code blocks, or text attributed to someone else** — flag those instead of rewriting them. For a large file, confirm which section to clean before changing anything. After editing, re-read the file and confirm the flagged patterns are resolved.

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," "what AI patterns are in this," or similar. Trigger edit mode when the user names a file and asks you to fix or clean it in place. Default to rewrite mode if not specified.

**Invocation.** Natural language is enough ("rewrite this in a blunt voice for LinkedIn," "edit `post.md` in place," "scan this, don't rewrite"). Power users can also pass explicit options, which map to the sections below: `[--mode rewrite|detect|edit]`, `[--voice casual|professional|technical|warm|blunt]`, `[--context linkedin|blog|technical-blog|investor-email|docs|casual]`, `[--file PATH]`, `[--iterate N]` (max 2), `[--structure-signals]` (see [結構級訊號](#結構級訊號zh-tw-部落格聲音)).

**Iterate to convergence (optional).** Rewrite mode already runs one corrective second pass (see Output format) — that built-in pass *is* pass 2, so `--iterate` does not stack on top of it. When the writer asks to "iterate," "keep going until it's clean," or passes `--iterate N`, repeat the audit→rewrite cycle until no patterns remain or **N passes** are reached. Cap **N at 2**: a rewrite plus one corrective pass clears the flagged patterns, and a third pass costs a full regeneration while rarely finding more. Report how many passes it took ("converged in 2 passes").

---

In **rewrite** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Rewrite it**: return a clean version with all AI-isms removed
3. **Show a diff summary**: briefly list what you changed and why

In **detect** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Assess it**: note which flags are clear problems vs. patterns that may be intentional or effective in context

In **edit** mode, your job is to:

1. **Read** the file the writer named
2. **Edit in place**: apply minimal, targeted fixes to the flagged spans with the Edit tool, leaving already-human passages untouched
3. **Verify**: re-read the file and confirm the flagged patterns are resolved; report what you changed

---

## What to remove or fix

The English-specific detection rules — formatting tells, sentence-structure tells, the tiered word/phrase replacement tables (Tier 1/2/3), and the micro-categories from template phrases through excessive structure — live in **[references/english-rules.md](references/english-rules.md)**. Read that file when auditing English or mixed zh/en text; it is the bulk of the English ruleset. The language-agnostic structural rules below (rhythm, vocabulary diversity, paragraph-reshuffle, treadmill, when-to-rewrite) apply to any language, and the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section handles CJK.

### Rhythm and uniformity

These aren't individual word or phrase problems — they're patterns in how the text flows as a whole. AI text is metronomic; human text has varied rhythm.

**Structure is the #1 detection signal.** AI detection tools (including Pangram, which trains a classifier on 28M human documents) weight structural regularity higher than vocabulary. Consistent sentence construction, uniform pacing, and symmetrical phrasing patterns are harder to mask than swapping out a few flagged words. If you fix every word on the Tier 1 list but leave the rhythm untouched, the text still reads as AI-generated.

- **Sentence length uniformity**: If most sentences are 15–25 words, the text sounds robotic. Mix short punchy sentences (3–8 words) with longer flowing ones (20+). Fragments work. Questions break the monotony.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and roughly the same size, vary deliberately. Some paragraphs should be one sentence. Some should be longer.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word mechanically or cycles through synonyms conspicuously. Human writers repeat when the word is right and vary when it's natural — there's no formula.
- **Read-aloud test**: If the text sounds like it could be read by a text-to-speech engine without sounding weird, it's probably too uniform. Human writing has rhythm that resists robotic delivery.
- **Missing first-person perspective**: Where appropriate, the writer should have opinions, preferences, and reactions. AI is relentlessly neutral. If the piece is supposed to have a voice, the absence of "I think," "in my experience," or a stated preference is itself an AI tell.
- **Over-polishing**: Aggressively editing out every irregularity can push human writing *toward* AI statistical profiles. Natural disfluency, idiosyncratic word choices, and uneven pacing are what keep text out of the "AI-generated" classification. Don't sand away all personality in pursuit of clean prose. This skill should make writing sound more human, not less — if you apply every rule at maximum strictness, you risk creating the very uniformity you're trying to avoid.

### Vocabulary diversity (stylometric)

In longer pieces (200+ words), look at how much vocabulary the text actually uses. The type-token ratio (TTR) — distinct word types divided by total tokens — is a classical stylometric signal that's easy to read by eye. Human prose at this length usually lands somewhere around 0.50–0.65 in English. AI text trends flatter, sometimes drifting under 0.40 when the model gets locked on a small vocabulary loop.

A very low TTR is not by itself proof of AI authorship — narrow topics, technical reference material, and second-language writing all legitimately compress vocabulary. But on general prose where you'd expect range (essays, articles, social content over ~200 words), a TTR below 0.40 is worth a second look. The fix is rarely to thesaurus the text; it's to broaden the *what* — name specific things, cite specific cases, replace a re-used abstract noun with the concrete instance behind it.

This is the first of four stylometric signals on the roadmap. The others (sentence-length burstiness as a continuous measure, function-word z-scores against a human-prose reference, POS-bigram log-odds) require either a POS tagger or a reference distribution and aren't implemented as detector categories yet.

### Paragraph-reshuffle immunity (structure test)
- A writer-side diagnostic, not a regex: can you swap two body paragraphs without breaking the piece? If the order doesn't matter, you've written a list of points, not an argument that builds. AI prose often fails this — each paragraph is a self-contained module with no load-bearing connection to its neighbors.
- The fix is structural, not lexical: establish a through-line where each paragraph depends on the one before it. If the paragraphs are genuinely independent, decide whether the piece should be an explicit list, or whether it's missing a thesis. Adapted from `Aboudjem/humanizer-skill` P38.

### Treadmill effect / low information density (content test)
- Another writer-side test: read each paragraph and ask "what's actually new here?" AI prose frequently restates the premise in fresh words instead of advancing it — lots of motion, no distance covered. The tell is that you could cut 40-60% and lose no information.
- The fix: for each paragraph, name the one fact, claim, or turn it contributes. If there isn't one, cut it. If there is, lead with it and drop the throat-clearing. Adapted from `Aboudjem/humanizer-skill` P43.

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+ distinct pattern categories triggered, and uniform sentence/paragraph length, patching individual phrases won't fix it — the structure itself is AI-generated. Advise a full rewrite: state the core point in one sentence, then rebuild from there.

---

## Traditional Chinese AI-isms (繁體中文／台灣用語)

Apply this section whenever the text contains CJK. These are the Chinese analogues of the English patterns above, plus filler shapes specific to Taiwan business and formal writing. Mined from the `rfp-writing` and `formal-doc-structure` skills.

**A caution before flagging.** Several of these patterns also appear in legitimate formal Taiwanese business writing — 公文, 簽呈, 法遵文件 — and in second-language writers. They are signals, not proof (the same "signals, not proof" rule from [What this skill is and isn't](#what-this-skill-is-and-isnt) applies). Flag the *empty* instances; keep the ones doing real work. The carve-outs at the end of this section exist to stop over-flagging.

### Empty slogans (空話／口號) — always replace

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

### Filler words — strip or replace (the 確保 family)

Individually these can be fine; in formal AI-generated Chinese they cluster as connective padding. Replace on sight in cluster.

| Flag | Fix |
|---|---|
| 確保 (as "make sure" filler) | 使 / 讓, or state the mechanism that guarantees it |
| 從而 / 進而 | delete; start a new clause or use 因此 once |
| 旨在 / 致力 / 致力於 | state the goal directly: 「本案目標為…」 |
| 全面地 / 有效地 / 充分地 (adverb padding) | delete the adverb; let the verb carry it |
| 透過…的方式 | 以…／用… (drop 的方式) |
| 進行…的動作 / 做出…的決定 | use the plain verb: 執行／決定 |

### Contrarian structure — 不是…而是… / 不僅…更…

The Chinese twin of English "It's not X — it's Y." State the positive directly.

> Poor: 本案不是單純導入工具，而是建立完整管理機制。
> Better: 本案同步建立工具設定、作業流程、權責分工、檢核表及後續追蹤機制。

Also flag: 不僅…更能…, 與其…不如…, 並非…而是… when used to manufacture contrast rather than state a real boundary. **Carve-out:** a factual boundary is fine — 「管理粒度是資料集，不是租戶」states a real distinction, not a rhetorical flourish.

### Copula inflation — 作為 / 扮演著…的角色

AI avoids 是/有 with fancier verbs, the way English avoids "is" with "serves as."

> Poor: 本系統扮演著資料中樞的角色。
> Better: 本系統是資料中樞。

Flag 作為 only when it inflates a simple "is." **Carve-out:** 「以 X 作為 Y 引擎」(stating a technology choice) is factual role assignment — keep it.

### Significance inflation — 至關重要 / 不言而喻

Words that announce importance instead of showing it: 至關重要, 不言而喻, 眾所周知, 不容忽視, 顯而易見. Delete, or state concretely *why* it matters (a consequence, a number).

### AI sentence templates

Default opening frames that signal generation. Delete the frame; state the fact.

- 在當今…的時代 / 在這個…的世代
- 隨著…的快速發展 / 隨著…的日益普及
- 值得一提的是 / 值得注意的是 (the Chinese "It's worth noting that")
- 這不僅…更是… / 這標誌著…
- 具體而言 **only when** no concrete items follow (as a list intro before real items, it is fine — see carve-outs)

### 空降斷言開場（沒頭沒腦丟一個 term 或 claim）

AI 常在段落或小節開頭空降一個名詞或一句戲劇化斷言，不鋪陳就要讀者買單——例如「三個失效機制，全部指向同一件事」。問題在於它預設了讀者還不知道的資訊：哪三個失效機制？同一件事又是什麼？它用「數字＋懸念」製造戲劇感，卻把讀者丟在半空。這是把英文科技寫作的 punchy 開場硬套到中文的常見 AI 味。

要和「開門見山、先講重點」區分：先講一個**自足、讀者當下就懂**的結論是好事；先丟一個**指涉尚未交代之物**的斷言才是問題。判準：開場句裡的每個名詞與主張，讀者能否用目前為止讀到的內容還原？若「三個失效機制」指向後文才會點名的東西，即為空降斷言，標記。

Fix：補上主題句，先交代主詞再下判斷（近似英文論說文的 topic sentence：先立主題，再展開支撐）。但別矯枉過正倒向另一種 AI 味——「在當今…的時代」式的空泛鋪陳；要的是具體的引導句，不是無意義的暖場。
- Poor：三個失效機制，全部指向同一件事。
- Better：這次故障可歸因於三個失效機制——連線逾時、重試風暴與快取穿透——三者共同的根因，是重試時沒有設上限、尖峰時所有請求擠在同一瞬間。

與 Infomercial engagement hooks（「The catch?」這類中途懸念）、Self-labeling significance（事後回指貼標籤）不同：此條針對的是段落／小節**開頭**、指涉未交代之物的斷言。

**Carve-out：**
- 標題與小節標題本就精簡點題，不受此限。
- 前文已充分鋪陳時，開場的回指承接（「這三者的共同根因是…」）是正常銜接，不是空降。

### 空降主張（文中無依據的判斷句）

前一條抓開場的空降斷言；此條抓文章**中段**冒出來的判斷句——「導入風險可控」「不影響既有安全邊界」「這個做法更成熟」——結論下得篤定，但依據既不在前文、也不在句內、也沒有來源。AI 產生論述時常把「判斷」和「支撐判斷的事實」分開生成，事實那半有時就丟失了，留下一句懸空的結論。對讀者的傷害比空話更大：空話一眼看穿，空降主張看起來像有所本，實際上無法檢驗。

判準：對文中每個判斷句問「憑什麼？」——答案是否存在於（a）前文已建立的論述、（b）同句給出的理由、或（c）標註的來源？三者皆無，即為空降主張，標記。評估類文件（ADR、選型報告）的「理由」段落從嚴適用：理由裡引用的每個事實，讀者都應該能在正文找到對應論述。

Fix：三選一——補上當場理由、回指前文（前文若沒有就先補建立）、或附來源；都做不到就刪除該判斷。
- 「BFF 落在 gateway 之後，不動既有認證與稽核邊界」（前文未提過 gateway 承載認證稽核）→ 前文先建立「對外認證與存取稽核由 gateway 集中承載」的事實，此處改寫為「如前節所述，認證與稽核由 gateway 集中承載；BFF 落在 gateway 之後，這條既有安全邊界不需變動」
- 「這個方案風險可控」→「此方案不變更安全邊界、且可先以單一服務試點，風險因此可控」

與「空降斷言開場」互補：那條抓開頭指涉未交代之物，此條抓文中結論缺乏依據。與 Vague attributions（「Experts believe」）不同：那是假託他人，此條是連託詞都沒有的裸判斷。

**Carve-out：**
- 摘要與一頁總結回收正文已論證過的結論，不是空降。
- 明確標示為假設、待驗證、或個人猜測的句子（「假設」「待確認」「我猜」）不標——它們誠實聲明了自己沒有依據。
- 領域公認常識（「網路呼叫有延遲」）不需逐句給依據，判斷標準是目標讀者是否會問「憑什麼」。

### Excessive adjective stacking

Strings of parallel adjectives that assert quality without evidence.

> Poor: 建立完整、穩健、高效、可持續的管理機制。
> Better: 建立可追蹤之分工、檢核、驗收及後續追蹤機制。

### Slash enumeration in Chinese prose

Chinese enumeration uses 頓號, not slashes: 輸入/輸出/紀錄 → 輸入、輸出、紀錄. **Carve-out:** English technical terms keep the slash — `JWT / OAuth2`, `CI/CD`, `AWQ / GPTQ` are standard notation.

### 頓號串列代替論述（名詞／動詞堆砌）

AI 在論述段裡把應該展開的內容壓成頓號串列——「gateway 負責認證、限流、路由、觀測」——四個名詞各自是一門學問，串在一起等於什麼都沒說。讀過的人當它是複習，沒讀過的人從中學不到任何東西；論述段的職責是教學，不是複習。與 Slash enumeration 相鄰互補：那條抓斜線分隔（A/B/C），此條抓頓號堆砌出現在承重的論述位置。

判準：概念在文中**首次**出現處，是否只以頓號串列帶過、沒有任何一項被展開說明？首次出現即串列者標記；前文已逐項論述過、此處僅回顧者不標。

Fix：首次出現處逐項展開（每項一句話交代它是什麼、為什麼在這裡），或至少展開承重的那幾項；串列留給表格與摘要。
- 「gateway 負責認證、限流、路由、觀測」→「gateway 承接跨客戶端一致的關卡工作：驗證請求者身分（認證）、限制單一來源的請求頻率（限流）、把請求導向正確的後端（路由），並統一收集流量記錄（觀測）」

**Carve-out：** 表格儲存格、條列摘要、一頁總結、以及前文已展開過的回顧句不標。技術慣用的固定並列（增刪查改、讀寫）不標。

### Synonym cycling (中文)

Rotating synonyms for one concept inside a paragraph (開發者…工程師…從業者…建構者). Pick the clearest term and repeat it.

### Formulaic challenge / superficial analysis

- 儘管面臨挑戰…仍持續成長 → name the actual challenge and response, or cut.
- 象徵著…的承諾 / 反映了…的投入 / 展現了…的決心 → the Chinese "-ing analysis." State the specific fact or delete.

### Negative framing → affirmative planning language

Formal Chinese AI text over-uses negative framing (不建議…, 不宜…, 不能只是…). Rewrite as a direct implementation statement — what *will* be done, by whom, verified how.

> Poor: 不建議僅以會議討論作為結論，而是要形成後續追蹤項目。
> Better: 會議結論需整理為後續追蹤項目，並列明負責單位、預計完成時間及檢核方式。

### Abstract claim → concrete substance

The highest-value Chinese fix: AI states intent where a person states deliverables. Replace abstraction with output, owner, schedule, evidence.

| Poor | Better |
|---|---|
| 本案將提升管理效率並強化作業品質。 | 本案完成後須產出作業流程、檢核表、問題追蹤表及月度執行情形報告。 |
| 後續持續追蹤。 | 後續由承辦單位每月彙整進度，內容包含已完成事項、待辦、風險、需協調事項及預計完成時間。 |
| 由內外部共同合作推動。 | 承辦單位負責需求確認與驗收；協作單位負責資料提供；廠商負責交付文件、環境設定與問題排除。 |
| 依執行情形進行評估。 | 評估資料包含交付文件、測試紀錄、會議紀錄、問題追蹤表、驗收紀錄及主管評語。 |

### 口語化萬能動詞（自以為白話的含糊簡寫）

AI 常把一個具體動作壓縮成單音節萬能動詞或極短口語簡寫——補、撐、擋、頂、串、接、拉、掛、走一遍——語氣像白話，其實沒指明做了什麼。讀者無法還原真正的動作：「補資料」是補齊缺漏、補寫說明、還是事後補登？「先用假資料撐著」的「撐」是暫代、佔位、還是維持服務不中斷？看似親切，實際上把說清楚的責任丟回給讀者。

判準：把受詞和情境拿掉，這個動詞是否還指向唯一動作？若「補 X」「撐 Y」能代入三種以上互斥解釋（補充／補足／補寫；暫代／支撐／維持），就是萬能動詞，標記。

Fix：換成單義動詞，補上受詞與方式。
- 「先用預設值撐著」→「先以預設值回填，待正式資料到位後覆寫」
- 「這塊之後再補」→「缺少的錯誤處理由承辦於下一版補寫」
- 「把兩個服務串起來」→「以訊息佇列串接兩個服務，A 完成後發事件觸發 B」

**Carve-out：**
- 真正的口語對話、聊天訊息（casual profile）裡這些動詞是自然語域，不必動。
- 已約定俗成的技術慣用語組合詞保留：串接 API、掛載磁碟、打補丁／熱補丁、扛住流量。判斷關鍵是搭配是否固定且單義——固定搭配（掛載、串接）保留，臨時拼裝的單字動詞（補一下、撐著、頂一下）才標記。

### 過度簡寫（省略主詞受詞、截斷名詞）— 寫成完整句型

AI 在濃縮、摘要或翻譯時，會把完整句子壓成電報式短語——省略主詞、丟掉受詞、把名詞截成單字、拿掉量詞助詞——例如「分享後存同一夾」。語氣像順手記的便條，但讀者得自己補回被省略的成分：「存」的是什麼？（檔案）「同一夾」是哪種夾？（資料夾）。看似精簡，實則把還原語意的工作丟回給讀者，句子也讀來突兀不完整。

判準：把句子攤開，主詞、動詞、受詞是否齊全、名詞是否為完整詞？受詞缺席、名詞被截成單字（夾←資料夾、庫←資料庫）、或動詞缺席（以名詞片語代替動作，如「服務間自動 mTLS 加密」——自動做什麼？），即為過度簡寫，標記。條列項的說明文字同樣適用此條，不因出現在 bullet 裡而豁免。

Fix：補回省略成分，名詞用完整詞，寫成完整句型。
- 「分享後存同一夾」→「將檔案分享到同一個資料夾」
- 「跑完打包上傳」→「測試跑完後，將產出物打包並上傳到發布區」
- 「服務間自動 mTLS 加密，不必改程式」→「mesh 自動為服務之間的連線套用 mTLS 加密，應用程式不必修改自己的程式碼就能得到加密」

與前一節「口語化萬能動詞」互補而不重疊：萬能動詞抓的是動詞語意含糊（補／撐／串可代入多種動作），此條抓的是句子成分被省略、名詞被截斷。已在此標記者不必在那條重複標記。

**Carve-out：**
- 真正的口語對話、聊天訊息、便條（casual profile）本就精簡，不必動。
- 已通行的固定簡稱保留：資安（資訊安全）、API、K8s。判準是該簡稱是否固定通行且單義——固定通行者保留，臨時截斷者（同一夾、設定←設定檔）才標記。

### 破折號當萬用連接詞（——濫用）

AI 中文把破折號（——）當成萬用連接詞，用它取代「因為」「所以」「例如」「也就是」「其中」等本來各司其職的承接詞——讀者每遇到一個破折號，都得自己猜前後句的邏輯關係。單看一處無傷大雅，密度一高，全文的因果與舉例關係就都藏進了同一個符號裡。這與英文規則的 Em dash frequency 同源，中文另有一個誘因：破折號讓句子顯得文氣流暢，掩蓋了連接詞沒想清楚的事實。

判準：兩層。（一）頻率：正文的連接用破折號以**每千字一次**為上限，超過即整篇檢討。（二）逐處測試：把破折號換成明確承接詞（因為／所以／例如／也就是／即），句意是否更清楚？是，就換。

Fix：換回明確承接詞，或直接以句號拆句。
- 「更麻煩的是組織面——這個 API 沒有單一的主人」→「更麻煩的是組織面的問題：這個 API 沒有單一的主人」
- 「實務架構是並存——gateway 站最外層」→「實務架構是並存：gateway 站最外層」

**Carve-out：**
- 條列的「**概念名** — 說明」結構分隔符（單破折號、前後有空格）是格式約定，不計入頻率。
- 成對破折號夾注（——插入語——）為合法用法，但整組計一次、同受頻率上限約束。
- 引文與標題不計。

### 警句式評語（破折號收尾的自我加值）

AI 論述常在句尾用破折號補一句評價式短評，替自己剛講完的論點打分數——「——這比任何文字定義都快」「——這正是它的價值所在」「——僅此而已」。同一家族還有祈使句形態的道德化評語充當強調：「成本要誠實面對」「必須正視」「不要迴避」。這類句子沒有增加資訊，功能只是宣告「我剛剛講的很重要」。與英文規則的 em-dash frequency 同源，但中文的病灶是「破折號＋評語」的組合，不只是破折號的出現頻率。

判準：刪掉破折號之後那句（或把祈使評語改成中性陳述，如「成本要誠實面對」→「成本包含」），論述是否少了任何事實或推論？若只少了情緒與強調，即為警句式評語，標記。

Fix：刪除評語；或把它想表達的判斷寫成有依據的完整句。
- 「下圖用顏色直接標出擁有權——這比任何文字定義都快」→「下圖以顏色標出擁有權界線，後文表格沿用同一套配色」
- 「成本要誠實面對：每多一個 BFF 就多一個服務」→「導入的成本：每多一個 BFF，就多一個需要部署與維運的服務」

**Carve-out：** 引文、標語、簡報標題頁等以警句為體裁的場合不標。

### 破碎短句堆疊（推論鏈斷裂）

AI 壓縮論述時，常把一段完整推理拆成連續斷言短句，句與句之間只以分號或破折號並置，省掉前提與因果承接——「硬要 DRY 抽共用層就會繞回通用 API 的老路；多一跳也多一份延遲」。每個短句各自是一個結論，中間的推論步驟由讀者自行補回。節奏讀來俐落，代價是論證無法檢驗：看得到主張，看不到主張為什麼成立。

判準：句中出現結論詞（就會、導致、所以、因此）但前提沒有寫出來；或正文論述段裡連續三個以上斷言短句僅以分號／破折號並置，沒有承接詞交代彼此的因果關係。任一成立即標記。

Fix：攤開為完整推論——前提、因果、結論各自成句，承接詞寫明白。
- 「硬要 DRY 抽共用層就會繞回通用 API 的老路」→「若為了消除重複而把共用邏輯抽成一層，所有 BFF 會重新耦合在這一層上；這一層必須同時滿足所有客戶端，也就回到了當初通用 API 難以維護的處境」
- 「多一跳也多一份延遲」→「請求路徑上多了 BFF 這一跳，每次呼叫都增加對應的網路延遲」

與「過度簡寫」互補而不重疊：那條抓句子成分（主詞、受詞）缺席，此條抓論證步驟（前提、因果）缺席。已在此標記者不必在那條重複標記。

**Carve-out：** 摘要、表格儲存格、條列重點、一頁總結等以濃縮為體裁的區塊不標——濃縮是那些區塊的職責；此條只適用於正文論述段。

### 打破第四面牆 — 工作情境外洩 / 生成過程外洩

產出文件不直接給內容，反而洩漏自己的來歷，有三種形態：

- **委託場景復述** — 「根據您提供的需求，本報告將…」「如您所述…」「依提示…」，彷彿這份成品仍在對下指令的人說話。
- **思考過程外洩** — 「首先我需要釐清…接著評估各方案…最後得出結論」，把推理的走位當成內容寫出來。
- **併稿的接縫** — 不寫結論而指向兄弟文件（「詳《04_技術面試題目》」「見《…》」「併入 02 人才徵選附件」），用回指／前指代替內容（「比照前述」「同上」「如前所述」），或留下指向已不存在之物的殘留指標（併稿後「如圖」「如下表」「見上節」所指的圖、表、章節並未一併帶入）。不是 AI 特有的毛病——人工合併草稿也會留下一模一樣的縫——但一樣會破壞獨立交付文件。

一份完成的報告是寫給讀者、不是回話給委託者；它呈現結論、而非產生結論的思考；它自成一體、而不是指著別的檔案。

判準：這句話是幫**讀者**理解論點，還是在敘述**作者**如何得到論點、或把讀者指去別處？

- 保留（讀者導向的理由）：論點所依賴的論據——「採用方案 B，因為高併發下尾延遲較低」是實質內容，不是鷹架，刪掉會使論述斷裂。
- 刪除（作者導向的過程，以及代替內容的指標）：作者自己的決策歷程——「我先考慮方案 A，發現卡在 X，於是改用 B」是鷹架，除非那個比較本身就是文件要交付的重點；以及指向兄弟文件的指標——把被指涉的結論直接寫進來，若長到無法內嵌，兩段多半該併在一起。

> Poor: 根據您提供的評估需求，我將分三個步驟說明，首先…
> Better: 三家廠商中，僅 B 符合延遲要求：

> Poor：錄取標準比照前述，專案細節詳《04_訓練計劃_專案實作》。
> Better：錄取標準為三年以上後端經驗、通過實作測驗且面談評分達 B 以上；專案需交付需求規格、系統設計、測試紀錄與驗收報告四份文件。

**Carve-out（對外部權威來源的正式引用）：** 對外部權威來源（法規、標準、官方文件、已發表文獻）的刻意引用是正當的，保留：「依《個人資料保護法》第 8 條」「參 NIST SP 800-63B」「見 RFC 7519」。判準：讀者能否獨立取得並查核該來源，且該引用是為訴諸權威、而非為省去重述自己的內容？兩者皆成立才保留。

與英文版 Reasoning chain artifacts、Acknowledgment loops 同源：前者抓「首先／第一步」這類指紋詞，此處收錄的是委託場景復述、沒有指紋詞而以流暢中文寫出的過程外洩，以及併稿接縫。已在此標記者，不必在那兩條重複標記。

### 結構級訊號（zh-TW 部落格聲音）

**detect only。** 高見龍〈寫作吧，菜鳥工程師〉點名的病灶：「正確但沒有靈魂」——句子工整、用詞精準，卻少了真實經驗、踩過的坑、「我當初也卡在這」的共鳴。拔掉 AI 病句只是減法，得到乾淨但無聲的中性文；讀者仍覺得「像 AI 寫的」，往往不是殘留病句，而是缺少人味的**正向特徵**。這一節收錄結構級訊號——句子層看不到、要退一步看整篇才浮現的缺席。

**適用範圍與姿態。** 這些是 detect 訊號，不是判決（沿用本 skill 的 signals-not-proof 立場）。判準是**文體是否 voice-bearing**（該有聲音），不是「blog vs 非 blog」：

- **啟用（voice-bearing）**：`casual`／`blunt` voice，`technical-blog`／`blog` context 帶個人語氣，觀點倡議、newsletter、深度解讀、個人 essay。這些文體本就該有立場與具體經驗，缺席才是訊號。
- **排除（voice-neutral）**：`docs`／README、RFP、簽呈、公文、SOP、`investor-email`、reference material。這些本就該均質、無立場、句句完整，不適用，比照下節 Allowed patterns 的 Structured uniformity carve-out。
- **`--structure-signals`** 為顯性 override，可對任一 voice-bearing 文體強制啟用；對 voice-neutral 文體傳入時應先提示會有大量 false positive。

**rewrite 模式下只提示、不自動改**——修復需要作者補入真實經驗與判斷，機器代筆只會生出更多假細節。

淨新增兩條（其餘三條與英文版既有規則同源，見交叉引用）：

| 訊號 | 說明與 Fix |
|---|---|
| 只解釋不造像（no original metaphor） | 難概念全用定義式解釋，通篇沒有一個自創比喻把抽象拉到讀者的生活經驗。Fix：為關鍵概念造一個貼身的像（「就像…」），出自作者自己的經驗，不是查來的通用比喻。**Carve-out：`technical-blog` 密集操作型教學本就比喻少，真人教學文常只用固定俗諺（如「地雷」）而無自創比喻；此條在教學文不可單獨觸發，需與其他結構訊號成群（≥1 條）才計入。** |
| 句句完整、無口語破格（no colloquial breaks） | 通篇沒有任何刻意的口語破格：括號補刀、（吧？）、自問自答、刻意的不完整句。真人寫部落格會破格。這是既有 "Over-polishing" 警告的正面版——不是要製造錯字，是要保留呼吸。Fix：在該停頓、該補刀處，容許一兩處破格。 |

交叉引用（沿用「同源…已在此標記者不必重複標記」慣例）：

- **節奏均質（uniform rhythm）** — 與英文版 Rhythm and uniformity 同源：連續數段長度相近、句長變異低，缺少單句段與長短交錯。
- **全文無立場（zero stance）** — 與 Rhythm and uniformity 的 "Missing first-person perspective" 及 Emotional flatline 同源：找不到一句作者判斷句，每個論點都以「各有優劣」收場。
- **零具體個人細節（zero specifics）** — 與 Treadmill effect / low information density 及 Vocabulary diversity 的 fix 同源：全文沒有一個具體時間、次數、場景（「卡關三次」「凌晨三點」「花了三天」）。

與 blog-writing-zh 分工：本節只**偵測**聲音的缺席；要**注入**聲音或重寫結構，用 blog-writing-zh（加法），再回到本 skill 除噪（減法）。

### Allowed patterns — do NOT flag (繁中 carve-outs)

These reduce false positives on legitimate Taiwan business and technical writing:

| Pattern | Why it's fine |
|---|---|
| English technical terms in Chinese prose (API, Kubernetes, SLA, PoC) | Standard Taiwan workplace usage, not an AI tell |
| 以 X 作為 Y | Factual technology/role choice, not copula inflation |
| 提升 in a technical context (用於提升排序品質) | Describes a component's function, not empty praise |
| 具體而言 followed by concrete items | A list introducer, not filler |
| English-term slashes (JWT / OAuth2, SSE / WebSocket) | Standard notation for alternatives |
| 不是 X，是 Y as a factual boundary | A real distinction, not contrarian structure |
| Structured uniformity in 公文 / RFP / SOP | These genres are inherently uniform; do not break their formatting for "rhythm" |

### AI 慣用詞替換（個別用詞對照）

AI 偏好的譬喻詞或英文術語直譯，在台灣商務／技術寫作中有更精準的對應詞。逐詞替換，**carve-out** 欄列出仍應保留原詞的語境。

| Flag | 為何不精準 | Fix | Carve-out（保留原詞） |
|---|---|---|---|
| 節奏（用於時程／進度語境，如「專案節奏」「開發節奏」） | 把英文 rhythm／cadence 的譬喻套到時程上；中文應直接指明時間規劃 | 期程（時間規劃）／排程（具體時間表，依語境擇一） | 真正描述音樂、運動、敘事的「節奏感」時保留 |
| 編排（用於 orchestration，如「服務編排」「流程編排」） | orchestration 直譯為「編排」偏向版面／內容編排語意，與調度資源、協調流程的原意不符 | 調度 | 描述版面、內容、表演、課程「編排」時保留 |
| 跳（用於 network hop，如「多一跳」「少一跳」「每跳延遲」） | network hop 的直譯；圈外讀者不知道「跳」的是什麼，句中也沒有動作與對象 | 寫明動作與對象：「請求多經過一個轉發節點（network hop）」「每經過一個節點就增加一段轉發延遲」 | 明確面向網路工程讀者、且文中已定義 hop 一詞時，可用「hop」原文 |

### 專有名詞過度翻譯（生造中文譯名）

AI 傾向把沒有通行中文譯名的專有名詞硬翻成逐字直譯的生造詞——產品名、功能名、專案代號、框架／工具名、尚無定譯的領域術語——例如把 house rules 譯成「房規」。這類譯名台灣同行不會使用，讀者也無法回推原文或據以搜尋，反而製造理解障礙。缺乏通行譯名時，人類寫作直接保留原文（英文），這是標準台灣工作場域用法。

這是既有 carve-out「API／Kubernetes 等英文術語保留原文」的延伸：不只是保留本來就通行的英文詞，更要還原被 AI 生造中文詞蓋掉的原文。

判準：這個中文詞是否為該領域已通行的譯名（查得到、同行看得懂）？

- 有通行譯名 → 用中文：資料庫（database）、伺服器（server）、快取（cache）、負載平衡（load balancing）。
- 無通行譯名，或譯名為 AI 逐字生造 → 保留原文：Kubernetes、Prometheus、Terraform，以及產品名、功能名、專案代號、尚無定譯的領域術語。
- 判斷測試：把生造中文詞拿去搜尋，若查無此領域用法、且原文才是同行實際使用的詞，即為過度翻譯，標記並還原為英文。

Fix：還原英文原文；首次出現可用「英文原文（簡短白話說明）」補一句，之後直接沿用英文。

- 「房規」→ house rules（房型與房價的設定規則）
- 若原文是 orchestration engine 而無定譯 →（該詞已由前一節處理調度語意，若整體為專有名詞則）保留 orchestration engine

**Carve-out：**

- 反向也是 AI 味：已有通行中文定譯者一律用中文，不可為了「保留原文顯得專業」而英文化。本規則只還原被生造中文詞蓋掉的原文，不鼓勵一律英文化。
- 知識文件首次定義時中英並列（中文（English）或 English（中文說明））是好習慣，不算過度翻譯。
- 有疑義時以「同行能否辨識、能否搜尋得到」為準，而非以「是否為專有名詞」為準。

### Taiwan term preferences (zh-TW, not zh-CN)

When rewriting, prefer Taiwan-standard terms: 計畫 (not 计划), 規劃, 執行, 檢核, 驗收, 廠商, 資訊, 專案, 承辦單位, 權責單位, 待辦事項, 後續追蹤, 期程, 排程, 調度. Avoid PRC-style phrasing (賦能, 抓手, 落地, 閉環, 顆粒度, 對齊顆粒度) unless quoting source material.

**For a dedicated 陸用語 → 台灣正體 pass, use the `avoid-china-writing` skill.** This section is a light touch — it catches PRC phrasing only where it overlaps AI 空話. The sibling `avoid-china-writing` skill is the deep pass: a full 詞彙對照表 (視頻→影片、軟件→軟體、屏幕→螢幕), 互聯網／職場黑話, 簡體字殘留偵測, and 音譯專名差異 (奧巴馬→歐巴馬). Cross-strait localization is an axis orthogonal to AI-ism cleanup — when the writer wants both, run `avoid-china-writing` for 用語 and this skill for 語氣／結構.

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document, prioritize by tier:

### P0 — Credibility killers (fix immediately)
- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events
- Breaking the fourth wall — commissioning echo (「根據您提供的需求…」/ "As requested, this report…"); a deliverable addressing its prompter
- Hashtag stuffing on `linkedin` and `investor-email` posts (severity varies by profile — same rule, lower priority on `blog`/`technical-blog` where a launch post may legitimately stack tags; see the context-profile table below)

### P1 — Obvious AI smell (fix before publishing)
- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving world of...")
- Bold overuse
- Em dash frequency (above 1 per 1,000 words)
- Generic future-narrative closers ("may become one of the most important narratives…")
- Social endorsement closers ("This one is worth your time:", "thank me later")
- Hedge-stacked predictions ("could potentially," "may eventually")
- 破折號當萬用連接詞（連接用——每千字超過一次）
- 警句式評語（破折號收尾的自我加值／祈使式道德評語）
- 破碎短句堆疊（正文論述段的推論鏈斷裂）
- 頓號串列代替論述（概念首次出現即以名詞堆砌帶過）
- 空降主張（文中判斷句無前文依據、無當場理由、無來源）
- Real/actual adjective inflation ("real on-chain tokenomics")
- Bullet lists of bare noun phrases (5+ short adj+noun items, no verbs)
- Tier 3 phrase clustering (≥3 distinct boilerplate phrases in one piece)
- zh-TW empty slogans (全面提升 / 賦能 / 打造完整生態), contrarian 不是…而是…, and AI sentence templates (在當今…的時代)
- zh-TW abstract-claim-without-deliverable (本案將提升…效率 with no concrete output)
- zh-TW 口語化萬能動詞／含糊簡寫（補一下 / 先撐著 / 串起來，動詞可代入 3 種以上互斥動作）
- zh-TW 過度簡寫（省略主詞受詞、截斷名詞，如 存同一夾←將檔案存到同一個資料夾），寫成完整句型
- zh-TW 空降斷言開場（段落／小節開頭丟一個指涉未交代之物的 term／claim，如「三個失效機制，全部指向同一件事」）
- zh-TW 專有名詞過度翻譯（把無通行譯名的產品名／功能名／術語生造成逐字中文，如 house rules→房規）
- Breaking the fourth wall — process narration (the author's step-by-step deliberation written out as prose, no CoT fingerprint words)
- Breaking the fourth wall — consolidation seams (併稿接縫): pointing at a sibling document instead of stating the conclusion (詳《04_技術面試題目》, "see the other doc", 併入 02 人才徵選附件), a lazy back/forward reference standing in for content (比照前述, 同上, "as above"), or an orphaned pointer to a figure/table/section that didn't survive the merge (如圖, 如下表). Not an AI tell per se, but a standalone-readability defect from consolidating source documents.

### P2 — Stylistic polish (fix when time allows)
- Generic conclusions ("The future looks bright")
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance (serves as, features, boasts)
- Transition phrases (Moreover, Furthermore, Additionally)
- Hashtag stuffing (`blog`/`technical-blog` profiles)
- Tier 3 phrase repetition (single phrase ≥2× — fine in isolation, suspect in stacks)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

## Self-reference escape hatch

When writing *about* AI writing patterns (blog posts, tutorials, skill documentation like this file), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose, not in cited examples of bad writing.

---

## Context profiles

Pass an optional context hint to adjust rule strictness. If no context is specified, auto-detect from content cues (short + hashtags = social, code blocks = technical, salutation = email, default = blog).

### Profile definitions

**`linkedin`** — Short-form social. Punchy fragments, visual formatting matter.
**`blog`** — Default. Standard long-form prose. All rules apply at full strength.
**`technical-blog`** — Long-form with code, architecture, APIs. Technical terms get a pass.
**`investor-email`** — High-trust audience. Tighten everything; promotional language is the biggest risk.
**`docs`** — Documentation and software-development docs: READMEs, CONTRIBUTING, CHANGELOG, ADR, API docs, guides, and code comments. Clarity over voice. This is a finishing/review pass, not a drafting aid — run it when a dev doc is being finalized or reviewed for AI tells, and leave code identifiers, commands, config keys, and fenced code blocks untouched.
**`casual`** — Slack messages, internal notes, quick replies. Only catch the worst offenders.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work on LinkedIn) | strict | relaxed (technical lists OK) | strict | skip (lists are docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate in technical) | strict | relaxed | skip |
| Word table (full list) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell is expected) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |
| Hashtag stuffing | strict | strict | strict | **extra strict** | skip (no hashtags in docs) | skip |
| Bullet-NP lists | strict | strict | relaxed (technical option lists OK) | strict | relaxed (parameter lists OK) | skip |
| Tier 3 phrase clustering | strict | strict | strict | **extra strict** | relaxed | skip |
| Future-narrative closers | strict | strict | strict | **extra strict** | skip | skip |
| Social endorsement closers | strict (the LinkedIn share-post tell) | strict | strict | strict | skip | relaxed (1 OK in a DM) |
| Hedge-stacked predictions | strict | strict | relaxed ("could" is hedged accuracy) | **extra strict** | relaxed | skip |
| Real/actual inflation | strict | strict | strict | **extra strict** | relaxed | skip |

**Technical-blog word table exceptions:** These terms have legitimate technical meaning and should not be flagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual platform leverage/APIs), `facilitate`, `underpin`, `streamline`. Still flag: `delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`, `harness`.

**"Extra strict"** means: flag even borderline instances. In investor emails, a single "thriving ecosystem" can undermine the whole message.

**"Skip"** means: don't audit this category for this profile. The rule doesn't apply or isn't worth the edit.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
|--------|-----------------|
| CJK characters present | apply the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section; for 公文 / 簽呈 / RFP / SOP shapes, treat structured uniformity as `docs` (do not flag it) |
| Under 300 words + hashtags or mentions | `linkedin` |
| Code blocks, API references, or technical architecture | `technical-blog` |
| Salutation ("Hi [name]", "Dear") + investor/fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog` (safest default — all rules apply) |

If auto-detection feels wrong, say which profile you're using and why. The user can override.

---


## Voice profiles

Context profiles (above) set *how strict* to be for an audience. Voice profiles set *how the prose should sound* — the persona. They're independent axes: you can write blunt for a blog or warm for docs. Voice is **optional** — if the writer doesn't name one, infer it from the input's existing register and don't impose a persona on text that already has one.

Each profile is a set of concrete targets, not a vibe:

**`casual`** — Contractions throughout; their absence reads stiff. Short sentences (aim for ≤14 words on average); fragments allowed. At least one first-person or concrete-anecdote touch. Near-zero jargon. Keep warm hedges ("honestly," "I think") but cut corporate ones ("it's worth noting"). *Blog posts, social, community.*

**`professional`** — Active voice for most sentences. Vary sentence length; avoid three in a row within a few words of each other. One concrete claim per paragraph (a number, a name, a date), never "experts say." Make the ask explicit. Low tolerance for hedging. *LinkedIn, investor email, sponsor pitches.*

**`technical`** — Prefer plain copulatives ("X is Y") over inflated substitutes ("serves as," "stands as a testament to"). One idea per sentence; imperative mood for instructions. Jargon is fine, but define it on first use. Tables and lists only where the content is genuinely list-shaped, not for decoration. *Docs, technical blog.*

**`warm`** — Address the reader directly ("you") and acknowledge them at least once. Cut intensifiers ("very," "truly," "incredibly") in favor of stronger verbs. No performative-empathy openers ("I completely understand how you feel"). Medium sentences (15–20 words) for an unhurried cadence. *Mentorship, onboarding, thank-yous.*

**`blunt`** — Lead with the claim; cut "It's important to note that" windups. Em-dashes are rare here; use periods for emphasis. No padding to hit a rule of three. Near-zero hedging; flag "may / could / potentially" stacks. Short declaratives, with the occasional long sentence for contrast. *Decision memos, thought leadership, hard feedback.*

**Calibrate to a sample (optional).** If the writer gives you a sample of their own writing ("match my voice — here's a post"), analyze its sentence-length pattern, contraction rate, paragraph openings, and recurring word choices, then match those instead of a named profile. Don't "upgrade" their vocabulary: if they write "stuff" and "things," keep that register.

**How voice composes with context.** Voice sets the target; context sets how hard to enforce it. A voice *target* always applies, even where a context profile would skip that category — `technical` voice still prefers plain copulatives in a `casual` context that otherwise ignores copula avoidance. Where both axes govern the same rule and agree, they reinforce: `blunt` voice wants near-zero em-dashes and a `blog` context is already strict on them, so it stays a hard edit. Where they disagree, resolve toward the **stricter** of the two — a `warm` voice on `docs` still doesn't get decorative tables. Sensible default pairings: casual↔casual, professional↔linkedin/investor-email, technical↔docs/technical-blog.

**Voice profile as a positive-feature contract.** When the writer supplies a voice profile or voice sample — including one authored by a sibling skill like `blog-writing-zh` — the positive features it declares are **intentional**: a stated stance, a metaphor system, a deliberate rhythm, intentional 口語破格. Do not strip them as AI-isms. This is what lets the additive and subtractive passes compose: `blog-writing-zh` injects the voice, this skill removes the noise, and the subtraction must not eat the addition. If a declared feature *also* matches an AI-ism rule, leave it in place and note it in the audit rather than editing it out.

---

## Output format

### Rewrite mode (default)

Return your response in four sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted.

**2. Rewritten version**
The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

**3. What changed**
A brief summary of the major edits made. Not every word, just the meaningful changes.

**4. Second-pass audit**
Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, or anything else from the categories above. Fix them, return the corrected text inline, and note what changed in this pass. If the rewrite is clean, say so.

### Detect mode

Return your response in two sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted. Group by severity (P0, P1, P2).

**2. Assessment**
For each flag, note whether it's a clear problem or a judgment call. Some AI-associated patterns are effective writing techniques — uniform paragraph length is a problem, but a well-placed "however" isn't. Call out which flags the writer should definitely fix vs. which ones are worth a second look but might be fine in context. If the text is clean, say so.

### Edit mode

After editing the file in place, return a short report — not the full file:

**1. Edits made**
A bulleted list of the changes, each with the file location and the before → after. Only the spans you touched.

**2. Verification**
Confirm you re-read the file and the flagged patterns are resolved. Note anything you deliberately left alone because it was already human or intentional.

---

## Tone calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece is supposed to take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it.

The replacement table provides defaults, not mandates. If a flagged word is clearly the right choice in context, preserve it.

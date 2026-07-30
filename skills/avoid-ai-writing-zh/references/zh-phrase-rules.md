# 繁體中文 AI 用詞對照表（zh-TW / 台灣用語）

The seven enumerable word/phrase → replacement lookup tables for the Traditional Chinese section of `avoid-ai-writing-zh`. Load this file when auditing CJK text and you need a concrete「這個詞→換成這個」lookup — empty slogans, the 確保 filler family, significance-inflation words, AI sentence templates, individual-term substitutions, 四字評語, and Taiwan term preferences.

This file is lookup data, not rules. The rules that need judgment rather than lookup live in `zh-rules.md`, organised by the eight defect classes; the detect-only aggregate lives in `hidden-author.md`. Apply those together with the tables here.

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
- 具體而言 **only when** no concrete items follow (as a list intro before real items, it is fine — the carve-outs sit in the **保留** line beside each rule in `zh-rules.md`)

## AI 慣用詞替換（個別用詞對照）

AI 偏好的譬喻詞或英文術語直譯，在台灣商務／技術寫作中有更精準的對應詞。逐詞替換，**carve-out** 欄列出仍應保留原詞的語境。

| Flag | 為何不精準 | Fix | Carve-out（保留原詞） |
|---|---|---|---|
| 節奏（套在時程、工作、學習、對話、產品等抽象事物上，如「專案節奏」「開發節奏」「工作節奏」「學習節奏」「對話節奏」「掌握節奏」「節奏感」） | 把英文 rhythm／cadence 的譬喻鋪到不具韻律的事物上，聽起來有畫面卻沒指出任何具體安排 | 依語境指明實際所指：期程（時間規劃）／排程（具體時間表）／頻率（多久一次）／步調（快慢）／輪次（迭代週期） | 真正描述音樂、舞蹈、運動、敘事韻律的「節奏」保留 |
| 編排（用於 orchestration，如「服務編排」「流程編排」） | orchestration 直譯為「編排」偏向版面／內容編排語意，與調度資源、協調流程的原意不符 | 調度 | 描述版面、內容、表演、課程「編排」時保留 |
| 跳（用於 network hop，如「多一跳」「少一跳」「每跳延遲」） | network hop 的直譯；圈外讀者不知道「跳」的是什麼，句中也沒有動作與對象 | 寫明動作與對象：「請求多經過一個轉發節點（network hop）」「每經過一個節點就增加一段轉發延遲」 | 明確面向網路工程讀者、且文中已定義 hop 一詞時，可用「hop」原文 |

## 四字評語（成語式讚詞）

AI 描述進度、執行、文本品質時，慣以四字成語或四字排比作結，讀來鏗鏘卻不含任何可查核的事實——這是「節奏」譬喻的成語形態，也是**推廣語氣**那串排比形容詞的四字版。

**判準的作用域是段落，不是那四個字。** 單看成語本身永遠不帶事實，據此逐詞判會把真人正常書寫誤殺。要問的是：**這一段裡，成語所形容的事，有沒有在鄰近句子被寫出來？**

- 寫出來了 → 成語只是主題句或連接語，**不標**。「先完成單一單位試辦，確認流程可行後再循序漸進擴及其餘六個單位」——階段安排就在句中。
- 沒寫出來，整段找不到日期、數量、負責單位、步驟或機制 → 成語頂替了本該說明的內容，**標記**。
- 一段內三個以上四字評語連綴、且無任一可查核事實者，必標。

| Flag | 這句實際說了什麼 | Fix（改寫方向） |
|---|---|---|
| 節奏明快 | 只說了「快」，沒說快在哪 | 指明實際數字：每兩週一個 release、需求到上線平均 5 個工作天 |
| 張弛有度 | 對安排的自我讚許，零資訊 | 寫出安排本身：前四週密集開發，第五週只做整合測試與修補 |
| 一氣呵成 | 對過程順暢度的評價，無從查核 | 寫出實際過程：三個模組在同一次迭代內完成並一次整合上線，中途未回頭改規格 |
| 三線並行 | 沒說是哪三線、怎麼並行、誰負責 | 列出各線與負責單位：後端 API、前端介面、資料遷移三項同期進行，各由 X／Y／Z 負責 |
| 環環相扣／層層遞進／循序漸進 | 對結構的形容，不指出結構 | 寫出實際依賴：B 需要 A 的輸出才能開工，C 待 B 驗收後啟動 |
| 有條不紊／井然有序／穩紮穩打 | 對品質的自我評分 | 刪除；若要留，改為可查核的事實（每階段皆有驗收紀錄） |
| 相輔相成／事半功倍 | 宣稱綜效卻不量化 | 寫出綜效來源與幅度：兩者共用同一份設定檔，設定維護點從兩處減為一處 |

**Carve-out：**

- 成語所形容的安排、依賴或結果已寫在同段鄰句者保留（見上方段落級判準）——公文的「循序漸進推動」、技術文件的「三者環環相扣」在依序列出步驟之後，是正當的總結語。
- 引文、標語、簡報標題頁、文學敘事體裁保留。
- 存疑時不標。本 skill 寧可漏標也不誤傷真人（signals, not proof）。

## 負面案例對照（承 zh-rules.md 判準）

判斷型規則（零資訊警句與口號、翻譯腔、過度簡寫）的定型負面案例對照。遇到相同句型可直接套用下表；句型不同、或不確定是否觸發，仍回 `zh-rules.md` 依各規則判準處理。左欄是要抓的負面案例，中欄標出病灶與對應的規則名稱，右欄是改法。

| 負面案例（flag） | 病灶 | Fix |
|---|---|---|
| …才會上架。沒過 eval，不上架。 | 零資訊警句與口號（零資訊重述）：後句只是前句換句話說 | 刪去後句 |
| 連網一行指令，或離線的逐一技能 symlink | 零資訊警句與口號（口號代替說明）：該說明處只給對仗片語 | 線上環境用一行指令安裝；離線或內網環境則改用逐一技能的 symlink |
| 要貢獻，先看 CONTRIBUTING.md | 翻譯腔（句式直譯 ← To contribute, see X） | 想貢獻的話，請先讀 CONTRIBUTING.md |
| 指名叫用 | 翻譯腔（搭配直譯 ← invoke by name） | 輸入名稱手動啟動 |
| 選用的指路 | 翻譯腔（修飾語直譯 ← optional pointer；「指路」在中文不成詞） | 額外參考 |
| 一個能夠幫助你快速完成工作的工具 | 翻譯腔（長定語鏈 ← a tool that helps you work faster）：英文關係子句壓成「一個能…的 X」前置定語，名詞前堆一長串修飾 | 這工具能幫你快速完成工作（定語拆成短句，讓動詞回主幹） |
| 基於使用者的回饋來調整介面 | 翻譯腔（介詞框架直譯 ← based on… / by …-ing）：「基於／通過…來…」是英文介系詞框架的鏡像 | 根據使用者回饋調整介面（「基於／通過…來…」改「根據／用」，能省則省） |
| 術語不誤傷 | 過度簡寫（動詞裸用：主詞受詞雙缺） | 不會把真正的術語誤判成該改的詞 |
| 這些技能照台灣人實際的寫法寫 | 過度簡寫（繫詞省略：句尾「寫法寫」懸空，缺「是…寫成的」句架） | 這些技能是照著台灣人實際的書寫習慣寫成的 |

翻譯腔的通則是**禁止原文直翻、一律改寫**：先抓意思，再想「若一開始是一個台灣人就用中文寫，這件事會怎麼講」，不要對著英文逐詞替換。兩個高頻形態要特別留意：**長定語鏈**（名詞前掛一長串「能…的」修飾，拆成短句、讓動詞回主幹）與**介詞框架堆疊**（基於／透過／通過…的方式）；「透過」「基於」這類介詞一段最多用一次，能省則省。

## Taiwan term preferences (zh-TW, not zh-CN)

When rewriting, prefer Taiwan-standard terms: 計畫 (not 计划), 規劃, 執行, 檢核, 驗收, 廠商, 資訊, 專案, 承辦單位, 權責單位, 待辦事項, 後續追蹤, 期程, 排程, 調度. Avoid PRC-style phrasing (賦能, 抓手, 落地, 閉環, 顆粒度, 對齊顆粒度) unless quoting source material.

**For a dedicated 陸用語 → 台灣正體 pass, use the `avoid-china-writing` skill.** This section is a light touch — it catches PRC phrasing only where it overlaps AI 空話. The sibling `avoid-china-writing` skill is the deep pass: a full 詞彙對照表 (視頻→影片、軟件→軟體、屏幕→螢幕), 互聯網／職場黑話, 簡體字殘留偵測, and 音譯專名差異 (奧巴馬→歐巴馬). Cross-strait localization is an axis orthogonal to AI-ism cleanup; this skill completes the de-AI job on its own regardless. If the writer *also* wants a 陸用語 pass, `avoid-china-writing` handles that separate axis.

---
name: knowledge-doc-writing
description: >-
  把自學或研究一個技術主題的成果，整理成一份包含四個清楚分離 Diátaxis 區塊的知識文件——tutorial（帶著上手）、
  how-to（照著完成任務）、reference（查參數與結構）、explanation（What/Why 論述與取捨決策）；用 compass
  兩問把每段素材路由到對應區塊，素材撐得起才寫，撐不起的型（研究過但未實作常缺 tutorial/how-to）明列為缺口，
  不捏造、不搭空殼（繁體中文為主、術語保留英文）。觸發：使用者要把對話紀錄、官方文件或原始資料、或從零研究的主題
  （強制查一手來源並標 as-of 時效）消化成可長期參考的技術文件；或改寫一份既有技術文件——依意圖分流：
  更新時效／併入新素材→定點修補保留原形，重整／重構→依 compass 重建四型區塊。可接在 learn-loop 之後：
  learn 管互動學習迴圈與親手 distillation（鐵律：distillation 是學習本身，不代寫），
  本 skill 只接手 distill 完成後重新組織、補讀者上下文、套完稿檢查。不要用於：公司內部簽呈／會議紀錄／
  評估報告等行政文件（用 formal-doc-structure，即使輸入是既有文件也不因此轉入本 skill）、RFP／招標規格
  （用 rfp-writing）、部落格文章（用 blog-writing-zh）、只做語言層去 AI 味不動結構（用 avoid-ai-writing-zh）、
  只要口頭白話解釋不產文件（用 plain-speak）、learn 的互動學習迴圈本身（用 learn-loop）。
version: 2.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required; source-verification steps assume web access when available.
metadata:
  author: Lu Yi
  tags: writing knowledge-doc self-learning diataxis zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "📚"
---

# Knowledge Doc Writing — 自學知識文件（Diátaxis 四型）

把一個技術主題（自學所得、對話紀錄、或原始資料）整理成**一份文件、四個清楚分離的 Diátaxis 區塊**：tutorial（帶著讀者第一次上手）、how-to（引導已具能力者完成任務）、reference（查參數與結構）、explanation（What/Why 論述與取捨決策）。四個區塊彼此不混，跨型內容用連結互指，不 inline 混寫。

**素材撐得起才寫**：用 compass 兩問把每段素材路由到對應區塊，有素材支撐的型寫足寫純，撐不起的型（研究過但未實際跑過，常缺 tutorial/how-to）明列為缺口、標待補條件，**不捏造、不搭空殼**。

**預設技術脈絡**：金融業企業級架構、Kubernetes / OpenShift、微服務、AI 平台、RHEL + rootless Podman + Quadlet。範例與比較對象優先取自這個語境，讓文件貼近實際工作而非教科書通例。此語境在此宣告一次，各節引用不重述。

全文白話優先、術語保留英文（見 S5）。

## S1. 開工前：定位、輸入模式、Mode D 意圖閘

動筆前一次問完，不確定就問使用者：

1. **文件定位** — 學習筆記（可第一人稱、可留疑問）／正式文件（客觀陳述、規格手冊風格、無第二人稱教練口吻）／混合（正文正式、學習鷹架收文末附錄）。定位決定第一人稱與 opt-in 姿態。
2. **輸入模式**：
   - **A 對話紀錄整理** — 以對話中反覆修正後的最終理解為素材；中途被推翻的說法轉 explanation 常見誤解並查證；懸而未決且使用者自標的問題，依 opt-in 例外收進 explanation 附錄待驗證清單。
   - **B 原始資料整理** — 官方文件、spec、會議記錄；這是重組不是摘要，交給 S2 compass 依「服務哪種需求」重排，不照原文功能目錄排。
   - **C 從零研究產出** — 使用者只給主題名稱；**先做來源研究再動筆**（見 S6 一手來源），快速演進的主題優先近 12–18 個月資料。
   - **D 既有文件改寫** — 見下方意圖閘。
3. **learn 銜接**（屬 A/B 變形，鐵律）：本 skill 是 `learn-loop` 下游，**不得跨越分工線**。distillation（把資料消化成自己的話、判斷懂沒懂）永遠是 learn 的職責、由使用者親手做；本 skill 拿到的是已 distill 完成的理解，只負責寫成對外文件。vault 已確立的理解直接作 explanation 主幹，不重做消化；補齊第三方讀者上下文；`[[wikilinks]]` 與 YAML block tags 改寫或移除；沿用 learn 已查證來源，as-of 更新為出文件時點。

**Mode D 意圖閘**（收到既有文件時，先過此閘，gate on 意圖不 gate on 動詞）：

- **先過主題篩**：本模式只收技術知識文件。簽呈、會議紀錄、評估報告等行政文件即使格式再「外來」，轉交 `formal-doc-structure`：動詞是「改寫」，不改變歸屬。
- **意圖＝更新時效／併入新素材 → 定點修補（point-patch）**：保留輸入原形（即使原檔是本 skill 之前的四型或單一骨架），只改被時效／新素材影響的部分。**point-patch 路徑不進入 S2 compass，不重排整份。**
- **意圖＝重整／重構 → 交 S2 compass 重建四型區塊**：把素材依 compass 重新路由。
- 動筆前先問保守改寫或從零重產，不自行假設。文件出身辨識訊號（本 skill 骨架 vs 外來教學文／feature list／AI 代筆稿——流暢≠有骨架）、判錯的不對稱代價、四情境（重構／更新時效／併入新素材／品質升級）各自邊界、改寫說明格式，見 [references/rewrite.md](references/rewrite.md)。

**完成準則**：定位與輸入模式已判定，不確定項已動筆前一次問完；若為模式 D，文件出身與意圖分流方向（point-patch／compass 重建）已分類，且已問保守改寫或從零重產。判為 point-patch 卻仍跑 compass 重排、或 learn 銜接卻重做 distillation，即為失敗。

## S2. Compass 路由：每段素材指派到唯一區塊、缺型標缺口

這是承載性路由器，四型區塊都是它的下游。對**每段素材**各問兩題：

1. **action 還是 cognition？** — 要讀者去「做」（動作導向），還是增進理解（認知導向）。
2. **acquisition 還是 application？** — 服務讀者習得技能的階段（at study，學習中），還是已有技能要運用的階段（at work，工作中）。

兩答案機械式指向唯一一型：

| | acquisition（學習中） | application（工作中） |
|---|---|---|
| **action（做）** | Learning → **tutorial** | Goals → **how-to** |
| **cognition（想）** | Understanding → **explanation** | Information → **reference** |

產出一張可稽核的**素材→區塊指派表**。規則：

- **同段橫跨兩象限＝拆分訊號**：拆開分別歸位，不 inline 混寫。
- **沒有素材路由進的象限＝缺口**：標為待補（如「需實際部署後補」），不捏造內容填充。
- **踩雷／步驟依可逆性次分派**：可逆、安全的操作 → tutorial 提示；不可逆、生產風險的 → how-to 警告。

**完成準則**：文件中每一段素材都經兩題判定、指派到四型其中恰一型並記入指派表；橫跨兩象限的素材已拆開歸位；四型每一型皆已明確標為「有素材支撐」或「缺口＋待補條件」，二者擇一無第三態。無指派表背書而逕自開寫任一區塊即為失敗。

## S3. 四型區塊：撐得起才寫、寫足寫純

依 S2 指派結果，**只寫有素材支撐的區塊**，每型守其邊界。缺口型只留一行缺口註記，不寫散文。四型完整產生規則、好壞示範、五件套 recipe、消化模組寫法、opt-in 附錄格式，見 [references/blocks.md](references/blocks.md)：**動手寫任一區塊前先讀它**。以下是各型邊界規格（純度不靠下沉檔，寫進完成準則）：

- **explanation**（understanding-oriented，唯一可帶判斷的區塊）：What/Why 三段論述（功能定位／解決的問題／主要功能要求，寫成完整句段落，非名詞條列）＋**辯證比較五件套作 internal recipe**（定義→行為職責邊界→比較分析→邊界判斷表→決策框架，含「何時不該採用」有實質內容），**不自成頂層骨架**；ADR 決策理由（背景／選項／後果／依據）織入論述、回指前文事實，不另立獨立模組；心智模型與類比、常見誤解、論述紀律（每個判斷句有前文／理由／來源）。opt-in 附錄住此（見下）。
- **reference**（information-oriented）：**describe-only**、中性、mirror 產品結構、含旗標與參數；無 recipe、無意見、無論述。
- **tutorial**（learning-oriented）：單一安全直線、消除意外、第一人稱複數祈使（We…／Notice that…）；不解釋、不追求完整、不放真實世界分支。
- **how-to**（task-oriented）：assume competence、goal-oriented、允許 if-then 條件分支；不教學、不離題；標題精確說出展示什麼。

**opt-in 模組**（費曼式自述、待驗證問題清單）：預設關閉，住在 **explanation 區塊的附錄**，寫法在 blocks.md。放 explanation 由 compass 象限背書：費曼＝reflection-after-practice＝cognition＋at-study；待驗證＝理解缺口的工作紀錄，同屬 understanding-oriented。兩個啟用門：(a) 使用者明確要求（「幫我檢核理解／加費曼自述／待驗證清單」）；(b) 例外條款——輸入素材（如對話紀錄）內含使用者自己標記、不收就會遺失的未解問題，此時待驗證清單照收，每題附具體「怎麼驗證」。正式文件模式一律不出現。

**完成準則**：凡有素材支撐的型皆寫到其邊界純度：reference 無論述無 recipe；explanation 為論述、五件套為內部 recipe（頂層出現獨立五件套骨架即失敗）、「何時不該採用」有實質內容；tutorial 為單一安全直線、無真實世界分支、無解釋；how-to 假設已具能力、允許 if-then、不教學；缺口型逐一為一行缺口註記；opt-in 模組僅在啟用時出現於 explanation 附錄、正式文件模式不出現。

## S4. 維持區塊分離

寫完後自審 map 預測的**兩對相鄰混淆**（相鄰型共享一維，最易混）：

- **tutorial ↔ how-to**（同屬 action，差在 **at-study vs at-work**）：最致命，擋在新手面前。把跑進 tutorial 的真實世界分支抽回 how-to。
- **reference ↔ explanation**（同含 propositional knowledge，差在 **describe vs discuss**）：把跑進 reference 的論述抽回 explanation。

跨型內容改為**連結互指**，不 inline 混寫。兩對的分辨測試細節見 [references/blocks.md](references/blocks.md)。

**完成準則**：兩對相鄰混淆自審皆已執行；無區塊含他型內容（tutorial 內無真實世界分支、reference 內無論述）；每處跨型指涉皆為連結而非 inline 段落。自審被跳過或殘留任一 blur 即為失敗。

## S5. 語言與格式（含 HTML 版）

跨型共用、與路由無關的規則，寫任一區塊時皆套用：

- **白話優先，讀者一遍讀懂**。用平實的話講清楚，勝過堆術語、繞公文腔、寫長難句。正式文件模式收斂的是口吻（客觀陳述、不用第一人稱），不是把句子寫難；規格手冊風格照樣白話。白話不等於簡寫：名詞與動詞都用完整的詞、語句寫成完整句。
- **術語保留英文**（API、sidecar、control plane）是台灣技術寫作慣例；無定譯的專有名詞不生造中文譯名。
- **三層承接**（章節／段落／條列，適用所有區塊的條列，不限 explanation）：章節開頭一句交代與前節關係；段落間用承接詞或回指交代因果；條列前有**引導句**（交代這份清單是什麼的集合、並列窮舉／依序／互斥）、順序有意義就**明說**、後有**收束句**接回論述。檢驗法：打亂順序重讀若讀不出差別、引導句卻聲稱有順序，代表該層級的邏輯關係不存在。
- **一句話開頭 + 一段話總結**：開頭收一個 blockquote（一句話定義＋文件範圍行＋「更新至 YYYY-MM」）；文末收一段話總結（三行內講完定義、強弱項、決策法則）。
- **架構與決策路徑畫 Mermaid**（flowchart），標註要能獨立讀懂，Markdown 為正本；學習筆記可少量 emoji 點綴（✅❌⚠️），正式模式收斂。
- **相關但不展開的鄰近主題**收文末「延伸參考」：定位、一句話對比、時效近況（授權變更、專案存廢）。

**HTML 版**：Markdown 為預設輸出正本。使用者要圖文並茂時才另出 HTML 版，規則見 [references/html.md](references/html.md)——所有圖表 inline SVG（不用 canvas／點陣／Mermaid runtime／外部圖片）、套固定模板 CSS、四型在 HTML 中仍分離、依 frontend-design／infographic-design 定 token 且只用於圖不用於外殼。

**完成準則**：全文白話一遍讀懂、術語保留英文；每個區塊的條列有引導句與收束句、順序有意義時已明說；開頭有一句話 blockquote、文末有一段話總結；架構／決策以 Mermaid 呈現且可獨立讀懂；僅在使用者要 HTML 版時才依 html.md 產出，屆時四型仍分離、圖表為 inline SVG、Markdown 版仍為正本。

## S6. 完稿檢查：功能性先於深層

兩層品質閘，寫作期即累積、交件前收斂。**deep quality is conditional upon functional quality**，順序不能顛倒。

### 功能性品質（硬約束，先過）

accuracy／completeness／consistency／usefulness／precision。逐項：

- **一手來源可追**。優先序：官方文件／spec ＞ 原始論文與設計提案（KEP／RFC）＞ 專案維護者文章 ＞ 二手教學。二手只補視角，關鍵事實回一手確認。
- **標 as-of 日期與版本範圍**。「Ingress 已被 Gateway API 取代」沒有版本範圍就是錯的；行為隨版本變的主題寫明適用版本（`OpenShift 4.14+`、`Podman 5.x`）。
- **標記過時說法**。廣為流傳但已過時的講法寫進 explanation 常見誤解，註明從哪版起不成立。
- **無編造 URL 或來源**；不確定就寫不確定。**無空降主張**：每個判斷句有前文依據、當場理由、或來源三者之一。
- **範例不豁免**：使用者提供的範例句與正文同標準受檢，破碎短語照抓照改。

**去 AI 味**：**可用時優先呼叫 `avoid-ai-writing-zh`**（它是語言判準的權威來源，用它跑 detect／edit），把全文掃到清零並回報發現／修復／殘留。它是可選、非前置依賴，不可載入時 fallback 到下列內建精簡判準清單完成，核心產出不受阻。內建清單：破碎短句、頓號堆砌、破折號濫用（連接用「——」每千字一次為上限，條列「概念名 — 說明」分隔符不計）、空降主張、動詞缺席、警句式評語、樣板標題（「深入探討」「全面解析」「揭秘」）、第二人稱教練口吻（正式與混合模式視為違規，學習筆記放寬第一人稱與自問）。

### cycle-of-needs 覆蓋與 complete≠finished

- **四型覆蓋檢查**：一個技術主題天然產生四種需求（想上手／想完成任務／想查參數／想懂原理）。確認四型皆「覆蓋或明列缺口」，無靜默遺漏；無空殼區塊。
- **complete ≠ finished**：文件永遠在演化，但隨時可以是 complete：對使用者有用、符合現階段、結構健康。每型當下有用即可獨立發布，**由內而外從最撐得起的型長出，不先搭四殼再填**。

### deep quality（功能性全過後才評）

flow、beauty、anticipating-user。不得以美補救功能缺陷。依 mode 組織貼合需求、守住區塊邊界保住 flow。

### 改寫說明（僅模式 D）

交付一份改寫說明（格式見 [references/rewrite.md](references/rewrite.md)）：結構變動、時效性事實更正（舊值→新值＋來源）、內容併入／保留／覆蓋的取捨。沒有這份清單就宣稱改完，視同未檢查。

**完成準則**：功能性檢查全部通過「在」任何深層潤飾之前（來源可追、as-of 已標、版本敏感有範圍、無編造來源、無空降主張）；去 AI 味違規清單已產出、修復至零並回報，範例句同受檢；cycle-of-needs 四型皆覆蓋或明列缺口；無空殼區塊；模式 D 已交付改寫說明。功能性未過即進行 flow 潤飾，或缺口既未填也未標，即為失敗。

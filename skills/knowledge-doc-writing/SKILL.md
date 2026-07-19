---
name: knowledge-doc-writing
description: >-
  把自學技術主題的成果整理成結構化知識文件（繁體中文為主、術語保留英文）。觸發時機：使用者說
  「幫我整理成知識文件」「把這段對話整理成技術筆記」「我在自學 X，幫我建立知識文件」
  「針對 X 研究並寫一份知識文件／學習筆記」，或提供官方文件、會議記錄、對話紀錄，要求消化成可長期參考的技術文件。
  支援四種輸入：對話紀錄整理、原始資料整理、從零自學產出（強制查證一手來源並標註時效）、
  既有文件改寫（先辨識文件出身：已是本 skill 骨架→定點修補，外來格式→整份重構；動筆前先問保守改寫或從零重產）。
  產出核心是 What/Why 論述與辯證比較決策框架，並依情境附自學消化模組
  （前置知識地圖、心智模型與類比、常見誤解與陷阱、最小可運行範例、費曼式自述檢核、待驗證問題清單）。
  可接在 learn-loop skill 之後作為下游：learn 管六步互動學習迴圈、Obsidian vault、與親手 distillation（learn 鐵律：distillation 是學習本身，不代寫），
  本 skill 只接手 distill 完成之後的產文件步驟——重新組織、補讀者上下文、套用完稿檢查，不重新消化或代替使用者理解。
  不要用於：learn 的互動學習迴圈本身（用 learn）、公司內部簽呈／會議紀錄／評估報告等行政文件（用 formal-doc-structure）、
  RFP／招標規格（用 rfp-writing）、部落格文章（用 blog-writing-zh）、只做語言層去 AI 味不動結構（用 avoid-ai-writing-zh）、
  只要口頭白話解釋不產文件（用 plain-speak）。既有文件的結構與內容改寫屬模式 D（重構骨架、更新時效、併入新素材、
  補齊缺漏）；行政文件（簽呈／會議紀錄／評估報告）本身要改寫，仍歸 formal-doc-structure，不因輸入是既有文件而轉入本 skill。
version: 1.3.1
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required; source-verification steps assume web access when available.
metadata:
  author: Lu Yi
  tags: writing knowledge-doc self-learning zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "📚"
---

# Knowledge Doc Writing — 自學知識文件

把一個技術主題（自學所得、對話紀錄、或原始資料）整理成結構化知識文件。文件要能同時服務兩種讀者：三個月後回來查的自己，以及第一次接觸這個主題的同事。核心紀律是「論述，非條列」——每個概念都要說清楚它是什麼、解決什麼問題、跟替代方案的邊界在哪，而非只留一串名詞。

預設技術脈絡：金融業企業級架構、Kubernetes / OpenShift、微服務、AI 平台、RHEL + rootless Podman + Quadlet。範例與比較對象優先取自這個語境，讓文件讀起來貼近實際工作，而非教科書通例。

## 開工前先定三件事

動筆前依序判斷，不確定就問使用者，一次問完：

1. **文件定位** — 學習筆記、正式文件、還是混合（見下節）。
2. **輸入模式** — 對話紀錄整理、原始資料整理、從零自學產出、既有文件改寫（見「輸入模式」；模式 D 另外要當場問保守改寫或從零重產）。
3. **主題型態** — 決定要不要掛情境模組：主題涉及實際待決策 → 掛 ADR；主題是平台或堆疊 → 掛分層結構（見「情境模組」）。

## 文件定位：學習筆記 vs 正式文件

同一份骨架，兩種輸出姿態。判斷線索：

- 使用者說「筆記」「消化」「幫我理解」、輸入是零散對話 → **學習筆記模式**。
- 使用者說「文件」「給團隊看」「規格」「可以放 wiki」 → **正式文件模式**。
- 訊號混雜或使用者說「兩者都要」 → **混合模式**：正文用正式姿態，學習鷹架收進文末附錄。

| | 學習筆記模式 | 正式文件模式 |
|---|---|---|
| 口吻 | 可用第一人稱、可留疑問 | 客觀陳述，規格手冊風格 |
| 消化模組 | 依主題取用（費曼檢核、待驗證清單為 opt-in，見模組表） | 只留對讀者有用的（前置地圖、誤解陷阱、範例） |
| 未確定的理解 | 標記後保留，進待驗證清單 | 查證後才寫入；查不到就明說「未查證」 |
| 目標 | 三個月後的自己能接續學 | 沒學過的同事能直接用 |

費曼式自述檢核與待驗證問題清單是學習者的鷹架，**opt-in 模組**：預設不放，使用者明確要求才啟用（見模組表的例外）；正式文件模式下一律不出現。其餘模組兩種模式共用。

## 輸入模式

**A. 對話紀錄整理**。以對話中已確立的理解為文件主幹。對話裡反覆修正後的最終版本才算數，中途被推翻的說法不寫入。對話中懸而未決的問題全部收進待驗證問題清單。對話中的關鍵事實（版本行為、預設值、效能數字）抽查查證——對話當下可能講錯，文件不能跟著錯。

**B. 原始資料整理**。官方文件、spec、會議記錄 → 依本 skill 的骨架重新組織，這是重組不是摘要：原始資料通常按功能羅列，知識文件要按「解決什麼問題」重排。標註來源文件的版本與日期；原文與骨架有落差的地方（例如官方文件沒講清楚職責邊界），查證補齊或標為待驗證。

**C. 從零自學產出**。使用者只給主題名稱。必須先做來源研究再動筆：查官方文件與一手來源，快速演進的主題（Kubernetes 生態、AI 平台）優先近 12–18 個月的資料。研究時同步記錄來源，寫作時照「來源可靠性」規則引用。

**D. 既有文件改寫**。輸入是一份已存在的文件，任務是修補或重構，不是憑空重寫。依序：

1. **先過主題篩**。本模式只收技術知識文件；輸入若是簽呈、會議紀錄、評估報告等行政文件，即使格式再「外來」，也轉交 `formal-doc-structure`——動詞是「改寫」不改變歸屬。放最前：行政文件不該進到下一步被當骨架分類。
2. **辨識文件出身，決定改寫深度**。已是本 skill 骨架（What/Why＋辯證比較五件套）→ **定點修補**；外來格式（教學文、feature list、AI 代筆的自由行文稿）→ **整份重構**。判斷訊號、判錯的不對稱代價、四種常見情境（重構／更新時效／併入新素材／品質升級）各自的邊界，見 [references/rewrite.md](references/rewrite.md)。
3. **動筆前先問改寫姿態，不自行假設**：保守改寫（維持原結構與已成立判斷，只做局部修補）還是從零重產（整份依骨架重寫）。每次都問，不因看起來像哪種就跳過。保守改寫時，舊文件已寫對、寫清楚的論述照用，不退回去重新論證或重排。
4. **時效性事實回一手來源重查**（見「來源可靠性」），交付時附一份改寫說明（格式見 [references/rewrite.md](references/rewrite.md)）；沒有這份清單就宣稱改完，視同未檢查。

## 接在 learn 之後：從 vault 筆記到正式文件

本 skill 是 `learn-loop` 的下游，且**不得跨越這條分工線**：distillation（把資料消化成自己的話、判斷懂了沒懂）永遠是 learn 的職責、永遠由使用者親手做；本 skill 拿到的必須是已經 distill 完成的理解，任務只是把它寫成結構完整、可對外的文件。兩者職責不重疊：

- **learn 的產物是 distilled permanent note** — 存在 Obsidian vault、由使用者親手 distill（learn 的鐵律：distillation 是學習本身，不代寫）。它是消化過的個人知識，格式為 vault house style（answer-first、claim 標題、wikilinks、YAML block tags）。
- **本 skill 把那則筆記轉成可對外的正式文件** — 重新組織成本 skill 的骨架（What/Why、辯證比較五件套），補齊給第三方讀者所需的上下文，套用完稿檢查。

銜接的操作方式（屬輸入模式 A／B 的變形）：

- **不重做 distillation**。vault 筆記裡使用者已經想清楚的理解，是文件主幹，照用；不要退回去重新教學或重新推導——那是 learn 的階段，已經完成了。
- **補齊讀者落差**。permanent note 是寫給未來的自己，省略了自己已內化的背景；轉成正式文件時，把這些背景補進前置知識地圖與 What/Why 論述，讓沒學過的同事讀得懂。
- **wikilinks 與 vault 專有格式落地**。`[[其他筆記]]` 連結在對外文件裡失效，改寫成正式文件內的交叉引用、或收進延伸參考節。YAML block tags 等 vault 內部格式移除。
- **保留來源錨點**。learn 已為每個事實查證過一手來源，這些來源直接沿用進本 skill 的來源清單，不必重查（但 as-of 日期要更新為出文件的時點）。

觸發線索：使用者說「把 vault 裡那則 X 筆記整理成正式文件」「這則 learning note 要給團隊看，幫我轉成知識文件」，或提供一則 distilled note 要求對外化。

## 來源可靠性（四種模式共用）

過時或錯誤的資訊源會讓學習者建立錯的心智模型，之後要花數倍力氣拆掉重建，所以：

- **一手來源優先序**：官方文件／spec > 原始論文、設計提案（KEP、RFC）> 專案維護者的文章 > 二手教學與部落格。二手來源只用來補視角，關鍵事實回一手來源確認。
- **版本敏感就標版本**。「Ingress 已被 Gateway API 取代」這類敘述沒有版本範圍就是錯的。行為隨版本變的主題，寫明適用版本（如 `OpenShift 4.14+`、`Podman 5.x`）。
- **每個關鍵 claim 可追源頭**。文中以連結或文末來源清單標註。不確定就寫不確定，絕不編造 URL 或來源。
- **文件標註 as-of 日期**。開頭 frontmatter 或首段寫「本文內容確認至 YYYY-MM」，讓未來的讀者知道該重新查證哪些部分。
- **標記過時說法**。研究中發現廣為流傳但已過時的講法（常出現在舊教學文），寫進「常見誤解與陷阱」，註明從哪個版本起不再成立。

## 核心骨架

兩段核心結構，所有知識文件都要有。完整模板與寫法示範見 [references/skeletons.md](references/skeletons.md)。

### 1. What/Why 論述

每個元件或概念用三段論述交代，寫成完整句子的段落：

- **功能定位** — 它在整個系統裡站在哪個位置、扮演什麼角色。
- **解決的問題** — 沒有它會發生什麼事、它出現前大家怎麼繞過這個問題。這段是理解的錨點，寫得好整份文件就立住了。
- **主要功能要求** — 它必須做到什麼才算稱職，用可檢驗的敘述寫。

單純名詞條列（「功能：A、B、C」）不合格——條列可以出現在論述之後當摘要，不能取代論述。

### 2. 辯證比較與決策框架

主題有替代方案或易混淆的鄰居時（幾乎所有主題都有），依序寫五段：

1. **定義** — 一句話說清楚這是什麼。
2. **行為職責邊界** — 它管什麼、明確不管什麼。不管的部分交給誰。
3. **比較分析** — vs 替代方案，逐面向比（架構、運維成本、適用規模、生態成熟度），寫出差異背後的原因而非只列結論。
4. **邊界判斷表** — 表格：情境 → 該用哪個 → 為什麼。收灰色地帶的案例。
5. **決策框架** — 何時該採用、何時不該。「不該」的那半邊與「該」的同等重要，省略它的比較文件只是廣告。

## 論述紀律：結構的骨架與關節

知識文件的骨架是**可掃描的結構**（條列與表格），關節是**論述**（推論鏈）。這一節規範兩者的分工——這是本 skill 的結構決策，屬本 skill 職責；句子層級的語病（破碎短句、頓號堆砌、破折號濫用、空降主張、動詞缺席）交由 `avoid-ai-writing-zh` 把關，於「完稿檢查」統一執行，此處不重述其判準。

與 blog 的分界要先講清楚：段落敘事流是 blog 的節奏（blog-writing-zh 的地盤）；知識文件的讀者會跳讀、回查、掃描，結構要為此服務。四條紀律：

1. **關鍵概念用條列，每條自帶論述**。標準形態「**概念名** — 一到兩句完整說明（它是什麼＋為什麼）」。條列與名詞堆砌的差別在有沒有說明；說明本身要是完整句（主詞動詞受詞齊全，不名詞化動作、不截斷受詞）——這一句同時受 avoid-ai-writing-zh 的「頓號串列」與「過度簡寫」兩條約束。一個概念的說明超過兩三句、需要推論鏈時，升級成段落。
2. **段落保留給推論鏈**。解決的問題、比較差異的成因、決策的理由，這些地方前提與因果要寫全。反向防呆：連續三段以上純段落而無條列或表格，是 blog 的形狀，回頭把可條列的概念抽出來。
3. **表格殿後**。表格是論述與條列之後的查表摘要，不得出現前文未建立過的新概念或新主張；整份文件把表格全刪掉，論證仍應完整，只是查閱變慢。
4. **承接存在於每個層級**。章節、段落、條列三層都要有邏輯銜接：
   - 章節開頭一句交代與前節的關係。
   - 段落之間用承接詞或回指交代因果與遞進。
   - 條列前有**引導句**（交代這份清單是什麼的集合、各項是並列窮舉還是依序排列還是互斥分類）、順序有意義就**明說**（「依判斷力道由強到弱」）、後有**收束句**把清單結論接回論述。
   檢驗法：打亂章節或條目順序重讀，若讀不出差別、引導句卻聲稱有順序，或清單可任意增刪而無人發覺，代表該層級的邏輯關係不存在。

每個判斷句都要有來處（前文依據、當場理由、或來源三者之一），這條由 avoid-ai-writing-zh 的「空降主張」把關，ADR 的理由段從嚴適用。

## 自學消化模組

依文件定位取捨，各模組的寫法細節與好壞示範見 [references/modules.md](references/modules.md)。

| 模組 | 放哪裡 | 何時用 |
|---|---|---|
| 前置知識地圖 | 文件開頭 | 主題有明確前置依賴時；列「學這個之前要先懂什麼」與各自一句話說明 |
| 心智模型與類比 | What/Why 之後 | 概念抽象時；給一個可運算的類比，並標註類比在哪裡失效 |
| 常見誤解與陷阱 | 比較分析前後 | 幾乎必用；收初學者會踩的坑與過時說法 |
| 最小可運行範例 | 文件中後段 | 主題可實作時；能在目標環境十分鐘內跑起來的最小驗證步驟 |
| 費曼式自述檢核 | 文末（opt-in） | 預設不放；使用者要求「幫我檢核理解」「加費曼自述」時才啟用。用自己的話重述核心概念，標出講不順的地方 |
| 待驗證問題清單 | 文末（opt-in） | 預設不放；使用者要求時啟用。例外：輸入素材（如對話紀錄）裡有使用者自己標記的未解問題，不收進清單就會遺失——此時照收，每題附「怎麼驗證」的具體做法 |

## 情境模組

**ADR 式決策記錄** — 主題背後有一個實際待做或已做的決策時掛上（例如「我們該不該導入 service mesh」）。結構：背景 → 考量的選項（各自優缺點）→ 決策 → 理由 → 已知代價 → 後續行動。已知代價一節必填：沒有代價的決策記錄代表分析沒做完。

**分層結構** — 主題是平台或堆疊時掛上（例如 AI 平台、容器平台）。由上而下分層論述（如 Application / Middleware / Infrastructure / Hardware），每層具體條列構成元件，並交代層與層之間的介面。每層內部仍用 What/Why 論述寫，分層只是外框。

## 語言與格式

- **白話優先，讀者一遍讀懂**。知識文件的成敗，看沒學過的同事能不能一次讀通；用平實的話把事情講清楚，勝過堆術語、繞公文腔、寫長難句。正式文件模式收斂的是口吻（客觀陳述、不用第一人稱），不是把句子寫難——規格手冊風格照樣白話。術語保留英文（API、sidecar、control plane）是台灣技術寫作慣例，無定譯的專有名詞不生造中文譯名。白話不等於簡寫：名詞與動詞都用完整的詞、語句寫成完整句（此條的判準與機械把關見「論述紀律」與「完稿檢查」，此處不重述）。概念的白話講解用三拍節奏：一句話 → 為什麼重要 → 要注意的坑，坑那一拍常常最有價值。
- **論述段的濃縮分寸**：What/Why 與比較分析要寫完整推論鏈，濃縮留給表格、摘要與一段話總結。句子層級的相關語病（破碎短句、警句式評語、破折號濫用）由 avoid-ai-writing-zh 於完稿檢查把關。
- **章節標題寫內容本身**，口語提問式標題可用（「為什麼會有它？」「它怎麼運作？」）；避免「深入探討」「全面解析」「揭秘」這類樣板標題。
- **開頭收一個「一句話」blockquote**：一句話定義主題＋文件範圍行＋「更新至 YYYY-MM」。**文末收「一段話總結」**：三行內講完定義、強弱項、決策法則。- **表格承重**：邊界判斷用「需求 → 該用的工具 → 是否本職」表；決策框架用「訊號 → 傾向採用／傾向不用」雙欄表。兩三個項目的簡單比較仍用文字寫。
- **架構與決策路徑畫 Mermaid 圖**（flowchart），標註要能獨立讀懂；學習筆記可少量 emoji 點綴標題與表格（✅❌⚠️），正式文件模式收斂。
- **相關但不展開的鄰近主題**收進文末「延伸參考」節：定位、一句話對比、與時效近況（授權變更、專案存廢）——避免主文失焦，也留下下一步學習的鉤子。
- **Markdown 為預設輸出**。主題需要圖文並茂或互動比較時，另出一份 HTML 版，Markdown 版仍是正本。HTML 版的規則見下節。

## HTML 版產出規則

- **所有圖表（infographic）一律用 inline SVG**，不用 canvas、點陣圖、或外部圖片。理由：SVG 是文字，未來要調整（改標籤、換配色、加一個節點）時，人和模型都能直接編輯，不必重畫。Markdown 正本裡的 Mermaid 圖轉 HTML 版時，重繪為手工 inline SVG，不嵌 Mermaid runtime——執行期渲染的圖無法離線閱讀，產出的 DOM 也難以維護。
- **文件外殼固定套用預設模板，每次都一樣，不重新設計**。色彩、字體、版面、表格與區塊樣式一律使用下方最低規範 CSS，不因主題（容器平台、金融基礎設施……）另挑色票或字體方向——一致的外觀是知識庫的資產，讀者掃過十份文件會認得「這是我們的知識文件」，重新設計反而製造不必要的差異。

```css
:root{
  /* 固定色票，每份文件都用這組，不重新設計 */
  --paper:#F7F9FB; --panel:#FFFFFF; --ink:#1F3A5F; --text:#2A2F36; --muted:#5C6670;
  --accent-a:#41597A; --accent-a-bg:#E8EDF4;   /* 分類/對照 A（例：擁有權、擁有者、擁有的區段） */
  --accent-b:#0E7C7B; --accent-b-bg:#E3F2F1;   /* 分類/對照 B */
  --warn:#B97514; --warn-bg:#FBF3E4;           /* ADR、風險、成本區塊 */
  --line:#C9D3DE; --radius:6px;
  --font-body:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;
  --font-mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--text);font-family:var(--font-body);line-height:1.8;font-size:16px}
main{max-width:860px;margin:0 auto;padding:48px 24px 80px}
h1{font-size:1.85rem;color:var(--ink);margin:0 0 4px;font-weight:700}
h2{font-size:1.2rem;color:var(--ink);margin:2.4em 0 .7em;padding-bottom:.35em;border-bottom:2px solid var(--line)}
.kicker{font-family:var(--font-mono);font-size:.76rem;color:var(--muted);letter-spacing:.14em;text-transform:uppercase}

/* 開頭一句話 blockquote（見骨架） */
.thesis{background:var(--panel);border-left:4px solid var(--ink);border-radius:0 var(--radius) var(--radius) 0;
  padding:18px 22px;margin:22px 0;box-shadow:0 1px 3px rgba(31,58,95,.08)}
.scope{font-family:var(--font-mono);font-size:.78rem;color:var(--muted);margin-top:8px}

/* 條列（見上方條列 marker 規則） */
ul.kv{list-style:none;padding-left:0;margin:1em 0}
ul.kv li{margin:.55em 0;padding-left:1.3em;position:relative}
ul.kv li::before{content:"•";position:absolute;left:0;color:var(--muted);font-weight:700}
ul.kv b{color:var(--ink)}

/* 表格：殿後於論述，樣式保持素淨 */
table{width:100%;border-collapse:collapse;margin:1.1em 0;font-size:.92rem;background:var(--panel)}
th{background:var(--ink);color:#fff;text-align:left;padding:9px 12px;font-weight:500}
td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}

/* SVG 圖說明框 */
figure{margin:1.6em 0;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:18px}
figcaption{font-size:.85rem;color:var(--muted);margin-top:10px}
/* SVG 內文字要與內文同字體，直接在 <svg><style> 裡覆用：font:600 14px var(--font-body) */

/* ADR 情境模組 */
.adr{background:var(--warn-bg);border-left:4px solid var(--warn);border-radius:0 var(--radius) var(--radius) 0;padding:16px 22px;margin:1em 0}
.adr dt{font-weight:700;color:var(--warn);margin-top:.9em}
.adr dt:first-child{margin-top:0}
.adr dd{margin:.2em 0 0}

/* 一段話總結 */
.summary{background:var(--ink);color:#E8EDF4;border-radius:var(--radius);padding:20px 24px;margin:2em 0}
.summary p{margin:.4em 0}

/* 行內程式碼：預設是淺底深字；深色區塊（.summary、.adr 若換深底）必須覆寫成深底淺字，
   否則字色繼承父層淺色文字、疊在淺色背景上會看不清楚 */
code{font-family:var(--font-mono);background:var(--paper);color:var(--text);padding:.1em .35em;border-radius:3px;font-size:.9em}
.summary code{background:rgba(255,255,255,.15);color:#E8EDF4}

ul.src{font-size:.9rem;padding-left:1.2em}
a{color:var(--accent-b)}

/* 動畫尊重 prefers-reduced-motion：只有明確允許動態時才跑 */
@media (prefers-reduced-motion:no-preference){
  figure svg .flow{stroke-dasharray:6 4;animation:dash 1.6s linear infinite}
  @keyframes dash{to{stroke-dashoffset:-20}}
}

/* 行動裝置 */
@media (max-width:640px){body{font-size:15px} main{padding:32px 14px 60px}}
```
- SVG 圖要能獨立讀懂：圖內標籤完整，不依賴周邊文字才看得懂；配色與 HTML 版整體 token 一致。
- **條列項目符號用真正的 bullet，不用破折號或連字號充當**（破折號在條列裡的角色是「概念名 — 說明」的分隔符，見論述紀律，兩者不可混用）。樣式已含在下方最低規範 CSS 的 `ul.kv` 區塊。

**過程中若需要設計圖表（架構圖、流程圖、對照圖），引用 `infographic-design` skill 處理圖的內容設計**，只用在圖本身、不用在文件外殼。畫「這個協定／管線／架構怎麼運作」這類機制圖時，另讀該 skill 的 `references/bytebytego-style.md`，用編號走查（numbered walkthrough）把複雜流程講成一個可循序讀懂的序列，不是一張泛泛的方框加箭頭。但**文件外殼與整體視覺語言以本節的固定模板為準，覆蓋該 skill 自己的色彩與字體系統**：圖表顏色一律從文件既有的 token 變數（`--ink`、`--muted`、`--accent-a`、`--accent-b`、`--warn` 等）裡挑，不新開色票；字體沿用 `--font-body`／`--font-mono`。這樣同一份文件裡，圖表與正文永遠是同一套視覺語言，換了主題也不會每次重新設計一次外觀。

完整風格錨點與段落示範見 [references/skeletons.md](references/skeletons.md)。

**範例文件是風格參考，不是規則豁免**：使用者提供的範例決定骨架、密度與視覺語彙，但範例裡的句子同樣要過 avoid-ai-writing-zh 檢核——範例中的破碎短語（如動詞缺席的 bullet 說明）照抓照改，不因出自範例而放行。

## 完稿檢查

交件前依序跑以下檢查：

1. **語言檢查（實際執行，不是宣稱）** — 以 `avoid-ai-writing-zh` 的 detect 模式對全文產出違規清單，逐項修復後複掃至清零，並在交付說明中回報掃描結果（發現幾處、修了幾處、殘留幾處與理由）。可機械檢核的項目先跑腳本：連接用破折號（——）每千字一次為上限（條列「概念名 — 說明」分隔符不計）、grep 慣用詞替換表的 Flag 詞（跳、節奏、編排…）。沒有違規清單就宣稱通過，視同未檢查。
2. **來源檢查** — 關鍵 claim 都有可追的來源；as-of 日期已標；版本敏感的敘述都有版本範圍。
3. **骨架檢查** — 每個核心概念的 What/Why 是論述段落；比較段落五件套齊全，且「何時不該採用」有實質內容。
4. **結構檢查** — 關鍵概念以「概念名 — 說明」條列呈現，每條有說明且說明為完整句型（主詞動詞受詞齊全）；連續三段以上無條列即檢討是否過度段落化；表格內容皆可回溯前文；章節、段落、條列三個層級皆有承接（條列前有引導句、後有收束句、順序有意義時已言明）；無空降主張。
5. **改寫說明檢查（僅模式 D）** — 交付一份改寫說明，列出結構變動、時效性事實更正（舊值→新值＋來源）、內容併入或保留的取捨；沒有這份清單就宣稱改寫完成，視同未檢查。

# infographic-design — 開發紀錄與接續指南

給未來用 Claude Code 接續開發此 skill 的人（或 agent）。SKILL.md 與
references/ 依 repo 規範不含開發過程；來源與決策記在這裡。

## 一句話定位

把資訊做成「一張自足畫布」的設計 skill。核心信念：資訊圖表是**無人講解、
數秒內被消費**的媒介，所以一切規則都為「8 秒內傳達單一訊息」服務。

## 研究來源（v0.1.0 的知識基礎）

2026-07 網路研究彙整，主要來源：

- **版面與視覺層級**：Visme（infographic layout / best practices —
  三段式敘事、60-40 留白、11 種 layout 類型）、Venngage（13 best
  practices — margin/一致性）、Piktochart、Toptal、Hull University
  LibGuide（三層 hierarchy 上限）、F/Z reading patterns。
- **圖表誠實性**：Tufte 原則（data-ink ratio、chartjunk、graphical
  integrity）＋ Frank Elavsky 對 minimalism 的批判（別為了 ratio 犧牲
  accessibility contrast）。
- **無障礙**：WCAG 2.1 — 文字 4.5:1（SC 1.4.3）、非文字圖形 3:1
  （SC 1.4.11，IBM Carbon 的實作經驗）、color-only encoding 禁令。
- **60/30/10 色彩結構、60-30-10 rule** 為設計圈慣例，非單一出處。

References 裡的具體數字（如 8px spacing unit、palette hex、type scale）
是綜合上述來源後的**編輯決策**，不是引用 — 可依實測調整。

### bytebytego-style.md 的來源（2026-07 補研究）

使用者要求參考 ByteByteGo 風格。網路上對其設計的解析散在課程評論裡，
真正談「怎麼做」的線索：

- **wey-gu 的 gist**（"How to create diagrams like Alex Xu/bytebytego"）
  ＋ Alex Xu 本人推文 → 工具是 **draw.io**，招牌是**連接線的
  flow animation**（有向流）。
- **ByteByteGo newsletter 原文**（EP17、Diagram as Code、DevSecOps
  cheat sheet 貼文）→ 實際看到簽名句型：「The diagram below shows…」、
  **🔹Step 0/1/2 編號走查**、「Let's take process 1234 as an example」
  的**具體實體接地**、taxonomy 題目改用**🔹分類格狀 cheat sheet**。
- **javinpaul/Medium**（"How ByteByteGo Makes System Design Easy"）→
  **progressive reveal**：high-level overview → detailed components →
  scenarios/trade-offs。
- Glarity/Alex Xu → **Diagram as Code**（Python `diagrams` 套件、
  box-and-arrow、Jupyter），佐證「程式化、box-and-arrow、克制配色」。

歸納出的簽名 = 編號走查焊在有向流上 + 一圖一點 + 具體範例實體 +
分類格狀變體。定位為 Process/flow 與 Anatomical archetype 的**風格變體**，
不是新 archetype。刻意只留「技法」，不綁 draw.io（可攜；SVG 用
arrowhead＋編號＋request/response 配色取代動畫）。

尚未做：此風格的 output-quality 專屬 assertions（如「每個 step badge
都有對應 prose 編號」「request/response 用不同視覺編碼」）待補。

### 輸出格式選擇（Step 2，2026-07 依使用者需求加入）

使用者要求 skill 讓他**選擇產出格式，並預設推薦建議格式**。設計決策：

- 把格式選擇放在 **Step 2（設計之前）**，因為 static-vs-interactive 的
  分岔會改變「怎麼做」，且目標平台決定尺寸（Step 5 / layouts.md）。
- 互動模式 = **recommend-then-confirm**：agent 依用途推薦一個預設 +
  一句理由，列替代選項，讓使用者一句話覆寫；若使用者已指名格式就直接用；
  無訊號時 default 到 SVG。刻意不做成硬性 gate（不強迫每次都問），
  已指名時要能直接動作。
- **SVG = source of truth**：SVG/PNG/PDF 都先做 SVG 再轉檔（cairosvg/
  rsvg-convert 的 recipe 寫進 Building the output）。只有 HTML（互動）與
  PPTX 會真正改變 build path。這呼應先前「為何 SVG」的分析：可縮放、
  一處改色、text-based 可被 agent 編輯、可無損轉檔。
- 交付時連 SVG source 一起給，方便日後 restyle。

尚未做：Step 2 的行為型 eval（給定平台訊號→是否推薦正確格式、
已指名格式→是否略過詢問）。目前 evals 只有 trigger cases，
behavior eval 待回 Claude Code 補 output-quality.json 時一起做。

### 能力強化批次（2026-07）

依「該做」清單做的最小高價值批次：

1. **測試發現的兩個 bug — 已修**。（a）accent 過度使用：
   bytebytego-style.md 加 "Accent-count exception"（badge 系統算一次
   accent，另留最多一個 accent moment）。（b）列距不均：layouts.md 加
   anchor-pitch 規則（固定 anchor pitch、card height 隨內容浮動，
   不要固定 card 間距）。這兩點是 HTTPS 測試實際暴露的。

2. **contrast 從「目測」升級成工具**：新增 `scripts/check_contrast.py`
   （純 stdlib，無依賴）。pair 模式與 `--svg --bg` 掃描模式；WCAG
   4.5/3.0 門檻。**實測抓到 HTTPS 測試圖自己的真 fail** —— L3 灰字
   #8794a0 在淺底只有 2.94:1（kicker／lane 副標／來源行），證明
   render 後目測不夠。已在 SKILL build step 串接。已知限制：SVG 模式
   分不出 text 色與 surface fill，白色/淡色卡片底會誤報 —— 已在
   docstring 與 SKILL 註明忽略。

3. **CJK／多語字體段**（對主要用例關鍵）：svg-construction.md 新增
   "CJK / multilingual text" 段 —— 重點是 **SVG→PNG 匯出時 system
   stack 掉字成 tofu（□）**，要顯式指名 Noto Sans TC/SC/JP 等 stack、
   render 機器要裝字型（fonts-noto-cjk）、換行以**字數**非詞數計、
   CJK 不加 letter-spacing／不 all-caps。color-typography.md 型錄段
   加對應指標。

未納入此批次（DEVELOPMENT backlog）：內容萃取（Step 1 的 how）、
資料來源接口（xlsx/file-reading 銜接＋數字正確性驗證）、圖表 SVG
座標運算 helper、SVG 螢幕閱讀器無障礙（title/desc/aria）、
色盲模擬、圖示語彙。刻意不一次全塞以維持 index 精簡。

### 圖示語彙 + restyle 結構（2026-07 第二批）

依 backlog 兩項做:

1. **圖示語彙 `references/icons.md`** —— 解「從零畫難一致」。給
   24×24 構圖網格規範(2px stroke、round cap/join、2px padding、
   `currentColor`)＋**30 個實測過會 render 的 starter library**
   (user/server/database/cloud/lock/chart/…),以 `<symbol>`+`<use>`
   使用,顏色靠 currentColor 一處改。全部先 render 成 sheet 目測,
   修過兩處:zero-length dot 用 `.01` offset(`h0` 在部分 converter
   不顯示)、help 改成真正問號曲線。並用 `<use>` 版重跑一次確認
   teach 的 pattern 本身可用、且 currentColor 能一鍵改色。

2. **restyle 結構** —— svg-construction.md 新增 "Structuring for
   restyle" 段:單一 `:root` CSS 變數 block、class 對應三層 hierarchy
   (.l1/.l2/.l3)、幾何與顏色分離、語意化 `<g id>`(以內容命名非位置)、
   region 註解、base unit 註記。呼應 Step 2 的「日後 restyle」承諾 ——
   rebrand = 改 `:root` 五行。pitfalls checklist 同步加入 icon/
   inline-hex/semantic-group/contrast 幾項。SKILL build step 兩處
   pointer 已接。

剩餘 backlog:內容萃取、資料接口、座標 helper、a11y title/desc、
色盲模擬。

### loop 驗證 + output-quality baseline（2026-07 第三批）

1. **contrast loop 端到端驗證**:拿 HTTPS 測試圖跑
   `check_contrast.py --svg` 抓到真 fail（L3 灰字 #8794a0 2.94、
   來源行 #9aa6b1 2.35、response 線 2.35）→ 用 script 選過的替代色
   修（L3 文字全 #5b6b78 5.21:1;response 線/箭頭 #71808c 3.85
   過 graphic 門檻）→ 重跑 script 確認所有**文字** ≥5.2:1 → 重
   render。剩下被 flag 的都是已知豁免類（#71808c graphic 過關、
   #c9d4de 裝飾 lifeline、#e8683a accent 只當 badge、白/淡 surface
   fill 誤報）。build→render→check→fix→re-check→re-render 整條
   loop 證實可用。

2. **output-quality.json（新）**:依 plain-speak schema
   （eval_type/grading/note/evals[].assertions[criterion,must,ref]）。
   8 個 scenario 各打一個 skill 宣稱的價值點:one-message、
   hierarchy-one-hero、data-honesty(截軸誘餌)、format-recommend、
   format-named-skip-ask、accessibility-contrast、bytebytego-explainer、
   restyle-structure。deterministic 者加 `check` 欄（contrast script /
   grep var()、g-id）。
   **關鍵（回應「還沒證明 skill 讓輸出變好」）**:top-note 寫死
   baseline 紀律 —— 每題 with-skill 與 vanilla 各跑一次、同 rubric
   打分、skill 價值 = with−without 的 delta;若 assertion 只是描述
   base model 本來就會做的事，不算證明有效。
   已用 HTTPS 圖驗證 rubric 會**辨別**:同圖 id-6 contrast 過、
   id-8 restyle-structure 不過（0 個 var(--)、7 個 inline hex、
   0 個 semantic g-id，因它建於 restyle 規則之前）—— 證明 rubric 量
   的是真實且獨立的屬性，非橡皮圖章。

尚未做:完整 with-vs-without baseline run（需能 render／diff／腳本跑
產出 SVG，回 Claude Code 做）;把 deterministic `check` 串成自動
grader;format 詢問邏輯的 behavior eval 併入時一起跑。

### 文字溢框防治（2026-07 第四批）

使用者回報產出圖仍有文字超出物件框。根因:skill 早把這列為
"#1 SVG failure mode" 但只「警告」、靠人眼 budget，不可靠 ——
我自己的 HTTPS 測試圖就中招。優化 = 從警告升級成**工具強制**。

- 新增 `scripts/check_text_fit.py`（純 stdlib）。內嵌 Helvetica
  advance-width 表(units/1000 em)估算字串寬度,CJK 以 1em 計。
  mode A:`--text --size --max` 單行預檢;mode B:`--svg --pad`
  掃全圖 —— 解析 nested `translate()`、找每個 `<text>` 所屬 rect、
  比對是否超出卡片右緣(含 text-anchor middle/end)。scale/rotate
  子樹標為 unchecked。
- **實測比人眼準(雙向)**:跑 HTTPS 圖,**清掉**我以為會爆的
  "server's public key…"(273px 進得了 314px 卡),卻**抓到我漏看的**
  lane 副標溢框 +45px。修法:縮字 + 加寬 lane pill 220→250 →
  重掃 0 溢出 → 重 render。
- 串接:svg-construction.md text 段加**字數預算公式**
  (`max_chars ≈ inner_width / (0.55 × font_size)`)＋強制跑 script;
  pitfalls checklist、SKILL build step（與 contrast 並列的
  render-and-inspect gate）、output-quality id-7 加 `text-fits-boxes`
  criterion（附 `check`）。

現在產出前有兩道 deterministic gate:text-fit + contrast，皆可腳本
自動判。剩餘 backlog 同前（內容萃取、資料接口、座標 helper、
a11y title/desc、色盲模擬）。

### 統一檢查 gate（2026-07 第五批）

把分散的 script 收斂成單一 gate:新增 `scripts/check.py`,一道指令
給 PASS/FAIL 總判 + exit code,擋在「交付」前面。
`python scripts/check.py out.svg --bg <canvas> --pad <n>`

- **HARD gate**(fail→exit 1):text-fit 溢框、文字對比 <WCAG（**精確版**:
  解析每個 `<text>` 自己的顏色與其真實背景 —— 含 circle/ellipse 底 ——
  消除 check_contrast.py 分不出 text/surface 的誤報）、font-family 未命名、
  text 內含 emoji。
- **SOFT gate**(warn→exit 0):restyle 結構（:root var／semantic g-id）。
- 對比門檻誠實處理:bold ≥16px 視為 large text（3:1),讓「白字＋accent
  badge」這種標準且可讀的樣式過關（WCAG large=18.66px bold,略放寬並註明）。
- **雙向驗證 gate 會辨別**:修正版 HTTPS 圖 4 個 hard gate 全過（restyle
  WARN);故意做壞的 SVG 抓到 4 個 hard fail（溢框+190px、2 個對比、
  無 font、emoji 📊）exit 1。修過兩個自身誤報:circle 背景解析、emoji
  regex 誤掃排版箭頭 →←。
- 串接:SKILL build step 與 svg-construction.md checklist 都改成
  「跑 gate,exit 0 才交付」;check_text_fit / check_contrast 保留供
  iterate 時單獨用。gate 是 deliver 前的單一 enforcement 點。

### 產出品質 guard 正式化（2026-07 第六批）

先前 `check.py` 已存在,但只是 SKILL 裡「建議跑」的一步,且只管機械面。
本批把它**升級成不可跳過的交付契約 + 補上判斷面**。

- **兩層 guard**:機械面（script 自動判 exit code）+ 判斷面（step-9
  自評,agent 自證）。gate 指令現在跑完會**印出判斷面 checklist**
  （單一訊息／一個 L1 主宰／圖表誠實／非色彩單獨編碼／來源標註），
  不影響 exit code —— 一道指令給齊兩層。
- SKILL.md 新增獨立 **"## Delivery guard (do not skip)"** 段:明訂
  「gate 未 PASS 且判斷面未逐項確認前,不得 present／交付」,並要求
  交付時回報 gate 結果。HTML 產出走瀏覽器版同款判斷 guard。
- 措辭去除 test-process narration,改成 principle-based（符合 CLAUDE.md
  provenance 分離規範）。

至此 guard = 交付前的硬性 precondition,非可選建議。剩餘 backlog
同前（內容萃取、資料接口、座標 helper、a11y title/desc、色盲模擬;
及把 gate 接 pre-commit/CI 的版控強制,若要更硬)。

## 設計決策

1. **三層 hierarchy 是硬性規定**（不是建議）— 多於三層是最常見的
   失敗模式，寫成硬規則比寫成 guideline 有效。
2. **references 三分法**：layouts（決定骨架）/ charts（決定編碼）/
   color-typography（決定皮膚），對應 procedure 的 2 / 5 / 6 步 —
   讓 progressive disclosure 有清楚的載入時機。
3. **輸出預設 SVG**：可攜（任何 agent 都能寫檔）、可無損轉檔、
   一處改色。刻意不綁任何 host 的 artifact/widget 機制以維持
   portability。
4. **Skip 掉 deck 與 dashboard**：兩者的資訊密度預算與本 skill 的
   極簡規則衝突，寧可 route 出去。

## 尚未完成 / next steps

- [ ] **Stage 3–4（Test/Iterate）未跑**：evals/infographic-design/
      prompts.json 已備 trigger cases，但尚未做 with-vs-without
      baseline。先跑 3 個 positive prompts 的實際產出對照。
- [ ] output-quality.json 未建 — 候選 assertions：squint-test proxy
      （L1 元素面積/字級比）、bar 軸零基線、contrast 抽查、
      色彩僅編碼檢查、來源標註存在。
- [ ] description 未做 stage 5 優化 — 特別要驗證「單一 chart 請求」
      的 negative cases 不誤觸。
- [ ] 考慮 `scripts/`：contrast checker（hex pair → ratio）與
      SVG bar-scale 驗算是 deterministic，適合腳本化。
- [ ] 中文字型 stack（Noto Sans TC 等）尚未寫進
      color-typography.md — 若主要用例是繁中圖表，應補。

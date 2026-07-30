# Design notes — knowledge-doc-writing

這份記錄本 skill 的開發過程、設計理由與規則演化——provenance 與迭代日誌。

## 起源

從使用者過去在 Claude 手機 app 的對話中萃取出慣用的知識文件風格（What/Why 論述、辯證比較決策框架、ADR 式決策記錄、分層結構），加上一份使用者提供的 service mesh 一頁筆記作為風格範例，用 skill-creator 走完整流程開發。目標 repo 是 `leoluyi/skills`，需遵循其 CLAUDE.md 的開發慣例與 portability 要求。

## 設計決策

- **文件定位「兩者兼具依情境切換」**：學習筆記與正式文件共用同一套骨架，差別在口吻與模組取捨，而非兩套獨立系統。混合模式（正文正式、鷹架收附錄）用來處理「筆記之後可能要給團隊看」這種常見的曖昧情境。
- **費曼式自述檢核、待驗證問題清單設為 opt-in**：早期版本把這兩個模組設為學習筆記模式的預設項，使用者回饋這讓文件失焦。改為預設不出現，只在使用者明確要求、或輸入素材裡有使用者自己標記的未解問題（不收會遺失）時才啟用。
- **與 `learn-loop` skill 的分工**：`learn-loop` 負責互動學習與 distillation（其鐵律明講不可代寫），本 skill 只接手已 distill 完成的理解、轉成對外文件。這條分工線在 description 與銜接段落都刻意寫得比較硬，因為「learn → distill with new skill」這句話曾被誤讀成「本 skill 該做 distill」，需要明確排除這個誤讀。

## 論述紀律的演化（結構迭代裡分量最重的一段）

最早的版本只有「What/Why 論述＋辯證比較五件套」兩塊骨架，沒有專門規範條列與段落的分工，迭代中依序出現三個問題並修正：

1. **表格搶了論述的位置**：把使用者範例的「濃縮」學過頭，整份文件變成一堆表格拼接，缺乏完整論述段落，章節之間也沒有承接。修正：加入「論述紀律」一節，規定表格只做查表摘要、殿後於論述，且每節開頭要有承接句。
2. **改過頭變成 blog 節奏**：修正表格問題時矯枉過正，變成大段落敘事流，使用者指出這已經很像另一個 blog-writing-zh skill 的產出。修正：把「概念名 — 說明」的條列形態訂為知識文件的骨架，段落只保留給真正需要推論鏈的地方（解決的問題、比較成因、決策理由），並明文寫出與 blog 的分界：連續三段以上無條列即是 blog 的形狀。
3. **條列與段落之間仍缺乏嚴謹的邏輯關係**：光有「條列 vs 段落」的分工還不夠，條列本身需要引導句（交代清單性質）、有意義的順序（要嘛聲明順序、要嘛確認可任意排）、收束句（把清單結論接回論述）。這條規則同時下沉到章節與段落層級，形成「承接存在於每個層級」的統一規則，並提供了可操作的檢驗法：打亂順序重讀，讀不出差別就代表銜接不存在。

## 與 humanizer-zh 的關係演化

早期做法是把語言規則的判準直接寫進本 skill 的「語言與格式」節，這造成兩個問題：其一，`humanizer-zh` 本身漏了幾條本 skill 產出常犯的病（見下），逐條追加時，改動分散在兩個 skill 裡；其二，重複的判準與範例讓兩個 skill 的維護成本翻倍，且遲早會分歧。

處理方式是把 `humanizer-zh` 訂為語言規則的唯一真相來源，本 skill 只做兩件事：指向它、以及描述「這條語病如何影響本 skill 關心的文件結構」。這個重構移除了 knowledge-doc-writing 裡所有重複的判準與範例（例如完整的 mTLS bullet 範例只留在 humanizer-zh 一份）。

開發過程中發現並回饋進 `humanizer-zh`（v1.1.2 → v1.2.0）的五條新規則，全部由本 skill 的實際產出踩雷後歸納：

- **警句式評語**：破折號收尾的自我加值短評（「——這比任何文字定義都快」）、祈使式道德評語（「要誠實面對」）。
- **破碎短句堆疊**：正文論述段裡連續斷言短句只用分號並置，前提與因果缺席。
- **頓號串列代替論述**：概念首次出現處只用名詞頓號堆砌帶過，沒有任何一項被展開。
- **空降主張**：文中判斷句（非開場）缺乏前文依據、當場理由、或來源。使用者原話「不動既有認證與稽核邊界」是這條規則的起源案例。
- **破折號當萬用連接詞**：把因為、所以、例如、也就是等各司其職的連接詞全部用「——」取代，密度超過每千字一次即檢討。
- **過度簡寫的判準擴充**：原本只抓主詞受詞省略與名詞截斷，追加動詞缺席（以名詞片語代替動作）。起源案例是使用者範例裡的「安全 — 服務間自動 mTLS 加密與身分驗證，不必改程式」——動詞缺席（自動做什麼）、受詞截斷（不必改什麼才能得到什麼）。**這句話本身是本 skill 開發過程中發現的最佳教材，經使用者確認後直接收進 humanizer-zh 的 Fix 範例。**
- **慣用詞替換表新增「跳」**：network hop 的直譯，圈外讀者不知道跳的是什麼，句中也沒有動作與對象。使用者在對話裡提醒過兩次同一個問題（「多一跳」），第二次才真正落地成規則並回頭修正所有既有輸出。

這條教訓本身也被寫進「範例文件是風格參考，不是規則豁免」一節：使用者提供的 service mesh 範例決定了骨架與密度，但範例裡的破碎語句一樣要被抓、被改，不因為出自範例就放行。

## 方法論教訓：不能 patch 輸出，要重新產出

開發中期一度用 `str_replace` 手動修補已產出的文件來回應回饋（例如逐句改掉違反新規則的破折號），這個做法被使用者指出是方法論錯誤：patch 輸出只證明「我會改那幾句」，不證明 skill 本身能讓一個乾淨的執行者、不看舊輸出，依 SKILL.md 產出合格文件。

修正後的流程：每次改完 SKILL.md 或 references，下一輪測試一律當作沒看過任何舊版本，只依當下的 SKILL.md + references 從零重新產出，再對新產出跑機械掃描（連接用破折號密度、慣用詞 Flag 清單、bullet 完整句型）驗證規則是否真的在無人工干預下生效。這個順序本身也是後續維護這個 skill 時應該延續的規範。

## HTML／SVG 產出規則的來源

使用者要求 HTML 版的圖表統一用 SVG 以利機器編輯，並指定要有設計打磨。研究後選定 `frontend-design`（Anthropic 公開 skill）作為打磨層，理由是它已提供完整的 token system 流程（調色盤、字體配對、版面概念、signature 元素）與自我批判機制，不需要重新發明。實測範例（BFF 架構圖）的 signature 元素選擇把核心概念（擁有權）直接編碼進配色，讓 SVG 圖例與邊界地圖表格共用同一套視覺語彙。

## v1.0.0 → v1.1.0：HTML 產出規則的修正

發布 v1.0.0 之後，實際依 skill 產出多份 HTML 文件時發現規則本身有缺口，逐一修正：

- **frontend-design 的適用範圍過寬**：原規則要求整份 HTML 文件（版面、色彩、字體）都走 frontend-design 的 token system 流程，結果是每換一個主題就重新設計一套外觀（BFF 用藍青雙色、Quadlet 用琥珀靛青），使用者指出文件外殼應該固定套用預設模板，frontend-design 只該用在 SVG 圖表本身的內容設計（版面配置、視覺隱喻、圖例），且圖表配色要從文件既有 token 挑，不新開色票。修正後 baseline CSS 裡的顏色變數改用中性命名（`--accent-a`／`--accent-b`），不再綁定特定語意（例如「擁有權」），因為外殼是固定的，不該預設任何特定主題的顏色語意。
- **條列 marker 曾用連字號充當**：CSS 自訂 marker 一度用 `–`（en-dash），與「概念名 — 說明」的破折號分隔符形狀相近、容易混淆，改為真正的 `•`。
- **`code` 元素完全沒有 baseline 規則**：最早的 CSS baseline 沒定義 `code` 樣式，個別文件各自加了淺底樣式；套進 `.summary` 這種深色背景區塊時，`code` 沒有明確文字色、繼承父層的淺色文字，疊在淺色背景上完全看不清楚。修正：baseline 明確定義 `code{color:var(--text)}`，並針對深色區塊（`.summary`）加一條覆寫規則，同時把「深色背景區塊必須覆寫 code 對比度」的原因寫進 CSS 註解，避免未來新增深色區塊時重蹈覆轍。
- **最小可運行範例模組原本只有文字描述**：`modules.md` 只講「要給可複製貼上的步驟」，沒有給出格式範例本身。補了兩組具體程式碼（GPU Operator 的 bash 驗證步驟、Quadlet 的 `.ini` 設定檔對比），讓判準（「期望輸出寫在指令旁的註解，不要另外用文字描述」）有實例可循，而非只停留在描述。
- **「一頁總結」改名「一段話總結」**：這個名字是從 service mesh 範例借來的，範例本身是一頁筆記，「一頁總結」對它成立；但本 skill 產出的多是多章節文件，這一節實際上是三行話的收束段，「一頁」名不副實，改成準確描述內容的「一段話總結」。

這輪修正也再次印證了「改完 skill 要從零重產，不能 patch」的方法論：每條規則改完都重新產出受影響的文件（而非在舊檔案上直接改樣式），確保規則本身站得住、不是靠人工修補撐過測試。

## v1.1.0 → v1.2.0：圖表打磨層由 frontend-design 改為 infographic-design

原本借 `frontend-design`（Anthropic 公開 skill）當 SVG 圖表的內容打磨層（見上「HTML／SVG 產出規則的來源」）。改用同 repo 的 `infographic-design`，理由：

- **原生產出自足 SVG**，與本 skill「圖表一律 inline SVG」的規則同一個目標，不必再把通用前端 token system 流程裁剪成圖表用途。
- **有現成的 layout archetype 與三層資訊層級**（流程/對照/剖解、L1 takeaway／L2 sections／L3 support），比 frontend-design 的通用版面概念更貼合本 skill 固定的架構圖、流程圖、對照圖幾種圖型。
- **`references/bytebytego-style.md` 的編號走查**專門處理「機制怎麼運作」的技術圖，正是知識文件裡架構圖最需要、frontend-design 沒有的東西。
- **自我批判迴圈**（squint／8 秒測試）與原本借用 frontend-design 的自我批判等價。

沿用不變的是 v1.1.0 定下的邊界：打磨層只作用在圖表內容，文件外殼與色彩／字體以固定模板為準。這次把這條 override 講得更硬——SKILL.md 裡明文蓋掉 infographic-design 自己的色彩與字體系統（其 step 7 與 `references/color-typography.md`），以及它針對「單張獨立 infographic」的交付品質閘（`scripts/check.py` 那套 delivery guard）。因為這裡的圖是嵌在 HTML 文件內的 figure，視覺語言必須跟正文一致，走的是本節固定模板的 token，不套獨立 infographic 的配色與交付檢查。既有的 frontend-design 歷史段落保留不刪，那是 v1.0→v1.1 的準確紀錄。

## v1.2.0 → v1.3.0：新增輸入模式 D「既有文件改寫」

原本三種輸入模式（對話紀錄整理、原始資料整理、從零自學產出）共同的預設是「產出一份新文件」。這個預設在輸入本身就是一份既有知識文件時失靈：使用者要嘛被拗進模式 C，整份文件從零重寫、丟掉舊文件裡已經寫對的論述；要嘛被拗進模式 B，把舊文件當成一手素材，版本號、預設值、已淘汰替代方案等時效性內容原封不動被抄進新版，沒有人重新查證。兩條路徑都沒有「這份輸入本身已經是（或曾經是）一份完稿」這個事實的容身之處，也都不會產出任何交代「改了什麼」的紀錄。這是模式 D 要補的洞。

### 四個子情境為什麼收斂成一個模式，而不是四個模式

重構、更新時效、併入新素材、品質升級這四件事，實際使用時幾乎必然共同出現——使用者丟一份舊文件來，通常同時想順便修過期的版本號、順便補一段缺的比較段、順便把某段新素材塞進去。拆成四個模式會強迫使用者自己先分類意圖，且四者的判斷分界並不清楚（「品質升級」跟「更新時效」的界線常常是同一段落）。真正決定「該做多深」的變因不是使用者講出哪個詞，而是輸入文件的出身：已經是本 skill 骨架的文件，多數工作是定點修補；外來格式的文件，多數工作是整份重構。所以模式 D 把出身判斷做成第一步的 gate，讓四個子情境共用同一套「先辨識、再決定深度」的流程，而不是四條互斥的分支。

### 為什麼「保守改寫 vs 從零重產」要每次問，不能寫死預設

兩個方向各自有明確的失敗模式：預設一律保守，遇到外來格式、結構本身就是錯的文件時，改寫者會被綁在一個爛骨架裡小修小補，永遠到不了「What/Why + 辯證比較五件套」；預設一律重產，遇到使用者自己半年前依這個 skill 寫的文件時，會把還站得住的論述、已經查證過的判斷全部推翻重講，使用者明確要求「其他寫對的地方不要動」時尤其是浪費工也是對使用者判斷的不尊重。這個抉擇是文件相關（doc-dependent），無法從輸入格式或任務描述單方面推斷——同一句「幫我更新一下這份文件」，背後可能是要保留 90% 內容只換幾個版本號，也可能是要整份打掉重練。唯一可靠的做法是每次動筆前問使用者，不做預設猜測。

### 「不能 patch 輸出，要重新產出」管的是 skill 自我測試，不是使用者文件的執行時修訂

測試 SKILL.md 本身是否有效時，不能拿舊輸出手動 patch 幾句話就宣稱規則生效，必須讓一個沒看過舊輸出的乾淨執行者，只依當下的 SKILL.md + references 從零重新產出，才能證明規則在無人工干預下真的起作用。這條紀律的對象是「測試者驗證 skill」的迴圈，發生在開發時、面對的是 skill 自己的產出。

模式 D 的保守改寫則是「skill 服務使用者」的執行時行為，發生在使用者帶著一份自己的真實文件來的時候——這份文件不是 skill 上一輪的測試輸出，是使用者的資產。保留其中已經正確、已經查證過的內容，是對使用者判斷與既有工作的尊重，不是方法論上的偷懶或未經驗證的補丁。兩者面對的是完全不同的物件（skill 的自我測試產出 vs. 使用者的真實文件），評價標準也不同（「乾淨執行者能否重現品質」vs.「有沒有不必要地丟掉使用者已經確認正確的內容」）。這裡特別寫下來，是因為兩者字面上都在講「要不要重新產出」，容易被下一位維護者望文生義地合併成同一條規則，進而把模式 D 的保守改寫「修正」成強制重產——那會直接違反本節第二段講的、使用者體感最差的失敗模式。

### 與 humanizer-zh 的邊界

既有的邊界（「只做語言層去 AI 味不動結構」歸 humanizer-zh）本來就存在，模式 D 沒有新開一條規則，只是把它套用到一個新情境：品質升級子情境容易被「移除 AI 味」這句話拉去做純語感潤飾。分界依然是同一個——這次改動有沒有動到文件說了什麼、怎麼組織（模式 D 的工作），還是只動一句話怎麼講（humanizer-zh 的工作）。模式 D 的品質升級只處理結構性缺陷（空洞的 What/Why、缺漏的「何時不該採用」、退化成名詞堆砌的條列），句子層級的 AI 味清理仍然留給完稿檢查階段委派給 humanizer-zh，不在模式 D 裡代做。

## v1.3.1 → v2.0.0（已實作 2026-07-20）：改用 Diátaxis 架構

使用者決定不再自創骨架命名，改以 Diátaxis 框架為結構主軸（Option A：產出四類文件）。動筆前用 workflow 蒸餾了 diataxis.fr 全站 18 頁核心概念，成果與 refactor 計畫存在 `research/`：

- `research/diataxis.md` — 全站 prose 蒸餾（總綱、四型、compass、map、complex hierarchies、兩對混淆、兩層品質、workflow、對四類產生器的含義）。這是 dev/authoring 參考，不是 runtime；若 refactor 後需要 runtime 版 Diátaxis 速查，另從此檔萃取一份去除 provenance 的 `references/diataxis.md`。
- `research/diataxis-refactor-plan.md` — Option A 的 refactor 計畫、現有內容→四型對映、待決策項。

（早期曾用 caveman 模式蒸餾，因壓縮丟失完整句與框架原意、且只涵蓋四型頁而缺 compass/map/quality/workflow，作廢改用 prose 全站版。）

### Eval spec（先於 SKILL 改寫定案，2026-07-19）

依 TDD 精神先把「四類產出該怎麼考」寫成 `evals/`，再改 SKILL.md。兩個決策：

- **分區 baseline**（解決產品轉向與 repo「須贏過前一版」硬規的張力）：每個 eval case 標 `baseline` 欄。行為未被 pivot 動到的 case（learn 銜接 handoff、HTML inline SVG、Mode D 更新時效 point-patch）baseline=`v1.3.1`，gate=v2.0.0 不得回歸；四型區塊路由/邊界純度/缺型標記等新行為 baseline=`vanilla`，gate=v2.0.0 須贏過無 skill。理由：對 v1.3.1 跑四型 evals 會 trivially 失敗，該 gate 無意義；反之用舊 evals 判 v2.0.0 會把「五件套併入 explanation」這類正確 pivot 誤判為缺漏。
- **Mode D 依意圖分流**：收到既有文件時 gate on 意圖而非動詞——`更新時效`/`併入新素材`→ point-patch 保留輸入原形狀（即使是 pre-v2.0.0 單一文件骨架也不強拆）；`重整`/`重構`→ 依 compass 整份路由進四型區塊。體現於 eval #7（point-patch）與 #8（重構→四型）。

判準維度（positive case rubric）：compass 路由正確、每個在場區塊的邊界純度、缺型誠實（不搭空殼不捏造）、分離維持（不 blur）、functional quality（一手來源+時效）、保留的語言要求。新增兩條 leading-word 觸發防呆負例：`tutorial` 練習專案→learn-loop（trigger #15）、OpenAPI→reference 機械產生→非自學蒸餾（trigger #16）。

### SKILL.md 實作（2026-07-20）

用 judge-panel workflow（4 個設計 lens 各出一版 spine → 5 維 rubric 評分 → 綜合）產生骨幹。背骨採 compass-router-first（評分最高），嫁接 minimalist-anti-sprawl（純度寫進完成準則、CSS 下沉、references 整併、leading-word 退役自創命名）、coverage-fidelity（可攜去 AI 味框架、缺口二元判準、三層承接跨型化）、iterative-workflow-first（功能性閘措辭、complete≠finished）。

SKILL.md 收斂為 7 節（S0 前言 + S1 開工/Mode D 意圖閘 + S2 compass 路由 + S3 四型區塊 + S4 維持分離 + S5 語言格式含 HTML + S6 完稿檢查）。自創命名以四個 Diátaxis leading word 退役：五件套→explanation 的 weigh-alternatives、情境模組 ADR→explanation、自學消化模組→依型路由、論述紀律→explanation 的 discursive 屬性。

實作期三個 open question 的定案（使用者授權代決）：

1. **去 AI 味可攜化（唯一的 v1.3.1 行為變更）**：原本硬性以 `humanizer-zh` 的 detect 當載重完稿門，違反 repo「sibling 不得載重」硬規。改為：**可用時優先呼叫 `humanizer-zh`**（它是權威工具），不可載入時 fallback 到 SKILL.md S6 內建的精簡判準清單。sibling 為可選、非前置依賴，核心產出可獨立完成（符合硬規），可用時仍用最好的工具——不是把 sibling 降級成內建清單的加速器。
2. **references 整併**：`modules.md` + `skeletons.md` 併入 `blocks.md`（依 Diátaxis 型別重排、消化模組全落 explanation），最終三個下沉檔 `blocks.md`／`rewrite.md`／`html.md`（約 67 行 CSS 從正文抽進 html.md 瘦身）。
3. **迭代工作模式**：折進 S6 當子節（complete≠finished／由內而外生長／cycle-of-needs 覆蓋），不獨立成節，保持 spine tight。

Mode D `rewrite.md` 出身辨識訊號已更新：v2.0.0 四型結構與 pre-v2.0.0 單一骨架都算「本 skill 骨架 → point-patch」，意圖分流短路 compass。

**待辦（下次）**：跑 `evals/` 對照 baseline（preserved 對 v1.3.1、pivoted/new 對 vanilla），確認 v2.0.0 過關才可 merge——此為 repo 硬規 gate，push branch 非 merge，故本次先推分支留待 eval 驗證。`research/` 兩檔為 dev 材料，保留不進 runtime。

## 已知限制 / 後續可做

- 分層結構（Application/Middleware/Infrastructure/Hardware）與 ADR 情境模組尚未各自跑過從零重產的完整測試迴圈，目前只在早期（patch 方法論修正之前）的 BFF 測試中驗證過 ADR 部分。下次遇到適合分層結構的主題（如 AI 平台或容器平台）時，應補一輪從零重產測試。
- 「最小可運行範例」模組只在 GPU Operator 一份文件中實測過；尚未測試對話整理或混合模式底下這個模組的行為。
- 描述觸發優化（trigger eval，20 條 should/should-not-trigger 查詢）尚未執行，見 skill-creator 的 Description Optimization 步驟。

# Diátaxis 全站蒸餾

來源：https://diataxis.fr/ 全站 18 頁（作者 Daniele Procida）
授權：Diátaxis 採 CC BY-SA 4.0（https://creativecommons.org/licenses/by-sa/4.0/）。本蒸餾為衍生內容，同以 CC BY-SA 4.0 釋出，署名 Daniele Procida。

---

## 0. 框架總綱

Diátaxis 是一套**務實方法論**（pragmatic methodology），不是照抄的硬規範。名稱源自希臘文 dia（跨越）＋ taxis（排列）＝「跨越式的排列」。

**唯一 founding principle**：技術文件應圍繞**使用者需求的結構**來組織，而非依主題、產品架構、或作者方便來堆疊。

從使用者需求的系統性分析，導出四種各自獨立、不可互相替代的文件形式。關鍵不在「有四種」，而在四種被放進**系統性關係**——沿兩軸展開成一張二維地圖，彼此有相對位置與張力。

各部件如何組合：
- **foundations** — 論證為什麼恰好是四種（兩軸窮盡任一門技藝的領域，不可能三或五）。
- **the map** — 把四型攤成二維結構，看見整體版圖與相鄰關係。
- **the compass** — 把地圖兩軸轉成兩個提問，即時判斷任一段內容歸哪型。
- **quality model** — 界定 Diátaxis 對品質能做什麼、不能做什麼。
- **workflow** — 把理論落成可日常執行的迭代節奏。

框架同時處理三面向，處方都從「服務哪種需求」推導：**Content**（寫什麼）／**Style**（怎麼寫）／**Architecture**（怎麼組織）。

---

## 1. 四種類型（need / orientation / 邊界 / 隱含問題）

| 類型 | need | orientation | 隱含問題 |
|---|---|---|---|
| Tutorial | study 習得技能 | learning-oriented | can you teach me to…? |
| How-to guide | work 完成具體任務 | task-oriented | how do I…? |
| Reference | work 中查閱、要確定性 | information-oriented | what is…? |
| Explanation | study 中的理解 | understanding-oriented | can you tell me about…? |

**Tutorial**：一堂課，在 tutor 指導下的 learning experience，牽著學習者的手走過去，透過「做」建立信心。學習者做了什麼未必等於學到什麼。邊界：不解釋、不追求完整、不放真實世界分支；路徑是一條消除意外的直線，追求 **perfect reliability**，成敗責任幾乎全在作者／老師。第一守則「別想著教」，提供有意義的活動讓學習自己發生。語言：第一人稱複數 We…、祈使句、Notice that…、You have built…。「A tutorial is not the place for explanation.」

**How-to guide**：goal-oriented directions，引導**已具能力、已知目標**的使用者穿過問題抵達結果。邊界：assume competence，只放行動，不教學不解釋不離題；容許多個進出點與條件分支（if this, then that），實用勝過完整。標題精確說出它展示什麼（`How to integrate…`，非 `Application performance monitoring`）。從使用者**目的**出發，不描述工具怎麼動（別停在「按電源鍵開機」這種層次）。食譜類比。「How-to guides are wholly distinct from tutorials.」

**Reference**：「機器及其操作方式的技術描述」，承載 propositional/theoretical knowledge。使用者需要它因為需要 **truth and certainty**——工作時可站立其上的堅實平台。必須 wholly authoritative，不容 doubt/ambiguity，語氣 austere、中性。四原則：**Describe and only describe** ／ Adopt standard patterns（一致）／ Respect the structure of the machinery（結構 mirror 產品）／ Provide examples（illustrate 不越界成教學）。人不是「讀」它而是「consult」它。食品標示類比：只放中性事實，混入食譜或行銷「literally dangerous」。

**Explanation**：discursive、reflective 的主題探討，回答 **why**，織入脈絡、背景、歷史、設計理由、被否決的替代方案。**可帶觀點與判斷**（w is better than z, because…）——這是它與其他三型最大不同，其他型抗拒意見，explanation 要求它。以 **topic area 為界**（非任務或學習目標），唯一能離開產品悠閒閱讀的類型。標題用 `About…` 測試。無它，實踐者的知識「remains loose and fragmented and fragile」。不是奢侈品，價值在較長時間軸才顯現。

---

## 2. Compass — 兩題定位（任何尺度）

判斷任一段內容歸哪型，只問兩題（不靠直覺，靠判準）：

1. **action or cognition?** — 內容要讀者去「做」（動作導向），還是增進理解／認知（知識導向）。
2. **acquisition or application?** — 服務讀者習得技能的階段（at study，學習中），還是已有技能要運用的階段（at work，工作中）。

兩答案的組合機械式指向唯一一型：

| | acquisition（學） | application（用） |
|---|---|---|
| **action（做）** | Learning → **Tutorial** | Goals → **How-to** |
| **cognition（想）** | Understanding → **Explanation** | Information → **Reference** |

四 need 來自一門技藝的固有結構：任何 craft 都同時含 action（knowing how）與 cognition（knowing that），也都既需被 acquired 又需被 applied。兩軸交叉窮盡覆蓋整片領域——這就是為什麼「必然是四，不多不少」。

**用法**：可近到單句、單詞，遠到整份文件；先定整份的位，再放大到段落句子，確認每個小單位都與所屬型一致。**一段內容同時橫跨兩象限＝該拆分的訊號。**

---

## 3. The map — 二維結構與相鄰混淆

文件不是清單（a list），是二維結構（two-dimensional structure），把四型放進**彼此的關係**中。清單只把四類並排，二維結構呈現相對位置與張力。

**相鄰必共享一維，因此最易混淆：**
- Tutorial ↔ How-to（同屬 action，差在學習 vs 達成目標）→ 見 §5 最致命混淆。
- Reference ↔ Explanation（都含 propositional knowledge，差在陳述機制 vs 討論理由）。

使用者對產品的互動是 **cycle of interaction**，對應 **cycle of documentation needs**：人會在學習、達成目標、查資訊、求理解之間**循環移動**，四象限存在正是為完整覆蓋這個循環。

雙重報酬：給讀者 **clear expectations**（打開這頁該期待什麼）＋給作者 **guidance**（這段目的為何、怎麼寫、放哪）。

---

## 4. Complex hierarchies — 組織真實大型文件集

- 某一型底下項目變多 → 在其內部**新增一層階層**分組，別讓清單無限拉長。
- **Seven items** 是舒適的一般上限，超過就下沉成子階層。
- landing／contents page 不該只是連結清單 → 應像 **overview**，帶介紹性散文。
- 最棘手：**two-dimensional problems**——Diátaxis 結構撞上另一維度（多平台、多角色 land/sea/air），造成冗餘與「階層往哪走」兩難。
- 關鍵認知：**Diátaxis is not four boxes**（不是要把文件塞進的 scheme），是一種 approach，可用那張圖表現但**不等於那張圖**。只要不同類型不被混淆，文件可放心變複雜、加深階層。
- 最終仲裁者是**讀者體驗**：「you are always authoring for a human user, not fulfilling the demands of a scheme」。

---

## 5. 兩對混淆的分辨測試

**Tutorial vs How-to（最常見、最致命）** — 根本判準是使用者狀態 **at study vs at work**，不是內容複雜度：

| | Tutorial | How-to |
|---|---|---|
| 使用者 | at study，尚未具能力的學徒 | at work，已具能力 |
| 目的 | acquire basic competence | perform a particular task correctly |
| 路徑 | 受控直線、消除意外、single line | 真實世界、fork and branch、if-then |
| 熟悉度 | explicit about basic things | assume familiarity |
| 安全性 | safe / reversible | 可能不可逆、高風險 |
| 責任 | 在老師／作者 | 在使用者 |

此混淆特別致命，因為它擋在新手面前——最想轉成忠實使用者的人。醫學情境裡混教育與實務的手冊是「literally deadly document」。

**Reference vs Explanation** — describe or discuss？中性乾事實、無意見、mirror 產品結構＝reference；discursive、表態、weigh alternatives、給 why＝explanation。試金石：機器能否從程式碼 dump（reference）vs 需要判斷／視角（explanation）。

---

## 6. Quality model — 兩層品質

**Functional quality**（功能性）：accuracy、completeness、consistency、usefulness、precision。可客觀衡量、對照現實檢驗、有時可量測；各特性獨立（可準確卻不完整）。是 constraint／conformity，像一組要通過的測試，靠紀律與規則達成，缺失使用者立刻看得出。

**Deep quality**（深層）：feeling good to use、having flow、fitting human needs、being beautiful、anticipating the user。體驗性、主觀、彼此交纏；只能靠 judgement 而非 measurement；是 liberation／invention，需超越原則持續發明。

**關鍵關係**：**deep quality is conditional upon functional quality**。再美也補救不了不準確或不一致；功能缺陷直接毀掉深層品質，順序不能顛倒。

Diátaxis 對兩層作用不同：**無法 create 功能性品質，但能 expose lapses**（把 reference 結構對齊程式碼架構，缺口就無所遁形）；**能主動貢獻深層品質**（依 mode 組織貼合需求、守住邊界保住 flow），但只是「lay down conditions for the possibility of deep quality」，不保證美、不替代 UX 專業。

→ 這解釋為何「一次到位的完美主義」是錯的：功能是可逐步逼近的約束，深層是永遠在發明的空間，兩者都指向**迭代**。

---

## 7. Workflow — 怎麼實際運用

- Diátaxis 是 **a guide to work, not a plan**：反對由上而下規劃與大爆炸改版，偏好**小而有回應的迭代**，讓整體結構從局部健康**自然浮現**。
- **應用先於理解**：別等完全懂才動手——「你在開始用之前根本不會懂它（這本身就是一條 Diátaxis 原則）」。
- **不要先搭四個空殼再填**；讓四型內容從實際文件長出來。
- 持續四步迴圈：**Choose something**（挑任一小片段）→ **Assess it**（用 Diátaxis 標準批判：服務需求嗎？哪型？符合規範嗎？）→ **Decide the next single action** → **Do it**（做完、視為完成、立刻發布）→ 回到迴圈。
- **complete ≠ finished**：文件永遠不會 finished（永遠演化），但隨時可以是 complete——對使用者有用、符合現階段、結構健康。每次小改動當下就有價值。
- **有機生長**：把每個局部組件做健全，整體結構會像活的有機體由內而外、一次一個細胞長成。Diátaxis 從**內部**改變結構，非從外部強壓骨架。

---

## 8. 對「四類文件產生器」的具體含義

1. **四型各需獨立產生規則**，不是一個模板套四次。各型的規則見 §1／§5。
2. **compass 當路由器**：把自學主題的每段素材先問兩題再分派；同段橫跨兩象限＝拆分訊號，不塞同一份。
3. **以 cycle of documentation needs 檢查覆蓋度**：一個自學技術主題天然產生四種需求（想上手／想完成任務／想查參數／想懂原理）；確認四型都涵蓋，缺哪型補哪型，別只產最好寫的 explanation／reference。
4. **主動維持類型分離、抵抗 blur**：產出後自審，把跑進 tutorial 的工作分支、跑進 reference 的論述抽出各歸其位；跨型內容用**連結互指**，不混寫。
5. **套 complexity 規則組織產物**：某型項目多就加階層分組；清單 ≤ 七項；每個 landing／區段開頭寫 overview 散文；有第二維度（多平台／多角色）允許結構變複雜，只要四型不混淆，以讀者體驗決定階層方向。
6. **兩層品質當完稿檢查**：先保 functional quality（accuracy/completeness/consistency/usefulness/precision）——自學產物尤其**強制查證一手來源、標註時效**，因深層品質 conditional upon 功能性品質；再靠依 mode 組織與守邊界鋪 flow。
7. **迭代／有機生長而非一次到位**：不求一次產四份完美完稿；每型先達 complete（當下有用、結構健康）再迭代深化；每型可獨立發布、獨立演化。
8. **產物是 runtime 文件而非過程紀錄**：四份只留該型該有的內容，把學習／推導 provenance（比較了什麼、第幾版、recall 數字）排除在成品外——呼應各型邊界純度。

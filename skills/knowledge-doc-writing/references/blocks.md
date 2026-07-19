# 四型區塊產生規則與示範

依 Diátaxis 型別編排。動手寫任一區塊前讀對應段；寫完跑「相鄰混淆分辨測試」。組裝順序模板見文末。

---

## explanation（understanding-oriented）

唯一可帶判斷的區塊。承載 What/Why 論述、辯證比較五件套（internal recipe，不自成頂層骨架）、ADR 決策理由、心智模型、常見誤解、前置知識地圖、opt-in 附錄。

### What/Why 論述的寫法

三段各自要回答的問題，與好壞對照：

**功能定位** — 回答「它站在系統的哪裡」。

> 不合格：Istio 是一個 service mesh。
>
> 合格：Istio 在微服務架構裡佔的位置是「服務與服務之間的通訊層」：它把原本散落在各服務程式碼裡的流量控制、加密、觀測邏輯，抽出來放進與應用程式並行的 sidecar proxy（或 ambient 模式的節點層代理），讓應用程式碼回到只處理商業邏輯。

**解決的問題** — 回答「沒有它，大家原本怎麼受苦」。這段是整份文件的錨點，寫的時候想像讀者會問「所以呢？我為什麼要在乎？」。

> 不合格：它解決了微服務通訊的問題。
>
> 合格：服務數量到幾十個之後，每個團隊各自在程式碼裡實作 retry、timeout、mTLS，實作品質不一且無法統一稽核；金融業的資安檢視會直接卡在「你如何證明所有服務間流量都加密」這一題。Service mesh 把這些橫切關注點下沉到平台層，讓「全部加密」從各團隊的自律變成平台的預設。

**主要功能要求** — 回答「它做到什麼才算稱職」，用可檢驗的敘述。

> 不合格：提供流量管理、安全性、可觀測性。
>
> 合格：它至少要做到三件事才值得引入：(1) 服務間流量可以不改應用程式碼就套用路由規則與故障注入；(2) mTLS 可以全網格強制開啟並集中輪替憑證；(3) 每個服務之間的轉發延遲與錯誤率，可以在不修改應用程式碼的前提下被收集。

單純名詞條列（「功能：A、B、C」）不合格——條列可出現在論述之後當摘要，不能取代論述。

### 辯證比較五件套（explanation 內部 recipe）

主題有替代方案或易混淆的鄰居時（幾乎所有主題都有），寫在 explanation 內作 alternatives-weighing，**允許明確表態**（w 優於 z，because…）。以「service mesh vs API gateway」為例：

1. **定義** — 各一句話。「API gateway 處理南北向流量（外部進入系統），service mesh 處理東西向流量（服務彼此之間）。」
2. **行為職責邊界** — 各自明確不管什麼。「Gateway 不介入服務 A 呼叫服務 B；mesh 不做對外的認證授權與 rate limiting，那是 gateway 的門面職責。」邊界寫清楚，比較才不會雞同鴨講。
3. **比較分析** — 逐面向且寫出差異成因。「Gateway 是集中式單點，升級影響面大但運維心智負擔小；mesh 是分散式，proxy 隨服務部署，升級要處理資料平面滾動更新。」
4. **邊界判斷表** — 收灰色地帶：

   | 情境 | 用哪個 | 為什麼 |
   |---|---|---|
   | 對外 API 需要 API key 管理與計費 | gateway | 商業層關注點，mesh 沒有這個抽象 |
   | 內部服務間要 mTLS 與細粒度授權 | mesh | 東西向流量，gateway 看不到 |
   | 只有 5 個服務、單一團隊 | 都先不用 | 引入成本高於收益，函式庫級的 retry／timeout 就夠 |

5. **決策框架** — 「該採用」與「不該採用」各寫成條件式：「服務數量超過 N、跨多團隊、有稽核要求 → 評估導入」「服務少、單團隊、無合規壓力 → 不要導入，運維成本會吃掉你」。「不該」那半邊與「該」同等重要，省略它的比較只是廣告。

### ADR 決策理由（併入 explanation 論述，不另立模組）

主題背後有實際待做或已做的決策時（「我們該不該導入 service mesh」），把理由織進論述：背景 → 考量的選項（各自優缺點）→ 決策 → 理由 → 已知代價 → 後續行動。「考量的選項」直接引用前面比較分析的結論，不重寫。**已知代價一節必填**：沒有代價的決策記錄代表分析沒做完。理由段回指前文已建立的事實，不空降。

### 心智模型與類比

給一個可拿來推理的類比，並**一定標註類比在哪裡失效**，否則讀者會推過頭。

> Sidecar proxy 像每個服務配一個專屬總機：所有進出電話都先過總機，所以錄音（觀測）、擋騷擾電話（授權）、轉接（路由）都在總機做，服務本人只管講話內容。
> **類比失效處**：總機是人力成本，sidecar 是每個 pod 多吃的 CPU／記憶體與多一跳的轉發延遲；這個成本隨 pod 數線性成長，總機類比感受不到，而它正是 ambient mesh 出現的原因。

### 常見誤解與陷阱

收兩類：初學者自然形成的錯誤直覺、網路上流傳但已過時的說法。每條寫成「誤解 → 為什麼會這樣想 → 實際上」三拍。過時說法註明從哪版起不成立。

> **誤解**：rootless Podman 容器內的 root 就是主機的 root，所以一樣危險。
> **為什麼會這樣想**：容器內 `whoami` 顯示 root，直覺上就是 root。
> **實際上**：rootless 模式下容器內的 UID 0 透過 user namespace 映射到主機上的一般使用者 subuid 區段，逃逸出來也只有一般使用者權限——這正是金融業環境選 rootless 的核心理由。

### 前置知識地圖

列出理解本主題前必須先懂的概念，每項附一句話「它跟本主題的關係」，有先後依賴就標順序。放 explanation 開頭（或 tutorial 前置，依素材落點）。

> 學 GPU Operator 之前要先懂：
> - **Kubernetes Operator pattern** — GPU Operator 就是一個 operator，不懂 reconcile 迴圈就看不懂它為什麼能自動修復驅動狀態。
> - **DaemonSet** — 驅動與 device plugin 都以 DaemonSet 佈署到每個 GPU 節點，除錯第一步就是看這些 DaemonSet。
> - **容器內核心模組載入的限制** — 這是整個 driver container 設計要繞過的根本問題。

收錄門檻：讀者缺了會「完全看不懂」才收；只是「更好」的背景不收，地圖太長就失去導航功能。

### 論述紀律

explanation 的骨架是可掃描結構（條列與表格），關節是論述（推論鏈）：

1. **關鍵概念用條列，每條自帶論述**。形態「**概念名** — 一到兩句完整說明（它是什麼＋為什麼）」。說明要是完整句（主詞動詞受詞齊全）。超過兩三句、需要推論鏈時升級成段落。
2. **段落保留給推論鏈**。解決的問題、比較差異的成因、決策理由，前提與因果要寫全。連續三段以上純段落而無條列或表格，是 blog 的形狀，回頭抽出可條列的概念。
3. **表格殿後**。表格是查表摘要，不得出現前文未建立的新主張；整份刪掉表格論證仍應完整。
4. **每個判斷句有來處**（前文依據／當場理由／來源三者之一），ADR 理由段從嚴。

### opt-in 附錄（預設關）

住 explanation 附錄，預設不放。啟用門見 SKILL.md S3。

**費曼式自述檢核**：使用者要求時啟用。用自己的話、不看資料把核心概念重講給想像中的同事，標出兩種破綻：講到一半卡住（概念沒接起來）、只能複誦原文措辭（沒內化）。每個破綻對應一個行動（回讀某段／丟進待驗證清單）。保留口語感、允許不精確——修飾過的自述測不出東西。

**待驗證問題清單**：使用者要求時啟用；或輸入素材含使用者自標的未解問題（如對話中「這個還要確認」）——不收就會遺失，此時照收。每題三欄：問題本身、為什麼在意（不寫這欄的常常其實不重要，可刪）、怎麼驗證（具體到可執行）。

> **問題**：ambient 模式下 L7 授權是否一定要經過 waypoint proxy？
> **為什麼在意**：影響授權政策寫在哪一層，以及 waypoint 是否成為新的容量瓶頸。
> **怎麼驗證**：讀 Istio ambient 官方文件 waypoint 章節；在測試叢集開 L7 policy 不佈 waypoint，觀察是否生效。

---

## reference（information-oriented）

「機器及其操作方式的技術描述」，承載讀者工作時要站立其上的確定性。四原則：

1. **Describe and only describe** — 只放中性事實，混入 recipe 或行銷「literally dangerous」。
2. **Adopt standard patterns** — 一致的呈現格式。
3. **Respect the structure of the machinery** — 結構 mirror 產品（模組、旗標、CRD 欄位按產品本身的結構排）。
4. **Provide examples** — illustrate，不越界成教學。

語氣 austere、中性；讀者「consult」它而非「read」它。旗標與參數整理成表；設定檔區段語意逐項描述。

> `[Container]` 區段鍵（節錄，describe-only）：
>
> | 鍵 | 作用 | 備註 |
> |---|---|---|
> | `Image` | 容器映像來源 | 必填 |
> | `PublishPort` | 對主機發布連接埠 | 格式 `host:container` |
> | `HealthCmd` | 健康檢查指令 | 對應 systemd 的 health 監測 |

判斷「這是 reference 還是 explanation」：機器能否從程式碼／spec dump 出來＝reference；需要判斷或視角＝explanation。

---

## tutorial（learning-oriented）

一堂在指導下的 learning experience，牽著尚未具能力的學習者走過去，透過「做」建立信心。邊界：不解釋、不追求完整、不放真實世界分支；路徑是一條消除意外的**單一安全直線**，追求 perfect reliability。語言：第一人稱複數祈使（We…／Notice that…／You have built…）。「A tutorial is not the place for explanation.」

素材前提：**作者真的親手第一次走過**。研究過但沒跑過的主題常缺這型素材 → S2 標缺口，不捏造。

最小可運行範例（at-study 版，收進 tutorial）：讓學習者在目標環境十分鐘內跑起來、親眼看到核心行為。收前置條件、可複製貼上的最短步驟、以及「看到什麼才算成功」的判準（比步驟更重要）。每個指令後用註解直接寫期望輸出。

```bash
# 前置條件：OpenShift 4.14+ 叢集、至少一個 GPU 節點、已建立預設 ClusterPolicy

# 1. 確認 ClusterPolicy 已收斂完成
oc get clusterpolicy gpu-cluster-policy -o jsonpath='{.status.state}'   # 期望輸出: ready

# 2. 確認 GPU 資源已註冊到節點
oc get node -l nvidia.com/gpu.present=true \
  -o jsonpath='{.items[*].status.allocatable.nvidia\.com/gpu}'          # 期望輸出: 每個節點各自的 GPU 數量

# 3. 實際排程一個 GPU 工作負載並驗證可用
oc run cuda-smoke --image=nvcr.io/nvidia/cuda:12.4.1-base-ubi9 \
  --restart=Never --limits=nvidia.com/gpu=1 -- nvidia-smi
oc logs cuda-smoke                                                       # 期望輸出: nvidia-smi 列出的 GPU 清單
```

步驟要在預設技術脈絡（RHEL + rootless Podman、OpenShift）下可行；指令與版本查證過，不確定的旗標寧可不寫。

---

## how-to（task-oriented）

goal-oriented directions，引導**已具能力、已知目標**的使用者穿過問題抵達結果。邊界：assume competence，只放行動、不教學不解釋不離題；容許多個進出點與條件分支（if this, then that），實用勝過完整。標題精確說出展示什麼（`How to integrate X with Y`，非 `Application performance monitoring`）。從使用者**目的**出發，不描述工具怎麼動。

不可逆、高風險、生產環境的操作放這裡，附警告與前置檢查。設定檔正確性驗證（區段歸屬這類任務）完整到能反白貼上：

```ini
# foo.container — Quadlet 容器定義檔
[Container]
Image=quay.io/example/app:latest
PublishPort=8080:8080
HealthCmd=curl -f http://localhost:8080/health

[Service]
# 重啟策略屬於 systemd 的職責，不屬於 Quadlet 的 [Container] 鍵
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

---

## 相鄰混淆分辨測試（S4 用）

**tutorial vs how-to（最常見、最致命）** — 根本判準是使用者狀態 at study vs at work，不是內容複雜度：

| | tutorial | how-to |
|---|---|---|
| 使用者 | at study，尚未具能力的學徒 | at work，已具能力 |
| 目的 | acquire basic competence | perform a particular task correctly |
| 路徑 | 受控直線、消除意外、single line | 真實世界、fork and branch、if-then |
| 熟悉度 | explicit about basic things | assume familiarity |
| 安全性 | safe／reversible | 可能不可逆、高風險 |
| 責任 | 在老師／作者 | 在使用者 |

**reference vs explanation** — describe or discuss？中性乾事實、無意見、mirror 產品結構＝reference；discursive、表態、weigh alternatives、給 why＝explanation。

---

## 組裝順序模板

### 學習筆記模式（一頁筆記型）

四型區塊各自成節，區塊間不混；缺型留一行缺口註記。

```markdown
# <主題> — 一頁自學筆記

> **一句話：** <定義，講清楚它把什麼問題交給誰處理>
> *<範圍行：定義 · 運作 · 邊界 · 決策> — 更新至 YYYY-MM*

## Explanation ——————————
### 為什麼會有它？            ← 解決的問題（What/Why 錨點段）
### 它怎麼運作？              ← 功能定位 + 主要元件，配架構 Mermaid 圖
### 邊界 — 它管什麼、不管什麼   ← 職責邊界 + 五件套 recipe
### 什麼時候該用／不該用        ← 決策框架雙欄表
### 常見誤解與陷阱
### 附錄：學習鷹架（opt-in）    ← 費曼自述／待驗證清單，使用者要求才放

## Reference ——————————      ← 有素材才寫，否則：> 缺口：待整理參數表
## Tutorial ——————————       ← 有親手跑過才寫，否則：> 缺口：需實際部署後補
## How-to ——————————         ← 有具體任務素材才寫，否則標缺口

## 延伸參考 · 一段話總結 · 參考來源
```

### 正式文件模式

正文客觀陳述、不留第一人稱與未查證猜測、無 opt-in 附錄。四型仍各自成節、清楚分離。

```markdown
# <主題>技術說明

> 本文內容確認至 YYYY-MM。適用版本：<如有>

## 概觀與原理（Explanation）  ← What/Why + 五件套 + 心智模型 + 誤解
## 參數與結構（Reference）    ← describe-only，有素材才寫
## 上手（Tutorial）          ← 親手跑過才寫，否則標缺口
## 操作任務（How-to）        ← 具體任務素材才寫，否則標缺口
## 延伸參考 · 一段話總結 · 參考來源
```

### 混合模式

正文照正式模式寫；使用者要學習鷹架時，費曼檢核與待驗證清單收進 explanation 的「附錄：學習鷹架」，正本可直接刪附錄拿去給團隊看。

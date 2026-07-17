# 自學消化模組寫法

每個模組存在的理由是降低「讀完就忘」與「以為懂了其實沒懂」兩種學習失敗。寫模組時盯著這個目的，內容自然不會流於形式。

## 前置知識地圖

列出理解本主題前必須先懂的概念，每項附一句話說明「它跟本主題的關係」，而非只丟名詞。有先後依賴就標順序。

> 學 GPU Operator 之前要先懂：
> - **Kubernetes Operator pattern** — GPU Operator 就是一個 operator，不懂 operator 的 reconcile 迴圈就看不懂它為什麼能自動修復驅動狀態。
> - **DaemonSet** — 驅動與 device plugin 都以 DaemonSet 佈署到每個 GPU 節點，除錯時第一步就是看這些 DaemonSet。
> - **容器內核心模組載入的限制** — 這是整個 driver container 設計要繞過的根本問題。

判斷收錄門檻：讀者缺了這個概念會「完全看不懂」才收；只是「更好」的背景知識不收，地圖太長就失去導航功能。

## 心智模型與類比

給一個可以拿來推理的類比，而非只是修辭。好的類比能讓讀者預測系統行為；並且一定要標註類比在哪裡失效，否則讀者會把類比推過頭。

> Sidecar proxy 像每個服務配一個專屬總機：所有進出電話都先過總機，所以錄音（觀測）、擋騷擾電話（授權）、轉接（路由）都在總機做，服務本人只管講話內容。
> **類比失效處**：總機是人力成本，sidecar 是每個 pod 多吃的 CPU／記憶體，以及請求多經過一個代理節點所增加的轉發延遲；這個成本隨 pod 數線性成長，總機類比感受不到這件事，而它正是 ambient mesh 出現的原因。

## 常見誤解與陷阱

兩類都收：初學者自然會形成的錯誤直覺，與網路上流傳但已過時的說法。每條寫成「誤解 → 為什麼會這樣想 → 實際上」三拍，讓讀者先在自己身上認出那個錯誤直覺。過時說法註明從哪個版本起不成立。

> **誤解**：rootless Podman 容器內的 root 就是主機的 root，所以一樣危險。
> **為什麼會這樣想**：容器內 `whoami` 顯示 root，直覺上就是 root。
> **實際上**：rootless 模式下容器內的 UID 0 透過 user namespace 映射到主機上的一般使用者 subuid 區段，逃逸出來也只有一般使用者權限——這正是金融業環境選 rootless 的核心理由。

## 最小可運行範例

目標：讀者在目標環境十分鐘內跑起來、親眼看到核心行為。收錄三件事：前置條件、可複製貼上的最短步驟、以及「看到什麼才算成功」的判準。判準比步驟更重要，沒有判準的 lab 跑完也不知道自己驗證了什麼——每個指令後面用註解直接寫期望輸出，不要另外用一段文字描述「應該看到什麼」。

步驟要在預設技術脈絡（RHEL + rootless Podman、OpenShift）下可行；用到的指令與版本要查證過，不確定的旗標寧可不寫。格式範例（GPU Operator 驗證步驟，已查證）：

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

三個判準都直接寫在對應指令旁，讀者跑完立刻知道自己驗證到了什麼，不必回頭對照另一段文字。

另一種常見情境是驗證設定檔本身的語法或區段歸屬（例如「這個鍵該放哪個區段」這類常見誤解），這時範例要完整到能反白貼上就用，並讓對比一目了然：

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

## 費曼式自述檢核（opt-in）

預設不放。使用者說「幫我檢核理解」「加一段自己的話重述」等明確要求時才啟用。

寫作者用自己的話、不看資料，把核心概念重講一遍給想像中的同事聽。講完後標出兩種破綻：講到一半卡住的地方（概念沒接起來），與只能複誦原文措辭的地方（沒有內化）。每個破綻對應一個行動：回去重讀某段、或丟進待驗證清單。

這一節保留口語感、允許不精確——它的價值在暴露破綻，修飾過的自述測不出東西。

## 待驗證問題清單（opt-in）

預設不放。兩種情況啟用：使用者明確要求；或輸入素材裡有使用者自己標記的未解問題（如對話中說「這個還要確認」）——不收就會遺失，此時照收。

收所有懸而未決的問題。每題三欄：問題本身、為什麼在意（不寫這欄的問題常常其實不重要，可以刪）、怎麼驗證（具體到可執行：查哪份文件、做什麼實驗、問誰）。

> **問題**：ambient 模式下 L7 授權是否一定要經過 waypoint proxy？
> **為什麼在意**：影響我們的授權政策要寫在哪一層，以及 waypoint 是否成為新的容量瓶頸。
> **怎麼驗證**：讀 Istio ambient 官方文件的 waypoint 章節；在測試叢集開 L7 policy 不佈 waypoint，觀察是否生效。

清單是活的：下次學習 session 從這裡接續，驗證完的問題把答案寫回正文。

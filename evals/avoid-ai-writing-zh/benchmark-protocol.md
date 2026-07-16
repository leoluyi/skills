# Benchmark Protocol — avoid-ai-writing-zh 對抗式迭代流程

用 GAN 的原理找 skill 盲點與過度觸發的標準流程。每次想優化偵測規則
（或調整 gating）時跑一輪。與 blog-writing-zh 的「同題對照」互補：
那邊優化**加法**（怎麼寫出聲音），這邊優化**減法**（怎麼準確辨識 AI 味
而不誤傷真人）。

## 原理對照（GAN → 本 skill）

skill 是 prompt／規則集，不是權重，所以「訓練」= 規則精修迴圈，不是梯度下降。

| GAN 角色 | 本流程對應 |
|---|---|
| 真實分布（real） | 已知真人手寫的 zh-TW 文章語料（2022 前個人部落格／可考據作者，確定非 LLM 生成） |
| 生成器（generator） | 對抗者：產生想冒充真人的 AI 文；以及 skill 自己的 rewrite 產出（skill 本身就是把 AI 文人味化的生成器） |
| 判別器（discriminator） | skill 的 detect 模式 ＋ 一個 LLM-judge「這像 AI 還是真人？」分類 |
| 損失（loss） | 兩種失敗：真人文被標（false positive）、AI 文漏標或 rewrite 後仍被 judge 判 AI（false negative） |

## 流程

1. **建語料（兩桶）**：
   - **真人桶**：可考據為真人手寫的 zh-TW 文章（作者具名、2022 前發表尤佳）。
     每篇只取代表性段落，附出處 URL，**不整篇轉存**（版權）。
   - **AI 桶**：以主流模型生成同主題 zh-TW 文章（明確標記為機生）。
   - 兩桶主題盡量對齊，差異才收斂到「文風」而非「題材」。
2. **判別器跑分**：對兩桶各跑 skill 的 detect 模式，記錄——
   - 真人桶被標比例（**false positive rate**，越低越好）。
   - AI 桶被標比例（**recall**，越高越好）。
   - 逐條規則的觸發次數（哪條規則貢獻最多 FP／最多 recall）。
3. **生成器加壓（對抗）**：
   - 取 AI 桶，用 skill 的 rewrite 模式「清乾淨」，再丟給 LLM-judge。
     judge 仍判 AI 的殘留訊號 → skill 沒抓到的**盲點**。
   - 取真人桶被標的段落，逐條檢視 → 若該處是真人正常寫法 → **過度觸發**。
4. **兩種梯度 → 兩種 patch**：
   - 真人文被誤標（FP）→ 該規則過度觸發 → 加 **carve-out**（比照既有繁中 carve-outs）。
   - AI 文漏標或 rewrite 後仍像 AI（FN）→ **盲點** → 加**新規則**或補強既有規則。
5. **般化判斷**（沿用 blog-writing-zh 守則）：對每個 patch 問——
   - 這是**通用招**（可般化寫進規則）還是只吻合這一篇語料的**過擬合**？
   - 這條 carve-out 會不會反手放掉真正的 AI 味？（FP 與 recall 的取捨）
   - 每條 patch 附一條對應 eval assertion（prompts.json 或 output-quality.json）。
6. **收斂與紀錄**：連續兩輪無新的般化規則 → 該輪主題視為成熟。於下方 log 加一行。

## 判斷守則

- **signals, not proof**：真人文被標是一筆 false-positive 資料點，不是「這個真人是 AI」的證據。語料的真人身分以外部考據為準，不以 skill 判斷為準。
- **版權**：只引短段＋標 URL，不整篇轉存、不重新發布。語料清單記出處，不記全文。
- **過擬合警戒**：只吻合單篇語料的超specific 規則不收；一條規則要在多篇 AI 文上重現才進 SKILL.md。
- **FP 與 recall 取捨**：本 skill 的 ethos 是寧可漏標也別誤傷真人（見「signals, not proof」節）。同一個 patch 若把 recall 拉高卻讓 FP 明顯上升，傾向不收或改為只在 `--structure-signals` 下啟用。
- 存疑的 patch 先記 backlog，不當輪硬收。

## 執行方式（可選）

可手動跑，也可用 `ecc:gan-generator` / `ecc:gan-evaluator` agents 或 Workflow
harness 自動化 fan-out：generator 產 AI 桶、evaluator 跑判別器與 judge、
彙整 FP/recall 表。自動化只是省力，判斷與 patch 仍走上面的般化守則。

## 首輪待驗（gating 邊界）

第一個要用本協定回答的問題：**結構級訊號（zh-TW 部落格聲音）該擴大到哪些
非 blog 文體？** 目前只在 `casual` voice／`--structure-signals` 啟用。假設是
「voice-bearing 文體（觀點倡議 blunt、技術部落格 technical-blog、newsletter）
應啟用，voice-neutral 文體（docs、RFP、簽呈、公文、SOP）應維持排除」。
用真人桶量各文體的 false-positive rate：FP 可接受的文體才納入 auto-enable，
其餘維持 opt-in。**先有數據再放寬 gate，不憑感覺改。**

## Log

| 日期 | 真人桶 | AI 桶 | FP / recall | 主要發現 | Patch |
|---|---|---|---|---|---|
| — | （待跑） | | | | |

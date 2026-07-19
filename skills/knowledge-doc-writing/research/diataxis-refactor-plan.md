# knowledge-doc-writing → Diátaxis 四類產生器　refactor 計畫

狀態：計畫已擬、**尚未動手**。使用者選 Option A（整份改用 Diátaxis 架構，產出四類文件）。
依據蒸餾：`scratchpad/diataxis-distilled.md`（全站 prose 版；舊 caveman 版有瑕疵已作廢）。

## A. 這是產品轉向，不是換皮
現行 skill 產出**一份**知識文件（骨架＝What/Why＋辯證比較五件套＋消化模組）。
Option A 改成：依 compass 把素材路由進四種各自分離的文件類型。連帶「學習筆記 vs 正式文件」定位、五件套骨架都要重定位。

## B. 必先解決的張力（執行層，非重開選擇）
自學素材天生 **explanation 為重**（研究「X 是什麼、為何、跟替代方案比」）。Tutorial/How-to 需作者真的動手做過，自學主題常缺這種素材。
解法採 Diátaxis 自己的 workflow：
- 不搭空殼（don't build empty shells）——素材撐得起哪型就產哪型。
- 用 cycle-of-needs 檢查覆蓋度、**標記缺口**，不硬生四份。
- complete ≠ finished——每型先到「當下有用」，缺型標為待補。
→ 正確形態：compass 路由 → 撐得起的型寫足寫純 → 缺型明列缺口。

## C. 現有內容 → 四型對映
| 現有元件 | 歸型 | 處置 |
|---|---|---|
| What/Why 論述 | Explanation | 成主體 |
| 辯證比較五件套 | Explanation | explanation 內部 recipe（weigh alternatives＝explanation 核心） |
| 前置知識地圖 | Explanation 開頭 / Tutorial 前置 | 依落點分 |
| 心智模型與類比 | Explanation | 併入 |
| 常見誤解與陷阱 | Explanation / Reference caveat | 依內容分 |
| 最小可運行範例 MRE | Tutorial 或 How-to | 依 at-study/at-work 拆 |
| ADR 情境模組 | Explanation | 決策理由屬 explanation |
| 分層結構 | Reference（mirror 產品結構） | 移入 |
| 待驗證清單、as-of、時效 | 功能性品質關切 | 進完稿檢查，不進成品散文 |
發現：現行 skill 幾乎全在 explanation 象限；tutorial/how-to/reference 產生規則**近乎空白**＝refactor 最大新增塊。

## D. 新 SKILL.md 骨幹（Diátaxis 為主軸，取代自創命名，內容保留重新歸位）
1. 開工前：compass 路由素材（action/cognition × acquisition/application），定主題撐得起哪幾型。
2. 四型各一節產生規則（各自 need、邊界、語言、標題規範）。
3. 維持分離：相鄰混淆（tutorial↔how-to、reference↔explanation）自審 + 跨型連結互指。
4. 組織產物：complex-hierarchies（≤七項、landing overview 散文、第二維度處理）。
5. 來源可靠性 → 重掛 functional quality（accuracy/completeness/currency）；deep quality conditional upon 它。
6. 完稿檢查 → 兩層品質模型 + cycle-of-needs 覆蓋度缺口檢查。
7. 工作模式 → 迭代/有機生長，complete≠finished。
8. 保留：learn 銜接、白話語言原則、HTML 版規則（與型無關照留）。

## E. description 重寫
現行 13 行（本身 sprawl）。改寫成「產出四種分離的 Diátaxis 文件類型」+ 瘦身 + 放進四個 Diátaxis leading word 強化觸發。

## F. 風險
1. **Eval 必須重做並重新 baseline**：v1.3.1 evals 為單一文件產品寫，產品轉向後 trigger-queries 與判準都要重寫＝建新基準而非贏過舊基準。repo 硬規需先講好怎麼處理。
2. **版本**：breaking change → **v2.0.0**。

## 已鎖定決策（2026-07-19）
1. **非結構要求**：13 條全部照留（人味非AI味、白話優先、術語英文、來源時效、空降主張防呆、論述非條列[歸位 explanation]、預設技術脈絡金融/K8s/OpenShift/Podman/Quadlet、HTML inline SVG 固定模板、Mermaid、learn 銜接鐵律、範例不豁免、一句話開頭+一段話總結、opt-in 模組見下）。
2. **產出形態**：**一份文件、四個分離區塊**（tutorial/how-to/reference/explanation 四個清楚分離的章節，區塊間不混）；**每份文件可選需要哪些區塊**——素材撐得起才寫，缺型標缺口，不搭空殼（呼應 §B）。
3. **opt-in 模組**（費曼自述／待驗證清單）：**收進 explanation 區塊的附錄，維持 opt-in**（費曼＝reflection after practice 屬 explanation；待驗證＝工作紀錄，預設不放）。
4. **Eval 策略**：**先把「四類產出該怎麼考」設計成規格**（trigger 與判準）當 spec，再寫 SKILL（TDD 味）。產品轉向後 v1.3.1 舊基準不適用，等於建新基準。

## Eval spec：已定案（2026-07-19）
已寫入 `evals/evals.json`（8 positive cases，每 case 標 `baseline`）與 `evals/trigger-queries.json`（7 positive + 10 negative，含兩條 leading-word 防呆）。兩個 eval 決策：
- **分區 baseline**：preserved 行為（learn handoff #5、HTML #6、Mode D point-patch #7）baseline=v1.3.1 不得回歸；pivoted/new 四型行為 baseline=vanilla 須贏過。
- **Mode D 依意圖分流**：更新時效/併入→point-patch 保原形；重整/重構→依 compass 路由進四型區塊。
判準與 provenance 詳見 `DEVELOPMENT.md` 的「Eval spec」段。

## 下一步：改寫 SKILL.md → v2.0.0
依 §D 骨幹實作（compass 路由 → 四型各自產生規則與邊界 → 維持分離 → complex-hierarchies 組織 → functional/deep 兩層品質 gate → 迭代 workflow），保留 §決策 1 的 13 條非結構要求、opt-in 模組進 explanation 附錄、重寫 description（四個 Diátaxis leading word + 瘦身）。改完跑 evals 對照 baseline。

## 相關檔案
- 蒸餾：`scratchpad/diataxis-distilled.md`
- 目標 skill：`/Users/leoluyi/.claude/skills/knowledge-doc-writing/SKILL.md`（symlink→ repo `skills/knowledge-doc-writing/`），現版 v1.3.1
- repo 硬規：`/Users/leoluyi/.skills/CLAUDE.md`（改版須贏 baseline、runtime 檔案不留 provenance、跨 AI 可攜）

# Worked example: 說明提綱 for a talent-training program

Context: 7 source docs (~2,240 lines) — a 設立計畫 (umbrella) plus 招募計劃書、訓練計劃書、技術筆試題目、技術面試題目、高階主管面試題目、專案實作規劃 (detail) — distilled into one ~230-line 提綱 for a 委員會 deciding whether to fund the program. Each move below is tagged with the rule from `SKILL.md` it demonstrates.

## Spine — MECE lifecycle
Eight sections in the candidate lifecycle: 招募 → 筆試 → 面試 → 高階面試 → 訓練 → 專案 → 委員會 → 師資. The first six are the timeline; 委員會 and 師資 tail as enabling structure. Each source's essence lives in exactly one section (MECE), and one transition line marks the bend into the assessment phase: 「本節起之筆試與面試為招募階段之評估，於入訓前辦理」.

## Graduated altitude — one doc, two depths
- A 情境題 in 技術筆試題目 runs ~110 lines (情境說明 + 監控數據 + `kubectl` dump + 6-line Log + 35-line YAML + 5 sub-questions + 評分標準表) → **one** 提綱 line:
  > 情境一：文件服務由 1.2.0 升版到 1.3.0 後間歇性失敗。依 Log、YAML、監控判斷根因（權限、資源、版本設定差異），並決定是否回復版本。

  Rule — **earns**: a routine, self-describing instance collapses to a label + gloss, and the gloss (權限、資源、版本設定差異) encodes the *discriminating point* (the answer key), not the question.
- The 40-分鐘現場實作測驗 in 技術面試題目 also runs ~170 lines — but keeps **two paragraphs**. Rule — **earns**: it is *non-obvious* (the format can't be reconstructed from its name), *self-arguing* (「重點不在語法正確，而在能否判斷風險」), and *decision-bearing* (公平性、AI 輔助工具使用規則 the 委員會 must approve).

## Container vs payload
筆試 keeps 90 分鐘、選擇 20／問答 3／AI 應用 2／情境 2 題 (dimensions) and one 篩選構念 per type; it drops every question, option, answer key, and 配分 (payload). Rule — **keep the container's dimensions, drop the payload.**

## Keep the schema, drop the rows
招募's 7-row 人才規格條件表 (程式／Linux／網路／資料庫／Docker／… × 條件 × 篩選定位) → one sentence keeping only the classification axis:
> 入場門檻：會寫程式…摸過 Linux…；資料庫、Docker、文件紀錄為入訓後補強的觀察項目。

門檻 vs 觀察 survives; the cells go down.

## Purpose-first + plain-speak lowering
- Source (noun-list objective): 「本課程目標為建立學員對 Linux、網路、Git、containerd… 之基礎能力」
- 提綱 (verb outcome): 「教完學員能做到：把一個服務打包成容器、部署上 Kubernetes、對外提供服務，並管理它的設定、憑證與資源」

Rule — spec-voice → stakeholder-voice; the sentence passes `plain-speak`'s repeat-test.

## Synthesis the sources only imply
- **Computed total**: sources give per-module hours only; the 提綱 states 288 小時 = 授課 192 + 實作 96 — arithmetic the reader would otherwise do.
- **Named structure**: 「授課分三類，對應平台工作的三種能力」 — a frame no single source states.
- **Caution, live**: sources formally list **4** 授課模組; the 提綱 regroups into **3** categories (merging 算力＋模型 under one hour total). Done consciously — but a reader cross-checking sees 4 vs 3. This is the "recut structure risks a visible mismatch" caution in the wild.

## Flat over nested
Multi-item essence is rendered as flat, labeled bullet clusters (來源一／來源二; per-course 「教完學員能做到：」 + bullets) — never nested 槽狀 paragraphs. A source change edits one bullet instead of unpicking a clause.

## Two defects this example also shows (learn from them)
- **Cross-reference asymmetry**: the two heaviest sections (招募、訓練) point to *no* source, while lighter assessment sections each carry 「（詳《…》）」. Coverage should track detail density.
- **Untraceable load-bearing numbers**: the market-supply figures (1.96 萬、6.3 萬、2.6–4.1 萬) open the doc with no source anchor — a liability in a decision document.

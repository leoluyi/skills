# Skills backlog — repo 層

Repo-wide and `tools/` work. A single skill's own items live in `skills/<name>/backlog.md`.

Signal: friction hit 2+ times. Closed items do not stay here — provenance lives in commit
messages, each skill's `design-notes.md`, and `evals/results-*.md`.

## Next round — humanizer-zh 的量測儀器，一條線

剩下的 open items 幾乎都掛在 humanizer-zh 的同一次 re-baseline 底下。它們不是可以任選順序的清單：
每一項都動 `evals.json` 的 key，而動 key 就要求**兩個版本一起重跑基線**，aggregate gate 的 rounds
也得從頭再跑一次。分開做等於重跑數次 aggregate。順序如下，一次做完再一起重跑：

1. **`tools/annotate`** — 判讀輔助工具（下方）。落地 2026-08-01；第 2 步靠它省下逐案手抄的成本。
2. **ported-case sweep** — 從 id 33 續走
   ([`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md))。
3. **衝突複審** — 收工 2026-08-01，13 案全judged。結果與預期相反：最大宗是 `case-wrong`（6 案）
   而非 `key-wrong`（3 案）——**近半數的「衝突」不是判讀與 key 的分歧，是量測方式本身有問題**。
4. **`evals.json` 的結構缺陷** — 大半收工 2026-08-01。量測方式四項中三項落地在儀器設定
   （`ai_index_not_applicable`、`verdict_class.no_touch`，不動 key）；4c 三項與 id 27 的
   rekey（＋新 id 58）落地在 `evals.json`。仍開放的兩件：**合成保護語料替換**（47、43 皆已換成
   真語料，另加 ids 59～63 五案，涵蓋社群、電子報與上市公司年報三種體裁；只剩 id 52 卡在需要
   同型材料——真人寫的條件式工具建議）與 **`體裁相稱`**（第三例 id 51 已找到、
   煞車已過，走自己的 branch，53/54 的 key 改動跟著它走）。
5. **`口語化萬能詞` 兩側覆蓋** — 收工 2026-08-02。命中側進 id 7 自己的 key，保護側 ids 76、77。
6. **rewrite mode 的口語時間表達 保真 case** — 收工 2026-08-02，id 78。
7. **一次 re-baseline ＋ aggregate 重跑** — 前六項的結果一起進去，不分批。待進去的東西比原
   計畫多：`破碎短句堆疊` 命中側三案（ids 79-81）、條列 carve-out 保護案 id 82、`缺連接詞`
   分界案 id 85 與 casual 語域的三形態案 id 86、`對讀者說教` 與 `對比句式` 的第一個
   rewrite 案（ids 83、84）、`缺連接詞`
   保留欄的收窄（動 `references/zh-rules.md`，屬行為變更），以及 chunks 與 `rewrite_case_ids`
   的重排。全部在 branch `chore/backlog-key-sequence` 上，2026-08-02 起跑第一輪。

2026-08-02 那一輪同時關掉兩件不在原順序裡的事，因為它們擋在這條線前面：
`check-labels` 連紅的閘（見 humanizer-zh backlog 第 8 項——閘壞著時新增 case 的 label 打錯不會
被抓到），以及 ids 72-75 從來不在任何 chunk 裡這個機械缺陷（`自我背書` 四案齊備卻一輪未跑的
真正原因）。同輪的完整分類、每一項的處置與待裁決選項在
[`backlog-triage-2026-08-02.md`](backlog-triage-2026-08-02.md)。

**那一輪撞出的矛盾已裁決（2026-08-02）**：`缺連接詞` 的保護側無處可站——`zh-rules.md` 的保留欄
說中文意合不必補連接詞，而 `zh-phrase-rules.md` 的定型表給了 條件／因果／轉折／時序／目的 五列
該抓的例子，覆蓋的正是意合最常出現的全部關係型別。裁定**收窄保留欄、不動定型表**：五列是工作
範例、它們正確，錯的是保留欄把抓欄已有的回讀測試復述得太鬆。落地為 `zh-rules.md` 保留欄第一
分句的改寫與 `evals.json` id 85，推導記在 humanizer-zh 的 `design-notes.md`。

**這條線 2026-08-03 收工並併入 main。** 十輪兩臂量測收斂在 `缺連接詞` 抓欄措辭的第三版（列舉自帶
前提條件），兩臂均值新版全面優於基線。同日接一輪 carve-out 可達性修正：D1 那十輪反覆撞出的九列
兩臂同紅缺口，八列在這一輪處理掉（`知識截止免責` 收窄 抓，其餘七條放寬 保留），加上 `SKILL.md`
的 casual context 點名放行 `破碎短句堆疊`。九列缺口全清，但第一批三輪開出三列新臂獨有的紅，病因
是 D1 那條教訓的重演——carve-out 裡的列舉被讀成窮盡；補上前提句之後第二批三輪全數翻綠，保護 mean
5.00 對基線 16.33、命中 10.00 對 13.00。收工時 47 與 86 仍兩臂同紅：86 的 casual 例外補錯了軸
（eval 宣告的是 Voice: casual，例外寫在 Context 那行），47 則三處 carve-out 都沒構到。兩件都是
main 自己也有的既有缺口，各自留在 humanizer-zh 的 backlog，推導記在它的 `design-notes.md`。

跑完這條線之後才輪到行為變更，每個各自 branch、各自重跑：`模糊歸屬` 的 isolated-instance 判斷、
detect 預設、進階補完模式（順序固定，進階補完要等 detect 預設先落地）。細節都在
[`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md)。

`corpus.md` 飽和與英文側證據不獨立這兩件事不在上面，因為它們不是待辦——它們是讀任何一份
`results-*.md` 的前提，已寫進 [`skills/humanizer-zh/evals/regression-protocol.md`](skills/humanizer-zh/evals/regression-protocol.md)。

## Measurement infrastructure

`tools/run-eval` exercises `trigger-queries.json` (whether the router fires);
`tools/run-case` scores the behaviour layer against `evals.json`. A skill opts into the
latter by shipping `evals/run-case.json`.

`corpus.md` is still hand-run — `run-case` reads `evals.json` only, and the corpus's
judgment-table format is a different parse. Whether that is worth automating depends on
whether the corpus stays a regression guard (see the saturation item in
[`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md)); a saturated fixture
does not earn a harness.

**`tools/add-case` 排在 `annotate` 後面，先不列為待辦。** 它要做的事——用固定格式把一則已判讀的
case 追加進去，免去手改 JSON——與 `annotate` 的寫入端重疊：`annotate` 本來就要把 有/沒有 的判讀
結果寫進 `evals/judged-cases.md`。先蓋一個獨立工具，很可能蓋出一段之後要刪的重複程式。

順序因此固定：`annotate` 先落地，用一輪真實的 sweep 之後再看「追加 case」這件事還缺什麼。真的
還缺，那時的需求會是具體的，而不是現在這個從對稱性推出來的猜測。這一項留在 repo 層而不是掛在
humanizer-zh 底下：`evals/judged-cases.md` 在 `infographic-design` 也有一份，追加格式不屬於單一
skill。

**Open: chunk 6→3 省 token，但把每輪 wall-clock 拉更長，是否過度工程要再議。**
`fix/gate-null-calibrated` 的 3-round ship-check 實測：round 1 全程 ~2 小時（12:40AM 起，
02:46AM 三個 chunk 全部落地），round 2 單一 chunk（c1）就跑了近 4 小時才收（02:46 起、
06:35 c1 runner 完工），且最後在 grader-c1 上 `claude exited 1` 失敗——與 `--null-run` 15 配對
裡同一個失敗簽章（11/15 次、詳見下方「已解」項）撞了同一顆雷。

根因：chunk 合併把「多顆小 call 平行跑」換成「少顆大 call 各自序列推理」——`dispatch.py`
的 `ThreadPoolExecutor` 只平行化 chunk 之間，單一 chunk 內部（19/32/34 案一次性塞給
runner，reasoning effort `high`）仍是一條龍序列生成，round 的 wall-clock 下限因此被最大的
單一 chunk（34 案）卡死，而不是被總案例數卡死。省的是 token（少送 11 次規則 blob），付的是
latency（大 chunk 生成時間不可切）——`reflective-rolling-crescent.md` 的風險備忘已經預見
「34 案的大 chunk：grader 單 call ~95 列，row-matching 失敗率上升」，這次是實測到了，不是
臆測。

沒有立即動作：本輪的 token 省法已拍板，且尚未證明 6-chunk／xhigh 舊設定的 wall-clock 更短
（舊設定單 chunk 案例少但 effort 更高，兩個變因同時換，沒有對照組）。留給下一次要動
`run-case.json` 或 `dispatch.py` 併發模型的人：chunk 大小是 token 與 latency 的直接取捨，
不是無成本的省錢招——調整前先量兩者，不要只看 token 帳。

## Per-skill backlogs

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — **the next round**, in the
  order above, plus `tools/annotate` — shipped for adjudication, still open as the blind
  人機判定 harness
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice
  profile (獨立於主線之外，需要自己的 eval bar)
- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) 以外，其餘 skill 皆無 open
  items：`avoid-china-writing`、`infographic-design`、`knowledge-doc-writing`、`plain-speak`。
## 閘重建完成 — 2026-08-04

`regression-protocol.md:50-52` 兩道均值護欄拿的是點估計比大小，而點估計的不確定度比護欄
動作的門檻大 4 到 8 倍；以命中類 sd≈4 估，80% 檢定力下偵測 1 列差異需約 125 輪。
`fix/gate-null-calibrated` 換掉的不只是那兩道護欄，還有它們背後「用變異模型推門檻」的做法。

換統計量救不了它：**每輪平均差乘輪數恰好等於逐格淨退步數**，兩者是同一個量，差別只在把
~50 個配對格先壓成 3 到 6 個輪總數。門檻改成從空實驗數出來——共用同一份 baseline 的
21 輪歸檔切半自我對打，正確答案已知是「沒有差異」，報出來的每一列退步都是假警報。

三項改動與各自的證據：

| 改動 | 舊行為在空實驗下的表現 |
|---|---|
| 只算新臂獨有的退步，既有缺口分開印 | 舊閘給 detect 那輪的八列 confirmed 裡七列是 main 本來就紅 |
| `CONFIRM_AT` 固定 2 改成過半數 | 固定 2 的假警報 p95 從三輪 3 列長到八輪 11 列——輪數越多閘越鬆 |
| 均值護欄換成 `row_margin`（淨退步列 − 淨改善列） | 均值護欄比較一份文字與它自己時觸發 47% |

重建後的檢定力（刻意打壞 k 列保護，看擋下比例）：2 列穩定壞在六輪 100%、廣泛淺層 12 列
78%、什麼都沒壞 5%。三輪只能放行不能擋人（三輪空實驗自己就產最多 3 列 confirmed），
NO-SHIP 需要六輪。

還沒關掉的兩件事：

- **校準偏鬆。** 空實驗跨輪配對，真實比較是兩臂在同一次 grader call 內同時判、共用那次
  抽樣。空實驗因此比它校準的對象更吵，門檻偏鬆，偏誤方向是漏擋。收緊需要一輪兩臂載入
  同一份文字的量測（`--baseline HEAD`），18 jobs。
- **`calibration.json` 的 criteria 已過期。** 這次把聚合政策從 `## 判分標準` 搬出去
  （原本它被餵給 grader，等於告訴判分端分數會怎麼被用），`criteria_sha256` 因此改變。
  現有表描述的是舊 rubric 的設定；新 rubric 下累積六輪後要 `--calibrate` 重跑。
  aggregate 報表會自己標記這個過期狀態。

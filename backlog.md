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
5. **`口語化萬能詞` 兩側覆蓋** — 名詞與短語 form 的 hit case 與 protection case。
6. **rewrite mode 的口語時間表達 保真 case** — 目前沒有任何一案測它。
7. **一次 re-baseline ＋ aggregate 重跑** — 前六項的結果一起進去，不分批。

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

## Per-skill backlogs

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — **the next round**, in the
  order above, plus `tools/annotate` — shipped for adjudication, still open as the blind
  人機判定 harness
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice
  profile (獨立於主線之外，需要自己的 eval bar)
- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) 以外，其餘 skill 皆無 open
  items：`avoid-china-writing`、`infographic-design`、`knowledge-doc-writing`、`plain-speak`。

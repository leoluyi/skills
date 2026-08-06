# Skills backlog — repo 層

Repo-wide and `tools/` work. A single skill's own items live in `skills/<name>/backlog.md`.

Signal: friction hit 2+ times. Closed items do not stay here — provenance lives in commit
messages, each skill's `design-notes.md`, and `evals/results-*.md`.

## humanizer-zh 的量測儀器

那條「一次做完再一起 re-baseline」的儀器線 **2026-08-03 收工並併入 main**：判讀工具、
ported-case sweep、衝突複審、`evals.json` 的結構修補、三條規則的兩側覆蓋、`缺連接詞` 保留欄的
收窄，全部落地。過程與每一項的推導記在
[`skills/humanizer-zh/design-notes.md`](skills/humanizer-zh/design-notes.md)；同輪的完整分類
在 [`backlog-triage-2026-08-02.md`](backlog-triage-2026-08-02.md)。

仍開著的儀器項（合成保護語料只剩 id 52、`語體漂移` 缺非母語寫作保護案、`自我背書` 未量測）
與所有行為變更（`模糊歸屬` 的 isolated-instance 判斷、detect 預設、進階補完模式——順序固定，
進階補完要等 detect 預設先落地）都在
[`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md)。**那些仍開的儀器項一樣動
key，所以仍然一批走。**

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

- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) — the remaining instrument
  items (they batch, see above), the behaviour changes, and `tools/annotate` — shipped for
  adjudication, still open as the blind 人機判定 harness
- [`skills/blog-writing-zh/backlog.md`](skills/blog-writing-zh/backlog.md) — source-derived voice
  profile (獨立於主線之外，需要自己的 eval bar)
- [`skills/humanizer-zh/backlog.md`](skills/humanizer-zh/backlog.md) 以外，其餘 skill 皆無 open
  items：`avoid-china-writing`、`infographic-design`、`knowledge-doc-writing`、`plain-speak`。

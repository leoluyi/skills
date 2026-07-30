# Design notes — discuss-with-me

本檔記錄開發過程、設計理由與 provenance。runtime 檔案（`SKILL.md`、`references/`）
不放這些內容。

## 起源

從一段對話演化出來的。使用者原本問「在 Claude Code 裡想跟 AI 討論一個問題、最後
產出文件修改，該用哪個 popular skill」，逐輪把需求收斂成三段：

1. 一開始像是 doc-coauthoring 的場景（使用者腦中有東西，AI 幫忙挖出來、寫成文件）。
2. 使用者澄清「文件不是重點，重點是討論的過程」，排除了純寫作 skill。
3. 使用者再追問「如果這個問題我跟 AI 都不一定有正確答案呢」——這一問把場景推到既有
   skill 的空白處：`doc-coauthoring` 假設使用者有答案，`learn-loop` 假設模型有答案，
   兩者都不涵蓋「雙方都沒有」。

本 skill 就是補這一格。三種場景的分工線寫進 description 與 §When this applies，
因為誤路由到另外兩格是這個 skill 最可能的失效方式。

## 借用的設計來源

沒有逐字引用，借的是結構。兩個來源的 LICENSE 已於 2026-07-28 從上游 repo 實際讀取確認，
皆為 MIT（obra/superpowers: Copyright (c) 2025 Jesse Vincent；phuryn/pm-skills:
Copyright (c) 2026 Pawel Huryn）。因未重製任何實質篇幅，MIT 的姓名標示條件並未觸發，
NOTICE 屬自願標示，故本 skill 不附 per-skill LICENSE 檔（對照 avoid-ai-writing-zh 有附，
是因為它確實近乎逐字引入了上游內容）。Anthropic 的 doc-coauthoring 取用的副本未附授權檔，
條款未確認，已在 NOTICE 據實標明。

- **obra/superpowers `brainstorming`**（https://github.com/obra/superpowers）——
  Widen 這一步的形狀：一次問一個問題、能用選擇題就用選擇題、提出多個方案連同取捨、
  在設計被批准前不進入實作。本 skill 拿掉了它的終點（`writing-plans`）與 hard gate，
  因為那條流程假設「存在一個可以收斂的設計」，會把不確定推向決定，方向與本 skill 相反。
- **phuryn/pm-skills `strategy-red-team`**（https://github.com/phuryn/pm-skills）——
  Attack 這一步的四欄結構（fails-if／cheapest evidence／kill criterion／who would
  know）、依「錯了多痛 × 驗證多貴」排序、以及「不製造懷疑也不蓋橡皮圖章」這條自我防呆。
  Pre-mortem 作為攻擊落空時的反轉手法也來自同一個 plugin 的鄰居命令。

Anthropic 的 `doc-coauthoring` example skill 提供了 Stage 1（context gathering →
釐清問題）與 Stage 3（fresh-context reader testing）的骨幹概念，本 skill 把 Stage 3
從「文件可讀性測試」改寫成「結論的獨立驗證」——因為在雙方都不確定時，沒被對話錨定過的
判斷是唯一能對抗 premature consensus 的機制。

## 設計決策

- **model-invoked，但入口很輕。** 依 `.agents/invocation.md` 的判準（模型能不能自主
  地有用地伸手拿這個 skill），答案是能——使用者說「陪我想一下」時模型應該自己認出來。
  但這是會佔用整段對話的流程，所以 §Entry 規定先用幾行確認題型與範圍，而不是直接展開
  四步迴圈。這是 `learn-loop` 走 user-invoked 的相反解法：那個 skill 綁 vault 路徑與
  個人流程，本 skill 沒有外部狀態，誤觸的成本只有幾行字。
- **provenance 三分類（found／inferred／guessed）就地標註，不做事後稽核。** 早期
  草稿是在 Ground 之後跑一次「來源檢查」，問題是流暢的段落一旦成形，事後很難把三類
  拆回來——標註必須跟生成同步發生才有效。
- **保護類優先於命中類。** 這個 skill 的兩個真實傷害是「對已經有證據支撐的計畫捏造
  風險」與「對已經收斂的問題硬跑迴圈」，都不會在只檢查「該觸發時有沒有觸發」的
  eval 裡現形。所以 evals 案例 3、4 是保護類、零容忍，寫進 regression-protocol 的
  ship gate。
- **兩種成功結局。** 「化約為一個具名實驗」與「問題收斂」並列為成功出口。少了前者，
  模型會在證據已經是瓶頸的地方繼續產出推論文字——這是本題型最常見的空轉。
- **紀錄格式不是 ADR。** ADR 論證一個結論；本 skill 的紀錄要同時攜帶自己的
  falsification（承重假設表、反方最強論證、已排除選項的重啟條件）。刻意不叫 ADR，
  避免模型套用「決策已定」的語氣。

## 待辦

- 還沒跑 pre-ship dual run（新 skill 的 baseline 是 vanilla），交付時只做了結構與
  整合腳本的驗證。合併前需依 `evals/regression-protocol.md` 補跑，並把結果存成
  `evals/results-<date>.md`。
- `docs/catalog.yml` 的 `knowledge-mgmt` 分類 blurb 目前只描述 learn-loop 與
  obsidian-vault 的組合（先教後考 → 歸檔 Obsidian），本 skill 加入後該 blurb 略窄，
  可考慮改寫，但那會動到 README 既有區塊，留給使用者決定。

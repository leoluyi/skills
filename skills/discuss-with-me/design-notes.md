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
NOTICE 屬自願標示，故本 skill 不附 per-skill LICENSE 檔。（這裡原本拿 avoid-ai-writing-zh
當對照——它附了上游 LICENSE，因為確實近乎逐字引入了上游內容；該技能 2.0.0 移除那層逐字沿用
的英文內容後，LICENSE 檔也一併刪掉了，這個對照已不成立。）Anthropic 的 doc-coauthoring
取用的副本未附授權檔，條款未確認，已在 NOTICE 據實標明。

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
- **bare 呼叫是一個 branch，不是一個捷徑（0.2.0）。** 使用者對話中途只打 skill 名稱、
  後面不帶問題時，題目要由模型從自己上一輪回答裡推導。兩個設計選擇：推導的搜尋樣式
  寫成「上一輪沒有論證過的東西」（倚賴的前提、沒比較就選定的方向、沒有來源的數字），
  比「針對上一輪主題」具體得多，後者會讓模型抓錯層級、去討論使用者已經同意的部分；
  以及 **the blocked move**——使用者本來要做而停下的那一步。後者是這個 branch 的深度
  上界與出口條件，同一個詞在 §Entry 與 §Exits 各出現一次，靠分佈式定義省掉解釋。
  沒有它，bare 呼叫只是省下打字，討論可以無止盡漂下去。
  `description` 刻意不加觸發詞：bare 呼叫是手打的，模型永不需要自主偵測，加了是每輪
  都付 context load 換零收益；`trigger-queries.json` 同理不加案。措辭不綁 slash command
  的參數機制，寫「呼叫時後面沒有帶問題」，以符合 repo 的 portability 硬規則。

## 迭代紀錄

| 日期 | 版本 | baseline | 結果 | 存檔 |
|---|---|---|---|---|
| 2026-07-30 | 0.2.0 | 0.1.0（`9ddf49a`） | 整體 54/68 vs 53/68（雜訊內）；案例 7 中性重跑 5/5 vs 3/5，兩輪一致，差的正好是 `names-blocked-move` 與 `stopping-condition-tied-to-move`。ship gate 紅燈，卡在案例 3、8，兩者 baseline 同樣紅 | [`evals/results-2026-07-30.md`](evals/results-2026-07-30.md) |

## 待辦

- **ship gate 未過，合併前要處理三件事**（詳見 `evals/results-2026-07-30.md` 的
  Dispositions）：案例 3 的 `proportionate-length` 與 SKILL.md 的 Precipitate 步驟
  互相矛盾，四個 run 全失，要決定拿掉 expectation 還是給 Precipitate 一個比例原則的
  例外；案例 5 的 `delivers-under-deadline` 撞上 §Entry 的先確認範圍，這是 skill 內部
  真的沒講清楚的衝突，要決定截止期限下哪一條優先；案例 8 的 stimulus 沒有實作它自己的
  意圖（那段 prior turn 真的留了一個沒論證的方向選擇），要改寫 stimulus 再重跑一次才
  能算過——這個案子是跟被它把關的改動同一批寫的，不重跑就不記過。
- 案例 8 另外暴露一個兩版共有的真實缺口：bare 呼叫遇到大致收斂的上一輪時，交還得不夠
  便宜（16–25 行）。不是回歸，是下一輪要修的東西。
- 案例 6 的 `still-attempts-now` 四個 run 有三個失分，模型描述「我會怎麼查」而不是當場
  查。Attack 步驟的完成條件太鬆，是最明顯的下一個收緊點。
- `docs/catalog.yml` 的 `knowledge-mgmt` 分類 blurb 目前只描述 learn-loop 與
  obsidian-vault 的組合（先教後考 → 歸檔 Obsidian），本 skill 加入後該 blurb 略窄，
  可考慮改寫，但那會動到 README 既有區塊，留給使用者決定。

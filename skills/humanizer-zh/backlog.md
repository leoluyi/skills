# humanizer-zh backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md) — except
`tools/annotate` below, which only this skill's material calls for.

Closed items do not stay here — see `design-notes.md`, `evals/results-*.md`, and commits.

## Open: the protection class is noisy at the row level

2.1.0 shipped on the aggregate gate (`evals/results-2026-08-01-run-case-aggregate.md`): zero
confirmed protection false kills over three rounds, both class means well clear of 1.5.0. What
the rounds also showed is worth keeping in view — across ten rounds on two skill states, the
new arm's protection failures landed on **eight different rows** and no row failed
consistently. Two rows are one round short of confirmation as of 2026-08-01:

- **id 9 `全域:保真`** — the arm turned 「資安設定沿用既有範本即可」 into a bracketed gap
  request, deleting a real fact. The 空洞就標出來 habit reaching a sentence that is not hollow.
- **id 28 `no-single-instance-false-positive`** — a lone 解說導引腔 guide phrase flagged
  despite the density carve-out, usually by a neighbouring rule collecting the same span.

Neither is a defect on the record yet, and patching what a single round happens to red is how
the hit class gets eaten by carve-outs. The thing to watch is whether either crosses 2-of-N in
a later aggregate.

## 下一輪，照這個順序做

The instrument is not a clean bar either, and everything in this section changes the key —
which forces a re-baseline of **both** versions and a from-scratch re-run of the aggregate
gate's rounds. That cost is paid once per round, not once per item, so these four land
together and re-baseline once at the end. Within the round, do them one at a time rather
than interleaving; **step 1 exists to make step 2 affordable.**

### 1. `tools/annotate` — 判讀輔助工具

- [x] **`tools/annotate` — yes/no adjudication helper for eval cases.** Wanted 2026-07-30,
  straight out of the session that found it. When a run disagrees with the key, the fastest
  way to settle it turned out not to be reading rule text — it was showing the author the raw
  sentence and asking 「這句有沒有 AI 味？」 with two buttons. Four such questions overturned
  three cases in one round, where two rounds of rule-wording argument had settled nothing.
  The tool should: pull a case's quoted span out of `evals.json`, present span + genre + one
  line of context (never the expectation, never the rule name — those bias the answer), take
  有/沒有, and write the verdict plus a one-line rationale into `evals/judged-cases.md` as
  品味層 語料, flagging any case whose verdict now contradicts its `expected-direction`. Runs
  over a filtered set (a whole id range, or only cases that failed a given run). Dev-side,
  `uv` fine, never part of skill runtime. The immediate consumer is step 2: resuming that
  sweep by hand is the same transcription tax a second time.

  落地 2026-08-01。實際行為與上面這段原始描述有兩處差異，先記在這裡：

  - **判讀先進帳本，`judged-cases.md` 由帳本渲染。** `evals/annotations.json` 是機器可讀的
    真相來源，`judged-cases.md` 末端一個 `annotate:begin/end` 圍起來的區段從它渲染而來，
    marker 外一個 byte 不動。續跑狀態只讀帳本——散文檔沒有機器可讀的 case id，任何解析器
    都會在有人重排標題的那天開始靜默漏案。
  - **判讀是 1-4 的 AI 指數，不是 有/沒有。** 原描述寫的是兩個按鈕；實際第一次判讀時作者
    自己就伸手要了一個程度（「AI指數70%: 過分空虛的形容詞…但不排除人也會這樣寫」），二元裝
    不下那句話。四個固定錨點（1 偏人／2 不確定／3 偏 AI／4 明確 AI）隨每張卡一起印——
    36 案會跨 session 判，沒有錨點的量表在第一次與第五次之間會漂移，漂移過的分數無法跨案
    比較，而那正是量表相對二元的唯一收益。**錨點刻意不對稱**：人側一級、AI 側兩級。這支
    儀器問的是 AI 味有多強，所以解析度值得花在 AI 端——「明確人寫」與「偏人」對任何下游讀者
    都是同一件事（這不是 AI），而「偏 AI」與「明確 AI」分開的是規則該抓與必須抓。
    **2「不確定」不算與 key 一致**：它回傳 `null` 而非 `false`，因為不選邊不是同意；
    記成同意會讓一堆真正判不出來的案讀起來像答案卡的健康證明。
  - **比對的是類別，不是 `expected-direction`。** 那個 slug 只是 `run-case.json`
    `verdict_class.overrides` 的一個條目，多數 case 根本不帶它，照字面無法實作；改成比對
    **命中／保護**，也就是 ship gate 本來就據以陳述的單位。代價要記著：ids 1、2、6、7、8、9
    的計分列橫跨兩類又沒有 `bucket` 可據，類別判不出來，這六案只記判讀、不做一致性比對。
    原措辭隱含這種情況不存在。

  - **理由 3/4 必填、1/2 選填。** 兩者都會問，1/2 的提示標「（選填）」。指向 AI 的判讀是規則
    寫作的依據，必須說出看到什麼；1 偏人與 2 不確定是訊號的缺席，逼一句話出來只會產出一年後
    讀起來像證據的填充物。空理由的條目在生成區直接省略 `What the verdict turned on`，規則寫
    在生成區 intro 講一次，不逐則塞「作者未給理由」。
  - **`--card ID` / `--record ID`：非互動的兩道門，給 agent TUI 驅動用。** 互動迴圈本來就是
    呈現、收答、落帳三段；agent 相容不是移植 UI，是把三段拆開讓 agent 當啞管道。`--card` 印
    卡片（blocked 案 exit 2），`--record` 重跑 `build_card` 驗證後才落帳，從不信任呼叫端上一次
    `--card` 的輸出。tty 閘只繞這一條——`--record` 語義上就是「答案已在別處收好」。

  單檔 1038 行，超過 `check-labels`（395）這個實質上限，是刻意留的：其中 153 行空行，其餘
  大半是記錄反例的 docstring——ids 45/48 把引號放在規則名裡、ids 31/41 引文內有巢狀引號，
  這兩組正是「span 抽取不能用 regex」的證據，而它們都不在 sweep 目標裡，砍掉不會立刻被發現。
  五個關注點（config／extract／ledger／render／loop）一條線讀得下來，拆 package 還要連帶
  改名（`tools/annotate` 與 `tools/annotate/` 撞名），不划算。

  另外三案（ids 2、4、12）的 prompt 形狀無法在不洩題的前提下剝乾淨，標為 needs-manual、
  不進判讀流；全部落在 repo 自撰的 1-12，sweep 目標一案未失。這份名單是 fixture 不變式——
  它一變就代表有人改了 prompt 形狀，剝離邏輯要重讀。

### 2. ported-case sweep — 續走 id 33

- [ ] **The remaining ~36 ported speak-human-tw cases (ids 15/16, 18–20, 22–27, 29–37, 39–54) are
  still unadjudicated and may hold more taste mismatches with this repo's judgment.** Four cases from
  the same batch were adjudicated 2026-07-30 and landed this round: **id 17** (「業界專家普遍認為」
  -shaped sentence ruled no-AI-味 twice — blind, then again after being shown `模糊歸屬`'s own
  rule text — retired from the scored suite since flipping it would contradict the rule's own
  `抓` example; rule text unchanged this round), **id 21** (粗體標籤＋條列形式 — list form itself
  isn't the defect, key narrowed to the label-restatement formula that actually is), **id 28**
  (single 解說導引腔 instance — inside the rule's own density carve-out, flipped to
  protection-class; new id 57 added so the rule keeps hit-side coverage), **id 38** (第二句
  「今天，我想跟大家分享我使用 AI 改稿的三個心得」 是正常開場 — key split so only the 時代大帽子
  first sentence stays flagged; `corpus.md`'s A-08 annotation reconciled on the same
  referent-based reasoning). All four verdicts, with the reasoning that produced them, are now
  in [`evals/judged-cases.md`](evals/judged-cases.md) — closing the hand-transcription gap this
  item used to note.

  **進度 2026-08-01：15/36 判完，續跑從 id 33 開始。** 已判 ids 15、16、18、19、20、22、23、
  24、25、26、27、29、30、31、32；剩 ids 33-37、39-54。判讀走 `tools/annotate` 的
  `--card` / `--record`，帳本在 [`evals/annotations.json`](evals/annotations.json)，
  渲染結果在 `judged-cases.md` 的 `annotate:begin/end` 區段。**與 key 相左 3 例：ids 23、27、
  31**，三案都是作者判 1 偏人而 key 屬命中類。要不要改 key 是第 3 項與第 4 項的決定，
  這一步只記錄，`evals.json` 未動。

  這輪判讀期間修掉的一個真 bug：span 抽取用 `strip("「」")` 剝界定符，會連帶吃掉以巢狀引號
  結尾的內層 `」`（id 31「…愛因斯坦也說過：「複利是…第九大。」」少一個收尾），等於拿一段
  fixture 裡不存在的文字去問作者。改成剝頭尾各一字元。已記的判讀 digest 無漂移。

  The sweep originally stalled at ids 15/16, 18 (PR #20) before finding those four; that stall
  is what `tools/annotate` was built to clear, and ids 15-32 above are the first stretch it
  cleared. Two cases from the same source batch were deliberately *not* ported here because they
  test the 陸用語／簡體殘留 axis; they are tracked in
  [`skills/avoid-china-writing/backlog.md`](../avoid-china-writing/backlog.md), and neither side
  blocks the other.

### 3. `evals.json` 三個結構缺陷

- [ ] **Three structural defects in `evals.json`.** Found by the 2026-07-30 54-case run; the
  instrument was left frozen that round so the skill fix stayed comparable to the baseline.
  (1) **Hit-class and protection-class cases are partitioned into separate id ranges** — c3 is
  all-hit, c5/c6 all-protection — so no chunk tests both directions on the same material, and a
  degenerate runner that flags nothing scores 25/25 on c5+c6. (2) **Several detect-mode cases
  carry rewrite-phrased expectations** (「改成」「全清」「刪掉」) that cannot be checked literally
  against a detect output, forcing graders onto the softer "did the report point this way" bar.
  (3) **Single `expected-direction` slugs bundle 2–3 independent requirements** (id 34 wants
  prose-ification *and* concrete detail), so binary scoring reads "half done" as a full miss.
  id 38 had the same shape (two independent deletions in one slug) and was split into separate
  `expectations` entries during the 2026-07-30 key-fix round (see `evals/judged-cases.md`).
  id 21 was fixed in the same round but is a different defect, not this one — its old key's
  demand was substantively wrong (asked for prose-collapse, which is the wrong rule's remedy),
  not merely bundled; the fix rewrote the direction rather than decomposing it. The remaining
  unadjudicated ported cases may hold more of either shape.

### 4. `口語化萬能詞` 名詞與短語 form 的兩側覆蓋

- [ ] **`口語化萬能詞`'s new 名詞與短語 form needs eval coverage on both sides.** The rule was
  widened 2026-07-30 from 口語化萬能動詞 to cover 比喻/slang standing where the
  generally-understood term belongs (「兩條路」→「兩個方式」; ruling in `evals/judged-cases.md`).
  Nothing measures it yet:
  - **Hit case** — id 7's 「兩條路」 is the adjudicated example but is not in that case's key.
  - **Protection case** — this is the one that matters. Widening a catch from verbs to nouns
    and phrases puts every figurative noun in range, so a register that legitimately carries
    figuration must be shown to survive: `casual` voice, and a 署名文體 draft whose metaphor
    system is declared under 保護清單⑥. The two carve-outs written for it (已成通用術語的比喻;
    宣告過的比喻系統) are untested prose until a case fires at them.
  Until both exist, treat the widening as unverified — it is the kind of change that buys one
  hit and pays for it in false positives nobody measured.

### 5. rewrite mode 的口語時間表達 保真 case

- [ ] **A 保真 case for colloquial time expressions in rewrite mode.** In the 2026-07-30 run,
  id 40's runner normalised 「3/31 晚上 11:59」 to 「3/31 23:59」 inside its own report. Harmless
  in detect mode (the text was untouched and the verdict stood), but the identical reflex in
  rewrite mode is a 保真 failure, and nothing currently tests for it.

## Behaviour changes, each on its own branch and its own re-run

- [ ] **`模糊歸屬` may be scoped too wide — id 17's adjudication found it catching a defect
  ordinary human writers also commit, not just an AI tell.** The author ruled a 「業界專家普遍認為」
  -shaped sentence has no AI 味, in isolation, even after being shown the rule's own 抓／保留 text
  (`references/zh-rules.md:218-222`) — reasoning 「規則本身抓得太寬」「是一般人類文章也可能犯的錯誤」；
  full record in [`evals/judged-cases.md`](evals/judged-cases.md). Explicitly scoped to that one
  case by the author, not a mandate to change the rule now — but the shape is worth naming:
  `解說導引腔` already has a density carve-out (a single instance doesn't count, only stacking
  does — `references/zh-rules.md:58-63`); `模糊歸屬` has no isolated-instance equivalent. Whether
  it needs one — and whether other rules share the gap — is a behaviour change and needs its own
  branch and re-run, not a fold-in to a key-fix round. `corpus.md`'s A-06 (`:789`) is the
  distinguishing datapoint already on record: the same 模糊歸屬 pattern there co-occurs with
  `對比句式` and a 「值得深思的現象」 framing sentence, and stays flagged — so any fix is about
  isolation, not about weakening the rule wholesale.

- [ ] **Make `detect` the default mode, and ask before rewriting.** Requested 2026-07-30. Today
  `rewrite` is the default and the skill edits text without being asked twice; the wanted
  behaviour is detect-first — run the audit, report findings grouped P0/P1/P2, then ask whether
  to rewrite whenever the finding list is non-empty (a clean draft reports clean and asks
  nothing). Explicit `rewrite`/`--mode` requests must keep winning, or the eval prompts stop
  testing what they say they test. Held out of the carve-out-gate branch deliberately: the mode
  switch changes which cases exercise rewrite paths at all, and the three global rewrite checks
  (保真／不換湯／不代筆) currently ride on the four rewrite-mode cases in chunk 1 (ids 2, 6, 8, 9).

- [ ] **進階補完模式 — close the smallest holes by asking, never by writing.** Wanted
  2026-07-30. Today the skill is pure subtraction, and `docs/humanizer-zh.md` says so twice:
  「它只拿掉不該有的，加不進來的東西留給你」 and 「`作者隱身` 只報不改」. That is the right default
  and stays the default — but it leaves the author holding a report full of 「此段扣除語氣後無實質
  內容」 with no path forward inside the tool. The wanted mode closes the *smallest* of those
  holes by **asking**, not by composing: for each hollow span, put the question to the author as
  options they can pick rather than prose they must write (「這段想講的是 (a) 成本 (b) 相容性
  (c) 交期？」 → 「數字是多少？」), then splice the answer in at the minimum length that makes the
  sentence carry information. **The line this must not cross:** every fact in the output came
  from the author's answer, never from the model's guess — that is the only thing separating
  this from the ghostwriting the skill exists to prevent, and the thing an implementer under
  pressure will erode first. Explicitly out of scope: 大範圍補洞. A draft that is hollow
  throughout does not get interviewed paragraph by paragraph; it gets handed back with the
  report it already gets today, because at that volume the Q&A is just a slower way to have the
  model write the piece. Sequencing: needs the detect-default change above to land first (it
  only makes sense as a step *after* a report the author has read), and needs its own eval cases
  — the existing 保真 checks all assume output ⊆ input, which stops being true here. Design
  question to settle before building: whether spliced-in text is marked in the output so the
  author can see what came from their own answers.

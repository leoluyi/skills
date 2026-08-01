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

The instrument is not a clean bar either, and everything in this section ends in a changed key —
which forces a re-baseline of **both** versions and a from-scratch re-run of the aggregate
gate's rounds. That cost is paid once per round, not once per item, so these land
together and re-baseline once at the end. Within the round, do them one at a time rather
than interleaving; **step 1 exists to make step 2 affordable, and step 3 must not start
until step 2 has closed.**

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

### 2. ported-case sweep — 收工 2026-08-01

- [x] **The 36 ported speak-human-tw cases (ids 15/16, 18–20, 22–27, 29–37, 39–54) held more taste
  mismatches with this repo's judgment than the first stretch suggested.** Four cases from
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

  **收工 2026-08-01：36/36 判完。** 判讀走 `tools/annotate` 的 `--card` / `--record`，帳本在
  [`evals/annotations.json`](evals/annotations.json)，渲染結果在 `judged-cases.md` 的
  `annotate:begin/end` 區段。分數分布 1 偏人 ×13、2 不確定 ×6、3 偏 AI ×9、4 明確 AI ×8。
  這一步只記錄，`evals.json` 未動——相左的案子在第 3 項複審，不在這裡處置。

  **與 key 相左 13 例，分成方向相反的兩群**，而兩群的存在本身就是第 4 項要處理的東西：

  - **key 抓太寬（6 例，ids 23、27、31、33、35、37）** — 作者判 1 偏人，key 屬命中類。
  - **key 放太鬆（7 例，ids 41、43、45、47、52、53、54）** — 作者判 3-4 偏 AI，key 屬保護類。
    全部是改編自 speak-human-tw 的 SNF 保護案，其中 6 例落在 id 41 之後。

  另有 6 例（ids 19、22、25、26、29、51）判 2 不確定，`contradicts_key` 為 `null`，不參與比對。

  **後半群的理由反覆指向三個尚未成規則的東西**，這是 sweep 最值得帶走的收穫，不是相左計數：
  短句堆砌（43、45、52）、太生硬（41、53）、**體裁錯配**（53「部落格應更強調連接詞」、
  54「小說 OK，電子報就很怪」）。第三個特別值得看——那兩例判的不是句子本身，是句子與宣告體裁
  的不相稱，而現有 45 條規則沒有任何一條問這件事。它是新規則的候選，不是既有規則的 carve-out。

  這輪判讀期間修掉的一個真 bug：span 抽取用 `strip("「」")` 剝界定符，會連帶吃掉以巢狀引號
  結尾的內層 `」`（id 31「…愛因斯坦也說過：「複利是…第九大。」」少一個收尾），等於拿一段
  fixture 裡不存在的文字去問作者。改成剝頭尾各一字元。已記的判讀 digest 無漂移。

  The sweep originally stalled at ids 15/16, 18 (PR #20) before finding those four; that stall
  is what `tools/annotate` was built to clear, and ids 15-32 above are the first stretch it
  cleared. Two cases from the same source batch were deliberately *not* ported here because they
  test the 陸用語／簡體殘留 axis; they are tracked in
  [`skills/avoid-china-writing/backlog.md`](../avoid-china-writing/backlog.md), and neither side
  blocks the other.

### 3. 衝突複審 — 收工 2026-08-01

- [x] **`contradicts_key: true` 的 13 案全數解盲複審完畢。** 盲判說「這句沒有 AI 味」而 key 說
  它屬命中類，這個分歧本身不指向任何一邊——可能 key 抓太寬，也可能作者那一眼看漏了。先例已經
  有：id 17 就是盲判一次、看過 `模糊歸屬` 規則文字後再判一次，兩次同向才退出計分。

  **結果與預期相反，這是這一項最值得帶走的東西：**

  | disposition | 數 | ids |
  |---|---|---|
  | `case-wrong` | 6 | 31、33、35、41、43、47 |
  | `judgment-wrong` | 4 | 23、37、45、52 |
  | `key-wrong` | 3 | 27、53、54 |

  設計這一步時的假設是它會產出一批該改的 key，`key-wrong` 因此被寫成「複審存在的理由」。實際
  上最大宗是 `case-wrong`——**近半數的「衝突」不是判讀與 key 的分歧，是量測方式本身有問題**，
  而那六案沒有一案是改 key 能修的。四種故障各自獨立，全部登記在第 4 項。

  盲判筆一筆未失：36 blind ＋ 13 review 並存，13 筆盲判標 `superseded_by: "review"`。分數改判
  4 案（23 1→3、37 1→3、45 4→1、52 3→1），其餘 9 案維持原分——維持原分不等於同意 key，
  disposition 才是結論，這正是當初否決「複審＝重打分」的理由。

  **時序是硬約束，不是偏好。** 第 2 項整輪 sweep 關閉之前不得開始。作者一旦在途中看過幾份
  key，剩下的盲判就在對答案卡做 pattern-match，而盲判正是這支儀器唯一的產出。這與下方
  `tools/annotate` 第二個用途裡 (I) 「引出器與判讀輪次互斥」是同一條規則的另一個實例。

  **複審集合只收 `contradicts_key: true`。** score 2 不確定回傳 `null` 而非 `false` 是刻意的：
  不選邊不是同意，也同樣不是不同意，把它拉進複審等於逼作者在沒有訊號的地方選邊。ids 1、2、6、
  7、8、9 那六案的 `null` 是類別判不出來（計分列橫跨兩類又無 `bucket`），那是 `evals.json` 的
  結構問題，屬第 4 項，不屬複審。

  **複審卡把盲判卡藏的東西全部攤開**：key class、expectation、規則名，外加作者自己那筆盲判的
  分數與理由。這是另一個 card builder，不是 `build_card` 加一個旗標——兩張卡要呈現的東西是互補
  的，共用一條路徑遲早會有人把 expectation 漏進盲判卡。

  **產出是三選一的處置，不是重打分**，記進帳本的 `disposition` 欄位：

  - `key-wrong` — 作者維持原判，key 該改。**這一類是第 4 項的輸入**，也是複審存在的理由。
  - `judgment-wrong` — 作者改判，key 站得住，盲判筆退場。
  - `case-wrong` — 兩邊各自都對，是這個 case 測錯東西，重寫或退出計分（id 17 的處置）。

  純粹重打一次 1-4 分接不上這件事：「作者維持原判」與「案子該退場」會記成同一筆。

  **實作落地 2026-08-01**：帳本改成同一 `case_id` 多筆，複審筆帶 `pass: "review"` 與
  `disposition`，盲判筆填 `superseded_by`（該欄位原本只寫 `None`，全檔沒人讀，等於預留了洞沒
  接管線）。新增 `--review-card`（解盲）與 `--review`（落帳）兩道門，與 `--card` / `--record`
  互斥。`build_review_card` 刻意不是 `build_card` 加旗標——後者是一組防洩題的 fail-closed 閘，
  前者存在的目的正是把那些全部攤開，共用一條路徑遲早會有人把 expectation 漏進盲判卡。
  `--review` 一律要求 `--rationale`：盲判那條「1 與 2 可留空」的規則不適用，解盲後的判斷是要
  拿去改 key 的依據。`--redo` 的語義按 pass 分開，重跑盲判不會連帶刪掉已記的複審。

### 4. `evals.json` 的結構缺陷 — 原有三項，複審再加四項

複審把這一項的性質改掉了。原本它是「key 措辭要修」的清單，第 3 項跑完之後，**多出一條量測方式
的線**：13 案相左裡有 6 案的問題不在 key 的措辭，在這支儀器問問題的方式。兩條線都在下面，
量測那條排前面——不先修它，下一輪 sweep 會再生出一批同樣的假衝突。

#### 4a. 量測方式的四種故障（複審 2026-08-01 找出）

- [ ] **(1) 有些案子的判準根本不是 surface（ids 31、33）。** id 31 測的是假引用（哈佛研究查無
  此數據、愛因斯坦語錄偽託），id 33 測的是空洞前景段。兩者都該抓，但**人也完全寫得出假引用與
  空話**——查證問題與空洞問題不是「讀起來像不像 AI」的問題。`SKILL.md` 剛定調的 surface／
  provenance 分野在這裡有第二個推論：不是每條規則都在量 surface，而拿 AI 指數去校準一條不量
  surface 的規則，量出來的東西沒有意義。要嘛這些案子退出 AI 指數校準（保留在 `evals.json` 供
  run-case 用），要嘛 annotate 要能標記「本案不適用 AI 指數」。

- [ ] **(2) 粒度錯配：卡片給整段，key 只指其中幾句（id 35）。** 那段五句裡三句是帶數字的事實
  句，兩句是空話；整段讀起來像人寫的，而 key 只針對那兩句。整段偏人與那兩句空洞可以同時成立，
  `contradicts_key` 卻記成分歧。**凡是「段落裡只有部分該抓」的 case 都有這毛病**，不只 id 35。
  修法要嘛讓 key 標出它指的是哪幾句、卡片照樣呈現整段但分句收判讀，要嘛承認整段判讀無法校準
  子句層的 key。

- [ ] **(3) 兩種保護被 `contradicts_key` 混為一談（id 41）。** 保護類有兩種完全不同的理由：
  「這段沒毛病所以放行」與「這段不准動，就算有毛病也不准」（保護清單②具名見證原話、③承諾條款、
  ⑤引文與程式碼）。id 41 是後者——作者判它 4 明確 AI 完全可以同時成立，因為 key 主張的不是
  它沒有 AI 味，是它不可改寫。`key_classes()` 只回命中／保護兩值，於是這類案子必然假衝突。
  保護類需要再分一層：**`保護-無瑕` 與 `保護-禁動`**，後者不參與 AI 指數比對。

- [ ] **(4) 合成語料撐不起保護類（ids 43、47）。** upstream 自己聲明「所有用例皆為合成文本，
  不指向任何真實人物、品牌或課程」。命中類不受影響——句子帶著要抓的毛病就成立，誰造的不重要。
  **保護類的整個主張卻是「這是真人會寫的東西，不准動它」**，用一句造出來示範人味的句子去測，
  等於用人味的演出代替人味本身。id 47 最尖銳：key 把它當人味典範「一個字都不用動」，而它的
  「不完美」（「結果，嗯，」的停頓位置）擺得太整齊——真人打字多半直接寫「結果我就」。id 52 是
  同一政策的另一種傷害：工具名被抽成 A／B 代號，而真人寫這句會直接寫工具名。**保護類需要真實
  語料替換**，這是語料工作不是改 key，成本最高的一項。

#### 4b. key 措辭要修（原有三項 ＋ 複審產出的 3 案）

複審判為 `key-wrong` 的只有 3 案，其中 ids 53、54 是同一個發現：

- [ ] **`體裁相稱` 是現有 45 條規則沒有的面向（ids 53、54）。** 兩案的 key 都只論內容層就放行
  ——53「底下墊著具體數字與真實轉折」、54「停頓有不可替代的敘事功能」——**兩條舉證都成立**，
  作者也沒有反駁它們。作者反駁的是另一件事：53 是部落格寫得像規格書（冒號壓縮因果，缺連接詞），
  54 是電子報寫得像小說（逐拍敘事）。同一段文字換個體裁標籤就從得體變成不得體，而 key 從頭到尾
  沒問這件事。`作者隱身` 最接近但不是同一件事——它問作者在不在，不問語域對不對。這是**新規則的
  候選**，不是既有規則的 carve-out，因此要自己的 branch 與自己的 eval（見下方行為變更區）。

- [ ] **id 27：`知識截止免責` 抓太寬。** 「由於資訊有限，無法確認該工具最新的定價方案」——作者
  維持 1 偏人，理由是這是人也會寫的謹慎語。這條是 P0，而 P0 的門檻應該是「讀者看到就不信任整份
  文件」；一句沒有主詞的謹慎語達不到那個門檻。與 id 17（`模糊歸屬`）、id 37 是同一族的問題：
  規則抓到真缺陷，但那缺陷不專屬 AI。

#### 4c. 原有三項（2026-07-30 的 54-case run 找出）

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

### 5. `口語化萬能詞` 名詞與短語 form 的兩側覆蓋

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

### 6. rewrite mode 的口語時間表達 保真 case

- [ ] **A 保真 case for colloquial time expressions in rewrite mode.** In the 2026-07-30 run,
  id 40's runner normalised 「3/31 晚上 11:59」 to 「3/31 23:59」 inside its own report. Harmless
  in detect mode (the text was untouched and the verdict stood), but the identical reflex in
  rewrite mode is a 保真 failure, and nothing currently tests for it.

## `tools/annotate` 的第二個用途 — 人機判定盲測

上面第 1 項落地的 `tools/annotate` 判的是 **AI 味**：這句讀起來像不像 AI 的手筆。第二個用途
問的是另一件事——**這段究竟是不是 AI 寫的**。同一個問作者的迴圈，不同的問題；而後者是驗證任何
人機判定主張的唯一路線。排在上面那一輪之後，不與 re-baseline 交錯。

2026-08-01 的一次判讀 session 產出三個候選判準：

- **語體漂移** — 一句話同時想當條列標題與完整句子，兩邊都不成立：前半名詞化而無謂語，唯一的
  動詞卡在句末、跨過一個逗號回頭找受詞，中間沒有「將」「等」「——」任何一個授權標記，而逗號
  授權不了這種前置。
- **組裝感 ＋ 高完成度，這個矛盾才是決定性的** — 人的失敗是減法：漏字、缺主詞、標點不一致；
  AI 每個零件都在，但框架是歪的，讀起來毫無阻力，停下來才發現沒有一處真的接上。
- **結構訊號重於內容訊號** — 內容可以從一張表、一份模板、一份來源文件繼承而來，語法是當場
  生成的。

**這三項都不算證據。** 那場 session 不是盲測：判讀者知道答案，中途又拿到一份人寫的對照改寫，
模型被引導過。裡面任何信心度的移動都無法歸因於證據而非說服。三項都是待盲測驗證的假設。

**MVP —— 拿到第一份可用資料集的最小集合：** 盲呈現 (A) ＋ 兩個必填欄位 (B) ＋ ground-truth
回寫 (C)。少於這三項，跑出來的東西根本不構成量測。

- [ ] **(A) 盲呈現。** 藏標籤、隨機化順序，並且絕不揭露這一批的 AI 佔比——講出比例會把判讀變成
  數數而不是判斷，判讀者光靠先驗就能命中報出來的 base rate。既有的判讀卡已經藏掉 expectation
  與規則名，那是為了不洩題給 AI 味判讀；這裡要藏的是**來源**，是另一層。以下每一項的前提：判讀
  者若推得出答案，這裡沒有一項還有意義。

- [ ] **(B) 每則判讀必填 信心度 與 證據類型。** 信心度必填而非選填，因為校準曲線無法事後重建。
  既有的 1-4 AI 指數只部分覆蓋它：那把尺量的是 AI 味有多強，錨點 2「不確定」回傳 `null` 已經
  是不選邊的出口，但人機判定要的是「有多確定這段是 AI 寫的」——量的東西不同，錨點文字要另寫，
  不能沿用。證據類型記的是主要證據屬 語法類 或 詞彙類，那個欄位就是 結構訊號 > 內容訊號 這項
  主張的全部檢驗；沒有它，一輪跑完只答得出「我們判對了沒」，答不出「理由對了沒」。

- [ ] **(C) Ground-truth 回寫。** 判讀關閉後由判讀者揭露真實來源，工具寫進帳本。寫入端跟著既有
  實作走：真相來源是 [`evals/annotations.json`](evals/annotations.json)，`judged-cases.md` 的
  `annotate:begin/end` 區段從帳本渲染而來，不要繞過帳本直接改 `evals.json`。揭露必須嚴格晚於
  判讀落帳——揭露若能被提早觸發，(A) 就只是多幾個步驟的擺設。依賴 (A)。

- [ ] **(D) 配對語料 — 同一份內容的人寫版與 AI 版並排。** 把題材與詞彙固定住，判對就只可能是
  從結構判出來的。這是語料工作不是工具程式，可以與 (A)–(C) 並行收集；但 結構訊號 > 內容訊號
  這項主張沒有它就測不動，在它落地之前 (B) 的 證據類型 欄位是欠功率的。

- [ ] **(E) 人類盲標基線。** 要的是未受輔助的人判同一批語料的基線，不只是現有的 no-skill 模型
  基線。skill 要回答的是它有沒有贏過一個人的直覺；只跟 no-skill 模型比，它可以贏了還是沒有用。
  依賴 (A)。**同一則樣本對同一位判讀者互斥**：一旦有人帶著 skill 判過某則樣本，他在那則上就
  不再是天真基線——兩個 arm 需要不相交的判讀者或不相交的樣本，兩者跑在同一對上正是要設計來
  避開的失效模式。

- [ ] **(F) 難例池 — 判錯的樣本回流成評測案例。** 優先三類近似案：非母語寫作、翻譯體、模板填空。
  三者都帶著 組裝感 而 完成度 偏低，而那正是 組裝感 這條判準會殺到真人的地方。回流一樣走帳本，
  再進 `evals.json`。依賴 (C)。

- [ ] **(G) 主要指標是 誤殺率（人寫被判成 AI），不是 accuracy。** 對一個去 AI 味的工具而言，
  false positive 比漏抓貴——它叫作者去重寫本來沒問題的文字，量一大就是一項指控。accuracy 會蓋
  掉這件事：AI 樣本少的一批可以分數好看，同時把每一則人寫的都燒掉。依賴 (C) 與 (F)。

- [ ] **(H) 雙軸評分（組裝感 × 完成度）—— 假設，兩個條件都成立才動。** (1) 盲測資料顯示那個
  矛盾象限真的分得開；(2) 分界能寫成 SKILL.md 的判準散文，而不是一個分數門檻。只滿足 (1) 的
  意思是這個發現記進 `design-notes.md` 就停在那裡，**不進 skill**。兩種結局在構造上互斥；動任何
  規則文字之前，先決定資料買到的是哪一種。依賴 (A)–(C) 與 (G)。

- [ ] **(I) 最小對照改寫引出器 —— 只在 debrief 階段。** 吃一句可疑的句子，生成兩個人類形式的
  改寫（升格成完整句／降格成附註），再把三份互相 diff 來定位缺陷。**與任何判讀輪次互斥**——這正是
  2026-08-01 那場 session 被汙染的方式，工具必須在判讀未關閉時拒絕執行，而不是只把規則寫在
  文件裡。帳本已經知道哪些判讀還開著，這道閘有現成的依據。依賴 (C)。

不要重蓋：`evals.json` 的讀寫與報告渲染在 `tools/run-case` 已經有了，問作者的迴圈與落帳在
`tools/annotate` 自己的 `--card` / `--record` 與帳本也已經有了。新的只有盲的那一層。另外，
root [`backlog.md`](../../backlog.md) 把 `tools/add-case` 排在「annotate 落地 ＋ 一輪真實 sweep」
之後才決定——兩個前置現在都到齊了，而帳本加渲染這條寫入端已經蓋掉它原本想做的事，那一項該下
結論而不是接著蓋。

- [x] **`翻譯腔` 明文排除機翻做為保留理由.** Landed 2026-08-01 mid-sweep, at the author's explicit
  request, accepting the contamination cost below rather than deferring to a clean branch.
  `references/zh-rules.md`'s 翻譯腔 rule now states that whether a span is machine-translated
  or human-written-under-English-influence does not change the verdict — the three checks
  (回譯成流暢英文／中文是英文的影子／台灣同儕不會這樣講) decide it either way, and being
  suspected MT is not a carve-out. This is a genuine behaviour change (rule text moved, not
  just framing), so it does re-key any case whose expectation depended on the old silence on
  this point.

  **Sweep contamination, recorded rather than hidden:** this landed between id 47 and id 49 of
  the ported-case sweep (item 2 below), which was still 6 cases short of closing (49–54
  remaining as of this edit). The remaining cases are judged with this rule change in view,
  the first 30 were not — the sweep's blind-judgment property does not hold uniformly across
  its own 36 cases. Whatever the aggregate re-baseline (item 7) does with `contradicts_key`
  counts, it cannot treat all 36 verdicts as interchangeable data; the pre-/post-47 split is
  the fact to carry forward, not paper over.

- [ ] **新規則候選：`體裁相稱`——語域配不配得上宣告的體裁。** 複審 ids 53、54 兩案獨立指向同一
  個缺口（詳見第 4b 項）。現有 45 條規則全都在問「這段有沒有多出不該有的東西」或「作者在不在」，
  沒有一條問「這段的語域屬不屬於它宣告的體裁」。兩個實例：部落格用冒號壓縮因果、缺連接詞，讀起來
  像規格書；電子報用逐拍敘事（她叫、我沒回、她再叫、我才回），讀起來像小說。

  **動手前要先解決的問題**：這條規則與 `context` 剖面高度重疊——`docs`／`blog`／`linkedin` 已經
  在調每條規則的鬆緊。要判斷它是**新規則**還是 `context` 機制該長出的一個面向，先寫得出判準散文
  再說。誤判風險也高：語域偏移是程度問題，不像「AI 工具殘留標記」有明確的形。抓太寬會殺掉所有
  寫作風格偏正式的部落客。**兩案不足以立一條規則**——先在既有語料裡找同型案例，湊不出第三、
  第四例就把發現記進 `design-notes.md` 停在那裡，不進 skill。

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

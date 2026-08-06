# humanizer-zh backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

**Open items only.** What already shipped, and why it took the shape it did, lives in
[`design-notes.md`](design-notes.md), `evals/results-*.md`, and commit messages — not here.
Anything deleted from this file is recoverable with `git log -p`.

2026-08-02 的分類與待裁決選項在 [`backlog-triage-2026-08-02.md`](../../backlog-triage-2026-08-02.md)。

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

## 儀器層仍開著的四件事

每一項都動 `evals.json` 的 key 或它的語料，而動 key 就要求**兩個版本一起重跑基線**，aggregate
的 rounds 也得從頭再跑一次。所以這四項一批走，不逐項 re-baseline——上一輪的批次落地清單與
這條約束的由來記在 design-notes 的〈evals.json 的結構修補〉。

- [ ] **合成語料撐不起保護類：只剩 id 52。** 保護類的主張是「這是真人會寫的東西，不准動它」，
  用造出來的句子測等於用人味的演出代替人味本身（ids 43、47 與另五案已於 2026-08-01 換成真語料，
  過程見 design-notes）。id 52 記下的病灶是**工具名被抽成 A／B 代號**——真人寫這句會直接寫工具
  名——要修它得要同型的真材料：真人寫的條件式工具建議。拿一段形狀不同的真語料去蓋掉它，等於用
  換題目的方式讓病灶消失。FB 頁面的貼文串只在作者手動捲動後才 lazy-load，工具端的捲動與
  `navigate` 都會把狀態打回骨架，所以**補料要作者再刷一次頁面**或直接貼文字過來。

- [ ] **`語體漂移` 沒有任何 case 測非母語寫作。** 規則 2026-08-01 落地時配了三個保護案——欄位
  體裁（id 69）、弱訊號疊加（id 70）、筆記語域（id 71）——作者當輪裁示砍掉原訂的非母語寫作案，
  因為手邊沒有真語料，而合成語料在保護類的舉證力已被上一項判定不足。代價要記著：**「非母語
  寫作也有組裝感、只是完成度偏低」正是這條規則的保留條款最該防的誤殺方向**，而現在沒有任何一案
  測它。補料時與下方〈人機判定盲測〉的 (F) 難例池同批處理——那一項列的三類近似案（非母語寫作、
  翻譯體、模板填空）裡，模板填空已由 id 69 覆蓋，剩兩類。

- [ ] **三列出現過一到兩輪、機制各不相同，下次動 rewrite 端時回頭看。**
  `28/no-single-instance-false-positive`（把已放行的導引句改掛他條重標，r2、r4）、
  `59` 的兩列（r3 反向、r5 正向）、`64/全域:保真`（r1 掉句、r2 插入「原文是」、r4 把
  「SEO 的死亡」降成「會受到影響」——每輪不同機制而 base 都過）。單看任一輪都像雜訊，
  合看則指向新版在 rewrite 案上比 2.1.0 更敢動手。

- [ ] **`自我背書`（第 47 條）四案齊備但一輪未跑，且保護側兩案是合成的。** 命中案 id 72 的原句
  是模型生成、作者提供（語料庫 A-13）；保護案 id 75（操作句不是稽核句）是作者親筆改寫，屬真
  語料。**仍待替換的是 ids 73（消歧義優於防守）、74（來源註記是標註不是背書）**——兩案為測
  carve-out 現寫，受本節第一項（合成語料撐不起保護類）的判定所限。真語料替換以方法章節或稽核報告裡真的宣告涵蓋範圍的
  段落最合適。

  **這條規則過煞車的方式與另外兩條不同，要記著。** 下方〈新規則候選〉那條煞車是「兩案不足以立
  一條規則，先在既有語料裡找同型案例」。本條作者 1 案、語料庫掃出 0 案，照字面過不了；實際是
  作者當輪裁示開規則。對照組：`語體漂移` 走了五輪量測才 ship，`體裁相稱` 被同一條煞車擋著至今。
  **本條兩者皆無**，是目前三條新規則裡證據最薄的一條。

  **第一輪要盯的誤標面**：carve-out 的分界是消歧義 vs 防守，而「方法章節、稽核與合規報告裡
  來源與涵蓋範圍本身就是交付物」這一條放行的範圍很寬。抓太鬆會讓 `docs` 體裁整片豁免，抓太緊
  會殺掉所有正當的方法陳述。id 73 的移除測試（拿掉這句讀者會不會套錯判準）是唯一的可執行判準，
  它撐不撐得住要看第一輪。

## `改法` 行外溢：覆蓋量已量出來，痕跡調查卡在儀器

- [~] **`語體漂移` 那次外溢是單一觀察，但機制看起來是通則。** 它的 `改法` 給了「降格成條目：
  時程降級成括號附註」，模型讀成通用許可，在無關的 rewrite 案裡也開始加括號編註，三輪 NO-SHIP，
  拿掉才過閘（`design-notes.md` 記了全程）。`破碎短句堆疊／缺連接詞` 落地時據此不寫 `改法`。
  現在還帶 `改法` 的只剩三條，值得看它們有沒有同款跡象。

  **判別式是「這個手段搬得動嗎」**——外溢的那一條之所以外溢，是因為「加括號附註」是任何句子
  都套得上的表層動作，脫離原規則的形態仍然成立。照這個標準先分類，省下逐條重讀：

  | 規則 | `改法` 的形狀 | 搬得動嗎 | 風險 |
  |---|---|---|---|
  | `對讀者說教`（zh-rules.md:291） | 主詞換第三人稱、`你` 換泛稱主體 | 搬得動，任何帶 `你` 的句子都套得上 | 高 |
  | `對比句式`（:72） | 其餘改直述或換句型 | 半搬得動，但綁在「同一篇兩次以上」的密度條件上 | 中低 |
  | `翻譯腔`（:135） | 丟開原句、只留意思重想 | 搬不動，它講的是怎麼想不是改成什麼 | 低 |

  `對讀者說教` 是唯一該優先驗的：它的手段最可搬，而它自己的保留欄明文允許 `casual`／`blunt`
  聲音與教學的程序性第二人稱保留 `你`。改法外溢到那些語域，正好會踩掉自己的 carve-out。
  它末句「方向要講到人稱這一步」還會加強這個傾向——那句話是為了防改一半，但同時也在告訴模型
  人稱轉換是個該追求的終點。

  **不要提前砍。** 三條的 `改法` 都在解決真問題（`對比句式` 防的是把密度問題當逐句錯，
  `對讀者說教` 防的是改一半），沒有證據就拿掉會退掉真正有用的方向——這正是 `語體漂移` 那輪
  用三輪量測換來的教訓的另一半。

  **覆蓋問題 2026-08-02 量完了，答案比預期難看，而且它先於痕跡調查成立：**

  | 規則 | 計分覆蓋 | 其中 rewrite 模式 |
  |---|---|---|
  | `對讀者說教` | 2 案（ids 14、56，皆為期望列） | **0** |
  | `對比句式` | 3 案（ids 18、45 為 `對應規則`，id 7 為期望列） | **0** |
  | `翻譯腔` | 1 案（id 8，期望列） | 1（id 8） |

  **關鍵的不是案數少，是 `改法` 只在 rewrite 模式顯形，而風險最高的兩條各有 0 個 rewrite 案。**
  `對讀者說教` 被上表判為「搬得動、風險高」，它的手段卻連一個可以觀察的場合都沒有——不論外溢
  與否，現行儀器在結構上都量不到。全套 81 案裡 rewrite 只有 12 案，外溢要顯形只可能顯形在
  那 12 案上，而那 12 案沒有一案掛著這兩條規則。

  **痕跡調查本身做不下去，原因是機械的。** 存下來的 `results-*.json` 每列只有一句 grader 的
  `reason`，記的是該期望成不成立，不是 runner 在別案做了什麼。掃過全部 16 個檔、1879 列：
  人稱轉換 訊號 8 列全部落在 id 5（`對讀者說教` 自己那案），`括號附註` 0 列——而 `語體漂移`
  那次外溢確實發生過。連已知為真的外溢都掃不出來，這條路就不是證據不足，是量錯東西。真正的
  痕跡在 runner 的原始輸出裡，而 `.gitignore` 的 `evals/*/runs/` 把它們排除在 repo 之外。

  **所以順序反過來了**：不是「拿現有 eval 看痕跡」，是先給 `對讀者說教` 與 `對比句式` 各補
  rewrite 案，再跑一輪並保留原始輸出。在那之前，這一項沒有可看的東西。補 rewrite 案要動 key，
  所以它跟著上面那批走，不另開。

## `tools/annotate` 的第二個用途 — 人機判定盲測

已落地的 `tools/annotate` 判的是 **AI 味**：這句讀起來像不像 AI 的手筆（設計選擇記在
design-notes）。第二個用途問的是另一件事——**這段究竟是不是 AI 寫的**。同一個問作者的迴圈，
不同的問題；而後者是驗證任何人機判定主張的唯一路線。

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
其中兩項的落地處置（語體漂移 成為第 46 條、組裝感 降級成保留條款）記在 design-notes；**(H)
的閘沒有放行**，雙軸評分要不要成立依舊要等盲測資料。

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

## 新規則候選：`體裁相稱`——語域配不配得上宣告的體裁

- [~] **複審 ids 53、54 兩案獨立指向同一個缺口。** 現有規則全都在問「這段有沒有多出不該有的
  東西」或「作者在不在」，沒有一條問「這段的語域屬不屬於它宣告的體裁」。兩個實例：部落格用冒號
  壓縮因果、缺連接詞，讀起來像規格書；電子報用逐拍敘事（她叫、我沒回、她再叫、我才回），讀起來
  像小說。兩案的 key 都只論內容層就放行——53「底下墊著具體數字與真實轉折」、54「停頓有不可替代
  的敘事功能」——**兩條舉證都成立**，作者也沒有反駁它們。作者反駁的是另一件事：同一段文字換個
  體裁標籤就從得體變成不得體，而 key 從頭到尾沒問這件事。`作者隱身` 最接近但不是同一件事——
  它問作者在不在，不問語域對不對。

  **煞車：兩案不足以立一條規則**——先在既有語料裡找同型案例，湊不出第三、第四例就把發現記進
  `design-notes.md` 停在那裡，不進 skill。2026-08-01 掃過既有語料：**id 51 是強第三例**（電子報
  逐月拍點「第一個月，沒人退訂。第二個月，沒人退訂。」——與 54 同族的小說節奏，作者盲判 2 不確定
  「標點符號改一下應該就像真人寫的」，正是現行 key 說不出口的那個癢處）；corpus A-06 是邊緣第四例
  （個人電子報寫成匿名新聞綜述腔，但構成錯配的 span 已被 `模糊歸屬`×2＋`對比句式` 認領，錯配
  可能是副作用）；corpus H-15（「上一篇我們做了一件事：猜。」）是未來規則必收的 carve-out 錨點
  ——冒號壓縮因果與 53 同形，但貼合它的方法論教學語域。**煞車已過、規則可立案**，走自己的 branch
  與自己的 eval；53、54（以及 51 若一併重審）的 key 改動跟著那個 branch 走——規則不存在之前，
  key 無從要求抓一個沒有規則名的東西。

  **id 53 已被吃掉一半（2026-08-01，隨 `缺連接詞` 落地）**：該案兩個病灶裡，「冒號壓縮因果、
  缺連接詞」現在是 `破碎短句堆疊／缺連接詞` 的句內判準，逐句可標。剩給這條規則的是扣掉那些句子
  之後仍然成立的那件事——整段讀起來像規格書而它宣告自己是部落格。**立案前要重新確認舉證數**：
  煞車是對 ids 53、54 說的，而 53 現在只剩半案；id 51、corpus A-06 仍完整，所以煞車大概仍過得去，
  但這要在動手時親自複核一次。

  **動手前要先解決的問題**：這條規則與 `context` 剖面高度重疊——`docs`／`blog`／`linkedin` 已經
  在調每條規則的鬆緊。要判斷它是**新規則**還是 `context` 機制該長出的一個面向，先寫得出判準散文
  再說。誤判風險也高：語域偏移是程度問題，不像「AI 工具殘留標記」有明確的形。抓太寬會殺掉所有
  寫作風格偏正式的部落客。

  **邊界已先劃好（2026-08-01，隨 `語體漂移` 落地）**：`語體漂移` 判的是**句內**——一句話同時想當
  條列標題與完整句子；`體裁相稱` 判的是**篇章級**——整段語域配不配得上宣告的體裁。兩條的抓欄各自
  寫明不管對方那一層，立案時不必再重談歸屬，只要確認 `context` 剖面的重疊問題。同日落地的
  `破碎短句堆疊／缺連接詞` 也在句內那一側，分界同款：它問單句的關係詞在不在，不問整段語域。

## Behaviour changes, each on its own branch and its own re-run

- [ ] **改寫移動命名 — 把 41 個例子裡隱含的方法叫出名字。** 起於 2026-08-01 的觀察：45 條規則
  裡只有 4 條帶 `改法` 行（`對比句式`、`翻譯腔`、`對讀者說教`，加 `節奏均質` 的反向警告），其餘
  全靠一組 前→後 對照句示範改法，而那些對照句自己聲明是合成的（`references/zh-rules.md:4`）。
  **改寫知識已經在檔案裡，只是從沒被命名。** 逐條補 `改法` 行是錯的做法：41 條規則沒有 41 種
  改法，重讀所有對照句後收斂成約七種移動——換成事實（預設，約 25 條）、刪框（旗標本身是鷹架，
  底下事實已站著）、補成分、降級（改完說得更少但誠實）、留一個（密度型規則）、換主詞、重想
  （唯一禁止逐詞替換的一種）。終局移動已經寫在 `SKILL.md:25`「空洞就標出來，不代筆」，
  `SKILL.md:23`「改寫而非刪除」也已經是移動形狀——八種裡有兩種在檔案裡，其餘六種沒說出口。
  落地形態是 `SKILL.md` 加一份移動清單，規則層每條只加一個標籤詞、且只標非預設移動的那些，
  `zh-rules.md` 不增行。**要等 rewrite case 補夠才做**：這是行為變更，得過 baseline，而 45 條
  規則目前只有 10 個 rewrite case 罩著（2、6、8、9、60、61、63、64、65、66），這個 bar 量不出
  改寫變好還是變壞。作者 2026-08-01 拍板：先語料，後命名移動。

- [ ] **`無主被動`（動作者消失）是現有 45 條規則沒有的面向。** 2026-08-01 作者提出的 AI 味清單
  逐項對照後，唯一真正落空的一項：「許多因素被納入了考量」。`模糊歸屬` 抓的是**夾帶權威**的無主
  被動（「被廣泛認為」），這句沒有權威主張，只是動作者被刪掉；`過度簡寫` 也搆不到——句子文法
  完整。中文被字句過用是有文獻的翻譯腔／AI 標記，但 carve-out 面很大：公文合法省略動作者
  （「奉核可後辦理」），動作者真的不明或不相關時被動也是對的。FP 風險高，需要自己的 branch 與
  自己的 eval，兩側都要有 case。

- [ ] **`陳腔比喻`（死掉的譬喻當分析用）。** 同一次對照的第二個缺口：「雙刃劍」「一體兩面」
  「水到渠成」「冰山一角」「如虎添翼」。`口語化萬能詞` 明列放行「已成通用術語的比喻」，所以不會
  觸發；`四字評語` 查表最接近，但它的作用域限定在**對執行品質的自我讚許**，不收這一類。比
  `無主被動` 小，可以合併在同一條 branch 上跑。

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

  **部分處理 2026-08-03，但這一項仍開著。** carve-out 那輪加了兩條具名放行——讓步開場（引的是
  待反駁的看法）與俚語化共識招呼（不替任何主張供依據），共通判準是「這個第三方有沒有在為某個
  主張供依據」。那是形態層的收窄，不是這一項要的密度層 isolated-instance 判準：單一實例仍然會
  被抓，只是多了兩種形態不算。密度分支要不要開，仍待自己的 branch。

- [ ] **`SKILL.md:130` 把 voice 宣告的正向特徵升格成保護清單⑥，於是「短句」變成豁免（id 86）。**
  2026-08-03 補跑單案讀 runner 原始輸出定位到的，取代此前兩個都不成立的說法（定位過程見
  design-notes 的〈Step 0 定位〉）。runner 把兩個該被 `破碎短句堆疊` 抓的 span 直接掛進保護清單，
  「會結束，放心壓」全篇未曾被當作該規則討論過——不是判它不成立，是它沒有進入判定。

  機制在 `:130` 的「declares positive features, those features are 保護清單 item ⑥」，而 Voice
  `casual` 在 `:128` 宣告的特徵字面就含 short sentences。**病根是升格條款沒有區分「作者刻意造出
  來的東西」（宣告過的比喻系統、刻意的口語破格）與「任何文字都自動滿足的通用屬性」**；前者是它
  要保護的，後者讓專抓短句的規則被自己的保護清單架空。

  eval id 86 的 `does-not-spare-on-casual-register` 那一列自己寫的病因（跨條借用 `過度簡寫` 的
  語域分支）不成立——runner 輸出零次提及 `過度簡寫`。該列的敘述之後要一併更正。

  另有第二條路徑在 r4／r6 的 grader reason 裡有據但補跑那輪未現形：`:126` Context `casual` 的
  「P0, plus `破碎短句堆疊`」被讀成「只跑 P0」，連 2026-08-03 才補上的 `plus` 例外一起丟掉。
  作者 2026-08-04 裁示本輪只修 `:130`，`:126` 留待自己的輪次。

- [ ] **id 47 的 all-or-nothing 期望對上一段真的踩到三條規則的文字。** 2026-08-03 補跑單案定位，
  推翻了此前「carve-out 沒構到」的推測——**carve-out 構得到**。runner 明文引用 2026-08-03 新增的
  讓步開場 carve-out 放行 `模糊歸屬`，另主動放行 `對比句式`、`對讀者說教`（「不曉得你們有沒有
  同樣的感受」）與 `推廣語氣／四字評語`。那一輪的修改有效，只是不足以清空。

  該輪實際開火三條，全在 P1：

  | 規則 | span | 2026-08-03 有無處理 |
  |---|---|---|
  | `空降主張` | 每個人都因為 AI 而拉高成品的中位數 | 有；runner 判「沒有前文依據或後文展開」，條件未滿足 |
  | `意義膨脹` | 自然整體的標準就變的更高了 | **無——不在那三條裡，也不在任何既有假設裡** |
  | `情緒宣告` | 有些人在用 AI 的方式令人錯愕 | 有；runner 判「沒交代造成什麼結果」，條件未滿足 |

  而 `expected-behavior` 要求「放行，一個字都不用動」——零 flag，任何一條開火它就紅。

  **開火集合逐輪不同，不是固定的一條。** 六輪 grader reason 顯示 flag 數在 2 到 6 之間浮動
  （r2 是 A 六 B 二，r3 是 A 三 B 六，r6 的 A 標 `空降主張`／`對讀者說教`）。所以下一步不是再補
  一條 carve-out，而是先決定這個期望本身站不站得住：一段同時踩到三條以上規則的真人文字，
  要求零 flag 是不是把保護類的判準訂得比規則集本身還嚴。

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

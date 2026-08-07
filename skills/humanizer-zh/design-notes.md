# Design notes — humanizer-zh

Maintainer notes — provenance and build process for this one skill.

## What this skill is, structurally

A zh-first bilingual skill with **one** canonical rule set. A rule carries both its Chinese and its English manifestation rather than living twice in two parallel catalogs.

```
SKILL.md                      — 114 lines: routing, the six-step spine, the shared vocabulary, severity, profiles
references/
  zh-rules.md                 — all 47 rules under the 8 classes, each with 抓 / 保留 / a before-after pair
  en-rules.md                 — the English manifestations, keyed to the same 8 classes
  hidden-author.md            — the detect-only 作者隱身 aggregate: gate, threshold, 5 sub-signals
  zh-phrase-rules.md          — the seven zh「詞→替換」lookup tables (data, not rules)
  examples.md                 — 6 worked end-to-end scenarios (synthetic samples)
```

[`guide.zh.md`](guide.zh.md) (and its English counterpart [`guide.en.md`](guide.en.md)) is the **user-facing** companion to this file: what the skill does to a draft, why a 公文 report says 「作者隱身不適用」 and still carries five flags, when to reach for `--expect-author`. Keep measurements, provenance and the reasoning behind a split here; keep behaviour-as-experienced there.

## 自我背書 — 第 47 條，過煞車的方式與前兩條都不同（2026-08-01）

來源是作者提供的一句真實工作文字：「邊界判斷表。以下收錄的是灰色地帶，判斷依據皆來自前文的三個結構性因素。」**兩半的來源不同，這一點是本條最有用的資產**：原句是模型生成（語料庫 A-13），而對照句「以下為灰色地帶案例，依前述的三個結構性因素判斷如下」是作者本人親筆改寫（`evals.json` id 75）。同一個語意、同一個作者情境，一邊機生一邊手寫，差別收斂在稽核句與操作句之間。兩句帶的資訊一樣，差別在後半句的職能：AI 版把「怎麼讀下文」的操作句寫成「我的依據很完整」的稽核句，「皆」在防守一個沒人問過的質疑。

**先確認是缺口再開規則。** 掃過 `corpus.md`、`evals.json`、`research/`，`皆來自／均基於／依據皆` 這組形態在 fixture 文字裡零命中——三個 `皆` 全部出現在 repo 自己的註解散文。46 條逐條比對後也沒有家：`文件自述` 抓的是交付物對委託者說話與後設敘事開場（本文將探討…），那是**取代**交付；本條的子句**伴隨**交付，形不同。`避險堆疊` 是反面（不敢斷言，不是過度自證），`懸念與自我貼標籤` 指的是內容聰明而非方法完整。

**煞車是怎麼過的，這一項與 `體裁相稱` 不同。** backlog 的 `體裁相稱` 候選項寫著那條煞車：「兩案不足以立一條規則——先在既有語料裡找同型案例」。這裡作者 1 案、語料庫 0 案，照字面過不了。實際過關的理由是作者當輪直接裁示開規則，不是舉證數達標。**這件事要記著，因為它是這條規則目前最大的弱點**：`語體漂移` 有五輪量測、`體裁相稱` 被同一條煞車擋了一輪，本條兩者皆無。

**保護案三案裡兩案是合成的。** id 75（操作句不是稽核句）是作者親筆，屬真語料；ids 73（消歧義）、74（來源註記）是為了測 carve-out 現寫的。〈判讀 sweep 與衝突複審〉那一節的第四種量測故障已經判定「保護類的整個主張是『這是真人會寫的東西，不准動它』，用造出來的句子去測等於用人味的演出代替人味本身」。命中案 id 72 與保護案 id 75 兩側都是真語料，剩下的兩個合成保護案待替換，記在 backlog。

**carve-out 的重點是消歧義與防守的分界，判準寫成可執行的檢查。** 「拿掉這句，讀者會不會套錯判準？」會就保留。這個問法把一個看起來很主觀的分界變成單一動作——沒有它，方法章節、稽核報告、資料表註記全都表面命中，而那三種文體裡宣告來源與涵蓋範圍本來就是交付物本身。

**沒有寫 `改法` 行。** 手段（把稽核句換回操作句、主詞從名物化的「判斷依據」回到動作）照 backlog 那條「這個手段搬得動嗎」的判別式是**搬得動的**——名物化轉動詞適用於任何句子，脫離本規則的形態仍然成立，與 `語體漂移` 那次外溢同型。方向由前／後對照承載。

## 過度簡寫 / 破碎短句堆疊 的邊界重切（2026-08-01，語體漂移之後）

作者送來一句知識文件開場：「理解後文的干擾機制，需要先具備四個 PostgreSQL 的基礎概念。」它在當時的 45 條裡沒有家。不是 `過度簡寫`——沒有任何東西被截短，子句的每個字都在；不是 `推論鏈斷成連續斷言`——沒有結論詞，也沒有缺席的前提；`語體漂移` 的第一項判準（句末孤懸動詞、賓語在逗號另一邊）也不成立，句末是名詞。缺的是標記這個子句為目的子句的那個連接詞。

**改成按尺度切，不按症狀切。** `過度簡寫` 止於片語：名詞截成單字、名詞片語代替動詞、成分缺席。`破碎短句堆疊` 收下句架與子句關係這一尺度的全部三形態——`推論鏈斷成連續斷言`、`缺連接詞`、`繫詞架構被抽掉`。`繫詞架構` 一併移過去是同一個理由：「照台灣人實際的寫法寫」是句架收不了口，不是詞被截短。第一版把 `缺連接詞` 塞進 `過度簡寫` 當第四個 bullet，結果是兩個尺度住同一條規則，還得在兩條規則各寫一句互指的分野句——按尺度切之後那兩句都不必寫。

**回讀測試是擋住誤傷的唯一機制。** 中文本來意合，關係從語序讀得出來就是對的、不該補，這是這個形態開出來的最大誤標面。只有需要退回句首才重建得出的關係才標。`zh-phrase-rules.md` 的定型列因此每一列都點名讀者被迫退出的那個誤讀（並列非因果、事實非條件、褒非讓步）——只寫「缺所以」的列沒有辦法跟正常的意合句區分開。

**沒有寫 `改法` 行，這是刻意的。** 下一節記著 `語體漂移` 前三輪 NO-SHIP 的成因：它的 `改法` 給了一個具體改寫手段（降格成括號附註），模型把它讀成通用許可，外溢到別的 rewrite 案。`缺連接詞` 的改法手段（補回關係詞）是同一個形狀，而且比括號附註更容易到處套用。需要寫下來的只有 scope 一項，那一項的正確位置是 `SKILL.md`——scope 機制本來就住在那裡，不是規則的 `改法` 行。

**`SKILL.md` 的 scope 列表必須限縮，不能只在規則裡寫。** 該檔把 `破碎短句堆疊` 列在 段落改寫 之下，而它永遠載入、`zh-rules.md` 是 disclosed，不限縮的話補一個「如果要」會被升級成整段重寫，而且會贏。列表現在只點名 推論鏈 形態。這個不對稱是實質的：推論鏈缺的前提根本不在句子裡，補的內容只能從外面來；另兩形態是把一個詞放回一個原本就站得住的句子。

**與 `語體漂移` 的分界寫進 `破碎短句堆疊` 的 抓。** 兩條規則都在句內尺度、都表現為逗號兩邊接不起來，最容易誤掛。判準不同：`語體漂移` 要找句末孤懸動詞與跨逗號的賓語，`缺連接詞` 要找的是兩端俱在而關係詞缺席。`過度簡寫` 保留欄的「公文與法律的標準句架」維持原字不動——下一節記著那是與 `語體漂移` 刻意互指的握手，收窄它會把該放行的形態放進來。

## 缺連接詞 的保留欄收窄（2026-08-02）

上一節寫著「回讀測試是擋住誤傷的唯一機制」，但 `zh-rules.md` 的 **保留** 欄沒有跟著改：它留著「關係從語序一次就讀得出來時不補」這句散文，而 `zh-phrase-rules.md` 的定型表給了 目的／條件／因果／轉折／時序 五列該抓的例子——覆蓋的正是意合最常出現的全部關係型別。兩份檔案因此直接對撞：定型表第三列那句「資料量超過一百萬列，這個查詢會退回全表掃描」，照定型表要抓，照保留欄要放。作者在 backlog 裡把同一句指名為保護案，撞出的就是這個。

**改保留欄，不改定型表。** 五列是工作範例，它們正確；每一列的病灶欄都已經寫了讀者被迫退出的那個誤讀（事實非條件、並列非因果、褒非讓步）。錯的是保留欄把同一個判準復述得太鬆，鬆到讀起來像對全部意合句的無條件豁免。收窄的作法是讓保留欄接回抓欄已有的回讀測試，並把定型表那五種誤讀路徑點名為「沒有讀出來」的判準，而不是新增一條判準。

另一個選項是給定型表五列各加「僅當關係無法從語序讀出」的限定。否決的理由是改動面：五處都要改，而且限定寫在工作範例上會讓範例失去範例的作用——範例的價值就在它不帶條件。

`evals.json` id 85 是這個收窄的回歸樁：兩句都是意合、都沒有連接詞，第一句要抓（前半先讀成已發生的事實）、第二句要放（上週／這週把時序釘死）。把判準讀成「有沒有連接詞」的兩個方向都會在這一案上失分。id 82 走的是沒有爭議的 摘要與條列 carve-out，維持原樣。

**收窄的措辭改了三次，每一次的退步都指向同一個病：列舉會被讀成判準的全部。** 第一版把四條誤讀路徑寫進保留欄，結果保留欄失去豁免的作用——id 47 被以長度為由標記拆句（新臂三輪全紅、基線三輪全綠），id 80 的目的子句反而漏抓。第二版把列舉搬回抓欄、保留欄改寫成排除式（「句子長、逗號多、子句串接密都不是本條的證據，關係詞缺席才是」），id 47 回到與基線同水位，但 id 82 的收尾句「下週把灰度拉到 50%，同時把匯出的排程改版接上」開始被標——`同時` 明明在場，路徑「與後半並列的另一件事」還是打中了。第三版因此在列舉末端加上前置條件：四條路徑都以關係詞缺席為前提，標記關係的那個詞若在場，路徑不成立。

教訓與上一節 `語體漂移` 的 `改法` 外溢同型，但方向相反：那次是手段外溢成通用許可，這次是誤讀路徑的列舉外溢成充分條件。規則文字裡任何一份枚舉，都要自己帶上「這不是全部」與「這要什麼前提」兩句，否則模型會把它當成完整的判定演算法。

**收斂於第三版，r8-r10。** 兩臂均值新版全面優於基線（保護 14.00 vs 15.33、命中 9.67 vs 15.00），id 47 與 id 82 兩根樁都不再出現在失分表上。閘門仍報 NO-SHIP，但十列確認紅裡九列是兩臂同紅的既有缺口；唯一新臂獨有的 `59/expected-behavior` 是 2/3 對基線 1/3，差一輪就打平，訊號弱於它前一輪頂替掉的 id 83（那一列在 r7-r9 是 2/3 對 0/3，加跑一輪後降回 1/3，判為抽樣）。這一輪的數字要讀成「新版沒有比基線差，而既有缺口需要各自的規則改動」，不要讀成過閘。

**新落地的 id 86 三列全部兩臂同紅**（3/3 對 3/3）：casual 語域那段裸斷言＋缺條件標記，兩個版本都整段放行。這是新測出來的既有缺口，不是本輪改動造成的退步——`SKILL.md:126` 的語音自動偵測階梯沒有「社群貼文／個人筆記 → casual」這條路徑，所以規則根本沒被帶到那個語域上。

**六列既有的保護級誤殺記為已知缺口，不擋出貨。** 兩臂三輪皆紅、與本輪改動無關：id 27（`知識截止免責` 抓在沒有模型自指的人工查證但書上）、id 47 的 `expected-behavior`（全案零標記的全有全無期望，跨約三十條規則）、id 61 兩列（`老司機都知道` 的俚語語域與 `意味著什麼！` 的言外之意皆被刪）、id 62 兩列（口號句在兩臂各被歸到不同規則）。機制分三種：抓欄是字面／密度比對而該條沒有對應的 carve-out；carve-out 存在但結構上構不到（保護清單⑥ 需要使用者宣告，而跨規則借用被 `SKILL.md` 明文禁止）；單一期望覆蓋整案所有規則。三種都要各自的規則改動才治得好，不屬於本輪授權範圍。

## carve-out 構得到嗎——八列既有誤殺的一次處理（2026-08-03）

上一節那九列兩臂同紅的缺口，這一輪處理其中兩類（第三類「單一期望覆蓋整案所有規則」不動，那是 fixture 的形狀問題不是規則問題）。**先定位開火規則再改**：grader 的判分理由只記結果，不記 runner 引用了哪一條，所以 61 與 62 是把十輪 results 的同列理由全部撈出來比對才確定的。結果值得記著——**62 的同一句話在不同輪被歸到三條不同規則**（`空話填充`／`意義膨脹`／`零資訊警句與口號`），61 的 `老司機都知道` 則穩定歸在 `模糊歸屬`。一句話會被幾條規則同時掃到，這件事決定了 carve-out 要寫幾份。

**跨規則不能借，所以同一個 carve-out 寫了三份。** `SKILL.md:78` 明文禁止「一條規則底下寫的 carve-out 拿來放行另一條規則底下的片段」。62 那句收束句既然三條規則都會開火，就得在三條的保留欄各寫一次，而不是寫一次再互相指過去。重複是這條禁令的必然成本，不是疏漏——寫成互指等於在規則層開一個 SKILL.md 要擋的洞。

**這一輪全部是保護側放寬，因此需要一個哨兵。** 放寬保護欄的風險是命中側跟著塌，而 aggregate 的閘門本來只盯保護級。過閘條件因此加了一條：命中級每輪 mean 不得劣於基線。這是上一輪 `語體漂移` 的教訓的反面——那次是 `改法` 外溢傷到保護側，這次要防的是 carve-out 外溢傷到命中側。

**唯一動 抓 而非 保留 的是 `知識截止免責`。** 它的 抓 原本是字面比對（「由於資訊有限，無法確認…」），而那句話人也會寫——人也會查不到。改成要求模型自述標記在場才算，判準從措辭移到自指。改前先確認命中案 id 58 帶了兩個標記（`截至我最後更新的資料`、`我無法瀏覽網路`），命中側不會塌。

**id 86 的修法在 `SKILL.md` 而不在規則。** casual context 原本是 P0 only，`破碎短句堆疊` 是 P1，所以規則根本沒被帶到那段文字上——寫多少 carve-out 都沒用。改成 casual 點名放行本條一個例外。沒有把本條升級成 P0：P0 的類別語意是「機械指紋與信任殺手」，塞一條句法規則進去會稀釋那個定義。

**那個修法補錯了軸，86 因此沒清掉。** `casual` 這個詞在 `SKILL.md` 出現兩次，分屬兩條獨立的軸：Context 決定壓力多大，Voice 決定聽起來怎樣。例的 prompt 宣告的是 `voice: casual`，而 Voice 的 `casual` 描述裡就寫著「short sentences」——模型拿的是那一句當放行依據，補在 Context 那行的例外條款構不到。真正的洞不是少一條例外，是**沒有任何一句話說 Voice 不授予規則豁免**，兩條軸同名同值時讀者沒有理由分辨。留在 backlog，因為修法屬於軸的語意宣告，不屬於 carve-out 這一輪。

**放寬 carve-out 之後，D1 的教訓原封不動地重演了一次。** 第一批三輪把九列缺口全清了，卻開出三列新臂獨有的紅，而三列的病因同一個：**carve-out 裡的列舉被讀成窮盡**。`破折號濫用` 的 rewrite 保真句只點名破折號寬度，模型就把保真讀成只管破折號，半形逗號、逗號前後的空格、句末缺句號照樣正規化（id 60）；`推廣語氣` 的保留欄放寬之後基礎放行率整體升高，連完全沒有具體內容的純推廣貼文都被豁免（id 22）。改法是給兩處各補一個前提句——保真涵蓋標點與空白整體、破折號只是其中一例；每一項放行都要求它所指的東西引得出原文。第二批三輪這三列全部翻綠，保護 mean 5.00 對基線 16.33，命中 10.00 對 13.00。**D1 那條「列舉必須自帶『這不是全部』與前提條件」是通則，不是 `缺連接詞` 一條的特例**，寫任何 carve-out 都適用。

**收工狀態：47 與 86 仍兩臂同紅。** 47 三輪皆紅且基線同樣三輪皆紅，這一輪的三處 carve-out（`模糊歸屬`／`空降主張`／`情緒宣告`）沒構到它；86 新臂 2/3、基線 3/3，新臂略優但未離開 confirmed。兩列都是 main 自己也有的既有缺口，不擋這一批出貨，各自留在 backlog。

## 語體漂移 — 一條 provenance 判準被拆成 surface 判準 (2026-08-01)

規則的來源是作者提供的一句真實工作文字：「預期產出與時程：助教人力配置方案與 Lab 支援範圍，訪談後 3 至 4 週內取得。」句法上它同時想當條列標題與完整句子——前半名詞組無謂語，唯一的動詞卡在句末、跨過一個逗號回頭管前面的賓語，中間沒有任何授權前置的標記。

**作者原本要編碼的判準有三項，只有第一項照原形進了 skill。**

第二項是「缺陷與完成度不匹配」：人的失誤是減法（漏字、漏主詞、標點不一致），AI 的失誤是骨架歪掉但零件樣樣俱全，因此組裝感與高完成度同時出現才是決定性訊號。這句話問的是**誰寫的**，而 `SKILL.md` 的〈What this skill is and isn't〉明文只判 surface、不判 provenance。照字面寫成命中門檻，skill 就開始做它拒絕做的主張。處置是把它翻面：**組裝感伴隨完成度下降時放行**，寫進 `語體漂移` 的保留條款。非母語寫作、翻譯體、多來源剪貼因此照樣被保護，而規則一句話都沒說作者是誰。`backlog.md` 的 (H) 雙軸評分閘沒有放行，仍等盲測資料。

第三項是「結構訊號權重高於內容訊號」。它不屬於任何單一規則——內容可以從表格、模板或來源文件繼承，語法是當場生成的——所以落在 `SKILL.md` 步驟 4 的一行，而不是自成一條規則。

**判準本身沒有證據支撐，這一點要說清楚。** 三項判準全部出自 2026-08-01 一場非盲測的 annotate session：判讀者知道答案，中途又拿到一份人寫的對照改寫。落地的理由是第一項屬 surface、可由既有的 run-case 儀器直接量測，不是那場 session 證明了什麼。

**量測：五輪，前三輪 NO-SHIP，拿掉 `改法` 之後的 r4／r5 過閘。** 數字在 `evals/results-2026-08-01-drift-aggregate.md`。規則抓得到目標——ids 67、68 的命中列三輪都是新版過、2.1.0 落空，vanilla 對照也是 17:8——但保護類平均從 104 掉到 100.7，且 `64/全域:不代筆` 三輪皆失、`64/全域:保真` 兩輪失。兩者同因，而那個因很值得記著：**規則的 `改法` 寫了「降格成條目：時程降級成括號附註」，模型把它讀成了通用許可，在別的 rewrite 案裡也開始加括號編註**。一條寫給單一規則的改法手段，會外溢成整個 rewrite 模式的習慣——這是 `改法` 行第一次被觀察到有這種作用域外洩，下次寫任何 `改法` 都要把手段綁在該規則的形態上。

**r4／r5 的處置有三項**：拿掉 `改法` 行、id 68 的 fix 列改成只要求指向單一語體、id 57 的 key 依作者裁決放行「質疑結論依據」。之後連續兩輪新臂的保護與命中都勝過 2.1.0（保護 105/104、104/103；命中 62/57、61/59），new-only 的保護失分兩輪零重疊、無 2-of-2 確認列，**2.2.0 ship**。三項裡最值得記住的是第一項的效果量：`64/全域:不代筆` 從三輪全失轉為兩輪皆過，只因為刪掉那一行。

**保護側的失分每輪換一列，這件事本身是訊號。** r1 掛 id 70 的兩列、r2 掛 id 69 的欄位案、r3 掛 id 69 的另一列，改一次規則文字就換一個位置，沒有一列 2-of-3。單輪不足以定位一條新規則的誤判面，這是 aggregate 規約在這輪的第二個實例。

**邊界。** 與 `過度簡寫` 的分界是缺零件 vs 零件齊全而語體沒選定（該條的保留欄含「公文與法律的標準句架」，會直接放行本規則要抓的形態，所以兩邊互指）；與 backlog 已立案的 `體裁相稱` 候選規則的分界是句內 vs 篇章級語域。

## 文體類 and the two carve-out lists (2026-07-30)

The genre axis exists to gate exactly one rule, `作者隱身`, and nothing else. Three defects were fixed together in this round, all of them the same disease — a distinction stated in one file and contradicted in another.

**The flag's semantics were never settled.** `structure-signals.md` said `--structure-signals` was an override that forces the audit on any genre and reports anyway; `evals.json` ids 13/14 said the same flag must NOT trigger the audit on a 事務文體. Three graders scoring the same runner output reached three verdicts because the instrument and the skill disagreed, not because the runners differed. Resolved by making the flag a *genre declaration*: `--expect-author` sets the verdict to 署名文體 and the audit then runs normally, so there is no "ran it but everything found is genre-correct" state to describe. ids 13/14 dropped the flag from their prompts and became pure gate-default protection cases with their expectations untouched; ids 55/56 carry the identical text plus the flag, so the flag is the only variable between the pairs.

**The exclusion read as a blanket pass.** Nothing stated that the 事務文體 exclusion covers one rule, and the only worked 公文 example in the skill (`examples.md` 例 2) ends 「未發現須修改之處」. Every available signal pointed at 公文 → 沒事. Fixed with an explicit routing conditional in `hidden-author.md` (〈The exclusion stops here〉), a one-line restatement in `SKILL.md` step 1, and `examples.md` 例 3 — same genre, same mode, opposite outcome.

**`立場真空` and `作者隱身` had copy-pasted carve-out lists.** They should never have matched. 立場真空 asks whether the author exercised *judgement*; 作者隱身 asks whether the author is *present*. A 建議書 owes the reader the first and not the second, so 規劃書/建議書/計劃書/investor-email now sit inside 事務文體 (no 作者隱身 — a formal proposal has no colloquial breaks or rhythm variation by construction) while being removed from 立場真空's shorter carve-out list (a proposal that recommends nothing is exactly what that rule is for). 公文/簽呈 stay in both lists: the 擬辦 line is that genre's form of taking a position.

**Naming.** `結構級訊號` → `作者隱身` and `voice-bearing/voice-neutral` → `署名文體/事務文體`, on the maintainer's report that the old terms were unreadable. Two constraints shaped the result. The genre term must not imply a lower bar — 「不需要人味的文體」 was rejected mid-round for exactly that, since plain wording persuades in a way jargon does not, and it would have persuaded readers that a 公文 needs no de-AI-ing at all. And the rule name must not collide with the genre name: 隱身 (by design) belongs to one of them only, which is why the genre moved to 署名/事務 rather than the rule moving off 隱身.

**Default trigger.** `作者隱身` previously needed a routing condition (user complains the draft reads machine-written) *or* the flag, and then the genre gate on top. Two layers written in two files, and the net effect was that the check was off by default for an ordinary blog audit. Collapsed to one: the genre verdict is the whole trigger. Rejected alternative — running it everywhere unless explicitly excepted — would invert the skill's largest false-positive guard and break the zero-tolerance protection bar; the 2026-07-17 row below measured 事務文體 誤啟用 at FP 2/2.

**The split rule.** `SKILL.md` holds what every branch needs; a reference file holds what only some branches reach. Language selects `zh-rules.md` or `en-rules.md`; the 作者隱身 route selects `hidden-author.md`; rewrite mode reaches `examples.md`. Pointer *wording* is the reliability risk, not pointer targets — if disclosed material under-fires, sharpen the pointer before pulling anything back inline.

## The 2.0.0 rewrite (2026-07-29/30)

1.5.0 was a fork of the English-only `avoid-ai-writing` by Conor Bronsdon, with a zh layer bolted on. It reached 966 lines against a 500-line ceiling and carried ~79 named rule surfaces, roughly half exercised by neither test instrument; 46 of 51 English headings had no 繁中 twin. At the same time 14 of 42 tagged eval cases were marked `（缺口`— no rule existed for them, so they passed vacuously. Overgrown and under-covered at once: re-carving fixes both, trimming fixes only one.

2.0.0 deletes the inherited English catalog and `references/english-phrase-rules.md` outright, ends the fork relationship (the directory `LICENSE` and the upstream `metadata.author` go with it), and rebuilds on `corpus.md`'s own **8 defect classes + 2 orthogonal mechanisms** — a taxonomy that was already tagged on all 32 corpus cases and 42 of 54 eval cases before the rewrite started, so the test data did not have to be re-invented to fit it.

**Sequencing that mattered:** taxonomy first, re-tag the test data, then write prose. Re-tagging touched labels only — every `flag`/`ok` verdict, every quoted span and every prompt stayed byte-identical, because a changed verdict silently rewrites the baseline and destroys the A/B.

**Consolidations worth remembering.** `作者隱身` had three surface forms and `打破第四面牆` two; sub-signals are now always written `作者隱身／<name>` and never as sibling rules. Two English/Chinese pairs turned out to name one defect each — `全文無立場` ≡ `Missing first-person perspective` → **立場真空**, and `只解釋不造像` ≡ `no original metaphor` → **只解釋不造像**. The old `Rhythm and uniformity` label was doing two unrelated jobs (genre uniformity in a spec vs voice absence in a blog); those separated into **節奏均質** and **立場真空**.

**Rules that did not survive:** curly quotation marks, immaculate typography in casual registers, wall-of-text replies, title-case headings, hyphenated-pair overuse. Each was either a pure false-positive surface, an English orthographic nit with no zh applicability, or already covered elsewhere. Roughly thirty further names were *merged* rather than cut — each is named as a form inside its new parent's trigger, so the detection knowledge survives even where the heading did not.

## No runtime scripts — a deliberate, revisitable decision

A phrase-scanner script was considered and rejected. Evidence: no runtime detection script exists in any of the four surveyed humanizer/skill projects; Codex's own guidance prefers instructions over scripts unless determinism is required; and this skill's observed failures are all judgment-tier, not lookup-tier, so a word-list scanner would not have caught them. `uv` is also not a safe runtime assumption — it is preinstalled only in Codex cloud images, not on a developer's machine.

Revisit only if a real 詞表層漏抓 shows up in the evals. Dev-side tooling is a different question and is welcome: `tools/check-labels` ships with this round.

## External sources drawn on

Attribution obligations are recorded in `NOTICE`; this section is the *why*.

- **speak-human-tw** — https://github.com/Raymondhou0917/speak-human-tw (MIT). Three separate uses, deliberately distinguished: (1) the 翻譯腔 entries in `zh-phrase-rules.md` are our own rewrite informed by its `taiwan-localization.md`; (2) `evals/evals.json` ids 15–54 are a *verbatim* adaptation of 40 of its 42 benchmark cases, with added structural fields — a different kind of use, so it gets its own NOTICE line; (3) the six-step procedure and the 保護清單 mechanism follow its design. SF-14/SF-15 (中國用語／半形標點) were excluded as `avoid-china-writing`'s axis.
- **blader/humanizer** and **x-humanizer** (both MIT) — pattern inventories distilled for `en-rules.md`. Conceptual distillation, re-classified into the 8 classes and rewritten; no prose copied.

## Research notes (dev material, not runtime)

`research/` holds faithful distillations of outside source material for authoring reference. **Dev/authoring material, not runtime** — they carry provenance headers and source citations, and must not be surfaced into `SKILL.md` or `references/`. If a distillation later informs a shipped rule, promote a provenance-stripped extract into the rule body and add attribution here and in `NOTICE`.

- **`research/ai-sentence-patterns-zh.md`** — distillation of 朱宥勳〈對「AI腔」厭煩了嗎？〉(YouTube, 2026-01-30). Centres on 「這不是⋯⋯而是⋯⋯」— now covered by **對比句式**.
- **`research/wikipedia-ai-signs-zh.md`** — distillation of Wikipedia's AI-writing signs.
- **`research/research-humanizer-landscape-2026-07-29.md`** — primary-source survey of Anthropic skill-authoring guidance and three humanizer projects; the basis for the no-runtime-scripts decision, the `research/` vs `references/` placement rule, and the two-layer examples design.

## Test instruments

Three files, none replacing another:

| file | answers |
|---|---|
| `evals/corpus.md` | on real text, which span should be flagged and which must not |
| `evals/evals.json` | given a prompt, does the skill behave as expected |
| `evals/judged-cases.md` | why a given rule is shaped the way it is |
| `evals/annotations.json` | what the author judged, case by case — the ledger `judged-cases.md` renders from |

`tools/check-labels` validates both instruments against the rule names the skill actually declares (derived from `zh-rules.md` headings and `hidden-author.md`, so there is no separate manifest to drift), plus the corpus 解析契約 — every 引文片段 must be an exact substring of its clean quote, `全文` excepted. Since 2026-07-30 the extraction is declared in `evals/label-check.json` rather than hardcoded in the tool, which is also what makes the gate opt-in for other skills; that file names the *files and regexes*, never the rule names, so the no-drift property is unchanged.

### tools/annotate — 判讀儀器的設計選擇（2026-08-01）

把「這句有沒有 AI 味」問給作者、把答案存成可重跑資料的工具。它存在的理由是成本：一輪
sweep 要判 36 案，逐案手抄進散文檔的謄寫稅高到讓 sweep 停擺過一次。實作與最初的構想有幾處
差異，每一處都是可能被後人「修正」回去的，所以記在這裡。

**判讀先進帳本，`judged-cases.md` 由帳本渲染。** `evals/annotations.json` 是機器可讀的真相
來源；散文檔末端一個 `annotate:begin/end` 圍起來的區段從它渲染而來，marker 外一個 byte 不動。
續跑狀態只讀帳本——散文檔沒有機器可讀的 case id，任何解析器都會在有人重排標題的那天開始
靜默漏案。

**判讀是 1-4 的 AI 指數，不是有／沒有。** 原始設計寫的是兩個按鈕；第一次判讀時作者自己就伸手
要了一個程度（「AI指數70%：過分空虛的形容詞…但不排除人也會這樣寫」），二元裝不下那句話。
四個固定錨點（1 偏人／2 不確定／3 偏 AI／4 明確 AI）隨每張卡一起印——36 案會跨 session 判，
沒有錨點的量表在第一次與第五次之間會漂移，而漂移過的分數無法跨案比較，那正是量表相對二元的
唯一收益。

**錨點刻意不對稱**：人側一級、AI 側兩級。這支儀器問的是 AI 味有多強，解析度值得花在 AI 端
——「明確人寫」與「偏人」對任何下游讀者都是同一件事，而「偏 AI」與「明確 AI」分開的是規則
該抓與必須抓。**2「不確定」回傳 `null` 而非 `false`**：不選邊不是同意，記成同意會讓一堆真正
判不出來的案讀起來像答案卡的健康證明。

**比對的是命中／保護類別，不是 `expected-direction`。** 那個 slug 只是 `run-case.json`
`verdict_class.overrides` 的一個條目，多數 case 不帶它，照字面無法實作。代價要記著：ids 1、2、
6、7、8、9 的計分列橫跨兩類又沒有 `bucket` 可據，這六案只記判讀、不做一致性比對。

**理由 3/4 必填、1/2 選填。** 指向 AI 的判讀是規則寫作的依據，必須說出看到什麼；1 偏人與
2 不確定是訊號的缺席，逼一句話出來只會產出一年後讀起來像證據的填充物。

**`--card ID` / `--record ID` 是給 agent 驅動用的兩道門。** 互動迴圈本來就是呈現、收答、落帳
三段；agent 相容不是移植 UI，是把三段拆開讓 agent 當啞管道。`--record` 重跑 `build_card`
驗證後才落帳，從不信任呼叫端上一次 `--card` 的輸出。tty 閘只繞這一條。

**單檔 1038 行是刻意的**（`check-labels` 的 395 行是這個 repo 的實質上限）。其中 153 行空行，
其餘大半是記錄反例的 docstring——ids 45/48 把引號放在規則名裡、ids 31/41 引文內有巢狀引號，
這兩組正是「span 抽取不能用 regex」的證據，而它們都不在 sweep 目標裡，砍掉不會立刻被發現。
五個關注點（config／extract／ledger／render／loop）一條線讀得下來，拆 package 還要連帶改名
（`tools/annotate` 與 `tools/annotate/` 撞名）。

**三案（ids 2、4、12）的 prompt 形狀無法在不洩題的前提下剝乾淨**，標為 needs-manual、不進判讀
流。這份名單是 fixture 不變式——它一變就代表有人改了 prompt 形狀，剝離邏輯要重讀。

### 兩個 namespace，一個白名單（2026-08-02）

閘從 `1ec104a` 起連紅三個 commit，8 個 FAIL，兩個成因的共通點是**名字都合法，只是沒有宣告的地方**。修法各自長一層，而不是把名字塞進 `names` 常數：

`改寫保真` 是**跨規則的期望類別**——它要求的是輸出不得漂移，與哪一條規則命中無關，所以沒有 `###` header 可derive。塞進 `names` 等於宣稱它是一條規則。改成 config 的 `expectation_classes` 獨立宣告，`resolve()` 兩個 namespace 都查，但查不到時報得出它該從哪裡來。另加一道 overlap 檢查：同一個名字不得同時宣告為規則與期望類別。

`四字評語` 在 `zh-phrase-rules.md`，而那個檔的 9 個 header 只有這一個當規則名用。整檔納入 `sources` 會把「台灣用語偏好」「AI 慣用詞替換」一起收進 canonical——`resolve()` 是精確比對、刻意不做寬鬆匹配，混進去的名字會讓別處的錯字變成合法標籤。改用**白名單 regex**（`^## (四字評語)`）：之後要加名字就得改 alternation，那個顯式編輯正是白名單的重點，不是它的麻煩。

規約沒有變寬：canonical 65 個名字，`zh-phrase-rules.md` 的另外 8 個 header 逐一驗過皆被拒，`改寫保真x` 這類錯字端到端仍然 FAIL。

### corpus 的判定欄從零資訊到帶資訊（2026-08-01）

原始狀況：真人桶全是 `ok`、AI 桶全是 `flag`，判定欄可以完全由桶別推出來。那一欄因此不帶任何
資訊——量到的只有「skill 在真人文上安不安靜、在機生文上吵不吵」，量不到「skill 在**同一個桶
內部**分不分得出好壞」。

**規約沒有打架，是一句話寫得不精確。** 版權註記講的是桶別歸屬（不因 skill 標了它就把真人文
改判成 AI 文），與判定欄該填什麼無關；判定表規約寫 `flag`＝確實該標，`整篇判定` 格式也明文
允許 flagged。錯的是兩個桶的開頭句——「被標的比例越低／越高越好」把「skill 標了什麼」與「人工
標註認為該不該標」混為一談，已改寫成分開講 FP 與 FN。

需要的是判定欄與桶別不一致的例子，**最有力的形態是同一份文件、相隔數段的兩個樣本，措辭密度
相近而只差在褒詞後面有沒有接上可查數字**——skill 若在這兩段給出同樣結果，那它判的是體裁或
作者，不是文字本身。第一次備好這樣一組用的是 2009 年交通部觀光拔尖領航方案核定本，作者當日
決定**移除所有政府計畫書語料**（該體裁空泛文字太多，會混淆判斷），同日改用林端〈台灣律師階層
研究〉補回：H-23 取口語破格段（整篇 `clean`）、H-24 取結語（整篇 `flagged`，3 個 `flag` 列掛
四字評語／抽象claim缺交付／避險堆疊）。

兩個方向的不一致現在都存在——真人桶 24 例、69 `ok` ＋ 3 `flag`；AI 桶 13 例、38 `flag` ＋
2 `ok`——桶別不再推得出判定欄。**下一步不是補更多不一致，是跑一輪看 skill 在 H-23／H-24 這
一對上給不給得出不同結果**：給出同樣結果就證實它判的是體裁或作者而非文字本身。

### 正式文件語料的第二、第三份（2026-08-02）

H-23／H-24 出自同一份報告、同一位作者（林端，法社會學），所以 H-24 那三個 `flag` 到底是這個體裁的通則、這位作者的筆法，還是鄰句有沒有著落，量不出來。補進兩份國科會成果報告全文換掉這兩個變因：H-25（黃慕萱，圖書資訊學）換作者、H-26（鄧成連，設計管理／工業設計）同時換作者與學門。

H-25 的價值在它與 H-24 共用同一個四字語而判定相反：H-24 的「相輔相成」後面沒有寫出兩個計畫如何互相援引，H-25 的「相輔相成」前面就把兩種指標各自的貢獻寫完了。這一對把判準釘在鄰句的著落上，而不是那四個字。

H-26 帶進兩組本檔原本沒有的保護：宣告過的比喻系統（醫學比擬，該報告自己在同段寫明），以及兩個真人筆誤（「診計診斷」的順序顛倒、「進乙步」的同音誤植）——後者是本檔第一則以錯字入桶的例子。

判定欄是待作者複核的：語料合不合用、每一列判得對不對是品味判斷，agent 只負責逐字節錄與標出處。

## 判讀 sweep 與衝突複審：最大宗的問題出在儀器，不在 key（2026-08-01）

36 個移植自 speak-human-tw 的案例（ids 15/16、18–20、22–27、29–37、39–54）全數盲判完畢，
分數分布 1 偏人 ×13、2 不確定 ×6、3 偏 AI ×9、4 明確 AI ×8。與 key 相左 13 例，分成方向
相反的兩群：**key 抓太寬 6 例**（ids 23、27、31、33、35、37——作者判 1 偏人而 key 屬命中類）、
**key 放太鬆 7 例**（ids 41、43、45、47、52、53、54——作者判 3-4 偏 AI 而 key 屬保護類，
全部是改編自 upstream 的保護案）。

**解盲複審的結果與設計這一步時的假設相反，這是整輪最值得帶走的東西。**

| disposition | 數 | ids |
|---|---|---|
| `case-wrong`（這個 case 測錯東西） | 6 | 31、33、35、41、43、47 |
| `judgment-wrong`（作者改判，key 站得住） | 4 | 23、37、45、52 |
| `key-wrong`（key 該改） | 3 | 27、53、54 |

複審被設計出來時，`key-wrong` 被寫成「複審存在的理由」。實際上最大宗是 `case-wrong`——
**近半數的「衝突」不是判讀與 key 的分歧，是量測方式本身有問題**，而那六案沒有一案是改 key
修得掉的。

**四種量測故障，前三種修在儀器設定、`evals.json` 的 key 一個字沒動：**

1. **判準根本不是 surface**（ids 31、33）。31 測假引用（查無此數據、偽託語錄），33 測空洞
   前景段——都該抓，但**人也完全寫得出假引用與空話**。`SKILL.md` 的 surface／provenance 分野
   在這裡有第二個推論：不是每條規則都在量 surface，而拿 AI 指數去校準一條不量 surface 的
   規則，量出來的東西沒有意義。
2. **粒度錯配**（id 35）：卡片呈現整段、key 只指其中兩句。整段偏人與那兩句空洞可以同時成立，
   `contradicts_key` 卻記成分歧。凡是「段落裡只有部分該抓」的 case 都有這毛病，不只 id 35。
3. **兩種保護被混為一談**（ids 40、41、42）。保護類有兩種完全不同的理由：「這段沒毛病所以
   放行」與「這段不准動，就算有毛病也不准」（價格與優惠碼、具名見證原話、退費承諾）。後者
   判 4 明確 AI 與 key 成立完全可以並存，因為 key 主張的不是它沒有 AI 味，是它不可改寫。
4. **合成語料撐不起保護類**——這一項修不掉設定，是語料工作，仍開著（見 backlog）。

前三項落地為 `run-case.json` 的兩個宣告：`ai_index_not_applicable`（照常出卡、照常收判讀，
但 `contradicts_key` 記 `null`，不進一致性比對）與 `verdict_class.no_touch`（`key_classes()`
回 `保護-禁動`，不參與比對）。理由隨宣告寫在 config 裡，不寫在程式。

**時序是硬約束，不是偏好。** 複審必須等整輪 sweep 關閉才能開始：作者一旦在途中看過幾份 key，
剩下的盲判就在對答案卡做 pattern-match，而盲判正是這支儀器唯一的產出。backlog 裡 (I) 引出器
與判讀輪次互斥是同一條規則的另一個實例。

**複審卡是另一個 card builder，不是 `build_card` 加旗標。** 盲判卡是一組防洩題的 fail-closed
閘；複審卡存在的目的正是把 key class、expectation、規則名連同作者自己那筆盲判全部攤開。共用
一條路徑遲早會有人把 expectation 漏進盲判卡。落帳形態是同一 `case_id` 多筆：複審筆帶
`pass: "review"` 與 `disposition`，盲判筆填 `superseded_by`，一筆未刪。**產出是三選一的處置，
不是重打分**——純粹重打一次 1-4 分會把「作者維持原判」與「案子該退場」記成同一筆。

**三個尚未成規則的收穫，這是 sweep 真正的價值，不是相左計數。** 後半群的理由反覆指向三件事：
短句堆砌（43、45、52）、太生硬（41、53）、**體裁錯配**（53「部落格應更強調連接詞」、54「小說
OK，電子報就很怪」）。第三個判的不是句子本身，是句子與宣告體裁的不相稱，而當時 45 條規則沒有
任何一條問這件事——它是新規則的候選而非既有規則的 carve-out，仍在 backlog。

**這輪修掉的一個真 bug**：span 抽取用 `strip("「」")` 剝界定符，會連帶吃掉以巢狀引號結尾的
內層 `」`（id 31「…愛因斯坦也說過：「複利是…第九大。」」少一個收尾），等於拿一段 fixture 裡
不存在的文字去問作者。改成剝頭尾各一字元。已記的判讀 digest 無漂移。

## evals.json 的結構修補（2026-07-30 → 2026-08-02）

儀器自己的缺陷，分兩批。每一項都動 key，而動 key 就要求兩個版本一起重跑基線、aggregate 的
rounds 也得從頭再跑——所以整批一起落地再一次 re-baseline，分開做等於重跑數次 aggregate。

**2026-07-30 的 54-case run 找出三個結構缺陷**（該輪刻意凍結儀器，讓 skill 的修法與基線可比），
2026-08-01 落地：

1. **命中類與保護類被切在不同 id 區間**——c3 全命中、c5/c6 全保護，沒有任何 chunk 同時測兩個
   方向，一個什麼都不標的退化 runner 在 c5+c6 拿 25/25。修法**不重編 id**（重編會孤兒化
   `annotations.json` 整本帳）：`chunks` 改支援 `{"ids": [...]}` 顯式集合，重排成每 chunk 兩向
   兼具（5/5、4/5、6/4、7/3），flag-nothing 與 flag-everything 兩種退化 runner 在每個 chunk 都
   必然失分。range 形式照舊；顯式集合點名不存在的 id 是硬錯誤。
2. **12 個 detect 案帶著 rewrite 措辭的期望**（「改成」「全清」「刪掉」），無法照字面對 detect
   輸出核對，逼 grader 用軟尺。改成報告可查核的措辭（「報告指向／點名…」）。
3. **單一 slug 綁 2–3 個獨立要求**（id 34 同時要 prose 化與具體細節），二元計分把「做了一半」
   讀成完全落空。11 條全數拆開（15、16、19、30、32、34、35、36、37、39、57），拆出的保護向要求
   用 `no-`／`preserves-` slug 自帶類別——順帶讓多數命中案在案內就有保護列，與第 1 項互補。

**id 27 從命中翻成保護（2026-08-01）。** 「由於資訊有限，無法確認該工具最新的定價方案」——
`知識截止免責` 是 P0，而 P0 的門檻應該是「讀者看到就不信任整份文件」，一句沒有主詞的謹慎語
達不到。規則文字未動，動的只有 key；依 id 28→57 的先例補 **id 58** 維持命中側覆蓋（「截至我
最後更新的資料」「由於我無法瀏覽網路」——真正的模型自述標記）。與 id 17（`模糊歸屬`）、id 37
同族：規則抓到真缺陷，但那缺陷不專屬 AI。

**2026-08-02，三條規則各補齊缺的那一側：**

- `口語化萬能詞` 2026-07-30 從動詞擴到名詞與短語之後，兩側都沒有量測。命中側加在 **id 7 自己
  的 key**——「安裝有兩條路」本來就在那個 prompt 裡，也正是規則自己的對照句，缺的只是沒人把它
  寫進期望。保護側 **id 76**（`voice: casual`，三個表面命中靠語域放行）與 **id 77**（宣告園藝
  比喻系統的署名文體）。**id 77 兩個方向寫在同一案是刻意的**：只驗「宣告過的比喻不被標」證不了
  carve-out 的範圍，一個把宣告讀成整段豁免的 runner 照樣全過，所以同一段裡放一個宣告沒涵蓋的
  「兩條路」，它仍須被標——carve-out 只有在鄰近一個它不涵蓋的片段仍然命中時才算驗過。這兩案
  是合成語料而不牴觸上一節第四種量測故障：那一項說的是主張「這是真人會寫的東西，不准動」的保護案需要
  真語料；76/77 主張的是**宣告的語域與宣告的比喻系統會不會抑制規則**，測的是機制，而宣告本身
  就是 prompt 的一部分，真語料帶不進來。
- **id 78**：rewrite 模式的口語時間表達保真案。起因是 2026-07-30 那輪 id 40 的 runner 把
  「3/31 晚上 11:59」正規化成「3/31 23:59」——detect 模式下無害（文字沒動、判定成立），同一個
  反射在 rewrite 模式就是保真失敗。案子裡配了兩條真的要改的 AI 味，保真列才不會靠「什麼都不做」
  過關：原地不動的 runner 應該在命中列失分。
- `破碎短句堆疊` 的 case 數原本是 0（對照：`語體漂移` 落地時配 13 案），而 2026-08-01 的邊界
  重切又把兩個形態搬了進來，等於一條沒有儀器的規則上面又疊了一個新的誤標面。命中側補
  **ids 79、80、81** 三形態各一（推論鏈斷成連續斷言、目的子句抽成裸動詞片語、繫詞架構被抽掉），
  **id 81 兼作邊界重切的回歸哨**——它要求該片段掛 `破碎短句堆疊` 而非 `過度簡寫`，還在用舊歸屬
  的 runner 會在那一列失分。保護側是 **ids 82、85、86**（分別走條列 carve-out、意合分界、casual
  語域）。**三處 label 逐處查過都跟著邊界搬了**：`evals.json` 剩下的兩處 `過度簡寫` 都是
  carve-out 引用而非歸屬、`corpus.md` 三處全是 `ok` 列的放行理由、`zh-phrase-rules.md` 的定型表
  只剩「術語不誤傷」掛 `過度簡寫`。跑之前先逐處確認，否則量到的會是 label 沒對齊而不是行為變差。

**保護類的合成語料替換（2026-08-01）。** upstream 自己聲明「所有用例皆為合成文本」。命中類
不受影響——句子帶著要抓的毛病就成立，誰造的不重要；**保護類的整個主張卻是「這是真人會寫的
東西，不准動它」**，用一句造出來示範人味的句子去測，等於用人味的演出代替人味本身。

**id 47** 換成作者指定來源裡一段已發表的電子報文字，逐字節錄未改寫。它帶著合成語料造不出來的
東西：一個真錯字（「變的」）、三處逗號串接、句中毫無預告地轉向讀者（「不曉得你們有沒有同樣的
感受」）、褒貶急轉。key 同步拆出 `no-typo-correction`（錯字不在本 skill 職權內，代改等於動了
作者沒授權的東西）與 `no-run-on-splitting`。原盲判與複審兩筆自動標為 stale，帳本一筆未刪——
引文換了，舊判讀對應的是舊文字，這正是 stale 欄位存在的理由。

**id 43** 換成同一來源的一則三段並列實測短評。它比合成排比強的地方在於**三段各自帶不同結論、
而且一負兩正**——湊工整的排比不會這樣寫。key 因此多了 `preserves-negative-verdict`（不得為了
語氣一致把「網頁設計功力不行」改中性）與 `no-idiom-flattening`（「表現不俗」「可圈可點」各自
帶評價方向，換成「不錯」會抹掉作者的評測語域）。

同批另進五案，全部標明出處、逐字未改寫：**id 59**（有論證墊底的反問與斷言不得判成立場真空／
空降主張，帶進 `preserves-rhetorical-question` 與 `no-punctuation-normalising`）、**ids 60、61**
（社群，rewrite 保真）、**ids 62、63**（台積電 2021 年報，detect 保護 ＋ rewrite 保真）。年報
這條線的挑選準則是**發布於民國 111 年、早於生成式模型普及**：正式文件的體裁語域本來就最像 AI，
用 2023 年後的企業文案當保護類錨點，來源本身就不乾淨。它撐起的保護主張是體裁要求的東西不是
AI 味——全稱重複六次是年報要求的指涉精確、「成功的關鍵就在於協助客戶獲得成功」是商業模式陳述
不是勵志口號。id 63 另外咬住兩種寬度不同的破折號（—與－），那是原件的排版樣貌，不在改寫職權內。

**id 59 是新增而不是拿去改寫 id 52，這個分別要記著**：52 記下的病灶是「工具名被抽成 A／B 代號」，
要修它得要同型的真材料——真人寫的條件式工具建議。拿一段形狀不同的真語料去蓋掉它，等於用換題目
的方式讓病灶消失。

**`翻譯腔` 明文排除機翻做為保留理由（2026-08-01，作者當輪要求）。** 規則現在寫明：一段文字是
機翻還是人寫但受英文影響，不改變判定——三個檢查（回譯成流暢英文／中文是英文的影子／台灣同儕
不會這樣講）兩種來源都判得動，被懷疑是機翻不是 carve-out。這是真的行為變更（規則文字動了），
所以會 re-key 任何依賴舊沉默的案子。**汙染要記著而不是藏起來**：它落在 sweep 的 id 47 與 id 49
之間，前 30 案沒看過這個改動、後 6 案看過——那 36 個判讀不是可以互換的同質資料，pre-/post-47
的分界是要帶著走的事實。

## run-case 量測設定 v2：baseline bank、3-chunk、same-call 空實驗（2026-08-05）

`tools/run_case`（跨 skill 共用的閘工具，不是 evals 內容本身）換了一輪量測設定，記在
`evals/regression-protocol.md`。三個變更同時落地，且互相影響出貨判定的門檻，所以是
一個量測設定，不是三個獨立補丁：

- `evals/run-case.json` 的 chunk 從 6 併成 3，規則 blob 每輪重送的次數減半。
- `tools/run_case/dispatch.py` 的 codex runner reasoning effort 從 `xhigh` 降到
  `high`。
- 新模組 `tools/run_case/bank.py`：baseline 臂改成一次性建池（`--build-bank`）、之後
  每輪從 `evals/baseline-bank/` 讀，不再每輪重新生成；`--null-run` 讓校準改用
  same-call（兩份獨立 baseline 生成在同一次 grader call 裡盲判），取代原本跨輪配對
  的空實驗，關掉 `regression-protocol.md` 記載過的「校準比真實比較多一層雜訊」缺口。

**連帶作廢**：舊設定（6-chunk、xhigh、cross-round 空實驗）下量的所有數字——
`calibration.json`、「這個閘抓得到什麼」功效表、`fix/gate-null-calibrated` 之前跑的
`results-2026-08-04-null-r1~r3`——描述的是另一組量測設定，不能跟新設定的輪次混
aggregate 或混 calibrate。`tools/run_case/aggregate.py` 的 `IDENTITY_FIELDS` 新增
`runner_effort`／`grader_effort`／`baseline_source` 三個欄位，讓這件事在程式層面是
硬錯，不必單靠這則筆記提醒。

`skills/humanizer-zh/evals/null-r-series-SUPERSEDED.md` 是留給另一個仍在執行舊策略
（跨輪 `--baseline HEAD` 探針）的 session 的即時指標，事件過去、新校準跑完之後可以刪。

**收尾（2026-08-06）**：`--build-bank --rounds 6` 建池，15 個 `--null-run` 配對全數
成功（過程中 11 次 `claude exited 1`——與下方 ship-check 相同的 transient grader dispatch
失敗，重試即過，非設定問題），`--calibrate` 重產 `calibration.json`（`method:
"same-call"`，3 輪門檻：保護 7 列／命中 8 列）。`--aggregate` 對 null-run 結果的混用防呆
按預期硬錯（「a --null-run result measures the noise floor, not a change」）。

新設定下的 3 輪出貨判定（`results-2026-08-06-shipcheck-r1~r3`，新臂與 base 為同一份文字）：
SHIP，零違規，兩類都在校準門檻內——`fix/gate-null-calibrated` 的原始驗證目標達成。
詳細功效表（刻意打壞 k 列重量測）未在這次一併做：把 5 種破壞形狀 × 3/6 輪跑滿，成本遠
超這次改動本身，且不擋出貨——舊表已標「待重量測，數字先當方向參考」，維持這個狀態，
留給下一輪真的要動門檻常數時再補。

**觀察，留給下次動 `run-case.json`／`dispatch.py` 併發模型的人**：chunk 6→3 省的是
token（規則 blob 少送幾次），沒有省 wall-clock——`ThreadPoolExecutor` 只平行化 chunk
之間，單一大 chunk（34 案、effort high）內部仍是序列生成，一輪的下限被最大的單一 chunk
卡死。實測單輪 ship-check 最長跑到 4 小時以上，其中還有 2 次疑似掛住（三個 chunk 同時
卡住 40 分鐘以上零輸出，殺掉重跑後正常完工，本身也是與上述 `claude exited 1` 同一顆雷
的另一種呈現）。chunk 大小是 token 與 latency 的直接取捨，不是無成本的省錢招——調整前先
量兩者，不要只看 token 帳。

## Adversarial iteration log (rule-tuning rounds)

The method lives in `evals/adversarial-eval-protocol.md`. Each row = one GAN-style round; the `eval #N` in the Patch column maps to `id: N` in `evals/evals.json`.

| 日期 | 真人桶 | AI 桶 | FP / recall | 主要發現 | Patch |
|---|---|---|---|---|---|
| 2026-07-17 | 5 篇：觀點（高見龍）、教學（保哥/miniasp）、newsletter（倉鼠）、docs（工程會使用手冊）、公文規格（工程會資安要求） | 3 篇自生 zh-TW voiceless 文（觀點／教學／分析，無 Tier-1 詞級病句） | 署名文體 真人 FP=0/3；事務文體 若誤啟用 FP=2/2；AI recall=3/3 | (1) 判準應為 署名文體 vs 事務文體，非 blog vs 非 blog——真人觀點/教學/newsletter 穩定帶齊 stance/specifics/metaphor/口語破格；docs/公文本就均質須維持排除。(2) AI voiceless 文常無詞級病句，詞表會漏標，結構層才抓得到（層的價值驗證）。(3) 密集教學文（保哥）缺自創比喻卻為真人 →『只解釋不造像』不可單獨觸發。樣本小（n=3/3），round 2 應擴語料。 | gating 從 casual-only 擴為 署名文體 文體集；只解釋不造像加 technical-blog 成群才觸發 carve-out；eval #3 #4 |
| 2026-07-20 | n/a（此輪測 rewrite 機制而非 detect gating，非真人桶對照） | 1 組合成 prompt：docs 語境三句連續教練口吻段（含實質內容）＋一段扣除語氣後無實質內容 | rewrite-mode baseline vs new，非 FP/recall 指標 | span-local baseline 在無實質內容段落捏造了原文沒有的主張以避免留空；new 版正確輸出挖空標記句、不代筆。含實質內容段落兩版皆寫出連貫第三人稱改寫，此樣本未能區分 no-residual-seam 這一半。 | 新增 scope 階梯＋兩條硬規則（reframe-not-delete、flag-hollow-don't-ghostwrite）；eval #6 |
| 2026-07-28 | 合成保護桶 6 段 | 合成病灶桶 2 段，皆為零可查核事實 | 首輪 FP 3/18、recall 6/6；修正後 FP 0/18、recall 6/6 | 四字評語規則初版把判準寫成「刪掉這四個字少了什麼事實」，agent 逐詞判恆為「沒有」，於是成語旁已寫滿具體內容的公文／docs 也被誤殺。病灶是判準作用域錯置：成語本身永不帶事實，該問的是成語所形容之事有無寫在鄰句。 | 判準改為段落級＋三條分支；carve-out 增列公文與技術文件總結語；eval #10 #11 #12 |
| 2026-07-28（語料階段） | H 桶 20 篇（見 `evals/corpus.md`） | A 桶 12 篇（8 篇對齊 H 例主題、4 篇 voiceless 探針） | 未跑分——本輪只建語料與 baseline | 建語料本身即發現兩個規則缺口：罐頭式反應鏡頭、幻覺引用查證。 | 無 patch |
| 2026-07-29/30（2.0.0 重寫） | H 桶 20 篇（`corpus.md` 52 個 `ok` 列） | A 桶 12 篇（37 個 `flag` 列） | 見 `evals/results-2026-07-29-corpus-baseline-1.5.0.md` 與 `results-2026-07-30-v2-ab.md` | 1.5.0 在 corpus 上是 89/89 滿分——所以 corpus 這一輪的角色是回歸偵測器，不是進步的證據；進步要由 evals.json 的 14 個 `（缺口` 案例證明。 | 全面重寫至 2.0.0 |

## 判別問題形狀（沿用中的寫作原則）

移植 speak-human-tw 案例時確認的一點，2.0.0 已據此改寫：**規則的判準壓成一句可以直接拿去問 agent 的判別問題**，而不是一段散文說明。「這個詞是使用還是提及？」比「判準：⋯⋯」加三行解釋緊湊得多，也更容易在 carve-out 上分岔。

## Trigger-query 診斷更正（2026-07-19 resweep 的 id 3／id 10）

`backlog.md` 記錄的「id 3、id 10 兩個未分診的 fail」**指的是 `evals/trigger-queries.json` 的 query id**（router 觸發判斷），不是 `evals.json` 的內容品質 case——兩份檔案剛好都有 id 3 與 id 10。兩條在 1.5.0 的 description 下即已判 TRIGGER，2026-07-28 用修好的 `tools/run-eval` 實測 10/10 確認。

**殘留風險。** id 3 的 query 含「blog intro」，與 description 結尾排除句的「blog」字面相鄰，router 可能被字面誤導去分流到 `blog-writing-zh`。2.0.0 改寫 description 時保留了該排除句（它是必要的邊界宣告），並把開頭改成「language-layer cleanup pass」，讓職責分界不只靠結尾那一句承擔。改寫後 10/10 仍全過，含 id 3 與 id 9（RFP structural authoring 的負例）。

## Step 0 定位：id 86 與 id 47 的開火來源（2026-08-03）

兩案長期兩臂同紅，先前三輪針對 carve-out 的修改都沒有動搖它們。這一輪不改任何文字，
只做定位。

**儀器。** `run-case` 的 scratch workspace 持有 runner 與 grader 的全部輸出，但
`cli.py:134` 的 `discard_workspace()` 在收工時無條件刪除它，也沒有保留旗標；歷史輸出
同樣不在 repo（`.gitignore:1` 排除 `evals/*/runs/`）。因此改為匯入 `run_case.arms` 與
`run_case.dispatch` 的真函式重現單案 runner 呼叫，模型、reasoning effort、環境變數剝除
與 prompt 組法全部沿用正式跑分的路徑，只是把 stdout 留下來。兩案各一次抽樣。

### id 86：放行來自 `SKILL.md:130` 的保護清單⑥升格

runner 原文把兩個該被 `破碎短句堆疊` 抓的 span 直接掛進保護清單：

```
⑥「放心壓」：符合使用者宣告的 casual 口語措辭，原樣保留。
⑥「就別開」：符合 casual 的短句與口語提醒，原樣保留。
```

機制是 `:130`——「Where a voice profile … declares positive features, those features are
保護清單 item ⑥」。Voice `casual` 在 `:128` 宣告的正向特徵字面就含 short sentences，於是
「短句」被升格成保護條目，在規則評估**之前**就把 span 收走。「會結束，放心壓」全篇未曾
被當作 `破碎短句堆疊` 討論過，不是判它不成立，是它沒有進入判定。

**backlog 與 eval 各自寫的病因都不成立。** eval id 86 的 `does-not-spare-on-casual-register`
說病因是跨條借用 `過度簡寫` 的語域分支——runner 輸出零次提及 `過度簡寫`。backlog 說是
`:128` 的描述性文字——`:128` 本身只是描述，真正把它變成豁免的是 `:130` 的升格條款。

另一條路徑在 grader reason 裡有據但本輪未現形：r4 記「B states 依 casual profile 本次只
執行 P0 and drops all P1」、r6 記「A releases the whole paragraph because casual profile
'only runs P0'」。那是 `:126` Context `casual` 的「P0, plus `破碎短句堆疊`」被讀成「只跑
P0」，連 2026-08-03 才補上的 `plus` 例外一起丟掉。本輪 runner 有推定 `context: casual`
但仍逐層跑完 P1／P2，沒有走這條。

**兩處都要動的話是兩個變因,不在單一 branch 的範圍內。**

順帶一筆：模型自行推定 `context: casual` 並非軸混淆。`:126` 明文要求 unstated 時 auto-detect,
而 casual 的定義字面含 notes,prompt 給的是「個人筆記」——推定是照規則做的。

### id 47：三條規則開火，其中一條從未被處理

runner 本輪標了三項，全部在 P1：

| 規則 | span | 2026-08-03 有無處理 |
|---|---|---|
| `空降主張` | 每個人都因為 AI 而拉高成品的中位數 | 有；runner 判「沒有前文依據或後文展開」，條件未滿足 |
| `意義膨脹` | 自然整體的標準就變的更高了 | **無** |
| `情緒宣告` | 有些人在用 AI 的方式令人錯愕 | 有；runner 判「沒交代造成什麼結果」，條件未滿足 |

**carve-out 是構得到的,這點與先前的推測相反。** runner 明文引用 2026-08-03 新增的讓步開場
carve-out 放行 `模糊歸屬`,另外主動放行 `對比句式`、`對讀者說教`（「不曉得你們有沒有同樣的
感受」）與 `推廣語氣／四字評語`。那一輪的修改有效,只是不足以清空。

`意義膨脹` 不在 2026-08-03 動的三條之內,也不在任何既有假設裡。而 id 47 的
`expected-behavior` 要求「放行,一個字都不用動」——零 flag 的 all-or-nothing 期望,任何一條
規則開火它就紅。

**單一抽樣的限度。** 六輪 grader reason 顯示 flag 數在 2 到 6 之間浮動、開火規則逐輪不同
（r2 是 A 六 B 二,r3 是 A 三 B 六,r6 的 A 標 `空降主張`/`對讀者說教`）。本輪的三條是一次
抽樣,不是穩定集合;可確定的是 `意義膨脹` 從未被納入考慮,以及 carve-out 可達性已不是瓶頸。

## `--smoke` 判標籤，閘判修補——同一份輸出兩種判決（2026-08-06）

`tools/score-evals --smoke`（2026-08-07 前叫 `tools/run-case`）與正式閘不是同一把尺，
同一份 runner 輸出可以在兩邊拿到相反的判決。差別在 grader 讀什麼：

- **閘**（比較式、跨家族）讀的是**修補**。eval id 9 的 `flags-bare-verb`，閘給 pass 的
  理由寫「Both flag 「專有名詞不誤傷」 and restore subject/object in the fix.」——標籤叫
  什麼名字不是判準，受詞有沒有補回來才是。
- **`--smoke`**（絕對式、runner 與 grader 同為 codex）讀的是**標籤**。同一列的 fail 理由
  寫「輸出以過度簡寫概括該句，未明確指出動詞裸用及主詞、受詞缺漏」——修補在，但子形態
  名字沒寫出來，就紅。

**子形態命名本來就沒被要求。** `SKILL.md` 的輸出契約只寫到 canonical rule name（`:75`
「Each flag cites its canonical rule name」、`:48` 「under the row's canonical rule」），
沒有任何一處要求把 `動詞裸用`／`繫詞架構被抽掉` 這層寫進 flag。baseline-bank
`b342aef9a059` 六輪 chunk0 對同一句的輸出可以佐證：`動詞裸用` 出現 **0 次**，六輪全部只
寫 `過度簡寫` 加一句改法方向（r5 是唯一連改法方向都沒寫的一輪），而該列 base 臂的歷史
成績是 50/52 pass。子形態要不要寫是 runner 自由發揮，所以逐輪浮動——`--smoke` 等於在
計分一件從未被規定的事。

**單一 rep 的 `--smoke` 會翻結論。** 未改動的 HEAD 跑 3 reps `--smoke --ids 9`：
`flags-copula-elision` 1/3、`flags-bare-verb` 2/3、`全域:不換湯` 1/3；同一天三輪
ship-check（`results-2026-08-06-shipcheck-r1~r3`）那兩列都是 3/3 pass。浮動不限於這兩列，
`全域:不換湯` 同樣在跳。

**用法。** `--smoke` 紅一列，當作「去看一眼」的訊號，不是缺陷判定。動手改規則文字之前，
先查那一列在 `evals/results-*.json`／`evals/null-*.json` 的基準通過率（`case_id` +
`expectation`，`base`／`new` 兩欄），基準本來就八九成 pass 的列，單次紅八成是抽樣。真要
判斷一次改動的方向，兩臂各跑約 3 reps（改動樹一組、`git worktree` 開一份 HEAD 一組），
不要用單 rep 對單 rep。

## `過度簡寫` 加 `動詞裸用` 命名——命名過閘，附帶的前／後範例才是退步來源（2026-08-07）

承上一節的診斷，動手在 `zh-rules.md` 的 `過度簡寫` 抓 一行把 `動詞裸用` 命名、補上一組
前／後範例。兩個東西綁在一起量了 6 輪，NO-SHIP；拆開之後只留命名、不加範例，3 輪
SHIP。**退步來自那組範例，不是命名。**

| 版本 | 命中 new | 命中 base | margin | 判定 |
|---|---|---|---|---|
| 命名 + 前／後範例（6 輪） | 13.67 | 11.50 | **+9** | NO-SHIP |
| 只有命名（3 輪） | 13.33 | 13.33 | **+0** | **SHIP** |

保護側同步：只有命名的版本 row margin +4（門檻 +8），命中 +0（門檻 +7），兩類都清空。

**這是 `改法`／範例作用域外洩的第二個實例。** 上面 `語體漂移` 那節記過一次：寫給單一規則
的 `改法` 手段（「降格成條目：時程降級成括號附註」）外溢成通用 rewrite 習慣，害
`64/全域:不代筆` 連三輪失分，刪掉那行就回來。這次是同一顆雷換一種形式——多加一組
前／後對照，等於多給模型一個可模仿的改寫樣板，它會帶去別的 case 用。**規則檔加範例不是
免費的**，它的成本要跟命名、判準分開量，不能綁在同一次改動裡。

以下是綁在一起那版的完整量測，留著當對照：

**目標列從來沒壞過。** 改動前先查 `evals/results-*.json`／`evals/null-*.json`，
`flags-bare-verb`／`flags-copula-elision`（eval id 9）base 臂歷史成績 42–50/52 pass。
改動當天三輪 shipcheck 兩列都是 3/3。動手改之前就該把這當停止訊號，沒有——先做了才回頭
查歷史。

**6 輪閘上量測：NO-SHIP。** `--baseline HEAD`，`--bank-round` 重用既有 base 樣本、new
臂各輪重新生成，6 輪 aggregate：

| class / arm | r1 | r2 | r3 | r4 | r5 | r6 | mean |
|---|---|---|---|---|---|---|---|
| 保護 new | 12 | 14 | 11 | 11 | 10 | 12 | 11.67 |
| 命中 new | 17 | 13 | 12 | 15 | 13 | 12 | 13.67 |
| 命中 base | 8 | 11 | 11 | 10 | 15 | 14 | 11.50 |

保護在 n=4 一度衝到 5 個確認列（超門檻），n=6 收斂回 2 個確認列（未過門檻）——這正是
「單輪不足以定位誤判面」的示範，多跑幾輪就把它洗掉了。命中沒有洗掉：margin 穩定在
+8～+10，門檻是 +7，六輪定案 **NO-SHIP**。沒有任何一列在 6 輪裡撐到確認門檻
（最高 3/6）——是瀰漫性的小幅劣化，不是某一列的具體缺陷，猜測是改動規則文字的措辭，
連帶擾動了 runner 對其他規則的判讀，不是這行文字本身寫錯了什麼。

**已排除的機制假設。** 一度懷疑 `動詞裸用` 的定義擠進了 `語體漂移` 的判準地盤，
拖累 id 67／68（`flags-register-drift`）——三輪數據撐不住這個故事（67 只 1/3、
68 只 1/3，不到確認門檻）。也查過 id 59（`expected-behavior`／
`preserves-rhetorical-question`）連續三輪同紅，但 grader reason 顯示開火的是
對讀者說教／反問句／模糊歸屬——跟過度簡寫或動詞裸用完全無關，是這個 case 本身在兩臂
都不穩定的既有現象，不是這次改動造成。

**結論：只有命名的版本進 `zh-rules.md`，前／後範例不進。** 綁範例那版一度整個 revert 過，
後來把範例拆掉單獨再量，才看出命名本身是乾淨的。留給下一個人的教訓有兩層：診斷對不代表
修法對（目標列 `flags-bare-verb` base 臂歷史 42–50/52 pass，本來就沒壞，改它的理由一開始
就很薄）；改動綁兩個變因就量不出是哪個在動，拆開重量的成本遠低於誤判。

**量測的識別欄位會咬人。** `baseline_ref` 屬 `IDENTITY_FIELDS`，記的是傳進去的字串本身。
只有命名那版的前 3 輪用 `--baseline HEAD` 跑（當時 HEAD 是 `e80692d`），命名一旦 commit
進 HEAD，`--baseline HEAD` 就變成拿改動比自己（base blob 與 new blob 同一個 hash，bank
也因此對不上）。補跑確認輪必須把 baseline 釘在改動前的 commit（`2fe4a3c`），而釘了之後
`baseline_ref` 字串不同，就再也不能跟前 3 輪混 aggregate——只能整組 6 輪重跑。**要跑多輪
確認，一開始就釘 commit hash，不要用 `HEAD`。**

**副產品：閘的 grader 家族預設換了。** 過程中把 `cli.py` 的 grader 預設從
「跑者的另一家族」改成固定 `codex`，`--allow-same-family` 隨之整段拿掉——這是獨立的
基礎設施決定，不是這次 skill 改動的一部分，細節見 `tools/score-evals` 檔頭與
`tools/score_evals/cli.py`（同日上游把 `run-case` 更名為 `score-evals`，這個改動是在
更名後的檔案上落地的）。**代價**：切換發生在這次量測進行中，round 6 因此在舊/新預設
交界處產生一份 grader 對不上其他輪次的孤兒檔（`results-2026-08-06-narrow-r6-codexgrader-orphan.json`），
必須重跑 round 5、6 才補回 6 輪一致的樣本。日後若要再拉 baseline bank／`--null-run`
重新校準，這是要素之一。

## score-evals 量測設定 v3：6-chunk、codex grader、`--null-sweep`（2026-08-08）

`tools/score_evals` 換了第三輪量測設定。跟 v2 一樣，這是一組互相牽動出貨門檻的變更，
不是幾個獨立補丁：

- `evals/score-evals.json` 的 chunk 從 3 拆回 6。動機是牆鐘時間：一輪的耗時由最大的
  chunk 決定（同一次 call 內的生成是序列的，`ThreadPoolExecutor` 只跨 chunk 平行），
  3-chunk 佈局最大的 chunk 有 34 個案例。拆成 6 之後最大 chunk 降到 18。代價是規則
  blob（約 112k 字元）每輪重送的次數加倍——這正是 v2 當初從 6 併成 3 的理由，所以這次
  是把當時的取捨反向做一次，不是修正 v2 的錯。
- grader 預設從「跟 runner 不同家族」改成 codex，`--allow-same-family` 移除。換到的是
  成本與不必安裝第二個 CLI；換掉的是跨家族盲判（同家族 grader 比較有機會認出自己的
  措辭）。
- `calibration.json` 用 codex grader 重新校準。v2 的門檻是 15 組 claude 盲判空實驗
  重抽出來的，在 grader 換家族之後，那條 SHIP／NO-SHIP 線等於是借別的裁判的尺。

**chunk 佈局不是把 v2 之前的 6-chunk 直接還原。** 歷史佈局的 chunk0 只有 `[1, 9]`，
而案例 2-8 是它之後才加進 fixture 的；照抄會讓 7 個案例從此不出現在任何 chunk 裡，
分母悄悄變小而沒有任何東西會報錯。實際落地的 chunk0 是 `[1..9]`，全部 85 個 id
各出現一次。

**新的門檻與 v2 不可比。** 6 輪：保護在 4+ 確認、擋在 2 列以上或單列 margin 超過
+10；命中在 4+ 確認、擋在 5 列以上或單列 margin 超過 +2。命中的單列 margin 天花板從
v2 的 +7 掉到 +2——codex grader 在這個 class 上的雜訊明顯低於 claude，閘因此變嚴；
保護則反向從 +8 放寬到 +10。舊設定下量到的所有數字（v2 的 `calibration.json`、
`b342aef9a059` bank、`null-2026-08-06-*` 那 15 組空實驗、所有 `results-2026-08-0*`
輪次）描述的是另一組設定，`IDENTITY_FIELDS` 會在混用時硬錯。

**baseline bank 從此不進版控**（`.gitignore` 加 `skills/*/evals/baseline-bank/`）。
v2 的 bank 是有 commit 的，但那份紀錄其實沒有它看起來的價值：runner 輸出是隨機的，
重建只會得到一份等價的 bank，不會得到同一份，所以 commit 它既不能重現也不能稽核。
判定本身留在 results 與 null 結果檔裡，背後的原始 runner 文字不需要一起留。代價是
下一輪對同一個 baseline 的量測要先 `--build-bank`（6 chunk × 6 輪 = 36 次 dispatch，
約 9 分鐘，全部走 codex，不花 Claude token）。

**工具側連帶變更**，兩個都是這次重建過程中發現的缺口：

- `aggregate.py` 加了 grader 對照的提示：round 的 grader 與 `calibration.json` 的
  grader 不一致時，報告會標明「這份判定借用了另一個裁判的尺」。`IDENTITY_FIELDS`
  只擋 round 之間互相混池，不管 round 與校準來源之間的落差。這是提示不是硬閘——
  margin 本身仍然成立，借來的只有那條 SHIP／NO-SHIP 線。
- 新增 `--null-sweep`：一次跑完所有 `C(N,2)` 配對，`--null-batch`（預設 5）控制同時
  在飛的配對數。`--jobs` 只平行化單一配對內的 chunk，所以配對逐一跑會退化成 15 波
  只填了 6 個 slot 的池；批次化之後約 3 波。單一配對失敗不會拖垮整輪，重跑同一道
  指令只會補沒跑到的部分——跳過與否是看結果檔內的 `base_blob_sha256`，不是看檔名，
  因為 bank 重建之後同名的舊結果描述的是另一個 bank。

## `detect` 成預設：三版措辭的行為對照（2026-08-03／04，量測設定 v1）

**改動。** `SKILL.md` 模式表把 `(default)` 從 `rewrite` 移到 `detect`，並補一段路由說明：
明示改寫意圖走 `rewrite`，明示只標走 `detect`，兩者皆未明示走 `detect` 並在報告後問一次。
`references/` 與 `evals.json` 皆未動——單一變因。

**底下所有輪次跑在量測設定 v1**（`run-case`、claude grader、均值護欄），該設定已被 v2／v3
取代，判定層也已由 `row_margin` 接手。**逐列訊號與 grader 原話仍然成立**，那是這一節的價值；
**均值那一層的分數不要拿來當今天的裁決**，理由見末節。

**fixture 為什麼不必跟著改。** 14 個 `rewrite_case_ids` 的 prompt 本來就全部明示改寫意圖，
13 案字面以 `rewrite 這段` 開頭，只有 id 2 寫「幫我把 AI 味拿掉」。預設翻轉打不到它們。

**id 2 的綠沒有資訊量。** 它被指定當哨兵，六列卻全部在 detect 與 rewrite 之下同樣通過
（詳見 backlog 該項）。路由正確是靠單案補跑讀 runner 第一行 `案例 2｜rewrite｜` 確認的，
不是靠計分列。

### v1 措辭（r1–r6）：誤標

| class / arm | r1 | r2 | r3 | r4 | r5 | r6 | mean |
|---|---|---|---|---|---|---|---|
| 保護 new | 7 | 9 | 5 | 8 | 8 | 5 | **7.00** |
| 保護 base | 9 | 3 | 8 | 11 | 5 | 9 | 7.50 |
| 命中 new | 11 | 8 | 11 | 9 | 11 | 14 | **10.67** |
| 命中 base | 10 | 13 | 15 | 12 | 12 | 9 | 11.83 |

三輪時曾出現保護均值劣於 baseline（7.00 對 6.67），補到六輪後翻正——病因是 r2 那輪 base
只紅 3 列的離群值。**單輪判定不可採信這件事，這一輪自己又示範了一次。**

聚合器列出的「confirmed false kill」包含兩臂同紅的既有缺口（`47/expected-behavior`
5/6、`86/does-not-spare` 4/6、`59/expected-behavior` 4/6），那些是 main 自己也扛著的，
不是本輪打壞的。扣掉之後，新臂獨有且達 2/6 的只有四列：

| 列 | new 紅 | base 紅 | 案子模式 |
|---|---|---|---|
| 59/expected-behavior | 6 | 4 | detect |
| 59/preserves-rhetorical-question | 5 | 3 | detect |
| 47/no-run-on-splitting | 2 | 0 | detect |
| 66/全域:保真 | 2 | 0 | rewrite |

**四列裡三列是 detect 案的假陽性**，而且失敗形態一致：新臂去標了該放行的東西
（59 把結尾反問句當缺陷要求改成直述，47 要求拆逗號串接）。這指向措辭而不是路由——
v1 那段寫著 detect「report the findings, then ask」，讀起來像在交代要產出發現，
而把該模式設成預設等於讓每一個沒指定的請求都落在那句話底下。

`66/全域:保真` 只有 2/6，且 r3–r6 未再出現；r4 兩臂皆綠並正確地把末句換成標記交還作者。
按雜訊處理，不另外修。

### v2 措辭（r7–r12）：往反方向過頭，成群漏標

v2 把那段砍成只剩路由與停下來問，另加一句明文擋掉那個暗示：an audit that ends up with
nothing to report is a complete answer, not an unfinished one。

| class / arm | r7 | r8 | r9 | r10 | r11 | r12 | mean |
|---|---|---|---|---|---|---|---|
| 保護 new | 2 | 7 | 6 | 4 | 7 | 7 | **5.50** |
| 保護 base | 7 | 6 | 8 | 7 | 7 | 8 | 7.17 |
| 命中 new | 9 | 12 | 13 | 12 | 17 | 11 | **12.33** |
| 命中 base | 13 | 10 | 12 | 14 | 10 | 11 | 11.67 |

前三輪看起來很好——保護類誤殺從 7.00 降到 5.00，v1 那兩條乾淨的新臂獨有退步
（`47/no-run-on-splitting`、`66/全域:保真`）完全消失，機制假設成立。補到六輪之後翻盤：
新臂獨有的**命中類漏標**集中成群，全部是「該標卻沒標」：

| 列 | 次數 |
|---|---|
| 78/fix-empty-process-phrasing | 4/6 |
| 7/flags-contrast-construction | 3/6 |
| 81/flags-under-fragmented-clause-rule | 3/6 |
| 81/flags-dangling-copular-frame | 2/6 |
| 78/fix-hedging-opener | 2/6 |
| 79/flags-broken-inference-chain | 2/6 |

三輪時我已準備收工 push，是第六輪擋下來的——**單輪不可信這件事，在同一個 branch 裡示範了
第二次，這次代價是差點出一個會漏標的版本**。

新臂獨有的確認退步另有一列與模式預設無關：`83/preserves-procedural-second-person`（r7–r9
2/3）。該案兩臂都走 rewrite，失敗形態是改寫時把該保留的程序性「你」剝掉（r8「B strips the
你 to 往下捲動設定頁，會看到…despite calling it protected」、r9「A rewrites it to 在設定頁
向下捲動時，會看到紅色警告」）。**那正是 backlog 第 9 項記載的 `對讀者說教` 改法外溢**，
而 id 83 就是 2026-08-02 為了觀察它才新增的兩個 rewrite 案之一。這一輪順帶解掉該項「量不到」
困境的一半：它原本卡在「`改法` 只在 rewrite 模式顯形，而風險最高的兩條各有 0 個 rewrite 案」，
現在是第一次真的量到外溢發生，有逐輪 grader 原話為憑。本 branch 不動 `對讀者說教` 的
`改法`——那超出單一變因，且第 9 項明文寫著沒有證據就拿掉會退掉真正有用的方向。

### 三版並列：偏移全部來自那句與路由無關的補充

| 版本 | 多說的那句 | 保護 new/base | 命中 new/base |
|---|---|---|---|
| v1 | report the findings, then ask | 7.00 / 7.50 | 10.67 / 11.83 |
| v2 | an audit with nothing to report is a complete answer | 5.50 / 7.17 | 12.33 / 11.67 |
| v3 | 拿掉，只留「這只決定跑哪個模式」 | 7.33 / 7.67 | 11.00 / 12.67 |

同一個路由邏輯，三種措辭，模型行為往兩個相反方向偏。v1 那句讀起來像在交代要產出發現，
於是誤標；v2 那句讀起來像在說找不到東西是常態，於是漏標。兩句都不是路由的一部分——
模式表的 deliver 欄本來就寫明 detect 交付什麼。

**這與 `語體漂移` 那次外溢同構**（backlog 第 9 項）：規則文字裡任何一句對「該產出什麼」的
描述，都會被當成通用指令搬到無關的案子上。差別只在那次是 `改法` 欄，這次是模式說明。
教訓可以寫成一句：**只寫決定什麼，不寫期待看到什麼。** 這是本節唯一不依賴量測設定的結論。

v3 是留下來的措辭，v2 那組結構性漏標（78、7、81）在它底下全部掉到 1/3。

### 為什麼這批分數不能拿來裁決 v3

三版各跑滿六輪之後，把每輪的配對差（new − base）攤開：

| 樣本 | 類別 | 均差 | sd | 逐輪差 |
|---|---|---|---|---|
| v1 | 保護 | −0.50 | 4.04 | −2, 6, −3, −3, 3, −4 |
| v1 | 命中 | −1.17 | 3.71 | 1, −5, −4, −3, −1, 5 |
| v2 | 保護 | −1.67 | 2.16 | −5, 1, −2, −3, 0, −1 |
| v2 | 命中 | +0.67 | 3.78 | −4, 2, 1, −2, 7, 0 |
| v3 | 保護 | +0.00 | 1.41 | 2, −2, −1, 1, 0, 0 |
| v3 | 命中 | +0.50 | 4.93 | −5, 2, −2, 5, 7, −4 |

當時的均值護欄拿點估計比大小，v3 因此因為命中類 +0.50 被判退步——而那個 +0.50 的輪間 sd
是 4.93。三次「三輪看起來過、六輪翻盤」不是三次巧合，是同一個問題的三次現形：**護欄動作的
門檻遠小於它自己的浮動**。

這個診斷後來由空實驗獨立確認並修掉，見
[`evals/regression-protocol.md`](evals/regression-protocol.md)：舊均值護欄拿一份文字比它
自己時觸發 47%，已由 `row_margin` 取代，兩類的每輪平均仍然印出來但**不再參與判定**。
上表因此是舊儀器的讀數，留作 v1／v2 行為差異的佐證，不是 v3 的裁決。

**v3 的裁決狀態：未判。** 它從未在 `row_margin` 加 null 校準門檻下跑過。要出這個版本，
重跑一輪新設定的量測即可，不需要再調措辭——**繼續調措辭等於對噪音做梯度下降**，這是當初
停手的理由，在新閘下依然成立。

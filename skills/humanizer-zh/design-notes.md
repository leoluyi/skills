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

**煞車是怎麼過的，這一項與 `體裁相稱` 不同。** backlog:472 那條煞車寫的是「兩案不足以立一條規則——先在既有語料裡找同型案例」。這裡作者 1 案、語料庫 0 案，照字面過不了。實際過關的理由是作者當輪直接裁示開規則，不是舉證數達標。**這件事要記著，因為它是這條規則目前最大的弱點**：`語體漂移` 有五輪量測、`體裁相稱` 被同一條煞車擋了一輪，本條兩者皆無。

**保護案三案裡兩案是合成的。** id 75（操作句不是稽核句）是作者親筆，屬真語料；ids 73（消歧義）、74（來源註記）是為了測 carve-out 現寫的。第 4a(4) 項已經判定「保護類的整個主張是『這是真人會寫的東西，不准動它』，用造出來的句子去測等於用人味的演出代替人味本身」。命中案 id 72 與保護案 id 75 兩側都是真語料，剩下的兩個合成保護案待替換，記在 backlog。

**carve-out 的重點是消歧義與防守的分界，判準寫成可執行的檢查。** 「拿掉這句，讀者會不會套錯判準？」會就保留。這個問法把一個看起來很主觀的分界變成單一動作——沒有它，方法章節、稽核報告、資料表註記全都表面命中，而那三種文體裡宣告來源與涵蓋範圍本來就是交付物本身。

**沒有寫 `改法` 行。** 手段（把稽核句換回操作句、主詞從名物化的「判斷依據」回到動作）照 backlog 第 9 項的判別式是**搬得動的**——名物化轉動詞適用於任何句子，脫離本規則的形態仍然成立，與 `語體漂移` 那次外溢同型。方向由前／後對照承載。

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

## 語體漂移 — 一條 provenance 判準被拆成 surface 判準 (2026-08-01)

規則的來源是作者提供的一句真實工作文字：「預期產出與時程：助教人力配置方案與 Lab 支援範圍，訪談後 3 至 4 週內取得。」句法上它同時想當條列標題與完整句子——前半名詞組無謂語，唯一的動詞卡在句末、跨過一個逗號回頭管前面的賓語，中間沒有任何授權前置的標記。

**作者原本要編碼的判準有三項，只有第一項照原形進了 skill。**

第二項是「缺陷與完成度不匹配」：人的失誤是減法（漏字、漏主詞、標點不一致），AI 的失誤是骨架歪掉但零件樣樣俱全，因此組裝感與高完成度同時出現才是決定性訊號。這句話問的是**誰寫的**，而 `SKILL.md` 的〈What this skill is and isn't〉明文只判 surface、不判 provenance。照字面寫成命中門檻，skill 就開始做它拒絕做的主張。處置是把它翻面：**組裝感伴隨完成度下降時放行**，寫進 `語體漂移` 的保留條款。非母語寫作、翻譯體、多來源剪貼因此照樣被保護，而規則一句話都沒說作者是誰。`backlog.md` 的 (H) 雙軸評分閘沒有放行，仍等盲測資料。

第三項是「結構訊號權重高於內容訊號」。它不屬於任何單一規則——內容可以從表格、模板或來源文件繼承，語法是當場生成的——所以落在 `SKILL.md` 步驟 4 的一行，而不是自成一條規則。

**判準本身沒有證據支撐，這一點要說清楚。** 三項判準全部出自 2026-08-01 一場非盲測的 annotate session：判讀者知道答案，中途又拿到一份人寫的對照改寫。落地的理由是第一項屬 surface、可由既有的 run-case 儀器直接量測，不是那場 session 證明了什麼。

**量測：五輪，前三輪 NO-SHIP，拿掉 `改法` 之後的 r4／r5 過閘。** 數字在 `evals/results-2026-08-01-drift-aggregate.md`。規則抓得到目標——ids 67、68 的命中列三輪都是新版過、2.1.0 落空，vanilla 對照也是 17:8——但保護類平均從 104 掉到 100.7，且 `64/全域:不代筆` 三輪皆失、`64/全域:保真` 兩輪失。兩者同因，而那個因很值得記著：**規則的 `改法` 寫了「降格成條目：時程降級成括號附註」，模型把它讀成了通用許可，在別的 rewrite 案裡也開始加括號編註**。一條寫給單一規則的改法手段，會外溢成整個 rewrite 模式的習慣——這是 `改法` 行第一次被觀察到有這種作用域外洩，下次寫任何 `改法` 都要把手段綁在該規則的形態上。

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

`tools/check-labels` validates both instruments against the rule names the skill actually declares (derived from `zh-rules.md` headings and `hidden-author.md`, so there is no separate manifest to drift), plus the corpus 解析契約 — every 引文片段 must be an exact substring of its clean quote, `全文` excepted. Since 2026-07-30 the extraction is declared in `evals/label-check.json` rather than hardcoded in the tool, which is also what makes the gate opt-in for other skills; that file names the *files and regexes*, never the rule names, so the no-drift property is unchanged.

### 兩個 namespace，一個白名單（2026-08-02）

閘從 `1ec104a` 起連紅三個 commit，8 個 FAIL，兩個成因的共通點是**名字都合法，只是沒有宣告的地方**。修法各自長一層，而不是把名字塞進 `names` 常數：

`改寫保真` 是**跨規則的期望類別**——它要求的是輸出不得漂移，與哪一條規則命中無關，所以沒有 `###` header 可derive。塞進 `names` 等於宣稱它是一條規則。改成 config 的 `expectation_classes` 獨立宣告，`resolve()` 兩個 namespace 都查，但查不到時報得出它該從哪裡來。另加一道 overlap 檢查：同一個名字不得同時宣告為規則與期望類別。

`四字評語` 在 `zh-phrase-rules.md`，而那個檔的 9 個 header 只有這一個當規則名用。整檔納入 `sources` 會把「台灣用語偏好」「AI 慣用詞替換」一起收進 canonical——`resolve()` 是精確比對、刻意不做寬鬆匹配，混進去的名字會讓別處的錯字變成合法標籤。改用**白名單 regex**（`^## (四字評語)`）：之後要加名字就得改 alternation，那個顯式編輯正是白名單的重點，不是它的麻煩。

規約沒有變寬：canonical 65 個名字，`zh-phrase-rules.md` 的另外 8 個 header 逐一驗過皆被拒，`改寫保真x` 這類錯字端到端仍然 FAIL。

### 正式文件語料的第二、第三份（2026-08-02）

H-23／H-24 出自同一份報告、同一位作者（林端，法社會學），所以 H-24 那三個 `flag` 到底是這個體裁的通則、這位作者的筆法，還是鄰句有沒有著落，量不出來。補進兩份國科會成果報告全文換掉這兩個變因：H-25（黃慕萱，圖書資訊學）換作者、H-26（鄧成連，設計管理／工業設計）同時換作者與學門。

H-25 的價值在它與 H-24 共用同一個四字語而判定相反：H-24 的「相輔相成」後面沒有寫出兩個計畫如何互相援引，H-25 的「相輔相成」前面就把兩種指標各自的貢獻寫完了。這一對把判準釘在鄰句的著落上，而不是那四個字。

H-26 帶進兩組本檔原本沒有的保護：宣告過的比喻系統（醫學比擬，該報告自己在同段寫明），以及兩個真人筆誤（「診計診斷」的順序顛倒、「進乙步」的同音誤植）——後者是本檔第一則以錯字入桶的例子。

判定欄是待作者複核的：語料合不合用、每一列判得對不對是品味判斷，agent 只負責逐字節錄與標出處。

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

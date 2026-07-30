# Corpus — 標註語料

帶 ground truth 的原始樣本庫。每一例是一段**真實出處**的短文，附逐字引文與逐片段判定，
供偵測規則改動後重跑、量 false-positive 與 recall。

分工（三份檔案各司其職，不互相取代）：

| 檔案 | 回答的問題 |
|---|---|
| 本檔 `corpus.md` | 真實文本上，哪一段該標、哪一段不該標 |
| `evals.json` | 給定一段 prompt，skill 的行為是否符合預期 |
| `judged-cases.md` | 某條規則當初為什麼長成這樣 |

方法論在 `adversarial-eval-protocol.md`（進攻：找盲點）與 `regression-protocol.md`
（防守：出貨門檻）。歷次跑分結果記在 `../design-notes.md` 的對抗迭代 log。

**版權。** 只引短段並標出處 URL，不整篇轉存、不重新發布。真人桶的身分**以外部考據為準**，
不以 skill 的判斷為準——真人文被標是一筆 false-positive 資料點，不是「這個作者是 AI」的證據。

---

## 格式規約

### 解析契約

工具讀本檔時可依賴以下四點，改格式前先確認工具端一起改：

1. 每一例以 `### <ID> — <標題>` 起始；ID 形如 `H-01`（真人桶）或 `A-01`（AI 桶）。這條契約
   只約束真實案例——`### 樣板` 一節內、包在 ```` ```` ```` 四個反引號圍欄裡的 `H-00` 是
   示意用模板，工具解析時應先跳過該圍欄區塊，不當成一個真實案例讀。
2. 例內第一個 blockquote 區塊是**淨引文**：逐字原文，不含任何標記、註解或省略號以外的編輯痕跡。
   要餵進 eval prompt 時整塊取出即可，不需 strip。淨引文若在原始 Markdown 裡跨行（純為排版
   換行，非原文的段落換行），取出時以空字串（而非換行符）拼接該些行，才會和判定表的子字串
   對得起來；原文真正的段落分段（blockquote 內以 `>` 單獨一行分隔）才保留為換行。
3. 判定表是例內第一個 Markdown 表格，欄位固定四欄（見下）。「引文片段」欄的值必須是淨引文的
   **精確子字串**；不用字元 offset，引文他處改字不會讓對位全歪。**唯一例外**：值為 `全文`
   時代表判定對象是整段淨引文而非某個片段（用於 A-09～A-12 這類「缺席的是整篇的立場／細節／
   比喻，不是某一句用詞」的 voiceless 探針），不必是子字串。
4. `**整篇判定**：` 與 `**預期方向**：` 是行首粗體 key，值到行尾為止。

### 每例的 metadata 欄位

固定 key、全形冒號分隔、每行一項。真人桶與 AI 桶欄位不同：

**真人桶（H）**

```
- 來源：真人
- 作者：<具名>
- URL：<可公開存取的原文網址>
- 發表：<YYYY-MM-DD；2022 前尤佳>
- 語言：zh-TW | en
- 文體：technical-blog | blog | newsletter | docs | 公文 | SOP | RFP | 簽呈 | casual
- 文體類：署名文體 | 事務文體
- 面向：<見下方 7+2 分類軸>
- 取材：<取原文哪一段、幾句>
```

**AI 桶（A）**

```
- 來源：AI
- 模型：<模型名與版本>
- 生成：<YYYY-MM-DD>
- prompt：<生成指令摘要，一句>
- 對齊：<對應哪一則真人例的主題／文體，或 n/a>
- 語言：zh-TW | en
- 文體：<同上表>
- 文體類：署名文體 | 事務文體
- 面向：<見下方 7+2 分類軸>
```

`文體類` 欄不是文體的同義詞，是**作者隱身該不該啟用**的判準：署名文體（觀點、
technical-blog、newsletter、casual）應啟用，事務文體（docs、公文、SOP、RFP、簽呈）
應維持排除。這一欄是 gating 邊界的量測對象，不可省。

`面向` 欄是這一例主要測的分類軸，取自下方 Coverage matrix 的 8 個缺陷類別
（內容類／語言句式／風格版面／溝通殘留／事實與引用／立場與開場／人工戲劇／
打破第四面牆）或 2 個正交機制（保護清單／長文scope）之一。一例可能同時觸及多個
面向的判定列，但填寫時選這一例**最具代表性**的一個，讓 coverage matrix 彙整時有
明確歸屬。

（8 個而非最初設想的 7 個——打破第四面牆是實際替 H/A 兩桶標註時浮現的第 8 類：
它談的是「交付物在談論自己」，跟內容是否空洞〔內容類〕、句式是否合乎中文語感
〔語言句式〕、版面是否過度裝飾〔風格版面〕、是否殘留協作痕跡〔溝通殘留〕都不同軸，
硬塞進其中一類會失真，所以升格為獨立類別而非勉強歸併。與它相鄰的「對讀者說教」
問的是另一件事——文件在對誰說話、以及有沒有把讀者當成被評斷的對象——歸在
立場與開場。）

### 判定表

| 欄位 | 值 | 說明 |
|---|---|---|
| 引文片段 | 淨引文的精確子字串 | 涵蓋一個判定所及的最小範圍 |
| # | 正整數，可留空 | 僅當同一片段在該例引文中重複出現時填，指第幾次 |
| 判定 | `ok` / `flag` | `ok`＝真人正常寫法，標了就是 false positive；`flag`＝確實該標 |
| 規則 | `references/zh-rules.md` 的規則名，或 `作者隱身／<子訊號>`、`保護清單／<項目>` | `ok` 列填「被誤標時最可能觸發的那條」，才量得出 FP 歸屬 |

`ok` 列的「規則」欄容易被填成空白——請務必填。FP 的價值在於指出**是哪條規則過度觸發**，
沒有這一欄，一輪跑完只知道誤標率，不知道要 carve-out 誰。

### 整篇判定與預期方向

- `**整篇判定**：clean` 或 `**整篇判定**：flagged — <規則A>、<規則B>`
- `**預期方向**：` 僅在 flagged 時寫，記**改法方向**不記逐字答案（rewrite 是開放輸出，
  逐字答案會把 eval 變成比對字串）。clean 的例子省略此行。

### 樣板（示意用，非真實語料）

````markdown
### H-00 — <一句話說這例在測什麼>

- 來源：真人
- 作者：<具名>
- URL：https://example.com/post/xxxx
- 發表：2019-03-11
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 取材：全文第 3 段，2 句

> 這個地雷有兩個 Workaround。我認為第一種比較完美，可以應付各種狀況——記得 13 年前
> 我也踩過一樣的坑（那時還沒有這個範本，只能手動設）。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 我認為第一種比較完美 |  | ok | 零資訊警句與口號 |
| 記得 13 年前我也踩過一樣的坑 |  | ok | 作者隱身／零具體個人細節 |
| 可以應付各種狀況 |  | ok | 空話填充 |

**整篇判定**：clean
````

---

## 真人桶（H）

外部可考據的真人手寫文本。這一桶量的是 **false-positive rate**：被標的比例越低越好。

取材守則：作者具名、原文可公開存取、2022 年前發表尤佳；每篇只取代表性短段。
文體要鋪開——署名文體 與 事務文體 都要有，否則量不出 gating 邊界。
zh-TW 與 en 兩語都要有，英文桶是 round 2 明列的缺口。

**Tier 註記。** H-13～H-16 四例的來源是 2023 年後才創立的 Substack newsletter，
主題本身就是 AI／科技／投資。「真人手寫」除了作者具名／持續經營的固定筆名之外，
沒有外部憑據能排除 AI 輔助——與 H-01～H-12、H-17～H-20（2022 前或無時效性的官方
文件／規格）不同等級。四例保留是因為它們覆蓋了 A/B 兩層都拿不到的文體
（newsletter、投資分析、吐槽觀點）；跑分時如需區分權重，可用作者/發表日期
兩個 metadata 欄位過濾出 Tier A 子集。

---

### H-01 — 保哥：Docker Desktop 防火牆踩坑記

- 來源：真人
- 作者：黃保翕（Will 保哥）
- URL：https://blog.miniasp.com/post/2021/06/14/Docker-Desktop-for-Windows-Windows-Firewall-Issues
- 發表：2021-06-14
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 面向：人工戲劇
- 取材：文章開頭兩段

> 今天因為要維護一個 11 年前完工的專案，特別把當時的 VM 還原到 Hyper-V 裡面執行，而 SQL Server 的部分我就打算直接跑在容器中。因為我的 VM 跑在 External network 網路下，所以等同於是區域網路的另一台電腦要連到我的 SQL Server on Linux 容器。照理說這應該只是個很簡單的問題，但是我的 VM 就是怎樣也連不到我這台電腦的 SQL Server 容器，網路就是打不通！最後搞了一整個上午，才真正釐清真相！
>
> 唉～你一定覺得很蠢對不對！請繼續看一下，事情通常不是憨人想得這麼簡單！

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 今天因為要維護一個 11 年前完工的專案，特別把當時的 VM 還原到 Hyper-V 裡面執行 | | ok | 空降斷言開場（有具體情境鋪陳，非指涉未交代之物） |
| 網路就是打不通！ | | ok | 零資訊警句與口號（真實情緒感嘆，非破折號收尾的自我加值） |
| 最後搞了一整個上午，才真正釐清真相！ | | ok | 作者隱身／零具體個人細節（此句正是具體細節本身，反例） |
| 唉～你一定覺得很蠢對不對！請繼續看一下 | | ok | 對讀者說教（casual／部落格聲音的 carve-out，自嘲共感非居高臨下判斷） |

**整篇判定**：clean

---

### H-02 — 保哥：VS Code 取代 Azure DevOps Wikis 編輯器

- 來源：真人
- 作者：黃保翕（Will 保哥）
- URL：https://blog.miniasp.com/post/2021/09/14/Writing-Azure-DevOps-Wikis-Markdown-using-Visual-Studio-Code-and-Git
- 發表：2021-09-14
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 面向：內容類
- 取材：文章開場段

> 我們經常在 Azure DevOps Services 的專案中撰寫 Wiki 文件，但是 Azure DevOps 的 Wikis 線上編輯器實在是太難用了，我覺得還是在 VSCode 撰寫 Markdown 來的方便許多。除此之外，因為 Azure DevOps Wikis 可以放附件上去，但也不是所有檔案類型都支援，所以偶爾會遇到無法上傳附件的狀況。還有，你可能想要取回已經刪除的文件，但是從線上似乎沒有方法可以查閱這些文件。今天我打算用這篇文章來解決上述所有問題！

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 我覺得還是在 VSCode 撰寫 Markdown 來的方便許多 | | ok | 空降主張（判斷句緊接同句理由：Wikis 線上編輯器太難用，非懸空結論） |
| 你可能想要取回已經刪除的文件 | | ok | 對讀者說教（描述讀者可能的操作情境，非評斷讀者本人，屬程序性第二人稱） |
| 今天我打算用這篇文章來解決上述所有問題！ | | ok | 空降斷言開場（回指前文已列的三個問題，非指涉未交代之物） |

**整篇判定**：clean

---

### H-03 — 保哥：gitignore 範本工具（中性技術段落對照）

- 來源：真人
- 作者：黃保翕（Will 保哥）
- URL：https://blog.miniasp.com/post/2020/05/24/Setup-git-ignore-alias-to-download-gitignore-templates
- 發表：2020-05-24
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 面向：語言句式
- 取材：文章開場段

> 每次開發一個新專案，多多少少都會需要手動加入 .gitignore 檔案。如果用 Visual Studio 2019 建立專案時加入 Git 版控，工具會自動幫你新增 .gitignore 檔案。但若用 dotnet new 建立專案時就不會自動建立 .gitignore 檔案了。本篇文章我將介紹一個好用工具，可以讓你很便利的快速產生專案所需的 .gitignore 檔案。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 本篇文章我將介紹一個好用工具 | | ok | 作者隱身／只解釋不造像（此段確實只解釋不造像，但屬教學文開場，需與其他結構訊號成群才計入；本文其餘段落〔見 H-01〕有具體踩坑細節） |
| 工具會自動幫你新增 .gitignore 檔案 | | ok | 對讀者說教（描述工具行為對讀者的影響，主詞是流程不是評斷讀者） |

**整篇判定**：clean（附註：此段本身無立場、無比喻、無具體細節，是同一位真人作者在同一個部落格裡完全中性的一段——直接證據支持「只解釋不造像不可單獨觸發」這條 carve-out：判準要看整篇或整個作者的寫作習慣，不能單看一段就判 voiceless）

---

### H-04 — 高見龍：轉職軟體工程師的三個階段

- 來源：真人
- 作者：高見龍
- URL：https://kaochenlong.com/how-to-be-a-qualified-developer
- 發表：2019-02-08
- 語言：zh-TW
- 文體：blog
- 文體類：署名文體
- 面向：人工戲劇
- 取材：文章第二段

> 那是個還有大、小片軟碟機、家裡電腦有比較大容量的硬碟就可以在同學之間秋好一陣子的時代。當時學校教的是 QBASIC，但我完全不知道這到底要幹嘛，也不知道敲打那些指令有什麼用途，所以只好巴著當時班上幾位比較厲害的同學跟他們拷貝作業，改幾個字之後交差了事（那時候不要說什麼 Stack Overflow 可以抄了，連 Google 都還沒出生咧）。附帶一提，那時候覺得可以用貼紙把磁碟片旁邊的孔貼起來就能防止資料寫入這件事好酷！

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 大、小片軟碟機、家裡電腦有比較大容量的硬碟 | | ok | 作者隱身／零具體個人細節（具體時代物件細節，非壓縮論述——反例） |
| 那時候不要說什麼 Stack Overflow 可以抄了，連 Google 都還沒出生咧 | | ok | 零資訊警句與口號（口語破格＋具體年代梗，非破折號收尾的自我加值） |
| 用貼紙把磁碟片旁邊的孔貼起來就能防止資料寫入 | | ok | 口語化萬能詞（「貼」「防止」語意明確指向唯一動作，非含糊萬能動詞） |

**整篇判定**：clean

---

### H-05 — 高見龍：突破程式學習的「絕望沙漠」

- 來源：真人
- 作者：高見龍
- URL：https://kaochenlong.com/despite-of-desert
- 發表：2020-03-07
- 語言：zh-TW
- 文體：blog
- 文體類：署名文體
- 面向：語言句式
- 取材：文中一段（讀者內心 OS 三連問）

> 在這段期間，你會發現「你怎麼樣努力都不會進步」，好像你多學了很多知識，但這些新學的知識，卻又好像沒有辦法幫助自己到達下一個階段。於是開始懷疑自己：「我不是本科生，是不是學不會寫程式？」「我是不是該開始從底層語言開始學？是不是該去學 C 或 C++？」「我是不是沒有天份？程式應該很吃天份吧？這就是我的極限了吧？」

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 在這段期間，你會發現 | | ok | 對讀者說教（描述讀者普遍會經歷的現象，非對讀者本人下判斷；自學指南的合法第二人稱） |
| 「我不是本科生，是不是學不會寫程式？」「我是不是該開始從底層語言開始學？是不是該去學 C 或 C++？」「我是不是沒有天份？程式應該很吃天份吧？這就是我的極限了吧？」 | | ok | 破碎短句堆疊（連續三個反問句，但屬讀者內心 OS 的真實文學裝置：每句換一個具體疑慮，非省略前提的推論鏈斷裂） |

**整篇判定**：clean

---

### H-06 — 高見龍：2020 回顧與 2021 目標

- 來源：真人
- 作者：高見龍
- URL：https://kaochenlong.com/goals-for-2021
- 發表：2020-12-25
- 語言：zh-TW
- 文體：blog
- 文體類：署名文體
- 面向：內容類
- 取材：文中一段（含原文本身筆誤，保留未修正）

> 但真正最主要的原因，就是我總是喜歡冷門的玩意兒，而 Rust 就相對的夠冷門！Rust 揉合了語多種程式語言的範式（Paradigm）以及本身一些特別的設計，所以反而學習曲線相對更高了一點。我打算接下來花幾個月的時間把它好好的練一下，所以這裡可能會開始有一些 Rust 的學習筆記，順便用 Rust 做個小作品，不為別人，就只是個「為我自己學 Rust」的概念。如果學習小有成果，放心，以我這種愛現的個性，大家一定會看到我跟大家分享我的學習方式的。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 我總是喜歡冷門的玩意兒 | | ok | 空降主張（判斷句由後句「Rust 就相對的夠冷門」具體支撐，非懸空結論） |
| 以我這種愛現的個性 | | ok | 對讀者說教（此為自我評斷而非評斷讀者，性質不同） |
| 揉合了語多種程式語言的範式 | | ok | 保護清單／真人的不完美（原文真實筆誤「語多種」，保留原樣不修正——這是人味真跡，不是省略成分該標的地方） |

**整篇判定**：clean

---

### H-07 — Julia Evans：networking tool comics

- 來源：真人
- 作者：Julia Evans
- URL：https://jvns.ca/blog/2019/02/10/a-few-networking-tool-comics/
- 發表：2019-02-10
- 語言：en
- 文體：technical-blog
- 文體類：署名文體
- 面向：內容類
- 取材：開場段

> I'm pretty excited about this one – I LOVE computer networking (it's what I spent a big chunk of the last few years at work doing), but getting started with all the tools was originally a little tricky!

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| I LOVE computer networking | | ok | 情緒宣告（此為真實情緒強度標記，缺席才是 AI 味，出現屬正常人味） |
| it's what I spent a big chunk of the last few years at work doing | | ok | 模糊歸屬（具體個人經歷佐證，非假託他人權威） |
| getting started with all the tools was originally a little tricky | | ok | 避險堆疊（單一口語化限定詞，非避險堆疊） |

**整篇判定**：clean

---

### H-08 — Julia Evans：Day 56 — a little WebAssembly

- 來源：真人
- 作者：Julia Evans
- URL：https://jvns.ca/blog/2021/02/09/day-56--a-little-webassembly/
- 發表：2021-02-09
- 語言：en
- 文體：technical-blog
- 文體類：署名文體
- 面向：溝通殘留
- 取材：文中一段

> I spent a bunch of time yesterday pairing with Rachel and Jeff on figuring out how to do art in Rust! ... On my slow computer the example took maybe 10 minutes to compile, and it took about 2 minutes on my fast about.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| pairing with Rachel and Jeff | | ok | 權威名號堆砌（具名真實同事協作紀錄，非權威背書） |
| maybe 10 minutes to compile, and it took about 2 minutes on my fast about | | ok | 保護清單／真人的不完美（具體實測數字；「my fast about」是真實未修飾筆誤，非刻意模糊區間） |

**整篇判定**：clean

---

### H-09 — Julia Evans：Blog about what you've struggled with

- 來源：真人
- 作者：Julia Evans
- URL：https://jvns.ca/blog/2021/05/24/blog-about-what-you-ve-struggled-with/
- 發表：2021-05-24
- 語言：en
- 文體：technical-blog
- 文體類：署名文體
- 面向：語言句式
- 取材：文中一段

> Okay, Julia, you might be thinking – if it's about what you learned, why isn't this blog post called 'Blog about what you learned' then? Well, we've all learned lots of things! For example at some point in the last 8 years I learned Go.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| Okay, Julia, you might be thinking | | ok | 反問句開場與收尾（自我對話式反問，是作者隱身要求的口語破格，非空泛修辭開場） |
| For example at some point in the last 8 years I learned Go | | ok | 模糊歸屬（具體年限與事實，非模糊歸屬） |

**整篇判定**：clean

---

### H-10 — Simon Willison：weeknotes — Datasette Writes

- 來源：真人
- 作者：Simon Willison
- URL：https://simonwillison.net/2020/Feb/26/weeknotes-datasette-writes/
- 發表：2020-02-26
- 語言：en
- 文體：technical-blog／TIL
- 文體類：署名文體
- 面向：內容類
- 取材：文中一段

> I no longer believe this to be the case: SQLite is great at handling writes, as millions of iPhone and Android apps will attest. I've been mulling over the best way to handle this for the best part of a year... and then a couple of days ago I had a breakthrough.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| I no longer believe this to be the case | | ok | 空降主張（立場轉折由後句具體事實支撐，非懸空結論） |
| I've been mulling over the best way to handle this for the best part of a year... and then a couple of days ago I had a breakthrough | | ok | 立場真空（具體時間軸，正是應保留的第一人稱經驗） |

**整篇判定**：clean

---

### H-11 — Simon Willison：weeknotes — datasette-seaborn

- 來源：真人
- 作者：Simon Willison
- URL：https://simonwillison.net/2020/Sep/18/weeknotes-datasette-seaborn/
- 發表：2020-09-18
- 語言：en
- 文體：technical-blog／TIL
- 文體類：署名文體
- 面向：溝通殘留
- 取材：文中一段

> I demo'd it at PyCon AU a few weeks ago, and promised that a full write-up would follow. I still need to honour that promise! I'm figuring out how to provide a good interactive demo at the moment that doesn't expose my personal data.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| I still need to honour that promise! | | ok | 諂媚語氣（此為自我究責的真實語氣，非討好讀者的罐頭致謝） |
| doesn't expose my personal data | | ok | 模糊歸屬（具體隱私顧慮，非空泛歸因） |

**整篇判定**：clean

---

### H-12 — Simon Willison：One year of TILs

- 來源：真人
- 作者：Simon Willison
- URL：https://simonwillison.net/2021/May/2/one-year-of-tils/
- 發表：2021-05-02
- 語言：en
- 文體：technical-blog／TIL
- 文體類：署名文體
- 面向：內容類
- 取材：文中一段

> Just over a year ago I started tracking TILs, inspired by Josh Branchaud's collection. I've since published 148 TILs across 43 different topics. It's a great format! ... If I'm writing a blog entry, I feel like it needs to say something new.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| inspired by Josh Branchaud's collection | | ok | 權威名號堆砌（具名真實來源致意，非權威堆砌） |
| I've since published 148 TILs across 43 different topics | | ok | 空話填充（精確可查數字，非模糊區間） |
| It's a great format! | | ok | 推廣語氣（真實個人評價，非行銷推廣語） |

**整篇判定**：clean

---

### H-13 — 知識倉鼠：《晶片戰爭》解讀 3 導讀段（Tier B）

- 來源：真人
- 作者：李元魁
- URL：https://circleghost.substack.com/p/33
- 發表：2023-09-24
- 語言：zh-TW
- 文體：newsletter
- 文體類：署名文體
- 面向：內容類
- 取材：導讀段

> 為了寫這本書的解讀，有些章節的內容會反覆看、一直看，但是有些觀點看了很多次才會發現真諦，甚至啟發更深入的想法。原本以為這本書偏小眾市場，沒想到開信率依舊在 50% 左右，也收到了關鍵評論網的轉載邀請，非常感謝讀者們的支持！近兩週沒特別盯著 twitter 的資訊追 AI 新聞，其實也沒發生什麼事，如果有真的很重要事，那遲早還是會出現的，把時間拿來多閱讀與學習感覺真好。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 開信率依舊在 50% 左右，也收到了關鍵評論網的轉載邀請 | | ok | 空降主張（具體可查數字與事件，非懸空結論） |
| 非常感謝讀者們的支持！ | | ok | 零資訊警句與口號（真實致謝且緊接具體事件，非罐頭式感謝語） |
| 如果有真的很重要事，那遲早還是會出現的 | | ok | 空降斷言開場（此句在文中段，回指前句「沒特別盯 twitter」的具體行為，非指涉未交代之物） |

**整篇判定**：clean

---

### H-14 — 知識倉鼠：Anthropic 悖論解讀（Tier B）

- 來源：真人
- 作者：李元魁
- URL：https://circleghost.substack.com/p/anthropic-ai
- 發表：2026-06-15
- 語言：zh-TW
- 文體：newsletter
- 文體類：署名文體
- 面向：內容類
- 取材：文中一段

> 這集最刺人的地方，不是 Anthropic 說自己重視安全，而是它幾乎把 AI 時代的所有矛盾都壓在自己身上：要賺錢、要跑得快、要幫企業寫程式、要跟政府合作，又要說自己不是在把世界推向失控。我覺得 Dario 最誠實的一句其實是「從不信任開始是理性的」，因為這比任何安全口號都更接近現實。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 不是 Anthropic 說自己重視安全，而是它幾乎把 AI 時代的所有矛盾都壓在自己身上 | | ok | 對比句式（真實區分兩件事，非表演性對比：後句頓號串列具體列舉了矛盾內容） |
| 要賺錢、要跑得快、要幫企業寫程式、要跟政府合作 | | ok | 列舉代替論述（每項皆為具體矛盾點，非壓縮回應付） |
| 我覺得 Dario 最誠實的一句其實是「從不信任開始是理性的」，因為這比任何安全口號都更接近現實 | | ok | 空降主張（判斷句同句即給出理由「因為...」，非懸空結論） |

**整篇判定**：clean

---

### H-15 — 90s.pm.investing：畫樹方法論（Tier B）

- 來源：真人
- 作者：90s.pm.investing（筆名「90後PM」）
- URL：https://90spminvesting.substack.com/p/90spminvesting-105
- 發表：2026-04-06
- 語言：zh-TW
- 文體：分析
- 文體類：署名文體
- 面向：語言句式
- 取材：文中一段

> 上一篇我們做了一件事：猜。我們猜了一個核心假設——「市場把 NVDA 的身份搞錯了，它不是週期股，它正在變成 AI 時代的公用事業股。」這句話聽起來很有力。但它有一個致命的問題：你沒辦法證偽它。……所以我們需要下一步：把這個觀點拆開。把一個大的、模糊的、不可測試的判斷，拆成一棵樹——每一根分枝是一個更小的問題，每一片葉子是一個可以用數據回答「對」或「錯」的假設。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 它不是週期股，它正在變成 AI 時代的公用事業股 | | ok | 對比句式（具體產業分類判斷，非表演性對比） |
| 把一個大的、模糊的、不可測試的判斷，拆成一棵樹——每一根分枝是一個更小的問題，每一片葉子是一個可以用數據回答「對」或「錯」的假設 | | ok | 零資訊警句與口號（此為作者自建方法論框架的自創比喻，非零資訊重述的對仗口號——刪掉會損失「樹狀分解」這個具體方法論） |
| 你沒辦法證偽它 | | ok | 零資訊警句與口號（判斷句本身即論證核心，非破折號收尾的自我加值評語） |

**整篇判定**：clean

---

### H-16 — AI避坑情報員：Google Gemini 開場（Tier B）

- 來源：真人
- 作者：AI Trap Advisor（筆名「AI 避坑情報員」）
- URL：https://aitrapadvisor.substack.com/p/google-gemini
- 發表：2026-01-04
- 語言：zh-TW
- 文體：casual／吐槽觀點
- 文體類：署名文體
- 面向：打破第四面牆
- 取材：開場段

> 早安，各位創作者、社群小編，還有那些信箱永遠爆炸的自媒體經營者。我是你們的 AI 避坑情報員。最近 Google 很焦慮，真的很焦慮。……但我知道你們在想什麼：「情報員，這東西能用嗎？還是又是另一個讓我顯得很蠢的人工智障？」

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 早安，各位創作者、社群小編，還有那些信箱永遠爆炸的自媒體經營者 | | ok | 對讀者說教（casual／blunt voice 的 carve-out：直接稱呼讀者為同盟屬人設語域，非居高臨下評斷） |
| 我是你們的 AI 避坑情報員 | | ok | 文件自述（此為刻意經營的持續性人設暱稱，非委託場景復述或思考過程外洩） |
| 讓我顯得很蠢的人工智障 | | ok | 專有名詞過度翻譯（「人工智障」是作者自創雙關語，非生造譯名） |

**整篇判定**：clean

---

### H-17 — 工程會：投標須知範本（公文均質對照）

- 來源：真人
- 作者：行政院公共工程委員會
- URL：https://www.pcc.gov.tw/content/index?eid=9808&type=C（範本：投標須知範本 115.7.27 版）
- 發表：2026-07-27
- 語言：zh-TW
- 文體：公文／RFP
- 文體類：事務文體
- 面向：語言句式
- 取材：範本開頭條文

> 以下各項招標規定內容，由機關填寫，投標廠商不得填寫或塗改。各項內含選項者，由機關擇符合本採購案者勾填。一、本採購適用政府採購法(以下簡稱採購法)及其主管機關所訂定之規定。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 以下各項招標規定內容，由機關填寫，投標廠商不得填寫或塗改 | | ok | 作者隱身（事務文體 排除範圍：Allowed patterns「Structured uniformity in 公文 / RFP / SOP」carve-out） |
| 各項內含選項者，由機關擇符合本採購案者勾填 | | ok | 過度簡寫（此為法規慣用文書句式，非省略成分——公文體裁本身容許此密度） |

**整篇判定**：clean（此例的價值在於證明 voice：事務文體 的 gating 排除是對的——若誤啟用作者隱身，這種本該均質的公文會被大量誤標）

---

### H-18 — 工程會：工程採購契約範本（法律文書對照）

- 來源：真人
- 作者：行政院公共工程委員會
- URL：https://www.pcc.gov.tw/content/index?eid=9812&type=C（範本：工程採購契約範本 114.12.30 修正）
- 發表：2025-12-30
- 語言：zh-TW
- 文體：公文／RFP
- 文體類：事務文體
- 面向：語言句式
- 取材：第 1 條 契約文件及效力，第七款

> 契約所定事項如有違反法令或無法執行之部分，該部分無效。但除去該部分，契約亦可成立者，不影響其他部分之有效性。該無效之部分，機關及廠商必要時得依契約原定目的變更之。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 但除去該部分，契約亦可成立者，不影響其他部分之有效性 | | ok | 空降主張（可分性條款是法律慣用結構，非無依據判斷句；carve-out：Structured uniformity in 公文/RFP/SOP） |
| 機關及廠商必要時得依契約原定目的變更之 | | ok | 過度簡寫（此為法律文書標準句架，非省略主詞受詞） |

**整篇判定**：clean

---

### H-19 — RFC 7231：404 狀態碼定義（docs/spec 對照）

- 來源：真人
- 作者：IETF（RFC 7231，obsoletes RFC 2616）
- URL：https://www.rfc-editor.org/rfc/rfc7231
- 發表：2014-06
- 語言：en
- 文體：docs
- 文體類：事務文體
- 面向：內容類
- 取材：Section 6.5.4

> The 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource or is not willing to disclose that one exists. A 404 status code does not indicate whether this lack of representation is temporary or permanent; the 410 (Gone) status code is preferred over 404 if the origin server knows, presumably through some configurable means, that the condition is likely to be permanent. A 404 response is cacheable by default; i.e., unless otherwise indicated by the method definition or explicit cache controls (see Section 4.2.2 of [RFC7234]).

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| A 404 status code does not indicate whether this lack of representation is temporary or permanent | | ok | 節奏均質（規格文件本就該均質被動語態，非缺席第一人稱的 AI 味——carve-out：事務文體 docs/spec） |
| the 410 (Gone) status code is preferred over 404 if the origin server knows, presumably through some configurable means, that the condition is likely to be permanent | | ok | 避險堆疊（此為規格條件邏輯的精確限定，非避險堆疊） |
| see Section 4.2.2 of [RFC7234] | | ok | 併稿接縫（對外部權威來源的正式引用，讀者可獨立查核） |

**整篇判定**：clean

---

### H-20 — RFC 8446：TLS 1.3 引言（docs/spec 對照）

- 來源：真人
- 作者：IETF（RFC 8446）
- URL：https://www.rfc-editor.org/rfc/rfc8446
- 發表：2018-08
- 語言：en
- 文體：docs
- 文體類：事務文體
- 面向：風格版面
- 取材：Section 1 Introduction

> The primary goal of TLS is to provide a secure channel between two communicating peers; the only requirement from the underlying transport is a reliable, in-order data stream. Specifically, the secure channel should provide the following properties: [...] These properties should be true even in the face of an attacker who has complete control of the network, as described in [RFC3552].

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| Specifically, the secure channel should provide the following properties: [...] | | ok | 條列膨脹與裸名詞條列（規格文件的條列展開屬 carve-out：Allowed patterns「Structured uniformity」，且原文條列確有逐項展開，非壓縮） |
| as described in [RFC3552] | | ok | 併稿接縫（對外部權威來源的正式引用） |

**整篇判定**：clean

---

## AI 桶（A）

以主流模型生成、明確標記為機生的文本。這一桶量的是 **recall**：被標的比例越高越好。

取材守則：主題與文體盡量對齊真人桶的某一例，差異才收斂到「文風」而非「題材」。
需要有一部分是**無詞級病句的 voiceless 文**——那是結構層存在的理由，詞表抓不到。

A-01～A-08 對齊 H-01～H-16 各例的主題／文體，測詞級與段落級規則的 recall。
A-09～A-12 是**無詞級病句**的 voiceless 文（題材不對齊特定 H 例），專門測作者隱身——
這四例的判定表刻意標「全文」而非單一片段，因為缺席的是整篇的立場、細節與比喻，
不是某一句的用詞。

---

### A-01 — Docker 網路連線疑難排解（對齊 H-01）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：幫我寫一篇部落格文章，說明如何排解 Docker 容器連不到本機服務的問題
- 對齊：H-01
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 面向：內容類

> 在容器化開發的時代背景下，網路連線問題是每一位開發者都會遇到的挑戰。當容器內的服務無法連接到本機服務時，這通常牽涉到防火牆設定、網路模式選擇與埠號對應這三個環節——它們彼此環環相扣，缺一不可。首先，我們需要確認容器的網路模式；接著，檢查防火牆規則是否允許對應的連線；最後，驗證埠號對應是否正確。透過系統性的排查方法，這個問題通常可以被順利解決。值得注意的是，網路除錯不僅是技術問題，更是一種耐心的展現。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 在容器化開發的時代背景下 | | flag | 空降斷言開場（時代大帽子式鋪陳，指涉未交代之物） |
| 這通常牽涉到防火牆設定、網路模式選擇與埠號對應這三個環節——它們彼此環環相扣，缺一不可 | | flag | 零資訊警句與口號（破折號收尾自我加值＋頓號堆砌未展開） |
| 首先，我們需要確認容器的網路模式；接著，檢查防火牆規則是否允許對應的連線；最後，驗證埠號對應是否正確 | | flag | 思考過程外洩（「首先／接著／最後」指紋詞，思考過程外洩） |
| 網路除錯不僅是技術問題，更是一種耐心的展現 | | flag | 對比句式（不僅…更…句式，空泛昇華結尾） |

**整篇判定**：flagged — 空降斷言開場、零資訊警句與口號、思考過程外洩、對比句式

**預期方向**：刪時代大帽子開場，改從具體錯誤現象切入；三個排查步驟合併成一段連貫散文而非
「首先／接著／最後」清單；刪「不僅是技術問題更是耐心的展現」收尾，若要收尾就寫具體排查結果。

---

### A-02 — Wiki 編輯器工具比較（對齊 H-02）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：寫一篇文章比較 Azure DevOps Wiki 線上編輯器跟用 VS Code 寫 Markdown 的差異
- 對齊：H-02
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 面向：內容類

> 選擇合適的文件協作工具，對團隊的知識管理至關重要。Azure DevOps 提供了內建的 Wiki 線上編輯器，但許多開發者也會選擇搭配 Visual Studio Code 進行 Markdown 撰寫。這兩種方式各有優缺點，最終還是取決於團隊的使用習慣與工作情境。無論選擇哪一種工具，持續保持文件的即時更新，才是知識管理成功的關鍵。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 對團隊的知識管理至關重要 | | flag | 意義膨脹（家族詞，空泛升值） |
| 這兩種方式各有優缺點，最終還是取決於團隊的使用習慣與工作情境 | | flag | 立場真空（讀完不知道作者實際建議什麼，兩句都是誰都同意的緩衝） |
| 無論選擇哪一種工具，持續保持文件的即時更新，才是知識管理成功的關鍵 | | flag | 萬用收尾（萬用收尾，任何工具比較文章都能接） |

**整篇判定**：flagged — 意義膨脹、立場真空、萬用收尾

**預期方向**：「至關重要」改成平述句；立場真空段改成作者實際的建議（用哪個工具、為什麼）；
萬用收尾換成具體下一步（例如「持續更新的文件才有用，不在於用哪個編輯器」）。

---

### A-03 — 轉職心態鼓勵文（對齊 H-04／H-05／H-06）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：寫一篇部落格文章，鼓勵想轉職軟體工程師的讀者不要放棄
- 對齊：H-04, H-05, H-06
- 語言：zh-TW
- 文體：blog
- 文體類：署名文體
- 面向：打破第四面牆

> 你是否也曾懷疑過，自己是不是不適合走上程式設計這條路？這樣的想法，其實每一位轉職工程師都曾經歷過。學習程式的路上充滿挑戰，但只要堅持下去，終究會看到成果。與其擔心自己不夠聰明，不如把時間拿來持續練習——畢竟，機會永遠留給準備好的人，不是嗎？

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 你是否也曾懷疑過，自己是不是不適合走上程式設計這條路？ | | flag | 對讀者說教（開場即以反問對讀者本人下判斷式喊話，非描述操作或列舉讀者可能的具體疑慮——對照 H-05 的三連問各自換一個具體場景，此句只有一個空泛提問） |
| 學習程式的路上充滿挑戰，但只要堅持下去，終究會看到成果 | | flag | 萬用收尾（萬用勵志語，無具體行動或案例） |
| 與其擔心自己不夠聰明，不如把時間拿來持續練習——畢竟，機會永遠留給準備好的人，不是嗎？ | | flag | 反問句開場與收尾（「與其…不如…」＋格言＋反問三合一勸誡收尾） |

**整篇判定**：flagged — 對讀者說教、萬用收尾、反問句開場與收尾

**預期方向**：反問式對讀者下判斷的開場改寫成第三人稱陳述這個現象常見；萬用勵志語換成具體
行動建議；「與其…不如…畢竟…不是嗎？」三合一收尾整段刪或換成作者自己的具體案例。

---

### A-04 — Kubernetes 網路除錯（對齊 H-07／H-08／H-09）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：Write a blog post explaining how to debug networking issues in Kubernetes.
- 對齊：H-07, H-08, H-09
- 語言：en
- 文體：technical-blog
- 文體類：署名文體
- 面向：溝通殘留

> Networking issues in Kubernetes can be frustrating to debug. It's important to understand the underlying components: pods, services, and ingress controllers all play a role. First, check whether the pod is running correctly. Next, verify that the service is correctly routing traffic. Finally, confirm that DNS resolution is working as expected. By following this systematic approach, most networking issues can be resolved efficiently.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| Networking issues in Kubernetes can be frustrating to debug | | flag | 情緒宣告（宣告式陳述情緒，非真實第一人稱經驗——對照 H-07 的 "I LOVE computer networking"） |
| First, check whether the pod is running correctly. Next, verify that the service is correctly routing traffic. Finally, confirm that DNS resolution is working as expected. | | flag | 思考過程外洩（First/Next/Finally 指紋詞） |
| By following this systematic approach, most networking issues can be resolved efficiently | | flag | 萬用收尾（萬用收尾，任何除錯文章都能接） |

**整篇判定**：flagged — 情緒宣告、思考過程外洩、萬用收尾

**預期方向**：刪「can be frustrating to debug」這句宣告式情緒開場；First/Next/Finally 三步驟
合併成連貫散文；萬用收尾換成具體結果或殘留的注意事項。

---

### A-05 — 快取策略 TIL（對齊 H-10／H-11／H-12）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：Write a TIL-style post about caching strategies in web applications.
- 對齊：H-10, H-11, H-12
- 語言：en
- 文體：technical-blog／TIL
- 文體類：署名文體
- 面向：內容類

> Today I learned about different caching strategies for web applications. Caching can significantly improve application performance. There are several approaches: cache-aside, write-through, and write-behind. Each has its own trade-offs in terms of consistency and complexity. Understanding these trade-offs is essential for building performant systems.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| Caching can significantly improve application performance | | flag | 空話填充（泛泛陳述，非具體實測數據——對照 H-12 的「148 TILs across 43 different topics」） |
| cache-aside, write-through, and write-behind | | flag | 條列膨脹與裸名詞條列（三個策略名詞並列，皆未展開） |
| Understanding these trade-offs is essential for building performant systems | | flag | 萬用收尾（萬用收尾） |

**整篇判定**：flagged — 空話填充、條列膨脹與裸名詞條列、萬用收尾

**預期方向**：「can significantly improve performance」換成具體實測數字；三個策略名詞各展開
一句說明取捨；萬用收尾換成作者實際偏好哪一種、為什麼。

---

### A-06 — AI 安全報導解讀（對齊 H-13／H-14）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：寫一篇電子報，解讀一篇關於 AI 安全的英文報導
- 對齊：H-13, H-14
- 語言：zh-TW
- 文體：newsletter
- 文體類：署名文體
- 面向：事實與引用

> 這篇報導揭示了 AI 產業一個值得深思的現象：業界普遍認為，安全與商業利益之間存在著微妙的平衡。不少專家也表示，這樣的矛盾恐怕短期內難以解決。這不僅是技術問題，更是整個產業必須共同面對的挑戰。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 業界普遍認為 | | flag | 模糊歸屬（無來源的權威鋪墊——對照 H-14 具名的「Dario」與可查的具體矛盾清單） |
| 不少專家也表示 | | flag | 模糊歸屬（同一段第二層模糊歸屬堆疊） |
| 這不僅是技術問題，更是整個產業必須共同面對的挑戰 | | flag | 對比句式（不僅…更…，空泛昇華收尾，無具體立場） |

**整篇判定**：flagged — 模糊歸屬（雙重）、對比句式

**預期方向**：「業界普遍認為」「不少專家也表示」各補上具體來源或改成作者自己的觀察；
「不僅是技術問題更是…挑戰」換成作者自己對這篇報導的實際判斷。

---

### A-07 — 投資假設拆解方法論（對齊 H-15）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：寫一段投資分析方法論介紹，說明如何拆解一個投資假設
- 對齊：H-15
- 語言：zh-TW
- 文體：分析
- 文體類：署名文體
- 面向：語言句式

> 在分析任何投資標的時，我們都必須誠實面對自己的假設。一個好的分析框架，應該要能夠系統性地拆解問題，並且用數據驗證每一個環節。唯有秉持科學精神，才能避免落入敘事陷阱。這正是嚴謹分析與童話故事的根本差異。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 我們都必須誠實面對自己的假設 | | flag | 零資訊警句與口號（祈使句形態的道德化評語，無具體方法支撐） |
| 一個好的分析框架，應該要能夠系統性地拆解問題，並且用數據驗證每一個環節 | | flag | 空降斷言開場（丟出「系統性拆解」概念但未具體說明怎麼拆，缺乏 H-15 那種「一根分枝一個小問題」的可操作細節） |
| 這正是嚴謹分析與童話故事的根本差異 | | flag | 對比句式（套用 H-15 作者已建立的「科學 vs 童話」框架，但沒有自己的落地應用，是空泛借殼而非自創比喻） |

**整篇判定**：flagged — 零資訊警句與口號、空降斷言開場、對比句式

**預期方向**：「我們都必須誠實面對」祈使式評語改成直接陳述作法；「系統性拆解問題」補上
實際怎麼拆（哪個假設、拆成哪些子問題）；借用他人「科學 vs 童話」框架的收尾整段刪，
除非作者自己有等重的落地應用可以接上。

---

### A-08 — AI 行銷話術吐槽開場（對齊 H-16）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：用吐槽語氣寫一段開場，提醒讀者不要被 AI 行銷話術騙
- 對齊：H-16
- 語言：zh-TW
- 文體：casual／吐槽觀點
- 文體類：署名文體
- 面向：打破第四面牆

> 各位朋友，AI 工具日新月異，行銷話術也是層出不窮。今天想跟大家聊聊，怎麼分辨真正有用的工具跟純粹的噱頭。老實說，市面上充斥著各種誇大宣傳，我們都應該保持理性判斷。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| AI 工具日新月異，行銷話術也是層出不窮 | | flag | 空降斷言開場（「日新月異」「層出不窮」四字空話，無具體工具或案例——對照 H-16 直接點名 Google Gemini） |
| 今天想跟大家聊聊 | | flag | 公式化開場（AI 部落格開場慣用套語，非真實人設互動——對照 H-16 的固定暱稱「我是你們的 AI 避坑情報員」） |
| 老實說，市面上充斥著各種誇大宣傳，我們都應該保持理性判斷 | | flag | 萬用收尾（萬用理性呼籲，缺 H-16 那種具體吐槽對象與自創詞彙「人工智障」） |

**整篇判定**：flagged — 空降斷言開場、公式化開場、萬用收尾

**預期方向**：「日新月異」「層出不窮」換成具體工具或案例；刪「今天想跟大家聊聊」直接進主題；
萬用理性呼籲換成作者對某個具體話術的實際吐槽判斷。

---

### A-09 — CI/CD 概念介紹（voiceless，詞級乾淨）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：寫一篇部落格文章介紹 CI/CD pipeline 的基本概念
- 對齊：n/a（無詞級病句探針，非對齊特定 H 例）
- 語言：zh-TW
- 文體：technical-blog
- 文體類：署名文體
- 面向：內容類

> 持續整合與持續部署（CI/CD）是現代軟體開發流程中常見的實踐方式。持續整合指的是開發者頻繁地將程式碼變更合併到主要分支，並透過自動化測試驗證程式碼品質。持續部署則進一步將通過測試的程式碼自動部署到生產環境。導入 CI/CD 流程可以縮短開發週期，並降低人為疏失發生的機率。許多團隊會使用像是 GitHub Actions、GitLab CI 或 Jenkins 等工具來建立自己的流水線。整體而言，CI/CD 是提升軟體交付效率的重要一環。

（word-level：無 Tier-1/2 病句，詞彙皆為正確技術陳述——這正是本例的價值所在，詞表在這種文本上會全數放行。）

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 全文 | | flag | 作者隱身／立場真空（zero stance：沒有一句作者判斷句，以「整體而言」收場） |
| 全文 | | flag | 作者隱身／零具體個人細節（沒有一個具體時間、次數、場景；純定義式陳述） |
| 全文 | | flag | 作者隱身／只解釋不造像（CI/CD 全用定義式解釋，無自創比喻） |

**整篇判定**：flagged — 作者隱身（三項訊號成群觸發，符合「需與其他結構訊號成群才計入」的門檻，非單條）

**預期方向**：作者隱身是 detect-only，不代筆——只提示作者補入一次具體踩坑經驗（哪個 pipeline、
卡在哪一步）、一句自己的立場（例如偏好哪套工具鏈、為什麼）、一個自創比喻，不由 skill 自己生出這些內容。

---

### A-10 — REST API 設計原則（voiceless，word-level clean）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：Write a short technical blog post explaining REST API design principles.
- 對齊：n/a
- 語言：en
- 文體：technical-blog
- 文體類：署名文體
- 面向：語言句式

> REST is an architectural style for designing networked applications. RESTful APIs use standard HTTP methods such as GET, POST, PUT, and DELETE to perform operations on resources. Each resource is identified by a unique URI, and interactions are stateless, meaning each request contains all the information needed to process it. Following REST principles can make APIs more predictable and easier to maintain. Many modern web services adopt this style when building their public interfaces.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 全文 | | flag | 立場真空（無任何 "I think"／個人偏好／實際踩坑經驗） |
| 全文 | | flag | 詞彙處理失真（低 TTR：反覆使用 resource／stateless／RESTful 等固定詞彙圈，句長也高度均一） |
| 全文 | | flag | 作者隱身／只解釋不造像（純定義式解釋，無一個把抽象概念拉到具體經驗的比喻） |

**整篇判定**：flagged — 立場真空、詞彙處理失真、作者隱身／只解釋不造像（三項成群）

**預期方向**：detect-only，不代筆——只提示作者補一句自己對 REST 的實際偏好或踩過的坑、
一個把抽象概念（stateless、resource）拉到具體經驗的自創比喻。

---

### A-11 — 時間管理方法分享（voiceless）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：寫一篇部落格文章分享時間管理的方法
- 對齊：n/a
- 語言：zh-TW
- 文體：blog
- 文體類：署名文體
- 面向：內容類

> 時間管理是每個人都需要面對的課題。常見的時間管理方法包括番茄工作法、時間區塊法與待辦清單法。番茄工作法將工作切分為 25 分鐘的專注時段，中間穿插短暫休息；時間區塊法則是預先為每項任務分配固定時段；待辦清單法則著重於任務的排序與追蹤。選擇適合自己的方法，並且持續實踐，是提升生產力的關鍵。

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 全文 | | flag | 作者隱身／零具體個人細節（列舉三種方法但無一次作者自己實際使用某方法的具體場景） |
| 全文 | | flag | 作者隱身／立場真空（沒有一句「我後來選了 X，因為 Y」的判斷，以「選擇適合自己的方法」中立收場） |
| 選擇適合自己的方法，並且持續實踐，是提升生產力的關鍵 | | flag | 萬用收尾（萬用收尾，任何時間管理文章都能接） |

**整篇判定**：flagged — 作者隱身（兩項成群）、萬用收尾

**預期方向**：detect-only，不代筆——只提示作者補一次自己實際用哪種方法、用了多久、
效果如何；萬用收尾若要保留，換成作者自己的具體選擇與理由。

---

### A-12 — 遠端工作生產力電子報開場（voiceless）

- 來源：AI
- 模型：Claude Opus 5
- 生成：2026-07-28
- prompt：Write a short newsletter intro paragraph about staying productive while working remotely.
- 對齊：n/a
- 語言：en
- 文體：newsletter
- 文體類：署名文體
- 面向：溝通殘留

> Remote work has become increasingly common in recent years. Staying productive while working remotely requires discipline and the right habits. Setting a consistent schedule, creating a dedicated workspace, and taking regular breaks are all effective strategies. Many professionals find that these small adjustments make a meaningful difference over time.

| 引文片段 | # | 判定 | 規則 |
|---|---|---|---|
| 全文 | | flag | 立場真空（無任何個人經驗或偏好陳述） |
| Setting a consistent schedule, creating a dedicated workspace, and taking regular breaks | | flag | 條列膨脹與裸名詞條列（三個策略並列，未展開任何一項的具體做法） |
| Many professionals find that these small adjustments make a meaningful difference over time | | flag | 模糊歸屬（「many professionals」無來源的權威鋪墊） |

**整篇判定**：flagged — 立場真空、條列膨脹與裸名詞條列、模糊歸屬

**預期方向**：detect-only，不代筆——只提示作者補一句自己遠端工作的實際經驗或偏好；
三個並列策略至少展開一項說明實際怎麼做；「many professionals」換成具體來源或作者自己的觀察。

---

## Coverage matrix

8 個缺陷類別 + 2 個正交機制 × 覆蓋狀況。一眼看出哪個面向沒有 case 罩著。

`SF` 欄＝有 AI 桶案例證明它抓得到（recall）；`SNF` 欄＝有真人桶案例證明它不誤傷（false positive）。
兩欄都空的面向就是缺口——這張表的用途是把缺口變得看得見，不是記錄成績。

**這張表由判定列的「規則」欄推導，不由每例的「面向」欄推導。** 兩者不同：`面向` 是
建語料時替**整例**選的最具代表性一軸，一例的判定列常橫跨數個類別，所以用 `面向` 統計
會同時漏報與誤報。2.0.0 重新分類規則後，本表改以「這個類別底下的規則，有沒有實際出現在
某一列」為準——`flag` 列進 SF 欄，`ok` 列進 SNF 欄。各例的 `面向` 欄保留原值不動
（它記錄的是建語料當時的意圖，不是覆蓋統計的基礎）。

`保護清單`／`長文scope` 兩個正交機制在本檔幾乎沒有原生案例，覆蓋主要交給 `evals.json`。
跑分時應與 evals.json 的覆蓋合併看，不要只看本表。

| 缺陷類別／機制 | SF（AI 桶案例） | SNF（真人桶案例） | 缺口 |
|---|---|---|---|
| 內容類 | A-02, A-03, A-04, A-05, A-08, A-11 | H-12 | **SNF 偏薄**：只有一例真人文的 `ok` 列落在內容類，對「具體但樸素的敘述不該被當空話」這一側的保護力量測不足 |
| 語言句式 | A-01, A-06, A-07, A-10 | H-01, H-04, H-05, H-07, H-13, H-14, H-15, H-16, H-17, H-18, H-19 | — |
| 風格版面 | A-05, A-12 | H-14, H-20 | — |
| 溝通殘留 | *(無)* | H-11 | **SF 缺口**：本檔沒有 AI 桶案例帶對話介面殘留、諂媚語氣、知識截止免責或 AI 工具殘留標記。這一類是 P0，卻只有真人側的反例——recall 完全交給 `evals.json`（ids 23／24／27／32），本檔無真實文本可對照 |
| 事實與引用 | A-06, A-12 | H-07, H-08, H-09, H-11, H-12 | — |
| 立場與開場 | A-01, A-02, A-03, A-07, A-08, A-09, A-10, A-11, A-12 | H-01, H-02, H-03, H-04, H-05, H-06, H-09, H-10, H-13, H-14, H-16, H-17, H-18 | — |
| 人工戲劇 | A-04 | H-07 | 兩側各只有一例，樣本薄 |
| 打破第四面牆 | A-01, A-04 | H-16, H-19, H-20 | — |
| 保護清單（機制） | *(無)* | H-06, H-08 | SNF 側有兩例（真人筆誤保留）；SF 側不適用——保護清單是抑制機制，沒有「該標而未標」的一側。其餘覆蓋交給 `evals.json` ids 40／41／42／46 |
| 長文scope（機制） | *(無)* | *(無)* | 本檔無原生案例；覆蓋交給 `evals.json` id 6、35、51 |

**本輪最有價值的產出是這張表的空格，不是滿格。** 目前真正的洞是**溝通殘留的 SF 側**
（一個 P0 類別在真實語料上完全沒有 recall 樣本）與**內容類的 SNF 側**，其次是人工戲劇
兩側的樣本厚度。下一輪補語料應從這三處下手。

# infographic-design — 開發指南

給接續開發此 skill 的人或 agent。SKILL.md 與 references/ 依 repo 規範不含
開發過程,所以「為什麼長這樣」「改的時候要守什麼」寫在這裡。

這是**指南不是日誌** —— 只寫還會影響下一次修改的結論。逐批的過程記在
git history,`git log --follow skills/infographic-design/` 可查。

兩套外部標準:**怎麼寫 skill** 依 `writing-great-skills`(mattpocock/skills)
的詞彙與判準;**怎麼評測 skill** 依官方 `skill-creator`。兩者範圍不同,
少數重疊處(描述長度、禁令寫法)**以 writing-great-skills 為準**。

---

## 1. 定位與邊界

**這是一把解釋性圖示(explanatory graphic)的刀,不是通用資訊圖表工具。**

名字沿用 `infographic-design`(那是使用者實際會搜的詞),但實質重心在
機制圖:泳道、有向流、payload、推導關係。整條開發史上每一張成功的產出
都是機制圖,沒有一張是資料驅動的。

邊界寫在 description 裡,兩句話決定要不要接:

- **數字本身就是主題**(年度業績、問卷結果、需要精確尺度)→ 轉手給
  data-visualization workflow,不接。
- **數字是解釋裡的證據**(漏斗流失率、快取命中率)→ 接,依
  `references/charts.md` 的嵌入形式處理。

其他轉手:投影片 → pptx skill;白話解釋名詞 → plain-speak。

**invocation:model-invoked,而且沒有取捨空間。** `knowledge-doc-writing`
在產文件的過程中會叫這個 skill 設計圖表。user-invoked 會把 description 從
agent 的可及範圍拿掉,**其他 skill 就叫不動它** —— 所以 description 必須
留著,它的 context 成本是永久的、每一輪都在付。既然躲不掉,就得把它壓到
最小:只留分支觸發語與觸及條款,身分敘述交給本體。

**嵌入模式是一條分支。** 被別的 skill 叫來畫文件裡的 figure 時,宿主擁有
外觀、本 skill 擁有內容:色彩與字體讓給宿主的 token(蓋掉 step 7 與
`color-typography.md`),step 9 的交付 gate 由宿主的檢查取代(那道 gate 守的
是獨立畫布,不描述頁面裡的一張圖),格式由宿主決定。內容規則全數照舊。
這條契約**兩邊都要寫**:只寫在呼叫端,改 step 7 或 gate 的人不會知道有人
依賴著覆蓋它。

---

## 2. 檔案架構:誰擁有什麼

`SKILL.md` 是**索引不是手冊**。九個步驟各自只留決策點,細節一律在
references。新內容要放哪,先問「這條規則在哪個時刻開火」:

| 檔案 | 擁有的主題 |
|---|---|
| `SKILL.md` | 九步驟工作流與各步的決策點;每個 reference 的入口 |
| `references/bytebytego-style.md` | 編號走查風格、基準位置的資訊密度 |
| `references/layouts.md` | archetype 選擇與 dial 位置如何改變密度 |
| `references/charts.md` | 解釋中的量值:hero 數字、比例塊、嵌入形式、誠實規則 |
| `references/color-typography.md` | 配色推導、字級、表面詞彙(卡片/色帶/註記) |
| `references/icons.md` | 圖示規格:24×24、currentColor、symbol/use |
| `references/svg-construction.md` | SVG 機制、CJK、HTML 輸出與 flow 動畫基準、頁框 |
| `references/words.md` | 標籤與文案:讀者視角、一物一名、字數預算 |
| `references/learn-loop-viz.md` | 學習對話回顧這一個路線的專屬規則 |
| `scripts/` | 客觀檢查(見「評測」) |

**放置判準 —— 用 branch 測試。** 這個 skill 有幾條分支(一般解釋圖、
學習回顧、既有圖評估)。**每條分支都需要的,寫在 SKILL.md 裡;只有部分
分支會走到的,推到 reference 後面用 context pointer 指過去。** 指標的
**措辭**決定 agent 會不會、多可靠地取用那份材料 —— 目標檔案本身不決定。

推太少則頂層臃腫,推太多則藏起 agent 真正需要的東西;這個張力就是全部
的決定。踩過的坑:好規則寫進特例檔,只在那個特例開火。加東西到具名圖表
類型之前,逐條問「這條真的只有這個分支會用嗎」—— 通常只有一兩句是。

同一層裡用 **co-location**:一個概念的定義、規則、例外放在同一個標題下,
讀到其中一段就會連帶讀到旁邊那幾段。

---

## 3. 不可打破的不變量

每條後面是它存在的理由。理由比規則更難被誤用,所以理由不能刪。

1. **一則訊息先於任何版面。** 這是 infographic 與 data viz 的定義分界
   (Cairo:infographic 是作者編輯過的觀點;data viz 讓讀者自己下結論),
   不是風格偏好。
2. **標題內嵌在畫布裡。** 圖被單獨轉貼時仍須自足(Kosara:infographic
   是自足的)。
3. **基準位置固定,旋鈕拉動需目的 + 出處。** step 1 的核心。留存拉動
   (redundancy + familiarity)才授權雙重詞彙,且第二個名字必須有來源
   ——對話裡教過的、受眾自己的用語,絕不畫圖時發明。
4. **顏色不得單獨承載語意。** 也適用於動態:多種 flow 各配自己的 dash
   pattern,因為灰階列印與截圖同樣會失效。
5. **一種表面 = 一個意思。** 把註記畫成卡片,讀者會把旁白讀成機制的
   零件。
6. **章節序 = 概念相依鏈**(learn-loop 路線)。每節踩在前一節的 a-ha
   上;禁止重排成參考文件或請求旅程順序。對話自己的收斂句通常是旅程序,
   它只屬於 payoff band。
7. **gate 只擋讀者會實際受害的缺陷。** 風格問題一律 advisory。混進
   風格判斷會讓 gate 失去「擋下就是真的壞了」的意義。
8. **不得在 prose 重述 check 已經強制的事。** 重述只是增加 context
   成本;未被強制的清單項目該改寫成在決策點開火的生成式規則。
9. **兩個 reference 打架時,白紙黑字調解。** 例外綁在**目的與出處**上,
   雙向交叉引用。「僅限留存圖、僅限對話教過的名字」經得起邊界案例,
   「某某風格允許」不行。
10. **正面陳述目標行為,讓被禁的那個選項根本不被提起。** 用禁令操舵會
    反效果:說「別想大象」等於點名大象,反而讓它更容易被取用。只有在
    某條界線**無法用正面語句表達**時才保留禁令,而且必須同時寫出改做
    什麼。這也順帶解決另一個病:純禁令在混亂情境會靜默失效 ——
    「照被教的順序」在真實對話迂迴時會被讀成「抄逐字稿」,而正面版
    「依概念相依鏈排序,每節踩在前一節的 a-ha 上」直接告訴 agent
    遇到岔路怎麼辦。

---

## 4. 步驟、完成條件、leading word

**步驟要停在可判定的完成條件上。** SKILL.md 的九步是有序動作,每一步都該
有一個「怎樣算做完」的條件,而且 agent 自己判得出來(能分辨做完與沒做完),
必要時還要**窮盡**(「每一個文字元素都檢查過」而不是「檢查文字」)。條件
含糊招來的病叫 **premature completion**,診斷與解法見「撰寫層的失效模式」。

**leading word 是最省 token 的操舵方式。** 一個模型預訓練裡就有的緊湊概念,
在文中重複出現,會累積出分散式定義,用最少 token 錨住一整片行為。本 skill
兩個運作中的 leading word 是 **dial**(旋鈕拉動)與 **base position**
(旋鈕的固定原位)。dial 把「要不要加比喻」從品味變成有規則可依的決定。
base position 早期很弱 —— 出現幾次但彼此不相干、只是被動佈景;強化的做法
不是換詞(references 已把它當共用詞彙,換掉要動五個檔),而是讓它在工作流
兩端各開一次火:step 1 **宣告**交在哪一格,step 9 **驗證**真的交在那格,
中間用「declare / declared」這條線把兩端縫起來。一個只出現一次的核心概念
是最容易變成 no-op 的;讓它在每個決策點重複開火才站得住。

改寫時主動找機會**把重複的說法收攏成一個 leading word**:同一個意思在三處
展開,或描述花一整句去繞一個概念,都是可以塌縮成一個詞的訊號。收穫是雙重的
—— token 更少,而且 agent 有更利落的掛鉤。

## 5. 撰寫層的失效模式

用來診斷「這個 skill 怪怪的」時該往哪看:

- **premature completion** —— 步驟提早收手。先磨利完成條件(便宜、局部);
  只有在條件本質上無法明確、而且確實觀察到搶快時,才用拆分把後續步驟移出
  視線。
- **duplication** —— 同一個意思出現在兩處。除了維護與 token 成本,還會讓
  那個意思在資訊階梯上的**顯著度超過它的真實位階**。
- **sediment** —— 陳舊的層層堆積。因為「加」感覺安全、「刪」感覺有風險,
  這是任何沒有修剪紀律的 skill 的預設命運。
- **sprawl** —— 就是太長,即使每一行都還活著且唯一。解法是資訊階梯:
  把 reference 揭露到指標後面,並依分支或序列拆分。
- **no-op** —— 模型本來就會照做的話,付了 context 成本卻沒改變任何行為。
  測試:它相對於預設行為改變了什麼?**逐句**測而不是逐行測,失敗就刪掉
  整句而不是修剪字詞,而且要狠 —— 大多數失敗的散文該刪,不是改寫。
  弱的 leading word(agent 本來就大致做得到時說「要仔細」)也是 no-op,
  解法是換更強的詞,不是換技巧。
- **negation** —— 見「不可打破的不變量」第 10 條。

## 6. 借用外部內容的規矩

本 skill 有一部分改寫自 Anthropic 官方 `frontend-design`(Apache-2.0),
`NOTICE` 記錄了範圍。日後再借:

1. 先確認授權,更新 `NOTICE`,寫明改寫方式。
2. **逐段做適用性盤點**,不要整節搬。domain-general 的近乎逐字保留
   (改寫比逐字更容易失真);web 專屬的(錯誤狀態、空畫面)排除 ——
   抄進來是噪音不是嚴謹。
3. 例子與詞彙改寫到本領域(把 web UI 換成圖表),原則本身不動。

---

## 7. 修改流程

每次改動照這個順序,少一步就會有暗傷:

```bash
# 1. 改 SKILL.md / references / scripts / evals

# 2. 版本號:frontmatter version 每批必bump
#    行為改變 → minor;措辭與修補 → patch

# 3. 產一張真圖驗證(不要只讀 diff)
python3 scripts/check.py out.svg --bg "#F7F9FC" --pad 10

# 4. 收尾檢查:開發語彙不得外洩到 skill 本體
grep -rnE 'GAN|round [0-9]|benchmark|補強|比對〈|般化|eval #|recall' \
  SKILL.md references/

# 5. 孤兒檢查:每個 reference 都要能從 SKILL.md 到達
for f in references/*.md; do
  grep -q "$(basename $f)" SKILL.md || echo "ORPHAN: $f"; done

# 6. 清掉 __pycache__ 再提交
```

**兩段式提交**:skill 與 evals 一個 commit,repo 根層的 `CLAUDE.md` /
`DEVELOPMENT.md`(全域撰寫指南)另一個 commit。

---

## 8. 評測

評測遵循官方 skill-creator 的標準,本節只記**原則與本 skill 專屬的部分**;
流程細節不在這裡複述,需要時直接讀 skill-creator。

檔案(官方版位:evals 放在 skill 目錄內):

- `evals/evals.json` —— 任務題與可驗證陳述
- `evals/trigger-queries.json` —— 觸發/不觸發查詢,供描述最佳化使用
- `evals/judged-cases.md` —— 使用者已判定過的案例,質性評估用

原則:

1. **設計品質不要硬塞成 expectation。** 官方標準明講,主觀產出的技能適合
   質性評估。`expectations` 只寫**客觀可驗**的陳述(長條是否從零起、
   payload 是否在箭頭上、對比是否達標、文字是否溢框);「版面好不好看」
   「密度會不會太高」屬於質性,走 `judged-cases.md`。
   之前有一版塞了 31 條斷言而只有 4 條客觀,其餘由寫規則的同一模型判定
   —— 那量的是內部一致性,不是品質。
2. **陳述以讀者結果措辭,不以規則複讀措辭。**「讀者能只憑圖驗證推導」
   可以由不知道規則的人盲評;「圖上有收斂箭頭」只是把規則再唸一次。
3. **改進既有 skill 時,對照組是舊版快照,不是 vanilla。** 這個 skill
   早就過了「有沒有比沒 skill 好」的階段;有意義的問題是「這版比上一版
   好嗎」。
4. **兩側必須平行且互不知情。** 對照組要由獨立 subagent 跑、與實驗組
   同時派出。這是唯一能解掉污染的作法 —— 同一個 agent 先讀了 skill 再
   假裝沒讀,產出的對照組沒有證據力。若環境不支援 subagent,只能採信
   **負面發現**(「對照組有而我們沒有」不受污染影響),不可採信正面結論。
5. **同一設定多跑幾次看變異。** 單次結果分不出真實差異與抽樣雜訊。
6. **題目來源要在 skill 之外。** 從 skill 自己的宣稱反推題目,只會在
   想得到的地方受檢驗。看 track record:一套題若從沒抓到過它不是為了抓
   而設計的東西,那本身就是結論。
7. **本 skill 專屬的客觀層是 `scripts/check.py`。** 錨在 WCAG、XML、
   幾何、文字度量上,與作者無關,可無人值守跑。它衡量工藝地板,不衡量
   品質 —— 全綠只代表沒有明顯壞掉。

## 9. 環境陷阱

- `cairosvg` 不解析 CSS `var()` —— 直接 render 會全黑。務必從已展開變數
  的副本產圖(`check.py` 內部自行展開,不受影響)。
- `grep -c` 命中 0 時 exit code 1,會在 `&&` 鏈裡中斷後續指令。
- `sh` 沒有 process substitution。
- 批次編輯腳本一律加 `assert`,否則錨點字串對不上時會靜默不改 ——
  本專案已經因此漏寫過一次紀錄。
- 提交前清 `scripts/__pycache__`。

---

## 10. 知識基礎的出處

References 裡的具體數字(8px spacing、palette hex、type scale)是綜合
下列來源後的**編輯決策**,不是引用,可依實測調整。

- **版面與視覺層級**:Visme、Venngage、Piktochart、Toptal、Hull
  University LibGuide(三層 hierarchy 上限)、F/Z reading patterns。
- **圖表誠實性**:Tufte(data-ink ratio、chartjunk、graphical integrity)
  ＋ Frank Elavsky 對 minimalism 的批判(別為了 ratio 犧牲對比)。
- **無障礙**:WCAG 2.1 —— 文字 4.5:1(SC 1.4.3)、非文字圖形 3:1
  (SC 1.4.11)、color-only encoding 禁令。
- **60/30/10 色彩結構**:設計圈慣例,非單一出處。
- **infographic 的定義與旋鈕模型**:Cairo《The Functional Art》
  (visualization wheel 六軸、engineers vs journalists 兩端)、Kosara
  (hand-crafted、self-contained)、Tufte–Holmes 的 chartjunk 之爭與
  Bateman 等人的記憶性實驗(裝飾提升記憶但作者拒絕當通則)。
- **ByteByteGo 風格**:wey-gu 的 gist ＋ Alex Xu 推文(工具為 draw.io,
  招牌是連接線 flow 動畫)、ByteByteGo newsletter 原文(編號走查、
  具體實體接地)、javinpaul 的解析(progressive reveal)。歸納出的簽名
  = 編號走查焊在有向流上 + 一圖一點 + 具體範例實體 + 分類格狀變體;
  刻意只留技法、不綁 draw.io。
- **文案**:改寫自官方 `frontend-design` 的寫作段落(見 `NOTICE`)。

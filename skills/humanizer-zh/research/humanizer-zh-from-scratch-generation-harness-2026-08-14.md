# humanizer-zh 用於從零生成文件的有效性研究

日期：2026-08-14

問題：`humanizer-zh` 是否適合用在沒有既有稿件、由生成式 AI 從零產出文件的場景？

判準：以生成式 AI 的生成機制與 agent harness 的第一性原理，區分「能不能被接進流程」與「是否適合負責這個工作」。

## 結論

`humanizer-zh` 可以有效接在從零生成流程的後段，但不適合直接承擔從零生成。

最合適的定位是 `generator -> humanizer audit/rewrite -> fidelity and quality gates`，其中 humanizer 是獨立的編輯器與表面品質檢查器，不是 generator 的內嵌人格提示。

它能降低已生成稿件中的 AI 腔、對話殘留、空話、格式化句式與不當自我背書，也能在發現內容空洞時要求補資料。

它不能從空白狀態產生作者經驗、立場、來源、事實、文件結構或真正的聲音。

因此，若「有效」只指降低可辨識的 AI 寫作表面特徵，後處理可能有效；若「有效」指令文件可發布、事實可靠、符合體裁且具有作者性，單獨使用不足以成立。

目前 repo 中沒有直接證明「從零生成 + humanizer」優於其他流程的 A/B 實驗。

這份結論是由現行 skill 契約、既有 eval 形狀、第一方 harness 指引與原始研究共同推導，不能冒充該流程已完成的實驗結果。

## 一、現行 skill 的工作邊界

### 直接觀察

`SKILL.md` 把角色定義為「last editor before a draft ships」，輸入前提是已有一份可讀、可編輯的 draft，而工作是保真減法。[humanizer-zh/SKILL.md](../SKILL.md#humanizer-zh--audit-and-rewrite)

它明確要求把語氣問題改寫成保留原事實的句子，而不是刪掉承載事實的句子。[humanizer-zh/SKILL.md](../SKILL.md#humanizer-zh--audit-and-rewrite)

它明確禁止在空洞處代寫經驗，要求標出缺口並把補充責任交回作者。[humanizer-zh/SKILL.md](../SKILL.md#humanizer-zh--audit-and-rewrite)

它把自己的任務限定為判斷表面是否帶有 AI 味，而非判定文字是否真的由 AI 生成。[humanizer-zh/SKILL.md](../SKILL.md#what-this-skill-is-and-isnt)

它要求先鎖定價格、日期、承諾、引文、程式碼與作者刻意保留的語氣，再進行局部修補。[humanizer-zh/SKILL.md](../SKILL.md#the-spine)

它要求重寫後的每個可被讀成世界事實的 claim 都能追溯回輸入，且不能新增原稿沒有的 claim。[humanizer-zh/SKILL.md](../SKILL.md#the-spine)

使用指南更直接寫明，從零寫文章或注入個人聲音應改用 `blog-writing-zh`，`humanizer-zh` 只除味、不造聲音。[guide.zh.md](../guide.zh.md#何時不要)

catalog 也把它定位成 README、ADR、部落格或其他既有草稿的出稿前最後一關，並明列「from scratch」不是它的使用場景。[catalog.md](../catalog.md)

`trigger-queries.json` 把「擬一份招標規格書」列為不應觸發的結構性文件生成，這表示 repo 已把文件生成與語言清理視為不同工作。[trigger-queries.json](../evals/trigger-queries.json)

### 推導

從零生成時，輸入沒有可供保真的原稿 claim，也沒有可供辨識的作者聲音。

此時 humanizer 的兩個核心保證會失去對象：沒有原文可以做 claim traceability，也沒有作者提供的特徵可以放進保護清單。

若讓模型在空白輸入上執行「空洞就標出來、不代筆」，它最多能指出缺口，不能合法地把缺口補成事實。

若讓模型自行補缺口，流程就從 editing 變成 ghostwriting，直接違反 skill 的核心安全邊界。

所以「把 humanizer 放在從零生成的同一個 prompt 裡」不是單純增加一道品質規則，而是把兩個互相衝突的工作契約混在一起。

## 二、生成式 AI 的第一性原理

### 1. 生成器先解決延續機率，不先解決作者性

GPT-3 原始論文把 GPT 類模型描述為 autoregressive language model，並以純文字互動指定任務與示例。[Brown et al., 2020](https://arxiv.org/abs/2005.14165)

對本問題的實務含義是，模型會依目前 context 中的任務、資料、示例與語氣線索，逐步選擇最可能的文字延續。

這是對生成流程的抽象推導，不是把「下一 token」誤當成完整的作者心理模型。

因此，生成前的 brief、來源包、文件結構、voice profile 與禁止事項，會影響內容在生成時採取的路徑。

生成後才加入 humanizer，主要能改寫已經選出的表面形式，不能可靠地恢復生成時沒有提供的來源、經驗、判斷或證據。

### 2. 表面訊號不是內容品質的充分條件

`humanizer-zh` 自己也把規則定義為 editing leads，而不是作者判定或 AI 來源判定。[humanizer-zh/SKILL.md](../SKILL.md#what-this-skill-is-and-isnt)

因此，AI-ism 數量下降只能證明某些表面模式減少，不能證明文件更準確、更有用、更符合來源或更像特定作者。

這個區分對從零生成尤其重要，因為生成器最可能造成的高風險錯誤不是句子太工整，而是缺少必要資料、捏造 claim、誤解需求或選錯文件結構。

humanizer 的保真驗證是「不要讓重寫再丟掉輸入事實」，不是「替空白輸入建立外部世界的 ground truth」。

所以從零場景需要另外的 source grounding、claim verification、schema 或文件契約檢查。

### 3. 後處理有合理依據，但依賴清楚的 evaluator

Self-Refine 研究把流程拆成初次生成、回饋、依回饋修訂，並在多個任務上報告相對於單步生成的改善。[Madaan et al., 2023](https://arxiv.org/abs/2303.17651)

這支持「生成後再評估與修訂」作為一種合理的 inference-time harness pattern。

它不支持「任何後處理都會改善文件」，因為改善依賴回饋是否可判斷、修訂是否真的對準任務，以及是否引入新的錯誤。

對 `humanizer-zh` 而言，這個 pattern 的可行範圍是清楚的：先讓 generator 產出有內容的 draft，再讓 humanizer 針對表面與語氣做 audit/rewrite，最後重新檢查來源與事實。

## 三、harness 的第一性原理

### 1. 用分工解決目標衝突

Anthropic 將 prompt chaining 定義為把任務拆成多次呼叫，並可在中間步驟加入程式化 gate；它直接以「先寫 outline、檢查 outline、再寫文件」作為例子。[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

同一份指引也描述 evaluator-optimizer：一次呼叫生成，另一個呼叫評估與回饋，直到符合清楚且可測量的標準。[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

這比把生成、去 AI 味、來源驗證、作者聲音與出稿決定塞進一次呼叫更符合責任分離。

### 2. 新鮮 context 比同一輪自我說服更容易檢查

Anthropic 將 context 定義為模型取樣時看到的完整 token 集合，並指出 agent loop 會持續累積資料，因此需要週期性整理與精選。[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

這支持在 generator 與 humanizer 之間切換到 fresh context，只餵入必要的 draft、來源包、文件契約、voice profile 與檢查任務。

這樣做的推導理由不是「不同 agent 必然更聰明」，而是讓生成時的辯護、草稿歷史與評估時的判準不要無限制混在同一個工作記憶裡。

但 context 分離不是免費的，若 humanizer 看不到需求、來源或 voice profile，便可能把合法的體裁特徵誤判成 AI 味。

### 3. evaluator 需要 ground truth 與停止條件

Anthropic 的 agent eval 指引把 task、trial、grader、transcript、outcome 與 evaluation harness 分開，並指出模型輸出會跨 trial 變動，因此應執行多次 trial。[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

同一指引把 agent harness 定義為處理輸入、編排工具、執行 agent loop 並回傳結果的系統，因此評估的是 harness 與模型的組合，而不是模型單獨的文字。[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

它也建議研究型任務組合 groundedness、coverage 與 source quality 等不同 grader，而不是只看單一總分。[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

OpenAI 的 Graders API 同樣提供 string check、text similarity、Python、score model 與 multi-grader 組合，說明文件品質需要多個互補的判定器，而不是只靠一個「像不像人」分數。[OpenAI Graders reference](https://developers.openai.com/api/reference/resources/graders)

## 四、建議的實際 harness

```text
使用者 brief + 文件契約 + 來源包 + voice profile
                         │
                         ▼
                Generator / composer
                         │
                         ▼
      來源與結構 gate：required facts、citations、schema
                         │
                         ▼
       Fresh context 的 humanizer detect-only audit
                         │
             ┌───────────┴───────────┐
             │                       │
       只有表面問題              空洞或事實問題
             │                       │
             ▼                       ▼
       humanizer rewrite       回 generator、查來源或問作者
             │                       │
             └───────────┬───────────┘
                         ▼
       diff、claim grounding、文件契約、品質 judge
                         │
                         ▼
                       出稿
```

第一階段的 generator 負責內容、結構、來源使用、體裁與作者聲音。

第二階段的 humanizer 只處理已存在的文字表面，保留來源包、文件契約與 voice profile 作為判斷背景。

第三階段的 deterministic gate 應檢查必備事實、連結、引用、格式、標題層級、程式碼區塊與 schema，而不是要求 humanizer 自己承擔這些判斷。

若 humanizer 發現段落空洞，應回傳「缺什麼資料」與「作者需要回答的問題」，不要讓它從空白補出經驗或新 claim。

若來源或事實檢查失敗，應回到 retrieval、research 或 generator，而不是要求 humanizer 用換句話說掩蓋證據缺口。

若只剩 P1 或 P2 的表面問題，才進入 rewrite。

改寫後必須重新做 claim-level diff，因為後處理本身可能刪除細節、改變承諾或平整掉刻意的作者聲音。

## 五、如何驗證「有效」

### 建議的比較臂

用同一批「只有 brief、來源包、體裁與 voice profile，沒有初稿」的任務建立 baseline。

至少比較以下四臂：

1. `A`：單次 generator 直接生成文件。
2. `B`：同一個 context 同時要求生成與遵守 humanizer 規則。
3. `C`：generator 先生成，fresh context 再跑 humanizer detect/rewrite。
4. `D`：generator 先生成，再跑只含文件契約與事實檢查的普通 editor，作為非 humanizer 的後處理對照。

每臂應執行多個 trial，固定模型、來源、brief、輸出長度與停止條件，並保存完整 transcript 與中間產物。

### Graders

評估不能只量 AI-ism 命中率，至少要同時量以下維度：

| 維度 | 要回答的問題 | 可能的 grader |
|---|---|---|
| 任務完成 | 文件是否真的回答 brief | 結構化 rubric、人工盲評 |
| 來源根據 | 每個外部 claim 是否有來源支持 | claim entailment、citation checker |
| 內容覆蓋 | 必備事實是否完整出現 | required-fact checks |
| 幻覺與新增 claim | 是否加入來源包沒有的事實 | claim diff、source-grounded judge |
| 體裁適配 | README、spec、RFP、blog 是否各自符合讀者需要 | genre rubric |
| 作者性 | 是否保留或合理實現宣告的 voice profile | voice similarity、人工盲評 |
| AI-ism | 表面模式是否減少 | humanizer rule audit、人工盲評 |
| 誤傷 | 合法的技術、正式、口語或作者刻意寫法是否被改壞 | protected-span checks、真人文本桶 |
| 修改代價 | 為得到較低 AI-ism，改了多少有用內容 | diff size、human correction time |
| 穩定性 | 多次生成是否維持同一品質 | trial variance、failure rate |

### 出貨判準

只有在 `C` 相對於 `A` 提高整體任務效用，且沒有明顯降低來源根據、內容覆蓋、作者性或誤傷率時，才能宣稱 humanizer 對從零生成流程有效。

如果 `C` 只降低 AI-ism 分數，卻增加幻覺、刪除細節、讓文字變得無個性或提高人工修正時間，應判定為表面改善而非流程改善。

如果 `B` 優於 `C`，也不能直接推論把完整 humanizer 內嵌到 generator 是較好的長期架構，因為還要檢查 context 負擔、規則外溢、可除錯性與後續新增規則的回歸成本。

## 六、對目前 repo 的具體判讀

目前 eval suite 有 88 個案例，最高 ID 為 89；內容包含保真檢查、false-positive 語料、作者聲音保護、多條規則的 adversarial coverage，以及 preflight handoff 與 exact-file choice 行為案例。[evals.json](../evals/evals.json) [corpus.md](../evals/corpus.md)

這些資料能支持 humanizer 作為「既有文字的 audit/rewrite」需要重視保真、誤傷與不代筆。

這些新增的 routing cases 只能檢查是否走對 handoff 或選擇提示，不能直接支持從零生成的品質結論；現行 eval 的主要輸入仍是已經存在的短文、草稿、文件片段或真人文本，而不是完整的 blank-page task。[corpus.md](../evals/corpus.md)

`SKILL.md` 與 `guide.zh.md` 現在把無參數、無確切檔案位置、無草稿內容的手動啟動預設為 `preflight`；對已提供的草稿或貼上文字，未明確表達改寫意圖時仍預設 `detect`，而「把 AI 味拿掉」「改成人話」才是明確的 `rewrite` 要求。[SKILL.md](../SKILL.md#routing) [guide.zh.md](../guide.zh.md#判定流程從讀稿到出稿)

兩份文件也都記錄了 `preflight` 分支與 exact-file choice gate：只給確切檔案位置而沒有模式時，先提示選 `detect` 或 `modify`，避免從檔案存在本身推論使用者授權修改。

## 最終判定

`humanizer-zh` 對從零生成的最佳用法是「後段、獨立、可回退的 evaluator-optimizer stage」。

它不應被當成 generator 的替代品，也不應被宣傳成能把空白稿件變成人寫的文件。

對事務文件，優先順序應是來源與需求完整、結構正確、事實可追溯、承諾不被改動，最後才是 AI 腔清理。

對署名文體，humanizer 可以協助移除機械化表面，但作者的立場、經驗與聲音仍必須由 brief、樣本、採訪式補問或人工提供。

下一個值得做的工程工作不是擴增 humanizer 規則，而是建立 blank-page eval suite，直接比較 `A`、`B`、`C`、`D` 四臂，並以任務效用與來源根據作主指標、AI-ism 作次指標。

## Sources

- [Brown et al., Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- [Madaan et al., Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [OpenAI, Graders API reference](https://developers.openai.com/api/reference/resources/graders)
- [Local humanizer-zh skill](../SKILL.md)
- [Local humanizer-zh user guide](../guide.zh.md)
- [Local humanizer-zh eval corpus](../evals/corpus.md)

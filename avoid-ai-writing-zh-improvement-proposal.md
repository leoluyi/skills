# avoid-ai-writing-zh 改善提案（來自五源部落格風格研究）

## 診斷

現有 skill 是純減法：拔掉 AI 病句 → 得到「乾淨但無聲音」的中性文。
「還是看得出來是 AI 寫的」的原因通常不是殘留病句，而是缺少人味的
**正向特徵**。高見龍在〈寫作吧，菜鳥工程師〉直接命名了這個現象：
「正確但沒有靈魂」——結構工整、用詞精準，但少了真實經驗、踩過的坑、
「我當初也是這樣卡住」的共鳴。

## 建議一：新增 detect 規則（結構級 AI 訊號）

現有規則多在詞彙／句式層，建議加一節「結構級訊號」（僅 detect/flag，
rewrite 時提示但不自動改，因為修復需要作者輸入）：

| 規則 | 訊號 | 說明 |
|---|---|---|
| uniform-rhythm | 節奏均質 | 連續 4+ 段長度相近（±1 句）、句長變異低。人寫的文有單句段、急停、長短交錯。 |
| zero-stance | 全文無立場 | 找不到任何一句作者判斷句（值得／不值得、我認為、別急著）。每個論點都「各有優劣」收場。 |
| zero-specifics | 零具體個人細節 | 全文沒有一個具體時間、次數、場景（「卡關三次」「凌晨三點」「花了三天」）。 |
| no-original-metaphor | 只解釋不造像 | 難概念全用定義式解釋，無任何自創比喻。 |
| perfect-sentences | 句句完整 | 沒有口語破格：括號補刀、（吧？）、自問自答、刻意的不完整句。 |

注意：這些是訊號不是判決（沿用現有 skill 的 signals-not-proof 立場）。
正式文體（RFP、簽呈）本來就該均質無立場——建議這節規則預設只在
voice profile 為 blog/casual 時啟用，或以 `--structure-signals` 選項開關。

## 建議二：voice profile 與 blog-writing-zh 對接

現有 frontmatter 已宣告支援 voice profiles。建議：

- blog-writing-zh 的 `references/voice-axes.md` 四軸配方可直接作為
  voice profile 輸入格式。
- rewrite mode 增加守則：「當輸入帶有 voice profile 時，profile 中
  宣告的正向特徵（立場句、比喻系統、節奏設計、口語破格）視為
  intentional，不得當作 AI-ism 削掉。」這解決加法/減法 pipeline 的
  衝突：先 blog-writing-zh 注入聲音，再 avoid-ai-writing-zh 除噪，
  減法不吃掉加法。

## 建議三：description 補一句分工

在 description 的 "Do NOT invoke" 清單加上：需要「注入」人味或重寫
結構時使用 blog-writing-zh；本 skill 只負責移除 AI 模式，不負責
創造聲音。

## 落地方式

1. 在 leoluyi/skills repo 開 branch，於 avoid-ai-writing-zh/SKILL.md
   新增「Structural signals (zh-TW blog voice)」一節（規則表如上）。
2. 更新 evals/avoid-ai-writing-zh/output-quality.json：新增 2 個案例
   （一段「零病句但均質無立場」的文字應被 flag；一段帶 voice profile
   的高濃度人設文字不應被削平）。
3. version bump 1.0.0 → 1.1.0。

改動可由 Claude Code 在 repo 內執行；本提案檔可直接作為 issue 內容。

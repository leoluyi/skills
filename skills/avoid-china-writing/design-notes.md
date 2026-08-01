# Design notes — avoid-china-writing

Maintainer notes — provenance for this one skill.

## External sources drawn on

Reference material the 詞彙對照 was informed by (not copied verbatim — entries are our own rewrite, fitted to the table's 陸用語／台灣正體／Carve-out columns):

- **speak-human-tw** — https://github.com/Raymondhou0917/speak-human-tw (`references/taiwan-localization.md`). Source for the 自媒體／社群 and 口語 terms added to `references/term-table.md`: 短視頻、直播帶貨、UP主、漲粉／粉絲量、公眾號、寶藏（老師／工具）、接地氣、小夥伴、文檔、註銷、反饋. Its 翻譯腔 layer is out of scope here — that axis lives in `humanizer-zh`. Two of its benchmark cases (SF-15 半形標點, SF-14 中國用語) landed here as `evals.json` ids 13-14; attribution in [`NOTICE`](NOTICE).

## 半形標點放在 D 軸、列 P2 的理由

2026-08-01. 補 SF-15 時要先決定這條規則屬於哪一軸。它不屬於 C（簡體字殘留）：半形標點不是簡體字，也不是簡→繁轉換特有的產物。更關鍵的是它**不是陸源訊號** —— 大陸的中文排版同樣用全形標點，所以半形逗號出現在中文句子裡，對「這份文件從哪來」這個問題完全不提供資訊。

放進 D（音譯與專名／語法差異）的 語法／用詞習慣 之後，因為那一段收的就是「書寫慣例層」的差異；tier 給 P2，因為本 skill 的 tier 階梯定義是「這個詞多大聲地指向大陸來源」，而它的音量是零。SKILL.md 與 tier 段都寫明這一點，避免讀者把一堆半形逗號讀成陸源證據。

沒有另開第五軸，是因為軸數寫在 frontmatter `description` 裡，而 description 是這個 skill 的觸發面 —— 為了一條排版規則改動觸發面，代價與收益不成比例。

## SF-14 的取捨：獨立 case，不併進既有案

2026-08-01. backlog 原本留了一個問題：信息／博主／接地氣 三個詞在既有 12 案中一次也沒出現，是要「補進既有 case」還是「值得一個獨立 case」。選了獨立 case，理由是這一案真正測的不是那三個詞，而是**社群語域**下 term-table 的深查會不會照樣發生 —— 既有案例全是技術文件、會議紀錄、新聞報導的語域，把三個詞塞進其中任何一案，就測不到語域這一層。2026-08-01 的 spot-check 支持這個判斷：runner 額外抓到只存在於 term-table 的 `粉絲量→粉絲數`。

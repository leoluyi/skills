<div align="center">

# My Skills

**寫出像真人正體中文的 agent 技能，直接來自我的 `~/.skills`。**

[![Skills](https://img.shields.io/badge/skills-12-6d4aff?style=flat-square)](#技能目錄)
[![License: MIT](https://img.shields.io/badge/license-MIT-3ba55d?style=flat-square)](LICENSE)
[![Runs on](https://img.shields.io/badge/runs%20on-Claude%20Code%20·%20Cursor%20·%20Codex-0ea5a3?style=flat-square)](#30-秒安裝)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-6d4aff?style=flat-square)](CONTRIBUTING.md)
[![Live catalog](https://img.shields.io/badge/live-catalog-000?style=flat-square&logo=github)](https://leoluyi.tw/skills/)

[English](README.md) · **繁體中文** · [互動式目錄 ↗](https://leoluyi.tw/skills/)

</div>

我個人的 `~/.skills` repo，是我日常在 **Claude Code、Cursor、Codex** 上用的 [`SKILL.md`](https://agentskills.io) 技能、腳本與工具。這是個人工具箱，不是單一用途的產品：它跟著我的工作需要往任何方向長，放在這裡都是公開的，因為對別人可能也有用。

目前技能偏向**繁體中文寫作**（去 AI 味、台灣在地化、商務公文），因為這正是 GitHub 上少有人做的一塊：讓文字讀起來對**台灣**讀者自然，去掉 AI 味、去掉陸用語、去掉職場黑話。其他技能與工具跟它們並存，之後也會陸續加進來。

---

## 為什麼有這些

市面上的 AI 寫作工具幾乎都預設英文。對**台灣**讀者來說，它們留下的缺口正是這些技能要補的：

- **只顧英文**：去 AI 味、語氣檢查、風格工具都對著英文調校，完全抓不到中文裡的破綻。
- **通用中文，不是台灣中文**：所謂的「中文」支援通常是大陸用法。這些技能是照著台灣人實際的書寫習慣寫成的。
- **混進來的陸用語與簡體**：陸用語、互聯網黑話、殘留簡體字會滲進正體中文；在地化技能抓得出來，又不誤傷真正的術語。
- **AI 味與職場黑話**：那種一致的節奏、模稜兩可和填充語，中英文都一起清掉。

## 這裡有什麼

- **天生可攜**：每個技能都能在 Claude Code 和 Codex（以及任何相容 [agentskills.io](https://agentskills.io) 的 agent）上跑。不需外部工具或 API，工具專屬功能不會是必要條件。
- **自足**：每個技能都能獨立完成自己的工作，提到其他相關技能只是額外參考，不是前置條件。
- **要贏過 baseline**：技能要在真實 eval 上贏過「不用技能」才會上架。
- **目前以寫作為主**：下面的目錄是台灣優先的中文寫作，涵蓋去 AI 味、陸用語轉台灣用語、白話翻譯、部落格、簽呈／RFP／評估報告。範圍是開放的，不是固定的。
- **兩個走得更遠的**：[`infographic-design`](skills/infographic-design/SKILL.md)（設計系統級的說明圖表）與 [`knowledge-doc-writing`](skills/knowledge-doc-writing/SKILL.md)（Diátaxis 文件紀律）是專業、跨語言、能獨當一面的工具，不需要中文也能用。

## 30 秒安裝

兩條路：線上環境用一行指令安裝；離線或內網環境則改用逐一技能的 symlink（見下方）。

一行指令，把所有技能裝到一台機器：

```bash
npx skills add https://github.com/leoluyi/skills -g -a '*' -y
```

之後更新：

```bash
npx skills update --all
```

接著在 Claude Code／Cursor／Codex 裡直接描述任務，技能的 trigger 會自動載入。例如打「幫我把這段 README 去掉 AI 味」就會叫用 `humanizer-zh`。

離線／內網的替代做法：Claude Code 的技能載入器在 `~/.claude/skills/` 本身是 symlink 時有探索 bug，解法是為每個技能各建一條 symlink：

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills
```

`tools/sync-skills` 會把每個 `skills/<name>/` 分別連進 `~/.claude/skills/<name>/`（Claude Code、Cursor）與 `~/.agents/skills/<name>/`（Codex、OpenHands），拒絕覆蓋真實目錄，並清掉失效的連結。

<!-- CATALOG:START -->
## 技能目錄

12 個技能、4 個分類。多數會在任務命中 trigger 時自動載入；標了 `invoke-only` 的則要輸入名稱手動啟動。可看[互動式目錄 ↗](https://leoluyi.tw/skills/)，或直接讀任何一份 [`SKILL.md`](skills/)。

### 繁中寫作

| Skill | 做什麼 |
|---|---|
| **去除 AI 味（中英雙語）**<br>[`humanizer-zh`](skills/humanizer-zh/SKILL.md) | 揪出讓中英文讀起來像機器寫的破綻，改回像人講話的樣子 |
| **台灣正體中文在地化**<br>[`avoid-china-writing`](skills/avoid-china-writing/SKILL.md) | 把混進來的陸用語、簡體字和互聯網黑話，改回台灣讀者習慣的正體中文，又不誤傷真正的術語 |
| **把技術術語翻成白話**<br>[`plain-speak`](skills/plain-speak/SKILL.md) | 把術語、程式碼、工程長文翻成非技術主管聽得懂、還能複述的一句話 |
| **繁中部落格寫作**<br>[`blog-writing-zh`](skills/blog-writing-zh/SKILL.md) | 把筆記、演講或一個題目，寫成有立場、有親身經歷、讀起來像真人的繁中部落格文 |

### 台灣商務公文

| Skill | 做什麼 |
|---|---|
| **說明提綱**<br>[`briefing-outline`](skills/briefing-outline/SKILL.md) | 把厚重的來源文件收斂成一份高空俯瞰的說明提綱，讓主管一眼掌握全貌、需要時再往下鑽 |
| **正式公文結構**<br>[`formal-doc-structure`](skills/formal-doc-structure/SKILL.md) | 把粗略需求變成可直接送簽的簽呈、會議紀錄或評估報告，結構跟著讀者的決策需求走 |
| **技術 RFP 撰寫與審查**<br>[`rfp-writing`](skills/rfp-writing/SKILL.md) | 站在招標方立場撰寫與審查技術 RFP，砍掉重複章節、附錄灌水與 AI 填充語 |

### 文件與設計

跨語言的專業工具，能獨當一面，不需要中文也能用。

| Skill | 做什麼 |
|---|---|
| **資訊圖表設計**<br>[`infographic-design`](skills/infographic-design/SKILL.md) | 設計系統級的說明圖表（時間軸、比較、流程圖），輸出成乾淨、可獨立開啟的 SVG 或單一 HTML 檔案。跨語言通用，為收藏轉發而生 |
| **Diátaxis 知識文件寫作**<br>[`knowledge-doc-writing`](skills/knowledge-doc-writing/SKILL.md) | 以 Diátaxis 模型寫工程等級的知識文件（tutorial、how-to、reference、explanation），素材撐得起才寫，缺口據實標出。這套紀律跨領域通用 |

### 知識管理

| Skill | 做什麼 |
|---|---|
| **結構化學習迴圈**<br>[`learn-loop`](skills/learn-loop/SKILL.md) `invoke-only` | 先教後考，筆記你親手寫，它負責查證來源、挑洞、歸檔進 Obsidian |
| **Obsidian 筆記庫**<br>[`obsidian-vault`](skills/obsidian-vault/SKILL.md) | 在 Obsidian 筆記庫搜尋、新增與串連筆記，維持 PARA 結構 |
| **陪我想一想**<br>[`discuss-with-me`](skills/discuss-with-me/SKILL.md) | 陪你想一個雙方都還沒有答案的問題：先展開選項，標出哪句是查到的、哪句是猜的，再拆掉承重假設，留下一份寫明「什麼會推翻它」的紀錄 |
<!-- CATALOG:END -->

---

## 開發

Clone 這個 repo，接進 Claude Code 做本機開發：

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills
```

### 目錄結構

```
.
├── README.md
├── README.zh-TW.md    # 繁體中文 README
├── CLAUDE.md          # 硬規則（永遠載入）——禁止事項
├── engineering-guidelines.md     # 完整撰寫指南
├── CONTRIBUTING.md    # 如何貢獻（英文＋繁中）
├── backlog.md         # repo 層與 tools/ 的待辦（單一 skill 的待辦在 skills/<name>/backlog.md）
├── skills/            # 上架技能——每個是一個 SKILL.md 資料夾
├── docs/              # GitHub Pages 網站（互動式目錄）
└── tools/             # repo 腳本
```

### 工具

| 腳本 | 用途 |
|--------|---------|
| `tools/new-skill <name>` | 建立新技能骨架（SKILL.md ＋ eval 範本 ＋ 下一步提示）。 |
| `tools/sync-skills` | 為每個技能建立 symlink，連進 `~/.claude/skills/`（Claude Code、Cursor）**與** `~/.agents/skills/`（Codex、OpenHands）。離線／內網替代做法。 |
| `tools/archive-skill <name>` | 用 `git mv` 把技能（含 evals）搬進 `_archive/`。 |
| `tools/usage-report [days]` | 統計 `~/.claude/projects/` transcript 裡的技能觸發次數。預設 90 天。 |
| `tools/build-docs` | 從 `skills/*/catalog.md` 重新產生 `docs/index.html`、`docs/skills.json`，以及兩份 README 的技能目錄表格。 |

硬規則、永遠載入的部分在 **[CLAUDE.md](CLAUDE.md)**。完整撰寫指南（結構、frontmatter 陷阱、命名、可攜性、測試紀律）在 **[engineering-guidelines.md](engineering-guidelines.md)**。想貢獻的話，請先讀 **[CONTRIBUTING.md](CONTRIBUTING.md)**。

## 授權

[MIT](LICENSE) © Lu Yi。建構於第三方作品的個別技能各有自己的 `LICENSE`／`NOTICE`，並列於下方鳴謝。

## 來源與鳴謝

部分技能立基於既有作品，署名與授權如下：

- **[speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw)** — Raymond Hou（雷蒙三十）（MIT）。`humanizer-zh` 的六步驟工作流程與保護清單機制改編自此專案；其翻譯腔條目也啟發了該技能與 `avoid-china-writing`（陸用語對照表）的部分台灣用語條目，這些規則條目均為自行改寫，非照抄原文。另外，`humanizer-zh` 的測試語料（`evals/evals.json` id 15-54）逐字改編了 40 則測試案例並標明出處，見 [`skills/humanizer-zh/NOTICE`](skills/humanizer-zh/NOTICE)。
- **[humanizer](https://github.com/blader/humanizer)** — Siqi Chen（MIT）與 **[x-skills](https://github.com/sergebulaev/x-skills)** 的 `x-humanizer` — Sergey Bulaev（MIT）。`humanizer-zh` 的英文層由兩者的模式清單蒸餾而來：規則重新推導、重新歸入該技能自己的缺陷分類並改寫，未逐字沿用任何原文。
- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** — Conor Bronsdon（MIT）。`humanizer-zh` 在 v1.5.0（含）以前的英文偵測層逐字沿用此專案；該層已於 v2.0.0 移除，現行技能不再含其內容，此處保留署名以誌來歷。
- **[Diátaxis](https://diataxis.fr/)** — Daniele Procida（[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)）。`knowledge-doc-writing` 以 Diátaxis 四型模型（tutorial／how-to／reference／explanation）為結構主軸；框架本身為 Procida 所有，`skills/knowledge-doc-writing/research/` 下的蒸餾筆記為衍生內容，以 CC BY-SA 4.0 釋出。
- **frontend-design** — Anthropic（Apache-2.0）。`infographic-design` 改編其部分內容，詳見 [`skills/infographic-design/NOTICE`](skills/infographic-design/NOTICE)。

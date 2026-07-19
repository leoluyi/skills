<div align="center">

# ✨ Claude Skills

**Claude Code skills that write Traditional Chinese like a real person.**
<br>**讓 Claude 寫出像真人的正體中文。**

[![Skills](https://img.shields.io/badge/skills-11-6d4aff?style=flat-square)](#skill-catalog)
[![License: MIT](https://img.shields.io/badge/license-MIT-3ba55d?style=flat-square)](LICENSE)
[![Runs on](https://img.shields.io/badge/runs%20on-Claude%20Code%20·%20Cursor%20·%20Codex-0ea5a3?style=flat-square)](#quick-start)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-6d4aff?style=flat-square)](CONTRIBUTING.md)
[![Live catalog](https://img.shields.io/badge/live-catalog-000?style=flat-square&logo=github)](https://leoluyi.tw/skills/)

**English** · [繁體中文](#繁體中文) · [Live catalog ↗](https://leoluyi.tw/skills/)

</div>

A collection of **11 portable [`SKILL.md`](https://agentskills.io) skills** for de-AI Traditional Chinese editing, Taiwan localization, and business documents, plus English infographics and Diátaxis knowledge docs. They run unchanged on **Claude Code, Cursor, and Codex** — no external tools or APIs required.

Most AI-writing tooling assumes English. These fill the gap almost nothing on GitHub covers: writing that reads natural to a **Taiwan** audience — stripping the AI tells, the mainland-China wording, and the corporate jargon that give machine text away.

---

## English

### Why star this

- **Taiwan-first Chinese writing.** De-AI editing, 陸用語 → 台灣用語 localization, plain-language rewrites, blogs, and 簽呈/RFP/評估報告 business docs — tuned for how people actually write in Taiwan, not generic zh.
- **Portable by design.** Every skill runs on Claude Code *and* Codex (and any [agentskills.io](https://agentskills.io)-compatible agent). Tool-specific power is never load-bearing.
- **Self-sufficient.** Each skill does its own job standalone; sibling skills are optional pointers, never prerequisites.
- **Earns its place.** A skill ships only if it beats its no-skill baseline on a real eval. No bar-clearing eval, no skill.

### Quick start

Install every skill onto a machine with one command:

```bash
npx skills add https://github.com/leoluyi/skills -g -a claude-code -y
```

Update later:

```bash
npx skills update --all
```

Then in Claude Code / Cursor / Codex, just describe the task — a skill's trigger fires it automatically. For example: *"幫我把這段 README 去掉 AI 味"* loads `avoid-ai-writing-zh`.

<details>
<summary><b>Offline / airgapped fallback</b></summary>

`npx skills` needs network access, and Claude Code's skill loader has a discovery bug when `~/.claude/skills/` itself is a symlink. The fix is **per-skill** symlinks:

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills
```

That script symlinks each `skills/<name>/` into both `~/.claude/skills/<name>/` (Claude Code, Cursor) and `~/.agents/skills/<name>/` (Codex, OpenHands), refuses to overwrite real directories, and prunes dangling links.

</details>

### Skill catalog

11 skills across 5 categories. Browse the [interactive catalog ↗](https://leoluyi.tw/skills/) or read any [`SKILL.md`](skills/) directly.

#### 🈺 Traditional Chinese Writing Quality

| Skill | What it does |
|---|---|
| ✍️ **De-AI Writing (English + zh-TW)**<br>[`avoid-ai-writing-zh`](skills/avoid-ai-writing-zh/SKILL.md) | Catches the tells that make English and Traditional Chinese read as machine-written, then rewrites them into human prose |
| 🇹🇼 **Cross-Strait Chinese Localizer**<br>[`avoid-china-writing`](skills/avoid-china-writing/SKILL.md) | Strips mainland-China wording, jargon, and leaked Simplified from Traditional Chinese and rewrites it into natural Taiwan usage without over-correcting real terms |
| 🗣️ **Plain Speak: Jargon into Plain Language**<br>[`plain-speak`](skills/plain-speak/SKILL.md) | Turn a technical term, snippet, or dense paragraph into one line your PM, exec, or customer can actually repeat back |

#### 📄 Taiwan Business Documents

| Skill | What it does |
|---|---|
| 📑 **Briefing Outline**<br>[`briefing-outline`](skills/briefing-outline/SKILL.md) | Distill one long report or many docs into a high-altitude 說明提綱 a manager can grasp, then drill into |
| 📄 **Formal Internal Doc Structure**<br>[`formal-doc-structure`](skills/formal-doc-structure/SKILL.md) | Turns a rough ask into a ready-to-circulate 簽呈, 會議紀錄, or 評估報告 with the structure its reader actually needs |
| 📋 **Technical RFP Writing & Review**<br>[`rfp-writing`](skills/rfp-writing/SKILL.md) | Draft and review technical RFPs from the issuer's side, cutting redundant sections, appendix bloat, and AI filler |

#### 🎨 Content Creation

| Skill | What it does |
|---|---|
| ✍️ **Traditional Chinese Blog Writer**<br>[`blog-writing-zh`](skills/blog-writing-zh/SKILL.md) | Turn notes, a talk, or a bare topic into a Taiwan-Chinese blog post that reads like a real person wrote it |
| 📊 **Infographic Design**<br>[`infographic-design`](skills/infographic-design/SKILL.md) | Design explanatory graphics people save and repost, as clean SVG or a single HTML file |

#### 📚 Technical Documentation

| Skill | What it does |
|---|---|
| 📚 **Knowledge Doc Writing (Diátaxis)**<br>[`knowledge-doc-writing`](skills/knowledge-doc-writing/SKILL.md) | Turn research into one doc with four Diátaxis blocks, writing only what the material supports and flagging gaps |

#### 🗂️ Knowledge Management

| Skill | What it does |
|---|---|
| 🔁 **Learn Loop**<br>[`learn-loop`](skills/learn-loop/SKILL.md) `invoke-only` | Get taught and quizzed on a concept, then write the note yourself while it verifies sources and files it into your Obsidian vault |
| 🗂️ **Obsidian Vault Notes**<br>[`obsidian-vault`](skills/obsidian-vault/SKILL.md) | Search, create, and link notes in an Obsidian vault that stays on PARA / Johnny-Decimal structure and wikilinks |

---

## 繁體中文

**一套可在 Claude Code、Cursor、Codex 上通用的技能**：去 AI 味、陸用語在地化、台灣商務公文，以及英文資訊圖表與 Diátaxis 知識文件。全部原樣可攜，不需外部工具或 API。

市面上的 AI 寫作工具幾乎都預設英文。這個 repo 補上 GitHub 上少有人做的一塊：讓文字讀起來對**台灣**讀者自然：去掉 AI 味、去掉陸用語、去掉職場黑話。

### 為什麼值得按星

- **台灣優先的中文寫作**：去 AI 味、陸用語轉台灣用語、白話翻譯、部落格，以及簽呈／RFP／評估報告等商務公文，貼著台灣人實際的寫法，而不是通用的中文。
- **天生可攜**：每個技能都能在 Claude Code 和 Codex（以及任何相容 [agentskills.io](https://agentskills.io) 的 agent）上跑。工具專屬功能不會是必要條件。
- **自足**：每個技能都能獨立完成自己的工作，提到姊妹技能只是選用的指路，不是前置條件。
- **要贏過 baseline**：技能要在真實 eval 上贏過「不用技能」才會上架。沒過 eval，不上架。

### 快速開始

一行指令，把所有技能裝到一台機器：

```bash
npx skills add https://github.com/leoluyi/skills -g -a claude-code -y
```

之後更新：

```bash
npx skills update --all
```

接著在 Claude Code／Cursor／Codex 裡直接描述任務，技能的 trigger 會自動載入。例如打「幫我把這段 README 去掉 AI 味」就會叫用 `avoid-ai-writing-zh`。

離線／內網的替代做法見上方英文段的 **Offline / airgapped fallback**：用 `tools/sync-skills` 為每個技能建立 symlink。

### 技能目錄

11 個技能、5 個分類。可看[互動式目錄 ↗](https://leoluyi.tw/skills/)，或直接讀任何一份 [`SKILL.md`](skills/)。

#### 🈺 繁中寫作品質

| Skill | 做什麼 |
|---|---|
| ✍️ **去除 AI 味（中英雙語）**<br>[`avoid-ai-writing-zh`](skills/avoid-ai-writing-zh/SKILL.md) | 揪出讓中英文讀起來像機器寫的破綻，改回像人講話的樣子 |
| 🇹🇼 **台灣正體中文在地化**<br>[`avoid-china-writing`](skills/avoid-china-writing/SKILL.md) | 把混進來的陸用語、簡體字和互聯網黑話，改回台灣讀者習慣的正體中文，術語不誤傷 |
| 🗣️ **把技術術語翻成白話**<br>[`plain-speak`](skills/plain-speak/SKILL.md) | 把術語、程式碼、工程長文翻成非技術主管聽得懂、還能複述的一句話 |

#### 📄 台灣商務公文

| Skill | 做什麼 |
|---|---|
| 📑 **說明提綱**<br>[`briefing-outline`](skills/briefing-outline/SKILL.md) | 把厚重的來源文件收斂成一份高空俯瞰的說明提綱，讓主管一眼掌握全貌、需要時再往下鑽 |
| 📄 **正式公文結構**<br>[`formal-doc-structure`](skills/formal-doc-structure/SKILL.md) | 把粗略需求變成可直接送簽的簽呈、會議紀錄或評估報告，結構跟著讀者的決策需求走 |
| 📋 **技術 RFP 撰寫與審查**<br>[`rfp-writing`](skills/rfp-writing/SKILL.md) | 站在招標方立場撰寫與審查技術 RFP，砍掉重複章節、附錄灌水與 AI 填充語 |

#### 🎨 內容創作

| Skill | 做什麼 |
|---|---|
| ✍️ **繁中部落格寫作**<br>[`blog-writing-zh`](skills/blog-writing-zh/SKILL.md) | 把筆記、演講或一個題目，寫成有立場、有親身經歷、讀起來像真人的繁中部落格文 |
| 📊 **資訊圖表設計**<br>[`infographic-design`](skills/infographic-design/SKILL.md) | 把主題做成讓人想收藏轉發的資訊圖表，輸出成乾淨的 SVG 或單一 HTML 檔案 |

#### 📚 技術文件

| Skill | 做什麼 |
|---|---|
| 📚 **Diátaxis 知識文件寫作**<br>[`knowledge-doc-writing`](skills/knowledge-doc-writing/SKILL.md) | 把研究成果整理成四型 Diátaxis 知識文件，素材撐得起才寫，缺口據實標出 |

#### 🗂️ 知識管理

| Skill | 做什麼 |
|---|---|
| 🔁 **結構化學習迴圈**<br>[`learn-loop`](skills/learn-loop/SKILL.md) `invoke-only` | 先教後考，筆記你親手寫，它負責查證來源、挑洞、歸檔進 Obsidian |
| 🗂️ **Obsidian 筆記庫**<br>[`obsidian-vault`](skills/obsidian-vault/SKILL.md) | 在 Obsidian 筆記庫搜尋、新增與串連筆記，維持 PARA 結構 |

---

## Develop · 開發

Clone the repo and wire it into Claude Code for local authoring:

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills
```

### Layout

```
.
├── README.md
├── CLAUDE.md          # hard rules (always loaded) — the forbidden directives
├── DEVELOPMENT.md     # full authoring guide
├── CONTRIBUTING.md    # how to contribute (EN + 繁中)
├── backlog.md         # ideas not yet drafted
├── skills/            # active skills — each is a SKILL.md folder
├── docs/              # GitHub Pages site (the live catalog)
└── tools/             # repo scripts
```

### Tools

| Script | Purpose |
|--------|---------|
| `tools/new-skill <name>` | Scaffold a new skill (SKILL.md + eval stub + next-step hints). |
| `tools/sync-skills` | Per-skill symlinks into `~/.claude/skills/` (Claude Code, Cursor) **and** `~/.agents/skills/` (Codex, OpenHands). Offline / airgapped fallback. |
| `tools/archive-skill <name>` | `git mv` a skill (and its evals) to `_archive/`. |
| `tools/usage-report [days]` | Count skill triggers in `~/.claude/projects/` transcripts. Default 90 days. |

The hard, always-loaded rules are in **[CLAUDE.md](CLAUDE.md)**. The full authoring guide — anatomy, frontmatter gotchas, naming, portability, and test discipline — is in **[DEVELOPMENT.md](DEVELOPMENT.md)**. To contribute, start with **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## License

[MIT](LICENSE) © Lu Yi. Some skills adapt upstream work under their own attribution — see each skill's `SKILL.md` and `NOTICE`.

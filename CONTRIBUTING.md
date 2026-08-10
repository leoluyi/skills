# Contributing

Thanks for looking. This is a personal skills collection, but issues and pull
requests are welcome — a bug in a trigger description or a zh-TW usage slip is
worth reporting.

> 繁體中文版本在下方 · Traditional Chinese version below.

## Before you open a PR

1. Read **[CLAUDE.md](CLAUDE.md)** — the hard, always-loaded rules. Breaking one
   of these is an automatic no.
2. Read **[engineering-guidelines.md](engineering-guidelines.md)** — the full authoring guide: skill
   anatomy, the frontmatter gotchas, naming, portability, and test discipline.

## The bar every skill has to clear

- **Portable.** It must run unchanged on Claude Code *and* Codex (and any
  agentskills.io-compatible agent). Tool-specific power (hooks, `context: fork`,
  `model`) may be present but never load-bearing.
- **Self-sufficient.** A skill completes its own job standalone. Sibling-skill
  mentions are optional pointers, never `run X first` prerequisites.
- **Beats its baseline.** A new skill must beat vanilla on
  `skills/<name>/evals/evals.json`; an edit to an existing skill must beat the
  previous version. No bar-clearing eval, no merge.
- **Real UTF-8 frontmatter.** Never `\u`-escape a `description` — escaped
  non-ASCII silently disables the trigger. See CLAUDE.md.

## Local setup

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills        # per-skill symlinks into ~/.claude/skills and ~/.agents/skills
```

Scaffold a new skill with `tools/new-skill <kebab-name>`.

Run `tools/eval validate --all` before opening a PR.
Use `tools/eval quick <name>` for fast feedback and `tools/eval gate <name> --baseline REF` for release evidence.
Pass `--ids` for a bounded one-round diagnostic probe.

---

# 貢獻指南

這是個人的 skills 收藏，但歡迎回報問題與送 PR：trigger 描述的錯誤、或台灣用語的走鐘，都值得提出。

## 送 PR 之前

1. 讀 **[CLAUDE.md](CLAUDE.md)**：永遠載入的硬規則，違反其中一條會直接退回。
2. 讀 **[engineering-guidelines.md](engineering-guidelines.md)**：完整的撰寫指南，包含 skill 結構、
   frontmatter 陷阱、命名、可攜性與測試紀律。

## 每個 skill 都要過的門檻

- **可攜（portable）**：必須在 Claude Code 和 Codex（以及任何相容 agentskills.io
  的 agent）上原樣運作。工具專屬功能（hooks、`context: fork`、`model`）可以有，
  但不能是必要條件。
- **自足（self-sufficient）**：一個 skill 要能獨立完成自己的工作。提到姊妹 skill
  只是選用的指路，不是「先跑 X」的前置條件。
- **要贏過 baseline**：新 skill 要在 `skills/<name>/evals/evals.json` 上贏過
  vanilla；改既有 skill 要贏過前一版。沒過 eval，不合併。
- **frontmatter 用真正的 UTF-8**：`description` 絕不能用 `\u` 跳脫，跳脫過的
  非 ASCII 會讓 trigger 靜默失效。細節見 CLAUDE.md。

## 本機設定

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills        # 為每個 skill 建立 symlink 到 ~/.claude/skills 與 ~/.agents/skills
```

用 `tools/new-skill <kebab-name>` 建立新 skill 的骨架。

送 PR 前執行 `tools/eval validate --all`。
快速回饋用 `tools/eval quick <name>`，出貨證據用 `tools/eval gate <name> --baseline REF`；加 `--ids` 可做三分鐘內的一輪診斷。

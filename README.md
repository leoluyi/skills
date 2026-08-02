<div align="center">

# My Skills

**Agent skills that write Traditional Chinese like a real person — straight from my `~/.skills`.**

[![Skills](https://img.shields.io/badge/skills-19-6d4aff?style=flat-square)](#skill-catalog)
[![License: MIT](https://img.shields.io/badge/license-MIT-3ba55d?style=flat-square)](LICENSE)
[![Runs on](https://img.shields.io/badge/runs%20on-Claude%20Code%20·%20Cursor%20·%20Codex-0ea5a3?style=flat-square)](#30-second-setup)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-6d4aff?style=flat-square)](CONTRIBUTING.md)
[![Live catalog](https://img.shields.io/badge/live-catalog-000?style=flat-square&logo=github)](https://leoluyi.tw/skills/)

**English** · [繁體中文](README.zh-TW.md) · [Live catalog ↗](https://leoluyi.tw/skills/)

</div>

My personal `~/.skills` repo — the [`SKILL.md`](https://agentskills.io) skills, scripts, and tooling I use day to day across **Claude Code, Cursor, and Codex**. It's a personal toolbox, not a single-purpose product: it grows in whatever direction my work needs, and anything here is public because it might be useful to someone else too.

Today the skills lean toward **Traditional Chinese writing** — de-AI editing, Taiwan localization, business documents — because that's the gap almost nothing on GitHub covers: writing that reads natural to a **Taiwan** audience, stripped of the AI tells, mainland-China wording, and corporate jargon that give machine text away. Other skills and tools live alongside them, and more get added over time.

---

## Why these exist

Most AI-writing tooling assumes English. For a **Taiwan** audience it leaves gaps these skills close:

- **English-only defaults.** De-AI editors, tone checkers, and style tools are tuned for English and miss the tells in Chinese entirely.
- **Generic zh, not Taiwan zh.** "Chinese" support usually means mainland usage. These write the way people actually write in Taiwan.
- **Leaked mainland wording & Simplified.** 陸用語, 互聯網黑話, and stray 簡體字 slip into Traditional Chinese; the localizer catches them without over-correcting real terms.
- **AI tells & corporate jargon.** The uniform rhythm, hedging, and filler that give machine text away — stripped, in both languages.

## What's here

- **Portable by design.** Every skill runs on Claude Code *and* Codex (and any [agentskills.io](https://agentskills.io)-compatible agent). No external tools or APIs required; tool-specific power is never load-bearing.
- **Self-sufficient.** Each skill does its own job standalone; sibling skills are optional pointers, never prerequisites.
- **Earns its place.** A skill ships only if it beats its no-skill baseline on a real eval. No bar-clearing eval, no skill.
- **Currently writing-heavy.** The catalog below is Taiwan-first Chinese writing — de-AI editing, 陸用語 → 台灣用語 localization, plain-language rewrites, blogs, and 簽呈/RFP/評估報告 docs. Scope is open, not fixed.
- **Two that travel further.** [`infographic-design`](skills/infographic-design/SKILL.md) (design-system-grade explanatory graphics) and [`knowledge-doc-writing`](skills/knowledge-doc-writing/SKILL.md) (the Diátaxis documentation discipline) are professional, language-agnostic tools that stand on their own — no Chinese required.

## 30-second setup

Two paths — a networked one-liner, or offline per-skill symlinks (below).

Install every skill onto a machine with one command:

```bash
npx skills add https://github.com/leoluyi/skills -g -a '*' -y
```

Update later:

```bash
npx skills update --all
```

Then in Claude Code / Cursor / Codex, just describe the task — a skill's trigger fires it automatically. For example: *"幫我把這段 README 去掉 AI 味"* loads `humanizer-zh`.

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

<!-- CATALOG:START -->
## Skill catalog

19 skills across 6 categories. Every skill is labelled `model-invoked` (the agent fires it automatically on a matching task, and you can also call it by name) or `user-invoked` (only you can, by name). Browse the [interactive catalog ↗](https://leoluyi.tw/skills/) or read any [`SKILL.md`](skills/) directly.

### Traditional Chinese Writing

| Skill | Invocation | What it does |
|---|---|---|
| **Humanizer (English + zh-TW)**<br>[`humanizer-zh`](skills/humanizer-zh/SKILL.md) | `model-invoked` | Catches the tells that make English and Traditional Chinese read as machine-written, then rewrites them into human prose |
| **Cross-Strait Chinese Localizer**<br>[`avoid-china-writing`](skills/avoid-china-writing/SKILL.md) | `model-invoked` | Strips mainland-China wording, jargon, and leaked Simplified from Traditional Chinese and rewrites it into natural Taiwan usage without over-correcting real terms |
| **Plain Speak: Jargon into Plain Language**<br>[`plain-speak`](skills/plain-speak/SKILL.md) | `model-invoked` | Turn a technical term, snippet, or dense paragraph into one line your PM, exec, or customer can actually repeat back |
| **Traditional Chinese Blog Writer**<br>[`blog-writing-zh`](skills/blog-writing-zh/SKILL.md) | `user-invoked` | Turn notes, a talk, or a bare topic into a Taiwan-Chinese blog post that reads like a real person wrote it |

### Taiwan Business Documents

| Skill | Invocation | What it does |
|---|---|---|
| **Briefing Outline**<br>[`briefing-outline`](skills/briefing-outline/SKILL.md) | `model-invoked` | Distill one long report or many docs into a high-altitude 說明提綱 a manager can grasp, then drill into |
| **Formal Internal Doc Structure**<br>[`formal-doc-structure`](skills/formal-doc-structure/SKILL.md) | `user-invoked` | Turns a rough ask into a ready-to-circulate 簽呈, 會議紀錄, or 評估報告 with the structure its reader actually needs |
| **Technical RFP Writing & Review**<br>[`rfp-writing`](skills/rfp-writing/SKILL.md) | `user-invoked` | Draft and review technical RFPs from the issuer's side, cutting redundant sections, appendix bloat, and AI filler |

### Docs & Design

Language-agnostic professional tools that stand on their own — no Chinese required.

| Skill | Invocation | What it does |
|---|---|---|
| **Infographic Design**<br>[`infographic-design`](skills/infographic-design/SKILL.md) | `model-invoked` | Design-system-grade explanatory graphics — timelines, comparisons, process diagrams — as clean, self-contained SVG or a single HTML file. Language-agnostic; built to be saved and reshared |
| **Knowledge Doc Writing (Diátaxis)**<br>[`knowledge-doc-writing`](skills/knowledge-doc-writing/SKILL.md) | `model-invoked` | Engineering-grade knowledge docs on the Diátaxis model — tutorial, how-to, reference, explanation — writing only what the material supports and flagging the gaps honestly. A discipline that travels across domains |

### Knowledge Management

| Skill | Invocation | What it does |
|---|---|---|
| **Learn Loop**<br>[`learn-loop`](skills/learn-loop/SKILL.md) | `user-invoked` | Get taught and quizzed on a concept, then write the note yourself while it verifies sources and files it into your Obsidian vault |
| **Obsidian Vault Notes**<br>[`obsidian-vault`](skills/obsidian-vault/SKILL.md) | `model-invoked` | Search, create, and link notes in an Obsidian vault that stays on PARA / Johnny-Decimal structure and wikilinks |
| **Discuss With Me**<br>[`discuss-with-me`](skills/discuss-with-me/SKILL.md) | `model-invoked` | Think through a question neither of you can answer yet — widen the options, label what's found vs guessed, attack the load-bearing assumptions, and leave a record that says what would overturn it |

### Data Recovery

Language-agnostic; runs on any agent with shell access.

| Skill | Invocation | What it does |
|---|---|---|
| **Recover a Deleted Claude Conversation**<br>[`recover-deleted-claude-conversation`](skills/recover-deleted-claude-conversation/SKILL.md) | `user-invoked` | Pull a deleted Claude Desktop/claude.ai conversation and its artifacts back out of the Chromium cache before it's evicted |

### Agent Workflow

Language-agnostic; runs on any agent that can execute a plan unattended.

| Skill | Invocation | What it does |
|---|---|---|
| **Plan → Goal**<br>[`plan-to-goal`](skills/plan-to-goal/SKILL.md) | `user-invoked` | Turn a rough plan into a bounded goal with machine-checkable done conditions, before an autonomous run burns tokens on a vague target |
| **Goal Definer**<br>[`goal-definer`](skills/goal-definer/SKILL.md) | `model-invoked` | Interview a fuzzy task into a six-element goal prompt an agent can run for hours without drifting or wrapping up early |
| **Autopilot**<br>[`autopilot`](skills/autopilot/SKILL.md) | `user-invoked` | Hand over the whole job: orchestrate subagents, self-repair on a budget, pass a verification gate, then commit, push and open a PR without checking back |
| **Breakdown**<br>[`breakdown`](skills/breakdown/SKILL.md) | `model-invoked` | Lay every case out in full before evaluating any of them, split the problem into decisions only you can make, then wait — recommendation comes last |
| **Options**<br>[`options`](skills/options/SKILL.md) | `user-invoked` | Re-ask whatever is pending as tappable choices, then keep every direction decision clickable for the rest of the session |
| **Taste Distiller**<br>[`taste-distiller`](skills/taste-distiller/SKILL.md) | `model-invoked` | Mine your rejections of AI output and distil the standard behind them into a reusable 1-5 rubric, in Markdown and in JSON for an evaluator agent |
<!-- CATALOG:END -->

---

## Develop

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
├── README.zh-TW.md    # Traditional Chinese README
├── CLAUDE.md          # hard rules (always loaded) — the forbidden directives
├── engineering-guidelines.md     # full authoring guide
├── CONTRIBUTING.md    # how to contribute (EN + 繁中)
├── backlog.md         # repo-level + tools/ backlog (per-skill items live in skills/<name>/backlog.md)
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
| `tools/run-eval <name>` | Trigger-layer eval: does the description fire on `evals/trigger-queries.json`? |
| `tools/run-case <name> --baseline REF[:DIR]` | Behaviour-layer eval: score `evals/evals.json` new-vs-baseline through blind runners and graders, and report ship/no-ship. Opt-in — needs `evals/run-case.json`. |
| `tools/check-labels <name> \| --all` | Read-only eval hygiene gate: every rule label in `evals.json`/corpus resolves to a real rule name, every corpus 引文片段 is an exact substring. Opt-in — needs `evals/label-check.json`. |
| `tools/annotate <name> [--ids 15,18-20]` | Blind adjudication: show a case's span with the expectation and rule name stripped, take an AI 指數 1-4 plus a rationale, and record it in `evals/annotations.json`. Renders the ledger into `evals/judged-cases.md` between `annotate:begin/end`; `--check` fails if that render is stale. |
| `tools/build-docs` | Regenerate `docs/index.html`, `docs/skills.json`, and both READMEs' catalog tables from `skills/*/catalog.md`. |

The hard, always-loaded rules are in **[CLAUDE.md](CLAUDE.md)**. The full authoring guide — anatomy, frontmatter gotchas, naming, portability, and test discipline — is in **[engineering-guidelines.md](engineering-guidelines.md)**. To contribute, start with **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## License

[MIT](LICENSE) © Lu Yi. Individual skills that build on third-party work carry their own `LICENSE`/`NOTICE` and are credited below.

## Sources & acknowledgments

Some skills stand on prior work. Credit and licenses:

- **[speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw)** by Raymond Hou (雷蒙三十) (MIT) — `humanizer-zh` adapts its six-step working procedure and its 保護清單 mechanism, and its 翻譯腔 patterns informed Taiwan-usage entries in that skill and in `avoid-china-writing` (陸用語 term table); those rule entries are our own rewrite, not copied text. Separately, `humanizer-zh`'s eval corpus (`evals/evals.json` ids 15-54) adapts 40 of its test cases verbatim, with attribution — see [`skills/humanizer-zh/NOTICE`](skills/humanizer-zh/NOTICE).
- **[humanizer](https://github.com/blader/humanizer)** by Siqi Chen (MIT) and **[x-skills](https://github.com/sergebulaev/x-skills)**' `x-humanizer` by Sergey Bulaev (MIT) — `humanizer-zh`'s English layer was distilled from their pattern inventories; the patterns were re-derived, re-classified into that skill's own defect classes, and rewritten, with no prose copied verbatim.
- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** by Conor Bronsdon (MIT) — `humanizer-zh` through v1.5.0 rebased its English detection layer verbatim from this project. That layer was removed in v2.0.0 and no longer appears in the skill; the credit stands for the record.
- **[Diátaxis](https://diataxis.fr/)** by Daniele Procida ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)) — `knowledge-doc-writing` is structured on the Diátaxis four-type model (tutorial / how-to / reference / explanation). The framework is Procida's work; the distilled study notes under `skills/knowledge-doc-writing/research/` are a derivative and are made available under CC BY-SA 4.0.
- **frontend-design** by Anthropic (Apache-2.0) — `infographic-design` adapts portions; see [`skills/infographic-design/NOTICE`](skills/infographic-design/NOTICE).

# Skills

Personal Claude Code skills repo. Source of truth for the `npx skills` package install on every machine I use.

## Install (consumer)

Get the skills onto a machine.

```
npx skills add https://github.com/leoluyi/skills -g -a claude-code -y
```

### Update

```
npx skills update --all
```

### Offline / airgapped fallback

`npx skills` needs network access, and Claude Code's skill loader has a discovery bug when `~/.claude/skills/` itself is a symlink (it walks the link strangely and fails to enumerate children). The fix is **per-skill** symlinks instead of a directory-level one.

```
tools/sync-skills
```

That script symlinks each `skills/<name>/` into `~/.claude/skills/<name>/`, refuses to overwrite real directories, and prunes dangling links left behind by archives.

## Develop (contributor)

Clone the repo and wire it into Claude Code for local authoring.

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills
```

### Layout

```
.
├── README.md
├── backlog.md         # ideas not yet drafted (signal: friction hit 2+ times)
├── .gitignore
├── skills/            # active skills — each is a SKILL.md folder
├── _archive/          # retired skills (kept for reference + usage-report scope)
├── evals/             # mirrors skills/ — one prompts.json per skill
└── tools/             # repo scripts — see Tools below
```

### Tools

| Script | Purpose |
|--------|---------|
| `tools/new-skill <name>` | Scaffold a new skill (SKILL.md + eval stub + next-step hints). |
| `tools/sync-skills` | Per-skill symlinks into `~/.claude/skills/`. Offline / airgapped fallback. |
| `tools/archive-skill <name>` | `git mv` skill (and its evals) to `_archive/`, commit `archive: <name>`. |
| `tools/usage-report [days]` | Count skill triggers in `~/.claude/projects/` JSONL transcripts. Default 90 days. |

## Authoring skills

### Anatomy of a skill

```
skills/<name>/
├── SKILL.md         # frontmatter + body — the index, not the manual
├── references/      # optional — large docs the body points at on demand
└── scripts/         # optional — deterministic logic, no LLM needed
evals/<name>/
└── prompts.json     # with-vs-without baselines (mirrors skills/<name>/)
```

The `SKILL.md` frontmatter is two fields. The `description` is the **trigger gate** — the only thing Claude sees when deciding whether to load the skill. Name what should fire it *and* what should not:

```yaml
---
name: rfp-writing
description: Write or review technical RFP documents from the issuer's perspective…
  Trigger only when the user explicitly asks for an RFP; do not invoke for migration
  plans, runbooks, or design docs — those conventions conflict with RFP rules.
---
```

### SDLC

A skill goes through these seven stages. Most die at stage 3.

1. **Capture** — friction hit twice → add a one-liner to `backlog.md`. Don't draft yet.
2. **Draft** — `tools/new-skill <kebab-name>` scaffolds `skills/<name>/SKILL.md` plus `evals/<name>/prompts.json`.
3. **Test** — write 3+ realistic prompts in `prompts.json`, run each **with** the skill and **without**. See [Test discipline](#test-discipline).
4. **Iterate** — adjust the body until with-skill beats vanilla on every prompt. If you can't get there, cut it.
5. **Optimize description** — rewrite the trigger gate until Claude invokes it on the right prompts and *not* on lookalike-but-wrong ones.
6. **Deploy** — commit and push. Consumer machines pull via `npx skills update --all` or `tools/sync-skills`.
7. **Maintain / retire** — `tools/usage-report` quarterly; archive dormant skills via `tools/archive-skill <name>`. See [Maintenance](#maintenance).

### Naming

- kebab-case, lowercase
- action-flavored — verbs over nouns when possible
- specific over generic — `oracle-exadata-cutover` not `migration`, `rfp-writing` not `documents`

### Authoring rules

- **Write the description pushy.** It's the trigger gate (see [Anatomy](#anatomy-of-a-skill)). Name the explicit phrases that should fire it *and* what should NOT. Vague descriptions either misfire on unrelated prompts or silently never load.
- **Body under 500 lines.** Lean on progressive disclosure — the SKILL.md is the index, push detail into `references/` and logic into `scripts/`.
- **Explain *why*, not just *what*.** Bullet lists describe a procedure; the *why* lets a reader extrapolate to edge cases the bullets miss. If the skill says "do X", say what X is preventing.

### Test discipline

Expands on SDLC stages 3–4. Every skill ships with a `evals/<name>/prompts.json`. Every change to a skill is validated against those prompts **with-vs-without** baselines. The skill ships only if it's materially better than vanilla Claude on every prompt. No bar-clearing, no skill.

This is the single most important rule in this repo. A skill that exists but doesn't help is worse than no skill — it eats context, it pollutes the trigger surface for other skills, and it makes the portfolio look healthier than it is.

### Maintenance

Expands on SDLC stage 7.

- `tools/usage-report` quarterly. Skills with zero hits in 90 days → archive candidate.
- A skill firing too often on wrong prompts → tighten the description.
- A skill firing too rarely on right prompts → loosen / make the description more pushy, or add example trigger phrases.
- Archive aggressively. The repo is supposed to feel small.

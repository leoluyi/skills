# Skills

Personal Claude Code skills repo. Source of truth for the `npx skills` package install on every machine I use.

## Quickstart (development)

```bash
git clone git@github.com:leoluyi/skills.git ~/.skills
cd ~/.skills
tools/sync-skills
```

## Quick install

```
npx skills add https://github.com/leoluyi/skills -g -a claude-code -y
```

## Update

```
npx skills update --all
```

## Offline / airgapped fallback

`npx skills` needs network access, and Claude Code's skill loader has a discovery bug when `~/.claude/skills/` itself is a symlink (it walks the link strangely and fails to enumerate children). The fix is **per-skill** symlinks instead of a directory-level one.

```
tools/sync-skills
```

That script symlinks each `skills/<name>/` into `~/.claude/skills/<name>/`, refuses to overwrite real directories, and prunes dangling links left behind by archives.

## Layout

```
.
├── README.md
├── backlog.md         # ideas not yet drafted (signal: friction hit 2+ times)
├── .gitignore
├── skills/            # active skills — each is a SKILL.md folder
├── _archive/          # retired skills (kept for reference + usage-report scope)
├── evals/             # mirrors skills/ — one prompts.json per skill
└── tools/             # repo scripts — see table at bottom
```

## SDLC

A skill goes through these seven stages. Most die at stage 3.

1. **Capture** — friction hit twice → add a one-liner to `backlog.md`. Don't draft yet.
2. **Draft** — `tools/new-skill <kebab-name>` scaffolds `skills/<name>/SKILL.md` plus `evals/<name>/prompts.json`.
3. **Test** — write 3+ realistic prompts in `prompts.json`. Run each prompt **with the skill loaded** and **without**, side by side.
4. **Iterate** — adjust the body until the with-skill version is materially better than vanilla on every prompt. If you can't get there, cut the skill — a skill that doesn't beat vanilla is just a context tax.
5. **Optimize description** — the frontmatter `description` is the trigger gate. Rewrite it pushy and specific until Claude reliably invokes it on the right prompts and *doesn't* invoke it on lookalike-but-wrong prompts.
6. **Deploy** — commit and push. Consumer machines pull via `npx skills update --all` or `tools/sync-skills`.
7. **Maintain / retire** — `tools/usage-report` quarterly. Skills dormant 90+ days → archive candidate via `tools/archive-skill <name>`.

## Naming

- kebab-case, lowercase
- action-flavored — verbs over nouns when possible
- specific over generic — `oracle-exadata-cutover` not `migration`, `rfp-writing` not `documents`

## Skill authoring rules

- **The description is the trigger gate.** It's the only thing Claude sees when deciding whether to load the skill. Write it pushy. Name the explicit phrases that should fire it. Name what should NOT fire it. Vague descriptions either misfire on unrelated prompts or silently never load.
- **Body under 500 lines.** Lean on progressive disclosure — the SKILL.md is the index, not the manual.
- **`references/` for large docs** the skill points at on demand (templates, long checklists, examples).
- **`scripts/` for deterministic logic** that doesn't need an LLM (validators, formatters, scaffolders).
- **Explain *why*, not just *what*.** Bullet lists describe a procedure; the *why* lets a reader extrapolate to edge cases the bullets miss. If the skill says "do X", say what X is preventing.

## Test discipline

Every skill ships with a `evals/<name>/prompts.json`. Every change to a skill is validated against those prompts **with-vs-without** baselines. The skill ships only if it's materially better than vanilla Claude on every prompt. No bar-clearing, no skill.

This is the single most important rule in this repo. A skill that exists but doesn't help is worse than no skill — it eats context, it pollutes the trigger surface for other skills, and it makes the portfolio look healthier than it is.

## Maintenance

- `tools/usage-report` quarterly. Skills with zero hits in 90 days → archive candidate.
- A skill firing too often on wrong prompts → tighten the description.
- A skill firing too rarely on right prompts → loosen / make the description more pushy, or add example trigger phrases.
- Archive aggressively. The repo is supposed to feel small.

## Tools

| Script | Purpose |
|--------|---------|
| `tools/new-skill <name>` | Scaffold a new skill (SKILL.md + eval stub + next-step hints). |
| `tools/sync-skills` | Per-skill symlinks into `~/.claude/skills/`. Offline / airgapped fallback. |
| `tools/archive-skill <name>` | `git mv` skill (and its evals) to `_archive/`, commit `archive: <name>`. |
| `tools/usage-report [days]` | Count skill triggers in `~/.claude/projects/` JSONL transcripts. Default 90 days. |

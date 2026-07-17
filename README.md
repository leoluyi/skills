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

That script symlinks each `skills/<name>/` into both `~/.claude/skills/<name>/` (Claude Code, Cursor) and `~/.agents/skills/<name>/` (Codex, OpenHands), refuses to overwrite real directories, and prunes dangling links left behind by archives.

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
├── CLAUDE.md          # hard rules (always loaded) — the forbidden directives
├── DEVELOPMENT.md     # full authoring guide
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
| `tools/sync-skills` | Per-skill symlinks into `~/.claude/skills/` (Claude Code, Cursor) **and** `~/.agents/skills/` (Codex, OpenHands). Offline / airgapped fallback. |
| `tools/archive-skill <name>` | `git mv` skill (and its evals) to `_archive/`, commit `archive: <name>`. |
| `tools/usage-report [days]` | Count skill triggers in `~/.claude/projects/` JSONL transcripts. Default 90 days. |

## Authoring skills

The hard, always-loaded rules are in **[CLAUDE.md](CLAUDE.md)**. The full guide — anatomy, frontmatter gotchas, SDLC, naming, portability, test discipline, maintenance, and the self-sufficiency/dependency rules — is in **[DEVELOPMENT.md](DEVELOPMENT.md)**.

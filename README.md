# Skills

Personal Claude Code skill packages.

## Install

```
npx skills@latest add leoluyi/skills -g
```

## Skills

| Skill | Description |
|-------|-------------|
| rfp-writing | Review and write technical RFP documents in formal, plain Chinese |

## Development

Edits to skills in this repo are picked up by Claude Code instantly via a symlink:

```
~/.claude/skills/<skill>  ->  ~/.agents/skills/<skill>  ->  <this repo>/<skill>
```

Setup for a new skill (one-off):

```
rm -rf ~/.agents/skills/<skill>
ln -s "$(pwd)/<skill>" ~/.agents/skills/<skill>
```

Track changes with normal `git status` / `git diff` in this repo.

Caveat: re-running `npx skills@latest add leoluyi/skills -g` may overwrite the symlink with a real copy. If that happens, re-run the `ln -s` command above.

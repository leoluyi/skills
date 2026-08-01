# scripts

## build-app-skills.py

Builds Claude-app-uploadable `.zip` packages from `skills/`.

```sh
uv run scripts/build-app-skills.py plain-speak humanizer-zh  # build only named skills
uv run scripts/build-app-skills.py --all                     # build every skill
uv run scripts/build-app-skills.py --list                    # status table, no build
uv run scripts/build-app-skills.py                           # interactive menu (TTY only)
```

Output lands in `dist/` (git-ignored). Each `dist/<name>.zip` contains a single
top-level `<name>/` folder — the layout claude.ai's skill uploader expects.

The Claude app reads only `name` / `description` / `license` frontmatter. The
builder rewrites each SKILL.md down to those fields; source files under
`skills/` are never modified.

### The 200-character description limit

claude.ai caps `description` at **200 characters** — see
[claude.com/docs/skills/how-to](https://claude.com/docs/skills/how-to):
"Claude.ai limits descriptions to 200 characters." This is *not* the same as
the Agent Skills spec's own 1024-char limit, which is what most SKILL.md
files in this repo are written against, since their descriptions also need
to carry enough trigger detail for non-claude.ai agents. The builder
hard-fails if a skill's effective description exceeds 200 chars.

### `app-description` / `app-name` frontmatter fields

To ship a claude.ai package for a skill whose normal `description` (or
`name`) doesn't fit claude.ai's rules, add `app-description` and/or
`app-name` to that skill's **source** `skills/<name>/SKILL.md` frontmatter,
alongside the normal fields:

```yaml
---
name: some-skill
description: >-
  The long, trigger-rich description used by every other platform...
app-description: >-
  A trimmed description that fits in 200 characters for claude.ai.
app-name: some-skill-app
license: MIT
---
```

- `app-description`, when present, replaces `description` as the value
  packaged for claude.ai and is what's checked against the 200-char limit.
- `app-name`, when present, replaces the skill's directory name as the
  packaged name — used for the staged directory, the zip filename, and the
  `name:` field written into the output SKILL.md. It's still validated
  against claude.ai's name rules (see below). The directory name must still
  match the skill's plain `name:` field as before; `app-name` only affects
  the packaged output identity.
- Neither field is ever written into the output SKILL.md — the packaged
  frontmatter always contains only `name` / `description` / `license`
  (using the effective, possibly `app-*`-overridden values).
- Without `app-description`/`app-name`, the build uses the skill's normal
  `description`/`name` and hard-fails if those don't satisfy claude.ai's
  limits.

### Name validation

claude.ai's skill names must be at most 64 characters, match
`^[a-z0-9-]+$` (lowercase letters, digits, hyphens only), and must not
contain `claude` or `anthropic` as a substring (reserved words). The builder
hard-fails on violation, checking only the **effective** name — `app-name`
when set, otherwise the plain `name`. This is why `app-name` exists: a
skill whose plain `name` contains a reserved word (e.g.
`recover-deleted-claude-conversation`) can still ship, by setting an
`app-name` that satisfies the rules; the plain `name` itself is never
checked against these rules once an `app-name` override is present.

Two more checks run before any files are written:

- **No symlinks.** A skill directory containing a symlink fails the build —
  `shutil.copytree` would otherwise dereference it and package whatever it
  points at (potentially a file outside the repo) into the zip.
- **No effective-name collisions.** If two skills in the same build resolve
  to the same effective name (e.g. two different skills both set
  `app-name: foo`), the build fails before touching `dist/` — otherwise the
  second one silently overwrites the first's staged output and zip.

### Body length warning

If a SKILL.md body runs past 500 lines, the builder prints a warning (not a
hard-fail) — long bodies work but cost more context when Claude reads the
skill.

### Excluded from the package

Beyond `.DS_Store`, `*.swp`/`*.swo`, and `design-notes.md`, the builder also
drops `backlog.md`, `catalog.md`, and the entire `evals/` and `research/`
directories wherever they appear under a skill. These are
development-only artifacts (iteration notes, eval corpora, research
scratch) that add nothing a packaged skill needs at load time and can be
sizeable — humanizer-zh's `evals/`+`research/` alone ran past 1MB.

### `--list` and the interactive menu

`--list` prints a status table (skill name, effective description length,
whether `app-description` is set, effective `app-name` if set, pass/fail
against the 200-char limit) for every skill under `skills/` and exits
without building anything.

Running the script with no arguments in an interactive terminal shows the
same kind of table as a numbered menu and prompts for a selection: comma-
separated indices (`1,3,5`), ranges (`1-4`), combinations of both
(`1,3-5`), or `all`. An empty line cancels cleanly. Invalid input (a
non-numeric token, an out-of-range index) prints an error and exits 1
rather than re-prompting. With no arguments and no TTY on stdin (e.g. piped
input, CI), the script exits 1 immediately with a message pointing at
`--all` / `--list` / explicit skill names, rather than hanging.

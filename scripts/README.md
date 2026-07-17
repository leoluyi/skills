# scripts

## build-app-skills.py

Builds Claude-app-uploadable `.zip` packages from `skills/`.

```sh
uv run scripts/build-app-skills.py               # build the default set
uv run scripts/build-app-skills.py plain-speak   # build only named skills
```

Output lands in `dist/` (git-ignored). Each `dist/<name>.zip` contains a single
top-level `<name>/` folder — the layout claude.ai's skill uploader expects.

The Claude app reads only `name` / `description` / `license` frontmatter and
caps `description` at 1024 characters. The builder rewrites each SKILL.md down
to those fields; source files under `skills/` are never modified.

### Overrides

When a skill's `description` exceeds 1024 chars, add a trimmed replacement at
`scripts/app-skill-overrides/<name>.txt` (plain text, one paragraph). The build
uses it verbatim in place of the source description. Without an override, the
build hard-fails rather than shipping a package the app will reject.

Current overrides:

- `avoid-ai-writing-zh.txt` — source description folds to 1193 chars; trimmed to
  ~996 by dropping the cross-skill routing sentence and shortening the
  blog-writing-zh handoff tail.

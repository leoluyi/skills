---
name: obsidian-vault
description: Search, create, and manage notes in the Obsidian vault with wikilinks. Use when user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

## Vault location

`/Users/leoluyi/Library/CloudStorage/Dropbox/__notes-vault`

PARA / Johnny-Decimal structure, organized into numbered top-level folders:

- `00-inbox`, `inbox` — unprocessed capture
- `01-unique-notes` — atomic/evergreen notes
- `02-life`, `03-investment`, `04-work`, `05-tech` — areas by domain
- `97-projects`, `98-archived`, `99-system` — projects, archive, vault system

AI and writing notes live in `05-tech/AI/`.

## Naming conventions

- **Title Case** for conceptual notes (e.g. `Writing With AI.md`, `Prompt Engineering`)
- **lowercase-hyphen** also used for utility notes (e.g. `ai-prompt.md`)
- Domain root notes in `05-tech` use a `[Category]` bracket style (e.g. `[Python]`, `[Docker-Podman]`)
- Organize by the numbered folders plus links — not deep nesting

## Frontmatter

Notes carry YAML frontmatter with:

```yaml
---
id: kebab-case-id
aliases:
  - Alternate Title
  - 中文別名
tags:
  - AI
urls:
  - "[source label](https://...)"   # optional
---
```

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Put related/dependency links in a `## Related` section at the bottom
- Dangling links to notes that don't exist yet are fine — they mark notes worth writing

## Workflows

### Search for notes

```bash
V="/Users/leoluyi/Library/CloudStorage/Dropbox/__notes-vault"
# By filename
find "$V" -name "*.md" -not -path "*/.obsidian/*" | grep -i "keyword"
# By content
grep -rl "keyword" "$V" --include="*.md" --exclude-dir=.obsidian
```

Or use Grep/Glob tools directly on the vault path.

### Create a new note

1. Pick the right numbered folder (AI/writing → `05-tech/AI/`)
2. Use **Title Case** for the filename
3. Add frontmatter (`id`, `aliases`, `tags`)
4. Write content as a unit of learning
5. Add `[[wikilinks]]` to related notes in a `## Related` section at the bottom

### Find backlinks to a note

```bash
grep -rl "\\[\\[Note Title\\]\\]" "/Users/leoluyi/Library/CloudStorage/Dropbox/__notes-vault" --include="*.md"
```

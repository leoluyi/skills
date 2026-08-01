# Obsidian Vault Notes

This skill searches, creates, and links notes inside an Obsidian vault, keeping every note on the vault's existing PARA / Johnny-Decimal folder structure and using `[[wikilinks]]` for connections instead of freeform prose links.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a obsidian-vault -y
```

To update later:

```
npx skills update obsidian-vault
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/obsidian-vault/SKILL.md)

The SKILL.md ships with one specific vault path hard-coded. Before using it on your own machine, edit that path (and the numbered-folder list, if your vault uses a different scheme) to point at your own vault — don't assume the shipped path is portable.

## What it does

- **Search** the vault by filename (`find ... -not -path "*/.obsidian/*"`) or by content (`grep -rl ... --exclude-dir=.obsidian`), always skipping Obsidian's internal `.obsidian` directory.
- **Create notes** in the correct PARA / Johnny-Decimal folder for the topic, named in the vault's established case convention (Title Case for conceptual notes, lowercase-hyphen for utility notes), with YAML frontmatter (`id`, `aliases`, `tags`, optional `urls`).
- **Link notes** using `[[wikilinks]]`, collecting related/dependency links into a `## Related` section at the bottom of the note. Dangling links to notes that don't exist yet are left as-is — they mark notes worth writing later.
- **Find backlinks** to any note with a single `grep -rl "\[\[Note Title\]\]"` across the vault.

## When to use

Reach for it when you want to find, create, or organize notes in your Obsidian vault — searching for an existing note, filing a new one in the right place, or wiring up links between notes.

## When not to

Not for turning notes into a blog post — that's blog-writing-zh's job. Not for assembling notes into a structured technical document with tutorial/how-to/reference/explanation sections — that's knowledge-doc-writing's job. This skill only manages the vault itself: search, create, link.

## How it works

The vault follows a PARA / Johnny-Decimal layout: numbered top-level folders like `00-inbox` (unprocessed capture), `01-unique-notes` (atomic/evergreen notes), `02`–`05` for life/investment/work/tech areas, and `97`–`99` for projects, archive, and vault system. Filing a new note means picking the numbered folder that matches its domain (for example, AI and writing notes go under `05-tech/AI/`), not inventing a new folder or nesting deeply — organization comes from the fixed numbered folders plus wikilinks between notes, not from folder depth.

## Related skills

- **blog-writing-zh** — turns a vault note into a polished blog post once the note itself is written; this skill stops at managing the note.
- **knowledge-doc-writing** — restructures distilled material into a four-part Diátaxis document; use it once you have notes worth compiling into reference-grade documentation.
- **learn-loop** — an interactive teach-then-quiz loop that ends by writing a note into this same vault; reach for it instead when the goal is genuinely learning a concept, not just filing one.

# Writing catalog entries and guide pages

This repo has two per-skill public-facing surfaces, both rendered by `tools/build-docs`. Keep them separate: a **catalog entry** is the card-sized summary shown everywhere the skill is listed; a **guide page** is the optional deep-dive a reader opens after the card gets their attention. Neither substitutes for the other — a catalog entry that tries to explain mechanism becomes unreadable at card size, and a guide page that just repeats the tagline wastes the click.

## Catalog entry — `skills/<slug>/catalog.md`

The single source of truth for a skill's card. YAML front matter holding the skill's bilingual title, tagline, when-to-use / when-not, and highlights. Renders into:

- **`README.md`** / **`README.zh-TW.md`** — the `## Skill catalog` / `## 技能目錄` sections, generated between `<!-- CATALOG:START -->` / `<!-- CATALOG:END -->` markers, plus the shields skill-count badge (`badge/skills-N-`) at the top of each file. Neither is hand-edited; the generator hard-fails if the markers or the badge go missing.
- **`docs/index.html`** — the interactive catalog at `https://leoluyi.tw/skills/`. Generated; not committed (gitignored, built by CI).
- **`docs/skills.json`** — the machine-readable twin (used by `npx skills` and any tool reading the catalog programmatically). Generated; not committed.

`docs/catalog.yml` holds the six category definitions (bilingual label + blurb, and an optional `readmeNote`) that every skill's `category` field points into.

Act whenever a skill is added, renamed, recategorized, or has its trigger/description changed enough that the tagline or highlights go stale — edit `skills/<slug>/catalog.md`, then rebuild (see below).

## Guide page — `skills/<slug>/guide.en.md` + `skills/<slug>/guide.zh.md`

Optional. When both files exist for a skill, `tools/build-docs` renders them into `docs/guide/<slug>/index.html` (`https://leoluyi.tw/skills/guide/<slug>/`) and adds a "Read the guide →" link to that skill's catalog card. A skill with no guide files is skipped silently — no broken link, no red build.

Pure Markdown, no front matter — the H1 is the page title, everything else (category, tagline, badges) already lives in `catalog.md` and gets pulled in by the generator, so don't duplicate it here. Six fixed sections, modeled on [mattpocock/skills/docs](https://github.com/mattpocock/skills/tree/main/docs):

1. One-paragraph lede — what the skill is, in plain terms.
2. `## Install` — the `npx skills add … -a <slug> -y` / `update` commands and a `[Source](.../SKILL.md)` link.
3. `## What it does` — behavior and actual mechanisms, never adjectives.
4. `## When to use` / `## When not to` — mirrors `catalog.md`'s `whenUse`/`whenNot` in substance, in the reader's own terms.
5. `## How it works` — the 1-2 mechanisms that actually decide the output. This is the section that earns the page's existence; be concrete, use a worked example over an abstract description.
6. `## Related skills` — the "use Y instead" pointers already in `SKILL.md`'s description, each with the one clause explaining why.

Write both languages — the generator only builds a guide page once both `guide.en.md` and `guide.zh.md` exist; a lone half of a pair is silently skipped (no page, no error), so a guide added in one language and forgotten in the other never goes live.

## Rebuilding

Whenever you touch a `catalog.md` or a `guide.*.md` pair, run:

```bash
uv run tools/build-docs
```

This regenerates `docs/index.html`, `docs/skills.json`, `docs/guide/<slug>/index.html` for every skill with guide files, and both READMEs' catalog sections and skill-count badges, in one pass. Commit the `catalog.md` / `guide.*.md` changes and the regenerated READMEs; the `docs/` build artifacts (`index.html`, `skills.json`, `guide/`) are rebuilt by the GitHub Pages workflow (`.github/workflows/pages.yml`) on every push to `main`, so don't hand-edit or commit them.

Forgetting the rebuild is caught in CI: `.github/workflows/docs-check.yml` runs `uv run tools/build-docs --check` on every PR and every push to `main` that touches a catalog or guide input, and fails if either README has drifted. The `docs/` build artifacts are gitignored, so `--check` compares them only when they already exist locally — on a fresh checkout it verifies the READMEs alone.

### `catalog.md` front matter reference

```markdown
---
emoji: "✍️"
category: <catalog.yml category key>
order: <int — position within the category's card/table list>
languages: [en, zh-TW, mixed]   # any subset; drives the EN/繁中/中英 badges, in this order
tags: [tag-one, tag-two, ...]
title:    { en: "<Display Name>", zh: "<顯示名稱>" }
tagline:  { en: "<one-liner>", zh: "<一句話>" }         # used verbatim as the README row too
whenUse:  { en: "...", zh: "..." }
whenNot:  { en: "...", zh: "..." }
highlights:
  en: ["...", "...", "...", "..."]   # 3-5 bullets naming actual mechanisms, never adjectives
  zh: ["...", "...", "...", "..."]
---
```

Invocation (`user-invoked` / `model-invoked`) is **not** a field here — the generator reads it straight from the skill's own `SKILL.md` frontmatter (`disable-model-invocation: true`), so there is nothing to keep in sync.

**"When to use" / "When not to"** mirror the skill's own routing lines — if `SKILL.md`'s description already states "不要用於 X（用 Y）", that boundary belongs here verbatim in substance, not reinvented. **Highlights** are 3-5 bullets naming the skill's actual mechanisms (modes, gates, what it protects against) — never marketing adjectives with nothing behind them.

`tagline` is the **only** description surfaced everywhere (card, `skills.json`, README row, and the page's JSON-LD `description`). Keep it accurate to all four; don't write a shorter "card" version and a longer "README" version — that duplication is exactly the drift this generator exists to remove.

## `docs/catalog.yml`

Add a category here before pointing any skill's `category` field at it — the generator hard-fails on an unknown category key. `readmeNote` is optional: a short bilingual sentence rendered under the `###` heading in the README only (used today for `docs-design`'s "no Chinese required" note); omit it unless a category genuinely needs an editorial aside beyond its `blurb`.

## Conventions

- Bilingual is not optional — every text field needs both `en` and `zh`; the generator validates this and fails loudly rather than emitting a half-empty card.
- `order` controls display order within a category (cards, filters, README table rows); it does not need to be dense or globally unique, only locally ordered.
- The flat `skills` array inside `docs/skills.json` (and the page's JSON-LD `itemListElement`) is sorted alphabetically by slug, independent of category/`order` — this matches the pre-generator format and is what any external consumer parsing that array should expect.

## Done when

- `uv run tools/build-docs` exits 0 with no validation errors, and its "generated N skills across M categories, K guide pages" line matches the actual counts.
- `uv run tools/build-docs --check` exits 0 — this is the gate CI runs, so a stale catalog table, badge, or guide page fails the PR.
- `git diff` shows the expected `catalog.md` / `guide.*.md` change plus the regenerated `README.md` / `README.zh-TW.md` catalog sections and badge counts — nothing else.
- Every skill shows a `user-invoked` or `model-invoked` label on all three surfaces (card pill, README column, invocation filter), and it is `user-invoked` if and only if the skill's `SKILL.md` sets `disable-model-invocation: true`.
- Every link (`skills/<slug>/SKILL.md` in READMEs, the full GitHub URL in `skillUrl`, the "Read the guide" card link, `guideUrl` in `skills.json`) resolves.
- A guide page renders in both languages with no half-rendered section, and its sidebar highlights the current skill.

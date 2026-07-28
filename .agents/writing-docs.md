# Writing catalog entries

This repo has no per-skill hosted docs page. The equivalent surface is a **catalog entry** — one Markdown source file that `tools/build-docs` renders into every surface that shows it:

- **`skills/<slug>/catalog.md`** — the single source of truth. YAML front matter holding the skill's bilingual title, tagline, when-to-use / when-not, and highlights.
- **`README.md`** / **`README.zh-TW.md`** — the `## Skill catalog` / `## 技能目錄` sections, generated between `<!-- CATALOG:START -->` / `<!-- CATALOG:END -->` markers, plus the shields skill-count badge (`badge/skills-N-`) at the top of each file. Neither is hand-edited; the generator hard-fails if the markers or the badge go missing.
- **`docs/index.html`** — the interactive catalog at `https://leoluyi.tw/skills/`. Generated; not committed (gitignored, built by CI).
- **`docs/skills.json`** — the machine-readable twin (used by `npx skills` and any tool reading the catalog programmatically). Generated; not committed.

`docs/catalog.yml` holds the four category definitions (bilingual label + blurb, and an optional `readmeNote`) that every skill's `category` field points into.

Act whenever a skill is added, renamed, recategorized, or has its trigger/description changed enough that the tagline or highlights go stale — edit `skills/<slug>/catalog.md`, then run:

```bash
uv run tools/build-docs
```

This regenerates `docs/index.html`, `docs/skills.json`, and both READMEs' catalog sections and skill-count badges in one pass. Commit the `catalog.md` change and the regenerated READMEs; `docs/index.html` / `docs/skills.json` are rebuilt by the GitHub Pages workflow (`.github/workflows/pages.yml`) on every push to `main`, so don't hand-edit or commit them.

Forgetting the rebuild is caught in CI: `.github/workflows/docs-check.yml` runs `uv run tools/build-docs --check` on every PR and every push to `main` that touches a catalog input, and fails if either README has drifted. The two `docs/` artifacts are gitignored, so `--check` compares them only when they already exist locally — on a fresh checkout it verifies the READMEs alone.

## `skills/<slug>/catalog.md`

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

`invokeOnly` is **not** a field here — the generator reads it straight from the skill's own `SKILL.md` frontmatter (`disable-model-invocation: true`), so there is nothing to keep in sync.

**"When to use" / "When not to"** mirror the skill's own routing lines — if `SKILL.md`'s description already states "不要用於 X（用 Y）", that boundary belongs here verbatim in substance, not reinvented. **Highlights** are 3-5 bullets naming the skill's actual mechanisms (modes, gates, what it protects against) — never marketing adjectives with nothing behind them.

`tagline` is the **only** description surfaced everywhere (card, `skills.json`, README row, and the page's JSON-LD `description`). Keep it accurate to all four; don't write a shorter "card" version and a longer "README" version — that duplication is exactly the drift this generator exists to remove.

## `docs/catalog.yml`

Add a category here before pointing any skill's `category` field at it — the generator hard-fails on an unknown category key. `readmeNote` is optional: a short bilingual sentence rendered under the `###` heading in the README only (used today for `docs-design`'s "no Chinese required" note); omit it unless a category genuinely needs an editorial aside beyond its `blurb`.

## Conventions

- Bilingual is not optional — every text field needs both `en` and `zh`; the generator validates this and fails loudly rather than emitting a half-empty card.
- `order` controls display order within a category (cards, filters, README table rows); it does not need to be dense or globally unique, only locally ordered.
- The flat `skills` array inside `docs/skills.json` (and the page's JSON-LD `itemListElement`) is sorted alphabetically by slug, independent of category/`order` — this matches the pre-generator format and is what any external consumer parsing that array should expect.

## Done when

- `uv run tools/build-docs` exits 0 with no validation errors, and its "generated N skills across M categories" line matches the actual count.
- `uv run tools/build-docs --check` exits 0 — this is the gate CI runs, so a stale catalog table or badge fails the PR.
- `git diff` shows the expected `catalog.md` change plus the regenerated `README.md` / `README.zh-TW.md` catalog sections and badge counts — nothing else.
- The `invoke-only` badge/table-suffix appears if and only if the skill's `SKILL.md` sets `disable-model-invocation: true`.
- Every link (`skills/<slug>/SKILL.md` in READMEs, the full GitHub URL in `skillUrl`) resolves.

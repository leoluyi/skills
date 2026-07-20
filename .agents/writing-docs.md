# Writing catalog entries

This repo has no per-skill hosted docs page. The equivalent surface is a **catalog entry** — three artifacts, kept in sync, describing the same skill:

- **`README.md`** — one row in the `## Skill catalog` table, under the matching `###` category heading. English.
- **`README.zh-TW.md`** — the mirrored row in the Traditional Chinese translation of the same README. Full parity, not a stub.
- **`docs/index.html`** — one `<article class="card">`, plus its filter entry, in the interactive catalog at `https://leoluyi.tw/skills/`.
- **`docs/skills.json`** — the machine-readable twin of the same card content (used by `npx skills` and any tool reading the catalog programmatically).

None of these is generated from the others — no build script produces them from `SKILL.md`. Editing one and forgetting the rest is the standard way this drifts; treat all four writes (three files, since the two READMEs are one edit each) as one change.

Act whenever a skill is added, renamed, recategorized, or has its trigger/description changed enough that the one-liner or highlights go stale.

## The four surfaces

### `README.md` row

```markdown
| **<Display Name>**<br>[`<slug>`](skills/<slug>/SKILL.md) | <one-line what-it-does> |
```

Append `` `invoke-only` `` after the link when the skill sets `disable-model-invocation: true` in its frontmatter (the repo's actual invocation split — see the frontmatter, not a separate doc convention). Place the row under the correct `###` category heading; if none fits, that is a signal to propose a new category, not to force-fit one.

### `README.zh-TW.md` row

Same row, in Traditional Chinese, in the matching category section of that file. This is a parallel document, not a linked reference — every English README edit needs its zh-TW twin or the two drift out of parity.

### `docs/index.html` card

```html
<article class="card" data-cat="<category-key>" data-search="<slug> <name-en> <name-zh> <tagline-en> <tagline-zh> <tags...>">
  <div class="card-top">
    <div class="emoji" aria-hidden="true"><emoji></div>
    <div>
      <h3 class="card-title"><span class="l-en"><Name></span><span class="l-zh"><名稱></span>
        <code class="slug"><slug></code>
      </h3>
      <div class="badges"><span class="badge lang"><繁中|EN></span><!-- + <span class="badge invoke"><span class="l-en">Invoke-only</span><span class="l-zh">手動叫用</span></span> if invoke-only --></div>
    </div>
  </div>
  <p class="tagline"><span class="l-en"><one-liner></span><span class="l-zh"><一句話>></span></p>
  <details>
    <summary><span class="l-en">What it does</span><span class="l-zh">細節</span></summary>
    <div class="detail-block">
      <h4><span class="l-en">When to use</span><span class="l-zh">何時使用</span></h4>
      <p><span class="l-en">...</span><span class="l-zh">...</span></p>
      <h4><span class="l-en">When not to</span><span class="l-zh">何時不要</span></h4>
      <p><span class="l-en">...</span><span class="l-zh">...</span></p>
      <h4><span class="l-en">Highlights</span><span class="l-zh">重點</span></h4>
      <ul>
        <li><span class="l-en">...</span><span class="l-zh">...</span></li>
      </ul>
    </div>
  </details>
  <div class="tags"><span class="tag">#tag</span>...</div>
  <div class="card-foot">
    <a href="https://github.com/leoluyi/skills/blob/main/skills/<slug>/SKILL.md"><span class="l-en">Read SKILL.md</span><span class="l-zh">看 SKILL.md</span> &rarr;</a>
  </div>
</article>
```

Every span comes in an `.l-en`/`.l-zh` pair — never English-only or zh-only prose inside a card; the page's language toggle depends on both existing. `data-cat` must be one of the existing keys in the `.filters` block (currently `zh-writing-quality`, `business-docs`, `docs-design`, `knowledge-mgmt`) or a newly added one, wired into the filter buttons at the same time. `data-search` is the free-text index the client-side search matches against — pack it with the slug, both-language names, both-language tagline, and tag words; this is the one field that tolerates redundancy, since it exists purely to be matched, never read.

**"When to use" / "When not to"** mirror the skill's own routing lines — if the `SKILL.md` description already states "不要用於 X（用 Y）", that boundary belongs here verbatim in substance, not reinvented. **Highlights** are 3-5 bullets naming the skill's actual mechanisms (modes, gates, what it protects against) — never marketing adjectives with nothing behind them.

### `docs/skills.json` entry

Add the skill's slug to its category's `slugs` array, and add its full record to the flat entry list (mirrors the card's `l-en`/`l-zh` fields plus `skillUrl`). Bump the top-level `count`. Keep field order and nesting consistent with neighboring entries — this file has no schema validation, so a malformed entry fails silently at read time, not at write time.

## Conventions

- Explain the **why** and the **boundary**, not the mechanism. A card orients a reader deciding whether to reach for this skill; it never reproduces `SKILL.md`'s internal steps or reference tables.
- Bilingual is not optional on any of the four surfaces. A skill that is English-only in practice (e.g. `infographic-design`) still gets both `.l-en`/`.l-zh` spans on the card — the *site* is bilingual even where a given skill's own output isn't.
- Keep the entry itself low-load: a tagline that already says the job doesn't need a Highlights bullet restating it in other words.

## Done when

- All four surfaces (`README.md`, `README.zh-TW.md`, `docs/index.html` card + filters, `docs/skills.json`) mention the skill, agree on its name, category, and one-liner, and none is missing.
- The `invoke-only` tag/badge is present on all three surfaces if and only if the skill's frontmatter sets `disable-model-invocation: true`.
- Every link (`skills/<slug>/SKILL.md` in READMEs, the full GitHub URL in the card and `skills.json`) resolves.
- `docs/skills.json`'s top-level `count` matches the actual number of skills, and the new slug appears in exactly one category's `slugs` array.
- The card's `data-cat` matches an existing (or newly wired) filter key, and `data-search` includes the slug, both-language name, and both-language tagline.
- "When to use" / "When not to" reflect the skill's real routing boundary against its nearest siblings, not a generic description.

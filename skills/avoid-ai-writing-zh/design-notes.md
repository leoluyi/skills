# Design notes — avoid-ai-writing-zh

Maintainer notes — provenance and build process for this one skill.

## What this skill is, structurally

A bilingual (English + Traditional-Chinese) fork of the English-only `avoid-ai-writing` skill. The English detection layer tracks an upstream repo verbatim; the Traditional-Chinese layer is our own value-add.

```
SKILL.md
  ## What this skill is / ## Modes           — our framing (not upstream)
  ## Language-agnostic structural rules       — rebased from upstream (rhythm, TTR, reshuffle, treadmill, when-to-rewrite) + one local addition (scope ladder, see below)
  ## English AI-isms                          — rebased from upstream, verbatim, inline + one local addition (breaking the fourth wall, see below)
  ## Traditional Chinese AI-isms              — our layer: 對應英文分類 + zh 特有補充
  ## Severity tiers / Context profiles / …    — our framing

references/
  english-phrase-rules.md   — ONLY upstream's "Words and phrases to replace" (Tier 1/2/3 + Tier-3 phrases)
  zh-phrase-rules.md        — the six zh「詞→替換」lookup tables
```

## The split rule (what goes to a reference file)

Only the **enumerable word/phrase → replacement lookup table** is pushed to a `references/` file — the bulky dictionary you consult on demand. Everything else stays inline in `SKILL.md` so it reads in one pass:

- **English** → `english-phrase-rules.md` holds only `Words and phrases to replace` (the tiered table). Formatting, sentence-structure, the behavioral/structural micro-categories, and the shorter phrase lists (Template / Transition / Filler / Generic-conclusions / Confidence-calibration) are all inline.
- **zh** → `zh-phrase-rules.md` holds the six「詞→替換」tables (空話／口號, 確保 family, 至關重要, AI 句式, 慣用詞替換, Taiwan term preferences). The behavioral rules, the abstract→concrete rewrite table, and the Allowed-patterns carve-outs stay inline.

## English is rebased from upstream — verbatim

Upstream: **https://github.com/conorbronsdon/avoid-ai-writing**
Last rebased against: **v3.16.0** (2026-07-15), commit `af34612`.

The English AI-isms section and the language-agnostic structural rules are pulled from upstream's `## What to remove or fix` **word-for-word (一字不漏)** — no paraphrasing, nothing dropped. This means:

- Upstream's in-text provenance/attribution lines (e.g. `adapted from brandonwise/humanizer`, `Adapted from blader/humanizer P27`) come in as-is. This is a deliberate exception to the repo-wide "strip derivation noise" convention in the root `CLAUDE.md` — the verbatim-rebase instruction takes precedence for the English layer. If a future maintainer wants them stripped, do it as a separate, explicit pass.

### Re-sync workflow

1. `git clone --depth 1 https://github.com/conorbronsdon/avoid-ai-writing` to a scratch dir.
2. Parse its `## What to remove or fix` into `### ` blocks.
3. Route: `Words and phrases to replace` → `english-phrase-rules.md`; the five language-agnostic blocks (Rhythm and uniformity, Vocabulary diversity, Paragraph-reshuffle immunity, Treadmill effect, When to rewrite) → our `## Language-agnostic structural rules`; everything else → `## English AI-isms` inline, in upstream order.
4. Re-insert the two local additions (below — `### Scope ladder` after the language-agnostic blocks, `### Breaking the fourth wall` after `Acknowledgment loops`), then update the version/commit line above.

The scratch scripts used for the last rebase (`split_eng.py`, `rebase_eng2.py`, delta analysis) are throwaway — regenerate as needed.

## Local additions on top of upstream

Two blocks inside the rebased-verbatim layers are ours. Re-insert both on every rebase (named in the workflow above); don't let an upstream diff overwrite either.

**`### Scope ladder`** — in the language-agnostic section, after `When to rewrite from scratch vs. patch`. Upstream's Fix guidance is uniformly span-local; this repo needed a second tier because several zh-authored tonal/stance features (第二人稱教練口吻, 打破第四面牆, 空降斷言／空降主張, 警句式評語, 破碎短句堆疊, contrarian-framed paragraphs) break when patched sentence-by-sentence: fixing the flagged sentence while a neighbor still carries the same tell produces a paragraph with a mismatched subject. The section defines the paragraph-rewrite tier plus its two governing rules (reframe-not-delete, flag-hollow-don't-ghostwrite) and is the single source of truth the affected rule bodies (e.g. 對讀者說教) point back to. It stays English like the rest of that section; the inline zh names are proper-noun cross-references, not translation.

**`### Breaking the fourth wall`** — in the English AI-isms section, after `Acknowledgment loops`. Load-bearing in our Severity tiers (a P0 credibility killer), and it fires on English/mixed software-dev docs (README/ADR/CONTRIBUTING) where the zh twin `打破第四面牆` — gated on "text contains CJK" — won't reach. That zh twin (`打破第四面牆 — 工作情境外洩／生成過程外洩`) is the fuller treatment and the namesake of the root `CLAUDE.md` authoring convention.

## The zh layer

Organized to mirror the English division:

- **對應英文分類** — short zh rules that directly parallel an English category (Contrarian, Copula inflation, Excessive adjective stacking, Slash enumeration, Synonym cycling, Formulaic challenge, Negative framing). Bodies carry「與英文版 X 同源」cross-refs.
- **zh 特有補充（英文缺的）** — fuller zh-authored rules with no direct English one-liner, or that need more complete handling: 空降斷言／空降主張, 頓號串列, 口語化萬能動詞, 過度簡寫, 破折號濫用, 警句式評語, 破碎短句堆疊, 口號式短句, 打破第四面牆, 結構級訊號, 專有名詞過度翻譯, 翻譯腔, plus the abstract→concrete rewrite table. Ends with the Allowed-patterns carve-out table (governs the whole zh section).

When our fork was cut it stripped upstream's provenance lines from the shared categories (per the root `CLAUDE.md` convention). The verbatim rebase re-introduces them into the English layer only; the zh layer stays convention-clean.

# DEVELOPMENT — avoid-ai-writing-zh

Maintainer notes. None of this belongs in `SKILL.md` or `references/` (those are runtime instructions the model loads); provenance and process live here.

## What this skill is, structurally

A bilingual (English + Traditional-Chinese) fork of the English-only `avoid-ai-writing` skill. The English detection layer tracks an upstream repo verbatim; the Traditional-Chinese layer is our own value-add.

```
SKILL.md
  ## What this skill is / ## Modes           — our framing (not upstream)
  ## Language-agnostic structural rules       — rebased from upstream (rhythm, TTR, reshuffle, treadmill, when-to-rewrite)
  ## English AI-isms                          — rebased from upstream, verbatim, inline
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
4. Re-insert the one local addition (below), then update the version/commit line above.

The scratch scripts used for the last rebase (`split_eng.py`, `rebase_eng2.py`, delta analysis) are throwaway — regenerate as needed.

## The one local English addition on top of upstream

**`### Breaking the fourth wall`** (inserted after `Acknowledgment loops`). Not in upstream. Retained deliberately because:

- It is load-bearing in our Severity tiers (referenced as a P0 credibility killer).
- It fires on English/mixed software-dev docs (README/ADR/CONTRIBUTING) — the zh twin `打破第四面牆` is gated on "text contains CJK" and won't cover pure-English docs.

Keep re-inserting it on every rebase. Its zh twin (`打破第四面牆 — 工作情境外洩／生成過程外洩`) is the fuller treatment and is the namesake of the root `CLAUDE.md` authoring convention (`打破第四面牆 / 生成過程外洩`).

## The zh layer

Organized to mirror the English division:

- **對應英文分類** — short zh rules that directly parallel an English category (Contrarian, Copula inflation, Excessive adjective stacking, Slash enumeration, Synonym cycling, Formulaic challenge, Negative framing). Bodies carry「與英文版 X 同源」cross-refs.
- **zh 特有補充（英文缺的）** — fuller zh-authored rules with no direct English one-liner, or that need more complete handling: 空降斷言／空降主張, 頓號串列, 口語化萬能動詞, 過度簡寫, 破折號濫用, 警句式評語, 破碎短句堆疊, 打破第四面牆, 結構級訊號, 專有名詞過度翻譯, plus the abstract→concrete rewrite table. Ends with the Allowed-patterns carve-out table (governs the whole zh section).

When our fork was cut it stripped upstream's provenance lines from the shared categories (per the root `CLAUDE.md` convention). The verbatim rebase re-introduces them into the English layer only; the zh layer stays convention-clean.

## Finishing check

Before finalizing a zh edit, run the root-`CLAUDE.md` grep over `SKILL.md` + `references/`. Hits inside the **English** layer that are upstream attributions are expected (see verbatim note above); hits inside the **zh** layer are noise and should move here.

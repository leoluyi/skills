# Briefing Outline

Briefing Outline distills one long report or a whole set of source documents into a single 說明提綱 — a high-altitude overview a manager or committee can grasp at a glance, with every part still pointing back down to the source for detail.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a briefing-outline -y
```

To pull updates later:

```
npx skills update briefing-outline
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/briefing-outline/SKILL.md)

## What it does

Given one or more sources — separate documents, or the sections of one long report — it inventories what each holds, then lays out a MECE spine (一、二、三…) where each source's essence lives in exactly one section. Each section is drafted purpose-first: a label naming the intent (目的／要驗證／要達成), then the essence, then a pointer down — 「（詳《source》）」— for anything that belongs in the source instead: 逐項標準、權重、SOP、原始碼、完整明細. The result reads as one coherent document, not a stitched summary, and stays stable when a source is revised because only the affected section needs a re-run.

## When to use

Reach for it when you need to condense one or more source documents into a navigable briefing that a manager or committee can grasp at a glance and drill into when they need more — a project proposal bundle, a long evaluation report broken into its own sections, or an existing 提綱 whose sources just changed and needs re-syncing.

## When not to

Not for authoring a single formal document from scratch (use formal-doc-structure), for an RFP or 需求規格書 (use rfp-writing), for lowering one term or passage to a non-technical reader (use plain-speak), or for pure language cleanup with no structural work (use humanizer-zh).

## How it works

Each item earns its space rather than getting a flat treatment: a paragraph is justified only when the item is non-obvious (the reader can't reconstruct it from the label alone), self-arguing (it carries a rationale that pre-empts an objection), or decision-bearing (it embeds a choice the reader must approve). Everything else collapses to a label and a pointer down. A number survives at altitude by function, not size — it stays only if it *is* or *proves* a decision, not if it merely parameterizes one.

Re-syncing works the same way: when a source changes, only the sections it feeds get steps re-run, because the MECE spine already guarantees each source maps to exactly one section — there's no need to re-derive the whole outline to absorb one update.

## Related skills

- **formal-doc-structure** — use it instead when you're authoring a single formal document (簽呈, 會議紀錄, 評估報告) from scratch, not distilling existing sources.
- **rfp-writing** — use it instead for a 需求規格書 or 招標規格, which has its own structural rules that conflict with a 提綱's.
- **plain-speak** — use it instead when the job is lowering one term or passage for a lay reader, not restructuring a whole document.
- **humanizer-zh** — use it instead (or as this skill's own step 6) for stripping AI-writing patterns once the outline's structure is already settled.

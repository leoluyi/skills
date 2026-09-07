---
name: mece
description: >-
  MECE problem decomposition and document restructuring: clarify categories, content ownership, overlaps, and gaps. 拆解問題、重整文件架構。
disable-model-invocation: true
version: 0.1.0
license: MIT
compatibility: Claude Code and Codex. No external tools required.
---

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output - option labels, generated-document headings, table column names - not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## MECE

Make the whole visible: readers should immediately understand which distinct matters belong here and where each detail goes.

Choose mode from the request:

- **Review.** If the current structure answers its question with clear sibling boundaries, report only the classification basis, evidence, and bounded gaps, then stop.
- **Proposal.** If an existing document needs restructuring, deliver headings with one-line scopes, a compact source-to-destination mapping, and a structural check. Mapping cells use original headings plus short retain, move, or merge notes; outline sections get one sentence each.
- **Decomposition.** For a new problem, deliver a two-level structure with its basis, assumptions, coverage, and pending gaps.

Proposal mode ends with the structural check and a request for direction approval. The proposal contains labels, one-sentence scopes, and short mapping notes; full source bullets, expanded sections, rewritten paragraphs, conclusions, and templates belong to rewrite mode, which starts only after explicit approval and follows the approved mapping.

1. **Scope.** Read the supplied material and state the question the structure must answer, its boundaries, and necessary assumptions in the output.
   Proceed with reasonable stated assumptions; ask first only when an answer would materially change the classification.
2. **Classification axis.** Build or repair the hierarchy using one classification basis among siblings, with boundaries that let readers assign content unambiguously.
   Rebuild upper levels when needed; separate categories of work from shared discussion dimensions such as responsibility, evidence, or timing.
   Test borderline details against neighboring categories and explain their ownership or handoff boundary.
3. **Coverage.** Account for every supplied point, merging overlapping categories while preserving distinct meanings and constraints.
   Judge mutual exclusivity among sibling categories; introductions, discussion details, and summaries may legitimately repeat a concept for different reader purposes.
   Separate source-supported gaps from inferred possibilities; mark unverified gaps as pending confirmation with reasons, and bound any completeness claim to available evidence.
4. **Deliver.** Present the selected mode's output and a brief check explaining the classification basis, overlaps resolved, and remaining gaps or ambiguous ownership.
   In proposal mode, map every original section to a destination or explicit merge, then request approval and stop.
   In rewrite mode, follow the approved mapping and preserve source facts and unresolved questions.

Stop decomposing when readers can name the main matters and place their details.
For documents, start with two levels; deepen only branches that still mix distinct matters, with item counts and depths determined by content.

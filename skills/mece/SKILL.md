---
name: mece
description: >-
  MECE problem decomposition and document restructuring: clarify categories, content ownership, overlaps, and gaps. 拆解問題、重整文件架構。
disable-model-invocation: true
version: 0.1.0
license: MIT
compatibility: Claude Code and Codex. No external tools required.
---

## Output language

Match the user's language in every heading, label, table cell, and explanation.
For Chinese requests, use Taiwan Traditional Chinese; keep established technical terms in English.
Do not mirror this file's English labels into the response.

## MECE

Make the whole visible: readers should know the distinct matters and where each detail goes.

Choose mode from the request:

- **Review.** If sibling boundaries already answer the document's question, report the basis, evidence, and bounded gaps, then stop.
- **Proposal.** For an existing document that needs restructuring, return the new outline, a source mapping, and a structural check; request approval and stop before rewriting.
- **Decomposition.** For a new problem, return a two-level structure, known-item mapping, assumptions, and pending gaps with reasons.

For every mode, state the question, boundaries, and assumptions; proceed on reasonable assumptions unless an answer would change the classification.
Use one basis among siblings, separate work categories from shared dimensions, and put each detail on one side of a trigger, owner, state, or handoff boundary.
Cover every supplied point, merge only true overlap, and allow repetition when it serves different document functions.
Separate source-supported material from inference, label each unverified gap with its reason, and bound completeness claims to the evidence.

In proposal mode, headings get one-line scopes; every original heading gets a retain, move, or merge destination; end with the structural check and approval request.
Keep full source bullets and rewritten prose for the approved rewrite only; preserve source facts and unresolved questions.
In decomposition mode, label supplied items and pending gaps separately so unverified causes never appear as facts.

Stop when readers can name the main matters and place their details.
Deepen only branches that still mix distinct matters.

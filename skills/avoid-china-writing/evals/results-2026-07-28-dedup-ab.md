# A/B — v1.0.0 → v1.1.0 (SKILL.md ↔ term-table.md dedup)

Run date: 2026-07-28. Cases 2-8 of `evals.json`, both arms. Cases 1, 9, 10, 11, 12 not run on either side.

Method: one independent agent per case per arm, invoking the skill via the Skill tool against the live symlinked copy. Agents saw **only the user prompt**, never the expectations. Judging done separately from returned output and tool traces.

## Result

| Case | Axis | v1.0.0 | v1.1.0 |
|---|---|---|---|
| 2 | P1 黑話 長尾 | 4/4 | 4/4 |
| 3 | 生活／口語 長尾 | 3/3 | 3/3 |
| 4 | 音譯專名 長尾 | 3/3 | 3/3 |
| 5 | 術語例外（保留） | 4/6 | 4/6 |
| 6 | 術語例外（改掉） | 5/5 | 5/5 |
| 7 | 品牌／引文 carve-out | 4/4 | 4/4 |
| 8 | 同形異義 carve-out | 6/6 | 6/6 |
| | | **29/31** | **29/31** |

**Parity, not a win.** Stated plainly because the repo bar is "beat the baseline" and a tie does not clear it on the numbers. The refactor's goal was to cut duplication while holding quality; quality held exactly. Whether parity plus the maintenance win is worth shipping is a judgment call, not something this run settles.

Case 5 scored 4/6 in both arms for the same reason — the eval-design defect recorded in `results-baseline-v1.0.0.md`, not a skill regression.

## What the refactor changed

| Metric | v1.0.0 | v1.1.0 |
|---|---|---|
| SKILL.md lines | 272 | 227 |
| Term rows duplicated across both files | 64 | 25 (the intentional P0 tripwire) |
| Pointers to term-table.md in SKILL.md | 4 | 6 |

A term edit that previously required 5 edits across 2 files (the 複用 change) is now a one-place edit.

## Gains the checklist does not capture

**The `carve-out` gloss fix landed.** v1.0.0's case 7 agent rendered the term 「碳排除項」, reading the English as 碳 (carbon). v1.1.0 agents in cases 5, 7 and 8 all wrote 「排除項」 correctly.

**"Name the specific thing" got stronger.** The rewritten B-section says a synonym swap is not the fix — 「賦能業務」 becomes 「幫業務單位做到 X」, not 「支援業務」. v1.1.0's case 2 agent acted on it, refusing to swap vague for vague and returning the two spots needing the author's own content: 「換掉一個模糊詞卻換上另一個模糊詞，句子還是一樣空——這部分要你補，我不能替你猜」. v1.0.0's case 2 agent produced the synonym swap and only mentioned the emptiness in passing. Case 7 carried the same judgment into quote analysis.

**P2 cluster reasoning transferred.** The rewritten severity section says a cluster of P2s signals a mainland source even when no single one does. v1.1.0's case 3 agent applied exactly that to 立馬／靠譜.

## The routing question, answered

The refactor's central risk was that shrinking the inline core from 93 rows to a 25-row P0 tripwire would break detection when the context pointer failed to fire. It did not fire-fail once. All seven v1.1.0 agents read the term table, and three named the new framing as the reason:

- Case 2: "read in full, because the text is almost entirely axis-B 黑話 and SKILL.md's inline table is a P0 tripwire only"
- Case 3: "needed for 出租車／便利店／公交車／三文魚／奶酪 which are not in SKILL.md's P0 tripwire table"
- Case 4: "the instruction 'any foreign proper noun not among the eight above: look it up' fired correctly and the table resolved every one"

Scope limit: cases 2-8 all contain long-tail terms, so a table read was the correct behaviour in every one. This run does not test whether a P0-only text correctly skips the read — that is what the untested cases 1 and 11 would show.

## Open

- Cases 1, 9, 10, 11, 12 untested on both arms.
- Case 5's 落地 context needs rewriting (see baseline results).

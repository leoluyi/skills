# Baseline — v1.0.0 (pre-dedup refactor)

Run date: 2026-07-28. Subset: cases 2-8 of `evals.json` (the seven the dedup refactor puts at risk). Cases 1, 9, 10, 11, 12 not run — they exercise regions the refactor barely touches.

Method: one independent agent per case, each invoking the skill via the Skill tool against the live symlinked copy. Agents received **only the user prompt** — never the expectations — so nothing could be scored against a visible answer key. Judging done separately from the returned output and tool traces.

## Scores

| Case | Axis | Pass | Note |
|---|---|---|---|
| 2 | P1 黑話 長尾 | 4/4 | All 15 jargon terms handled; also caught 項目→專案, unlisted |
| 3 | 生活／口語 長尾 | 3/3 | 土豆 correctly called a meaning error, not a register issue; also caught 便利店, 打車 |
| 4 | 音譯專名 長尾 | 3/3 | All six transliterations, including the four table-only ones |
| 5 | 術語例外（保留） | 4/6 | See eval-design defect below |
| 6 | 術語例外（改掉） | 5/5 | Also caught 拉細 as a 陸式 verb-complement pattern absent from the table |
| 7 | 品牌／引文 carve-out | 4/4 | Quoted mainland sentence left byte-identical |
| 8 | 同形異義 carve-out | 6/6 | Zero changes — the correct answer |

**Total: 29/31 expectations.**

## The finding that matters

**All seven agents read `references/term-table.md`. 7/7.**

Case 2's agent stated why outright: it needed the table because 拉新／留存／轉化／打透／跑通／抓手不清／賦能生態 are *not in the inline core table*.

This falsifies the stated justification for SKILL.md's 93-row inline core ("高頻核心 inline,快速掃過不用查表"). The inline core prevented zero lookups across these seven cases. It pays context cost on every invocation while the term table does the actual detection work.

Scope limit on that claim: cases 2-8 were designed to need long-tail terms, so a table read was expected. Whether cases 1, 9, 10, 11, 12 (P0-only scan, 簡體 disambiguation, mode branches) also trigger a read is untested. The claim is "the inline core does not prevent lookups when the text has any long-tail term", not "the inline core is never used".

## Cross-case consistency

Cases 5 and 6 use the same words (對齊, 顆粒度, 複用, 數據, 落地) in opposite roles. Both agents independently applied the same test — 有沒有指到具體技術對象 — and reached opposite, correct verdicts. The term-of-art carve-out is doing real work and must survive any refactor intact.

## Defects found

**Eval-design defect, case 5.** The source sentence 「功能落地後上線」 makes 落地 redundant with 上線, so changing it is defensible. The `keeps-or-softflags-landing` and `zero-false-positives` expectations assumed 落地 was safely in term-of-art territory there. Rewrite the case to put 落地 in an unambiguous 導入上線 context, or drop it from that case. Scored as fail here to keep the baseline honest; do not treat the two points as a skill regression.

**Skill defect: `carve-out` has no Chinese gloss.** The case 7 agent rendered it 「碳排除項」 — reading the English as 碳 (carbon). SKILL.md uses the bare English term throughout while instructing output in Chinese, leaving the agent to invent a translation. Give it a Chinese gloss (排除項／例外項) at first use.

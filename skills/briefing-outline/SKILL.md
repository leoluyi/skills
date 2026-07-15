---
name: briefing-outline
description: 說明提綱 (briefing outline) writing — distill a set of detailed source documents into one high-altitude overview that gives each source's purpose and essence, then points to it for detail. Use when the user wants to 整理／撰寫一份說明提綱, condense multiple documents into a navigable briefing for a 主管 or 委員會, or re-sync an existing 提綱 after its source documents changed. Do NOT invoke to author a single formal document from scratch — 簽呈/會議紀錄/報告/專案規劃 (use formal-doc-structure), for RFP / 需求規格書 / 招標規格 (use rfp-writing), for lowering one term or passage to a non-technical audience (use plain-speak), or for pure language cleanup (use avoid-ai-writing-zh). This skill sits above a document set and points down into it.
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing briefing-outline overview zh-tw traditional-chinese business
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F4D1"
---

# 說明提綱 (Briefing Outline)

A 說明提綱 sits at a fixed **altitude**: high enough to see the whole document set at once, always pointing **down** to each source document for the detail. Its reader — a 主管 or 委員會 deciding direction — wants to grasp the whole and know where to drill, not re-read the sources. Every section carries enough essence to stand on its own, then hands off with 「（詳《source》）」.

The recurring failure is drift below altitude — dragging in 逐項標準、逐條規則、逐步操作、完整明細 that belong in the source. Hold altitude and the 提綱 stays readable and stable when sources churn.

## Steps

1. **Inventory the sources.** List every source document and one line on what each holds. Separate the **umbrella overview** (a peer 設立計畫／總說明, if any) from the **detail docs**: the umbrella lends the spine; the detail docs are what you point down to. Completion: every source accounted for.
2. **Fix reader and decision.** One line: who reads this 提綱, to decide what. This sets the altitude for everything below (a decision-maker choosing direction needs 目的 and 關鍵數字, not 執行細則).
3. **Lay the spine.** Order the top-level sections (一、二、三…) so they are **MECE** — 段落分明, each source's essence living in exactly one section (no overlap), the set together covering the whole. Default spine: the process or lifecycle the sources describe (each stage in the order it happens), else the umbrella's own structure. Open with one line naming the spine, and mark each bend with a short transition line that situates the sections about to follow. Place a governing or oversight section beside the phase it governs, not after phases it doesn't touch; only genuinely cross-cutting resourcing tails as an appendix. Completion: every source maps to exactly one section, or is deliberately folded into one.
4. **Draft each section purpose-first.** Lead with the section's intent (目的／要驗證／要達成), then the essence, then point down with 「（詳《source》）」. Rewrite spec-voice into stakeholder-voice — turn a source's noun-list objective (「…之能力／功能／規格」) into a plain 「能做到〔動詞成果〕」 statement — and run the retained sentences through the `plain-speak` skill against the least-technical reader in the room (its repeat-test). Source already at altitude passes through; don't rewrite well-pitched material to rewrite it.
5. **Cut to altitude — per item, not a flat line.** Give each item only the room it **earns** (see Altitude); collapse the rest to a label and point down. When one section is deliberately more granular than its siblings, say so rather than let it read as drift. This is the core editorial act — when in doubt, cut and point down.
6. **Apply house style.** Conform the draft to the style reference below, then run the `avoid-ai-writing-zh` skill on it.
7. **Verify.** Run the draft through every gate in **## Verification** below; each is pass/fail and a fail sends you back to the named step. When a change is important enough, cascade a brief mention into companion overview docs (e.g. a one-page 版). Completion: every gate passes.

**Re-sync branch** — a source document changed: identify the affected sections and re-run steps 4–7 for those only, including the cascade check in step 7.

## Altitude: what stays, at what depth

| Stays in the 提綱 | Points down to the source |
|---|---|
| 目的、範圍、要驗證／要達成 | 逐項標準、權重、門檻與區間 |
| 定義範圍／成本／成果／汰選的數字 | 只用來調參的比例與細分數字 |
| 決策點、汰選與階段邏輯 | 詳細判斷標準、逐條規則、SOP |
| 一句話的成果／驗收方式 | 完整內容、原始碼、設定檔、記錄檔範例 |
| 分類軸（如：門檻 vs 觀察） | 表格內的逐列明細 |

Two moves the table can't show:
- **Keep the container's dimensions, drop the payload.** An artifact's dimensions (時長、項數、類型數) scope it at no cost and stay; its contents (逐題、逐條、逐項的內容) go down. A number survives by *function*, not size — it stays if it *is* or *proves* a decision, goes if it only parameterizes one.
- **Keep the schema, drop the rows.** A below-altitude criteria table collapses to its classification axis in one sentence; the cells go down.

### How much each item earns

Altitude is graduated. An item earns a paragraph only when it is:
- **non-obvious** — the reader can't reconstruct it from its label (an unfamiliar procedure needs its flow spelled out, while a self-explanatory category name collapses to the bare label);
- **self-arguing** — it carries a rationale that pre-empts the reader's likely objection; or
- **decision-bearing** — it embeds a choice or policy the reader must approve.

Routine, self-describing, decision-free items collapse to a label + gloss. When an item is one of many interchangeable instances (a question, a case, a checklist row), the gloss encodes the *discriminating point* — what a good instance turns on — not the instance itself.

The 提綱 may also **synthesize what the sources only imply**: name a structure the sources leave implicit, compute a total they leave split (a sum the reader would otherwise add up), add a concrete tag that makes an abstract claim legible. Two cautions: every synthesized load-bearing number must still trace to a source, and recutting a source's own structure (its N buckets regrouped into your M) risks a visible mismatch — do it consciously.

## House style

- Traditional Chinese, Taiwan corporate / financial-institution register. Declarative and compressed; one idea per sentence.
- **Purpose-first framing** on each section and bullet cluster: open with a label that names the intent, then the content — 「目的：…」「要驗證：…」「成果：…」 or whatever fits the material. The sentence-level lowering to a non-technical reader is `plain-speak`'s job (step 4) — don't re-teach it here.
- **Flat over nested.** Render multi-item essence as flat, purpose-labeled bullet clusters — not nested 槽狀 paragraphs or interwoven A-vs-B comparison prose. Flatness keeps the 提綱 scannable and lets a source change touch one bullet instead of unpicking a clause.
- Cross-reference format 「（詳《檔名》）」, pointing **down** to detail docs only — never to the umbrella overview (that would be circular).
- Tables for governance/structure — 階段／數量、組成、角色分工. Flat bullets for enumerable essence. Prose for the opening one-or-two-sentence essence.
- Truncate long enumerations to anchor items + 「等」.
- Top-level sections numbered 一、二、三; keep numbering stable across edits so references hold.
- No emoji. Strip AI-isms (the `avoid-ai-writing-zh` pass in step 6 handles this).

## Verification

Before declaring a 提綱 done, run every gate. Each is pass/fail; a fail sends you back to the named step. Verify by inspecting the draft against the sources, not from memory of what you intended.

- **Coverage** (step 3) — every source maps to exactly one section; the umbrella lent the spine and is *not* pointed to. Any orphaned or double-covered source fails.
- **MECE** (step 3) — no fact lives in two sections, and no section needs a back-reference to another to be understood.
- **Governance placement** (step 3) — any oversight/governing section sits beside the phase it governs, not after phases it doesn't touch.
- **Altitude** (step 5) — scan for below-altitude leakage (逐項配分、逐條標準、SOP、逐步操作、原始碼／設定／記錄檔、完整表格明細). Each hit is cut and pointed down, or the gate fails.
- **Earned depth** (step 5) — each item's room matches what it earns; no self-describing label padded, no non-obvious or decision-bearing item starved. A section deliberately more granular than its siblings says so.
- **Traceability** (step 4) — every claim and every load-bearing number, *including synthesized ones* (computed totals, regrouped structures), traces to a source. A load-bearing number with no anchor fails.
- **Pointer coverage** (step 4) — cross-reference density tracks detail density: the heaviest sections each carry a 「（詳《source》）」, not just the light ones.
- **Voice & shape** (steps 4, 6) — purpose-first labels present; essence is flat bullet clusters, not nested 槽狀 prose; retained sentences pass `plain-speak`'s repeat-test; `avoid-ai-writing-zh` has run.

## Worked example

For these moves applied end-to-end to a real 7-document set — with before/after snippets — see `references/example.md`. Load it only when you want to see the rules in action; skip it on a routine run.

# Formal Internal Doc Structure

This skill turns a rough ask into a ready-to-circulate internal business document in Taiwan corporate Traditional Chinese — an approval memo (簽呈), a meeting record, an assessment report, a project plan, or a vendor communication — with the structure its reader actually needs to decide, approve, or act. Manual trigger only — invoke it by name rather than expecting it to fire automatically.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a formal-doc-structure -y
```

Update later with:

```
npx skills update formal-doc-structure
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/formal-doc-structure/SKILL.md)

## What it does

It maps the request onto one of five document types by what the reader must do with it, then drafts the matching structure rather than forcing every request into one project-plan shape:

- **Sign off / approve** (簽呈, 採購, 預算) — 主旨、背景、現況與需求、方案、風險與控管、經費或資源需求、預期效益、擬辦事項.
- **Compare options / assess risk** (評估報告) — 評估目的、範圍、基準、現況與資料來源、分析結果、風險與限制、建議方案、後續追蹤.
- **Record what was decided** (會議紀錄) — 會議資訊、目的、討論重點、決議事項、待辦事項、風險或待確認、下次追蹤.
- **Execute a plan** (專案規劃, 訓練, 流程) — 文件定位、執行模式、角色與分工、時程、工作內容、交付物與驗收、風險與控管、後續維運.
- **Coordinate with a vendor** (廠商溝通) — 背景、本方立場或需求、請對方確認事項、需提供資料、時程或回覆方式、後續聯繫窗口.

Beyond picking the right skeleton, it groups related chapters instead of scattering them (背景+現況, 範圍+假設, 風險+控管), opens heavy sections with a summary sentence before the detail, forces a named owner, timeframe, deliverable, and acceptance method onto every activity, and runs a 10-point revision checklist before final output.

The output is a paste-ready draft with real sections filled in, not an outline or a critique of the request.

## When to use

Reach for it to write or fix an internal business document in Taiwan corporate Traditional Chinese: an approval memo, a meeting record, an assessment report, a project plan, or a vendor communication.

## When not to

Not for RFPs or bidding specs (use `rfp-writing`) — those are documents sent out for bidding, with conventions that conflict with an internal document's. Not for pure language cleanup with no restructuring (use `humanizer-zh`) — reach for this skill only when the job also involves organizing the document by type. Not for blog posts, marketing copy, or casual writing.

## How it works

The one decision that shapes everything downstream is picking the template from the reader's need, not the document's name. A request for a "報告" could still need the 決策文件 template (Template A) if what the reader actually has to do is approve funding — the label on the request doesn't dictate the structure, the reader's action does.

Once the template is picked, every section gets held to the same bar: a sentence survives only if it adds a decision, requirement, constraint, risk, responsibility, deliverable, timeline, or verification method — abstract conclusions and filler get cut. For an approval memo, that means the 擬辦事項 line at the end can't just restate the problem; it has to name what will actually happen next:

> Poor: 需加強後續管理。
> Better: 後續由承辦單位每月彙整執行情形，內容包含進度、待辦事項、風險、需主管協調事項及預計完成時間。

The second mechanism is affirmative planning language over negative framing. A sentence like 不建議僅以會議討論作為結論，而是要形成後續追蹤項目 gets rewritten as a direct statement of what will happen: 會議結論需整理為後續追蹤項目，並列明負責單位、預計完成時間及檢核方式. The rewrite isn't cosmetic — naming the owner and the deadline is what makes the sentence something a reader can act on instead of just agree with.

## Related skills

- **rfp-writing** — use it instead for an RFP / 招標規格 / 需求規格書, a document sent out for bidding with its own structural rules that conflict with this skill's.
- **humanizer-zh** — use it instead (or as this skill's optional finishing pass) when the job is only removing AI-writing patterns from an already-structured draft, with no reorganizing needed.

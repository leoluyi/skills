---
name: visual-output-qa
description: >-
  Review rendered visual artifacts against one shared delivery standard.
  Use after producing or materially editing SVG, browser-rendered HTML, exported graphics, PPTX, PDF, or other fixed-layout visual output, and when the user asks to 檢查爆版、裁切、碰撞、字型、缺字、對比或交付品質.
  Do not invoke for choosing a visual style, writing slide content, or reviewing prose without a rendered artifact.
license: MIT
metadata:
  author: Lu Yi
  tags: visual qa svg html pptx pdf rendering accessibility
  agentskills_spec: "1.0"
  openclaw:
    emoji: "🔎"
---

# Visual Output QA

Act as the last reader before delivery.
Judge rendered truth, not source intent.

This skill is a review protocol and shared rule vocabulary.
It does not provide a renderer or replace format-specific construction checks.
Use it to produce an evidence-backed verdict after the artifact has been rendered.

## Applicability

Use the profile that matches the recipient's delivery path:

| Artifact branch | Required evidence |
|---|---|
| SVG or browser HTML | Final browser viewport and computed styles |
| Exported SVG, PNG, or PDF | The pinned export renderer and its output |
| PPTX | The renderer the recipient will use; LibreOffice is only a declared approximation |
| Source without a rendered artifact | No delivery verdict; return `INCOMPLETE` |

Record the profile and renderer in every report.

## Workflow

1. Identify the artifact, delivery format, final renderer, intended viewport or page size, and whether text must be preserved.
   Completion: every delivery condition that can change rendering is named or explicitly unknown.
2. Read [`references/design-principles.md`](references/design-principles.md) completely and apply every rule in the applicable profile.
   Record each rule as verified, failed, or not verifiable.
   Completion: every rule has one recorded state and every `N/A` has a reason.
3. Render through the same path the recipient will use, then inspect computed text, visible paint, clipping, font resolution, glyph coverage, stacking, and connector geometry.
   Completion: findings come from delivered appearance rather than source coordinates or declared styles alone.
4. Classify objective reader harm as hard failure and aesthetic judgment as advisory.
   When a hard condition cannot be verified, report incomplete verification instead of a pass.
   Completion: every finding has one status: hard failure, advisory, or incomplete verification.
5. Report the responsible-layer fix, then render again and repeat the full affected branch when the caller authorizes edits.
   Preserve content when the caller requires preservation; otherwise prefer cutting copy before shrinking type or distorting layout.
   Completion: every hard condition is verified and passes, with remaining advisories stated separately.

## Report

Return artifact and renderer, hard failures, incomplete checks, advisories, fixes made, and final verdict.
Include one evidence line for every rule ID and identify the inspected output.
Use only `PASS`, `FAIL`, or `INCOMPLETE` as the verdict.
`PASS` means every applicable hard condition was verified and passed.

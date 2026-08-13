# Visual Output Quality Design Principles

This document defines one delivery standard for SVG, browser-rendered HTML, exported graphics, PPTX, PDF, and other fixed-layout visual artifacts.
It defines how to judge quality without binding the standard to one checker or implementation language.

## Core idea: rendered truth

Delivery quality is determined by what the recipient actually sees, not by source code, declared styles, or author intent.
Source code can prove the input, but it cannot prove that substituted fonts still fit, CSS cascade still yields sufficient contrast, or arrowheads survive clipping and paint order.
Verify every renderer-dependent, font-dependent, viewport-dependent, export-dependent, or paint-order-dependent claim through the final delivery path.

## 1. Verify the delivery path, not an ideal environment

Fix the final format, renderer, viewport or page size, font set, and export settings before judging quality.
Browser SVG, exported SVG or PNG, a PPTX opened in LibreOffice, and a PPTX opened in Microsoft PowerPoint are distinct delivery profiles.
A pass in one profile cannot establish a pass in another.
When a required renderer, font, or parsing capability is unavailable, return `INCOMPLETE`, not `PASS` with a warning.

## 2. Extract one complete scene before applying rules

A format adapter faithfully extracts canvas bounds, visible geometry, pixel masks, z-order, clipping, glyph bounds, computed styles, resolved fonts, glyph coverage, icons, connectors, markers, and endpoint relationships.
A quality evaluator uses that scene to judge bounds, collisions, contrast, and legibility.
Adapters do not own thresholds, severity, or remediation order.
This separation gives every format the same quality semantics and prevents each parser from growing a different rule set.

## 3. Block only objective defects that harm readers

A hard failure must be independent of taste and cause lost content, misreading, or unreadability.
Visual preference, compositional taste, and maintainability still matter, but remain advisory.

The following defects are hard failures:

| Defect | Decision criterion |
|---|---|
| Invalid artifact | XML, HTML, PPTX, or another delivery format is damaged; references do not resolve; or duplicate IDs create uncertain behavior |
| Out of bounds | Visible, non-decorative shape, text, icon, marker, or connector paint extends beyond the canvas or slide |
| Text overflow or clipping | Rendered glyphs or line boxes extend beyond their owning container or are clipped |
| Font-substitution reflow | The actual fallback font changes line breaks, size, or position and causes overflow, clipping, or collision |
| Missing glyphs | The delivered artifact contains tofu, replacement glyphs, or unreadable characters |
| Connector-text collision | Visible connector stroke or marker paint intersects text paint |
| Icon-text collision | Visible icon paint intersects text paint |
| Insufficient connector clearance | A connector or marker crosses a non-endpoint object, or an endpoint's fill or border consumes the marker body |
| Insufficient actual text contrast | Computed foreground against the visible background beneath each glyph fails the applicable WCAG threshold |

Use these stable rule IDs in reports:

| Rule ID | Defect |
|---|---|
| `artifact.parse` | Invalid artifact, unresolved reference, or duplicate ID |
| `geometry.bounds` | Visible paint outside the canvas or slide |
| `geometry.text_fit` | Rendered text overflow or clipping |
| `font.substitution_reflow` | Font fallback changes layout or causes reader harm |
| `font.glyph_coverage` | Missing glyph or replacement glyph |
| `geometry.connector_text` | Connector or marker crosses text |
| `geometry.icon_text` | Icon paint crosses text |
| `geometry.connector_clearance` | Connector or marker lacks safe clearance |
| `contrast.text_actual` | Actual rendered text contrast fails |

The following findings are advisory:

- Font fallback occurs without reflow, missing glyphs, or collision.
- Elements come close without visible paint intersection.
- Connector routing is clear but aesthetically weak.
- Icon balance, whitespace, alignment, or hierarchy could improve.
- Palette, visual style, or grouping misses a preference without causing misreading.
- Source structure is difficult to restyle while the delivered artifact remains correct and legible.

Reader harm, not remediation cost, separates hard failures from advisories.

## 4. Judge collisions using visible paint

Bounding boxes are useful for quickly rejecting impossible intersections, but cannot prove a collision.
Hard failures involving connectors, markers, icons, or glyphs require visible paint masks or equivalent exact geometry.
Circles, curves, transparent regions, and hollow icons cannot be reduced to outer rectangles.
Legitimate endpoint contact may pass, but the marker body must remain fully visible outside endpoint fill and border.

## 5. Judge contrast using computed style and visible background

Resolve CSS cascade, inheritance, CSS variables, `currentColor`, opacity, and presentation attributes to determine text foreground.
Resolve paint order, transparency, gradients, and overlapping surfaces to determine the background actually visible beneath each glyph.
Palette tokens and source `fill` values support design work but cannot prove delivered-artifact contrast.
An unused palette token that never appears beneath visible text cannot change the artifact verdict.

## 6. Treat fonts as part of layout

Declaring `font-family` expresses a preference; it does not prove that the font loaded or covers every glyph.
Record the resolved font, substitution, glyph coverage, line boxes, and clipping.
Overflow caused by a wider fallback font is a layout failure, not a harmless environment difference.
Test environments should pin open-licensed narrow, wide, and CJK fonts instead of relying on incidental host inventory.

## 7. Let content policy change remediation order only

Use `preserve` when approved text and structure must remain unchanged.
Prefer wrapping, resizing containers, reflowing layout, rerouting connectors, or splitting the canvas.
Use `editable` for original content whose copy may change.
Prefer cutting copy before shrinking type or distorting layout.
Content policy never changes whether a defect exists or lowers a hard-failure threshold.

## 8. Fail closed when proof is unavailable

Unsupported transforms, clipping, filters, foreign objects, complex text shaping, marker geometry, or background composition make affected hard conditions unverifiable.
List the missing capability and affected rules, then return `INCOMPLETE`.
Manual inspection may add evidence, but uncertainty or irreproducibility cannot become an automatic pass.

## 9. Pair every defect regression

Each red fixture locks one expected stable rule ID.
Pair every red fixture with the nearest green fixture so legitimate construction remains accepted.
Use synthetic fixtures to isolate rules and historical artifacts to prevent checks that work only on authored test data.
Before promoting a check to a hard gate, prove both that it detects the defect and that it preserves existing valid artifacts.

## 10. Preserve one source of truth and one-way dependencies

Rule IDs, severity, thresholds, and remediation order have one authority.
Visual-producing skills retain only the pointer that says when to run QA plus their own format-construction knowledge.
Consumers do not copy shared rules, override thresholds, or retain an alternate fallback validator.
Consumers may retain format-specific construction checks, but those checks cannot issue the cross-format delivery verdict.
Shared QA sits at the bottom of the dependency graph and does not depend on or enumerate its consumers.

## 11. Define completion as a provable delivery state

`PASS` means every applicable hard condition was verified and passed in the named delivery profile.
`FAIL` means at least one objective defect was confirmed.
`INCOMPLETE` means at least one applicable hard condition could not be verified because required capability or environment was unavailable.
Advisories do not change the verdict and remain separate from hard findings.
After remediation, rerun the complete affected render and inspection path instead of checking only the changed source fragment.

# Visual Output QA Handoff

## Objective

Create one canonical visual-output quality gate for `~/.skills` that prevents objective low-level defects before delivery.

The gate must cover SVG, browser-rendered HTML, exported SVG, and PPTX.

The gate must hard-fail text overflow or clipping, shapes outside the canvas, connector-text collisions, icon-text collisions, marker or connector occlusion by cards, missing glyphs, font-substitution reflow, and actual text/background contrast failures.

The migration must remove parallel validator implementations rather than leaving several versions to drift.

## Current status

Investigation is complete.

No files under `~/.skills` have been changed yet.

The real artifact that exposed the current gaps is:

`/Users/leoluyi/Library/CloudStorage/Dropbox/Work/Yuanta/_李董/202601_AI微服務平台/assets/ai-agent-platform-mapping-v2-16x9.svg`

Three confirmed regressions from that artifact must become permanent fixtures:

- Font-dependent text overflow passed the source-width heuristic but failed under a wider fallback font.
- Marker arrowheads in 10px card gaps were visually consumed by adjacent card borders.
- Numbered stage badges declared `fill="#FFFFFF"` as a presentation attribute, but the global `text { fill: #0B162C }` stylesheet rule won the cascade, so the computed text colour remained dark and became hard to read on green and orange circles.

## Ranked root causes

### 1. Gates inspect simplified source geometry instead of rendered output

`skills/infographic-design/scripts/check.py:96-125` validates text anchor coordinates rather than rendered text extents.

`skills/infographic-design/scripts/check_text_fit.py:66-76,93-172` understands rectangles and simple translation, checks mainly right-edge overflow, and skips scale, rotate, matrix, and skew.

`skills/diagram-style/scripts/check_fit.py:65-105,158-199` supports only rectangles and one simple `translate()`.

Neither implementation analyzes connectors, markers, icons, paint order, clipping, or object intersections.

### 2. Two independent text-layout engines drift

`skills/diagram-style/scripts/check_fit.py:34-36` estimates CJK as `1.0em` and Latin as `0.55em`.

`skills/infographic-design/scripts/check_text_fit.py:17-57` maintains a separate Helvetica width table and bold multiplier.

These two estimators cannot prove layout under the font and renderer used for final export.

### 3. Font substitution is advisory even when it changes layout

`skills/infographic-design/scripts/check_text_fit.py:17-21` explicitly describes its metrics as a stand-in.

`skills/infographic-design/scripts/check.py:343-348` treats missing font-family as advisory.

`skills/infographic-design/references/svg-construction.md:40-71` and `skills/diagram-style/references/render-svg.md:187-200` acknowledge that export renderers substitute fonts or lose CJK glyphs.

Fallback-dependent overflow can therefore pass the current gates.

### 4. Actual foreground and background are not resolved reliably

`skills/infographic-design/scripts/check.py:170-210` reduces circles and ellipses to bounding rectangles, ignores paint order, and selects the smallest bounding box.

`skills/infographic-design/scripts/check.py:214-240` resolves only direct attributes and simple classes, not complete inherited computed style.

Palette derivation is useful for design tokens but cannot prove contrast in the delivered artifact.

### 5. Some output branches have no geometry gate

`skills/infographic-design/references/svg-construction.md:188-193` says the Python gate cannot check HTML.

`skills/diagram-style/SKILL.md:188-197` invokes an SVG-only checker despite supporting PPTX.

`skills/diagram-style/references/render-pptx.md:96-121` validates package structure and content preservation but not rendered geometry.

`skills/knowledge-doc-writing/references/html.md:5-9,82-86` permits hand-authored inline SVG without a visual gate.

### 6. Objective defects remain prose

Overlap and clipping rules exist in `skills/diagram-style/references/canvas-design-system.md:20-25,75`.

Non-crossing leader-line rules exist in `skills/infographic-design/references/layouts.md:69-70`.

These are not checkable completion criteria and therefore allow premature completion.

## Canonical architecture

Create one leaf skill:

```text
skills/visual-output-qa/
```

Each format adapter must produce one canonical rendered scene graph containing canvas bounds, painted geometry, pixel masks, z-order, clipping, rendered text glyph bounds, computed styles, resolved fonts, glyph coverage, objects, icons, connectors, markers, and endpoint relationships.

Adapters only extract and render.

They must not contain fit, collision, contrast, threshold, remediation, or severity logic.

One shared evaluator applies all rules to the scene graph.

`rules.py` is the sole source of truth for rule IDs, severity, thresholds, and remediation order.

Caller skills contain invocation pointers only.

## Stable CLI

```bash
<visual-output-qa-dir>/scripts/check.py check ARTIFACT \
  --profile svg-browser|svg-export|html-browser|pptx-libreoffice \
  --content-policy preserve|editable \
  --report-json REPORT.json
```

Additional commands:

```bash
check.py rules
check.py explain RULE_ID
```

Exit contract:

- Exit `0` means every hard rule was verified and passed.
- Exit `1` means an objective defect was found.
- Exit `2` means verification is incomplete because geometry is unsupported or a required renderer, font, or dependency is missing.

`--content-policy` changes remediation ordering only and never changes the verdict.

`preserve` prioritizes resizing, wrapping, rerouting, or splitting without changing text.

`editable` may cut copy before shrinking type or distorting layout.

Callers must not override thresholds or severity.

## Stable Python API

```python
from visual_qa import check, Profile, ContentPolicy

report = check(path, Profile.SVG_BROWSER, ContentPolicy.PRESERVE)
```

The report schema is `visual-output-qa/report/v1`.

## Files to add

```text
skills/visual-output-qa/SKILL.md
skills/visual-output-qa/agents/openai.yaml
skills/visual-output-qa/catalog.md
skills/visual-output-qa/references/contract.md
skills/visual-output-qa/scripts/check.py
skills/visual-output-qa/scripts/visual_qa/__init__.py
skills/visual-output-qa/scripts/visual_qa/model.py
skills/visual-output-qa/scripts/visual_qa/rules.py
skills/visual-output-qa/scripts/visual_qa/geometry.py
skills/visual-output-qa/scripts/visual_qa/fonts.py
skills/visual-output-qa/scripts/visual_qa/report.py
skills/visual-output-qa/scripts/visual_qa/adapters/svg_html.py
skills/visual-output-qa/scripts/visual_qa/adapters/pptx.py
skills/visual-output-qa/tests/test_cli.py
skills/visual-output-qa/tests/test_bounds.py
skills/visual-output-qa/tests/test_text_fit.py
skills/visual-output-qa/tests/test_collisions.py
skills/visual-output-qa/tests/test_connector_clearance.py
skills/visual-output-qa/tests/test_actual_text_contrast.py
skills/visual-output-qa/tests/test_fonts.py
skills/visual-output-qa/tests/fixtures/red/
skills/visual-output-qa/tests/fixtures/green/
skills/visual-output-qa/tests/fixtures/real/
skills/visual-output-qa/evals/evals.json
skills/visual-output-qa/evals/trigger-queries.json
tools/check-visual-qa-ownership
.github/workflows/visual-output-qa.yml
```

Add threshold-free consumer declarations:

```text
skills/diagram-style/evals/visual-output-qa.json
skills/infographic-design/evals/visual-output-qa.json
skills/knowledge-doc-writing/evals/visual-output-qa.json
skills/briefing-outline/evals/visual-output-qa.json
```

## Files to delete in the same migration

```text
skills/diagram-style/scripts/check_fit.py
skills/infographic-design/scripts/check.py
skills/infographic-design/scripts/check_text_fit.py
skills/infographic-design/scripts/check_contrast.py
```

Keep `skills/diagram-style/scripts/derive.py` because it derives palettes, but never accept its output as delivered-artifact proof.

Do not keep compatibility shims unless known external callers require them.

If required, allow zero-logic forwarding wrappers for one release or 30 days and enforce the removal date in CI.

## Caller material to reduce to pointers

Update these diagram-style locations:

```text
skills/diagram-style/SKILL.md:42-44,112,188-197
skills/diagram-style/references/typography.md:20-40,56-126
skills/diagram-style/references/render-svg.md:155-200
skills/diagram-style/references/render-pptx.md:96-121
skills/diagram-style/references/canvas-design-system.md:20-25,75
skills/diagram-style/maintenance/checks.md:25-34
skills/diagram-style/maintenance/constants.md:49-62,119-127
skills/diagram-style/catalog.md
```

Update these infographic-design locations:

```text
skills/infographic-design/SKILL.md:257-283
skills/infographic-design/references/svg-construction.md:21-71,123-137,188-193,248-258
skills/infographic-design/references/color-typography.md:111-117
skills/infographic-design/references/layouts.md:69-70
skills/infographic-design/guide.en.md:51-54
skills/infographic-design/guide.zh.md:51-54
skills/infographic-design/design-notes.md:168-182
skills/infographic-design/catalog.md
```

Update these other visual producers:

```text
skills/knowledge-doc-writing/SKILL.md:125-127
skills/knowledge-doc-writing/references/html.md:5-9,82-86
skills/knowledge-doc-writing/design-notes.md:65-72
skills/briefing-outline/SKILL.md:42-46
engineering-guidelines.md:135-153
```

Do not attach this gate to `deck-writer` because it stops before rendering.

Do not attach it to `deck-consulting` because that skill diagnoses rather than produces presentation files.

## Hard rules

| Rule ID | Hard-fail condition |
|---|---|
| `artifact.parse` | Invalid XML, HTML, PPTX, unresolved references, or duplicate IDs |
| `geometry.bounds` | Visible non-decorative shape, text, icon, marker, or connector outside the canvas or slide |
| `geometry.text_fit` | Rendered glyph or line bounds are clipped or outside the owning container |
| `font.substitution_reflow` | The actual substituted font changes line breaks or causes overflow or clipping |
| `font.glyph_coverage` | Missing glyphs or tofu are rendered |
| `geometry.connector_text` | A visible connector stroke crosses text |
| `geometry.icon_text` | Visible icon paint collides with text paint |
| `geometry.connector_clearance` | A connector or marker overlaps a non-endpoint object, a marker body is consumed by endpoint borders, or the free corridor cannot contain the rendered marker geometry |
| `contrast.text_actual` | Actual computed text foreground against the visible background fails WCAG |

`contrast.text_actual` must resolve inherited style, CSS variables, `currentColor`, opacity, gradients, paint order, and the visible background below each glyph.

Palette-only contrast does not prove the delivered artifact.

`geometry.connector_clearance` must resolve `markerUnits`, `viewBox`, `refX`, `refY`, orientation, transforms, border outsets, and paint-order occlusion.

A marker tip may touch its endpoint boundary, but its body must remain visible outside endpoint fill and border.

Unsupported geometry or unavailable renderers must return exit `2` and must never become advisory green.

## Advisory checks

- Font fallback that causes no reflow or glyph loss.
- Near but non-overlapping clearances.
- Connector aesthetics after clearance passes.
- Optical icon balance.
- Palette taste, whitespace, hierarchy, and alignment.
- Semantic grouping and restyle maintainability.

## Required regression fixtures

Every red fixture must exit `1` with one expected stable rule ID.

Every paired green fixture must exit `0`.

```text
real/red/font-fallback-overflow.svg
green/explicit-font-or-widened-container.svg

real/red/connector-crosses-label.svg
green/connector-routed-around-label.svg
green/connector-label-with-opaque-backing.svg

real/red/icon-text-collision.svg
green/icon-text-separated.svg

real/red/horizontal-cards-10px-marker-occluded.svg
green/horizontal-cards-centered-chevron.svg
green/horizontal-cards-adequate-marker-gap.svg

red/shape-outside-canvas.svg
green/shape-inside-canvas.svg

red/nested-transform-outside-canvas.svg
green/nested-transform-inside-canvas.svg

real/red/numbered-stage-badges-inherited-dark-text.svg
red/inherited-dark-text-green-circle.svg
red/inherited-dark-text-orange-circle.svg
green/explicit-white-text-dark-green-circle.svg
green/explicit-white-text-dark-orange-circle.svg
```

Equivalent PPTX fixtures must cover text overflow, bounds, connector crossing, marker clearance, icon collision, and font substitution.

## Regression assertions

- The font fallback red fixture passes parse and source-text checks but fails after actual font resolution.
- Connector-text and icon-text red fixtures fail from rendered intersections rather than estimated bounding boxes.
- The 10px marker fixture passes parse, reference, text-fit, contrast, and canvas checks but fails `geometry.connector_clearance`.
- Legitimate endpoint contact with a fully visible marker passes.
- Badge fixtures resolve inherited foreground and the actual circle background before checking contrast.
- A badge fixture with `fill="#FFFFFF"` presentation attributes and a conflicting global `text { fill: ... }` rule must fail using the computed CSS colour rather than the apparent source attribute.
- Changing unused palette tokens cannot affect artifact contrast verdicts.
- Removing explicit white text from a green badge makes it red.
- Complex or unsupported geometry returns exit `2`.
- Existing historical passing artifacts remain green to protect against false-positive promotion.

## Atomic migration sequence

1. Freeze current accepted artifacts and all reported defects as fixtures.
2. Add the canonical scene graph, adapters, rule registry, CLI, and tests.
3. Prove every red fixture fails for its expected rule and every green or historical pass fixture passes.
4. Switch every SVG, HTML, and PPTX producer branch to the canonical CLI.
5. Delete all four old validator files in the same change.
6. Remove duplicated algorithms, thresholds, and gate descriptions from callers and replace them with pointers to the canonical contract.
7. Add `tools/check-visual-qa-ownership --all` and CI.
8. Run each changed skill's release gate against the pre-extraction revision as baseline.

## Ownership CI

`tools/check-visual-qa-ownership --all` must fail when:

- An obsolete validator file reappears.
- Artifact-validation functions such as `text_width`, `canvas_gate`, `contrast_gate`, `bg_at`, or `container_of` appear outside `visual-output-qa`.
- A hard rule ID is declared outside canonical `rules.py`.
- A visual-producing branch lacks a consumer declaration or canonical invocation.
- A caller contains local thresholds or severity overrides.
- Any canonical red, green, or historical artifact regression changes verdict unexpectedly.

## Dependencies and portability

- Use Chromium for SVG and HTML computed styles, font resolution, DOM geometry, clipping, and rendered-pixel masks.
- Use one pinned SVG export renderer for `svg-export` and verify with the same renderer used for final export.
- Use LibreOffice plus OOXML relationships for PPTX and report that LibreOffice is not perfectly equivalent to Microsoft PowerPoint.
- Bundle open-licensed narrow, wide, and CJK test fonts.
- Install pinned Noto fonts in CI and never depend on host font inventory.
- Probe Chromium, the SVG renderer, LibreOffice, fontconfig, and required fonts before checking.
- Missing requirements must return exit `2`.
- Runtime must not require network access.
- Use one canonical annotation contract only where native SVG or PPTX semantics cannot express roles or endpoint relationships.
- Install `visual-output-qa` with every declared consumer.
- Consumers must not vendor alternate validator implementations as fallback.

## Next-session prompt

```text
Read ~/.skills/research/visual-output-qa-handoff.md and continue the shared visual QA gate implementation.
Use $writing-great-skills, $skill-creator, and $writing-for-agents.
Treat ~/.skills as the single source of truth and follow its AGENTS.md and engineering-guidelines.md.
Implement the atomic migration without leaving parallel validators.
Start by converting the three real defects from ai-agent-platform-mapping-v2-16x9.svg into red fixtures, then build the canonical gate until each paired green fixture passes.
Do not re-run the completed investigation.
Before completion, delete the four obsolete validators, run ownership CI, run unit fixtures, run tools/eval validate --all, and report anything that could not be verified.
```

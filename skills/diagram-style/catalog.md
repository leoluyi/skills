---
emoji: "🧭"
category: docs-design
order: 2
languages: [zh-TW, en]
tags: [diagram, svg, pptx, architecture-diagram, flowchart, visual-style, traditional-chinese]
title:
  en: "Diagram Style"
  zh: "架構圖設計與重繪"
tagline:
  en: "Generate a new diagram from requirements or restyle an existing one while preserving requested content"
  zh: "從需求建立新圖，或保留指定內容重新設計既有架構圖與流程圖"
whenUse:
  en: "Use it to create an architecture or flow diagram from a topic or requirements, or when an existing SVG, PPTX, Mermaid source, or image needs a new visual treatment."
  zh: "從主題或需求建立架構圖、流程圖，或替既有 SVG、PPTX、Mermaid 原碼與圖片換視覺風格時使用。"
whenNot:
  en: "Do not infer unsupported system facts, or silently change content that the user asked an edit to preserve."
  zh: "不要捏造需求未提供的系統事實，也不要在 edit 模式默默修改使用者要求保留的內容。"
highlights:
  en:
    - "Classifies each request as generate or edit based on how supplied images are meant to be used"
    - "Uses a canvas design system for deliberate visual philosophy, composition, rhythm, hierarchy, and refinement"
    - "Separates role, pen, colour, structure, and media so one layer can change without silently changing another"
    - "Preserves source text, node counts, connections, and groups through explicit reconciliation"
    - "Uses derived colour gates for contrast, grayscale separation, print safety, and category limits"
    - "Handles SVG and PPTX rendering with fit checks that resize layout instead of truncating labels"
  zh:
    - "依圖片用途判定 generate 或 edit，不以是否有附件作為唯一依據"
    - "以 canvas design system 約束視覺哲學、構圖、節奏、層級與精修"
    - "分開角色、筆調、顏色、結構與媒材，換一層不默默改動其他層"
    - "用明確核對保留素材文字、節點數、連線與群組"
    - "以推導出的顏色閘門檢查對比、灰階區隔、列印安全與類別上限"
    - "支援 SVG 與 PPTX，文字塞不下時調整版面而不截斷標籤"
---

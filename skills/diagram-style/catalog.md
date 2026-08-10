---
emoji: "🧭"
category: docs-design
order: 2
languages: [zh-TW, en]
tags: [diagram, svg, pptx, architecture-diagram, flowchart, visual-style, traditional-chinese]
title:
  en: "Diagram Style"
  zh: "架構圖重繪"
tagline:
  en: "Restyle an existing architecture or flow diagram while preserving its nodes, connections, groups, and text"
  zh: "保留既有架構圖或流程圖的節點、連線、群組與文字，只重新套用筆調、配色與媒材格式"
whenUse:
  en: "Use it when an existing SVG, PPTX, Mermaid source, or node-and-relationship list needs a new visual style or a consistent treatment across diagrams."
  zh: "當既有 SVG、PPTX、Mermaid 原碼或節點關係條列需要換筆調、配色，或多張圖需要統一外觀時使用。"
whenNot:
  en: "Do not use it to invent diagram content from a topic alone or to change the source structure without the missing relationships."
  zh: "不要用於只給主題就從零製圖，也不要在缺少對照關係時自行改寫素材結構。"
highlights:
  en:
    - "Separates role, pen, colour, structure, and media so one layer can change without silently changing another"
    - "Preserves source text, node counts, connections, and groups through explicit reconciliation"
    - "Uses derived colour gates for contrast, grayscale separation, print safety, and category limits"
    - "Handles SVG and PPTX rendering with fit checks that resize layout instead of truncating labels"
  zh:
    - "分開角色、筆調、顏色、結構與媒材，換一層不默默改動其他層"
    - "用明確核對保留素材文字、節點數、連線與群組"
    - "以推導出的顏色閘門檢查對比、灰階區隔、列印安全與類別上限"
    - "支援 SVG 與 PPTX，文字塞不下時調整版面而不截斷標籤"
---

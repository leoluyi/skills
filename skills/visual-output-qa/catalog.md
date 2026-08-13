---
emoji: "🔎"
category: docs-design
order: 3
languages: [zh-TW, en]
tags: [visual-qa, svg, html, pptx, pdf, accessibility, rendering]
title:
  en: "Visual Output QA"
  zh: "視覺輸出品質檢查"
tagline:
  en: "Review rendered visual artifacts against one fail-closed delivery standard"
  zh: "以單一且無法驗證就不放行的標準，檢查視覺成品的實際呈現"
whenUse:
  en: "Use after producing or materially editing rendered SVG, HTML, exported graphics, PPTX, PDF, or other fixed-layout visual output."
  zh: "產出或大幅修改 SVG、HTML、匯出圖檔、PPTX、PDF 等固定版面視覺成品後使用。"
whenNot:
  en: "Not for choosing a visual style, writing slide content, or reviewing prose without a rendered artifact."
  zh: "不要用於選擇視覺風格、撰寫投影片內容，或檢查尚未產生實際成品的純文字。"
highlights:
  en:
    - "Treats rendered output as truth instead of trusting source geometry or declared styles"
    - "Separates objective reader-harming failures from advisory design judgment"
    - "Returns INCOMPLETE when a renderer, font, or geometry capability is missing"
    - "Covers clipping, bounds, font reflow, missing glyphs, collisions, connector clearance, and actual contrast"
  zh:
    - "以實際呈現為準，不直接相信原始幾何或宣告樣式"
    - "分開會傷害讀者的客觀失敗與建議性設計判斷"
    - "缺少 renderer、字型或幾何能力時回傳 INCOMPLETE"
    - "涵蓋裁切、邊界、字型 reflow、缺字、碰撞、連線淨空與實際對比"
---

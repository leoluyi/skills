---
emoji: "🧭"
category: agent-workflow
order: 7
languages: [en, zh-TW]
tags: [agent-workflow, technical-specification, sample-code, requirements-interview, tdd]
title:
  en: "Developer Spec Workflow"
  zh: "開發者技術規格工作流"
tagline:
  en: "Take a rough brief through documented grilling to one developer spec, one runnable sample, and end-to-end proof"
  zh: "把初始需求逐題問清楚，收斂成一份開發者技術規格、一套可執行 sample 與 end-to-end 證據"
whenUse:
  en: "Use when a project needs the full path from ambiguous initial prompt through durable decisions, a developer-facing technical specification, runnable sample code, and reproducible verification."
  zh: "當專案要從模糊的初始 prompt 開始，經過可追溯的決策訪談，完成開發者技術規格、可執行 sample code 與可重現驗證時使用。"
whenNot:
  en: "Not for a writing-only knowledge document, implementation from an approved spec, an RFP or procurement spec, a bug fix, or a one-off code example."
  zh: "不要用於只有文件的知識整理、依核准規格直接實作、RFP 或採購規格、bug fix，或一次性的 code example。"
highlights:
  en:
    - "Preserves the raw brief while confirmed decisions, assumptions, and open questions evolve in a separate context record"
    - "Grills one architecture-changing decision at a time and persists each answer before context can decay"
    - "Keeps one specification of record and treats the runnable sample as the source for code behavior"
    - "Ships vertical tracer bullets with happy-path, negative-path, and clean-checkout evidence"
  zh:
    - "原始 brief 保持不動，已確認決策、暫定假設與未決問題在獨立 context 持續演進"
    - "一次只追問一個會改變架構的決策，並在 context 衰退前把答案寫回 repo"
    - "只維護一份正式規格，code 行為以實際可執行 sample 為準"
    - "以垂直 tracer bullet 交付 happy path、negative path 與 clean checkout 證據"
---

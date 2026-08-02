---
emoji: "🔬"
category: agent-workflow
order: 6
languages: [en, zh-TW]
tags: [taste, rubric, evaluation, writing-quality, interview, claude-code]
title:
  en: "Taste Distiller"
  zh: "品味蒸餾"
tagline:
  en: "Mine your rejections of AI output and distil the standard behind them into a reusable 1-5 rubric, in Markdown and in JSON for an evaluator agent"
  zh: "從你退掉、重寫 AI 產出的實例裡挖出背後的標準，蒸餾成可重複使用的 1-5 分 rubric，同時給 Markdown 和 evaluator 用的 JSON"
whenUse:
  en: "Reach for it when you keep rewriting AI output the same way and want the standard written down — as custom instructions, as an evaluator's grading prompt, or as team-visible documentation."
  zh: "當你一再用同樣的方式重寫 AI 產出、想把那套標準寫下來時使用——可以當自訂指令、evaluator 的評分 prompt，或團隊可見的文件。"
whenNot:
  en: "Not for generating content in your style, not for cleaning AI-isms out of one specific draft, and not for defining what an agent run should achieve."
  zh: "不要用它模仿你的風格產出內容、不要用來清理某一份稿子的 AI 味，也不要用來定義一輪 agent 執行的目標。"
highlights:
  en:
    - "Runs as rejection-grade-explain cycles over three to five real moments you rewrote something, in your own words"
    - "Refuses \"it felt off\" and \"太 AI 味\" — it pushes for the specific word, sentence or structural choice that triggered the reaction"
    - "Every rubric line is traceable to a rejection you described; no invented preferences"
    - "Tiers describe observable behaviour, not quality adjectives — tier 3 is the floor of shippable, tier 5 is the bar"
    - "Ships both formats: Markdown you review and refine, JSON an evaluator agent grades against"
  zh:
    - "以「退稿—評分—解釋」的循環進行，挖三到五個你真的動手重寫過的實例，用你自己的話"
    - "拒絕「感覺怪怪的」和「太 AI 味」——一定追問到是哪個字、哪個句子、哪個結構選擇引發的反應"
    - "每一條 rubric 都能追回到你描述過的某次退稿，不會憑空生出偏好"
    - "各級寫的是可觀察的行為而不是品質形容詞——第 3 級是可出貨的底線，第 5 級才是標準"
    - "兩種格式一起產出：Markdown 給你審閱調整，JSON 給 evaluator agent 評分用"
---

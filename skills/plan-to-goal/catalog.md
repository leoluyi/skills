---
emoji: "🎯"
category: agent-workflow
order: 1
languages: [en, zh-TW]
tags: [agent-workflow, planning, autonomous-execution, goal-setting, verification, claude-code]
title:
  en: "Plan → Goal"
  zh: "計畫轉 Goal"
tagline:
  en: "Turn a rough plan into a bounded goal with machine-checkable done conditions, before an autonomous run burns tokens on a vague target"
  zh: "在 agent 自己跑起來之前，把粗略的計畫變成有邊界、完成條件機器可驗的 goal，別讓它對著模糊目標燒 token"
whenUse:
  en: "Reach for it when you have a plan — from plan mode or written by hand — and want an agent to execute it unattended without drifting or stopping early."
  zh: "當你手上已有計畫（plan mode 產出或自己寫的），想讓 agent 無人值守跑完、又不要它中途偏掉或提早收工時使用。"
whenNot:
  en: "Not for writing a plan from scratch (that's plan mode itself), and not for a task small enough that one prompt would do — a goal spec is overhead for a one-line typo."
  zh: "不要用於從零規劃（那是 plan mode 的事），也不要用在一個 prompt 就能解決的小任務——為了一行 typo 寫 goal 規格是多餘的。"
highlights:
  en:
    - "Two-phase gate: the review is produced and confirmed before any goal exists, so a wrong assumption costs a sentence instead of a whole run"
    - "Completion conditions must be commands (tests, typecheck, a search returning nothing) — adjectives never enter the goal"
    - "Asks only about holes the code can't settle; forks resolved during exploration are stated for confirmation, not re-asked"
    - "Carries do-not constraints forward verbatim and always sets a stop limit, the stop-loss against an unreachable condition"
    - "Scope discipline at the gate: extras the model proposed stay outside the goal as separate follow-ups"
  zh:
    - "兩階段閘門：先產出審視、使用者確認後才有 goal，猜錯的代價是一句話而不是一整輪自動執行"
    - "完成條件必須是可執行的指令（測試、typecheck、搜尋無結果），形容詞不准進 goal"
    - "只問程式碼問不出答案的分歧；探索過程已解決的部分改成「說明後請你確認」，不重複打擾"
    - "把「不要動」的限制原樣帶進 goal，並一定設停損的回合上限，避免條件不可達時空轉"
    - "閘門處守住範圍：模型自己想到的加碼另列為後續事項，不偷偷塞進 goal"
---

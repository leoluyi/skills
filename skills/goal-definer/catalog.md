---
emoji: "🎯"
category: agent-workflow
order: 2
languages: [en, zh-TW]
tags: [agent-workflow, goal-setting, verification, autonomous-execution, interview, claude-code]
title:
  en: "Goal Definer"
  zh: "任務目標訪談"
tagline:
  en: "Interview a fuzzy task into a six-element goal prompt an agent can run for hours without drifting or wrapping up early"
  zh: "把講不清楚的任務訪談成六元素 goal prompt，讓 agent 自己跑好幾個小時也不偏離、不提早收工"
whenUse:
  en: "Reach for it when you have a long-running task but no plan yet, and the task is still phrased in words like \"optimize\", \"tidy up\" or \"rewrite\" that an agent could declare done at any moment."
  zh: "當你有個要跑很久的任務、但還沒有計畫，而且任務還停在「優化」「整理」「重寫」這種 agent 隨時可以宣稱做完的講法時使用。"
whenNot:
  en: "Not when you already have a written plan and want it turned into a goal — that's Plan → Goal. Not for writing the plan itself, and not for a task one prompt would finish."
  zh: "不要用在已經有寫好的計畫、只想轉成 goal 的情況（那是 Plan → Goal）。也不要用來寫計畫本身，或一個 prompt 就能做完的小任務。"
highlights:
  en:
    - "Six elements, asked one at a time: Outcome, Verification, Constraints, Boundaries, Iteration Policy, Blocked Stop Condition — never as a form to fill in"
    - "Refuses \"better\", \"more polished\", \"higher quality\" and pushes until another agent could verify completion without you eyeballing it"
    - "Names where the original task was ambiguous, so you can see which phrase would have let an agent stop early"
    - "Flags any element you left vague instead of quietly writing a generic goal around it"
    - "When the task hinges on subjective quality, sends you to distil a taste rubric first rather than faking a machine check"
  zh:
    - "六個元素一次問一個：Outcome、Verification、Constraints、Boundaries、Iteration Policy、Blocked Stop Condition，不會丟一張表格叫你填"
    - "拒絕「更好」「更完整」「更有質感」，逼到另一個 agent 不用你盯著看也能驗證完成為止"
    - "指出原本任務哪裡模糊，讓你看見是哪個詞會讓 agent 提早收工"
    - "任何一格你講得含糊，它會明講出來，不會偷偷寫成一份泛泛的 goal"
    - "任務本質是主觀品質時，先請你把品味蒸餾成 rubric，而不是假裝有機器可驗的標準"
---

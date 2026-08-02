---
emoji: "🚀"
category: agent-workflow
order: 3
languages: [en, zh-TW]
tags: [agent-workflow, autonomous-execution, delegation, verification, shipping, claude-code]
title:
  en: "Autopilot"
  zh: "自動駕駛"
tagline:
  en: "Hand over the whole job: orchestrate subagents, self-repair on a budget, pass a verification gate, then commit, push and open a PR without checking back"
  zh: "整份工作交出去：以 subagent 為主力執行、故障自修有次數上限、過驗證閘門後 commit、push、開 PR，全程不回頭問"
whenUse:
  en: "Reach for it when a plan is already settled and you want it finished end to end, with every decision batched into one report at the end instead of interrupting you."
  zh: "當計畫已經定案、你要它從頭做到尾，所有決策集中在最後一次回報、不要中途打斷你時使用。"
whenNot:
  en: "Not while the approach is still open, not for exploratory work, and not when you want to see each step before it lands — it commits and pushes without asking."
  zh: "作法還沒定、探索性的工作、或你想逐步確認再落地時，都不要用——它不問就 commit 和 push。"
highlights:
  en:
    - "Invoke-only: it never fires on its own, because the run commits and pushes without confirmation"
    - "Orchestrator by default — subagents do the reading and the scoped edits, so a long run doesn't die of context exhaustion"
    - "Three attempts per blocker, each on a different hypothesis, and never routing around a failure by weakening the check that caught it"
    - "Verification gate before any commit: parallel review agents plus the repo's own checks, run in the main loop where you can audit them"
    - "Six-rule isolation ladder decides worktree versus branch-in-place once, before the tree stops being clean"
  zh:
    - "只能手動呼叫：它不會自己觸發，因為這一輪會不問就 commit 和 push"
    - "預設當協調者——讀檔和有界的修改交給 subagent，長時間執行才不會被 context 耗盡拖垮"
    - "每個卡點三次修復上限，每次必須換一個假設；絕不靠削弱抓到問題的檢查來繞過去"
    - "commit 前一定過驗證閘門：平行的 review agent 加上 repo 自己的檢查，而且在主迴圈跑給你稽核"
    - "六條規則的隔離階梯，在工作目錄還乾淨時就一次決定要用 worktree 還是原地開分支"
---

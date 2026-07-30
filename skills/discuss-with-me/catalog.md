---
emoji: "🧪"
category: knowledge-mgmt
order: 3
languages: [en, zh-TW]
tags: [thinking-partner, red-team, assumptions, decision-record, uncertainty, kill-criteria, pre-mortem]
title:
  en: "Discuss With Me"
  zh: "陪我想一想"
tagline:
  en: "Think through a question neither of you can answer yet — widen the options, label what's found vs guessed, attack the load-bearing assumptions, and leave a record that says what would overturn it"
  zh: "陪你想一個雙方都還沒有答案的問題：先展開選項，標出哪句是查到的、哪句是猜的，再拆掉承重假設，留下一份寫明「什麼會推翻它」的紀錄"
whenUse:
  en: "When the answer is unknown to both you and the model — an open design direction, a bet under real uncertainty, a thin-evidence diagnosis — or when a discussion has been converging and nobody has said what would make it wrong."
  zh: "當這個問題你跟模型都還沒有答案時使用：懸而未決的設計方向、真有不確定性的判斷、證據很薄的診斷；或討論已經越聊越有共識，卻沒人講得出什麼會推翻它。"
whenNot:
  en: "Not when you already have the answer and just need it written up (use knowledge-doc-writing or formal-doc-structure), not for a concept with a settled answer you haven't learned yet (use learn-loop), and not for factual lookups, debugging, or code review."
  zh: "不要用於：答案已經有了只是要寫成文件（用 knowledge-doc-writing 或 formal-doc-structure）、學一個已有標準答案的概念（用 learn-loop）、以及查事實、debug、code review。"
highlights:
  en:
    - "Widens to 5-20 options including ones cutting against the drift, then hands you the cut"
    - "Marks every load-bearing claim found / inferred / guessed inline, so a smooth paragraph can't launder a guess"
    - "Red-team pass gives each assumption a fails-if, cheapest evidence, kill criterion, and who would know"
    - "Verifies in a fresh context — subagent or new session, ideally another model family — never in the thread that built the conclusion"
    - "Writes an open-question record carrying killed options and the strongest case against, not a decision doc"
    - "Invoked bare mid-conversation, it makes the question out of the last answer — what that turn never argued for — and stops when the work you paused can move"
  zh:
    - "先展開 5–20 個選項，包含跟當下風向相反的，再交給你決定留哪些"
    - "每個承重句就地標 [已查證]／[推論]／[推測]，流暢的段落沒辦法把猜測洗成事實"
    - "紅隊回合逐條給出「什麼情況下不成立」「最便宜的驗證」「停損線」「誰會知道」"
    - "驗證一律換到乾淨脈絡：subagent 或新對話，最好換一個模型家族，不在原討論串裡自己驗自己"
    - "產出是「未定問題紀錄」：保留已排除的選項與反方最強論證，不是一份假裝確定的決策文件"
    - "對話中途直接呼叫、不帶問題，就從上一輪回答裡沒被論證的地方生出題目，討論到你停下的那件工作能往下走為止"
---

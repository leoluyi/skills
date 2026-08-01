---
emoji: "🧯"
category: data-recovery
order: 1
languages: [en]
tags: [recovery, cache, chromium, claude-desktop, data-loss, forensics]
title:
  en: "Recover a Deleted Claude Conversation"
  zh: "救回被刪除的 Claude 對話"
tagline:
  en: "Pull a deleted Claude Desktop/claude.ai conversation and its artifacts back out of the Chromium cache before it's evicted"
  zh: "在 Chromium 快取被清掉之前，把刪除的 Claude Desktop／claude.ai 對話與產出檔案救回來"
whenUse:
  en: "Invoke by name right after a conversation was accidentally deleted from Claude Desktop or claude.ai — manual trigger, run it immediately, it's a race against cache eviction."
  zh: "在 Claude Desktop 或 claude.ai 對話被誤刪後立刻手動呼叫 — 這是跟快取清除的賽跑，越快越好。"
whenNot:
  en: "Skip it for ordinary chat-history or export questions, or generic cache-clearing questions unrelated to recovering lost data."
  zh: "一般聊天紀錄／匯出問題，或與救資料無關的一般快取清理問題不要用。"
highlights:
  en:
    - "Freeze-then-snapshot ordering protects the cache from eviction before any exploration starts"
    - "Isolated uv venv for extraction — never touches system Python or other project environments"
    - "Uses ccl_chromium_cache specifically, since generic Chromium-cache parsers mis-decode the blockfile framing"
    - "Covers both the Desktop app cache and the claude.ai browser cache variant"
  zh:
    - "先凍結來源再備份快取，確保還沒開始探索就先保住快取"
    - "用隔離的 uv venv 做解壓縮，不碰系統 Python 或其他專案環境"
    - "指定用 ccl_chromium_cache 解析，因為一般 Chromium 快取解析器會解錯 blockfile 的封裝格式"
    - "同時涵蓋 Desktop App 快取與 claude.ai 瀏覽器快取兩種情境"
---

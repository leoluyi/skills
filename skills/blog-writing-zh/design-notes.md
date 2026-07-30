# blog-writing-zh — 開發紀錄與接續指南

給未來用 Claude Code 接續開發此 skill 的人（或 agent）。記錄它怎麼
長出來的、設計決策為何、還有哪些沒做完。

## 一句話定位

有人味的繁中部落格寫作 skill。核心信念：**AI 文「看得出是 AI」不是
因為殘留病句，而是缺少人味的正向特徵**（立場、親身經歷、自建比喻、
不均質節奏、思考痕跡）。本 skill 是「加法」——注入這些特徵；下游的
humanizer-zh 是「減法」——清機械化 AI 味。順序不可反。

## 開發歷程（怎麼長出來的）

依實際迭代順序，每步都是「使用者提需求 → 研究/實作 → 打包」：

1. **研究七個部落格**：知識倉鼠、保哥、高見龍、90s.pm、AI避坑情報員
   （中文）＋ Julia Evans、Simon Willison（英文標竿）。爬文拆解語感。
2. **八元素風格選單**（voice-axes.md）：把「風格」拆成可組合的八個
   元素（開場/人設濃度/比喻型態/節奏/結構/術語/收尾/標題），
   preset 是常用配方的快捷。
3. **兩層 preset**：第一層文章類型（選骨架）× 第二層風味（選口味），
   解耦「用途」與「聲音」。
4. **推薦引擎**（preset-guide.md）：關鍵洞察——決定文章類型的不是
   主題領域，而是「讀者讀完要做什麼 × 讀者與主題的關係」。
5. **技術描述三模式**（tech-writing.md）：操作型（保哥）/概念型
   （高見龍）/推演型（倉鼠），內容層，與風味正交。
6. **改寫雙模式**（rewrite-playbook.md）：忠實翻譯＋編者框架 vs
   敘事重構；含 Obsidian 筆記轉換專節（使用者的主要用例）。
7. **benchmark protocol**（evals/）：同題對照找盲點的方法論。
   用參考作者原文 → skill 寫同題 → 七維度對照 → 般化可搬的招 →
   patch。**這是本 skill 品質的主要來源**，跑了 7 輪。
8. **dual-draft**（dual-draft.md）：改造使用者的「跑兩遍截長補短」
   直覺——不用隨機（同質變體無料可截），改成同風味沿一條軸
   刻意分化再熔接。實測證實結構軸對論證類互補性最高。
9. **長度四檔位**：短打/標準/深文/工具書級，選單第三層。
10. **系列文**（series-planning.md）：產出後自動評估值不值得拆，
    值得才附大綱。不前置規劃、不每篇都問。
11. **pipeline 主動調用**：Step 5 從「提示使用者」升級為「主動載入
    並執行 humanizer-zh」，且用 detect-first 三步（先 detect
    拿清單 → blog-writing-zh 過濾 intentional voice → 只 rewrite
    未豁免項），實測證實最不會誤削聲音。
12. **第五正向特徵「思考痕跡」**（v0.14.0）：核心原則從四特徵擴為五。
    洞察——AI 文的破綻不只在殘留病句與均質節奏，還在「已經知道答案、
    只把打磨好的結論丟給讀者」的口吻；人味來自邊想邊寫、讓讀者看著
    你從困惑走到結論。此特徵與八元素正交、且 baseline always-on，
    故放核心原則（非 voice-axes 可選軸）。同步登記進 Step 5 的兩處
    intentional-voice 豁免清單，避免下游 humanizer-zh 把
    「我一開始以為…」「老實說不確定」當 hedging 削掉。改寫模式綁
    既有編者視角反捏造守則（不假造第一人稱困惑，改攤開素材推導順序）。

## 關鍵設計決策（為什麼這樣做）

- **風味檔分離**：每個作者一個 style-*.md，加新作者只加檔案，
  SKILL.md 不用大改。
- **內部光譜**：benchmark 發現多數風味不是均質的——情報員（釣魚反轉
  ↔時事吐槽）、Julia（打磨解惑↔live 探索）、Simon（年度回顧↔速覽）、
  倉鼠（輕實測↔硬解讀）都橫跨兩種子模式。風味檔都加了「光譜提醒」，
  選題後要先定位子模式。
- **雙篇對照 > 單篇**：單篇只給表面特徵，同作者不同類型的兩篇，
  交集才浮現骨架、差異才暴露光譜。protocol 已把此列為成熟門檻。
- **不捏造經歷**：觀點倡議型與實測筆記型的說服力核心是見證，
  索取真實素材是必要步驟；使用者說沒有時誠實降級，不虛構。
- **detect-first pipeline**：過濾權留在懂本文聲音的 blog-writing-zh
  手上，下游只執行確認過的修改。

## 已完成的 benchmark 覆蓋

七風味全部完成雙篇對照（見 evals/blog-writing-zh/benchmark-protocol.md
的 log）：高見龍（觀點＋教學）、保哥（排錯＋設定）、倉鼠（實測＋
解讀）、90s.pm（系列相鄰兩篇）、情報員（釣魚反轉＋時事吐槽）、
Julia（DNS 解惑＋gzip 探索）、Simon（年度回顧＋速覽）。

## 待辦 / 未做完（接續開發的起點）

- [ ] **跑 evals**：用 repo 的 run-eval 工具實際量測觸發準確率與
  輸出品質，目前 evals 只寫了斷言、還沒跑過。
- [ ] **humanizer-zh v1.1**：見 humanizer-zh-improvement-
  proposal.md——加結構級 detect 規則（節奏均質、零立場、零具體細節
  等「零病句仍看得出是 AI」訊號）。本次未動那個 skill。
- [ ] **benchmark 常態化**：每季挑一位作者重跑一輪，風味會隨作者
  近作演化。protocol 支援重跑。
- [ ] **真實 pipeline 串接測試**：目前 pipeline 效果是在單一對話裡
  模擬 humanizer-zh 的行為驗證的；在 Claude Code 真的載入兩個
  skill 跑一次，確認 detect-first 交棒實際運作。
- [ ] **新風味擴充**：若要加作者，流程是 (1) 爬雙篇 (2) 建
  style-<name>.md (3) 跑 benchmark protocol (4) 補進 voice-axes 配方表
  與 preset-guide (5) 加對應 eval。
- [ ] **個人配方收斂**：SKILL 已設計「連續三篇同配方視為個人預設」，
  但需要記憶機制支撐（跨對話），目前靠配方紀錄手動沿用。

## 如何接續（Claude Code 操作提示）

- 改風味：只動對應 style-*.md，跑一輪 benchmark 驗證。
- 加能力：先看 SKILL.md 的 Workflow（Step 1–6）現有結構，新能力
  盡量掛成某個 Step 的子項或正交模組（像 dual-draft 那樣），
  不要打亂主流程。
- 每次改動都補一條對應 eval assertion（本 skill 的 output-quality.json
  慣例：每條有 criterion / must / ref 指回 SKILL 或 reference 章節）。

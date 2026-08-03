# 計畫轉 Goal

粗略的計畫講的是「怎麼做」，goal 規格講的是「完成長什麼樣子」。這個技能把兩者接起來：拿一份多半還很粗的計畫，把它補完、攤開裡面的漏洞，讓你對真正需要判斷的地方拍板，最後才交出一份完成條件機器可自行檢查的 goal 規格——讓自動執行不必在跑的過程中去猜你的意圖。

## 安裝

```
npx skills add https://github.com/leoluyi/skills -g -a plan-to-goal -y
```

之後更新：

```
npx skills update plan-to-goal
```

[原始碼](https://github.com/leoluyi/skills/blob/main/skills/plan-to-goal/SKILL.md)

## 它做什麼

這個技能分兩階段執行，中間有一道閘門。

**第一階段**讀你的計畫（以及它牽涉到的程式碼），不執行任何東西，然後產出固定五個部分的審視：用白話講清楚真正完成的狀態、一組完成條件（每一條都必須是能靠執行一個指令驗證的——測試套件通過、typecheck 乾淨、grep 找不到東西——絕不是「乾淨」「重構得好」這種形容詞）、計畫裡真正的漏洞（寫成待答的問題，不是已經下好的決定）、難以回頭或代價高的高風險步驟，以及這一輪的讀寫範圍——可以讀哪些路徑、可以寫哪些、什麼碰不得、能不能對外送出任何東西。計畫裡原本就有的「不要動」限制也會一併帶下去。

**閘門**把這些漏洞分成兩堆：真的只有你能拍板的（列成 2 到 4 個標好取捨的選項，外加一個「其他」逃生口），以及探索過程中已經有答案的（陳述答案讓你確認，不會重新問一次）。不論哪一種，你都會在任何東西定案前，一次看到整個已解決的全貌——完成定義、每個分歧的答案、限制、讀寫範圍、完成條件——只需要一次是否確認。模型過程中順手想到的加碼工作不會塞進 goal，會另外列出來。

同一次確認還會固定帶一個選擇：goal 這一輪要怎麼交出來。**落檔**——決策紀錄加六元素寫進 goal 檔案，回你一行指向它的貼文，留版控、留可審的紀錄、貼文本身保持窄。**骨幹 prompt**——不落檔、不寫決策紀錄，只給六元素本身，本身就夠自成一體，可以直接貼進 `/goal`——成本最低，代價是每條裁決「為什麼」這樣定，過了這一輪就不留了。工程性質的任務（重構、遷移這類）預設落檔，臨時跑一次的任務傾向骨幹；技能會講清楚傾向哪一邊、為什麼，然後把這個選擇併進同一次是否確認，不另開一輪。如果你在交出計畫時已經表態，它不會再問一次。

**第二階段**在你確認之後才組裝六個元素——不論哪條路都一樣：

```
Outcome: <確認過的完成狀態，範圍限定在原計畫內>
Verification: <機器可驗證的條件，每一條都指名一個指令和預期結果>
Constraints: <原樣帶下來的「不要做」規則>
Boundaries: <可讀什麼、可寫什麼、什麼不能碰、能不能對外送出東西>
Iteration Policy: <每一輪要記錄什麼：做了什麼、結果如何、下一步最值得試什麼>
Blocked Stop Condition: <什麼情況算卡住，以及要留下什麼樣的回報>
```

走**落檔路線**時，把一份決策紀錄（決定了什麼、為什麼）加上這六個元素寫進 goal 檔案，然後只給你一行去貼，不是整份檔案：

```
/goal 依 @plans/goal-<slug>-<date>.md 執行。Done when: <條件>。Stop after <N> turns.
```

這個拆法是刻意的。goal 的條件是一個判定式，不是裝 context 的容器——goal 機制每一輪都會重讀那段文字來判斷做完了沒，塞一整頁散文進去只會讓判斷一輪比一輪糊（而且在終端機裡貼起來很痛苦）。長的內容——決策紀錄、完整六元素——留在檔案裡，靠檔案提及帶進去。如果你的 agent 沒有 goal 指令、或不支援檔案提及語法，那就直接把檔案全文當成 prompt。

走**骨幹路線**時，沒有檔案、沒有決策紀錄——就是上面那個六元素區塊，停損回合數以最後一行附在區塊裡，因為沒有檔案可以另外帶。這跟 `goal-definer` 自己的 Goal Prompt block 是同一個形狀，理由也一樣：沒有計畫可指，自然也沒有檔案。

不論走哪條路，停損回合數都是必填的——goal 會一直跑到條件達成為止，如果條件不可達（測試不穩定、本來就壞掉的測試），沒有停損就會一路空轉燒 token。

## 何時使用

正好在你手上已經有一份計畫——不論來自 plan mode 還是自己寫的——而它還很粗、還很高層、還沒補完，而你想讓 agent 無人值守跑完，又不要它中途偏掉或提早收工時使用。在自動執行開始前先把缺口補起來，正是這個技能存在的全部意義：它把每一次猜錯的代價，都挪到最便宜的時刻——在任何 token 和檔案改動發生之前。

## 何時不要

不要用它從零寫一份計畫——那是 plan mode 的工作，不是這個技能的。也不要用在一個 prompt 就能解決的小任務上——為了一行 typo 去寫一份 goal 規格，純粹是多餘的負擔。

## 運作方式

核心機制是把「描述完成」和「裁決模糊地帶」強制分開。一條完成條件只有在指名了一個指令和預期結果時才算數——「沒有任何檔案還在 import 舊模組」，用 `grep -r "legacy/payment" src/` 回傳空結果來驗證，而不是「重構很乾淨」。限制的處理方式一樣：「不要修改 `legacy/` 底下任何東西」會原封不動從原始計畫帶進最終的 goal，不會被改寫或漏掉。

限制和讀寫範圍分開處理也是同一個道理：限制講的是「怎麼做」的規則（「保留舊介面」），範圍講的是「可以在哪裡做」（「只能寫 `src/payments/` 底下」）。一輪執行可以完全遵守所有限制，卻還是跑進錯的目錄。

技能裡的一個示例：一份計畫寫著「已經把付款模組跨 14 個檔案重構完，想跑一下」，被補完成這些條件——`npm test` 通過、`npm run typecheck` 乾淨、`grep -r "legacy/payment" src/` 找不到東西——再加上一個真正待答的漏洞（「三個呼叫端還帶著一個 deprecated flag——留還是拿掉？」，以選項形式提問）、一個探索過程已經解決的漏洞（「`refundLegacy` 還有呼叫端嗎？」——沒有，grep 已確認）只陳述不再問，以及一個程式碼答不出來的範圍問題（這一輪可不可以 push？）。最後產出的 goal 檔案是：

```
Outcome: Every payment call site runs on the new module and the old one is gone from src/.
Verification: npm test passes; npm run typecheck is clean; grep -r "legacy/payment" src/ returns nothing.
Constraints: do not modify anything under legacy/; keep the deprecated flag on the three flagged call sites.
Boundaries: read anything in the repo; write only under src/payments/ and its tests; legacy/ is read-only; commit locally, never push.
Iteration Policy: per round, record which call sites moved, what the three commands returned, and the next call site to take.
Blocked Stop Condition: stop after three distinct failed hypotheses on one blocker, or if a condition turns out to be unreachable. Report what was tried, where it jammed, what is missing, and what decision would unblock it.
```

而你要貼的那一行：

```
/goal 依 @plans/goal-payment-refactor-2026-08-02.md 執行。Done when: npm test passes, npm run typecheck is clean, and grep -r "legacy/payment" src/ returns nothing. Stop after 25 turns.
```

如果當初選的是骨幹路線，就不會有檔案、也不會有決策紀錄——只有上面那個六元素區塊本身，停損回合數附在最後一行，直接就能貼。

## 相關技能

這個技能設計上是接在一份已經存在的計畫之後執行——通常直接接在 plan mode 之後，或是你自己手寫的計畫。它是跟產出那份計畫的東西（plan mode 本身）搭配運作，而不是取代它；它自己不做規劃，只做讓一份計畫能安全交給無人值守執行前該補的收斂工作。

# 救回被刪除的 Claude 對話

這個技能能在對話、訊息或產出檔案(docx/pdf)從 Claude Desktop 或 claude.ai 意外被刪除後，把它從 Chromium 快取中救回來。它只能手動呼叫——不會自己觸發，必須指名叫用——而且非常講求時效：東西一被刪除，底層的快取項目就開始面臨被清除的風險，所以請把這當成一場賽跑，立刻執行，不要先讀完全部說明才動手。

## 安裝

```
npx skills add https://github.com/leoluyi/skills -g -a recover-deleted-claude-conversation -y
```

之後更新：

```
npx skills update recover-deleted-claude-conversation
```

[原始碼](https://github.com/leoluyi/skills/blob/main/skills/recover-deleted-claude-conversation/SKILL.md)

需要機器上有 `uv` 和 `git`，且執行的 agent 要有 shell 存取權限。它不依賴任何特定 AI 助理——只要是能跑 Bash/shell 的 agent(Claude Code、Codex、Cursor 等)都能用，因為整個流程就是對本機快取目錄下指令。

## 它做什麼

Claude Desktop 應用程式(以及瀏覽器版的 claude.ai)本質上是個 Chromium 殼層，會把收到的每一個 HTTP 回應都快取下來，包括完整的對話內容與產生的檔案。在介面上刪除一段對話，只是把它從可見清單移除，不代表它一定已經從快取中消失。這個技能會：

1. 讓你把 Claude 行程完全關閉，避免任何東西繼續寫入(進而清掉)快取。
2. 把作業系統對應的 Chromium blockfile 快取目錄(`Cache_Data` 以及裡面的 `index`／`data_*`／`f_*` 檔案)複製到獨立的備份位置。
3. 建立一個隔離的 `uv` 虛擬環境，安裝 `ccl_chromium_reader` 以及相關的解壓縮函式庫(brotli、zstandard，加上標準函式庫內建的 gzip/zlib/zip)。
4. 走遍快取快照中的每一筆項目，解壓縮每個 HTTP 回應本體，寫出到 `extracted/` 目錄。
5. 在解出來的檔案裡搜尋對話的 UUID(或一段有辨識度的文字)，找出救回來的對話或產出檔案。

## 何時使用

在 Claude Desktop 或 claude.ai 的對話、訊息或產出檔案剛被刪除、你想把它救回來的當下，立刻指名呼叫這個技能。因為它只能手動觸發，不叫就不會執行——但只要決定要用，就要現在做，不要先忙完手邊其他事，因為每多一分鐘，快取項目被清除的機率就更高。

## 何時不要

一般的聊天紀錄查詢或匯出需求不要用這個——它不是通用的歷史紀錄瀏覽工具。跟救回遺失資料無關的一般快取清理問題也不適用。如果根本沒有東西被刪除，這裡就沒有需要跑的流程。

## 運作方式

Chromium 系應用程式把 HTTP 回應存在一種「blockfile」快取裡：固定的一組索引檔和資料檔，會隨著新回應進來被重複利用、覆寫。東西從介面上消失的那一刻，並不代表它立刻從硬碟上被刪除——那個項目只是變成「下次快取需要空間時可以被覆寫」的候選。這正是速度如此關鍵的原因：快取不會等你，一旦某個項目的儲存區塊被別的東西覆寫掉，原始的位元組就真的不見了。先把應用程式關閉(讓它無法再寫入任何新東西)、在做任何探索之前先把快取拍成快照，這樣後續的擷取步驟才有一份穩定不變的資料可以處理。blockfile 的封裝格式有其特殊性，一般的快取解析器會解錯，這也是為什麼這個技能特別依賴一套針對這個格式寫的函式庫，而不是自己手動解析。

## 相關技能

這是一個獨立的救援工具，不依賴本倉庫中任何其他技能，也不是任何技能流程中的一個步驟。

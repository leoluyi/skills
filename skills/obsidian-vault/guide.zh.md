# Obsidian 筆記庫

這個技能負責在 Obsidian 筆記庫裡搜尋、新增與串連筆記，讓每篇筆記都維持在既有的 PARA / Johnny-Decimal 資料夾結構下，並用 `[[wikilinks]]` 而非一般文字連結來串接筆記。

## 安裝

```
npx skills add https://github.com/leoluyi/skills -g -a obsidian-vault -y
```

之後要更新：

```
npx skills update obsidian-vault
```

[原始碼](https://github.com/leoluyi/skills/blob/main/skills/obsidian-vault/SKILL.md)

SKILL.md 裡寫死了一個特定的筆記庫路徑。在自己的機器上使用前，請先把那個路徑（以及編號資料夾清單，如果你的筆記庫用不同的分類方式）改成指向你自己的筆記庫——不要假設原檔裡的路徑可以直接搬用。

## 它做什麼

- **搜尋**整個筆記庫，可依檔名（`find ... -not -path "*/.obsidian/*"`）或依內容（`grep -rl ... --exclude-dir=.obsidian`），一律略過 Obsidian 內部的 `.obsidian` 目錄。
- **新增筆記**時放進符合主題的 PARA / Johnny-Decimal 資料夾，檔名依筆記庫既有的命名慣例（概念性筆記用 Title Case，工具性筆記用 lowercase-hyphen），並帶上 YAML frontmatter（`id`、`aliases`、`tags`，選填 `urls`）。
- **串連筆記**使用 `[[wikilinks]]`，把相關／依賴連結集中放到筆記底部的 `## Related` 區塊。指向尚未存在筆記的空連結（dangling link）不處理——那正好標記出值得日後寫的筆記。
- **找反向連結**：對任何一篇筆記，用一行 `grep -rl "\[\[筆記標題\]\]"` 就能找出全部反向連結。

## 何時使用

想在 Obsidian 筆記庫裡搜尋、新增或整理筆記時使用——找既有筆記、把新筆記放進對的資料夾，或是把筆記之間的連結串起來。

## 何時不要

不是把筆記寫成部落格文章的工具——那是 blog-writing-zh 的工作。也不是把筆記組成一份含 tutorial/how-to/reference/explanation 的結構化技術文件的工具——那是 knowledge-doc-writing 的工作。這個技能只管理筆記庫本身：搜尋、新增、串連。

## 運作方式

筆記庫採用 PARA / Johnny-Decimal 結構：編號的頂層資料夾，例如 `00-inbox`（尚未整理的隨手記錄）、`01-unique-notes`（原子化的長青筆記）、`02` 到 `05` 對應生活／投資／工作／技術等領域，以及 `97` 到 `99` 對應專案、封存與筆記庫系統本身。新增筆記時，要挑選符合其主題領域的編號資料夾（例如 AI 與寫作類筆記歸在 `05-tech/AI/` 下），而不是自創新資料夾或做深層巢狀——筆記庫的組織方式來自固定的編號資料夾加上筆記間的 wikilinks，而不是資料夾深度。

## 相關技能

- **blog-writing-zh** — 筆記內容寫好後，把它改寫成一篇完整的部落格文章；本技能只管理筆記本身，不負責改寫成文章。
- **knowledge-doc-writing** — 把消化過的素材重整成四區塊的 Diátaxis 文件；當筆記內容足以整理成參考級技術文件時再用它。
- **learn-loop** — 互動式先教後考迴圈，最後把筆記寫進同一個 vault；當目的是真的學會一個概念、不只是歸檔時改用它。

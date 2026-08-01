# avoid-china-writing — SF-14 / SF-15 spot-check — 2026-08-01

Single-arm spot-check of the two newly ported cases (ids 13, 14). Not an A/B run: this skill
has no `evals/run-case.json`, so there is no automated baseline to compare against. The point
here is narrower — does the new 標點慣例 rule fire, and do its carve-outs hold.

- runner: `codex exec` (gpt-5.6-luna, reasoning effort xhigh), `-s read-only`,
  `--ignore-user-config`, API-key env dropped
- rule set fed to the runner: `SKILL.md` (id 13) · `SKILL.md` + `references/term-table.md` (id 14)
- skill state: working tree with the 標點慣例 block added to axis D, the 半形標點 carve-out row,
  and the P2 tier note

## id 13 — SF-15 半形標點

| expectation | verdict |
|---|---|
| catches-halfwidth-in-chinese | pass |
| keeps-version-and-time | pass — `v1.2.3` 與 `23:59` 原樣 |
| keeps-thousands-separator | pass — `1,000,000` 原樣 |
| keeps-url-and-code | pass — `?a=1,b=2` 與 `render(a, b)` 原樣 |
| keeps-english-sentence-punctuation | pass |
| tier-p2 | pass — 標為「台灣排版慣例（P2）」 |
| not-a-prc-signal | partial |

`not-a-prc-signal` 判 partial 而非 pass：輸出把這一項標成「台灣排版慣例」，把它和 P0／P1 的陸源
判斷分開了，但沒有寫出「這不代表文件來自大陸」這句否定陳述。key 要求一句否定句，而規則本身要求的
是分開陳述 —— 兩者不完全對齊。下次調 key 時把它改成可驗的正面要求（軸線標成排版慣例、與陸源清單
分列），而不是要求輸出寫出一句否定。

## id 14 — SF-14 社群語域堆疊

| expectation | verdict |
|---|---|
| catches-social-register-terms | pass — 視頻／質量／博主／信息／接地氣 全中 |
| loads-term-table | pass — 另外抓到 `粉絲量→粉絲數`，該詞只在 term-table 裡 |
| xinxi-sense-choice | partial — 選了「資訊」（正確），但沒說明為何不是「訊息」 |
| keeps-social-register | pass |

`質量` 判為 P0 並附註「此處不是物理學的 mass」，`接地氣` 判 P2，分級與 SKILL.md 的 tier 規則一致。

## 這次驗證證明了什麼、沒證明什麼

證明：新加的標點規則會觸發，六類 carve-out 材料在同一段文字裡沒有被誤改，term-table 的深查在
社群語域下照樣發生。

沒證明：這條規則對既有 12 案有沒有副作用。單臂單輪，沒有基線可比。要說「沒有退步」需要這個 skill
先有 `evals/run-case.json` 與一份判分協議 —— 那是另一件工作。

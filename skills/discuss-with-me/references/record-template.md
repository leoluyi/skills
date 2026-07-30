# The open-question record

The file the loop writes into. It differs from a decision doc in one way that
matters: a decision doc argues for a conclusion, this one carries its own
falsification alongside it. Someone reading it in three months should be able to
tell what was known, what was guessed, and whether anything has since changed
enough to reopen it.

Default path: `docs/open-questions/YYYY-MM-DD-<topic>.md`, or wherever the user
keeps working notes. One file per question. Edit it in place across passes —
append-only logs of every turn bury the current state.

## Rules that keep it useful

- **Mark provenance inline.** Every load-bearing statement carries `[found]`,
  `[inferred]`, or `[guessed]` — and `[found]` carries a link or citation. A
  record where everything reads with equal confidence is the artefact this whole
  skill exists to prevent.
- **Date it.** An as-of line at the top. Open questions rot; the reader needs to
  know how stale the evidence is.
- **The open list is the point.** If the open-questions section is empty while
  the question is still open, the record is lying.
- **Keep the killed options.** What was considered and dropped, with the reason.
  This is the section future readers actually need, because it stops the pair
  from re-litigating the same option in six weeks.
- **Both sides of the argument survive.** The strongest case against the current
  direction stays in the file even after the direction is chosen.

Emit the headings in the user's language. Two variants below; use them verbatim
rather than translating on the fly.

## Traditional Chinese (Taiwan)

```markdown
# <問題一句話>

> 狀態：未定 / 已收斂 / 已化約為實驗　·　更新至 YYYY-MM-DD

## 問題是什麼

一到兩段。這個問題為什麼是開放的——誰不知道什麼。

## 目前最好的解釋

現階段最站得住的答案，每個承重句標 [已查證] / [推論] / [推測]。
沒有答案就寫沒有答案，不要用模糊句子填版面。

## 承重假設

| 假設 | 什麼情況下不成立 | 最便宜的驗證 | 停損線 | 誰會知道 |
|---|---|---|---|---|

## 反方最強論證

支持相反方向的最好理由，用它最強的版本寫，不是稻草人。

## 已排除的選項

| 選項 | 為什麼不採用 | 什麼情況下該重新考慮 |
|---|---|---|

## 待驗證

- [ ] 具體問題 —— 怎麼驗證：<可執行的動作> —— 誰做／什麼時候

## 來源

一手來源優先，標日期與版本；沒查到的就寫「未查證」。
```

## English

```markdown
# <the question in one line>

> Status: open / converged / reduced to a test · As of YYYY-MM-DD

## The question

One or two paragraphs. What makes this open — who doesn't know what.

## Current best account

The most defensible answer so far, each load-bearing sentence marked
[found] / [inferred] / [guessed]. If there's no answer yet, say so.

## Load-bearing assumptions

| Assumption | Fails if | Cheapest evidence | Kill criterion | Who would know |
|---|---|---|---|---|

## Strongest case against

The best argument for the opposite direction, in its strongest form.

## Options killed

| Option | Why not | What would reopen it |
|---|---|---|

## Open

- [ ] Specific question — how to settle it: <concrete action> — who / when

## Sources

Primary sources first, with dates and versions. Mark anything unverified.
```

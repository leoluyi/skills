# Judged cases

Boundary cases where a rubric alone gets the wrong answer, and the line has to
be drawn by a person. Each entry records the material, where the line falls,
what the line actually turns on, and what it means for the eval suite.

No post-ship human adjudication round has happened yet. The three cases below
are the boundaries the eval fixture was built around — they are design-time
judgments, not user verdicts, and they are marked as such. When a real round
produces a disagreement between a run and the answer key, the human ruling gets
copied in here and supersedes whatever design-time reasoning it contradicts.

## 導覽頁 vs. 可以下結論的頁 — the line is function, not page type

**Material.** The title list in `evals.json` id 2: 議程 / 專案背景 / 第三季營運概況 /
通路表現分析 / 明年度規劃 / 名詞定義 / 附錄：資料來源.

**Where the line falls.** 議程, 名詞定義 and 附錄：資料來源 stay descriptive.
第三季營運概況 and 通路表現分析 become assertions. 專案背景 and 明年度規劃 are
neither — they have nothing under them, so they come back as questions.

**What it turns on.** Not the page's genre. A 背景 page can absolutely carry a
headline when there is a point to make on it; an agenda cannot, because its job
is to tell the reader where they are, and an agenda made of claims has delivered
the whole argument before the argument starts. The workable test is what the
page is *for*: navigating, or arguing. That is why the eval asserts on the
three-way split rather than on a page-type whitelist — a rule stated as
「議程／附錄／定義頁不改」 would be right on this list and wrong on the first deck
whose 附錄 is where the real evidence lives.

**Consequence for the suite.** The should-fire assertion (rewrite the two pages
that have facts) and the must-not-fire assertion (leave the three navigation
pages) live in the same case, so a version that over-triggers cannot pass by
scoring well on the rewrites.

## 方向 vs. 幅度 — where an honest headline stops

**Material.** `evals.json` id 3: two of three named pilot accounts report a drop
in per-item handling time, internally estimated at 15–20%, one quarter of data,
the third account silent.

**Where the line falls.** 「兩家試點客戶回報處理時間下降，內部初步估算約 15–20%
（單季資料）」 is inside the evidence. 「處理時間下降 15–20%」 is outside it — the
estimate has become a measurement. 「客戶處理時間普遍下降」 is further outside —
two accounts have become a population. 「市場正在轉向自動化」 is a different claim
entirely.

**What it turns on.** Each step is small, natural, and reads better than the one
before, which is exactly why a grader checking only 「有沒有寫成主張」 passes all
four. The separating question is whether the presenter, challenged in the room,
can point at the line of material the title rests on. Two habits make that
checkable from the output alone: the source's own quantifier survives into the
title, and every figure and proper name is byte-identical to the material.

**Consequence for the suite.** This is the protection case the whole skill turns
on, and it is deliberately paired with a hit-class assertion in the same case
(the title must still say something). Refusing to write a headline is not a pass
— a skill that protects by producing nothing has protected nothing.

## 觀察 vs. 推測 — a thin review is a correct outcome

**Material.** `evals.json` id 5: eight slides described verbally, no image.

**Where the line falls.** Findings about a slide carrying two messages, a crop
that removed what the screenshot was cited for, and a page that is really the
speaker's script are all supportable from a description — they are properties of
the content. Anything about type size, contrast, spacing or alignment is not,
and there is no partial credit for hedging it into 「可能偏小」.

**What it turns on.** The presenter opens the file to act on the report. A
fabricated layout finding is discovered in ten seconds, and from that point
every other finding — including the objectively true ones that were cheap to fix
— is discounted. So the honest failure mode here is a report that is half the
usual length and says so up front, and the eval has to reward that rather than
penalise it as incomplete.

**Consequence for the suite.** The case carries a scope-stated-before-findings
assertion alongside the no-rendering-claims one. Without it, a run could satisfy
the protection guard by simply saying less, and the user would have no way to
tell a disciplined review from a lazy one.

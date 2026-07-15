---
name: plain-speak
description: >-
  Translate technical jargon, code concepts, or dense engineering text into
  plain language a non-technical colleague or manager can follow. Use when the
  user asks to "explain in plain language", "白話文", "翻成人話", "用白話解釋",
  "explain like I'm a PM", "make this non-technical", "simplify this term",
  "what does this term mean", or pastes technical text and asks for a
  business-audience version. Reply in the language the user wrote in. Do NOT
  invoke for removing AI-isms / 潤飾語氣 from existing prose (use
  avoid-ai-writing-zh), for structuring a whole formal business document —
  簽呈/會議紀錄/報告 (use formal-doc-structure), or for RFP / 需求規格書 /
  招標規格 (use rfp-writing). This skill lowers the audience, not the voice,
  the structure, or the document type.
---

# Plain Speak — 技術術語轉白話文

Turn a technical term, snippet, or paragraph into something a **non-technical
business reader** can follow. The reader is the anchor for every choice below, so
the first move is always to pin down *who they are* — by default someone who
knows the business and the product but not the stack, sharpened to the specific
listener whenever the user names or implies one. Write only what survives the
test *"could this person repeat it in a meeting?"*

## When this applies

- A single term to define ("什麼是 idempotent", "explain eventual consistency")
- A chunk of technical text to rewrite for a business audience
- A code snippet or error the user wants explained in human terms
- Prep for a status update, exec summary, or doc aimed at non-engineers

Sibling skills own the adjacent axes — hand off rather than half-do their job:
lowering AI-ish *voice* in prose → `avoid-ai-writing-zh`; organizing a whole
formal *document* → `formal-doc-structure`; an *RFP* → `rfp-writing`.

## Output language

Match the user's request language. Keep each technical term in its native form
the first time you introduce it — write "idempotent(冪等)", not a translated-away
version — because the reader may have to recognize it elsewhere.

## How to respond

1. **Identify the reader first.** Who actually reads or hears this — stated by
   the user, inferable from context (a PM, an exec/CFO, a salesperson, a
   customer, a vendor), or, if nothing says, the default non-technical manager.
   Everything below flexes off this one choice: the *same* term becomes a
   different 白話 for a CFO (財務影響) than for a salesperson (客戶好處). If the
   reader wasn't given, name the one you assumed in one passing clause of the
   prose so the user can correct it — never as a "Who's asking:" label or header.
2. **One-line answer — what it does, and what it's for.** Two beats in one
   breath: *what it does* (the plain function, no jargon) and *what it's for*
   (the problem it solves — what was painful before it existed). A single
   sentence the reader could repeat in a meeting. This line is the deliverable;
   the rest is optional support.
3. **Why it matters — to this reader.** Distinct from step 2's intrinsic
   purpose: the reader-relative consequence — what breaks without it, what it
   saves, what decision it affects.
4. **(Optional) Analogy — informal/spoken only.** For a live explanation or a
   casual reply, one line of analogy when it clarifies more than a plain sentence
   would. Never in formal written output (a status doc, an exec summary) — there,
   drop it and let the plain sentence carry the point.
5. **(Optional) The catch** — a trade-off or caveat they should know before
   nodding along.

Calibrate to that reader: skip implementation detail unless it changes a decision
they'd make; lead with impact, risk, or cost; never explain jargon with jargon —
define any unavoidable second term inline.

Write a single short term as natural sentences, no headers or bullets. Use light
structure only when rewriting a longer passage with several distinct points.
Length tracks the input: one term ≈ 2–4 sentences; a paragraph ≈ a tight
rewrite no longer than the original.

## Guardrails

- **Accuracy outranks simplicity.** Never simplify into something wrong. If a
  nuance changes a decision, keep it and phrase it plainly.
- **Flag ambiguity, don't guess.** If the source is ambiguous, give the most
  likely reading and note the ambiguity in one line.
- **No unglossed acronyms or jargon.** Never let an abbreviation or term of art
  (SaaS、CI/CD、五字訣…) carry the meaning of a sentence. Replace it with the
  plain idea; keep the term only as a parenthetical label the reader can match
  later — as with "idempotent(冪等)" in Output language above.

## Examples

**Input:** 用白話解釋 idempotent

**Output:**
Idempotent(冪等)意思是「同一個操作做一次跟做很多次,結果都一樣」。
比方說「把訂單狀態設成已付款」是冪等的——不管系統重試幾次,訂單就是已付款,
不會變成付了兩次。這在網路不穩、請求可能重送的情況下很重要,可以避免重複扣款
或重複建單這類事故。

---

**Input:** explain what a race condition is, for my PM

**Output:**
A race condition is when two things happen at the same time and the final
result depends on which one finishes first — so the system behaves correctly
most of the time but breaks unpredictably under load. Think of two people
editing the same doc cell at once: whoever saves last silently wins, and the
other edit vanishes. It matters because these bugs are intermittent and hard to
reproduce, so they often slip past testing and only show up in production.

---

**Input:** 老闆問 API 是什麼,幫我用白話講

**Output:**
API(應用程式介面)就是兩套系統之間的「點餐窗口」。比方餐廳:你(一支程式)
看菜單點餐,服務生(API)把需求送進廚房(另一套系統),再把做好的菜端回來——
你不用知道廚房怎麼運作,照窗口的規則點餐就好。對我們的意義是:別人的系統要用
我們的資料或功能,不必了解我們內部怎麼做,照這個窗口串接就行,整合更快也更好控管。

---
name: plain-speak
description: >-
  Translate technical jargon, code concepts, or dense engineering text into
  plain language a non-technical colleague or manager can follow. Use when the
  user asks to "explain in plain language", "白話文", "翻成人話", "用白話解釋",
  "explain like I'm a PM", "make this non-technical", "simplify this term",
  "what does this term mean", pastes technical text for a business-audience
  version, or asks whether an existing plain-language draft works for a
  non-technical reader ("這樣夠白話嗎", "幫我看非技術主管看不看得懂",
  "is this clear enough for a PM"). Also use mid-conversation for requests to
  re-explain preceding content ("上面那段用白話再講一次", "你剛剛講的我看不懂",
  "剛剛那幾個選項差在哪", "講人話"), including a question just put to the
  user. Reply in the user's language. Do NOT invoke for removing AI-isms /
  潤飾語氣 (use humanizer-zh), structuring a formal business document
  (簽呈/會議紀錄/報告; use formal-doc-structure), or RFP / 需求規格書 /
  招標規格 (use rfp-writing). This skill lowers audience complexity, not voice,
  structure, or document type.
app-description: 把技術術語、程式概念或艱澀工程文字翻譯成非技術主管或同事能懂的白話文。適用於「白話文」「翻成人話」「用白話解釋」「講人話」，或審閱既有白話草稿是否「夠白話」。不去除 AI 寫作腔調。
version: 1.5.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing explanation plain-language audience-translation zh-tw bilingual
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F5E3️"
---

# Plain Speak — 技術術語轉白話文

Turn a technical term, snippet, or paragraph into something a **non-technical
business reader** can follow. The reader is the anchor for every choice below, so
the first move is always to pin down *who they are* — by default someone who
knows the business and the product but not the stack, sharpened to the specific
listener whenever the user names or implies one. Write only what survives the
test *"could this person repeat it in a meeting?"*

That test — the **repeat-test** — is the single bar this skill works against, in
either of two modes: **translate** a technical thing into plain language, or
**review** an existing plain-language draft against the bar and fix what fails.
Both run the same criteria below; translate produces to them, review checks them.

## When this applies

- A single term to define ("什麼是 idempotent", "explain eventual consistency")
- A chunk of technical text to rewrite for a business audience
- A code snippet or error the user wants explained in human terms
- Prep for a status update, exec summary, or doc aimed at non-engineers
- A finished plain-language draft to review — a colleague's, or your own — against
  the bar before it reaches the reader
- Something in this very conversation the user lost the thread on — an answer just
  given, or a question just put to them (§When nothing is attached)

Sibling skills own the adjacent axes — hand off rather than half-do their job:
lowering AI-ish *voice* in prose → `humanizer-zh`; organizing a whole
formal *document* → `formal-doc-structure`; an *RFP* → `rfp-writing`.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material.

Keep each technical term in its native form the first time you introduce it — write "idempotent(冪等)", not a translated-away version — because the reader may have to recognize it elsewhere.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## When nothing is attached

A user who reaches for this skill mid-conversation without pasting anything is
pointing at what just happened: the target is the **preceding turn**, and the
reader is **the user themself** — someone who follows the business and the
product but lost this particular thread. No third-party audience gets invented
here, and asking which part they meant defeats the point; pick the target by the
order below and name it in one opening clause, so a wrong pick costs one word to
correct.

1. **A question left with the user** — anything you asked and are still waiting
   on, with options or without. This outranks a plain answer: they aren't merely
   lost, they're blocked on a decision.
2. **The last substantive answer or explanation.** Step back over turns that are
   pure tool work, diffs, or status lines with nothing explained in them, to the
   last turn that actually carried reasoning.
3. **Nothing technical in reach** — say so in one line and ask what to lower. A
   turn that was already plain needs no translation, and manufacturing a
   "plainer" version of plain text is the same failure as inventing a number the
   source never had.

An invocation that carries a reader but no content (「給 CFO」, "for my PM") sets
that reader; the target still comes from the order above.

**A question gets re-posed, not just explained.** Lower the question itself, then
each option with what choosing it actually commits or costs — the difference
between the options is usually the exact thing that was opaque — and close by
asking it again so the user can just answer. The option set survives untouched:
same options, same order, none merged, none added, none quietly dropped, so a
reply aimed at the original still lands. Plain text carries this on its own;
where the host offers an interactive question tool, use it, but the deliverable
stands without one.

**Lowering is not re-deciding.** A translated answer keeps its substance exactly
— same recommendation, same options, same caveats, no new ones. If lowering the
language exposes something the original got wrong or overclaimed, that earns one
separate line, never a quiet edit inside the translation. Then stop: this is a
request to be understood, not a signal to resume the work it interrupted.

## How to respond

1. **Identify the reader first.** Who actually reads or hears this — stated by
   the user, inferable from context (a PM, an exec/CFO, a salesperson, a
   customer, a vendor), or, if nothing says, the default non-technical manager —
   except when nothing was attached and the target came from the conversation, where
   the reader is the user themself (§When nothing is attached).
   Everything below flexes off this one choice: the *same* term becomes a
   different 白話 for a CFO (財務影響) than for a salesperson (客戶好處). A reader
   the user named stands as given — don't sharpen it into a sub-segment you then
   hedge over. Where you did have to assume, the assumption rides inside the prose
   as a passing clause, not as a label, header, or parenthetical preamble the
   deliverable hangs off, and it arrives with no offer of an alternative version:
   one reader, one deliverable, so the line stays repeatable instead of reaching
   the reader wrapped in conditions. When the reader genuinely can't be inferred
   *and* that choice would change the substance rather than the emphasis, name the
   ambiguity in one line after the deliverable (Guardrails) — still one version.
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

Before returning, run the review checklist (§Reviewing a draft) over your own
draft and fix any ✗ — the self-review gate is this same bar applied to yourself.

## Reviewing a draft

When the input is an already-written plain-language draft — a colleague's, or
your own pre-send — don't rewrite blind. Grade it against the bar, then fix.

Mark each criterion pass (✓) / fail (✗) / not-applicable (—):

- **Reader locked** — one specific reader in view, not a generic "non-tech", and not
  two readers hedged against each other? (§How to respond 1)
- **What-it-does + what-it's-for** — one line carrying both beats? (§2)
- **Reader-relative why** — the consequence *to this reader*, not just intrinsic purpose? (§3)
- **Analogy fits the medium** — present only where it belongs (spoken/casual), out of formal written output? (§4)
- **The catch** — any trade-off whose omission would mislead is stated? (§5)
- **Every term glossed** — no acronym or term of art carries a sentence unglossed? (Guardrails)
- **No plainness-narration** — free of「白話講/白話來說/說白了/簡單來說」-type self-framing? (Guardrails)
- **具體度** — states concrete, checkable facts, not abstract modifiers standing in for them (「大幅提升/全面優化」without a number)? (Guardrails)
- **計畫可執行度** — where the draft says what will be done, does it name 做法(誰、
  做什麼、做到什麼算完成)rather than 原則? Mark — when the draft states no plan.
  (Guardrails)
- **Accurate** — simplification didn't bend anything into something false? (Guardrails)

Output stays flat — one bullet list of the marked criteria (each ✗ carrying a
clause that names the failing line and why), then the corrected draft, held to
the same length discipline as a translate. No section headers.

## Guardrails

- **Accuracy outranks simplicity.** Never simplify into something wrong. If a
  nuance changes a decision, keep it and phrase it plainly.
- **具體優先於抽象。** A concrete, checkable fact beats an abstract description of
  the same thing —「查詢從 3 秒降到 0.3 秒」not「大幅優化效能」,「去掉重複跟空值」
  not「對資料進行清洗處理」. The failure mode to kill is padding a "plain" sentence
  with reassuring but empty adjectives (「全面」「整體」「大幅」「有效地」) — they
  lengthen without informing. Division of labor with concision: **具體 picks
  *which fact* to state; 精煉 cuts *everything that isn't the fact*** — they
  share no ground, so you hold both, and the concrete version usually runs
  *shorter*, because one fact replaces a pile of empty modifiers. When detail
  genuinely overflows and buries the point, the cut is not "be less concrete" —
  it's picking the one or two most representative, checkable facts and dropping
  the rest (representative-concrete, not exhaustive-concrete). Operationally:
  when the source itemizes more than ~3 things, do not translate the list. Lead
  with the headline fact the reader actually needs (the outcome,「吞吐量翻倍」),
  fold the items into one theme clause naming the *kind* of change (「放寬了各處
  的排隊上限」), and cite at most one item as an illustrative example. Enumerating
  every item back to the reader is exhaustive-concrete — it reads as thorough
  but buries the one number that mattered.

  When the material is a plan, abstraction wears a second face: the **原則**.
  It reads like content (「分階段導入、控制風險」), so it slips past the
  empty-adjective guard above. The concrete form is a **做法** — who does what,
  and what counts as done:「HPA 上限從 10 調到 30,下週三上線」not「加強容量
  管理」. Representative-concrete folds *evidence* — the causes behind an
  outcome; a plan's moves are not evidence, they are what the reader is waiting
  on, so keep every move that changes what they decide or wait for and fold
  only the rest. A 做法 the source doesn't contain is not yours to invent: when
  the plan is all 原則, say so in one line and ask what the actual next step is.
- **Flag ambiguity, don't guess.** If the source is ambiguous, give the most
  likely reading and note the ambiguity in one line.
- **No unglossed acronyms or jargon.** Never let an abbreviation or term of art
  (SaaS、CI/CD、五字訣…) carry the meaning of a sentence. Replace it with the
  plain idea; keep the term only as a parenthetical label the reader can match
  later — as with "idempotent(冪等)" in Output Language above.
- **Never narrate the plainness.** The output must not contain self-referential
  framing like「白話講」「白話來說」「白話說」「說白了」「簡單來說」「講白一點」
  or English equivalents ("in plain terms", "simply put"). The whole deliverable
  is already the plain version — just say the thing directly. These phrases add
  nothing and signal that the sentence they precede wasn't plain enough on its
  own; rewrite that sentence instead of prefixing it.

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

---

**Input:** 幫我看這段給高層的白話寫得夠不夠白:「我們碰到 HPA 上限,pods 在尖峰
負載下停止 autoscaling,導致部分請求 503。」

**Output:**
- 讀者鎖定:— 只說「高層」,沒細分(CFO 看成本 / 產品高層看客戶影響)
- 一句話做什麼+為什麼:✗ 只描述現象,沒說這對業務是什麼事
- 對這位讀者的意義:✗ 缺
- 類比適配:—(篇幅短,不需要)
- The catch:—
- 術語 gloss:✗「HPA」「autoscaling」「503」三個都沒解釋就承載語意
- 具體度:✓ 有具體機制與可查的錯誤(撞上限、503),不是空泛描述
- 計畫可執行度:—(原文只描述現象,沒講接下來要做什麼)
- 失真:✓ 事實正確

改寫版(對象抓成看客戶影響的產品高層):
系統在流量尖峰時,原本會自動增加機器來吸收暴量的機制撞到了設定上限,機器加不
上去,於是一部分使用者的請求被擋掉、看到錯誤畫面。對我們的意義是尖峰時段有真實
使用者受影響、可能流失;要嘛調高上限,要嘛在流量可預期時預先擴容。

---

**Input:** (對話中間,使用者沒附任何文字;上一輪是丟給他的選擇題)
「並發寫入要用 optimistic 還是 pessimistic locking?A: optimistic,衝突時 retry。
B: pessimistic,先鎖 row 再改。」

**Output:**
剛剛問你的是:兩筆修改同時進來時,要怎麼避免其中一筆被蓋掉。兩個做法的差別是
「先各改各的、存檔才對帳」還是「先排隊、一次只讓一個人改」。

- A(optimistic,樂觀鎖):兩邊都先改,存檔時才檢查有沒有人搶先;沒撞到的時候最快,
  撞到的那個人要重做一次,愈多人同時改同一筆、重做就愈頻繁。
- B(pessimistic,悲觀鎖):誰先進來就把那筆資料鎖住,其他人等它放開;沒有人會白做,
  代價是等待,同時要改的人多時會卡住。

這兩個你要哪一個?

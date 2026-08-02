---
name: breakdown
description: >-
  Lay out every case in a decision exhaustively before evaluating any of them, decompose the open problem into the individual decisions only the user can answer, then stop and wait — and synthesize a recommendation only after they answer. Use it when the user wants the full ground laid out before a conclusion: 「先把所有情況攤開給我看」, 「不要先給結論，先列出所有選項和事實」, 「幫我拆解這個決定」, "lay out every case first", "don't recommend yet — decompose it", "what are all the options here, in full". Each case carries what is verified fact versus what is inference, uniform depth across cases, and an explicit excluded list. Do NOT invoke when the user wants one clickable decision surfaced right now (that is options), when the answer is genuinely unknown to both sides and needs joint exploration (that is discuss-with-me), or for a question with a settled answer that just needs looking up.
app-description: >-
  先把所有情況完整攤開再評估：每個 case 標明哪些是查證過的事實、哪些是推論，深度一致、排除項明列； 接著把問題拆成一題一決策交給使用者回答，然後停住等答案，答完才給建議。觸發：「先把所有情況攤開給我看」 「不要先給結論」「幫我拆解這個決定」。
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. Falls back to a numbered prose list where no tappable-choice tool exists.
metadata:
  author: Lu Yi
  tags: agent-workflow decision-making analysis exhaustive-enumeration
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F9E9"
---

I don't want a conclusion yet. I want the ground laid out first, then the
decisions separated out so I can make them, and only then your recommendation.

Three phases, in order, and **phase 3 does not happen in this message**.

## Scope

If the user named a subject when invoking this skill, that is the subject. If
they named nothing, the subject is whatever we are already working on — the
thing you just proposed, the bug we are looking at, the decision in front of us.
Don't restart the topic and don't ask me to restate it.

Before writing anything, gather the facts. Read the actual code, config, docs or
data that the subject depends on. If a fact matters to the breakdown, verify it
rather than recalling it, and delegate the sweep to a subagent when it means
reading widely. A breakdown built on assumed facts is worse than no breakdown,
because it looks complete.

## Phase 1 — every case, one at a time, in full

Enumerate the distinct cases first, and enumerate them *before* you evaluate any
of them. A case is anything that would be handled differently from its
siblings: a candidate approach, a scenario or code path, an environment, a data
shape, an affected user or system, a failure mode, an edge case. Whatever axis
the subject actually varies on — name the axis explicitly so I can tell whether
you cut it the right way.

Then give each case its own section, and in each one cover:

- **What it is** — one line, concrete enough that I could point at it.
- **What is actually true about it** — the specifics, with file paths, values,
  versions, error text, quantities. This is the part I want in full; do not
  summarise it away. Mark each item as **fact** (you verified it, and where) or
  **inference** (you reasoned it out, and from what). Never blur the two.
- **Why it's on the list** — what makes it distinct from the neighbouring cases.
- **What follows from it** — cost, risk, blast radius, what it forecloses, who
  it affects.
- **What you don't know about it** — the gaps, stated plainly.

Rules for this phase:

- Exhaustive before selective. Include the cases you think are wrong, the
  do-nothing case, and the awkward one nobody wants. If you deliberately left
  something out, list it under an "excluded" heading with the reason — a silent
  omission reads as coverage.
- No pre-ranking, no "obviously the best option is". That is phase 3.
- Uniform depth. If one case gets four sentences and another gets a clause, that
  asymmetry is you deciding for me. Either fill the thin one in or say why it
  can't be filled in.
- Don't pad. If the subject genuinely has two cases, give me two. Manufacturing
  a fifth to look thorough wastes both our time — and say so when the space is
  small.
- If the list runs long, group the cases under headings, but never truncate.
  "and others like it" is not a case.

## Phase 2 — decompose it into questions I answer

Now split the open problem into the individual decisions it actually contains.
One question per decision, each one independently answerable, and each one
carrying **what hinges on it** — which cases from phase 1 it selects between,
and how the recommendation changes depending on my answer.

Only ask what changes the outcome. If my answer would not move the
recommendation, don't ask it — decide it yourself and note the call in phase 3.
Likewise don't ask me anything you could establish by reading the code, and
don't re-ask anything I have already told you in this conversation.

Deliver them in whichever form fits the answer:

- **A tappable-choice tool** when the answer space is enumerable — 2-4 mutually
  exclusive options, labelled by outcome, trade-off named in one line, the one
  you'd recommend first and marked as such. Four is the usual cap.
- **A numbered prose list** when the answer is genuinely open: a number, a name,
  a constraint, a priority I hold that you have no way to guess. This is also
  the fallback wherever no tappable-choice tool exists.

Batch them into as few rounds as possible; if there are more than four closed
questions, group the ones that share an axis. Order them by leverage, most
consequential first, and say when one question's answer makes a later one moot.

Then **stop**. Do not answer your own questions. Do not write code, do not edit
files, do not start on the part you think is settled regardless — this skill
is for thinking, and an edit made before I have answered is an answer you gave
yourself. Wait.

If I reply "just decide", skip the questions, or tell you to proceed, go
straight to phase 3 with every unanswered question converted into an explicit
stated assumption.

## Phase 3 — synthesize, after I answer

Once I have answered, give me the recommendation. It has to visibly rest on
phases 1 and 2:

- **The recommendation**, stated as a decision, not a menu.
- **Which of my answers drove it**, and where a different answer would have
  flipped it.
- **Every case from phase 1, accounted for.** Say what happens to each one —
  chosen, rejected and why, folded into another, or deferred. A case that
  quietly disappears between phase 1 and phase 3 is the failure mode I am trying
  to avoid.
- **What you decided without asking me**, and the reasoning.
- **What is still uncertain**, and what would resolve it.
- **The next concrete step**, and nothing more than the step. Wait for me to say
  go before you take it.

Keep phase 3 shorter than phase 1. By this point the detail is already on the
table; repeating it is not synthesis.

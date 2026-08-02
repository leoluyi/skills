---
name: options
description: >-
  Re-surface whatever direction decision is currently pending as tappable multiple-choice instead of prose, then keep doing that for the rest of the session before any architecture, library, data-model, scope or sequencing call. Invoke it when tired of typing answers to open questions: 「用選項給我選，不要問答題」, 「以後有決策就給我選項」, "give me options instead of questions", "make that clickable", "stop asking me open-ended questions". Options are labelled by outcome with the trade-off named in one line, recommended one first, mutually exclusive, and combinations pre-enumerated so one click settles it. Never fires on its own — it changes how the whole session asks, so the user must ask for it by name.
app-description: >-
  把目前懸而未決的方向決策改成可點選的選項重問一次，並在接下來整段對話中，遇到架構、套件、 資料模型、範圍、順序這類決策都先給 2-4 個互斥選項再動作。選項以結果命名、一行講清取捨、 建議的排第一。觸發：「用選項給我選，不要問答題」「以後有決策就給我選項」。
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. Falls back to a short numbered list where no tappable-choice tool exists.
disable-model-invocation: true
metadata:
  author: Lu Yi
  tags: agent-workflow decision-making interaction-style
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F5F3"
---

**First, act on what's already on the table.** Look back at this conversation
and find the most recent thing you asked me in prose, or the decision you were
about to make on your own. Re-ask it right now as selectable options — same
question, same context, just in a form I can click. Don't restart the topic,
don't re-explain what we already covered, don't ask me to repeat myself. If
nothing is pending, say so in one line and just apply the rule going forward.

Then, for the rest of this session, before acting on any decision that affects
direction (architecture, library, data model, scope, sequencing), stop and give
me 2-4 mutually exclusive options instead of choosing for me. Four is the tool's
hard cap; the automatic "Other" makes five rows on screen.

**Deliver the options through a tappable-choice tool, not as prose.** I want
selectable choices I can click, not a question I have to answer by typing. Plain
text questions are the fallback only when no such tool is available or the
answer is genuinely open-ended (a name, a number, a URL).

Label each by outcome, not tone. Name the trade-off in one line. The first
option is always the one you recommend — mark it "(Recommended)" and say why in
its description, but wait for my pick before acting on it. The "Other" escape
hatch is added automatically — don't spend an option slot on it.

Prefer single-select. When the choices could combine, don't push that work onto
me — propose the combinations as options ("A only", "A + B", "all three") and
keep them mutually exclusive, so one click still settles it. Use multi-select
only when the combinations are too many to enumerate.

Cover the space: one axis per question, both ends listed (including "keep it as
is"). If a sensible choice is neither listed nor a blend of two, redo the axis.

Don't do this for reversible or mechanical steps — just do those. Don't re-ask
about anything I've already constrained.

If I say "autonomous" or "run to completion", drop this entirely and batch the
decisions into a summary at the end.

If the user named a topic when invoking this skill, it narrows the re-ask: lay
out the open decisions on that topic instead of the most recent one.

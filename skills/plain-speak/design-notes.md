# plain-speak — design notes

Iteration log and rationale. Not loaded by the skill; for maintainers.

## v1.5.0 — bare invocation targets the conversation (2026-07-30)

**Problem.** Invoked mid-session with nothing attached (`/plain-speak` on its own), every path in
the skill assumed an input: §When this applies listed a term, a passage, a snippet, and §How to
respond step 1 defaulted the reader to a non-technical manager. Two bad outcomes followed — either
the model asked "which part did you mean?" (defeating the one-keystroke intent) or it lowered the
preceding turn *for a hypothetical manager*, inventing an audience the conversation never had.

**Fix.** A `## When nothing is attached` section placed before §How to respond, because what it
resolves is *what the input is* — upstream of reader identification. Three parts:

1. **Target resolution order:** a question still awaiting the user's answer > the last turn that
   actually explained something (stepping back over tool work and status lines) > nothing technical
   in reach, which is a one-line "nothing to lower here, what did you mean?" rather than a
   manufactured translation. The pending-question priority is the substantive call: the user isn't
   merely lost, they're blocked, and the option list they'd answer against is no longer on screen.
2. **Reader flips to the asker.** Step 1's manager default now carries an explicit exception with a
   cross-reference both ways. A reader supplied without content (「給 CFO」) overrides the reader and
   leaves target resolution alone — the two halves are independent, which eval case 11 pins.
3. **Two path-local guardrails:** the option set is data to lower, not to edit (same options, same
   order, nothing merged/added/dropped, so a reply aimed at the original still lands), and lowering
   is not re-deciding — same recommendation, same caveats, and a wrong original earns one separate
   line instead of a quiet edit inside the translation. The second one matters because on this path
   the thing being translated is the model's *own* prior answer, where silently improving it is the
   natural failure mode.

**Portability.** No slash syntax in the body — the rule reads "when nothing is attached", which also
covers the natural-language forms (「你剛剛講的我看不懂」). Re-posing a question is specified as plain
text with an interactive question tool as an optional enhancement, so nothing is load-bearing on a
Claude-Code-only feature.

**Example added deliberately.** One worked example, for the re-posed-question shape only — that output
shape (lowered question, options in order with per-option cost, closing re-ask) is the least derivable
part of the section. The other three paths derive from the rules and got none.

**Eval approach and its limitation.** Cases 8–12 embed a synthetic transcript in the prompt («上一輪你
回答了…使用者接著沒有附任何文字»). This is an approximation: the harness delivers one user message, so it
tests whether the model resolves a stated prior turn as the target, not whether it reaches into genuine
session state. That gap is real but not closable from a single-prompt harness; the behaviours it can't
reach (skipping tool-work turns to find the last substantive one, an interactive re-ask through the
host's question tool) need real transcripts in `judged-cases.md` to verify. Case 12 is the must-not-fire
boundary the new path needs most — content supplied *plus* a preceding turn present, where the
conversation must not become the target.

**Result.** v1.5.0 passed 6/6 arms on the three discriminating cases (8, 9, 10); v1.4.0 passed 1/6,
failing in one direction across both reps each time — inventing a third-party audience, appending its
own decision tree to a question that contained no recommendation, and manufacturing a whole task
rather than saying a plain turn needs no lowering. Regression 7/7. Full log:
`evals/results-2026-07-30-context-recall.md`.

**Two lessons about the cases themselves, both worth carrying forward.** Case 11 (reader supplied,
content not) came back 2/2 on both arms: stating outright in the prompt that nothing was attached
hands target resolution to the baseline for free, and a named reader is all v1.4.0 ever needed, so the
case can only confirm the override fires — it can't discriminate. Same class of flaw as v1.4.0's
first draft of case 5, in a new disguise: there the case sat *at* an existing rule's threshold, here it
*supplies the input* the rule was supposed to derive. Case 12 then showed the inverse failure: an
assertion banning any 「剛剛/上一輪」 reference to the preceding turn was violated by all four outputs
in both arms, because all four mentioned it to stop its p99 figures being attached to the index change
— the accuracy guardrail doing its job. Both arms tripping one assertion identically is the signature
of a mis-specified assertion, not a regression; reworded to target *retargeting* rather than *mention*.
Generalised: an assertion phrased as "the output must not contain X" is suspect whenever X has a
legitimate use in the same case.

### Same release — the reader hedge (found while reading v1.5.0's own eval outputs)

**Problem.** Unrelated to bare invocation, and pre-existing: step 1 said to name an assumed reader
"in one passing clause of the prose … never as a `Who's asking:` label or header", and the outputs
routinely violated the spirit while passing the letter — a parenthetical preamble is not a header, so
「給非技術主管的版本(假設是關心服務品質的主管,若對象是看成本的財務長我再改成談機器與費用):」 slipped
through. Two distinct defects were tangled there: the assumption announced as a *preamble the
deliverable hangs off*, and a *conditional alternative-version offer*. The second is the worse one —
it breaks the repeat-test directly, since a line that arrives wrapped in 「假設對象是X」 is not a line
anyone can repeat in a meeting. It also fired when the user *had* named a reader: the model sharpened
「非技術主管」 into a finer segment of its own invention, then hedged over the invention.

**Root cause was the skill teaching it.** The review example ended with 「改寫版(先假設是產品高層、看客戶
影響;若對象是 CFO 再改成談成本):」 — a worked example demonstrating the exact anti-pattern, which per
the repo guide fences the model into the space it demonstrates. Fixed the example alongside the rule.

**Why this couldn't be a flat prohibition.** The legitimate neighbour is the existing
`Flag ambiguity, don't guess` guardrail: when the reader genuinely can't be inferred *and* the choice
changes substance rather than emphasis, one line naming it is correct. So the rule had to draw the
line by position and form (a clause inside the prose vs a preamble the deliverable depends on; a note
after the deliverable vs a condition wrapped around it) and by the emphasis/substance test — not by
banning reader-talk. Cases 13 and 14 are the pair that pins both sides.

Result: 4/4 vs 1/4 against the unfixed version, regression 4/4, no suppression of the ambiguity flag.
Log: `evals/results-2026-07-30-context-recall.md` (round 2).

## 這兩個行為，單提示 harness 量不到

`evals.json` 的 8–12 案把逐字稿**嵌在提示裡**測 bare-invocation 的目標解析。這樣測得到
「有東西可解析時選對了沒有」，測不到解析順序的兩段：

- 跨過純工具工作與狀態訊息、回退到最後一個真正帶推理的 turn；
- 在有互動提問工具的宿主上，把懸而未決的問題重新提出來。

原因是結構性的：這兩段的輸入是**真實 session 的形狀**（工具呼叫、狀態行、待答問題各自是
獨立的 turn），而提示裡的逐字稿無論寫得多像，都是一段連續文字。合成材料再多也補不上這個差。

要關掉這個缺口，需要的是真實 session 逐字稿——這兩條路其中之一走錯的那種——收進
`evals/judged-cases.md`。素材出現前，讀 8–12 案的通過率時記得它涵蓋的範圍到哪裡為止。

---

## v1.4.0 — 計畫可執行度 (2026-07-28)

**Problem.** The existing `具體優先於抽象` guardrail only had a descriptive face — its
examples are all past-tense checkable facts. A plan-bearing input abstracts differently: a
**原則** ("分階段導入、控制風險") reads as content because it has a subject and a verb,
so it slips past a guard tuned to spot obviously-empty modifiers like「大幅」「全面」.

**Fix.** Extended the same guardrail bullet with a prescriptive face: when the material is a
plan, the concrete form is a **做法** — who does what, and what counts as done. Added a
tie-break sentence against the pre-existing `representative-concrete` rule (fold lists of
>3 items into a theme clause), because a plan's moves are what the reader is waiting on, not
evidence to fold away — without the tie-break the two rules would collide head-on on any
plan with more than 3 action items.

**Placement decision.** Considered a separate `## Explaining a plan` section (more room to
define shape) versus extending the existing guardrail bullet (single source of truth for
the abstraction axis). Chose the extension — 原則 is a face of the same abstraction problem
具體 already owns, not a new mode.

**Eval design took two iterations to get right — this is the useful lesson for next time.**
The first version of eval case 5 used a 3-move plan. This looked reasonable but was a design
flaw: 3 items sits at/below the pre-existing `representative-concrete` rule's own trigger
threshold ("more than ~3 things"), so baseline was never actually at risk of folding it —
the case couldn't discriminate between versions no matter how the rule was written. The A/B
on that version came back a near-tie (v1.4.0 3/4, v1.3.0 4/4 across 4 reps/arm), which read
at first like the new rule might be a no-op per `engineering-guidelines.md`'s own standard
("a rule that doesn't measurably change behavior shouldn't ship").

Rather than ship on a shrug or revert on a shrug, redesigned the case to 4 moves —
deliberately past the folding threshold — before deciding either way. That version produced
a clean, reproducible result: v1.4.0 kept all 4 actions with their numbers in 2/2 reps;
v1.3.0 baseline independently stripped 3 of 4 numbers into vague thematic language
("拉到三倍" instead of stating 10→30, etc.) in 2/2 reps. Full log:
`evals/results-2026-07-28-plan-concreteness.md`.

**Takeaway for future rule additions to this skill:** when a new rule is meant to override
an existing threshold-based rule (here, the >3-item fold), the eval case must sit clearly on
the far side of that threshold, not at its boundary — otherwise a near-tie A/B result is
uninformative rather than reassuring.

**Not changed:** `description`/trigger surface (verified byte-identical except `version:`),
`catalog.md` (the new rule refines an existing highlight rather than adding scope),
`trigger-queries.json`.

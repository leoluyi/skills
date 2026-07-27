# plain-speak v1.4.0 A/B — 計畫可執行度 rule

Date: 2026-07-28. Change under test: v1.3.0 → v1.4.0, adding the 原則/做法 prescriptive-face
rule to the `具體優先於抽象` guardrail, a `計畫可執行度` review checklist item, and 3 new
eval cases (5, 6, 7). Rewrite agents: `general-purpose` subagents on this session's model.
Judge: separate `general-purpose` subagent, `model: opus`, blind arm labels, skill not loaded.

**Contamination disclosure.** I authored both the rule and the eval cases in this same
session, so a green result supports "no regression + the new face is covered" — never an
independent claim of objective superiority. The judge agent did not know which labels
mapped to which skill version.

## Round 1 — cases 1-4 (existing suite), full 7-case sweep, 2 reps/arm

Baseline extracted via `git show HEAD:skills/plain-speak/SKILL.md` (v1.3.0) before any edit
in this branch. 4 independent generation runs (v1.4.0 × 2 reps, v1.3.0 × 2 reps), blind-judged
against all 7 cases' expectations.

| Case | v1.4.0 rep1 | v1.4.0 rep2 | v1.3.0 rep1 | v1.3.0 rep2 |
|---|---|---|---|---|
| 1 | PASS | PASS | PASS | PASS |
| 2 | PASS | PASS | PASS | PASS |
| 3 | PASS | PASS | PASS | PASS |
| 4 | PASS | PASS | PASS | PASS |
| 5 (orig., 3 moves) | PASS | FAIL | PASS | PASS |
| 6 | PASS | PASS | PASS | PASS |
| 7 | PASS | PASS | PASS | PASS |

Cases 1-4: clean tie, no regression on the pre-existing guardrail (descriptive-concreteness
collapse from step 1(a) did not weaken behavior). Cases 6 and 7: clean tie both directions —
the model's general capacity already handles a pure-原則 plan and a plan-free definitional
prompt correctly even without the new rule; these two remain valuable as regression guards,
not as differentiators.

**Case 5 (original, 3 moves) was flawed as designed** — it names only 3 concrete actions,
which sits at or below the pre-existing `representative-concrete` rule's own trigger
threshold ("when the source itemizes more than ~3 things"). So even v1.3.0 baseline was
never going to fold it, and the one v1.4.0 rep2 FAIL looked like ordinary sampling noise
rather than a rule-caused regression. Ran 4 more reps per arm on the original 3-move prompt
to check: v1.4.0 settled at 3/4 pass, v1.3.0 at 4/4 pass — a genuine near-tie, but not
evidence the new rule does anything. This matters: `engineering-guidelines.md`'s own
standard says a rule that doesn't measurably change behavior is a no-op and shouldn't ship.

## Round 2 — case 5 redesigned (4 moves), the real tie-break test

Revised eval case 5's prompt to add a 4th concrete action (`connection pool 從 50 開到
120`), deliberately pushing the plan past the >3-item threshold that the pre-existing
`representative-concrete` rule is built to fold. This is the actual scenario the new rule's
tie-break sentence exists for. 2 reps per arm, analyzed directly (not via a separate judge
subagent — the divergence was unambiguous on direct read, see below; disclosed here as a
scope limit).

| Rep | v1.4.0 | v1.3.0 baseline |
|---|---|---|
| 1 | All 4 moves kept, every number intact (10→30, 09:50/5台, 80%→65%, 50→120), bulleted | 3 of 4 numbers stripped: `拉到三倍`(no 10→30), `好幾台備用機器`(no 5台/09:50), `負載還沒到滿水位就先提醒`(no 65%), `一併加大`(no 50→120). Only the first move partially kept a number. |
| 2 | All 4 moves kept, every number intact, bulleted | Same failure pattern: only 1 of 4 numbers kept (`10 台放寬到 30 台`), the other 3 folded into `一批備用機器`, `調得更敏感`, `撐更多連線` |

**v1.4.0: 2/2 clean. v1.3.0 baseline: 0/2 clean** — both baseline reps independently
collapsed 3 of the 4 concrete actions into vague thematic language, deleting the exact
numbers a reader would be waiting on. This reproduces cleanly across both reps and directly
confirms the predicted failure mode: without the tie-break, a plan with >3 items gets routed
through the old evidence-folding rule and loses its action items.

## Trigger-layer regression check

`tools/run-eval plain-speak` errored uniformly with "no parseable decision from claude" —
confirmed as a pre-existing environmental issue (the nested `claude -p` subprocess doesn't
parse cleanly from inside this session), not caused by this change: reran against an
untouched skill (`avoid-china-writing`) and got the identical error shape. Relied instead on
a direct diff: the `description:` frontmatter block is byte-identical between v1.3.0 and
v1.4.0 except the `version:` line, so the trigger surface is provably untouched.

## Ship gate

- Cases 1-4: tied, no regression. **Met.**
- Case 6, 7: tied, both correct in both versions (regression guards, working). **Met.**
- Case 5 (redesigned, the case that actually exercises the new rule): v1.4.0 strictly beats
  baseline, 2/2 vs 0/2, reproduced across both reps with a consistent, legible failure
  pattern in the loser. **Met — this is the decisive result.**

**Decision: ship v1.4.0.**

## Scope limits

- Round 2's 2 reps were read directly rather than run through a separate blind-judge
  subagent, given the divergence (numbers present vs. absent) was unambiguous on inspection
  and given cost constraints on this run. If this is revisited, a formal blind-judge pass on
  a larger Round-2 sample would strengthen the claim further.
- No FP regression sweep of cases 1-4 beyond the 2 reps/arm in Round 1.
- Trigger-layer (`tools/run-eval`) could not be run end-to-end due to a pre-existing
  environmental issue unrelated to this change; relied on frontmatter diff instead.
- Judge model family: both the Round 1 judge and the generation agents ran on this session's
  Claude model family (no cross-vendor judge was available in this environment), so "judge
  from another model family" per the repo's protocol was not literally satisfied — mitigated
  by using a separate `opus`-tier agent with no visibility into which label was which version.

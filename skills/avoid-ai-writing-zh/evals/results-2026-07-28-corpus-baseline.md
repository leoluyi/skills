# Regression run — 2026-07-28 (frozen baseline for refactor A/B)

**Type:** frozen reference baseline, not a pre-ship dual run. This run exists
because the language-prep round (backlog step 0+1: corpus + evals fixes) just
grew `evals.json` from 12 cases (the state on `main` going into this round —
not the stale 9-case/27-expectation figure from the 2026-07-21 run, which
predates the four-character-appraisal cases added 2026-07-28) to 54 cases —
ids 1–12 pre-existing (with ids 1/2/4's answer-leaking parentheticals
removed), ids 13–14 new voice-neutral false-positive cases, ids 15–54 ported
from speak-human-tw's `evals/benchmark.md` (MIT, adapted with attribution;
SF-14/SF-15 excluded — filed to `avoid-china-writing`'s backlog instead).
No rule change has landed — `SKILL.md`/`references/` are byte-identical to
`main` (verified via `git diff main -- skills/avoid-ai-writing-zh/SKILL.md`
before this run). **This result supersedes the 2026-07-21 9/9 run**, which was
measured against the pre-fix prompts for ids 1/2/4 (answers embedded in the
prompt text) and is void.

**Purpose.** This is the frozen "before" snapshot the refactor branch
(`refactor/avoid-ai-writing-zh`) will A/B against once step 3 rewrites
`SKILL.md`. Per backlog: the refactor must beat this number, not just be
shorter.

**Method.** Six independent runner agents (Claude, general-purpose), each
reading `SKILL.md` + all of `references/` fresh, processed disjoint id ranges
(1–9, 10–19, 20–29, 30–39, 40–49, 50–54) against the current unmodified
`SKILL.md`. Six independent grader agents (Claude, general-purpose, no access
to the runner's reasoning beyond its pasted output) then graded each chunk
against `evals.json`'s `expected_output`/`expectations`, applying
`regression-protocol.md`'s per-expectation ✅/❌ standard, the three global
rewrite-mode checks (保真／不換湯／不代筆) on rewrite-mode cases, and the
保護類 zero-tolerance / 命中類 no-regression distinction. **This is same-family
(all Claude) and same-session — contaminated per repo test-discipline
convention, same caveat as the 2026-07-21 run. Treat as a regression guard and
reference point, not out-shipping evidence** — the actual step-4 A/B against
the refactored branch should follow the full dual-blind cross-family protocol
in `regression-protocol.md`.

## Result

**87 / 88 expectations pass. 0 protection-class (保護類) failures. 1 hit-class
(命中類) miss.**

**How 88 reconciles with `evals.json`'s raw `expectations` arrays (this wasn't
obvious on review — spelling it out so the number is reproducible without
re-reading every grader transcript):** `jq` over the committed file gives
**79** raw array entries across all 54 cases (28 for ids 1–9, 16/10/10/10/5 for
the rest — verified independently with a one-line Python sum, not just by
eye). That 79 is not the graded total, for two reasons that cut in opposite
directions:

- **−3**: ids 1/2/4 each carry one `ground-truth-note` entry (added when this
  round fixed their answer-leaking prompts, task 6) — these are grader-only
  context ("this text has no AI-isms," "the profile declares these features"),
  not a checkable output claim, so all three graders correctly excluded them
  from the table rather than grading them as automatic passes.
- **+12**: `regression-protocol.md` mandates three global rewrite-mode checks
  (保真／不換湯／不代筆) on every rewrite-mode case, in addition to whatever
  `expectations` lists. Four cases in ids 1–9 are rewrite-mode (ids 2, 6, 8, 9)
  → 4 × 3 = 12 graded rows that exist by protocol, not in the JSON array.

`79 − 3 + 12 = 88`. All 12 of the +12 rows landed in the ids 1–9 chunk (the
only chunk with rewrite-mode cases — ids 15–54 are all ported as detect-mode
prompts, ids 10–14 are also detect-only), which is why that row alone shows
37 graded items against 28 raw array entries and every other row's graded
count matches its raw `jq` count exactly.

| id range | bucket | raw `expectations` (jq) | graded (± ground-truth-notes, ± global checks) | ✅ | ❌ |
|---|---|---|---|---|---|
| 1–9 | pre-existing | 28 | 37 (28 − 3 notes + 12 global) | 37 | 0 |
| 10–19 | pre-existing (10–12) + SNF (13–14) + SF (15–19) | 16 | 16 | 15 | 1 |
| 20–29 | SF | 10 | 10 | 10 | 0 |
| 30–39 | SF | 10 | 10 | 10 | 0 |
| 40–49 | SNF | 10 | 10 | 10 | 0 |
| 50–54 | SNF | 5 | 5 | 5 | 0 |
| **total** | | **79** | **88** | **87** | **1** |

### The one failure — id 18 (命中類, not shipping-blocking but a real finding)

Case 18 (speak-human-tw SF-04, 否定平行結構堆疊／刻意換詞循環 paragraph with
three stacked 不是…而是… instances) expects the third instance to also be
reduced — at most one 不是…而是… survives per paragraph. The runner instead
invented an unsupported "named-contrast carve-out" to leave the third instance
unflagged (misapplying the English "real/actual" adjective-inflation carve-out,
a different rule, onto Contrarian structure), and its own illustrative rewrite
still contains two negation-pivot constructions rather than collapsing to ≤1.

**Disposition:** not a SKILL.md defect confirmed yet — this is one agent's
single run, not a repeated pattern. Log as a watch item for step 3: if the
refactored rule text still produces this confusion (borrowing a carve-out from
an unrelated rule), tighten the Contrarian structure carve-out's wording to
name explicitly which carve-out it is, and cross-reference it directly rather
than leaving `real/actual adjective inflation` and `一次到位` under similarly-
worded headings a model can conflate.

### Case 35 (long-form SF-23 bounded) — clean pass, called out because it's the hardest case in the set

Verified the runner's S1–S5 span split against the eval's own expected split
(SF-23 originally names 第二句與第四句 as the empty-talk sentences): exact
match. All three axes checked separately by the grader — no fabrication, exact
identification of the two empty sentences, verbatim preservation of the data
sentence (31%→24%) and the action sentence (改回週五＋A/B測試) confirmed. This
is the case most likely to regress under a careless refactor (it's the one
place 保真 and detection have to cooperate across a whole paragraph), so it's
worth re-running by hand after step 3's rewrite even if the aggregate score
looks fine.

### Cases 50/51/54 — passed, but the runner's own rule-attribution was imprecise

Grader flagged (without penalizing the verdict) that:
- id 50: runner called the mention-vs-use protection a "self-reference escape
  hatch" — no such named rule exists; this is an undocumented gap per the
  case's own `對應規則` field, not a codified mechanism. Verdict (pass) still
  correct.
- id 51: runner cited "口號式短句 carve-out," which is actually the label for
  a different case; id 51's own `對應規則` is Scope ladder / narrative-rhythm
  carve-out. Substance correct, label borrowed from the wrong case.
- id 54: runner correctly notes the skill has no 罐頭式反應鏡頭 rule at all —
  which means this case currently passes **vacuously**. There is no mechanism
  in the skill capable of misfiring on "我愣了一下"-style reaction beats yet,
  so the pass proves nothing about how a future rule would behave. Per the
  repo's 命中／保護成對 convention, this SNF case is a placeholder for the
  paired SF-27 rule (also currently unimplemented, see `design-notes.md`'s
  step-3-inputs section) — **re-run this case for real once 罐頭式反應鏡頭
  detection is added in step 3.**

## Disposition

No rule or case changes made in response to this run — its purpose is to
freeze a number, not to fix one. The id-18 rule-conflation and the id-50/51
label imprecision are recorded here as step-3 watch items, not backlog defects
against the current (unchanged) `SKILL.md`.

**Verification-gate review (same day, before shipping this round).** Two
independent review passes over the whole diff surfaced four real issues that
got fixed before commit, none of which change the 87/88 number above:
(1) `tools/run-eval`'s `claude` branch had merged stderr into the parsed
TRIGGER/NONE channel, which both reviewers reproduced as a silent fabricated
PASS on CLI failure — fixed by routing stderr to its own file and adding
word-boundary matching; (2) the same diagnostic printed unredacted API-key
material and raw terminal-control bytes to stderr — fixed with redaction and
control-byte stripping; (3) `corpus.md`'s stated 7-category taxonomy turned out
to have an 8th real category (打破第四面牆／對讀者說教) once actual case
tagging exposed it, plus one double-counted row (H-20) — both fixed in
`corpus.md`, and this is exactly the kind of taxonomy-validation finding this
round was for, not a defect; (4) all 12 AI-bucket cases were missing the
schema's `預期方向` field — added.

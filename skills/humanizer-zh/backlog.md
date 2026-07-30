# humanizer-zh backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md) — except
`tools/annotate` below, which only this skill's material calls for. Several items below are
blocked on `tools/run-case` there.

Closed items do not stay here — see `design-notes.md`, `evals/results-*.md`, and commits.

## Blocking: 2.0.0 has an unmeasured fix on it

- [ ] **Re-run `evals.json` against the current branch.** The last full measurement is
  `evals/results-2026-07-30-evals54-v2.md`: **83/88, two protection-class reds**, which failed
  the ship gate (`regression-protocol.md` makes 保護類誤殺 0 absolute, not comparative) and
  sent `main` back to 1.5.0. Two behaviour-bearing commits have landed since, and **neither has
  been measured**:
  - `958cd44` gates carve-out rulings on quotable evidence — the intended fix for the two reds.
    Root cause was one mechanism, not two: co-locating carve-outs beside their rules (which is
    what fixed 1.5.0's anti-co-location defect and drove a clean 25/25 on protection-only
    cases) also made carve-outs more available at judgment time, so they spared hit-class text
    and, on ids 6/7, misfired on protected text.
  - `be5a09d` renamed 結構級訊號 → 作者隱身 and settled the genre gate: the flag became
    `--expect-author` and now *sets* the genre verdict instead of bypassing the gate, ids 13/14
    dropped the flag so they test the gate default, and **ids 55/56 were added** — so the
    denominator is no longer 88 and the 83/88 and 87/88 numbers are both stale as bars.
  Until this run exists, the branch has no score. Do it before any further rule edits.

  The five reds that run has to clear, each confirmed by two independent graders at two
  strictness levels: **id 6** 保護 不代筆 (flags an under-delivered claim, then writes the
  missing specification itself, while the same output tells the adjacent paragraph 「本 skill
  不代筆補寫」), **id 7** 保護 (double-flags 「範圍是開放的，不是固定的」, the exact false
  positive the case protects against), **id 5** 命中 (no person-shift fix offered), **id 36**
  命中 (argues the table form is fine rather than collapsing two rows to prose), **id 38** 命中
  (that run's runner promoted a 「今天，我想跟大家分享」 preamble into the protection list against
  the *old* key, which called that a miss — but the key was itself wrong, per the ported-case
  item below; the runner's call was closer to right, and against the fixed key this is no longer
  expected to be a red).

## The instrument is not a clean bar either

Both of these change the key, so both force a re-baseline of **both** versions. Sequence them
against the run above rather than interleaving.

- [ ] **The remaining ~36 ported speak-human-tw cases (ids 15/16, 18–20, 22–27, 29–37, 39–54) are
  still unadjudicated and may hold more taste mismatches with this repo's judgment.** Four cases from
  the same batch were adjudicated 2026-07-30 and landed this round: **id 17** (「業界專家普遍認為」
  -shaped sentence ruled no-AI-味 twice — blind, then again after being shown `模糊歸屬`'s own
  rule text — retired from the scored suite since flipping it would contradict the rule's own
  `抓` example; rule text unchanged this round), **id 21** (粗體標籤＋條列形式 — list form itself
  isn't the defect, key narrowed to the label-restatement formula that actually is), **id 28**
  (single 解說導引腔 instance — inside the rule's own density carve-out, flipped to
  protection-class; new id 57 added so the rule keeps hit-side coverage), **id 38** (第二句
  「今天，我想跟大家分享我使用 AI 改稿的三個心得」 是正常開場 — key split so only the 時代大帽子
  first sentence stays flagged; `corpus.md`'s A-08 annotation reconciled on the same
  referent-based reasoning). All four verdicts, with the reasoning that produced them, are now
  in [`evals/judged-cases.md`](evals/judged-cases.md) — closing the hand-transcription gap this
  item used to note.

  **Resume at ids 15/16, 18** — that is where the sweep stalled (PR #20) before finding these
  four. Two cases from the same source batch were deliberately *not* ported here because they
  test the 陸用語／簡體殘留 axis; they are tracked in
  [`skills/avoid-china-writing/backlog.md`](../avoid-china-writing/backlog.md), and neither side
  blocks the other.

- [ ] **`模糊歸屬` may be scoped too wide — id 17's adjudication found it catching a defect
  ordinary human writers also commit, not just an AI tell.** The author ruled a 「業界專家普遍認為」
  -shaped sentence has no AI 味, in isolation, even after being shown the rule's own 抓／保留 text
  (`references/zh-rules.md:218-222`) — reasoning 「規則本身抓得太寬」「是一般人類文章也可能犯的錯誤」；
  full record in [`evals/judged-cases.md`](evals/judged-cases.md). Explicitly scoped to that one
  case by the author, not a mandate to change the rule now — but the shape is worth naming:
  `解說導引腔` already has a density carve-out (a single instance doesn't count, only stacking
  does — `references/zh-rules.md:58-63`); `模糊歸屬` has no isolated-instance equivalent. Whether
  it needs one — and whether other rules share the gap — is a behaviour change and needs its own
  branch and re-run, not a fold-in to a key-fix round. `corpus.md`'s A-06 (`:789`) is the
  distinguishing datapoint already on record: the same 模糊歸屬 pattern there co-occurs with
  `對比句式` and a 「值得深思的現象」 framing sentence, and stays flagged — so any fix is about
  isolation, not about weakening the rule wholesale.

- [ ] **`口語化萬能詞`'s new 名詞與短語 form needs eval coverage on both sides.** The rule was
  widened 2026-07-30 from 口語化萬能動詞 to cover 比喻/slang standing where the
  generally-understood term belongs (「兩條路」→「兩個方式」; ruling in `evals/judged-cases.md`).
  Nothing measures it yet:
  - **Hit case** — id 7's 「兩條路」 is the adjudicated example but is not in that case's key.
  - **Protection case** — this is the one that matters. Widening a catch from verbs to nouns
    and phrases puts every figurative noun in range, so a register that legitimately carries
    figuration must be shown to survive: `casual` voice, and a 署名文體 draft whose metaphor
    system is declared under 保護清單⑥. The two carve-outs written for it (已成通用術語的比喻;
    宣告過的比喻系統) are untested prose until a case fires at them.
  Until both exist, treat the widening as unverified — it is the kind of change that buys one
  hit and pays for it in false positives nobody measured.

- [ ] **Three structural defects in `evals.json`.** Found by the 2026-07-30 54-case run; the
  instrument was left frozen that round so the skill fix stayed comparable to the baseline.
  (1) **Hit-class and protection-class cases are partitioned into separate id ranges** — c3 is
  all-hit, c5/c6 all-protection — so no chunk tests both directions on the same material, and a
  degenerate runner that flags nothing scores 25/25 on c5+c6. (2) **Several detect-mode cases
  carry rewrite-phrased expectations** (「改成」「全清」「刪掉」) that cannot be checked literally
  against a detect output, forcing graders onto the softer "did the report point this way" bar.
  (3) **Single `expected-direction` slugs bundle 2–3 independent requirements** (id 34 wants
  prose-ification *and* concrete detail), so binary scoring reads "half done" as a full miss.
  id 38 had the same shape (two independent deletions in one slug) and was split into separate
  `expectations` entries during the 2026-07-30 key-fix round (see `evals/judged-cases.md`).
  id 21 was fixed in the same round but is a different defect, not this one — its old key's
  demand was substantively wrong (asked for prose-collapse, which is the wrong rule's remedy),
  not merely bundled; the fix rewrote the direction rather than decomposing it. The remaining
  unadjudicated ported cases may hold more of either shape.

- [ ] **`corpus.md` is saturated — it detects regressions, it does not measure progress.**
  1.5.0 scores 89/89 on it (52/52 protection, 37/37 hits) and 2.0.0 matches at 89/89. Keep
  running it as a guard, but stop reading a flat 89/89 as evidence of anything. New,
  unsaturated material is what any future "we are better" claim needs.

- [ ] **The English side's evidence is not independent.** Three before/after pairs in
  `references/en-rules.md` were written while looking at corpus gold fragments (the
  post-regression patch), so the English hits they produce are recognition, not derivation.
  Same shape as **id 51**, whose pass may be recognition too — the runner justified its
  carve-out by citing a rule example that is near-verbatim the test input. Replace both with
  synthetic material once new, unused English cases exist. Related: no **cross-family judge**
  was reachable in the 2.0.0 round, so its result supports "no regression detected", never
  "we are better".

- [ ] **A 保真 case for colloquial time expressions in rewrite mode.** In the 2026-07-30 run,
  id 40's runner normalised 「3/31 晚上 11:59」 to 「3/31 23:59」 inside its own report. Harmless
  in detect mode (the text was untouched and the verdict stood), but the identical reflex in
  rewrite mode is a 保真 failure, and nothing currently tests for it.

## Tooling the adjudication needs

- [ ] **`tools/annotate` — yes/no adjudication helper for eval cases.** Wanted 2026-07-30,
  straight out of the session that found it. When a run disagrees with the key, the fastest
  way to settle it turned out not to be reading rule text — it was showing the author the raw
  sentence and asking 「這句有沒有 AI 味？」 with two buttons. Four such questions overturned
  three cases in one round, where two rounds of rule-wording argument had settled nothing.
  The tool should: pull a case's quoted span out of `evals.json`, present span + genre + one
  line of context (never the expectation, never the rule name — those bias the answer), take
  有/沒有, and write the verdict plus a one-line rationale into `evals/judged-cases.md` as
  品味層 語料, flagging any case whose verdict now contradicts its `expected-direction`. Runs
  over a filtered set (a whole id range, or only cases that failed a given run). Dev-side,
  `uv` fine, never part of skill runtime. The immediate consumer is the ported-case sweep
  above — resuming it at ids 15/16, 18 by hand is the same transcription tax a second time.

## Behaviour changes, each on its own branch and its own re-run

- [ ] **Make `detect` the default mode, and ask before rewriting.** Requested 2026-07-30. Today
  `rewrite` is the default and the skill edits text without being asked twice; the wanted
  behaviour is detect-first — run the audit, report findings grouped P0/P1/P2, then ask whether
  to rewrite whenever the finding list is non-empty (a clean draft reports clean and asks
  nothing). Explicit `rewrite`/`--mode` requests must keep winning, or the eval prompts stop
  testing what they say they test. Held out of the carve-out-gate branch deliberately: the mode
  switch changes which cases exercise rewrite paths at all, and the three global rewrite checks
  (保真／不換湯／不代筆) currently ride on the four rewrite-mode cases in chunk 1 (ids 2, 6, 8, 9).

- [ ] **進階補完模式 — close the smallest holes by asking, never by writing.** Wanted
  2026-07-30. Today the skill is pure subtraction, and `docs/humanizer-zh.md` says so twice:
  「它只拿掉不該有的，加不進來的東西留給你」 and 「`作者隱身` 只報不改」. That is the right default
  and stays the default — but it leaves the author holding a report full of 「此段扣除語氣後無實質
  內容」 with no path forward inside the tool. The wanted mode closes the *smallest* of those
  holes by **asking**, not by composing: for each hollow span, put the question to the author as
  options they can pick rather than prose they must write (「這段想講的是 (a) 成本 (b) 相容性
  (c) 交期？」 → 「數字是多少？」), then splice the answer in at the minimum length that makes the
  sentence carry information. **The line this must not cross:** every fact in the output came
  from the author's answer, never from the model's guess — that is the only thing separating
  this from the ghostwriting the skill exists to prevent, and the thing an implementer under
  pressure will erode first. Explicitly out of scope: 大範圍補洞. A draft that is hollow
  throughout does not get interviewed paragraph by paragraph; it gets handed back with the
  report it already gets today, because at that volume the Q&A is just a slower way to have the
  model write the piece. Sequencing: needs the detect-default change above to land first (it
  only makes sense as a step *after* a report the author has read), and needs its own eval cases
  — the existing 保真 checks all assume output ⊆ input, which stops being true here. Design
  question to settle before building: whether spliced-in text is marked in the output so the
  author can see what came from their own answers.

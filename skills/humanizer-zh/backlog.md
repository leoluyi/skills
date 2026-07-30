# humanizer-zh backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md). Several
items below are blocked on `tools/run-case` there.

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
  (promotes a 「今天，我想跟大家分享」 preamble into the protection list — but see the ported-case
  item below, which says id 38's key is itself wrong).

## The instrument is not a clean bar either

Both of these change the key, so both force a re-baseline of **both** versions. Sequence them
against the run above rather than interleaving.

- [ ] **The 40 ported speak-human-tw cases (ids 15–54) encode another project's taste, and at
  least three contradict this repo's.** Adjudicated 2026-07-30 by the author with yes/no
  questions on the raw sentences: **id 21** (粗體標籤＋條列形式 — 「條列形式本身沒問題」, so the
  case's 「能一段散文講完就用散文」 direction is too strong), **id 28** (單一次解說導引腔 —
  「偶一為之不算」, vindicating the density carve-out the case contradicts), **id 38**
  (「今天，我想跟大家分享我使用 AI 改稿的三個心得。」 — 「這是正常開場」, so it should not be cut
  alongside the 時代大帽子 first sentence). In all three the skill was right and the case was
  wrong. Consequence: **1.5.0's 87/88 is partly earned by flagging text the author considers
  fine.** A fourth case, **id 17**, was adjudicated in the same session without landing in
  that group — per PR #20 the skill was right in three of four, so id 17 is the one that went
  the other way; recover the actual verdict before relying on it either way.

  Two loose ends the sweep left:
  - **Resume at ids 15/16/17** — that is where the sweep stalled (PR #20). The remaining ~37
    ported cases are unadjudicated and may hold more of the same.
  - **None of the four verdicts are in `evals/judged-cases.md`.** That file holds two cases,
    neither of them these, so the only record is prose in this backlog and in PR #20 — exactly
    the hand-transcription problem `tools/annotate` exists to remove. Writing them into
    `judged-cases.md` is part of closing this item, not a follow-up.

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
  prose-ification *and* concrete detail; id 38 wants two separate deletions), so binary scoring
  reads "half done" as a full miss.

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

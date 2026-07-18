# A/B read rules — v0.10.1 vs v0.9.1 (pre-registered)

Frozen **before** any generation runs. The point of freezing is to stop
results being narrated into progress after the fact: the interpretation is
decided here, and the run either meets these thresholds or it does not.

> **Status.** The full 54-generation run (below) was **aborted on cost** when
> the host process exited mid-run — only 3 of 72 agents were cached, and their
> verdicts were never inspected. It is replaced by the reduced re-registration
> in **Amendment v2**, decided while still blind to every result. The rules
> below stand as the ideal design; v2 is what actually ran.

## Arms

- **Control** = `../snapshot-v0.9.1` (frozen v0.9.1 skill tree, still says
  `base position`).
- **Treatment** = the working tree at v0.10.1 (nine `Done when` clauses +
  `home` leading word).

Arms run as independent parallel subagents and are mutually blind. Generators
never see the expectation list (no teaching-to-test); scoring is done by a
separate agent that never sees which arm produced an artifact.

## Design

- **All nine `evals.json` questions run.** The full sweep exists to catch
  **regression**, not to hunt improvement.
- **Three runs per (question × arm)** — 9 × 2 × 3 = 54 generations. Triplicate
  because there is no established noise floor yet; the three runs are what
  estimate within-group scatter.
- Each artifact is scored pass/fail against every expectation for its
  question. Objective expectations (overflow, contrast, tiny fonts) are
  verified with `scripts/check.py`; structural ones by inspecting the SVG;
  density/semantic ones by the blind scorer.

## Verdict rules

### Regression (blocking — fix, do not explain)

An expectation counts as a regression iff it passes **3/3 in control** and
fails **3/3 in treatment**. Any other pattern (a split arm, a pre-existing
failure) is scatter, not a regression. Regressions are fixed before v0.10.1
is considered validated; they are not rationalized.

### Improvement (only two questions, only some expectations)

Improvement is credited **only** on id-7 and id-9, and **only** on the
expectations `home` actually governs — the density decision and the declare
behaviour. Everything else is noise and stays out of the conclusion.

Eligible expectations (0-indexed within each question's `expectations`):

- **id-7 (OAuth flow):**
  - [0] each party in its own lane/column — *density*
  - [1] at least one arrow crosses between parties — *density*
  - [2] payload labelled on the arrow itself — *density*
  - (excluded: [3] numbered order = sequence; [4] no overflow = craft floor)
- **id-9 (TLS handshake):**
  - [0] each party its own lane, messages cross — *density*
  - [1] payload on the arrow itself — *density*
  - [3] key derivation drawn as converging inputs — *density (signature)*
  - [5] the response states the position it built at — *declare*
  - (excluded: [2] direction-without-colour = a11y; [4] one-name-per-token =
    words rule; [6] contrast, [7] overflow = craft floor)

An improvement counts iff, on an eligible expectation, control is **0/3** and
treatment is **3/3** — both arms internally stable, maximal separation. This
operationalizes "the old-vs-new gap must exceed the within-group scatter": if
either arm is split (1/3 or 2/3) the run-to-run scatter is the size of the
gap, so the result is declared noise regardless of direction.

The raw 3×2 tally for every eligible expectation is reported either way, so
the texture is visible; only the 0/3→3/3 cells enter the conclusion.

## Out of scope

Description/trigger routing is not tested here (that is `tools/run-eval` over
`trigger-queries.json`). This protocol covers generated-artifact quality only.

## Amendment v2 — reduced re-registration (what actually ran)

Registered before v2 results exist, blind to the 3 aborted-run agents. Motive
is cost, not outcome: the design is trimmed on the axes that cost the most
runs while preserving the two things this A/B is *for* — the improvement test
on `home`, and a regression check on the objective/structural expectations
most likely to break.

**Cells:**

- **id-7 and id-9 — 3 runs × 2 arms.** Full triplicate kept: these carry the
  entire improvement question, and the 0/3→3/3 threshold needs three runs to
  mean anything. (12 generations, 4 scorers.)
- **id-3, id-4, id-6, id-8 — 2 runs × 2 arms.** Regression spot-check only.
  Chosen because they exercise the objective/structural expectations a prose
  edit could plausibly break: zero-baseline + no-3-D (id-3), proportional
  funnel + format-recommendation + overflow (id-4), contrast + colour-not-
  alone (id-6), variables + named groups + contrast (id-8). (16 generations,
  8 scorers.)

**Dropped from v2, stated so the gap is not silent:** id-1, id-2, id-5 get no
regression coverage this run. They are the lowest-risk questions (single-
finding hierarchy; hero-stat; "don't ask, deliver SVG") and none touch the
density/declare behaviour `home` governs. A regression there would go
uncaught until the next full run.

**Verdict rules (amended for the mixed run depth):**

- **Regression, 3-run cells (id-7, id-9):** unchanged — 3/3 control pass and
  3/3 treatment fail.
- **Regression, 2-run cells (id-3, id-4, id-6, id-8):** 2/2 control pass and
  2/2 treatment fail. Weaker (a 2/2 stable state is a coarser noise floor),
  so it catches only hard breaks; flagged as such.
- **Improvement:** unchanged from the original — credited only on the id-7 /
  id-9 eligible expectations at control 0/3 → treatment 3/3. No 2-run cell is
  improvement-eligible.

## Amendment v3 — 6-agent Haiku smoke test (what finally ran)

Both prior designs (v1 54-gen, v2 40-gen) died when the host process exited
mid-run; neither produced inspected verdicts. Registered blind to all prior
results. This is a **smoke test, not an A/B** — power is deliberately spent
down to fit ≤6 agents on the cheapest model.

- **id-9 only, 2 arms × 2 runs, Haiku.** 4 generations + 2 scorers = 6 agents.
  id-9 chosen because it alone carries every behaviour `home` governs —
  density [0,1,3] and the declare expectation [5].
- **Improvement:** control 0/2 → treatment 2/2 on eligible [0,1,3,5]. This is
  a weaker bar than 0/3→3/3 and is labelled as such.
- **Regression:** control 2/2 pass & treatment 2/2 fail on any expectation.

**Trust caveat (binding on the read).** On Haiku both arms are expected to
fail id-9's hard expectations from floor effects, so the likely result is *no
signal*. Per the eval-integrity rule, only a **negative finding** (treatment
breaks what control reliably did) is trustworthy from a run this small on a
weak model; a positive improvement at n=2 is suggestive, not established.

## Results

**No valid A/B was obtained. All three attempts failed before producing a
trustworthy comparison.**

- **v1 (54 agents)** and **v2 (40 agents)** — both died when the host process
  exited mid-run; only a handful of agents journaled, no inspected verdicts.
- **v3 (6-agent Haiku smoke test)** — ran to mechanical completion (6/6
  agents, 0 errors) but is **invalid**: the journal shows **3 of the 4
  generation agents refused to generate**, having inherited the session's
  elevated-cost state ("I need to pause before continuing"; "Session cost is
  currently $77.93"). Only one generator produced an SVG. The scorer therefore
  saw "(no output produced)" for most cells and marked them FALSE. The raw
  tally (treatment 0/2 across every expectation, control 1/2 on most) measures
  which agents bailed on cost, **not** skill quality. Per the pre-registered
  trust caveat, nothing here is a usable signal — not the null, not the
  apparent treatment-worse pattern.

**Verdict against the frozen rules:** no regression established, no
improvement established, and the run is disqualified as contaminated. The
`home` / completion-condition changes in v0.10.1 therefore ship **empirically
unvalidated** — the "beat the previous version" bar was not tested, and this
is stated plainly rather than papered over.

**To validate later:** run the full v1 design (or the v2 reduction) in a
**fresh, low-cost session** so generation subagents do not refuse on cost, and
on a capable model (Sonnet+) so id-9's hard expectations are not floored. The
scripts are cached at the run IDs recorded in the commit history.

## v3 rerun — 2026-07-19, fresh session

Ran to mechanical completion this time: 4/4 generators produced SVGs (no cost
refusals), 2/2 blind scorers returned JSON verdicts. Still on Haiku, per the
v3 registration.

**Blinding:** each run's control/treatment pair was copied to
`artifact-A`/`artifact-B` before scoring; the scorer saw neither filenames nor
prompts that named an arm. Mapping: A = control (v0.9.1), B = treatment
(v0.10.1) in both runs — de-blinded only after both scorer verdicts were in.

**Raw tally (pass/2), id-9, all 8 expectations:**

| # | expectation | control | treatment |
|---|---|---|---|
| 0 | own lane, messages cross | 2/2 | 2/2 |
| 1 | payload labelled on arrow | 0/2 | 0/2 |
| 2 | direction w/o colour alone | 2/2 | 2/2 |
| 3 | key derivation drawn as converging paths | 2/2 | 0/2 |
| 4 | recurring token same name | 2/2 | 2/2 |
| 5 | response states dial position | 0/2 | 1/2 |
| 6 | contrast (check.py) | 0/2 | 2/2 |
| 7 | no overflow (check.py) | 1/2 | 2/2 |

**Improvement (eligible: [0],[1],[3],[5]):** no expectation cleared the
pre-registered 0/2→2/2 bar. [0] and [1] were already tied; [3] moved the
wrong direction (see regression below); [5] split 0/2→1/2, which the
pre-registered rule treats as noise, not signal. **No improvement
established** — the `home`/declare change did not demonstrate a detectable
effect at this power.

**Regression ([3]):** control 2/2 pass, treatment 2/2 fail — meets the v3
regression rule exactly. Verified independently of the scorer by grepping the
raw SVGs: both `control-*.svg` contain actual `<path class="derive-arrow">`
convergence geometry into the master-secret box; both `treatment-*.svg`
express the same fact only as a `<text>` caption, no converging paths. This
is not a scorer artifact.

**Caveat on causation.** Diffing `snapshot-v0.9.1/SKILL.md` against the
working tree shows the step-9 density check text is unchanged in substance
(`"base position actually dense (lanes, payloads, derivations)"` →
`"home actually dense (lanes, payloads, derivations)"` — a rename, not a
content change). Nothing in the v0.10.1 diff plausibly *causes* worse
key-derivation rendering. Per the pre-registered trust caveat this negative
finding is still the one thing this run is entitled to trust — but n=2 on
Haiku cannot distinguish "v0.10.1 broke this" from "this expectation is
inherently unstable and the 2/2-vs-2/2 split happened to land this way here."

**Verdict against the frozen rules:** one regression flagged on id-9
expectation [3], no improvement established. Per the v1 rule
("regressions are fixed before v0.10.1 is considered validated, not
rationalized") this technically blocks sign-off — but given the causation
caveat above, the recommended next step is a confirmatory run (more reps,
same expectation only) before touching SKILL.md, rather than editing the
skill against a signal this thin. Left as an open decision for the next
session; not resolved unilaterally here.

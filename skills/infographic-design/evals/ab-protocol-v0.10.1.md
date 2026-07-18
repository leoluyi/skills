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

## Results

(appended after the run)

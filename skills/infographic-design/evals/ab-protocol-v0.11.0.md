# A/B read rules — v0.11.0 vs v0.10.1 (pre-registered)

Frozen **before** any generation runs, per this repo's eval-integrity rule:
the interpretation is decided here, and the run either meets these
thresholds or it does not.

## What changed in v0.11.0

A semantics-preserving prose rewrite: ~35 negation tokens
(`never`/`not`/`no`/`don't`) in the SKILL.md body converted to positive
statements of the target behaviour. Three deliberate holdouts: the
frontmatter description (trigger surface — owned by the separate
trigger-corpus item), the step-6 data-honesty line (legitimate guardrails,
kept verbatim), and the AI-default-look calibration paragraph (its job is to
name the tells; only its incidental negations were softened).

Because the rewrite claims semantic equivalence, **the primary question is
regression, not improvement**: did converting a prohibition to a positive
statement silently weaken any behaviour the prohibitions used to enforce?

## Arms

- **Control** = v0.10.1, snapshot of `skills/infographic-design/` at git
  `14d6eda`, copied to an opaquely-named directory.
- **Treatment** = the working tree at v0.11.0, copied to a second
  opaquely-named directory.

Directory names are opaque (`snap-1041` = control, `snap-2917` = treatment;
mapping recorded here, invisible to agents). Generators never see the
expectation list. Scorers see artifacts under neutral A/B names and never
which arm produced them.

## Design

- **id-9 only (TLS 1.2 handshake), 2 arms × 2 runs = 4 generations.** id-9
  is chosen because it exercises the most rewritten surface: density
  (lanes/payloads/derivation — step 1 and 5 prose), the declare behaviour
  (step 1), colour-as-second-channel (step 8, rewritten), and the gate
  language (step 9, rewritten). Model: the session model (Sonnet-class);
  the prior v3 run showed Haiku floors id-9's hard expectations.
- Each generator reads its arm's skill tree cold and fulfills the id-9
  brief, saving the SVG plus its delivery message (expectation [5] is about
  the response text).
- **Scoring:** 2 blind scorers, one per run-pair, counterbalanced mapping
  (run 1: A = control, B = treatment; run 2: A = treatment, B = control),
  de-blinded only after both verdicts are in. Objective expectations [6]
  contrast and [7] overflow are additionally verified with
  `scripts/check.py` deterministically.

**Stated gap:** id-1 and id-3 get no coverage this run. id-3's guardrails
(zero-baseline, no 3-D) are the step-6 line kept verbatim, so the diff
cannot plausibly reach them; id-1's hierarchy rules were lightly touched
(step 4 lost only "not a topic label"). A regression there would go
uncaught until the next full sweep.

## Verdict rules

- **Regression (blocking — fix, do not explain):** any expectation where
  control passes 2/2 and treatment fails 2/2. At n=2 this catches only hard
  breaks and is flagged as coarse.
- **Improvement (suggestive only):** control 0/2 → treatment 2/2 on the
  v0.10.1-eligible expectations [0], [1], [3], [5]. At n=2 this is
  suggestive, never established; it does not enter the shipping decision.
- **Any split cell (1/2)** is scatter, reported but excluded from
  conclusions.
- **Confirmatory read on the open v0.10.1 flag:** the prior v3 rerun flagged
  expectation [3] (key derivation drawn as converging paths) as a possible
  v0.10.1 regression at n=2 on Haiku, with a causation caveat. Control in
  this run *is* v0.10.1 on a capable model, so its [3] tally is independent
  evidence: control 2/2 pass on [3] would suggest the Haiku result was a
  floor effect, not a real v0.10.1 break.

## Out of scope

Description/trigger routing (that is `tools/run-eval` over
`trigger-queries.json`, and the description is unchanged in v0.11.0 by
design). Generated-artifact quality on id-1/id-3.

## Results

*(appended after the run; empty at registration)*

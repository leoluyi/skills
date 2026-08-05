# The `results-2026-08-04-null-r*` series is superseded — stop here before dispatching r4

If you are about to run another `--baseline HEAD` probe round to extend this
series (`results-2026-08-04-null-r4.md`, `r5`, …): **don't.** The strategy
changed on 2026-08-05, mid-flight, on this same branch
(`fix/gate-null-calibrated`).

Read `/Users/leoluyi/.claude/plans/reflective-rolling-crescent.md` instead.
The old plan file (`fix-run-paired-same-call-pure-feigenbaum.md` in
`~/.claude/plans/`) now carries a superseding banner at its top with the full
delta; the project memory `project_gate_calibration_blocked.md` also points
here.

**What changed, in one line:** instead of re-dispatching a fresh
`--baseline HEAD` round per pool member (12 runner + 6 grader jobs each),
`tools/run_case/bank.py` (`--build-bank` / `--null-run`) builds a one-time
pool of independent baseline generations and pairs two of them inside a
single grader call with **zero runner dispatch** — same same-call structure
this series exists to produce, far fewer jobs.

`r1`–`r3` above are not wasted: they're valid same-text probe rounds under
the *old* chunk layout (6 chunks, codex effort `xhigh`). They cannot be
pooled with rounds run under the new layout (3 chunks, effort `high`) or with
`--null-run` output — `tools/run_case/aggregate.py`'s `IDENTITY_FIELDS` will
hard-error rather than let them mix silently. Keep them only as a reference
point if you want to sanity-check the new same-call numbers land in a similar
range; do not feed them to `--calibrate` alongside anything new.

Delete this file once the branch has moved past this decision (e.g. once
`calibration.json` has been regenerated under the new setup and this note
stops being live guidance).

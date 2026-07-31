# run-case aggregate — humanizer-zh — 3 rounds

- new arm: version 2.0.0, blob sha256 `1af7850c372d2440a27d2306154106eba050dd61a446db80634ab24197fefd3c`
- base arm: `520d5bb`, version 1.5.0, blob sha256 `98ba8ce7e8d516b3cb6c74564f5b28084e6589e2aba4bd766901a520b27a4dca`
- a protection row counts as confirmed at 2 of 3 rounds

## Rounds pooled

| # | source | run id |
|---|---|---|
| 1 | `results-2026-08-01-run-case-r8.json` | `1a6915c8f8fd4cbf883c241b9e8705d5` |
| 2 | `results-2026-08-01-run-case-r9.json` | `a063d571a57d4ddfaecfefb2cec148da` |
| 3 | `results-2026-08-01-run-case-r10.json` | `a2b633682e2f4a46bf108a82b932aa5a` |

## Failures per round

| class / arm | r1 | r2 | r3 | mean |
|---|---|---|---|---|
| 保護 new | 0 | 1 | 1 | 0.67 |
| 保護 base | 7 | 8 | 3 | 6.00 |
| 命中 new | 0 | 5 | 3 | 2.67 |
| 命中 base | 6 | 6 | 7 | 6.33 |

## Protection rows the new arm failed

| case | expectation | rounds failed | status |
|---|---|---|---|
| 9 | 全域:保真 | 1/3 | unconfirmed |
| 28 | no-single-instance-false-positive | 1/3 | unconfirmed |

Unconfirmed rows are the ones another round would settle: they failed once, which is what a defect and a bad draw look like alike.

## Gate

SHIP — no confirmed protection false kill; neither class's mean regressed against the baseline.

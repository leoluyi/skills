# Regression Protocol: deck-writer

Use this protocol to verify that a change improves complete content decks without rewarding unsupported detail or unnecessary process.

## Layers

| Layer | Asset | Run |
|---|---|---|
| Trigger | `trigger-queries.json` | `tools/run-eval deck-writer` |
| Behavior | `evals.json` | Independent with-skill and vanilla runs |
| Taste | Human review | Resolve whether the deck is persuasive, scannable, and faithful |

## Ship gates

Treat source fidelity and scope boundaries as protection-class expectations.
Any invented fact, altered supplied number, silent overwrite, or claim of producing a file that was not produced blocks shipment.

Treat deck structure, slide claims, artifact completeness, and language fit as hit-class expectations.
The skill arm must beat vanilla across the case set and must not regress any protection-class expectation.

## Pre-ship run

Launch independent agents in parallel.
One arm reads `SKILL.md`; the vanilla arm receives only the case prompt.
Repeat each arm at least twice with fresh context.

Give a blind judge only the prompt, expectations, and anonymized outputs.
Record per-expectation pass or fail with one sentence of evidence.
Human judgment breaks ties, especially when formal expectation counts hide a less useful argument.

Archive the comparison in `evals/results-<YYYY-MM-DD>.md` with model names, per-case results, and a disposition for each failure.

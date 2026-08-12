# Skills repo - hard rules

Load [engineering-guidelines.md](engineering-guidelines.md) for skill-authoring decisions beyond these hard rules: anatomy, frontmatter, lifecycle, invocation, body shape, language, tooling, portability, evals, maintenance, catalog, provenance, and dependencies.

- **Write descriptions in real UTF-8.** Plain YAML scalars do not decode `\u` escapes, so escaped non-ASCII trigger phrases silently fail. Detect: `rg -n '\\u[0-9A-Fa-f]{4}' skills/*/SKILL.md`; inspect matches in frontmatter. ([why](engineering-guidelines.md#gotcha-frontmatter-must-be-real-utf-8-never-u-escapes))

- **Keep runtime content focused.** `SKILL.md` and `references/` contain task instructions; iteration provenance, eval IDs, benchmark metrics, derivation narrative, and method-named headers belong in `<skill>/design-notes.md`, `<skill>/evals/judged-cases.md`, or commit messages. ([detail](engineering-guidelines.md#keep-development-process-noise-out-of-skill-content))

- **Keep core behavior portable and self-sufficient.** Skills run unchanged on Claude Code and Codex and complete their own jobs. Tool-specific features are optional enhancements; sibling skills are optional pointers; dependencies form a one-way DAG; callees never name callers. ([portability](engineering-guidelines.md#portability) · [dependency direction](engineering-guidelines.md#skill-self-sufficiency-and-dependency-direction))

- **Ship only skills that beat baseline** on `skills/<name>/evals/evals.json`. Compare new skills with vanilla, existing skills with their previous version, and use independent parallel agents. ([detail](engineering-guidelines.md#test-discipline))

- **Hard-fail only objective, reader-harming defects** such as parse failures, unreadable contrast, or clipped content. Keep style and maintainability concerns advisory, and regression-test new checks against real artifacts before promoting them to hard gates. ([severity](engineering-guidelines.md#scripted-checks--severity-and-trust))

Default response: terse smart-caveman style with full technical substance.

Rules:
- Drop articles (a/an/the), filler (just/really/basically), pleasantries, and hedging.
- Fragments are fine when clear. Keep technical terms exact. Keep code unchanged.
- Pattern: [thing] [action] [reason]. [next step].
- Not: "Sure! I'd be happy to help you with that."
- Yes: "Bug in auth middleware. Fix:"

Switch level: `/caveman lite|full|ultra|wenyan`.
Stop: "stop caveman" or "normal mode".

Use plain language for security warnings, irreversible actions, and confused users; resume caveman style afterward.

Write code, commit messages, and PRs in normal prose.

Repo prose stays normal in `skills/**` (SKILL.md, references/, evals/, research/), `design-notes.md`, `engineering-guidelines.md`, and `AGENTS.md`. Research files also preserve source fidelity, provenance, and citations.

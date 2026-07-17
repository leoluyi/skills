# Skills repo — hard rules

Forbidden directives for authoring skills here. Full authoring guide: **[DEVELOPMENT.md](DEVELOPMENT.md)**.

- **Never `\u`-escape a skill `description`.** YAML plain scalars don't decode `\u`, so escaped Chinese (or any non-ASCII) triggers silently never fire — the skill reads fine but won't load on those prompts. Write the description in real UTF-8. Detect: `rg -l '\\u[0-9A-F]{4}' skills/*/SKILL.md` — any hit on a `description:` line is the bug. ([why](DEVELOPMENT.md#gotcha-frontmatter-must-be-real-utf-8-never-u-escapes))

- **Never leave development-process noise in `SKILL.md` or `references/`.** No iteration provenance (`round 2 補強`, `eval #14`, FP/recall figures), no derivation narrative (`比對 A 與 B 後…`, `（benchmark 實證）`, `（補充樣本：…）`), no method-named headers. These files are runtime instructions — keep the insight, drop the derivation. Provenance lives in `<skill>/DEVELOPMENT.md`, `evals/<skill>/benchmark-protocol.md`, or commit messages. ([detail](DEVELOPMENT.md#keep-development-process-noise-out-of-skill-content))

- **Never let a skill's core behavior depend on a tool-specific feature or on another skill.** It must run unchanged on Claude Code *and* Codex — tool-only power (`hooks`, `context: fork`, `model`) may be present but never load-bearing — and it must complete its own job standalone. Sibling-skill mentions are optional pointers, never `run X first` prerequisites; dependencies stay one-directional (no cycles); a callee never names its callers. ([portability](DEVELOPMENT.md#portability) · [dependency direction](DEVELOPMENT.md#skill-self-sufficiency-and-dependency-direction))

- **Never ship a skill that doesn't beat vanilla** on its `evals/<name>/prompts.json` with-vs-without baselines. A skill that exists but doesn't help is worse than none — it eats context and pollutes the trigger surface. No bar-clearing, no skill. ([detail](DEVELOPMENT.md#test-discipline))

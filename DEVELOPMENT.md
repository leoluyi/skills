# Developing skills in this repo

The full authoring guide. The always-loaded `CLAUDE.md` carries only the hard *prohibitions*; this file is the reference behind them.

(Note: `<skill>/DEVELOPMENT.md` is a *per-skill* dev-notes file — iteration log, method, provenance for one skill. This root `DEVELOPMENT.md` is the repo-wide authoring guide. Different scope, same name by tier.)

## Anatomy of a skill

```
skills/<name>/
├── SKILL.md         # frontmatter + body — the index, not the manual
├── references/      # optional — large docs the body points at on demand
└── scripts/         # optional — deterministic logic, no LLM needed
evals/<name>/
└── prompts.json     # with-vs-without baselines (mirrors skills/<name>/)
```

The `SKILL.md` frontmatter is two fields. The `description` is the **trigger gate** — the only thing Claude sees when deciding whether to load the skill. Name what should fire it *and* what should not:

```yaml
---
name: rfp-writing
description: Write or review technical RFP documents from the issuer's perspective…
  Trigger only when the user explicitly asks for an RFP; do not invoke for migration
  plans, runbooks, or design docs — those conventions conflict with RFP rules.
---
```

### Gotcha: frontmatter must be real UTF-8, never `\u` escapes

The `description` is an unquoted YAML plain scalar, and **YAML does not decode `\u` escapes in plain scalars** — the skill loader hands Claude the raw `\u`-escaped codepoints, not the decoded `台灣`. A zh skill whose description is `\u`-escaped therefore has *dead* Chinese triggers: Claude sees escape gibberish, not 「去除 AI 味」, and never fires on Chinese prompts. The body is unaffected (it isn't parsed as YAML), which is why the bug hides — the skill reads fine, it just won't trigger. This silently disabled every Chinese trigger in `avoid-ai-writing-zh` until it was caught.

- **Detect:** `rg -l '\\u[0-9A-F]{4}' skills/*/SKILL.md` — any hit on a `description:` line is the bug. An escaped emoji on a *double-quoted* line (`emoji: "✍️"`) is fine; double-quoted scalars do decode.
- **Fix:** write the description in real Traditional Chinese, same as the body. `tools/new-skill` is the suspected source of escaping — check new skills before shipping.
- **Related:** a `: ` (colon-space) inside an *unquoted* description breaks strict YAML parsers. The fix is a `>-` folded block scalar (see `plain-speak`) — inside a block scalar `:` and `"` are literal, so a description can hold them freely. Scaffold new descriptions as `>-`.

## SDLC

A skill goes through these seven stages. Most die at stage 3.

1. **Capture** — friction hit twice → add a one-liner to `backlog.md`. Don't draft yet.
2. **Draft** — `tools/new-skill <kebab-name>` scaffolds `skills/<name>/SKILL.md` plus `evals/<name>/prompts.json`.
3. **Test** — write 3+ realistic prompts in `prompts.json`, run each **with** the skill and **without**. See [Test discipline](#test-discipline).
4. **Iterate** — adjust the body until with-skill beats vanilla on every prompt. If you can't get there, cut it.
5. **Optimize description** — rewrite the trigger gate until Claude invokes it on the right prompts and *not* on lookalike-but-wrong ones.
6. **Deploy** — commit and push. Consumer machines pull via `npx skills update --all` or `tools/sync-skills`.
7. **Maintain / retire** — `tools/usage-report` quarterly; archive dormant skills via `tools/archive-skill <name>`. See [Maintenance](#maintenance).

## Naming

- kebab-case, lowercase
- action-flavored — verbs over nouns when possible
- specific over generic — `oracle-exadata-cutover` not `migration`, `rfp-writing` not `documents`

## Authoring rules

- **Write the description pushy.** It's the trigger gate (see [Anatomy](#anatomy-of-a-skill)). Name the explicit phrases that should fire it *and* what should NOT. Vague descriptions either misfire on unrelated prompts or silently never load.
- **Body under 500 lines.** Lean on progressive disclosure — the SKILL.md is the index, push detail into `references/` and logic into `scripts/`.
- **Explain *why*, not just *what*.** Bullet lists describe a procedure; the *why* lets a reader extrapolate to edge cases the bullets miss. If the skill says "do X", say what X is preventing.
- **Every skill must be portable.** It runs unchanged on Claude Code *and* Codex — not Claude Code only. See [Portability](#portability). Tool-specific power (hooks, `context: fork`, `model`) may be present but never load-bearing.

## Portability

This repo is the single source of truth, symlinked into each agent's skills tree. So every skill must run **unchanged** on Claude Code *and* Codex (Cursor and OpenHands then come nearly free). Portability is a shipping requirement, not a nice-to-have — a skill that only works in Claude Code is half-built.

What actually breaks portability, and the rule for each:

- **`name` + `description` are the only universally-required frontmatter.** That's the agentskills.io 1.0 core, and exactly what Codex requires. Claude-Code extras (`hooks`, `context: fork`, `model`, `effort`, `agent`, `argument-hint`, `disable-model-invocation`) are no-ops in Codex — keep them where they earn it, but **never let a skill's core behavior depend on one**. Custom data goes in the spec's `metadata:` map, not new top-level keys — Codex tolerates unknown keys, but the spec only *guarantees* a home under `metadata`.
- **The body stays invocation-agnostic.** Write "when the user asks to X", never "when the user runs `/x`" (Claude) or "`$x`" (Codex) — invocation syntax differs per tool. Let `description` carry the trigger; keep the body about *what*, not *how it's typed*.
- **No CWD assumptions.** Different tools launch from different directories. Reference bundled files by relative path from `SKILL.md` (both honor that); resolve machine paths through an env var with a default (`learn-loop`'s `LEARN_VAULT`), never a hardcoded absolute. Don't put `${CLAUDE_SKILL_DIR}` in text Codex must execute — it won't expand there.
- **Tool-specific runtime features live outside the skill, registered separately.** Claude Code hooks are the worked example: `learn-loop`'s vault guard is `skills/learn-loop/hooks/guard-vault-path.sh` plus a `~/.claude/settings.json` registration — *not* a line in `SKILL.md`. A machine without Claude Code just loses the guard; the skill still runs. Same discipline for MCP-only tools — name plain `Bash`/`Read`/`Grep` both agents have, not a specific MCP tool, unless both are guaranteed to have it.
- **Sync must bridge every tool's tree — or "portable" is only a claim.** `~/.claude/skills/` is read by Claude Code and Cursor. **Codex and OpenHands do not read it** — they read `~/.agents/skills/`, the emerging cross-tool standard dir. `tools/sync-skills` links each `skills/<name>/` into both trees, so this is enforced, not just documented.

Who reads what:

| Tool | reads `~/.claude/skills`? | native skills dir |
|------|---------------------------|-------------------|
| Claude Code | yes (home) | `~/.claude/skills/` |
| Cursor | yes (compat) | `~/.cursor/skills/`, `~/.agents/skills/` |
| Codex | **no** | `~/.agents/skills/` |
| OpenHands | **no** | `~/.agents/skills/` |

Sources: `code.claude.com/docs/en/skills` · `learn.chatgpt.com/docs/build-skills` · `agentskills.io/specification` · `cursor.com/docs/context/skills`.

## Test discipline

Expands on SDLC stages 3–4. Every skill ships with a `evals/<name>/prompts.json`. Every change to a skill is validated against those prompts **with-vs-without** baselines. The skill ships only if it's materially better than vanilla Claude on every prompt. No bar-clearing, no skill.

This is the single most important rule in this repo. A skill that exists but doesn't help is worse than no skill — it eats context, it pollutes the trigger surface for other skills, and it makes the portfolio look healthier than it is.

## Maintenance

Expands on SDLC stage 7.

- `tools/usage-report` quarterly. Skills with zero hits in 90 days → archive candidate.
- A skill firing too often on wrong prompts → tighten the description.
- A skill firing too rarely on right prompts → loosen / make the description more pushy, or add example trigger phrases.
- Archive aggressively. The repo is supposed to feel small.

## Keep development-process noise out of skill content

`SKILL.md` and everything under a skill's `references/` are **runtime instructions** the model loads when the skill fires. They must read as "how to do the task," never "how this skill was built." This is the `打破第四面牆 / 生成過程外洩` rule (see `skills/avoid-ai-writing-zh`) applied to our own files.

Do **not** leave these in `SKILL.md` or `references/`:

- **Iteration provenance** — `依據 GAN 協定 round 1…`, `round 2 補強`, eval IDs (`eval #14`), FP/recall figures.
- **Derivation narrative** — `比對〈A〉與〈B〉後發現…`, `兩篇對照補強`, `（benchmark 實證）`, `（補充樣本：X 一文）`.
- **Method-named headers** — a header that names how a technique was derived instead of what it is (`## 兩篇對照補強` → `## 進階招式`).

Keep the **insight**, drop the **derivation**. Rewrite `比對 A 與 B 後發現此風味有兩種子模式` → `此風味有兩種子模式：…（下筆前先定位在哪一端）`. Article titles used as *illustrative* examples of a technique stay; titles used as *derivation evidence* go.

### Where provenance belongs instead

- `<skill>/DEVELOPMENT.md` — per-skill development notes.
- `evals/<skill>/benchmark-protocol.md` — iteration log and method.
- Commit messages / PR descriptions — what changed and why.
- `backlog.md` — deferred work.

### Finishing check

Before finalizing a skill edit, grep the skill and its references:

```
grep -rnE 'GAN|round [0-9]|benchmark|補強|補充樣本|比對〈|對照[^，。]*〈|可般化|般化|來自對照|eval #|FP ?=|recall' skills/<name>/
```

Hits inside `SKILL.md` or `references/` are noise — move them to the dev docs above. Hits inside `DEVELOPMENT.md` / `benchmark-protocol.md` / `.json` eval fixtures are fine; that is where provenance lives.

## Skill self-sufficiency and dependency direction

Every skill must complete its own stated job without another skill being invoked. Three rules:

- **Runtime self-sufficiency.** No `SKILL.md` step may require running another skill first. Mentions of sibling skills are *optional pointers* ("if you also want X, `foo` handles that"), never prerequisites.
- **Dependencies are one-directional — no cycles.** A one-way hard dependency is fine (e.g. `blog-writing-zh` always calls `avoid-ai-writing-zh` as its finishing pass). But the depended-on skill — the shared leaf utility — must itself be self-sufficient, and two skills must never hard-depend on each other. The graph is a DAG; shared utilities sit at the bottom.
- **A callee never enumerates its callers.** The routing edge lives on the caller's side (single source of truth). A utility skill that many others call must not name those callers in its own `description` — that only adds context load and manufactures apparent mutual coupling.

Check: a `description` or `SKILL.md` that says "run X first, then this," or that names its own upstream callers, breaks these. Convert to an optional pointer, or move the edge to the caller's side.

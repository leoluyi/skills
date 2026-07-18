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
2. **Draft** — `tools/new-skill <kebab-name>` scaffolds `skills/<name>/SKILL.md` plus `skills/<name>/evals/evals.json`.
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

## Write generative-first (the subtraction discipline)

A skill's words compete for the model's attention, and their *register* sets
the model's mode. Compliance vocabulary — gate, checklist, must, verify,
self-attest — pushes the model into satisficing: it optimizes *passing your
checks* instead of doing the craft (Goodhart's law, live). The observable
failure: told "text must fit", a compliance-mode model enlarges the box (the
fastest path to green) instead of cutting words; told to cover N cases, it
picks the layout easiest to parameterize instead of the one the content
needs.

- **Open with role, taste, and stakes; explain why; keep procedure light.**
  Model the register on Anthropic's official skills (~50–150 body lines):
  they read as a craft brief, not an SOP. The 500-line cap is a ceiling, not
  a target — a 340-line skill can be well under the cap and still degrade
  output quality.
- **Growth by incident is a defect log, not a skill.** When a failure
  happens, prefer in order: (1) delete or simplify the rule that created the
  pressure, (2) add an eval assertion, (3) add a scripted check. A new prose
  paragraph is the *last* resort — prose rules accreted per-incident are the
  fastest way to bury the generative core.
- **Know each rule's enforcement tier**: script-gated, eval-asserted, or
  taste. Prose-only rules lose whenever they conflict with a convenient
  path; if a taste rule keeps getting violated, promote it to an eval
  assertion — or cut it. A rule nobody enforces is context cost with no
  return.
- **Never restate in prose what a check already enforces.** If a scripted
  check or an eval assertion catches something objectively, naming it again
  as a prose "don't" adds zero enforcement and costs register: it teaches
  the model to read that passage as a checklist, which is the satisficing
  trigger. Keep prose for what cannot be derived from a principle or caught
  by a check — factual tells, taste, and judgment. Conversely, a blocklist
  item that *nothing* enforces is the weakest possible form of a rule;
  convert it into a generative rule that fires at decision time ("derive the
  arrangement from how the parts relate" beats "don't use uniform cards"),
  since a list of things to avoid is passive and a derivation method is not.
  The same applies to a prohibition you intend to keep: state the positive
  principle it protects, or the rule silently fails the messy case.
- **Two standards, different scopes — say which wins where.** How to *write*
  a skill follows `writing-great-skills` (mattpocock/skills): the information
  hierarchy, the branch test for disclosure, completion criteria, leading
  words, and the failure-mode vocabulary (premature completion, duplication,
  sediment, sprawl, no-op, negation). How to *evaluate* a skill follows the
  official `skill-creator`. They rarely overlap; where they do — description
  length and how to phrase a rule — `writing-great-skills` wins. Both agree
  a description must not become a list of specific queries.
- **Steer positive; a prohibition is the exception that needs a reason.**
  Naming the banned behaviour makes it more available, not less. State the
  target behaviour so the banned one is never spoken, and keep a prohibition
  only where the line genuinely cannot be phrased positively — paired with
  what to do instead.
- **Ask where a rule belongs, not just whether it is right.** A good rule
  written into a special-case file only fires on that case; the same rule
  in the general path fires every time. Before adding craft to a named
  chart type, check whether anything about it is actually specific to that
  type — usually only one or two clauses are, and the rest belong upstream
  with a pointer back. And when a reference already documents *how* to do
  something the workflow never asks for, the gap is the trigger, not the
  knowledge: put the decision where the build actually passes through. "Mirror
  the order it was taught" reads as "transcribe the log" the moment a real
  dialogue wanders; "order by the concept chain, each section resting on
  the last one's a-ha" tells the agent what to do with the detour.
- **When two references disagree, resolve it in writing — bind the
  exception to purpose and provenance, not to style.** Two rules that
  silently conflict (e.g. "one name per thing" vs a chart type built on
  dual naming) leave the loaded-context agent to guess which wins. State
  the exception where the general rule lives, name the purpose that
  licenses it and the source the exception's content must come from, and
  cross-reference both ways. "Only for retention graphics, and only with
  names the dialogue actually taught" survives edge cases that "the X
  style allows it" does not.
- **Borrow battle-tested content verbatim; paraphrase is the risk.** When a
  proven source (an official Anthropic skill, an established style guide)
  covers ground your skill needs and the passage is domain-general: check
  the license first, and if it permits, import near-verbatim with
  attribution (a `NOTICE` file in the skill dir; provenance in the skill's
  DEVELOPMENT.md). Rewriting proven prose regresses it toward the mean and
  adds mechanical failure modes (silent no-op replaces, mangled anchors).
  Adapt only where the domain genuinely diverges, at the vocabulary level.
  Domain-specific passages stay out — importing them is noise, not rigor.
  Note this doesn't conflict with subtraction: the line budget cuts
  compliance scaffolding, not proven *generative* content.
- Smell test across versions:
  `grep -ciE '\bmust\b|\bnever\b|hard-fail|checklist|verify' skills/<n>/SKILL.md`
  — a rising count is the bloat signal, independent of line count.

## Scripted checks — severity and trust

Skills may ship deterministic checks under `scripts/`. Their value is that
their verdicts are indisputable; protect that.

- **Hard-fail only objective, reader-harming defects** (won't parse,
  unreadable, clipped/overflowing content). Style preferences and
  maintainability concerns are advisory warnings that never block. Mixing
  style into hard-fail dilutes the true blockers and trains the model to
  route around the gate.
- **A false-positive hard gate is worse than no gate.** Regression-test
  every new check against *real past artifacts*, not only synthetic
  fixtures — fixtures share their author's assumptions; real artifacts
  don't (transform-nested coordinates were the live example).
- **Checks exert directional pressure.** Every constraint has a cheapest
  path to green; state the intended fix order next to the constraint
  ("cut words, then shrink type, enlarge boxes last") or the model will
  take the cheap path.
- **Verify automated edits actually landed.** `str.replace`/`sed` silently
  no-op on an anchor mismatch, and `grep -c` returning 0 breaks `&&`
  chains mid-script. After any scripted patch, grep the target string in
  the file — never print success unconditionally.

## Portability

This repo is the single source of truth, symlinked into each agent's skills tree. So every skill must run **unchanged** on Claude Code *and* Codex (Cursor and OpenHands then come nearly free). Portability is a shipping requirement, not a nice-to-have — a skill that only works in Claude Code is half-built.

What actually breaks portability, and the rule for each:

- **`name` + `description` are the only universally-required frontmatter.** That's the agentskills.io 1.0 core, and exactly what Codex requires. Claude-Code extras (`hooks`, `context: fork`, `model`, `effort`, `agent`, `argument-hint`, `disable-model-invocation`) are no-ops in Codex — keep them where they earn it, but **never let a skill's core behavior depend on one**. This repo's de-facto standard adds three tolerated top-level keys every skill uses — `version`, `license`, `compatibility` — which Codex ignores harmlessly; match that convention. Any *other* custom data goes in the spec's `metadata:` map, not new top-level keys — Codex tolerates unknown keys, but the spec only *guarantees* a home under `metadata`.
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

Expands on SDLC stages 3–4. Follow the official `skill-creator` standard rather than a house method: evals live at `skills/<name>/evals/evals.json`, each with a prompt, a description of success, and a list of *objectively verifiable* statements. Don't force assertions onto subjective quality — for design and writing skills the standard is explicit that quality is judged qualitatively, so keep a small corpus of cases the user has already ruled on (`evals/judged-cases.md`) instead of inflating the assertion count.

Run the two configurations as independent parallel agents launched together, never as one agent that reads the skill and then pretends it hasn't. When improving an existing skill the comparison is against the **previous version**, not vanilla — a mature skill is long past the question of whether it beats nothing. Repeat each configuration a few times; a single run can't separate a real difference from sampling noise.

Skills not yet migrated still use the legacy `evals/<name>/prompts.json`; `tools/run-eval` reads either.

This is the single most important rule in this repo. A skill that exists but doesn't help is worse than no skill — it eats context, it pollutes the trigger surface for other skills, and it makes the portfolio look healthier than it is.

Baselines are **agent-native**: the executing agent *is* the model. Run the
with side and the without side as separate agent sessions (or sub-agent
fan-out: one with the skill loaded, one without, one judging), graded by the
skill's own scripts where deterministic — never an external API harness. If
one agent authors both sides, say so in the log: deterministic script
verdicts stay objective, but qualitative judgments carry author bias, and a
contaminated run only "promotes" a skill's status, never clears it.

Guard against **circular (self-referential) evals**: qualitative assertions derived from
the skill's own prose, judged by a model reading the same prose, measure
conformance to your taste — not user value. Deterministic checks anchored to
external standards (WCAG, a language spec, geometry) don't have this
problem; the qualitative layer needs external anchors: compare at least one
output per round against a *real-world exemplar* of the genre (the
`avoid-ai-writing-zh` human-authored corpus is the in-repo precedent);
phrase assertions as reader outcomes ("a reader can verify X from the
artifact alone") rather than rule restatements ("the artifact contains
device Y"); Anchoring the *assertions* is not enough if the **scenarios** are also
self-authored: a suite written by asking "what does this skill claim to do
well?" can only fail where you already thought to look, so a green run
measures internal consistency, not quality. Watch the track record — if a
suite has never caught anything it was not designed to catch, that is the
finding. Source scenarios from outside instead: requests the user actually
made, and artifacts the user has already judged. A short `judged-cases.md`
(source material, the verdict, what the verdict turned on, the rule it
produced) is worth more than a large self-authored suite, because the ground
truth existed before the run. Keep the self-authored suite, but re-badge it
as a **regression guard** — it is good at noticing a deleted rule and
worthless as evidence of improvement. Note also that a contaminated
with/without comparison still supports one direction safely: "the
alternative has something we lack" survives contamination, while "we are
better" does not.

Finally, treat human judgment as the tie-breaker — when a person
says the output got worse while every internal metric is green, suspect the
rubric before the person.

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
- `skills/<skill>/evals/judged-cases.md` — the corpus of user verdicts
  (source material, the ruling, what it turned on, the rule it produced).
- Commit messages / PR descriptions — what changed and why.
- `backlog.md` — deferred work.

### Finishing check

Before finalizing a skill edit, grep the skill and its references:

```
grep -rnE 'GAN|round [0-9]|benchmark|補強|補充樣本|比對〈|對照[^，。]*〈|可般化|般化|來自對照|eval #|FP ?=|recall' skills/<name>/
```

Hits inside `SKILL.md` or `references/` are noise — move them to the dev docs above. Hits inside `DEVELOPMENT.md` / `judged-cases.md` / `.json` eval fixtures are fine; that is where provenance lives.

## Skill self-sufficiency and dependency direction

Every skill must complete its own stated job without another skill being invoked. Three rules:

- **Runtime self-sufficiency.** No `SKILL.md` step may require running another skill first. Mentions of sibling skills are *optional pointers* ("if you also want X, `foo` handles that"), never prerequisites.
- **Dependencies are one-directional — no cycles.** A one-way hard dependency is fine (e.g. `blog-writing-zh` always calls `avoid-ai-writing-zh` as its finishing pass). But the depended-on skill — the shared leaf utility — must itself be self-sufficient, and two skills must never hard-depend on each other. The graph is a DAG; shared utilities sit at the bottom.
- **A callee never enumerates its callers.** The routing edge lives on the caller's side (single source of truth). A utility skill that many others call must not name those callers in its own `description` — that only adds context load and manufactures apparent mutual coupling.

Check: a `description` or `SKILL.md` that says "run X first, then this," or that names its own upstream callers, breaks these. Convert to an optional pointer, or move the edge to the caller's side.

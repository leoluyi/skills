# Developing skills in this repo

The repo-wide authoring guide. The always-loaded `CLAUDE.md` carries only the hard prohibitions; this file is the reference behind them. (`<skill>/design-notes.md` is a *per-skill* dev-notes file: iteration log, method, provenance for that one skill.)

Formatting convention for this file: one paragraph per line, no hard wraps.

## Anatomy of a skill

```
skills/<name>/
├── SKILL.md         # frontmatter + body — the index, not the manual
├── references/      # optional — large docs the body points at on demand
├── scripts/         # optional — deterministic logic, no LLM needed
└── evals/
    ├── evals.json        # with-vs-without test cases
    ├── judged-cases.md   # optional — corpus of user verdicts
    └── label-check.json  # optional — opt into the tools/check-labels gate
```

Keep the body under 500 lines; everything past that belongs in `references/` or `scripts/`.

The frontmatter needs two fields. The `description` is the **trigger gate** — the only thing the agent sees when deciding whether to load the skill. Name what should fire it *and* what should not:

```yaml
---
name: rfp-writing
description: Write or review technical RFP documents from the issuer's perspective…
  Trigger only when the user explicitly asks for an RFP; do not invoke for migration
  plans, runbooks, or design docs — those conventions conflict with RFP rules.
---
```

### Gotcha: frontmatter must be real UTF-8, never `\u` escapes

The `description` is an unquoted YAML plain scalar, and YAML does not decode `\u` escapes in plain scalars — the loader hands the agent the raw escape sequences, not the decoded text. Non-ASCII trigger phrases written as escapes are therefore dead: the skill reads fine and loads fine, but silently never fires on those prompts. The body is unaffected (it isn't parsed as YAML), which is why the bug hides.

- **Detect:** `rg -l '\\u[0-9A-F]{4}' skills/*/SKILL.md` — any hit on a `description:` line is the bug. Escapes inside a *double-quoted* scalar are fine; those decode.
- **Fix:** write the description in real UTF-8, same as the body. Check scaffolded skills before shipping.
- **Related:** a `: ` (colon-space) inside an *unquoted* description breaks strict YAML parsers. Scaffold descriptions as `>-` folded block scalars — inside a block scalar, `:` and `"` are literal.

## Lifecycle

A skill goes through seven stages. Most die at stage 3.

1. **Capture** — friction hit twice → add a one-liner to a backlog. Don't draft yet. An item about one skill goes in `skills/<name>/backlog.md`; repo-level and `tools/` items go in the root `backlog.md`, which also indexes the per-skill files.
2. **Draft** — `tools/new-skill <kebab-name>` scaffolds `skills/<name>/SKILL.md` plus `skills/<name>/evals/` (`evals.json`, `trigger-queries.json`, and `regression-protocol.md` from `tools/templates/`; fill in the TODO ship gates per the skill's ethos).
3. **Test** — write 3+ realistic prompts, run each **with** the skill and **without**. See [Test discipline](#test-discipline).
4. **Iterate** — adjust the body until with-skill beats the baseline on every prompt. If you can't get there, cut it.
5. **Optimize the description** — rewrite the trigger gate until the agent invokes it on the right prompts and *not* on lookalike-but-wrong ones.
6. **Deploy** — commit and push. Consumer machines pull via `npx skills update --all` or `tools/sync-skills`.
7. **Maintain / retire** — `tools/usage-report` quarterly; archive dormant skills via `tools/archive-skill <name>`. See [Maintenance](#maintenance).

## Naming

kebab-case, action-flavored, specific over generic: `oracle-exadata-cutover` not `migration`, `rfp-writing` not `documents`.

## Invocation modes

Every skill is **model-invoked** (agent or user can fire it — the default) or **user-invoked** (only the human typing its name, via `disable-model-invocation: true`). The catalog marks the latter `invoke-only`. Which to pick, and how it changes what the `description` is written for, is in [`.agents/invocation.md`](.agents/invocation.md). Caveat for this repo: `disable-model-invocation` is a Claude-Code field Codex reads as a no-op (see [Portability](#portability)), so user-invoked is not yet enforced on the Codex side — a skill that must never auto-fire can't rely on the flag alone across tools.

## Write generative-first

A skill's words compete for the model's attention, and their *register* sets the model's mode. Compliance vocabulary — gate, checklist, must, verify — pushes the model into satisficing: it optimizes *passing your checks* instead of doing the craft. Told "text must fit", a compliance-mode model enlarges the box (the fastest path to green) instead of cutting words.

- **Open with role, taste, and stakes; keep procedure light.** Model the register on Anthropic's official skills (~50–150 body lines): a craft brief, not an SOP. The 500-line cap is a ceiling, not a target.
- **Explain *why*, not just *what*.** The why lets the model extrapolate to edge cases the bullets miss — it is what makes judgement possible instead of pattern-matching. If the skill says "do X", say what X prevents.
- **Growth by incident is a defect log, not a skill.** After a failure, prefer in order: (1) delete or simplify the rule that created the pressure, (2) add an eval assertion, (3) add a scripted check. A new prose paragraph is the last resort — per-incident prose is the fastest way to bury the generative core.
- **Don't spend tokens on what the model already does.** A rule earns its place only if removing it makes the output worse. Before adding one — and periodically for the ones already there — delete it and re-run the evals; if nothing regresses, it was stating the obvious, and the context it consumed was pure cost. Rules written to hobble an older model become the thing hobbling the current one.
- **Know each rule's enforcement tier** — script-gated, eval-asserted, or taste. If a taste rule keeps getting violated, promote it to an eval assertion or cut it. A rule nobody enforces is context cost with no return.
- **State each rule once, at the strongest tier.** If a check already enforces something objectively, restating it as prose adds zero enforcement and teaches the model to read the passage as a checklist. Keep prose for what checks can't catch — factual tells, taste, judgment — and phrase it generatively: a derivation method that fires at decision time beats a passive list of things to avoid.
- **Steer positive.** Naming a banned behaviour makes it more available, not less. State the target behaviour so the banned one is never spoken; keep a prohibition only where it genuinely can't be phrased positively, paired with what to do instead.
- **Put a rule where every affected path passes through.** Craft written into a special-case section only fires on that case — usually only a clause or two is actually specific, and the rest belongs upstream with a pointer back. When two rules conflict, resolve it in writing where the general rule lives: name the purpose that licenses the exception and the source its content must come from, and cross-reference both ways.
- **Design the interface before you teach by example.** Worked examples of a *procedure* fence the model into the exploration space they demonstrate; a well-shaped script signature, file layout, or reference structure does not. Spend the effort on the tool's parameters and expressiveness, then let the model derive the call. Only verbatim-output content is exempt — templates, term tables, phrasing tables are the output itself, not a demonstration of how to reach it (see [Language strategy](#language-strategy)). Example sentences that teach a judgement call are *not* exempt: convert them into a derivation rule or a reference the model consults on demand, or be able to say what each one buys that a rule can't.
- **Borrow battle-tested content verbatim.** When a proven source covers domain-general ground your skill needs, check the license, then import near-verbatim with attribution (a `NOTICE` file in the skill dir; provenance in the skill's `design-notes.md`). Paraphrase regresses proven prose toward the mean. Adapt only where the domain genuinely diverges.
- **Two external standards, one tie-break.** How to *write* a skill follows `writing-great-skills`; how to *evaluate* one follows the official `skill-creator`. Where they overlap, `writing-great-skills` wins.

Smell test across versions: `grep -ciE '\bmust\b|\bnever\b|hard-fail|checklist|verify' skills/<name>/SKILL.md` — a rising count signals bloat, independent of line count.

Sources: `writing-great-skills` · `skill-creator` · [The new rules of context engineering for Claude 5-generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models).

## Language strategy

A skill's language is a per-layer decision, made three times:

- **`description` (trigger layer): English skeleton + native-language trigger phrases, verbatim.** The description is semantically matched against user input, so the exact phrases users actually type must appear as typed — an English gloss of a native-language phrase matches unreliably. Those phrases must be real UTF-8 — see [the frontmatter gotcha](#gotcha-frontmatter-must-be-real-utf-8-never-u-escapes).
- **Body (instruction layer): English by default.** Denser per token, sharper imperative semantics, and consistent with the first-party skills loaded beside it, so instructions don't fight each other.
- **Verbatim-output content: written directly in the target language.** Document templates, phrasing tables, term blacklists, fixed option copy, example outputs — anything emitted as-is. Routing these through English and expecting the model to translate produces both semantic drift and language leakage.

### The leakage guard

An English body becomes the ambient register of the context, and the model follows it. Prose rarely leaks — the user's native-language request anchors it. What leaks is the short strings the model improvises because the skill never specified them (option labels, headings in generated documents); the classic symptom is native-language body text under English headings.

Any skill that emits non-English output carries a **leakage guard**: a fixed `## Output Language` block at the top of the body. It names its own scope — "respond in Traditional Chinese" alone gets read as covering prose only — and its last paragraph severs the body-language → output-language mimicry path. Canonical text:

```markdown
## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.
```

If a skill has a locale convention, append it as its own paragraph before the last:

```markdown
If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.
```

The guard is copied text — `SKILL.md` can't import — so **this file is its single source of truth**. When you change the canonical wording, `rg -l '## Output Language' skills/` and update every copy.

Acceptance check: run the full flow once and verify the improvised strings — option labels, every generated-document heading, interstitial status text — came out in the target language.

## Scripted checks — severity and trust

Skills may ship deterministic checks under `scripts/`. Their value is that their verdicts are indisputable; protect that.

- **Hard-fail only objective, reader-harming defects** (won't parse, unreadable, clipped/overflowing content). Style and maintainability concerns are advisory warnings that never block. Mixing style into hard-fail dilutes the true blockers and trains the model to route around the gate.
- **A false-positive hard gate is worse than no gate.** Regression-test every new check against real past artifacts, not only synthetic fixtures — fixtures share their author's assumptions; real artifacts don't.
- **Checks exert directional pressure.** Every constraint has a cheapest path to green; state the intended fix order next to the constraint ("cut words, then shrink type, enlarge boxes last") or the model takes the cheap path.
- **Verify automated edits actually landed.** `str.replace`/`sed` silently no-op on an anchor mismatch. After any scripted patch, grep the target string in the file — never print success unconditionally.

## Where a tool lives — `scripts/` vs `tools/`

Decide by **who runs it**, not by how many skills it serves.

- **Runtime → `skills/<name>/scripts/`.** Anything the skill itself invokes mid-flow. It ships with the skill, so its cost lands on every consumer. Bound by [Portability](#portability) and the severity rules above: the skill must still complete where the interpreter is missing (the check degrades to a human read), and a script stays a *verification gate*, never the only path to the output. `infographic-design/scripts/check.py` is the model.
- **Dev-side → `tools/`, even when exactly one skill uses it.** Eval dispatch, label hygiene, catalog builds — run by whoever maintains the repo. Don't copy a maintainer script into a skill dir to signal ownership: every file under `skills/<name>/` is a distribution artifact and a context cost for consumers who will never run it. `tools/check-labels` serves only humanizer-zh today and still belongs in `tools/`.
- **A dev tool's backlog item may sit in the skill's backlog even though its code lives in `tools/`.** The item goes where the *judgment* belongs (`tools/annotate` asks a humanizer-zh question, so it is tracked there); the code goes where the *runner* belongs. These two answers are allowed to differ — say which is which in the item.
- **A single-skill dev tool takes config, never hardcoded paths.** Make participation opt-in through a declaration the skill ships, so a skill that hasn't opted in **skips cleanly** rather than erroring — an exit-2 on every other skill is what stops a gate from being generalizable. A file the config *does* declare but that is missing stays a hard error: opting in and then losing a rule file is a defect, not an absent feature. `tools/check-labels` reads `skills/<name>/evals/label-check.json` (regex sources for the canonical rule names, plus an optional corpus path) and is run `--all` by `.github/workflows/eval-labels.yml`; the config declares *where names live*, never the names, so there is still no taxonomy manifest to drift.

## Portability

This repo is the single source of truth, symlinked into each agent's skills tree, so every skill must run unchanged on Claude Code *and* Codex (Cursor and OpenHands then come nearly free). What breaks portability, and the rule for each:

- **`name` + `description` are the only universally required frontmatter** (the agentskills.io 1.0 core). Claude-Code extras (`hooks`, `context: fork`, `model`, `effort`, `agent`, `argument-hint`, `disable-model-invocation`) are no-ops in Codex — keep them where they earn it, but never let core behavior depend on one. This repo's convention adds `version`, `license`, `compatibility`, which Codex ignores harmlessly. Any other custom data goes under the spec's `metadata:` map, not new top-level keys.
- **The body stays invocation-agnostic.** Write "when the user asks to X", never a tool-specific invocation syntax. The description carries the trigger; the body is about *what*, not *how it's typed*.
- **No CWD assumptions.** Reference bundled files by relative path from `SKILL.md`. Resolve machine paths through an env var with a default, never a hardcoded absolute. Tool-specific variables like `${CLAUDE_SKILL_DIR}` don't expand in other tools.
- **Tool-specific runtime features live outside the skill, registered separately** (e.g. a Claude Code hook script in the skill dir plus its `settings.json` registration — never a load-bearing line in `SKILL.md`). A machine without that tool loses the feature; the skill still runs. Name plain tools both agents have (`Bash`, `Read`, `Grep`), not tool-specific ones.
- **Sync must bridge every tool's tree.** `tools/sync-skills` links each `skills/<name>/` into both `~/.claude/skills/` and `~/.agents/skills/`, so this is enforced, not just documented.

| Tool | reads `~/.claude/skills`? | native skills dir |
|------|---------------------------|-------------------|
| Claude Code | yes (home) | `~/.claude/skills/` |
| Cursor | yes (compat) | `~/.cursor/skills/`, `~/.agents/skills/` |
| Codex | **no** | `~/.agents/skills/` |
| OpenHands | **no** | `~/.agents/skills/` |

Sources: `code.claude.com/docs/en/skills` · `learn.chatgpt.com/docs/build-skills` · `agentskills.io/specification` · `cursor.com/docs/context/skills`.

## Test discipline

Evals follow the official `skill-creator` standard: `skills/<name>/evals/evals.json`, each case a prompt, a description of success, and objectively verifiable assertions. Don't force assertions onto subjective quality — for design and writing skills, judge qualitatively against a small corpus of cases the user has already ruled on (`evals/judged-cases.md`). Legacy suites at `evals/<name>/prompts.json` still work; `tools/run-eval` reads either.

- **Beat the baseline or cut the skill.** A skill that exists but doesn't help is worse than none — it eats context, pollutes the trigger surface for other skills, and makes the portfolio look healthier than it is. This is the single most important rule in this repo.
- **Compare as independent parallel agents,** one with the skill and one without, launched together — never one agent that reads the skill and then pretends it hasn't. Repeat each configuration a few times; a single run can't separate a real difference from sampling noise. For an existing skill, the baseline is the previous version, not vanilla.
- **Declare contamination.** If one agent authors both sides, say so in the log: deterministic script verdicts stay objective, but qualitative judgments carry author bias. A contaminated comparison still supports "the alternative has something we lack" — never "we are better".
- **Anchor evals externally, or they measure your taste.** Assertions derived from the skill's own prose, judged by a model reading that prose, measure conformance — not user value. Phrase assertions as reader outcomes ("a reader can verify X from the artifact alone"), anchor to external standards where they exist, and compare at least one output per round against a real-world exemplar of the genre. Source scenarios from real user requests and artifacts the user has already judged, not from "what does this skill claim to do well?" — a self-authored suite can only fail where you already thought to look. Keep it as a regression guard: good at noticing a deleted rule, worthless as evidence of improvement.
- **Pair every should-fire assertion with a must-not-fire boundary.** A suite that only checks "the rule catches X" is blind to over-triggering: when adding a detection rule, also add the nearest legitimate text the rule must leave alone, and track the two failure classes separately — for most skills here, a false positive on real writing outranks a missed catch. Text-rewriting skills get three further standing checks on every rewrite output: fidelity (numbers, names, links, quoted text survive verbatim), no same-family substitution (deleting 「賦能」 only to insert 「加值」 is a fail, not a fix), and a prompt-injection probe (an "ignore your rules" instruction embedded in the manuscript is data to edit, not a command). Adapted from speak-human-tw's eval protocol.
- **Human judgment is the tie-breaker.** When a person says the output got worse while every internal metric is green, suspect the rubric before the person.
- **Cross-check a suspicious trigger result on the second router before calling it a regression.** `tools/run-eval` drives `trigger-queries.json` through Claude Code by default and through Codex with `RUN_EVAL_AGENT=codex`; both are pinned and both refuse to spend a billed API key. When the two disagree case-by-case, the harness is the suspect; when they agree, the router change is real. Re-running the same CLI and hoping tells you nothing.
## Maintenance

- `tools/usage-report` quarterly. Zero hits in 90 days → archive candidate (`tools/archive-skill <name>`).
- Fires too often on wrong prompts → tighten the description. Fires too rarely on right ones → make the description pushier or add trigger phrases.
- **A model upgrade invalidates the baseline.** Evals compare a skill against its previous version *on the current model*; when the model generation changes, re-run the with/without comparison before trusting old results. A skill that beat vanilla two generations ago may now be net-negative — the base model absorbed what it was teaching.
- Archive aggressively. The repo is supposed to feel small.

## Catalog upkeep

The repo has no per-skill hosted docs page; a skill's public face is its **catalog entry**, generated from one source — `skills/<slug>/catalog.md` — by `tools/build-docs` into the README tables, `docs/index.html`, and `docs/skills.json` (the last two are gitignored build output, regenerated by the Pages workflow on every push to `main`). Adding, renaming, or recategorizing a skill means editing `catalog.md` and re-running `uv run tools/build-docs`; there's nothing else to keep in sync. Full field reference and the done-checklist are in [`.agents/writing-docs.md`](.agents/writing-docs.md).

## Keep development-process noise out of skill content

`SKILL.md` and everything under `references/` are runtime instructions the model loads when the skill fires. They must read as "how to do the task", never "how this skill was built". Keep the **insight**, drop the **derivation**: iteration provenance (round numbers, eval IDs, precision/recall figures), derivation narrative ("comparing A and B showed…"), and headers named after how a technique was derived all go. Provenance belongs in the skill's `design-notes.md`, `evals/judged-cases.md`, commit messages, or `backlog.md` (the skill's own, or the root one for repo-level items).

Finishing check before finalizing a skill edit:

```
grep -rnE 'round [0-9]|eval #|FP ?=|recall|benchmark|precision' skills/<name>/
```

The grep only catches the mechanical tells; read for the rest — any sentence explaining *how a rule was arrived at* rather than how to apply it is noise, whatever words it uses. Hits inside `SKILL.md` or `references/` are noise — move them to the dev docs above. Hits inside `design-notes.md`, `judged-cases.md`, or eval fixtures are fine; that is where provenance lives.

## Skill self-sufficiency and dependency direction

Every skill completes its own stated job without another skill being invoked.

- **No prerequisites.** Mentions of sibling skills are optional pointers ("if you also want X, `foo` handles that"), never "run X first, then this".
- **Dependencies form a DAG.** A one-way hard dependency on a self-sufficient leaf utility is fine; two skills never hard-depend on each other. Shared utilities sit at the bottom.
- **A callee never names its callers.** The routing edge lives on the caller's side — single source of truth. A utility skill that lists its callers in its own description adds context load and manufactures apparent mutual coupling.

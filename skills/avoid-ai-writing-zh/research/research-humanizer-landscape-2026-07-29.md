# Humanizer-skill landscape research — for the avoid-ai-writing-zh rewrite

Researched 2026-07-29 against primary sources: official Anthropic/OpenAI docs, the agentskills.io spec, raw files from the three humanizer repos (fetched via GitHub API / raw.githubusercontent.com, snapshots in this scratchpad's `dl/`), and the local repo's own conventions. Every claim carries its source.

---

## Q1. Anthropic skill-authoring guidance (primary sources)

### SKILL.md length and shape

- **"Keep SKILL.md body under 500 lines for optimal performance. Split content into separate files when approaching this limit."** — Skill authoring best practices, https://platform.claude.com/docs/en/docs/agents-and-tools/agent-skills/best-practices (§Progressive disclosure patterns; repeated verbatim in §Token budgets and in the ship checklist "SKILL.md body is under 500 lines").
- The Agent Skills overview's progressive-disclosure table budgets **Level 2 (SKILL.md body) at "Under 5k tokens"**, Level 1 metadata at "~100 tokens per Skill", Level 3 resources at "None until accessed". — https://platform.claude.com/docs/en/docs/agents-and-tools/agent-skills/overview (§How Skills work).
- Shape: "SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide." — best-practices, §Progressive disclosure patterns.
- Core principle: "**Concise is key** … The context window is a public good … Default assumption: Claude is already very smart. Only add context Claude doesn't already have." — best-practices, §Core principles.
- The agentskills.io spec (which `anthropics/skills/spec/agent-skills-spec.md` now redirects to — the repo file is an 87-byte stub reading "The spec is now located at <https://agentskills.io/specification>") makes the same numbers normative: "Instructions (< 5000 tokens recommended)… Keep your main SKILL.md under 500 lines. Move detailed reference material to separate files." — https://agentskills.io/specification (§Progressive disclosure).
- Relevant to this rewrite: the current `avoid-ai-writing-zh/SKILL.md` is **966 lines / 112 KB** (`wc -l /Users/leoluyi/.skills/skills/avoid-ai-writing-zh/SKILL.md`) — roughly 2× the official line budget and far past the ~5k-token body guidance.

### Progressive disclosure guidance

- Three levels (overview, §How Skills work): metadata always loaded; SKILL.md body loaded on trigger; "Claude accesses these files only when referenced… A Skill can include dozens of reference files, but if your task only needs the sales schema, that's the one file Claude loads."
- Patterns (best-practices): Pattern 1 "High-level guide with references"; Pattern 2 "Domain-specific organization" (split by domain so only relevant files load); Pattern 3 "Conditional details" — "Show basic content, link to advanced content… Claude reads REDLINING.md or OOXML.md only when the user needs those features."
- **"Keep references one level deep from SKILL.md"** — nested reference chains cause partial reads (`head -100`) and incomplete information. — best-practices, §Avoid deeply nested references.
- **"For reference files longer than 100 lines, include a table of contents at the top"** so partial reads still reveal scope. — best-practices, §Structure longer reference files.
- Engineering blog: "Agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window"; "If certain contexts are mutually exclusive or rarely used together, keeping the paths separate will reduce the token usage." — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

### Scripts: recommended vs discouraged

- Recommended when determinism/fragility demands it: "**Prefer scripts for deterministic operations**: Write `validate_form.py` rather than asking Claude to generate validation code"; benefits list: "More reliable than generated code / Save tokens / Save time / Ensure consistency". — best-practices, §Provide utility scripts, §Runtime environment.
- The "degrees of freedom" framing: low freedom (specific scripts) only "when operations are fragile and error-prone, consistency is critical, a specific sequence must be followed"; high freedom (text instructions) "when multiple approaches are valid, decisions depend on context, heuristics guide the approach". — best-practices, §Set appropriate degrees of freedom.
- Engineering blog: "many applications require the deterministic reliability that only code can provide."
- Scripts must "solve, don't defer" (handle errors, no voodoo constants), and instructions must state whether a script is to be **executed** or **read as reference**. — best-practices, §Advanced: Skills with executable code.

### The "large prompt reductions don't degrade quality" claim

- **Neither engineering post makes this claim quantitatively.** The Agent Skills post describes architectural benefits without performance numbers. "Effective context engineering for AI agents" (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) frames it directionally: context is "a finite resource with diminishing marginal returns"; "Every new token introduced depletes this budget"; the goal is "the smallest possible set of high-signal tokens"; it endorses progressive disclosure ("allows agents to incrementally discover relevant context through exploration") and just-in-time loading via "lightweight identifiers (file paths, stored queries, web links)". If the rewrite's design rationale needs the "reduction is safe" claim, cite these directional statements — do not cite Anthropic for a specific percentage; no primary source found provides one.

### Official directory conventions inside a skill

From the agentskills.io spec (https://agentskills.io/specification, §Directory structure and §Optional directories) — the normative source, since anthropics/skills defers to it:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

- `scripts/`: "executable code that agents can run… self-contained or clearly document dependencies."
- `references/`: "additional documentation that agents can read when needed… Agents load these on demand, so smaller files mean less use of context."
- `assets/`: "static resources: Templates… Images… Data files (lookup tables, schemas)."
- The trailing `└── ...` line explicitly permits "Any additional files or directories" beyond the three named ones.
- File references: "use relative paths from the skill root… Keep file references one level deep from SKILL.md."

**Verdict (Q1):** Official guidance is unambiguous: SKILL.md is an index under 500 lines / ~5k tokens; detail goes into on-demand `references/` files, one level deep, each with a TOC if >100 lines; scripts only for deterministic/fragile operations, with judgment-heavy work left as instructions. The current 966-line SKILL.md violates the primary guidance the rewrite should fix.

---

## Q2. Three humanizer projects — actual files

Snapshots read for this analysis: `dl/humanizer-SKILL.md`, `dl/xh-SKILL.md`, `dl/xh-examples.md`, `dl/xh-scrub-rules.md`, `dl/xh-audit.md`, `dl/sht-SKILL.md`, `dl/sht-examples.md`, plus the three LICENSE files, in `/private/tmp/claude-501/-Users-leoluyi--skills/961d5bc0-b2f8-4698-8b75-e91a79618428/scratchpad/dl/`.

### blader/humanizer (https://github.com/blader/humanizer)

- **Structure** (GitHub API tree, main branch): `SKILL.md` (29,632 B / **412 lines**), `README.md`, `AGENTS.md`, `LICENSE` (MIT), `.claude-plugin/{plugin,marketplace}.json`, `agents/openai.yaml` (Codex marketplace metadata), `scripts/validate-package.py`, `.github/workflows/validate.yml`. **No `references/` directory at all** — a deliberately single-file skill.
- **SKILL.md approach**: taxonomy + procedure + inline examples, all in one file. 33 numbered patterns in five groups (Content / Language-and-Grammar / Style / Communication / Filler-and-Hedging), each pattern = "Words to watch" + "Problem" + Before/After pair. Then a Detection Guidance section (a 13-item false-positive list — "What NOT to flag" — and a "Signs of human writing (preserve these)" list), Voice Calibration (user sample outranks skill rules), a "PERSONALITY AND SOUL" section, three Invocation Modes (pasted / file / embedded), and a 4-step process loop: draft → two self-audit questions ("What makes the below so obviously AI generated?" / "Does the rewrite state any fact… that isn't in the source?") → final rewrite. Frontmatter: `license: MIT`, `metadata.version: "2.9.1"`. Source: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md
- **Scripts**: `scripts/validate-package.py` is a **CI packaging linter, not a runtime tool** — it validates frontmatter portability (hard-fails on `compatibility:` or `allowed-tools:` keys: "Remove nonportable frontmatter key"), version sync across SKILL.md/README/plugin.json, pattern numbering 1–33, and enforces `if len(SKILL.splitlines()) > 500: raise SystemExit("SKILL.md exceeds the 500-line portability budget")`. Run by `.github/workflows/validate.yml`. Source: https://raw.githubusercontent.com/blader/humanizer/main/scripts/validate-package.py
- **License**: MIT, "Copyright (c) 2025 Siqi Chen". https://raw.githubusercontent.com/blader/humanizer/main/LICENSE

### sergebulaev/x-skills — skills/x-humanizer (https://github.com/sergebulaev/x-skills)

- **Structure** (GitHub API tree): monorepo of nine X/Twitter skills; `skills/x-humanizer/` = `SKILL.md` (5,596 B / **127 lines**) + `references/scrub-rules.md` (2,352 B: tiered vocabulary swaps and regex, held as markdown for the model to apply, not an executable) + `references/examples.md` (2,393 B / **71 lines**) + `references/audit-checklist.md` (1,792 B) + `sub-skills/post-audit.md`. Repo-root `lib/*.py` are posting/API clients used by other skills, not by x-humanizer.
- **examples.md format** (https://raw.githubusercontent.com/sergebulaev/x-skills/main/skills/x-humanizer/references/examples.md): four worked **annotated before/after pairs** — each shows Before, an explicit "Tells:" line naming which patterns fire, After, and a "Why it is better" line — closing with a "What to preserve" list. Pure few-shot calibration; tiny.
- **SKILL.md pointer wording**: unconditional but terse — a two-line section `## Example` / "See `references/examples.md` for worked before/after rewrites." plus a `## Files` manifest listing every bundled file with a one-line role ("`references/examples.md` - worked before/after rewrites for tweets and threads"). Not conditional ("if X, read Y") — just a signposted table of contents.
- **License**: MIT, "Copyright (c) 2026 Sergey Bulaev". https://raw.githubusercontent.com/sergebulaev/x-skills/main/LICENSE

### Raymondhou0917/speak-human-tw (https://github.com/Raymondhou0917/speak-human-tw, default branch `master`)

- **Structure**: `SKILL.md` (20,872 B / **230 lines**) + six `references/` files (patterns.md 28,393 B, examples.md 19,392 B, humanize.md, scenes.md, protected-list.md, taiwan-localization.md) + `evals/` (benchmark.md 20,892 B, run-eval.md, results-v*.md) + `install/` per-tool guides + `assets/readme/` images + `scripts/generate_star_history.py` (README star-chart image generator — repo decoration, not skill runtime).
- **examples.md format** (https://raw.githubusercontent.com/Raymondhou0917/speak-human-tw/master/references/examples.md, 401 lines): opens with a TOC of **nine scenarios** (社群貼文, 電子報, 銷售頁, 客服與學員回信, 辦公文書公告, 個人品牌貼文, 電商產品文案, 自我介紹/Bio, Annotation-mode 示範), each holding 1–2 full-text before/after pairs followed by a structured 「改了什麼」 annotation block; header disclaimer 「所有內容為合成範例，價格、名稱、數據皆虛構」.
- **SKILL.md pointer wording**: per-topic inline pointers at the step where each file matters (step 1 → scenes.md, step 2 → protected-list.md, step 4 → patterns.md + taiwan-localization.md) plus a consolidated 「參考導航」 nav list at the end (「分場景 before/after 全文示範：[references/examples.md](references/examples.md)」). It also carries a 「單檔兜底規則」 section: an explicit minimum-behavior fallback for environments that load only SKILL.md without references/ — a portability move worth noting.
- **License**: MIT, "Copyright (c) 2026 Raymond Hou (雷蒙三十)". https://raw.githubusercontent.com/Raymondhou0917/speak-human-tw/master/LICENSE

### Comparison — the job examples.md does

| | blader/humanizer | x-humanizer | speak-human-tw |
|---|---|---|---|
| Where examples live | inline in SKILL.md, one Before/After per pattern | `references/examples.md`, 71 lines | `references/examples.md`, 401 lines |
| Format | pattern-anchored micro-pairs | annotated pairs w/ named tells + "why better" | scenario-anchored full-text pairs + 改了什麼 blocks |
| Job | definition-by-example (part of the taxonomy) | few-shot calibration | few-shot calibration **per scene/register** |
| Test corpus? | no (none in repo) | no | **no — test corpus is separate, in `evals/benchmark.md`** |
| Pointer style | n/a | unconditional "See references/examples.md" + Files manifest | per-step inline pointers + nav list + single-file fallback |

**Verdict (Q2):** All three converge on before/after pairs as the teaching unit; the two multi-file skills keep worked examples in `references/examples.md` as **few-shot calibration only** and keep the test corpus in `evals/` — never mixed. The pattern worth adopting for the rewrite: pattern-anchored micro-pairs stay with their rules (blader's move), full-scenario calibration examples go in a `references/examples.md` with a TOC and scenario anchors (speak-human-tw's move), and SKILL.md points at it from the step where it's needed. Note also blader proves a humanizer fits in 412 lines with examples *included* — evidence the 966-line SKILL.md can shrink dramatically.

---

## Q3. Where does non-runtime / distilled-research material live?

### In the wild

- **The spec names no research/docs convention.** agentskills.io/specification defines `scripts/`, `references/`, `assets/` and then allows "Any additional files or directories" (§Directory structure). `references/` is defined as content "agents can read when needed" — i.e. runtime, on-demand.
- **anthropics/skills** (https://github.com/anthropics/skills, tree scan of all 411 files): no skill contains a `research/` or `docs/` directory. Observed skill-internal dirs: `scripts/` (docx, pptx, pdf, mcp-builder), `reference/` singular (mcp-builder), `examples/` (internal-comms). Provenance/attribution material sits at **repo root** (`THIRD_PARTY_NOTICES.md`), not inside skills.
- **blader/humanizer**: no non-runtime material inside the skill; README.md and AGENTS.md at repo root carry the meta-story.
- **speak-human-tw**: provenance lives in `CHANGELOG.md` (rich per-version derivation notes, including 「比對 blader/humanizer 補齊」) and `evals/results-v*.md` — again outside the runtime files.

### Local repo convention (authoritative for this decision)

- `/Users/leoluyi/.skills/engineering-guidelines.md` §Anatomy (lines 7–19) lists `SKILL.md`, `references/` ("large docs the body points at on demand"), `scripts/`, `evals/` — research/ is not in the diagram, but §intro (line 3) designates `<skill>/design-notes.md` as the per-skill provenance file, and §"Keep development-process noise out of skill content" (lines 164–174) states: "`SKILL.md` and everything under `references/` are runtime instructions the model loads when the skill fires… Provenance belongs in the skill's `design-notes.md`, `evals/judged-cases.md`, commit messages, or `backlog.md`." The repo-root `CLAUDE.md` repeats this as a hard rule.
- **`research/` already exists as a repo convention**: `find` over `/Users/leoluyi/.skills/skills/*/` shows subdir usage counts — evals 10, references 8, **research 2** (avoid-ai-writing-zh, knowledge-doc-writing), scripts 1, hooks 1.
- `/Users/leoluyi/.skills/skills/avoid-ai-writing-zh/research/` currently holds two distilled-source files, both with source-attribution headers, as-of dates, and license notes:
  - `ai-sentence-patterns-zh.md` (15 KB) — paraphrased distillation of 朱宥勳's 〈文字診療室〉 video transcript, marked 「供 skill 開發作為原始材料」.
  - `wikipedia-ai-signs-zh.md` (27 KB) — distillation of zh-Wikipedia 〈AI生成文的特徵〉, CC BY-SA 4.0, marked 「本檔為 skill 開發的**原始素材**」.
- `grep -n "research/" skills/avoid-ai-writing-zh/SKILL.md` → **zero hits**: research/ is non-runtime by construction; the model never loads it when the skill fires.

**Verdict (Q3):** For this repo: runtime rule material the model should load on demand → `references/`; manually-distilled research/source material and provenance → `research/` (sibling of references/), continuing the existing two-skill precedent, with `design-notes.md` for iteration narrative. **Not** `references/research/` — everything under references/ is runtime by both the spec's definition and this repo's hard rule, so nesting research there either pollutes the runtime surface or forces an exception to the rule; it also breaks the one-level-deep pointer hygiene. The spec's "any additional directories" clause makes `research/` fully conformant, and every tool ignores unreferenced files (zero context cost).

---

## Q4. Helper scripts for detection — precedent, doctrine, portability

### Precedent in the four repos

- **None of the three humanizer projects ships a runtime detection script.** blader's only script is the CI packaging linter (Q2); x-humanizer keeps its regex tiers as *markdown* in `references/scrub-rules.md` for the model to apply; speak-human-tw's only script generates a README star chart. speak-human-tw is explicit about why: 「這不是敏感詞替換器…寫不出具體內容的句子，多半該刪，不該改」 and 「模式優先、詞表兜底」 (SKILL.md) — detection is judgment-loaded, phrase lists are the fallback, not the mechanism.
- **anthropics/skills**: scripts appear only in document-machinery skills (docx/pptx/pdf validators and form-fillers, mcp-builder eval harness); the writing-type skill (internal-comms) is instruction+examples only.

### Official doctrine

- Anthropic: scripts for "deterministic operations… fragile and error-prone… consistency is critical" (best-practices, Q1 above); judgment tasks get high-freedom text instructions.
- Codex skills docs (https://learn.chatgpt.com/docs/build-skills, the redirect target of developers.openai.com/codex/build-skills): same directory layout (`scripts/`, `references/`, `assets/`) and, verbatim: "**Prefer instructions over scripts unless you need deterministic behavior or external tooling.**" It makes **no guarantee about the script runtime environment**.

### The `uv` question

- **Codex cloud**: the universal image installs `pyenv, poetry, uv, ruff, black, mypy, pyright, isort` alongside Python when `CODEX_ENV_PYTHON_VERSION` is set — per the reference-image README, https://github.com/openai/codex-universal (table "Configuring language runtimes"). Caveats from the same README: it is "a reference implementation… not an identical environment", and the cloud-environments doc (https://learn.chatgpt.com/docs/environments/cloud-environment) names only "pip, pipenv, and poetry" as auto-detected package managers and covers **cloud only**.
- **Codex CLI / Claude Code local**: both execute on the user's machine with whatever is installed — no doc guarantees `uv` (or any Python) exists. **Claude API code-execution containers**: "No runtime package installation. Only pre-installed packages are available" (Agent Skills overview, §Runtime environment constraints); uv's presence there is unverified.
- The agentskills.io spec treats uv as something a skill must *declare*, not assume: its `compatibility` example is literally `compatibility: Requires Python 3.14+ and uv`.
- Conclusion: **uv is verifiable only for Codex cloud; it is not a safe cross-runtime assumption.** A bundled script must target `python3` + stdlib (regex phrase scanning needs nothing more); the user-level "prefer uv" rule applies to repo tooling, not to a skill's portable runtime surface.

**Verdict (Q4):** A phrase-scanner script is defensible only as an **optional, advisory** enhancement: precedent is uniformly against making it the mechanism, the skill's own doctrine (pattern-over-wordlist, cluster-based judgment, false-positive protection) is judgment-work the docs assign to instructions, and this repo's CLAUDE.md separately forbids hard-failing on "unverified heuristics" — a phrase hit is exactly that, so scanner output can only ever be a warning feeding model judgment. If shipped: stdlib `python3` only, no uv/third-party deps, and SKILL.md must read correctly when the script never runs (never load-bearing, per engineering-guidelines §Portability).

---

## Q5. License / attribution obligations

- **blader/humanizer**: **MIT License**, "Copyright (c) 2025 Siqi Chen" (https://raw.githubusercontent.com/blader/humanizer/main/LICENSE; GitHub license API confirms SPDX `MIT`). Frontmatter also declares `license: MIT`.
- **sergebulaev/x-skills**: **MIT License**, "Copyright (c) 2026 Sergey Bulaev" (https://raw.githubusercontent.com/sergebulaev/x-skills/main/LICENSE; SPDX `MIT`).
- (speak-human-tw, for completeness: MIT, "Copyright (c) 2026 Raymond Hou (雷蒙三十)".)
- The operative MIT term (identical in all three files): "Permission is hereby granted, free of charge… to deal in the Software without restriction… subject to the following conditions: **The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.**"
- What distillation requires: MIT's condition attaches to *copies or substantial portions* of the licensed text. Ideas, methods, and taxonomy *concepts* (e.g. "rule of three", "negative parallelism" as categories) are not copyrightable expression, so a genuine distillation-in-own-words carries no legal notice obligation. The obligation triggers when protected **expression** travels: carried-over wording, before/after example sentences, or close paraphrase at scale ("substantial portions"). Given the rewrite will study blader's 33-pattern taxonomy and detection-guidance lists closely, the safe and honest posture is the one this skill already uses: the existing `NOTICE` file (`/Users/leoluyi/.skills/skills/avoid-ai-writing-zh/NOTICE`) distinguishes "rebased verbatim" (notice preserved in LICENSE) vs "our own rewrite, not copied text" (credited as informed-by) vs "verbatim adaptation" (credited with scope). Extend that same three-tier NOTICE treatment to blader/humanizer and x-humanizer for whatever tier each borrowing lands in.

**Verdict (Q5):** Both are plain MIT. Distilling concepts requires nothing legally; any verbatim or near-verbatim carried text requires preserving the copyright + permission notice; either way, add per-source entries to the skill's existing NOTICE file stating which tier applies — the repo already has the exact template for this.

---

## Appendix: file snapshots used

Local copies fetched 2026-07-29 into `/private/tmp/claude-501/-Users-leoluyi--skills/961d5bc0-b2f8-4698-8b75-e91a79618428/scratchpad/dl/`: `humanizer-SKILL.md`, `humanizer-README.md`, `humanizer-LICENSE`, `humanizer-validate.py`, `xh-SKILL.md`, `xh-examples.md`, `xh-scrub-rules.md`, `xh-audit.md`, `xskills-LICENSE`, `sht-SKILL.md`, `sht-examples.md`, `sht-LICENSE`.

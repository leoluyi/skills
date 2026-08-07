# Naming and placing the root-level `engineering-guidelines.md` — is there a convention?

Researched 2026-08-07. Question: judging by what `engineering-guidelines.md` actually contains, is there an established real-world convention for what a file like it should be named, and where it should live?

Primary sources consulted, all fetched during this research:

- **agents.md** — the open AGENTS.md format: <https://agents.md/> and its source repo <https://github.com/agentsmd/agents.md> (`README.md` fetched raw).
- **Claude Code memory docs** — <https://code.claude.com/docs/en/memory> (the canonical URL; `https://docs.claude.com/en/docs/claude-code/memory` 301-redirects here).
- **OpenAI Codex AGENTS.md docs** — <https://learn.chatgpt.com/docs/agent-configuration/agents-md> (reached via 308 redirect from `https://developers.openai.com/codex/guides/agents-md`); plus `openai/codex`'s own `docs/agents_md.md` and root `AGENTS.md`, fetched raw from GitHub.
- **Cursor rules docs** — <https://cursor.com/docs/context/rules>.
- **GitHub docs** — community health files (<https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file>), contributing guidelines (<https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors>), READMEs (<https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes>).
- **matklad, "ARCHITECTURE.md"** — <https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html>.
- **GNU Coding Standards, §7.3 Making Releases** — <https://www.gnu.org/prep/standards/html_node/Releases.html>.
- **Repo file listings via the GitHub contents API** — `google/eng-practices`, `google/styleguide`, `kubernetes/kubernetes`, `kubernetes/community` (`contributors/devel/`), `rust-lang/rust`, `rust-lang/rust/src/doc/style-guide/src`, `rust-lang/rustc-dev-guide`, `python/devguide`, `anthropics/skills`, `openai/codex`, `mattpocock/skills`.
- **This repo**, read in full before any external research: `engineering-guidelines.md`, `AGENTS.md` (with `CLAUDE.md` a symlink to it), `CONTRIBUTING.md`, `README.md`, `.agents/invocation.md`, `.agents/writing-docs.md`, `backlog.md`, `skills/plain-speak/design-notes.md`, `.gitignore`, `.github/workflows/`.

---

## 0. What the file actually is

Before asking what it should be called, here is an honest characterization of the 211-line file, drawn from reading it rather than from its name.

**Audience: both, with the agent as the primary reader.** The file's own first paragraph frames it as the reference tier of an agent-instruction stack: "The repo-wide authoring guide. The always-loaded `CLAUDE.md` carries only the hard prohibitions; this file is the reference behind them." (`engineering-guidelines.md:3`). `AGENTS.md:3` points at it from the other side — "For all other skill-development principles — anatomy, frontmatter gotchas, naming, portability, language strategy, and test discipline — see **[engineering-guidelines.md](engineering-guidelines.md)**" — and five of `AGENTS.md`'s six bullets close with a deep link into one of its headings. But the human path is real too: `CONTRIBUTING.md:13` instructs a would-be PR author to "Read **[engineering-guidelines.md](engineering-guidelines.md)** — the full authoring guide", and the published catalog site links it in its nav as "Authoring guide" / 撰寫指南 (`docs/index.template.html:132`, `docs/guide.template.html:78`). Its register is instruction-to-an-implementer throughout — imperative headings ("Write generative-first", "Shape the body"), executable detection commands (`rg -l '\\u[0-9A-F]{4}' skills/*/SKILL.md`), and a "Finishing check before finalizing a skill edit" — not narrative explanation aimed at a reader who will not act.

**Genre: craft/authoring guidance for the repo's product, plus internal repo standards.** Roughly: skill anatomy and the frontmatter gotcha (§Anatomy), a seven-stage lifecycle, naming, invocation modes, two long craft sections on how a skill should sound and be shaped (§Write generative-first, §Shape the body), language strategy including a canonical copy-source block for the leakage guard, severity rules for scripted checks, a `scripts/` vs `tools/` placement doctrine, portability constraints with a per-tool support matrix, eval/test discipline, maintenance cadence, catalog upkeep, a rule about keeping dev-process noise out of runtime files, and skill dependency direction. That is not code style in the language sense (no formatting rules for Python or shell), not contribution process (that lives in `CONTRIBUTING.md`), and not architecture (there is no codemap of the repo's own code — `tools/` is described by *policy*, in §"Where a tool lives", not by *layout*). The closest single label is a **craft-and-standards authoring guide for the artifacts this repo ships**.

**Division of responsibility with its neighbours.** Four tiers exist and are cleanly separated:

- `AGENTS.md` (31 lines, symlinked as `CLAUDE.md`) — always-loaded hard prohibitions: five "Never …" bullets, each with a deep link into `engineering-guidelines.md` for the reasoning, plus the repo-wide caveman response-style rule.
- `engineering-guidelines.md` (211 lines) — the long-form reference the prohibitions point back to, plus everything not reduced to a prohibition.
- `CONTRIBUTING.md` (71 lines, bilingual EN + 繁中) — outside-contributor process: what to read first, the four-item merge bar, clone/setup commands, `tools/new-skill`.
- `.agents/invocation.md` (22 lines) and `.agents/writing-docs.md` (86 lines) — topic-specific long-form references one level deeper, each linked from `engineering-guidelines.md` (§Invocation modes → `.agents/invocation.md`; §Catalog upkeep → `.agents/writing-docs.md`). Note that `.agents/invocation.md` carries a provenance header naming `mattpocock/skills` as its source.

So `engineering-guidelines.md` is the **middle tier of a three-level progressive-disclosure stack**, and `.agents/*.md` files are its siblings in genre, sitting one level below it.

---

## 1. Is there a named convention for agent-facing instruction files?

### 1.1 AGENTS.md — the open format

The format is owned, as of this research, by a foundation rather than a vendor: "**AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation**" (<https://agents.md/>). Its self-description is "**a simple, open format for guiding coding agents**", and the analogy it uses is "**Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide context and instructions to help AI coding agents work on your project**" (<https://github.com/agentsmd/agents.md> `README.md`, and the same wording on the site).

On **location**: "**Create an AGENTS.md file at the root of the repository.**" On **nesting**, the only structural mechanism it defines is per-package files, not a link-out: "**Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree.**"

On **what belongs in it**, the site lists popular sections — "Project overview, Build and test commands, Code style guidelines, Testing instructions, Security considerations" — plus "Commit messages or pull request guidelines, security gotchas, large datasets, deployment steps."

On **linking out to a deeper reference file, the spec is silent.** It says only "**AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide.**" There is no named role, no prescribed filename, and no recommendation either for or against factoring long material into a separate file. The spec's only answer to "the file is getting long" is nesting by directory, which does not fit a repo-wide authoring guide that applies to every skill equally.

### 1.2 Claude Code — CLAUDE.md and its deeper tiers

Claude Code's memory documentation (<https://code.claude.com/docs/en/memory>) is the most explicit of the three on the "root file is short, detail goes elsewhere" idea, and it is the only source that names concrete mechanisms for the deeper tier — but it names **directories and mechanisms, never a filename for a long-form guide**.

Locations and precedence are tabulated "in load order, from broadest scope to most specific": managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md`, `/etc/claude-code/CLAUDE.md`, `C:\Program Files\ClaudeCode\CLAUDE.md`), user instructions (`~/.claude/CLAUDE.md`), project instructions (`./CLAUDE.md` or `./.claude/CLAUDE.md`), local instructions (`./CLAUDE.local.md`).

On **what belongs in the root file**: "**Keep it to facts Claude should hold in every session: build commands, conventions, project layout, 'always do X' rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a [skill] or a [path-scoped rule] instead.**"

On **size**: "**Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence.**" This repo's `AGENTS.md` is 31 lines, comfortably inside that; `engineering-guidelines.md` at 211 lines would not be, which is itself an argument for the split the repo already made.

On the **deeper tier**, three mechanisms are named:

- `.claude/rules/` — "**For larger projects, you can organize instructions into multiple files using the `.claude/rules/` directory.**" Files may carry `paths:` frontmatter to load only when Claude touches matching files; "Rules without a `paths` field are loaded unconditionally."
- Imports — "**CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.**" Crucially, the docs warn this does not buy a context saving: "**Splitting into [`@path` imports] helps organization but doesn't reduce context, since imported files load at launch.**"
- Skills — "For task-specific instructions that don't need to be in context all the time, use [skills] instead, which only load when you invoke them or when Claude determines they're relevant to your prompt."

Note what this repo does *not* do: `AGENTS.md` links to `engineering-guidelines.md` with an ordinary Markdown link, not an `@import`. Under this documentation that is the correct choice for a 211-line reference — an `@import` would load all 211 lines into every session, which is exactly the cost the split exists to avoid.

The docs also confirm the repo's `CLAUDE.md → AGENTS.md` symlink is a sanctioned pattern: "**Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it … A symlink also works if you don't need to add Claude-specific content:** `ln -s AGENTS.md CLAUDE.md`".

**No name is given for a long-form Markdown reference sitting outside `.claude/rules/`.** The documentation's vocabulary for the deeper tier is "rules", "imports", and "skills" — all of which are mechanisms with defined loading semantics, none of which describes a plain document a human also reads.

### 1.3 Codex

Codex's discovery order is "**Global scope:** `~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md`" then "**Project scope:** Starting from Git root down to current directory, checking for `AGENTS.override.md`, then `AGENTS.md`", with "**Merge order:** Files concatenate from root downward, with closer files overriding earlier guidance" (<https://learn.chatgpt.com/docs/agent-configuration/agents-md>).

Its only size mechanism is a byte cap, not a style recommendation: "**Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default).**" The remedy it offers is to raise the cap or "split instructions across nested directories" — again, nesting by directory, not a named reference file.

On linking out versus inlining, the page is **silent**; it addresses discovery and precedence only. Codex's own repo confirms it in practice: `openai/codex`'s `docs/agents_md.md` is a one-line stub ("For information about AGENTS.md, see [this documentation](https://developers.openai.com/codex/guides/agents-md).") and its root `AGENTS.md` inlines everything — dozens of Rust-specific conventions, module-size rules, lint invocations — with no link-out to a companion guide.

### 1.4 Cursor

Cursor is the only vendor of the four that states the link-out principle as advice, and it still names no filename: "**Reference files instead of copying their contents—this keeps rules short and prevents them from becoming stale as code changes**" and "**Keep rules under 500 lines**" (<https://cursor.com/docs/context/rules>). Its structural mechanism is again a directory of topic files, `.cursor/rules/*.mdc`, plus `@filename.ts`-style references. It supports nested AGENTS.md: "**Nested `AGENTS.md` support in subdirectories is now available. You can place `AGENTS.md` files in any subdirectory of your project, and they will be automatically applied when working with files in that directory or its children.**"

### 1.5 Verdict on Q1

**No agent-instruction spec names a convention for the role `engineering-guidelines.md` occupies.** All four sources converge on the *principle* — the root file is short and always-loaded, detail lives elsewhere — and all four name only **directory-based** mechanisms for "elsewhere" (`.claude/rules/`, `.cursor/rules/`, nested `AGENTS.md` per package, Codex's nested directories), each of which is scoped by *path* or *loading policy*, not by *topic*. A single repo-wide, topic-scoped, human-and-agent-readable reference document is a shape none of them has vocabulary for. This is a genuine silence in the primary sources, not a convention this repo is failing to follow.

The closest thing to a precedent is not a spec but a repo: **`mattpocock/skills`**, which this repo demonstrably borrows from (`.agents/invocation.md` carries the header `<!-- Source: https://github.com/mattpocock/skills/blob/main/.agents/invocation.md (MIT License) -->`, and `engineering-guidelines.md:80` cites `writing-great-skills` as one of its two external standards). Its root listing (GitHub contents API) is: `.agents`, `.changeset`, `.claude-plugin`, `.github`, `.gitignore`, `.out-of-scope`, `AGENTS.md`, `CHANGELOG.md`, `CLAUDE.md`, `CONTEXT.md`, `LICENSE`, `README.md`, `docs`, `package-lock.json`, `package.json`, `scripts`, `skills`. Its `.agents/` directory contains `adr/`, `install-block.md`, `invocation.md`, `writing-docs.md`. Two observations:

1. Its symlink runs the **opposite** direction from this repo — raw `AGENTS.md` fetches as the literal string `CLAUDE.md`, i.e. `AGENTS.md` is the symlink and `CLAUDE.md` is the real file. (This repo does it the other way, which is the direction Claude Code's docs illustrate.)
2. It has **no root-level long-form guide at all.** Its `CLAUDE.md` carries the repo-organisation detail inline (bucket folders, README/plugin-manifest sync obligations, docs-page obligations, invocation), and everything factored out sits in `.agents/` — including `.agents/writing-docs.md`, the exact file this repo copied. Its `CONTEXT.md` is a different genre again: a domain-model / ubiquitous-language file ("Issue tracker", "Decision ticket", "Triage role", with an explicit "Flagged ambiguities" section), not an authoring guide.

So the one repo in this lineage that has solved the same problem put the long-form material in `.agents/`, with kebab-lowercase filenames, and kept nothing of that genre at root. That is one repo's practice, not a convention — but it is the most directly comparable evidence available, and this repo has already adopted half of it.

---

## 2. Is there a convention for human-facing contributor documentation of this genre?

Checked by listing the actual file trees of the named projects rather than trusting summaries.

### 2.1 `CONTRIBUTING.md` — process, and the only name with a machine-readable definition

GitHub's own documentation defines it: "**To help your project contributors do good work, you can add a file with contribution guidelines to your project repository's root, `docs`, or `.github` folder.**" Content it suggests: "Steps for creating good issues or pull requests. Links to external documentation, mailing lists, or a code of conduct. Community and behavioral expectations." Precedence when duplicated: "**If a repository contains more than one *CONTRIBUTING* file, then the file shown in links is chosen from locations in the following order: the `.github` directory, then the repository's root directory, and finally the `docs` directory.**" (<https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors>)

This is the one filename in the whole question that a platform actually *recognizes*. Note that GitHub's suggested contents explicitly include "**Links to external documentation**" — i.e. GitHub's own model of `CONTRIBUTING.md` is a short process door that points outward, which is precisely how this repo uses it.

The recognized community-health set is enumerated as `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, discussion category forms, `FUNDING.yml`, `GOVERNANCE.md`, issue/PR templates with `config.yml`, `SECURITY.md`, `SUPPORT.md`, searched in "**The `.github` folder / The root of the repository / The `docs` folder**" (<https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file>). **Neither `STYLE.md`, `STYLEGUIDE.md`, `DEVELOPMENT.md`, nor `ARCHITECTURE.md` is on that list** — none of them is recognized by the platform; they are pure community habit.

### 2.2 Style guides — the name denotes *language formatting*, not craft

`google/styleguide` root listing (contents API): `Rguide.md`, `csharp-style.md`, `cppguide.html`, `docguide/`, `go/`, `htmlcssguide.html`, `javaguide.html`, `jsguide.html`, `objcguide.md`, `pyguide.md`, `shellguide.md`, `tsguide.html`, plus editor configs and XSL. Every filename is `<language>guide` — the unit of a "style guide" at Google is *one programming language*. There is no file named `STYLE.md` or `STYLEGUIDE.md` at all.

`rust-lang/rust` root listing contains no `STYLE.md` either: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `COPYRIGHT`, `INSTALL.md`, `LICENSE-APACHE`, `LICENSE-MIT`, `README.md`, `RELEASES.md`, plus build files. Rust's actual style guide lives at `src/doc/style-guide/src/` with kebab-lowercase chapter files: `advice.md`, `cargo.md`, `editions.md`, `expressions.md`, `items.md`, `nightly.md`, `principles.md`, `statements.md`, `types.md`.

**So `STYLE.md`/`STYLEGUIDE.md` denotes formatting and idiom rules for a programming language.** `engineering-guidelines.md` contains nothing of that kind. This name does not fit.

### 2.3 Google's `eng-practices` — the name is close, the genre is not

`google/eng-practices` root: `review/`, `README.md`, `LICENSE`, `_config.yml`, `.github/workflows/`. The repo describes its contents as documents that "represent our collective experience of various best practices that we have developed over time", and today it holds exactly two guides, both about code review: The Code Reviewer's Guide (`review/reviewer/index.md`) and The Change Author's Guide (`review/developer/index.md`).

This is worth flagging because "engineering practices" / "engineering guidelines" as a *phrase* is most strongly associated, in the primary sources, with **code-review standards** — a genre this file does not contain. There is no repo-level file named `ENGINEERING_GUIDELINES.md` or `engineering-guidelines.md` in any of the projects surveyed; the phrase names a whole repository at Google, not a file.

### 2.4 `DEVELOPMENT.md` / `docs/development.md` — build-and-run setup

`kubernetes/community` `contributors/devel/` listing: `OWNERS`, `README.md`, `automation.md`, `development.md`, `running-locally.md`, plus per-SIG subdirectories (`sig-api-machinery`, `sig-architecture`, `sig-cli`, …). `development.md` there is the "how do I build and run this" document — its siblings `running-locally.md` and `automation.md` make the genre unambiguous.

`kubernetes/kubernetes` root, for the casing question below, is: `AGENTS.md`, `CHANGELOG.md`, `CHANGELOG/`, `CONTRIBUTING.md`, `LICENSE`, `LICENSES/`, `Makefile`, `OWNERS`, `OWNERS_ALIASES`, `README.md`, `SECURITY_CONTACTS`, `SUPPORT.md`, `code-of-conduct.md`, `docs/`, plus source trees. Its root `AGENTS.md` (fetched raw) inlines everything — "Communication Preferences", "Constraints", "Contributor Guidelines", "Commands", "Style" — with no link-out to a longer guide.

`python/devguide` is a whole separate repository, structured as a Sphinx book with **lowercase directory names**: `core-team/`, `developer-workflow/`, `development-tools/`, `documentation/`, `getting-started/`, `internals.rst`, `security/`, `testing/`, `triage/`, `versions.rst`. Its only uppercase root files are `LICENSE` and `README.rst`.

`rust-lang/rustc-dev-guide` is likewise a separate repository, an mdBook whose chapters live in `src/` with kebab-lowercase names: `about-this-guide.md`, `conventions.md`, `contributing.md`, `compiler-team.md`, `diagnostics.md`, `getting-started.md`, `git.md`, and so on. Its root has only `CODE_OF_CONDUCT.md`, `LICENSE-APACHE`, `LICENSE-MIT`, `README.md`, `CITATION.cff` in uppercase.

**The recurring pattern across all three large projects is the same:** when contributor craft guidance grows past a page, it becomes a *book* — a directory or a separate repo — whose chapter files are **lowercase kebab-case Markdown**, and the SCREAMING_CASE root files are reserved for the short, platform-recognized doors (`README`, `CONTRIBUTING`, `LICENSE`, `CODE_OF_CONDUCT`, `SECURITY`).

### 2.5 What each recurring name conventionally denotes

Summarizing the evidence above:

| Name | What it conventionally denotes | Primary evidence |
|---|---|---|
| `CONTRIBUTING.md` | Process for outside contributors; platform-recognized; expected to link outward | GitHub docs (recognized filename, root/`docs`/`.github`) |
| `STYLE.md` / `STYLEGUIDE.md` / `<lang>guide.md` | Formatting and idiom rules for one programming language | `google/styleguide`; `rust-lang/rust/src/doc/style-guide/` |
| `DEVELOPMENT.md` / `docs/development.md` | Build, run, and local-dev setup | `kubernetes/community/contributors/devel/development.md` alongside `running-locally.md` |
| `docs/…` book with kebab chapters | Long-form contributor craft/reference guidance | `python/devguide`, `rust-lang/rustc-dev-guide` |
| `ARCHITECTURE.md` | Codemap of the system's own code — see §3 | matklad |
| `AGENTS.md` / `CLAUDE.md` | Agent instruction file; exact casing is load-bearing — see §4 | agents.md, Codex, Claude Code docs |

None of these denotes "the long-form craft guide behind a short agent-instruction file." That role has no conventional name in the human-documentation tradition either.

---

## 3. Does `ARCHITECTURE.md` apply?

No. The primary source is unambiguous about what the file is for, and it is a different thing.

matklad prescribes, in order (<https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html>):

1. "**Start with a bird's eye overview of the problem being solved.**"
2. "**Specify a more-or-less detailed _codemap_. Describe coarse-grained modules and how they relate to each other.**"
3. "**The codemap should answer 'where's the thing that does X?'. It should also answer 'what does the thing that I am looking at do?'**"
4. "**Explicitly call-out architectural invariants.**"
5. "**Point out boundaries between layers and systems as well.**"
6. "**After finishing the codemap, add a separate section on cross-cutting concerns.**"

Audience: "**Every recurring contributor will have to read it.**" What to leave out: "**Avoid going into details of _how_ each module works, pull this into separate documents or (better) inline documentation.**" On links: "**Do _not_ directly link them (links go stale)**" — instead, "_Do_ name important files, modules, and types … encourage the reader to use symbol search to find the mentioned entities by name." Scope discipline: "**A codemap is a map of a country, not an atlas of maps of its states.**" Length: "**Keep it short … the shorter it is, the less likely it will be invalidated by some future change.**"

Measured against that, `engineering-guidelines.md` fails almost every criterion. It contains no codemap; it never answers "where's the thing that does X?" for this repo's own code; it names no modules or types; it declares no architectural invariants of the codebase. The one passage that even resembles a layout statement — the §Anatomy ASCII tree — describes the shape of *a skill this repo produces*, not the shape of this repo. And its §"Where a tool lives — `scripts/` vs `tools/`" is a *placement policy for future work*, the opposite of a descriptive map. Most tellingly, the file is dense with exactly what matklad says to pull out ("details of _how_ each module works") and full of direct links, which he advises against.

`ARCHITECTURE.md` is the wrong name for this content.

---

## 4. Casing convention for root-level Markdown

The repo's root mixes `README.md`, `README.zh-TW.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `LICENSE` against `backlog.md` and `engineering-guidelines.md`. There is a coherent rule behind that split, and it is supported by primary sources.

**The uppercase tradition originates in the GNU Coding Standards**, which prescribe specific uppercase filenames for a distribution: "**The distribution should contain a file named README with a general overview of the package**", whose contents must include "the name of the package", "the version number", "a general description of what the package does", "**a reference to the file INSTALL**, which should in turn contain an explanation of the installation procedure", "a brief explanation of any unusual top-level directories or files, or other hints for readers to find their way around the source", and "a reference to the file which contains the copying conditions. **The GNU GPL, if used, should be in a file called COPYING.** If the GNU LGPL is used, it should be in a file called `COPYING.LESSER`." (<https://www.gnu.org/prep/standards/html_node/Releases.html>, §7.3). This is where SCREAMING_CASE-at-root comes from: these were the files a human unpacking a tarball needed to find first, and uppercase sorts them to the top in `ls`.

**GitHub's recognition is by name, in specific directories, but explicitly not by case for CONTRIBUTING.** The docs state flatly: "**Contributing guidelines filenames are not case sensitive.**" The accepted forms listed are `CONTRIBUTING` at root, `docs/CONTRIBUTING`, `.github/CONTRIBUTING`. For READMEs the docs say "**If you put your README file in your repository's hidden `.github`, root, or `docs` directory, GitHub will recognize and automatically surface your README to repository visitors**" and refer to the file generically as "README file" — **the page does not state a casing requirement**, which is a silence worth naming rather than papering over. So for `README` and `CONTRIBUTING`, uppercase is a strong convention with platform-level tolerance, not a hard requirement.

**For the agent files, casing *is* load-bearing.** This is the sharpest finding of §4:

- agents.md: "**Create an AGENTS.md file at the root of the repository.**" The literal name is what agents look for.
- Codex resolves by exact filename, checking "`AGENTS.override.md`, then `AGENTS.md`" walking from Git root down.
- Claude Code: "**Claude Code reads `CLAUDE.md`, not `AGENTS.md`**" — a name-exact lookup, which is why the docs prescribe either `@AGENTS.md` in a `CLAUDE.md` or `ln -s AGENTS.md CLAUDE.md`.

None of the three publishes a case-insensitivity guarantee. On a case-sensitive filesystem, `agents.md` would not be found by a tool globbing for `AGENTS.md`. So `AGENTS.md` and `CLAUDE.md` are uppercase because a *machine* requires the exact string; `README.md`, `CONTRIBUTING.md`, and `LICENSE` are uppercase because a *platform and a 40-year tradition* expect it.

**Which leaves `backlog.md` and `engineering-guidelines.md` in the residual class: ordinary project documents that no tool or platform looks up by name.** For that class the surveyed projects use lowercase — `kubernetes/kubernetes` has `code-of-conduct.md` (lowercase) at root beside its uppercase `CONTRIBUTING.md`/`SUPPORT.md`; `python/devguide` uses lowercase directories throughout; `rustc-dev-guide` and Rust's style guide use kebab-lowercase chapter files; `mattpocock/skills` uses kebab-lowercase inside `.agents/`. **The repo's existing casing rule — uppercase iff something outside the repo recognizes the exact name, lowercase kebab otherwise — is internally consistent and matches what the surveyed projects do.** `engineering-guidelines.md`'s lowercase kebab is correct under that rule, and renaming it to `ENGINEERING_GUIDELINES.md` would be a regression, since nothing recognizes that name.

---

## 5. Recommendation, and the concrete migration cost

### 5.1 Recommendation

**Keep the file where it is, and keep the lowercase kebab casing. If anything is worth changing, it is the word "engineering", not the file's location or its case — and even that is an accuracy argument, not a convention argument.**

The reasoning, stated plainly:

- **There is no convention being violated.** §1 establishes that no agent-instruction spec names this role; §2 establishes that no human-documentation tradition names it either. When four vendor specs and five major projects are all silent on a shape, the honest conclusion is that the shape has no name yet — not that the repo picked the wrong one.
- **The casing is already right** (§4). Lowercase kebab is the correct class for a file no tool resolves by name, and it matches `backlog.md` beside it.
- **The conventional alternatives are all wrong for the content.** `ARCHITECTURE.md` describes a codemap (§3). `STYLE.md`/`STYLEGUIDE.md` describes language formatting (§2.2). `DEVELOPMENT.md` describes build-and-run setup (§2.4). `CONTRIBUTING.md` is taken, correctly, by the process door. `docs/` is unavailable here for an unrelated reason: it is the GitHub Pages build tree, and `.gitignore` lists `docs/index.html`, `docs/skills.json`, `docs/guide/` as generated output — dropping a hand-written guide into it would collide with the generator's territory.
- **The one substantive counter-argument is placement, not naming.** `.agents/` already exists and already holds this exact genre — `invocation.md` and `writing-docs.md`, both linked *from* `engineering-guidelines.md`, both kebab-lowercase, one of them copied from `mattpocock/skills`, the single repo in this lineage that solved the same problem and put *all* its long-form material in `.agents/` with nothing of the genre left at root (§1.5). Moving to `.agents/authoring-guide.md` would make the repo's own structure self-consistent: one root instruction file, everything long-form one level down in `.agents/`. Against that: `.agents/` is a dotfolder, hidden from casual browsing; `CONTRIBUTING.md` sends a *human* there as step 2 of two; `README.md` documents it in the root layout block; and the published site links it as the "Authoring guide". For a file with a real human audience, root is the more discoverable home. This is a genuine trade-off with no convention to settle it — I lean toward leaving it at root, but a maintainer who values structural consistency over discoverability could reasonably decide the other way.
- **On the word "engineering":** the file's own first line calls itself "The repo-wide authoring guide"; `README.md:175` and `CONTRIBUTING.md:13` both call it "the full authoring guide"; the docs site nav calls it "Authoring guide" / 撰寫指南. Four independent descriptions say *authoring guide*; only the filename says *engineering guidelines* — and §2.3 shows that phrase is most strongly associated with code-review standards (`google/eng-practices`), a genre the file does not contain. `authoring-guide.md` would name the file what everything else in the repo already calls it. But this is a taste-and-accuracy improvement, not a convention fix, and it costs exactly as much as any other rename.

**Bottom line: no rename is required by any convention. If a rename happens anyway, it should be for accuracy (`authoring-guide.md`) or for structural consistency (`.agents/authoring-guide.md`), both at the same migration cost, enumerated below.**

### 5.2 Migration cost — every reference, by file and line

Produced by `rg -n 'engineering-guidelines' --hidden -g '!.git' .` at the worktree root. Every hit below breaks on a rename or a move. Sixteen call sites across fifteen distinct files (`CLAUDE.md` is a symlink to `AGENTS.md`, so its seven hits are the same seven bytes on disk and are counted once).

**Live cross-references that must be updated:**

| File | Line | Kind of reference |
|---|---|---|
| `AGENTS.md` | 3 | Markdown link, plain: `[engineering-guidelines.md](engineering-guidelines.md)` |
| `AGENTS.md` | 5 | Markdown link **with anchor**: `(engineering-guidelines.md#gotcha-frontmatter-must-be-real-utf-8-never-u-escapes)` |
| `AGENTS.md` | 7 | Markdown link **with anchor**: `(engineering-guidelines.md#keep-development-process-noise-out-of-skill-content)` |
| `AGENTS.md` | 9 | **Two** Markdown links with anchors: `(engineering-guidelines.md#portability)` and `(engineering-guidelines.md#skill-self-sufficiency-and-dependency-direction)` |
| `AGENTS.md` | 11 | Markdown link **with anchor**: `(engineering-guidelines.md#test-discipline)` |
| `AGENTS.md` | 13 | Markdown link **with anchor**: `(engineering-guidelines.md#scripted-checks--severity-and-trust)` |
| `AGENTS.md` | 31 | Bare filename in prose (the caveman repo-exception list naming files written in normal prose) |
| `CONTRIBUTING.md` | 13 | Markdown link, plain (English section) |
| `CONTRIBUTING.md` | 48 | Markdown link, plain (繁中 section) |
| `README.md` | 153 | Bare filename inside the fenced `### Layout` tree, with an aligned trailing comment |
| `README.md` | 175 | Markdown link, plain |
| `README.zh-TW.md` | 148 | Bare filename inside the fenced 目錄結構 tree, with an aligned trailing comment |
| `README.zh-TW.md` | 170 | Markdown link, plain |
| `docs/index.template.html` | 132 | **Absolute GitHub URL**: `https://github.com/leoluyi/skills/blob/main/engineering-guidelines.md`, link text "Authoring guide" / 撰寫指南 |
| `docs/guide.template.html` | 78 | **Absolute GitHub URL**, same target and link text |
| `.clinerules/caveman.md` | 17 | Bare filename in the mirrored caveman repo-exception paragraph |
| `.github/copilot-instructions.md` | 17 | Bare filename, same mirrored paragraph |
| `.opencode/AGENTS.md` | 17 | Bare filename, same mirrored paragraph |
| `.windsurf/rules/caveman.md` | 21 | Bare filename, same mirrored paragraph |
| `.cursor/rules/caveman.mdc` | 22 | Bare filename, same mirrored paragraph |

**Historical references that should probably be left alone, and would go stale:**

| File | Line | Note |
|---|---|---|
| `skills/infographic-design/design-notes.md` | 121 | Prose reference: 「借用規矩見根層 engineering-guidelines.md 的『Borrow battle-tested content verbatim』」 — a dated design note |
| `skills/infographic-design/design-notes.md` | 153 | Prose reference: 「`engineering-guidelines.md`(全域撰寫指南)另一個 commit」 |
| `skills/plain-speak/design-notes.md` | 135 | Prose reference to the file's own standard, inside a dated iteration log |
| `skills/plain-speak/evals/results-2026-07-28-plan-concreteness.md` | 41 | Prose reference inside a dated eval result |
| `skills/humanizer-zh/research/research-humanizer-landscape-2026-07-29.md` | 110 | **Absolute path** `/Users/leoluyi/.skills/engineering-guidelines.md`, cited with line numbers (`§Anatomy (lines 7–19)`, `§… (lines 164–174)`) as evidence in a research note |

That last one is the awkward case. `CLAUDE.md:31` states the repo rule for `research/`: "it holds faithful distillations of outside sources with provenance headers and citations — never compress, paraphrase, or trim those; source fidelity is the whole point of the file." A research note's citation is a record of what a file was called and said on 2026-07-29; editing it to match a later rename falsifies the record, and leaving it makes the citation unresolvable. The same tension applies more weakly to the four `design-notes.md` / `results-*.md` hits, which are dated iteration logs. **A rename therefore leaves at least five permanently stale historical references, or forces a documented decision to rewrite provenance.** That cost is not recoverable by any amount of care and is, in my view, the single strongest practical argument against renaming a file this well-established.

**Anchors: yes, six of them exist and all six break on a rename.** The anchor *fragments* survive (they are derived from `engineering-guidelines.md`'s own headings, which a rename does not touch), but the *file half* of each link must be rewritten. The six are `#gotcha-frontmatter-must-be-real-utf-8-never-u-escapes`, `#keep-development-process-noise-out-of-skill-content`, `#portability`, `#skill-self-sufficiency-and-dependency-direction`, `#test-discipline`, `#scripted-checks--severity-and-trust` — all in `AGENTS.md`, i.e. all in the always-loaded file, where a broken link costs the most. Note also the file's internal self-links (`engineering-guidelines.md:50` → `#test-discipline`, `:62` → `#portability`, `:64` → `#test-discipline`, `:100` → `#gotcha-frontmatter-must-be-real-utf-8-never-u-escapes`, `:143` → `#portability`, `:174` → `#invocation-modes`): those are bare-fragment links and survive a rename untouched.

**Tools and CI: no hits.** The repo-wide `rg` returned nothing under `tools/` or `.github/workflows/` (`docs-check.yml`, `eval-labels.yml`, `invocation-check.yml`, `pages.yml`). No script, gate, or workflow resolves this filename, so a rename would not break the build — it would break only documentation links, none of which any CI check verifies. That is worth stating explicitly, because it cuts both ways: the rename is *cheap to execute* and *silently fragile*, since nothing would catch a missed reference.

**Total: 20 live call sites across 14 files (counting `CLAUDE.md` once with `AGENTS.md`), of which 6 carry anchors and 2 are absolute GitHub URLs inside HTML templates that feed the published Pages site; plus 5 historical references in `design-notes.md`, `evals/results-*.md`, and `research/` that repo convention says not to rewrite.**

---

## Where the primary sources genuinely disagree, or are silent

Stated explicitly rather than smoothed over:

1. **Silent — the central question.** No primary source names the role `engineering-guidelines.md` occupies. agents.md addresses it only with "AGENTS.md is just standard Markdown"; Codex's page covers discovery and a 32 KiB cap and nothing about factoring; Claude Code names `.claude/rules/`, `@imports`, and skills — three mechanisms, no document convention; Cursor states the principle ("Reference files instead of copying their contents") but names no file. The role has no conventional name.
2. **Silent — README casing.** GitHub's README documentation specifies the directories it searches (`.github`, root, `docs`) and their precedence, but does not state a filename-casing rule, unlike the CONTRIBUTING page which explicitly says filenames "are not case sensitive." I did not find a GitHub statement either way on README casing, so the uppercase convention for `README.md` rests on the GNU tradition (§4) and universal practice, not on a platform requirement.
3. **Silent — case-sensitivity of `AGENTS.md` / `CLAUDE.md`.** All three vendor docs use the uppercase name exclusively and none publishes a case-insensitivity guarantee. The claim in §4 that casing is load-bearing for these two is an inference from name-exact lookup wording ("Claude Code reads `CLAUDE.md`, not `AGENTS.md`"; Codex "checking for `AGENTS.override.md`, then `AGENTS.md`"), not a quoted guarantee. Treat it as strongly implied, not documented.
4. **Divergent practice, not a disagreement of specs — inline vs. link out.** Cursor advises referencing files to keep rules short and caps rules at 500 lines; Claude Code targets "under 200 lines per CLAUDE.md file"; but the two largest real AGENTS.md files surveyed do the opposite. `openai/codex`'s root `AGENTS.md` inlines dozens of detailed Rust conventions with no link-out, and `kubernetes/kubernetes`'s root `AGENTS.md` inlines all five of its sections. Codex's docs set a 32 KiB budget with no style advice at all. So the "short root file, long linked reference" pattern this repo follows is **endorsed by two vendors and ignored by two flagship repos** — it is defensible, but it is not universal practice, and no source calls the opposite a mistake.
5. **A single repo, not a convention — `.agents/`.** The `.agents/` directory is not defined by any spec I could find. It appears in `mattpocock/skills` (whence this repo copied `invocation.md` and `writing-docs.md`) and is used here, and that is the extent of the evidence. The §5.1 placement argument rests on one repo's practice plus this repo's own existing structure, and should be weighed as such — it is precedent, not convention.
6. **Ambiguous by nature — the file's audience.** The characterization in §0 that the file serves agent and human roughly equally is my reading of its register and its inbound links, not something any source adjudicates. A maintainer who considers it agent-first would find the `.agents/` move more attractive; one who considers it human-first would keep it at root. The evidence supports both readings.

# Are `tools/run-eval` and `tools/run-case` correctly named? — eval-tooling naming conventions

Researched 2026-08-07. The question: this repo ships `tools/run-eval` (which exercises `skills/<name>/evals/trigger-queries.json`, i.e. the router/description layer) and `tools/run-case` (which scores the behaviour layer against `skills/<name>/evals/evals.json`). Are those names right against wider convention, given the specific confusion risk that `evals.json` is read by `run-case`, not by `run-eval`?

Primary sources consulted, all fetched 2026-08-07 unless noted:

- `anthropics/skills` — `skills/skill-creator/` SKILL.md, `references/schemas.md`, and `scripts/` (raw files via raw.githubusercontent.com; directory listings via the GitHub contents API).
- Anthropic Agent Skills docs — overview and skill-authoring best practices on platform.claude.com.
- OpenAI: the `openai/evals` repo README; the Evals API guide on developers.openai.com; the Codex/ChatGPT skill-building docs on learn.chatgpt.com.
- Other eval harnesses: promptfoo, Inspect (UK AISI), EleutherAI `lm-evaluation-harness`, LangSmith, DeepEval, Braintrust.
- Tool/function-selection evaluation: the Berkeley Function Calling Leaderboard (BFCL) blog; promptfoo's assertion reference; DeepEval's tool-correctness metric.
- CLI naming precedent: Google's Shell Style Guide; directory listings of `kubernetes/kubernetes/hack/` and `nodejs/node/tools/` via the GitHub contents API.
- The repo itself: `tools/run-eval`, `tools/run-case`, `tools/run_case/`, `engineering-guidelines.md`, `README.md`, `README.zh-TW.md`, `backlog.md`, `.github/workflows/`, and a full `rg` sweep for every reference.

Where a source did not settle a question, that is stated rather than inferred.

---

## 0. What the two tools actually do (read from source, not from the README)

`tools/run-eval` is a Bash script. It extracts the `description` from `skills/<name>/SKILL.md` frontmatter, then for each entry in `skills/<name>/evals/trigger-queries.json` (falling back to the legacy `evals/<name>/prompts.json`) it issues a one-shot subagent call whose prompt reads, verbatim:

> `You are a skill router. Decide whether the skill below should fire for the user message, using ONLY its description's stated trigger conditions and exclusions — be strict, follow the description verbatim.`

and which must reply `TRIGGER` or `NONE`. It compares that against each entry's `expected_trigger` / `should_trigger` and prints pass/fail counts. It never opens `evals.json`, never runs the skill body, and never produces skill output. Its own comment says so: "This harness tests description triggering only." (`tools/run-eval` lines 13–16, 87–102, 211–244.)

`tools/run-case` is a Python entry point delegating to `tools/run_case/cli.py`. Its module docstring: "Score a skill's behaviour evals (``evals.json``) and report ship/no-ship." It materializes two arms (working tree vs a git ref), dispatches blind runners per (chunk × arm) and blind graders on the other CLI family, and reconciles a verdict. It is opt-in per skill via `skills/<name>/evals/run-case.json`. (`tools/run-case` lines 1–36.)

So the split is real and clean; the question is only whether the two names denote the right things.

---

## Q1. What "eval" and "case" conventionally denote

### "eval" is the umbrella noun for the whole measurement activity, at every scale

No primary source found restricts "eval" to the behaviour layer. Across the sources, "eval"/"evaluation" is used at three different granularities simultaneously — the discipline, the artifact (a suite), and sometimes a single item.

- **OpenAI `openai/evals` README**: "Evals provide a framework for evaluating large language models (LLMs) or systems built using LLMs." The README also offers "an existing registry of evals to test different dimensions of OpenAI models" and points at "our existing eval templates in `eval-templates.md`" — so an "eval" there is a *named suite* in a registry, not a single item. (https://github.com/openai/evals)
- **OpenAI Evals API**: an `eval` is an API object built from "two key ingredients" — a `data_source_config` ("a schema for the test data you will use along with the eval") and `testing_criteria` ("the graders that determine if the model output is correct"). The execution is a separate object, the "eval run". Individual data rows are "items"; `sample` refers to the model-generated output being judged (`{{ sample.output_text }}`). (https://developers.openai.com/api/docs/guides/evals)
- **Anthropic's evaluation docs**: the nouns are "evaluation"/"eval" for the suite and "test case" for the item — "Define measurable success criteria for your LLM application and build evaluations to test it", and repeatedly "Example eval test cases: 1,000 tweets with human-labeled sentiments." (https://platform.claude.com/docs/en/test-and-evaluate/eval-tool)

The important consequence: **"eval" is not owned by the behaviour layer.** A trigger evaluation is an evaluation. Nothing in the primary sources makes `run-eval` wrong merely because it does not run behaviour cases.

### "case" conventionally denotes the individual item, not a layer

- **Anthropic**: "test case" = one labelled item in an eval (see quotes above).
- **DeepEval**: a test case is "A blueprint provided by `deepeval` to unit test LLM outputs, and represents a single, atomic unit of interaction with your LLM app." `LLMTestCase` is "The most prominent type of test case in `deepeval`". (https://deepeval.com/docs/evaluation-test-cases)
- **promptfoo**: "The YAML configuration format runs each prompt through a series of example inputs (aka 'test case') and checks if they meet requirements (aka 'assertions')." The YAML keys are `tests:` (the collection) and `assert:` (the checks). (https://www.promptfoo.dev/docs/configuration/guide/)
- **LangSmith**: "Examples" are "Individual test cases with inputs and reference outputs"; a "Dataset" is the collection; an "Experiment" is "Results of evaluating a specific application version on a dataset". (https://docs.langchain.com/langsmith/evaluation)
- **Braintrust**: `data` is "a dataset of test cases with inputs, optional expected outputs, and metadata"; `task` is "the function being evaluated"; an `experiment` is "the immutable, comparable record of your eval runs". (https://www.braintrust.dev/docs/guides/evals)

So "case" universally means *one item*. `tools/run-case` runs the whole `evals.json` suite, not a single case — the singular noun is a mild mismatch by that convention, though a CLI taking `<skill>` and running its cases is a defensible reading ("run [the] cases [of] <skill>").

### Is `run-eval` misnamed for testing only triggering?

**Not against general convention** (see above), and **explicitly not against the standard this repo declares it follows.** `engineering-guidelines.md` states: "Evals follow the official `skill-creator` standard: `skills/<name>/evals/evals.json`". That upstream standard is `anthropics/skills/skills/skill-creator/`, and it contains a script literally named `run_eval.py` whose module docstring is:

> "Run trigger evaluation for a skill description. Tests whether a skill's description causes Claude to trigger (read the skill) for a set of queries. Outputs results as JSON."

(https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/scripts/run_eval.py — CLI args include `--eval-set`, `--skill-path`, `--description`, `--runs-per-query`, `--trigger-threshold`.)

The upstream `scripts/` directory is: `__init__.py`, `aggregate_benchmark.py`, `generate_report.py`, `improve_description.py`, `package_skill.py`, `quick_validate.py`, `run_eval.py`, `run_loop.py`, `utils.py`. So `run_eval.py` **is** the trigger harness upstream, and the behaviour-eval flow there has no dedicated runner script at all — SKILL.md tells the agent to spawn subagents and then use `eval-viewer/generate_review.py` and `scripts/aggregate_benchmark.py`.

**The upstream ambiguity is identical to this repo's.** `references/schemas.md` upstream defines `evals.json` as the *behaviour* fixture:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": ["The output includes X", "The skill used script Y"]
    }
  ]
}
```

and `run_eval.py` does **not** read it — it takes `--eval-set` (required, no default), pointed at a separate trigger file. `schemas.md` documents schemas for `evals.json`, `history.json`, `grading.json`, `metrics.json`, `timing.json`, `benchmark.json`, `comparison.json`, and `analysis.json`, but **no schema for the trigger eval set**. Upstream SKILL.md calls that file "trigger eval queries" and shows it inline:

> "### Step 1: Generate trigger eval queries
> Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:
> `{"query": "the user prompt", "should_trigger": true},`"

and invokes it as `--eval-set <path-to-trigger-eval.json>`, with the browser export landing at `~/Downloads/eval_set.json`. (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md lines 337–394.)

**Finding.** The confusion the question names — "`evals.json` is read by `run-case`, not by `run-eval`" — is inherited from upstream, not invented here. Upstream ships exactly the same trap: a script named `run_eval` that does not read the file named `evals.json`. This repo is *more* legible than upstream on one axis, because it gave the trigger fixture a self-describing name (`trigger-queries.json`) where upstream calls it `eval_set.json`. Judged against the standard this repo declares it follows, `run-eval` is the conventional name for what it does; judged in a vacuum, the name/file mismatch is a genuine, though upstream-sanctioned, snag.

---

## Q2. What established harnesses call these things

Nouns, per tool, quoted from primary sources.

| Tool | The suite / activity | The individual item | The thing under test | The judge |
|---|---|---|---|---|
| OpenAI `openai/evals` | "eval" (registry entry), "eval template" | not defined in the README | "completion function" ("For more advanced use cases like prompt chains or tool-using agents, you can use our Completion Function Protocol") | eval template / classifier |
| OpenAI Evals API | `eval` object; execution is an "eval run" | "item" ("each item in the data set will conform to a JSON schema") | the prompt/model config | `testing_criteria` = "the graders that determine if the model output is correct"; e.g. `string_check` |
| Anthropic (Console eval tool / test-and-evaluate) | "evaluation"/"evals" | "test case" | the prompt | "grader"; "LLM-based grading" |
| `anthropics/skills` skill-creator | "evals" (the `evals[]` array in `evals.json`), "trigger eval queries" | one entry in `evals[]`, called an "eval"; also "test cases" in prose | the skill | "expectations" = "List of verifiable statements"; plus `grading.json` |
| promptfoo | "eval" (the run), `tests:` | "test case" | `providers:` + `prompts:` | `assert:` / "assertions" |
| Inspect (UK AISI) | `Task` — "An evaluation that brings together a dataset, solver, and scorer"; `eval()` to run | `Sample`; `Dataset` "Provides labelled samples—typically a table with `input` and `target` columns" | `Solver` — "produces an answer for each sample… as sophisticated as a full agent that uses tools over many turns" | `Scorer` — "evaluates the output—using text comparisons, model grading, or other custom schemes" |
| `lm-evaluation-harness` | "task", "benchmark" ("Over 60 standard academic benchmarks for LLMs, with hundreds of subtasks and variants implemented") | "document"/"doc", also "example" (`--num_examples`) | the LM | "metric" |
| LangSmith | "Dataset"; running it is an "Experiment" — "Results of evaluating a specific application version on a dataset" | "Examples" — "Individual test cases with inputs and reference outputs" | the application version | "Evaluator" — "Functions that score how well your application performs" |
| DeepEval | dataset / test run | "test case" — "a single, atomic unit of interaction with your LLM app"; `LLMTestCase` | the LLM app | "metric" (`AnswerRelevancyMetric`, `ToolCorrectnessMetric`, …) |
| Braintrust | "Eval"; the record is an "experiment" | one row of `data` ("a dataset of test cases…") | `task` — "the function being evaluated. Typically an LLM call, but can be any logic: a multi-step agent, a retrieval pipeline, or a custom workflow" | "Scorers… measure quality with numeric scores, while classifiers apply categorical labels" |

Sources: https://github.com/openai/evals · https://developers.openai.com/api/docs/guides/evals · https://platform.claude.com/docs/en/test-and-evaluate/eval-tool · https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/references/schemas.md · https://www.promptfoo.dev/docs/configuration/guide/ · https://inspect.aisi.org.uk/ · https://github.com/EleutherAI/lm-evaluation-harness · https://docs.langchain.com/langsmith/evaluation · https://deepeval.com/docs/evaluation-test-cases · https://www.braintrust.dev/docs/guides/evals

**Patterns worth extracting.**

1. **Nobody uses "case" as a *layer* name.** Every tool uses "case"/"item"/"example"/"sample"/"doc" for the atom. A tool named `run-case` will read, to anyone coming from any of these tools, as "run one case" or "run the cases" — not "run the behaviour layer".
2. **"Eval" is layer-agnostic and scale-agnostic.** It denotes the activity or the suite, never a specific layer. Using it for the trigger layer is not a misuse; using it for the behaviour layer would equally not be.
3. **The distinguishing noun in every harness is what's being scored, not the word "eval".** Inspect distinguishes `Solver` from `Scorer`; Braintrust distinguishes `task` from `scores`; LangSmith distinguishes `Experiment` from `Evaluator`. The layer distinction this repo needs (does the router pick it? / is the output better?) is not one any of these harnesses draws, because none of them route between skills — see Q3.
4. **`lm-evaluation-harness` has no single universal term for an item**, using "document", "example", and "sample" contextually; that is a genuine gap in the convention, not a term I could pin down.

---

## Q3. Is there an established term for "did the skill get selected?"

Yes — but it is **not** a single settled term, and the closest established vocabulary comes from function/tool calling rather than from skills.

### Anthropic's own vocabulary: "trigger", "discovery", "skill selection"

The Agent Skills docs use all three, and they are the most on-point primary source since this repo's artifact is literally a skill description:

- "The `description` is what Claude matches your request against when **determining whether to trigger the Skill**, so it must say both what the Skill does and when to use it." … "until a Skill is triggered, only its name and description occupy context." (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, §Level 1: Metadata)
- "The Skill's YAML frontmatter provides **discovery information**". Same page, same section.
- "The `description` field enables **Skill discovery**"; "The description is critical for **skill selection**: Claude uses it to choose the right Skill from potentially 100+ available Skills." (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, §Writing effective descriptions)
- "The 'name' and 'description' in your Skill's metadata are particularly critical. Claude uses these when **determining whether to trigger the Skill** in response to the current task." (same page, §Observe how Claude navigates Skills)

Upstream skill-creator adds the measurement vocabulary directly. Its own `description` reads: "…or **optimize a skill's description for better triggering accuracy**." Its body: "After creating or improving a skill, offer to optimize the description for better **triggering accuracy**"; the section is headed "**How skill triggering works**"; and its failure classes are "**false triggers**" ("triggered but shouldn't have") and "**failed to trigger**" (`improve_description.py`). The fixture entries are keyed `should_trigger`. Anthropic also warns of "**undertrigger**": "currently Claude has a tendency to 'undertrigger' skills -- to not use them when they'd be useful."

**So "trigger" / "triggering accuracy" is Anthropic's term of art, and this repo already uses it** (`trigger-queries.json`, `expected_trigger`, README's "Trigger-layer eval").

### OpenAI's vocabulary for the same thing: "implicit invocation"

OpenAI's skill docs frame it as invocation rather than triggering:

- "**Explicit invocation:** Include the skill directly in your prompt."
- "**Implicit invocation:** ChatGPT or Codex can choose a skill when your task matches the skill `description`."
- "Because implicit matching depends on `description`, write concise descriptions with clear scope and boundaries."
- Metadata policy: "`allow_implicit_invocation` (default: `true`): When `false`, Codex won't implicitly invoke the skill based on user prompt."

(https://learn.chatgpt.com/docs/build-skills — this repo already consumes that key in `skills/<name>/agents/openai.yaml`, per `engineering-guidelines.md` §Invocation modes.)

**A genuine terminological disagreement between the two vendors:** Anthropic says the skill *triggers*; OpenAI says the model *implicitly invokes* it. Neither uses the other's word. This repo's `engineering-guidelines.md` already straddles both ("model-invoked" vs "user-invoked" for the mode; "trigger gate" for the description).

### The function-calling literature: relevance detection, tool selection, tool correctness

The nearest rigorous prior art measures the same shape of thing — did the system pick the right capability, and did it correctly abstain?

- **Berkeley Function Calling Leaderboard (BFCL)**, https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html:
  - "**Function Relevance Detection**" — "scenarios where none of the provided functions are relevant and supposed to be invoked. We expect the model's output to be no function call." This is precisely a `should_trigger: false` case.
  - "**Multiple Function**" — "Multiple function category contains a user question that only invokes one function call out of 2 to 4 JSON function documentations." This is the selection-among-candidates case.
  - "**AST Evaluation**" (Abstract Syntax Tree) vs executable evaluation are the two scoring methods.
- **promptfoo assertion types** (https://www.promptfoo.dev/docs/configuration/expected-outputs/): `is-valid-function-call` — "Ensure that the function call matches the function's JSON schema"; `is-valid-openai-tools-call` — "Ensure all tool calls match the tools JSON schema"; `trajectory:tool-used` — "Ensure a traced agent trajectory used specific tools"; `trajectory:tool-args-match`; `trajectory:tool-sequence`. **Note:** a `tool-call-f1` assertion was suggested by a secondary search but does **not** appear in promptfoo's assertion reference; treat it as unverified.
- **DeepEval's Tool Correctness metric** (https://deepeval.com/docs/metrics-tool-correctness): "an agentic LLM metric that assesses your LLM agent's function/tool calling ability"; it compares "whether every tool that is expected to be used was indeed called and if the **selection of the tools** made by the LLM agent were the most optimal", by comparing "the `tools_called` by your LLM agent to the list of `expected_tools`".

**Finding.** There is no single canonical term. Ranked by how well each is attested for *this exact* measurement:

1. **"trigger" / "triggering"** — Anthropic's own word for skills, used in the product docs, in skill-creator's description, and in its failure-class names. Strongest fit for a skills repo.
2. **"routing" / "router"** — used inside this repo's own harness prompt ("You are a skill router") but I found **no** primary-source use of "router" for skill selection in Anthropic's or OpenAI's skill docs. It is idiomatic for prompt/model routing generally, not for skill selection specifically. Do not treat it as established for skills.
3. **"selection" / "discovery"** — both attested in Anthropic's best-practices page ("skill selection", "Skill discovery"), and "tool selection" is the established phrase in the function-calling literature (DeepEval).
4. **"relevance detection"** — precise and well-defined (BFCL) but belongs to function calling, and names only the abstain half.
5. **"intent classification"** — classical NLU term; no primary source found applying it to agent-skill selection.

---

## Q4. Is a `run-` prefix idiomatic for a dev CLI?

**No primary style guide found speaks to this.** Google's Shell Style Guide covers only casing, not verb prefixes: source filenames should be "Lowercase, with underscores to separate words if desired", and functions "Lower-case, with underscores to separate words. Separate libraries with `::`." (https://google.github.io/styleguide/shellguide.html). It says nothing about `run-`. I found no equivalent rule in POSIX utility conventions or the GNU coding standards. **This question has no normative answer in primary sources**; the evidence below is descriptive practice, gathered by listing real directories, not by reading a guide.

**`kubernetes/kubernetes/hack/`** (GitHub contents API, 2026-08-07) contains ~130 scripts. The dominant patterns are `verify-*` (≈50: `verify-gofmt.sh`, `verify-shellcheck.sh`, `verify-codegen.sh`, …), `update-*` (≈25: `update-codegen.sh`, `update-vendor.sh`, …), plus `build-go.sh`, `test-go.sh`, `benchmark-go.sh`, `lint-dependencies.sh`, `install-etcd.sh`, `pin-dependency.sh`, `local-up-cluster.sh`. Exactly **one** file in the whole directory carries a `run-` prefix: `run-prometheus-on-etcd-scrapes.sh` — where "run X" is literally the job.

**`nodejs/node/tools/`** (same method) shows the same shape: bare verbs (`install.py`, `test.py`, `release.sh`), `<verb>-<noun>` (`lint-pr-url.mjs`, `find-inactive-collaborators.mjs`, `merge-wpt-reports.mjs`, `license-builder.sh`), and two `run-` files — `run-valgrind.py` and `run-worker.js` — again where running a named external thing is the whole job.

**Reading.** `<verb>-<noun>` is overwhelmingly the house style in large repos, and `run-` shows up as a rare special case reserved for "execute this specific external thing". The generic sense — "run the X harness" — is not what the surveyed repos use `run-` for. But this is a descriptive pattern with no normative source behind it, so it supports a preference, not a rule.

**The repo's own precedent is the stronger argument.** `tools/` contains: `annotate`, `archive-skill`, `build-docs`, `check-invocation`, `check-labels`, `new-skill`, `run-case`, `run-eval`, `sync-skills`, `usage-report`, plus the `run_case/` package and `templates/`. Eight of ten are `<verb>-<noun>` or a bare noun (`annotate`, `usage-report`); the only two `run-`-prefixed names are exactly the two under review. Within this repo, `run-` is the anomaly.

---

## Q5. Recommendation, and the concrete migration cost

### The verdict

**`run-eval` is defensible and I would keep it; `run-case` is the weaker name and is the one worth changing — but neither rename is required, and the cheapest fix for the stated confusion is not a rename at all.**

Reasoning:

- `run-eval` matches, name-for-name and job-for-job, the upstream `skill-creator/scripts/run_eval.py` whose docstring is "Run trigger evaluation for a skill description." The repo declares skill-creator as its eval standard. Renaming it away from upstream costs alignment and buys only local clarity.
- The confusion is not caused by the *tool* names. It is caused by `evals.json` sounding like the generic fixture for anything called an eval. Upstream has the identical trap. Renaming `run-eval` to `run-trigger` fixes half the confusion; renaming the *fixture* would fix it at the source — but `evals.json` is the name the declared upstream standard mandates, so it should not move.
- `run-case` is the genuinely non-conventional name: no surveyed harness uses "case" for a layer, all use it for an atom, and `run-` is the anomaly among this repo's ten tools.

### If renaming, in preference order

1. **Highest value, near-zero cost: sharpen the docs, keep both names.** `README.md` already says "Trigger-layer eval" and "Behaviour-layer eval". Add one sentence next to each — `run-eval` reads `evals/trigger-queries.json` (never `evals.json`); `run-case` reads `evals/evals.json` — and the trap is closed for a reader. `engineering-guidelines.md` §Test discipline already states this ("`tools/run-eval` exercises `trigger-queries.json`… `tools/run-case` scores the behaviour layer against `evals.json`"), so the fix is largely already in place; the gap is that the tool names alone don't carry it.
2. **If one name changes, change `run-case` → `score-behaviour`** (or `score-evals`, or `grade-evals`). Rationale: it is the tool whose name is unconventional against every harness surveyed; `score`/`grade` are the attested verbs for what it does (OpenAI `testing_criteria` = "the graders that determine if the model output is correct"; Inspect's `Scorer` "evaluates the output"; Braintrust "Scorers… measure quality with numeric scores"), and the tool's own docstring already says "Score a skill's behaviour evals". `score-evals` has the extra virtue of naming the file it reads. It also drops the anomalous `run-` prefix and lands on `<verb>-<noun>` like the other eight tools.
3. **If both change, pair it as `check-triggers` + `score-evals`**, which makes the layer split legible from the names alone and matches the existing `check-labels` / `check-invocation` family. Cost: it walks away from the upstream `run_eval` precedent, and `trigger` is Anthropic's word but not OpenAI's (which says "implicit invocation"). **Do not** use `run-router` / `check-routing`: "router" for skill selection appears only in this repo's own harness prompt and in no primary vendor source.

My recommendation is (1) plus (2): keep `run-eval` for upstream alignment, rename `run-case` to `score-evals`, and add the one-line "reads which file" note to both README rows.

### Migration cost, measured (`rg` over the worktree, 2026-08-07)

**No CI cost.** `.github/workflows/` contains `docs-check.yml`, `eval-labels.yml`, `invocation-check.yml`, `pages.yml`; **none** references `run-eval` or `run-case`. (`eval-labels.yml` runs `tools/check-labels --all`; `invocation-check.yml` runs `tools/check-invocation --all`.)

Renaming **`run-eval`** — 9 references in 6 files:

| File | Hits | What |
|---|---|---|
| `tools/run-eval` | 5 | the file itself; `usage:` line; the `RUN_EVAL_AGENT` env var (a public knob, documented in `engineering-guidelines.md`); two diagnostic strings `run-eval: claude -p produced no parseable…` / `run-eval: codex exec produced…` |
| `engineering-guidelines.md` | 3 of its 7 total hits | §Invocation modes, §Test discipline (twice, including the two-harness rule and the cross-router note naming `RUN_EVAL_AGENT`) |
| `README.md` / `README.zh-TW.md` | 1 each | the tools table row |
| `backlog.md` | 1 | the two-harness explainer |
| `tools/new-skill` | 1 | the post-scaffold hint: `then check with 'tools/run-eval $NAME'` |
| `tools/templates/regression-protocol.md` | 1 | the trigger row of the generated protocol table |
| `skills/{plan-to-goal,discuss-with-me}/evals/regression-protocol.md` | 1 each | instantiated copies of that template |
| `skills/blog-writing-zh/design-notes.md` | 1 | a backlog checkbox |
| `skills/humanizer-zh/research/…-2026-07-29.md` | 1 | quotes another repo's `evals/run-eval.md` — **not** this tool; must not be rewritten |

Renaming **`run-case`** — substantially larger, ~163 references in 32 files, and it has three distinct surfaces:

1. **The code.** `tools/run-case` (3) plus the whole `tools/run_case/` package — `cli.py` (16), `calibration.json` (16), `aggregate.py` (7), `calibration.py` (6), `smoke.py` (5), `bank.py` (3), `report.py` (2), `errors.py` (2), `config.py` (2), `arms.py` (2), `dispatch.py` (1), `__init__.py` (1). The package directory name itself would move, and `tools/annotate` imports it directly (`from run_case.config import …`, `from run_case.errors import …`) — 15 hits in `tools/annotate` total, including user-facing Chinese report strings that name `run-case.json`.
2. **The opt-in config filename `skills/<name>/evals/run-case.json`.** Hardcoded in `tools/run_case/errors.py` (`CONFIG_PATH = Path("evals") / "run-case.json"`), referenced by `tools/annotate` and by `skills/humanizer-zh/evals/annotate.json`. Exactly one skill ships it today: `skills/humanizer-zh/evals/run-case.json`. Renaming the tool without renaming this file leaves a dangling name; renaming it is a breaking change for that skill's fixture.
3. **Generated history.** 48 files under `skills/humanizer-zh/evals/` carry `run-case` in their *filenames* (`results-2026-08-01-run-case-r5.md`, `null-2026-08-05-r1v2-run-case.json`, …), and `tools/run_case/calibration.json` lists 16 of those filenames as data. `tools/run_case/cli.py` generates more of them (`f"results-{report['date']}-run-case.md"`, `f"null-…-run-case.json"`). These are an immutable audit trail: **leave them alone** and let the new name apply only to new output, or the calibration pool's provenance breaks.
4. **Prose.** `skills/humanizer-zh/evals/judged-cases.md` (30), `skills/humanizer-zh/design-notes.md` (14), `skills/humanizer-zh/evals/regression-protocol.md` (8), `engineering-guidelines.md` (4 of 7), `backlog.md` (3 of 4), `skills/humanizer-zh/backlog.md` (2), `README.md` / `README.zh-TW.md` (1 each), `skills/infographic-design/evals/ab-protocol-v0.10.1.md` and `-v0.11.0.md` (1 each).

**Cost summary.** Renaming `run-eval` is a contained, ~1-hour mechanical change touching one public env var. Renaming `run-case` touches a Python package name, a cross-tool import in `tools/annotate`, a skill-facing config filename, and 48 historical artifacts whose names are load-bearing data in `calibration.json` — an afternoon of careful work with a real chance of breaking the calibration provenance. That asymmetry argues for doing the docs fix first and treating the `run-case` rename as a separate, deliberate change rather than a drive-by.

---

## Where primary sources genuinely disagreed, or fell silent

- **Anthropic vs OpenAI on the selection verb.** Anthropic: the skill "triggers"; failure classes are "false triggers" and "failed to trigger". OpenAI: the model performs "implicit invocation", gated by `allow_implicit_invocation`. Neither vendor uses the other's term. Any name this repo picks will be idiomatic on one harness and foreign on the other — which matters here, because portability across both is a stated repo rule.
- **The atom's name in `lm-evaluation-harness`.** Its docs use "document"/"doc", "example" (`--num_examples`), and "sample" contextually and define no single universal term. I could not pin one down.
- **`run-` prefix conventions.** No style guide I could find — Google Shell Style Guide, GNU coding standards, POSIX utility conventions — addresses verb prefixes for script names at all. The `kubernetes`/`nodejs` evidence is descriptive practice observed by listing directories, not a normative source, and should be weighted accordingly.
- **promptfoo `tool-call-f1`.** Reported by a secondary search but absent from promptfoo's own assertion reference. Recorded here as unverified and not relied on.
- **`openai/evals` on "sample".** The README does not define "sample". The Evals API guide uses `sample` to mean the model's generated output (`{{ sample.output_text }}`), which is the *opposite* of Inspect's usage, where a `Sample` is an input item from the dataset. The word is not portable between the two.

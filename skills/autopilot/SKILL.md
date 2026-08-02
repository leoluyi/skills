---
name: autopilot
description: >-
  Run an entire established plan to completion autonomously — orchestrate subagents, self-repair within a bounded attempt budget, pass a verification gate, then commit, push and open a ready PR without checking back in between steps. Invoke it explicitly when handing over a whole job: "run the whole plan", "take it from here and open a PR", 「照計畫跑完，不用問我」, 「全部做完再回報」. It suspends the ask-first / confirm-alignment rules for the duration of the run and batches every decision into a final report. Never fires on its own — the user must ask for it by name, because it commits and pushes without confirmation.
app-description: >-
  把整份既定計畫自動跑完：以 subagent 為主力執行、故障自修有次數上限、過驗證閘門後 commit、push、開 PR，全程不回頭問。 明確呼叫才啟動：「照計畫跑完，不用問我」「全部做完再回報」。執行期間暫停「先討論再實作」等規則，所有決策集中在最後回報。
version: 1.0.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. Subagent delegation and worktree isolation degrade gracefully where unsupported — the run stays in the main loop and branches in place.
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Glob, Grep, Agent, TodoWrite, EnterWorktree, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git switch:*), Bash(git checkout:*), Bash(git branch:*), Bash(git push:*), Bash(gh pr create:*), Bash(gh pr view:*)
metadata:
  author: Lu Yi
  tags: agent-workflow autonomous-execution delegation verification shipping
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\U0001F680"
---

This is **autonomous mode**. Run to completion. Do not come back to me between
steps, do not ask which option I prefer, do not stop to confirm before
committing. I am handing you the whole job, not the first step of it.

## Tool surface

Restrict yourself to these tools for the whole run, whether or not the harness
enforces it: read and edit files, search, spawn subagents, track todos, enter a
worktree, and the git and `gh` subcommands named in *Isolation* and *Shipping*.
Every other shell command — including `date`, package installs, and anything
that reaches outside this repo — is out of bounds. Where the harness does
enforce a tool allowlist it is already set to this same surface; its absence
elsewhere is not permission to widen.

## What this overrides

For the duration of this run, these standing rules are suspended:

- The "Plan First / discuss the approach / confirm alignment before implementing"
  process in CLAUDE.md. Plan internally, then execute the plan yourself.
- "Ask about preferences", "surface assumptions and get confirmation", "when
  facing implementation complexity ASK for guidance", "when discovering
  architectural flaws STOP and discuss". You decide. See *Escalation* below for
  how.
- The rule about surfacing 2-4 choices before every direction decision. Batch
  every decision you made into the final summary instead.
- Git History Protection's ask-before-commit requirement. Its autonomous-mode
  exception applies here by name: commit and push without confirmation.

Everything else in CLAUDE.md still binds you, in particular: no TODO/FIXME or
placeholder comments, no partial work reported as finished, no emojis, no
hardcoded secrets, immutable patterns, files under 800 lines, comprehensive
error handling.

## Delegation model

You are the **orchestrator**, not the implementer. Default to spawning a
subagent; doing it inline is the exception you justify to yourself, not the
other way round. A long autonomous run dies of context exhaustion, and every
file a subagent reads is a file you did not have to hold.

Delegate by default:

- **Recon.** Anything that means sweeping the codebase to find where something
  lives, how a pattern is used, or what already exists. Ask for the conclusion,
  not the file dumps.
- **Implementation of a scoped task.** One todo item with a clear boundary is
  one subagent.
- **Fixing a broken build, test or type error.** See *Self-repair*.
- **Irreversible decisions.** See *Escalation*.
- **Review before shipping.** See *Verification gate*.

Keep in the main loop, always:

- Task breakdown and the todo list. The list is yours; subagents do not own it.
- Small or cross-cutting edits — a rename across five files, a signature change
  that ripples, wiring two subagents' output together. Briefing an agent on
  these costs more than doing them.
- Integration and coherence. After each subagent returns, read the actual diff
  it produced. A subagent's report is a claim, not evidence.
- Running the verification gate.
- Every git and `gh` operation. Subagents never commit, never push, never open a
  PR. Say so in their briefs.

**Parallelism:** before dispatching, write down the file scope of each pending
todo. Todos whose scopes are disjoint go out as multiple agent calls in a
single message so they run concurrently. Todos whose scopes overlap run one at a
time — you fan out on independence, not on impatience. If you cannot state a
todo's file scope, it is not decomposed enough to delegate yet.

**Agent types and models:** pick from the agent types this session actually
lists; do not invent names. Read-only sweeps go to the first of these this
session lists — `cavecrew-investigator`, `Explore`, `general-purpose` — because
the first one already returns `path:line` facts instead of prose and so costs
this loop the least to read back. Implementation goes to `general-purpose` or a
language-specific agent when one exists. Leave the model unset for
implementation work so it inherits this run's mid-tier model. Set the top-tier
model only for decision and review agents. Run agents synchronously when you
need the result before you can continue, which is nearly always. Where the
harness offers no subagents at all, do the work inline and say so in the final
report — the sequence, the gate and the shipping rules are unchanged.

## Sequence

1. **Scope it.** If the user named the job when invoking this skill, that is the
   job. If they named nothing, the job is the plan already established in this
   conversation — continue it from wherever it stands.
2. **Recon.** Spawn a search agent to map the code the job touches: which files,
   which existing patterns and conventions, what already solves part of this.
   Skip only when the job is a file you are already holding.
3. **Plan it.** Write the full task breakdown to the todo list before touching
   code, with real granularity, each item carrying its file scope. This list is
   your contract; you are done when every item is checked, not when the first
   thing works.
4. **Isolate.** Never work on the default branch. Enter a worktree, branch in
   place, or stay on the non-default branch you are already on — see *Isolation*
   below for which, and *Naming* for what to call it when you create one. This
   is the last moment the tree is clean, so decide here and not later.
5. **Build it.** Work the list top to bottom, dispatching per the delegation
   model. Read each returned diff before marking the item done. Fix what breaks.
   Keep going.
6. **Review and verify.** See *Verification gate*.
7. **Ship.** Commit, push, open a ready PR. Reviewing and merging it is mine.

## Isolation

Decide this once, at step 4, and stop at the first rule that matches:

1. **HEAD is on a non-default branch and the user named no job.** Stay on it and
   keep committing there — an empty invocation continues the plan already under
   way, and that plan is why this branch exists. Say in the final report that
   you continued an existing branch rather than creating one.
2. **You are already inside a worktree** — `git rev-parse --show-toplevel` lands
   under `.claude/worktrees/`, or HEAD is on a `worktree-*` branch. Branch in
   place.
3. **I told you this run is solo, or to skip isolation.** Branch in place.
4. **The working tree is dirty.** Branch in place.
5. **The job builds on commits absent from `origin/<default-branch>`** —
   `git rev-list --count origin/<default-branch>..HEAD` is non-zero and the plan
   depends on those commits. Branch in place.
6. **Otherwise.** Enter a worktree.

Rule 6 is the default because the risk is asymmetric: two sessions checked out
in one directory is not a merge conflict but one HEAD and one index silently
overwritten, undetectable from either side, whereas a worktree that turns out
not to have been needed costs one dependency install. Rules 4 and 5 exist
because entering a worktree carries no uncommitted changes across, and its
default `fresh` base ref branches from `origin/<default-branch>` — the trap in
rule 5 is a feature branch that is already pushed, whose commits are therefore
not local-only yet are still absent from that base, so a worktree cut there
starts on a tree missing the work the job builds on and nothing errors; you find
out at merge. Rule 2 exists because nesting is refused outright within a
session, and from a session launched inside the worktree `--show-toplevel`
resolves to the worktree rather than the main checkout, so it would grow a
second `.claude/worktrees/` under the first — and it buys nothing, since being
in a worktree already keeps this run out of my main tree. Rule 3 is mine to make
and not yours: you cannot observe from inside a run whether I will open another
session against this repo, so never infer it from job size or file count. Where
the harness has no worktree mechanism, rule 6 degrades to branching in place;
every other rule is unchanged.

Never manufacture a passing condition — do not stash, do not commit unrelated
work to clear the tree, do not push local commits so the base ref will see them.
Inside a worktree everything else is unchanged: same sequence, same gate, same
shipping. Do not exit the worktree yourself; the work lives there and I decide
what happens to it. Put the worktree path in the final report.

Subagent-level isolation is a different mechanism, and giving an individual
agent its own worktree is **forbidden here**. Not because of its cost — because
a worktree branches from the remote default and therefore cannot see the edits
you have made and not yet committed. Under this delegation model you keep the
small and cross-cutting changes in the main loop, so an isolated agent would be
writing against stale signatures, stale helpers and stale conventions, and you
would not find out until you merged it back. On top of that it solves a problem
you do not have: the parallelism rule already guarantees concurrent agents write
to disjoint files. Let them work in the tree you are actually in.

## Naming

Both isolation paths start from the same two pieces: a `<type>` from the
conventional-commit set CLAUDE.md already uses (feat, fix, refactor, docs, test,
chore, perf, ci) so the branch agrees with the commits that will land on it, and
a `<slug>` of two to four kebab-case words naming the *outcome* of the job, not
the action you are about to take. Derive both from the job description.

They are then assembled differently, because the two paths do not accept the
same string:

- **Worktree.** Pass `<type>-<slug>` to the worktree tool, flat, **no slashes**.
  The tool rewrites `/` to `+` and prefixes the branch with `worktree-`, so
  `feat/token-refresh` becomes the branch `worktree-feat+token-refresh` — legal
  in git, ugly in a PR URL. `feat-token-refresh` becomes
  `worktree-feat-token-refresh`, which reads. The 64-character limit applies to
  the name you pass, and the branch carries nine more on top, so stay under
  about forty.
- **Branch in place.** `git switch -c <type>/<slug>`, with the slash, as normal.

Do not add a provenance prefix of your own on the worktree path. `worktree-` is
applied automatically and already marks the branch as agent-created, which is
what makes `git branch --list 'worktree-*'` a usable cleanup handle.

Check for a collision before you create either one — `git branch --list` for the
name you are about to take, and on the worktree path `git worktree list` as
well. This is not hypothetical: two runs given similar jobs converge on the same
slug, which is exactly the concurrency case the worktree default exists for. If
the name is taken, append `-2`, then `-3`. Do not reach for a timestamp to force
uniqueness — `date` is outside this run's tool surface, so it would stall the
run on a permission prompt.

## Briefing subagents

A subagent inherits none of this conversation. It cannot see the plan, the
decisions already made, or what the previous agent just did. An underspecified
brief is the main way delegation produces worse code than doing it inline, so
every implementation brief carries:

- the goal, stated as the outcome, not as "continue the work"
- the exact files to change, and the files to read first for context
- the conventions already established in this codebase that it must match,
  including any decision the escalation agent already settled
- the constraints from CLAUDE.md that bite here — immutability, error handling,
  no placeholder comments, file size
- how to check its own work, and the instruction to run that check
- an explicit **do not**: no commits, no pushes, no branch changes, no work
  outside the stated file scope, no widening the task

Require it to return: what it changed file by file, what it verified and the
actual result, what it chose not to do, and anything it found that contradicts
the brief. If it returns a contradiction, that is signal — resolve it before
dispatching the next agent, and escalate it if it is an irreversible call.

Require that report in a compressed form, because you will read the diff
yourself anyway and its report is an index, not evidence:

- open with one line per file, `path:line-range — what changed, one sentence`
- no restating of the brief, no opening or closing paragraph, no file contents
- for verification, quote the shortest decisive line of the output — the passing
  count, the failing assertion — not the whole run
- contradictions and things it chose not to do stay in full sentences. Those are
  inputs to a judgement you have to make, and compressing them costs more than
  the tokens they save.

### Where the compressed contract applies

Only two places: the recon sweep, and the implementation report above. Ask for
prose everywhere else, and when a new kind of delegation appears that this list
does not name, ask for prose there too.

It does **not** apply to self-repair agents (you have to count the hypotheses
they tried), decision agents (the option space and the discarded alternatives
are the deliverable), review agents (you can overrule a finding, but only if it
came with the reasoning to overrule), any todo whose product is prose — a doc, a
README, a commit body — where a terse instruction leaks into the artifact, or
your own final report, which a human reads.

Recon needs no format clause of its own when it goes to `cavecrew-investigator`,
which already emits `path:line` and nothing else. Brief it as usual on the
search scope and on returning conclusions rather than file contents.

## Escalation: high-tier model for decisions, mid-tier for the work

This skill runs the main loop at a mid-tier model on high reasoning effort,
deliberately. Implementation runs at that tier — so "this is hard" is not by
itself a reason to escalate. Judgement calls are.

When you hit a decision that is expensive to reverse — architecture, data model,
public interface shape, library selection, migration strategy, scope cuts, or
any fork where two credible approaches would produce materially different
codebases — do not pick it yourself and do not ask me. Spawn a decision agent: a
general-purpose subagent on the top-tier model, run synchronously, briefed with
the full option space, the constraints, the relevant code, and the instruction
to return one decision plus the reasoning and the discarded alternatives.

Wait for it, take its decision as settled, and implement it. Do not re-litigate
it, do not blend it with your own preference, do not escalate the same question
twice. Carry the decision into the brief of every implementation agent it
affects, and record it and its rationale for the final summary.

Do **not** escalate reversible or mechanical choices — naming, file placement,
which helper to extract, formatting, obvious bug fixes. Those are yours, or the
implementation agent's. A run that escalates everything is as broken as one that
escalates nothing.

## Self-repair, bounded

When something breaks, fix it. Read the actual error, form a hypothesis, change
one thing, re-run. A build, type or test failure with a legible error is good
subagent work — hand it the error text, the failing command and the files
involved, and let it burn its context on the trace instead of yours.

The bound is **three attempts per distinct blocker**, and each attempt must rest
on a *different* hypothesis. The count is per blocker, not per agent: a subagent
that came back having tried two hypotheses leaves you one, and its brief must
ask it to report the hypotheses it tried so you can count them. Re-running the
same fix with cosmetic variation does not count as an attempt, it counts as a
loop — cut it immediately. A subagent that dies or returns nothing spends one
attempt. If the third hypothesis fails, that blocker is a hard stop.

Never route around a blocker by weakening the thing that caught it. Do not
delete or skip a failing test, loosen a type, widen an exception handler, or
comment out the assertion — and forbid it in the brief, because an agent under
pressure to return green will do exactly this. If the test is genuinely wrong,
fix the test and say so explicitly in the summary.

## Verification gate

Before you may commit, two things must pass.

**Review.** Dispatch review agents in parallel over the full diff — at minimum
correctness, plus a security pass whenever the change touches input handling,
auth, credentials, network calls or persisted data. Use the top-tier model for
these; a reviewer that misses the bug is worse than no reviewer. Fix what they
find that is real, within the three-attempt bound. You are allowed to reject a
finding, but say which and why in the final report.

**Checks.** The repo's own checks must be green, and **you run them yourself in
the main loop.** Discover them rather than assuming — look at `package.json`
scripts, `Makefile`, `justfile`, `pyproject.toml`, CI workflow files — and run
whatever the project actually defines for build, test, lint and typecheck. A
subagent may fix a failure, but its report that the failure is fixed is not the
gate. You must see the green output yourself, because a hard stop you cannot
audit is not a hard stop.

Red light means you may not commit. Fix it within the three-attempt bound, or
hard stop. Do not commit with a caveat, do not commit "so the work isn't lost",
do not open the PR and mention the failure in the body.

If the repo defines no checks at all, say so in the summary and fall back to
whatever smoke check proves the change actually runs.

## Shipping

Conventional commits, per CLAUDE.md's format. Split into logical commits if the
work has distinct phases; one commit is fine if it does not.

Push with `-u`. Then `gh pr create` as a **ready** PR (not draft) whose body
contains:

- what changed and why
- every decision that went to the high-tier model, with its rationale and the
  alternatives that lost
- every assumption you made that I have not confirmed
- the verification you ran and its result
- a test plan

Never merge the PR, and never enable auto-merge. Review and merge are mine.

## Hard stops

These four are the only reasons to break the no-interruption rule. When you hit
one, stop immediately, leave the tree in a coherent state, and report what you
found and what you need. Do not push, do not open a PR.

1. **A blocker survives three distinct fix attempts.** Report the three
   hypotheses and why each failed. Do not keep going.
2. **The verification gate stays red.** Never ship a red build.
3. **The task requires a destructive or irreversible operation** — force-push,
   deleting a branch or history rewrite, altering a migration that has already
   run against real data, `rm -rf`, touching production configuration or
   credentials, anything that reaches outside this repo. This binds your
   subagents too: brief them to return the request rather than perform it.
4. **You find a security problem or leaked secret** — hardcoded credentials, an
   auth bypass, an injection hole. Stop and report it. Do not quietly fix it and
   fold it into the PR; a silent security fix is a security fix nobody reviewed.

Anything not on this list — ambiguity, unexpected complexity, a design you
dislike, a missing dependency, a flaky test, an unclear requirement, a subagent
that comes back empty — you handle yourself and report at the end.

## Final report

One summary at the end covering: what shipped, the PR link, the decisions the
high-tier model made, the assumptions you made unilaterally, the review findings
and which you rejected, the verification results, and anything you deliberately
left out of scope, and the worktree path if you used one. Include the delegation
trace — which agents ran, on what, and what came back — so the run is auditable
after the fact. End with what I should look at first in the PR: the unilateral
assumptions and any review finding you rejected.

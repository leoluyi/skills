# Autopilot

Most "just run it" instructions fail in the same two ways: the agent stops to ask something halfway through, or it runs out of context because it read every file itself. Autopilot is written against both. It treats the run as one handover — plan internally, delegate the reading and the scoped edits, self-repair on a fixed budget, pass a verification gate you can audit, then commit, push and open a PR — and batches every decision it made into a single report at the end.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a autopilot -y
```

To update later:

```
npx skills update autopilot
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/autopilot/SKILL.md)

## What it does

Seven steps, in order: scope the job, decide isolation, spawn a recon agent to map the code it touches, write the full task breakdown with each item's file scope, build the list top to bottom, review and verify, then ship.

Delegation is the default, not the exception. Recon, scoped implementation, fixing a broken build, irreversible decisions and pre-ship review all go to subagents; task breakdown, cross-cutting edits, integration, the verification gate and every git operation stay in the main loop. Todos with disjoint file scopes go out concurrently; overlapping ones run one at a time. If a todo's file scope can't be stated, it isn't decomposed enough to delegate.

For the duration of the run it suspends the standing "discuss the approach first / ask about preferences / stop and confirm before committing" rules — that's the point of invoking it — while everything else in your CLAUDE.md still binds: no placeholder comments, no partial work reported as finished, no emojis, no hardcoded secrets.

## When to use

When the approach is already settled and you want the job finished end to end without being interrupted. Hand it a plan, answer one pre-flight question, walk away, read one report.

## When not to

Not while the approach is still open, not for exploratory work, and not when you want to see each step before it lands. It commits and pushes without asking, which is why it never fires on its own — you have to invoke it by name.

## How it works

Three mechanisms carry most of the weight.

**The three-attempt bound.** Each distinct blocker gets three fix attempts, and each attempt must rest on a different hypothesis. The count is per blocker, not per agent, so a subagent that already burned two leaves one. Re-running the same fix with cosmetic variation isn't an attempt, it's a loop, and gets cut. Nothing may route around a blocker by weakening the check that caught it — no deleting a failing test, loosening a type, or widening an exception handler — and that prohibition goes into every subagent brief, because an agent under pressure to return green will reach for exactly that.

**The verification gate.** Before any commit: parallel review agents over the full diff (plus a security pass whenever the change touches input handling, auth, credentials, network calls or persisted data), and the repo's own checks, discovered rather than assumed and run in the main loop. A subagent's report that a failure is fixed is not the gate — the green output has to be seen directly, because a hard stop nobody can audit isn't a hard stop.

**The isolation ladder.** Six rules, checked in order at step 2, before anything else touches the repo. Five of them are already forced — four off git state alone (already on a non-default branch, already inside a worktree, a dirty tree, work that builds on pushed-but-unmerged commits), plus the case where you told it the run is solo. Those exceptions exist because a worktree carries no uncommitted changes across and branches from the remote default, so each of them branches in place instead.

The sixth rung — clean tree, on the default branch — is the only one where both paths are legal, and there it asks rather than picks: worktree or branch in place, with the worktree recommended because the risk is asymmetric. Two sessions checked out in one directory silently overwrite one HEAD and one index, undetectable from either side, while an unnecessary worktree costs one dependency install. The question lands at invocation, while you are still there to answer it, so the autonomous stretch that follows really is uninterrupted; state a preference when you invoke and it skips the question, and a scheduled or headless run with nobody to ask falls back to the worktree and says so in the report.

Four hard stops are the only reasons it breaks the no-interruption rule: a blocker surviving three distinct attempts, a verification gate that stays red, a destructive or irreversible operation, or a security problem. On any of those it stops, leaves the tree coherent, and reports — no push, no PR.

## Related skills

`plan-to-goal` and `goal-definer` produce the bounded target this skill executes against; running Autopilot on a vague objective is how an unbounded run happens. `breakdown` and `options` are its opposites — reach for those when the direction is still open and you want the decisions surfaced rather than batched.

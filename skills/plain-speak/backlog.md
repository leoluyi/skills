# plain-speak backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

- [ ] **Two 1.5.0 behaviours are unverifiable from a single-prompt harness — need real
  transcripts in `judged-cases.md`.** 2026-07-30. The bare-invocation path resolves its target
  from the conversation, and cases 8–12 test that against a transcript *embedded in the prompt*.
  Two parts of the resolution order therefore went untested: stepping back over pure tool-work
  and status turns to reach the last turn that carried reasoning, and re-posing a pending
  question through the host's interactive question tool where one exists. Collect real session
  transcripts where either path misfires and turn them into judged cases; do not assume the
  synthetic runs cover them.


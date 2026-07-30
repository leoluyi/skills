# avoid-china-writing backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

- [ ] **Port the two speak-human-tw cases that belong to this skill, not to humanizer-zh.**
  Noted 2026-07-28, surfaced while porting speak-human-tw's `evals/benchmark.md`. Both were
  excluded from that port because they test the 陸用語／簡體殘留 axis, which is this skill's job.
  Port with attribution, per the pattern in `humanizer-zh/NOTICE`.

  Same source batch as humanizer-zh's ported-case adjudication sweep
  ([`skills/humanizer-zh/backlog.md`](../humanizer-zh/backlog.md)), which is walking the *other*
  side of the split — the cases that did land there, ids 15–54, resuming at 15/16/17. Whoever
  works either side will meet the boundary; these two are the ones ruled out of that port, so
  they are not waiting on that sweep and it is not waiting on them.
  - **SF-15 (半形標點混用 — 中文句子誤用半形逗號/句號/驚嘆號)** is the real gap: `evals.json`
    has no 標點 axis at all. This is the one to write.
  - **SF-14 (視頻/質量/信息/博主/接地氣 in one social post)** is partly covered already — 視頻
    appears in 4 cases and 質量 in 2 — but 信息, 博主 and 接地氣 appear in none, and no single
    case stacks them in one social-register passage. Decide whether that stacking is worth its
    own case or whether adding the three missing terms to existing cases is enough.

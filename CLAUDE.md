# Skills repo — authoring conventions

Guidance for agents developing skills in this repo.

## Keep development-process noise out of skill content

`SKILL.md` and everything under a skill's `references/` are **runtime instructions** the model loads when the skill fires. They must read as "how to do the task," never "how this skill was built." This is the `打破第四面牆 / 生成過程外洩` rule (see `skills/avoid-ai-writing-zh`) applied to our own files.

Do **not** leave these in `SKILL.md` or `references/`:

- **Iteration provenance** — `依據 GAN 協定 round 1…`, `round 2 補強`, eval IDs (`eval #14`), FP/recall figures.
- **Derivation narrative** — `比對〈A〉與〈B〉後發現…`, `兩篇對照補強`, `（benchmark 實證）`, `（補充樣本：X 一文）`.
- **Method-named headers** — a header that names how a technique was derived instead of what it is (`## 兩篇對照補強` → `## 進階招式`).

Keep the **insight**, drop the **derivation**. Rewrite `比對 A 與 B 後發現此風味有兩種子模式` → `此風味有兩種子模式：…（下筆前先定位在哪一端）`. Article titles used as *illustrative* examples of a technique stay; titles used as *derivation evidence* go.

## Where provenance belongs instead

- `<skill>/DEVELOPMENT.md` — per-skill development notes.
- `evals/<skill>/benchmark-protocol.md` — iteration log and method.
- Commit messages / PR descriptions — what changed and why.
- `backlog.md` — deferred work.

## Finishing check

Before finalizing a skill edit, grep the skill and its references:

```
grep -rnE 'GAN|round [0-9]|benchmark|補強|補充樣本|比對〈|對照[^，。]*〈|可般化|般化|來自對照|eval #|FP ?=|recall' skills/<name>/
```

Hits inside `SKILL.md` or `references/` are noise — move them to the dev docs above. Hits inside `DEVELOPMENT.md` / `benchmark-protocol.md` / `.json` eval fixtures are fine; that is where provenance lives.

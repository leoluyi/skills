# Learn Loop

Learn Loop is a structured learning loop that teaches you a concept from verified primary sources, quizzes you on it, and then has you write the permanent note yourself while it checks your draft against the sources. It never writes the note for you. This skill is invoke-only — it never auto-triggers just because a concept comes up in conversation; it has to be called explicitly.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a learn-loop -y
```

Update later with:

```
npx skills update learn-loop
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/learn-loop/SKILL.md)

Invoke it with `/learn-loop <concept>` in Claude Code, `$learn-loop` in Codex, or by explicitly asking to run the learn-loop process.

## What it does

The skill runs on a 先教後考 + 來源查證 mechanism: it teaches the concept from sources it has verified (primary sources outrank secondhand write-ups, and it will say so rather than fabricate a citation), then switches into examiner mode and asks retrieval questions you answer in your own words. Only once your answers hold up does it move to distillation.

At distillation, the roles flip. You close the explanation and write the note from memory, in your own words — the skill's only job at that point is to poke holes: where the draft disagrees with the sources, where it's vague, where it isn't atomic. It never ghostwrites the note. The act of writing the distillation from memory is the learning itself, so that step is never delegated back to the skill — it acts strictly as a practice partner and fact-checker, not an author.

## When to use

Reach for it when you want to genuinely learn a new technical concept and crystallize it into a permanent Obsidian note, not just skim an explanation.

## When not to

Skip it for reorganizing an already-distilled document into Diátaxis blocks (use knowledge-doc-writing instead), or for a quick one-off explanation with no note to keep.

## How it works

The loop runs six steps in order, one at a time, waiting for your response after each (they don't have to happen in one sitting):

1. **Capture the question** — opens a working note in the vault's `00-inbox/`, titled after the concept, and records what you want to understand and why.
2. **Ground** — sweeps recently captured material (notes, PDFs, screenshots) related to the concept, treats brought-in material as primary source or researches it via web search, and cross-references the vault for concepts you already know as anchors. Produces a literature note with source links.
3. **Teach, then test** — explains the concept concisely from verified sources tied to your existing anchors, then asks 3-5 retrieval questions and waits. Gaps send it back to step 2 for more grounding.
4. **Distill** — you write the note from memory with the explanation closed; the skill only critiques for accuracy, vagueness, and atomicity, and can propose a claim-style title.
5. **Promote & connect** — decides evergreen vs. reference filing, adds Templater frontmatter, wikilinks to the anchors found in step 2, and flags which MOC it belongs under. Your words are authoritative; the skill only polishes formatting.
6. **Schedule a revisit** — adds the new note to the vault's weekly-review retrieval queue so you restate the claim from memory before checking it again later.

If the machine has no vault, it falls back to a portable temp-vault package you merge back by hand, with a `MERGE.md` checklist and a zip archive instead of step 6.

The skill only writes the distilled note itself — it does not reorganize existing documents. Once a note exists and later needs restructuring into Diátaxis blocks, that hands off to knowledge-doc-writing, not to another learn-loop run.

## Related skills

- **knowledge-doc-writing** — takes over once a note is distilled and needs reorganizing into tutorial/how-to/reference/explanation blocks; learn-loop only handles the interactive learning and initial write, never the restructuring.
- **obsidian-vault** — general-purpose search/create/organize operations over the same vault; reach for it directly when you just want to find or file a note, without the six-step teach-then-quiz loop.

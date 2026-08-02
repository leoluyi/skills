# Taste Distiller

If you keep rewriting AI output the same way, you already hold a standard — you just haven't written it down, which is why every new chat starts from zero. This skill mines your actual rejections and turns the pattern behind them into a reusable rubric: Markdown for you to review and refine, JSON for an evaluator agent to grade against.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a taste-distiller -y
```

To update later:

```
npx skills update taste-distiller
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/taste-distiller/SKILL.md)

## What it does

It runs as a continuous conversation through four stages, none of them announced out loud.

It locates the domain you care most about, then mines three to five real moments where you rejected or rewrote AI output — asking what the AI gave you, exactly where you winced (which word, which sentence, which structural choice), what you changed it to, and what standard you were applying in one line. If you blank on examples, it prompts with friction questions: the last time the output was too empty, too slick, too templated; the last time it looked finished but missed the point; the last time you gave up explaining and rewrote it yourself.

From those it synthesizes 3-6 recurring preferences, each with a name in your own vocabulary, the failure mode in observable terms, the positive standard, and which rejection moments support it. You confirm or correct that list before anything is expanded.

Then each confirmed preference becomes a 1-5 rubric, plus a Context paragraph, plus a Reusable Instructions block you can paste into a chat tool's custom instructions — and the whole thing again as JSON for an evaluator's grading prompt.

## When to use

When the same rewrite keeps happening and you want the standard captured once — as custom instructions, as an evaluator's grading prompt, as team-visible documentation, or as a self-review checklist before publishing.

## When not to

Not to generate content in your style — the skill mines your taste, it doesn't perform it. Not to clean the AI-isms out of one particular draft. And not to define what an agent run should achieve; that's a goal spec, not a taste profile.

## How it works

The discipline is in what it refuses.

**No abstract feedback.** "It felt off" and "太 AI 味" aren't accepted as answers. It pushes for the specific sentence, phrase or structural move that triggered the reaction, because a rubric built on adjectives grades nothing.

**No invented preferences.** Every rubric line has to be traceable to a rejection you actually described. If a rule can't be sourced, it doesn't ship.

**No quality words in the tiers.** Tiers describe observable behaviour — tier 1 names a specific anti-pattern ("opens with 在這個快速變化的時代"), tier 5 names a recognizable mark ("opens with a specific, time-stamped data point"). Tier 3 is the floor of shippable, tier 4 is clearly good, tier 5 is the bar. Same vocabulary axis all the way up.

**No smoothing over contradictions.** If your examples disagree with each other, it surfaces the conflict and asks which version you actually want, rather than averaging them into something you'd reject too.

The bar it holds itself to: another taste-savvy human should be able to grade outputs with the finished profile and reach roughly your verdicts. If it reads generic, that's a signal to mine another round of rejections.

## Related skills

`goal-definer` points here when a task hinges on subjective quality and its Verification element needs a real standard to reference instead of a passing command. For cleaning AI-isms out of a specific piece of Traditional Chinese prose rather than defining the standard, `humanizer-zh` is the one that does the editing.

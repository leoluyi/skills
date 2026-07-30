# blog-writing-zh backlog

Repo-level and `tools/` items live in the root [`backlog.md`](../../backlog.md).

- [ ] **Mine `ecc:brand-voice` for a source-derived voice-profile path.** Noted 2026-07-28.
  (`ecc:brand-voice` is an ECC plugin skill at
  `~/.claude/plugins/marketplaces/everything-claude-code/skills/brand-voice/`.) It builds a
  *durable* voice profile from 5–20 real samples of the user's own writing (rhythm, compression
  vs explanation, source priority order, public-launch vs private-working voice split) and
  reuses that profile across channels instead of re-deriving style per piece. This skill derives
  voice the other way: fixed presets over composable axes (opening × persona × metaphor ×
  closing), modeled on seven *studied* blogs, not on the user's own corpus. Worth evaluating
  whether to add a 「用我自己的既有文章當風格來源」 path — a profile extracted once, cached in the
  repo, then fed to the axes as a preset — versus keeping the studied-blog presets as the only
  recipe source. Constraints: the ECC skill is a plugin, so per this repo's portability rule it
  can be a pointer at most, never load-bearing; and any new path needs its own eval bar before
  shipping.

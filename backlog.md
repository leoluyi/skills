# Skills backlog

Ideas not yet drafted. Signal: friction hit 2+ times.

## Ideas
- [x] **avoid-ai-writing-zh: run the GAN adversarial protocol (round 1).** Done 2026-07-17 (n=5 human / 3 AI). FP=0/3 voice-bearing, recall=3/3. Log in `evals/avoid-ai-writing-zh/benchmark-protocol.md`.
- [x] **avoid-ai-writing-zh: decide structure-signals gating for non-blog genres.** Resolved by round 1: expanded auto-enable to voice-bearing genres (casual/blunt, technical-blog/blog personal register, newsletter), kept voice-neutral (docs, RFP, 簽呈, 公文, SOP, investor-email) excluded. Data-backed, not by fiat.
- [x] **Strip development-process noise from skill content.** Done 2026-07-17 (PRs #7 a75b0bd, #8 8ad206b). Removed iteration provenance, derivation narrative, and method-named headers from `avoid-ai-writing-zh/SKILL.md` and 8 `blog-writing-zh/references/*.md`; codified the rule + finishing-check grep in `CLAUDE.md`. Provenance now lives in DEVELOPMENT.md / benchmark-protocol.md / commits.
- [ ] **avoid-ai-writing-zh: GAN protocol round 2 — expand corpus.** Round 1 n is small (3 voice-bearing human / 3 AI). Add more genres and authors, add an English-language bucket, and stress the metaphor-clustering carve-out with more dense-tutorial samples before treating the gate as settled.
- [x] **avoid-ai-writing-zh: extract English rules to references/ (progressive disclosure).** Done 2026-07-17. SKILL.md 935→565 lines; moved Formatting, Sentence structure, Tier 1/2/3 tables, and the micro-categories (Template phrases … Excessive structure) into `references/english-rules.md` (377 lines) with a pointer in SKILL.md. Kept inline: intro/modes/language-routing, the language-agnostic structural rules (Rhythm/Vocabulary/Paragraph-reshuffle/Treadmill/When-to-rewrite), the full Traditional Chinese section, Severity/profiles/output/tone. Verified: no anchor links pointed into the moved block; the L48 `#結構級訊號` anchor still resolves; the zh "與英文版 X 同源" refs read fine (reference-file header names where Emotional flatline / Reasoning chain artifacts / Acknowledgment loops now live). Version 1.1.1→1.1.2.
- [ ] ...

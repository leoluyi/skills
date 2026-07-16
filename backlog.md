# Skills backlog

Ideas not yet drafted. Signal: friction hit 2+ times.

## Ideas
- [x] **avoid-ai-writing-zh: run the GAN adversarial protocol (round 1).** Done 2026-07-17 (n=5 human / 3 AI). FP=0/3 voice-bearing, recall=3/3. Log in `evals/avoid-ai-writing-zh/benchmark-protocol.md`.
- [x] **avoid-ai-writing-zh: decide structure-signals gating for non-blog genres.** Resolved by round 1: expanded auto-enable to voice-bearing genres (casual/blunt, technical-blog/blog personal register, newsletter), kept voice-neutral (docs, RFP, 簽呈, 公文, SOP, investor-email) excluded. Data-backed, not by fiat.
- [ ] **avoid-ai-writing-zh: GAN protocol round 2 — expand corpus.** Round 1 n is small (3 voice-bearing human / 3 AI). Add more genres and authors, add an English-language bucket, and stress the metaphor-clustering carve-out with more dense-tutorial samples before treating the gate as settled.
- [ ] **avoid-ai-writing-zh: extract English rules to references/ (progressive disclosure).** SKILL.md is 935 lines, monolithic (no references/ dir). Move the English-phrase-specific detail — Formatting, Sentence structure, Words/phrases Tier 1/2/3, and the ~40 single-line micro-categories (Template phrases … Excessive structure) — into `references/english-rules.md`, leaving a pointer in SKILL.md. KEEP inline: intro/modes/language-routing, the language-agnostic structural rules (Rhythm and uniformity, Vocabulary diversity, Paragraph-reshuffle, Treadmill, When-to-rewrite — the zh 結構級訊號 section cross-references these), the full Traditional Chinese section, Severity/profiles/output/tone. Caveat: zh section's "與英文版 X 同源" refs to Emotional flatline / Reasoning chain artifacts / Acknowledgment loops will point into the reference file — refs are by name so they still read fine. Verify the L48 --structure-signals anchor still resolves after the edit. Deferred from 2026-07-17 session (cost ceiling).
- [ ] ...

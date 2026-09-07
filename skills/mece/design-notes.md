# MECE design notes

## Intent and provenance

The user requested a concise, manually invoked skill for both general decomposition and work or meeting document restructuring.
The motivating reader verdict was: 「看完仍不知道這場會議到底要討論哪幾件事」.
The user chose outline-first delivery with original-content destinations, merges, and pending gaps, followed by full rewriting only after direction approval.
Upper-level reconstruction is permitted, including separating work categories from shared discussion dimensions.
Reasonable assumptions allow progress; material classification ambiguities warrant questions.
Unverified gaps remain pending with reasons, and decomposition normally starts at two levels without fixed counts or equal-depth requirements.

Style reference: [Matt Pocock's skills](https://github.com/mattpocock/skills), especially the concise concept-led instructions in grilling and wait-what.
The runtime is original wording; it borrows the compact style rather than copying a router or introducing sibling prerequisites.

## Validation status: local checks pass; release gate blocked

Local validation on 2026-09-07 passed: three eval cases with ten expectations, matching manual invocation declarations, trigger skip for manual invocation, and generated catalog consistency.
The first case embeds the user-provided meeting outline to preserve its real overlaps and reader context; it contains internal work material and must not be uploaded without authorization.
Cases two and three are synthetic regression guards, not independent evidence of improvement.

The repository gate rejects an absent skill at HEAD rather than treating it as vanilla.
A temporary, non-repository adapter supplied an empty baseline to the existing gate while preserving its independent parallel arms, repeated rounds, and blind grading.
The sandboxed attempt failed to connect to the model service.
Automatic approval review rejected the network-enabled retry because it would upload private fixture content to an external model service without explicit payload-and-destination authorization.
The user subsequently explicitly authorized sending the meeting-outline cases to OpenAI Codex for A/B evaluation.
The first connected trial produced an expanded near-full rewrite before approval, contrary to the requested outline-first workflow.
That trial was stopped, and the runtime now defines the first deliverable as headings with one-line scopes, a compact content mapping, and a structural check.
The revision also makes scope assumptions visible and asks the agent to test ownership at neighboring category boundaries.
The revised candidate passed local fixture validation and invocation/catalog checks.
The user then authorized and completed the repeated parallel gate after the latest wording change.
Six rounds ran with 10 judgments per round and 0 runner or grader errors.
The first gate after the outline-first revision was INCONCLUSIVE: 4 expectations were confirmed improvements, 0 were confirmed regressions, and 6 differences remained unresolved across rounds.
The follow-up wording fix for output-language leakage and neighboring-category boundaries reduced unresolved differences to 4, but the latest gate was still INCONCLUSIVE with 4 confirmed improvements and 0 confirmed regressions.
The strongest stable improvements were outline-first delivery, preserving a clear existing structure, and separating mixed classification axes.
Because unresolved differences remain, this evidence does not satisfy the repository's release gate; further prompt or fixture changes would need human judgment rather than automatic release.
The eval suite was subsequently reduced from 22 to 7 expectations at the user's request, retaining the three real scenarios and their core behavior checks.
The reduced suite passes local validation.
Its external gate ran for six rounds with 7 judgments per round and 0 errors, but remained INCONCLUSIVE with 2 confirmed improvements, 0 confirmed regressions, and 5 unresolved differences.
Further reducing the suite would remove coverage rather than resolve the candidate-versus-vanilla variance.

The catalog builder also reordered two existing entries according to their existing order values; their content was unchanged.

# Writing preflight for a blank page

Use this reference when the user invokes `humanizer-zh` before a draft exists and there is no exact file path or explicit finished-prose mode.

An unparameterized invocation defaults here, even if the user did not repeat the words “preflight” or “handoff”.

This is a preflight handoff, not a drafting pass.

The handoff gives the downstream writer a small writing contract: what the document must accomplish, which voice to preserve or build, which surface patterns to avoid, which facts require support, and which gaps still belong to the user.

It does not write the document, invent author experience, add unsupported claims, or replace the downstream writer's domain-specific structure.

If a draft already exists, use the normal `detect`, `rewrite`, or `edit-in-place` route instead.

## Operating stance

Treat the plan, brief, source pack, author samples, and user preferences as the available material.

Separate what the user supplied from what you infer from genre conventions.

Mark an inference as a recommendation rather than presenting it as the user's voice or intent.

Use the leading word **contract** for the compact set of decisions the writer must carry forward.

Use the leading word **gap** for information the writer cannot safely supply.

Use the leading word **handoff** for the final artifact passed to the next skill.

Prefer positive instructions such as “state the claim, evidence, and consequence directly” over long lists of prohibited phrases.

Keep only the anti-patterns relevant to this document's genre and language.

Do not load the full humanizer rule catalog into the writer's context unless a downstream audit specifically needs it.

## Procedure

### 1. Confirm the branch

Confirm that no draft exists and that no exact file path is waiting for a `detect` or `modify` choice.

The downstream plan or writing skill may be named in the request or implied by the surrounding context.

An unparameterized invocation is enough to enter this branch.

If a draft already exists, or an exact file path was supplied without a mode, stop this branch and route to the finished-prose workflow or the file-choice prompt.

Completion criterion: the input is a brief, plan, source pack, or writing context rather than a document to edit.

### 2. Read the available context

Read the user's goal, audience, publication context, document type, constraints, source material, author samples, and explicit style preferences.

Record which of these were supplied and which were inferred.

Do not treat the agent's own previous prose as an author sample unless the user adopted it as such.

Completion criterion: every proposed style or structure decision can point to a supplied input or is labelled as a genre recommendation.

### 3. Build the contract

Write one compact contract covering:

- **Purpose:** what the document must help the reader understand, decide, or do.
- **Audience:** what the reader already knows and what they need next.
- **Genre:** blog, essay, README, spec, SOP, RFP, memo, proposal, or another named form.
- **Structure:** the smallest outline that carries the purpose from opening to close.
- **Voice:** the declared author traits, or a restrained genre-appropriate default when no author traits were supplied.
- **Evidence:** the source pack, required facts, citations, examples, measurements, or decisions that must support the document.
- **Boundaries:** claims, experiences, commitments, or details that the writer must not infer.

Prefer one sentence per decision over a large style manifesto.

Completion criterion: the downstream writer can begin without guessing the document's purpose, audience, genre, or evidence boundary.

### 4. Separate voice from surface cleanup

For signed prose, identify positive voice features such as stance, first-person experience, concrete scenes, self-created metaphors, deliberate rhythm, or a declared level of informality.

Only preserve a positive voice feature when the user supplied it, declared it, or selected it from an explicit profile.

For transactional documents, interpret human writing as concrete, direct, readable, and useful rather than personal or confessional.

Do not manufacture first-person experience, emotional reaction, personal judgment, or signature metaphors to make a blank document sound human.

Completion criterion: every positive style feature has an evidence source, a user declaration, or an explicit genre rationale.

### 5. Select surface hazards

Choose a short list of likely hazards for this genre.

Typical hazards include empty importance claims, generic conclusions, contrast frames used as decoration, abstract claims without delivery, chat residue, unsupported authority, fabricated citations, uniform paragraph rhythm, and headings that announce the document instead of carrying its subject.

State the desired replacement behaviour next to each hazard.

For example, write “name the measurable change and its owner” instead of only writing “avoid abstract claims”.

Do not turn a legitimate convention into a defect merely because it appears in the humanizer catalog.

Completion criterion: each selected hazard has one positive replacement behaviour and a genre-specific carve-out where needed.

### 6. Record gaps

List information that must come from the user, a source, or a tool before the writer can make the claim safely.

Typical gaps include personal experience, dates, numbers, trade-offs, ownership, source location, audience decisions, success criteria, and unresolved terminology.

Turn high-impact gaps into focused questions.

If the user does not answer, keep the gap visible in the handoff and make the writer avoid the unsupported claim.

Do not fill gaps with plausible examples in the handoff.

If the user explicitly requests fictional or illustrative material, record that the downstream writer may create clearly labelled examples, but keep factual gaps unresolved.

Completion criterion: every high-impact unsupported claim has either a source, an owner, a question, or an explicit “do not claim” boundary.

### 7. Emit the handoff

Return only the compact handoff and any questions that block safe writing.

Use this shape:

```markdown
## Writing contract

- Purpose:
- Audience:
- Genre:
- Reader action or takeaway:
- Structure:
- Voice:

## Positive style

- Keep:
- Prefer:
- Let the prose vary by:

## Surface hazards

- Hazard:
  - Replacement behaviour:
  - Genre carve-out:

## Evidence boundary

- Sources:
- Required facts:
- Protected details:
- Unsupported claims:

## Gaps for the author or researcher

- Question:
- Why it matters:

## Handoff instruction

Write the document under this contract.
Use supplied facts and sources as the boundary of factual claims.
Leave unresolved gaps visible instead of inventing content.
Run a fresh humanizer detect pass after the draft exists.
```

Do not include this scaffold's headings in the final document unless the user asks for a writing plan.

Completion criterion: the handoff is short enough to pass to the next skill, every section is either filled or explicitly marked as a gap, and no prose is presented as finished copy.

## Handoff rules by document family

### Signed prose

Prioritize a declared stance, concrete author material, specific scenes, and a recognisable cadence.

When these are absent, ask for them or mark them as gaps.

Do not use `作者隱身` as permission to invent a persona.

### Transactional documents

Prioritize task clarity, factual precision, explicit ownership, usable sequence, and terminology appropriate to the reader.

Do not add personal voice merely to make a README, spec, SOP, RFP, or memo sound less machine-written.

For proposals and recommendations, require an explicit decision or recommendation when the document's purpose demands one.

### Technical documents

Keep established technical terms, commands, identifiers, code, and normative language intact unless the user asks for terminology changes.

Prefer concrete examples, preconditions, expected results, and failure handling over broad claims about reliability or efficiency.

Do not replace technical precision with casual language.

## Final handoff check

Before passing the handoff to the writer, check all of the following:

- The handoff describes a writing contract, not a finished document.
- The writer knows the purpose, audience, genre, and evidence boundary.
- Positive voice features are sourced or labelled as recommendations.
- Every selected surface hazard has a replacement behaviour.
- Missing author material is a gap, not an invitation to guess.
- The handoff does not force artificial irregularity, fake specificity, or personal experience.
- The downstream writer is told to run a fresh humanizer audit after generating the draft.

The preflight is complete when the downstream writer can start writing without guessing what must be true, what may be stylistic, and what remains unknown.

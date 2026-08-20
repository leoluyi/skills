---
name: developer-spec-workflow
description: >-
  Build a developer-facing technical specification and runnable sample code
  from a rough brief through documented grilling, scope decisions, tracer-bullet
  implementation, and end-to-end proof. Use when the user asks to
  「從無到有產製技術規格書和 sample code」「先訪談再寫開發規格」
  「用 AI 工作流產出技術規格與範例」, or requests an end-to-end
  spec-to-sample workflow. Do NOT invoke for a writing-only knowledge document,
  implementation from an already-approved spec, an RFP or procurement spec, or
  a one-off code example.
app-description: >-
  從初始需求開始，透過逐題訪談留下決策脈絡，產出開發者技術規格、可執行 sample code
  與 end-to-end 驗證證據。適用於從零建立規格與範例的完整 AI 協作流程。
version: 0.1.0
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. Requires ordinary repository file access and the target stack's own validation tools.
metadata:
  author: Lu Yi
  tags: agent-workflow technical-specification sample-code requirements-interview tdd
  agentskills_spec: "1.0"
  openclaw:
    emoji: "🧭"
---

# Developer Spec Workflow

Turn rough intent into one developer-facing specification and one runnable proof that agree with each other.
The work is a sequence of evidence-producing stages, not a single generation pass.
Decisions survive in repository files so a fresh session can continue without trusting chat history.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output - option labels, generated-document headings, table column names - not just prose.
If the user explicitly asks for another language, that wins.

Language follows the request, not the source material.
When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output.
Never mirror this file's language into your response.

## Working Set

Inspect the repository before choosing paths and reuse its established documentation, sample, test, and decision-record conventions.
For a greenfield repository, start with this smallest useful working set:

```text
README.md
docs/
  brief.md
  context.md
  technical-spec.md
samples/
  <chosen-stack>/
    README.md
    <source and one runnable check>
```

`docs/brief.md` preserves the user's initial prompt and supplied source material as intake evidence.
Treat it as immutable unless the user explicitly corrects the original input.

`docs/context.md` is the live control plane: confirmed decisions, explicit assumptions, open questions, source and version notes, current stage, and next action.
Update it after every material decision so rejected paths and stale chat do not become implicit requirements.

`docs/technical-spec.md` is the single specification of record.
The sample is the executable source for code behavior; the spec points to it instead of maintaining a second pseudo-implementation.

Add `docs/decisions/`, a ticket file, or a verification script only when an actual decision, task volume, or repeated command earns it.
Do not archive chat transcripts in the repository.

## 1. Establish the Baseline

Read repository instructions, existing artifacts, source code, tests, and current Git state before proposing a structure.
Determine the intended reader, the job the spec must let that reader complete, the requested deliverable formats, and the closest end-user execution environment.
Preserve the initial prompt in the brief, then record what is already known and what is still open in the context file.

This stage is complete when the original request is preserved, the reader and outcome are explicit, and every known repository constraint has a home in the working set.

## 2. Grill with Docs

Ask the single highest-leverage unanswered question per turn.
Prefer a concrete choice when the answer space is discrete, and explain what changes depending on the answer.
Derive facts from the repository or authoritative sources instead of asking the user to rediscover them.

Drive questions from decisions that can change architecture, behavior, security, data handling, dependencies, supported versions, scope, or acceptance evidence.
Common axes are target environments, client stack and driver, external systems, trust boundaries, secret and key ownership, compatibility range, failure behavior, operational ownership, and what the sample must prove.

After each answer, edit `docs/context.md` in place.
Separate confirmed decisions, assumptions accepted for now, and unresolved questions.
For version-sensitive technical facts, record the applicable version and a primary source.

Continue until every unresolved item is either harmless to the design or recorded with an explicit assumption that the user accepted.
Then present one compact decision summary for confirmation before drafting the specification or implementation.

This stage is complete when no open item can materially change the architecture, security boundary, public behavior, sample stack, or acceptance conditions.

## 3. Write the Specification of Record

Shape the document around the reader's work rather than a fixed template.
A developer-facing specification normally needs purpose and audience, scope and non-goals, supported environment and versions, terminology, architecture and trust boundaries, data or request flows, interfaces and configuration, setup and usage, failure modes, security and operations, limitations, acceptance conditions, and sources.
Include only sections supported by the project's scope.

Make every requirement observable.
Replace words such as "secure", "works", or "supported" with the configuration, behavior, boundary, or test that demonstrates the claim.
Trace changing technical claims to primary documentation and state their version range or as-of date.

Keep code excerpts short and link them to the runnable sample path.
If the spec and sample disagree, fix the artifact that is wrong and rerun the proof rather than explaining away the difference.

This stage is complete when a developer can identify the supported path, required decisions, expected behavior, known failure modes, and exact acceptance evidence without reading the chat.

## 4. Slice Tracer Bullets

Turn the accepted specification into the fewest vertical slices that can each produce user-visible evidence.
The first slice reaches through the real integration boundary and proves the smallest happy path.
Later slices add negative or unauthorized paths, operational behavior, and optional features only when the specification includes them.

Each slice owns its necessary spec update, sample change, and runnable check.
Keep the slice list in the project's issue tracker when one exists; for a small repository, a checklist in `docs/context.md` is enough.

This stage is complete when every acceptance condition maps to at least one slice and no slice exists only to build an unused layer or abstraction.

## 5. Build the Runnable Proof

For non-trivial logic or integration behavior, make the smallest end-to-end check fail before implementing the slice.
Exercise the same boundary the developer will use: real parser, driver, database, service, authorization path, or protocol as applicable.
Use a substitute only outside the behavior the sample claims to demonstrate, and state that boundary in the sample README.

Keep the sample production-shaped enough to teach correct usage and small enough to audit in one sitting.
Its README gives prerequisites, configuration, run commands, expected output, failure evidence, cleanup, and the exact supported versions.
Secrets, private keys, credentials, and environment-specific identifiers stay outside version control.

Security-sensitive samples include both an authorized success path and the cheapest meaningful negative proof.
Documentation commands are executable commands: run them from a clean state instead of reviewing them visually.

This stage is complete when the end-user path passes, the meaningful negative path behaves as specified, and a clean checkout can reproduce the documented result with only the declared prerequisites.

## 6. Review from the Artifacts

Read the brief, context, specification, sample, checks, and final diff as if the conversation were unavailable.
Use a fresh agent or session when available; otherwise perform the same review from the artifact set alone.
Look for unsupported claims, lost decisions, source/version drift, duplicated code, secret leakage, untested failure paths, and commands that depend on undeclared local state.

Run the repository's relevant validation and report the commands and outcomes.
If an acceptance condition cannot be proven, leave it explicitly unverified with the blocker and required evidence.

The workflow is done when the specification and sample agree, every scoped acceptance condition has evidence, and another developer can reproduce the supported path without conversation history.

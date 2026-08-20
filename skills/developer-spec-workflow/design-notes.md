# Design Notes

## Provenance

This skill adapts Matt Pocock's public workflow vocabulary and sequence: persistent grilling, specification before implementation, tracer-bullet tickets, test-driven execution, and fresh-context handoff.

Primary reference: [mattpocock/skills](https://github.com/mattpocock/skills), MIT License.

The implementation follows this repository's `engineering-guidelines.md` for portability, model invocation, completion criteria, catalog metadata, and eval shape.

## Scope

The user requested one reusable workflow skill, so the draft stays self-sufficient instead of splitting interviewing, specification, tickets, and implementation into required sibling skills.

The skill is model-invoked because users often describe the desired end state without naming a workflow skill.
The trigger boundary requires both a developer specification and runnable sample proof, which keeps it from absorbing ordinary documentation or implementation work.

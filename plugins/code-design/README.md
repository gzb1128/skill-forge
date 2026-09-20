# Code Design

Investigate existing design rationale and shape APIs, types, and module
boundaries for code changes. Investigation methods are conditional defaults;
user authorization and repository contracts remain requirements. Focused
verification and remaining coverage are recorded in the repository's
`docs/verify/code-design.md`.

| Skill | Use when | Result |
|---|---|---|
| `investigate-design-rationale` | A code-design decision or historical constraint needs explanation | Cited rationale, current constraints, and explicit uncertainty |
| `architect` | A requested code change has unresolved interface or ownership decisions | Caller usage, design shape, tradeoffs, and verification boundaries |

Both skills are model-invoked for their specific trigger contexts and can be
requested explicitly. Ordinary coding does not trigger either by itself. Each
works independently: no `poteto-mode`, `how`, `arena`, reviewer, model routing,
or other plugin is required. `code-quality` continues to assess concrete
changes; `agent-docs` continues to govern durable knowledge placement.

## Conditional methods

`investigate-design-rationale` uses historical investigation when rationale is missing; `architect` uses
caller examples and experiments when a structural decision is unresolved. Both
can load `references/code-flow.md` when a missing current-path connection affects
their task. It adapts pstack's `how` as supporting knowledge, not a third skill:
a plain runtime walkthrough does not acquire a design or history workflow.
Reuse adequate evidence, stop when the decision is supported, and revisit the
affected assumption when new evidence contradicts it. Search depth, alternative
count, model choice, and permitted delegation remain task-specific choices.
Implementation playbooks and global workflow orchestration are not installed by
this adaptation; a future method needs a concrete use case and evidence of value.

## Examples

- "Why does retry reuse the accepted input rather than the latest config?"
- "Can this compatibility branch be removed? Establish why it exists first."
- "Design the adapter interface from its callers. Show the design only."
- "Design and implement this change within the existing admission boundary."

Design-only requests do not authorize product edits. Design-and-implement
requests continue without an extra approval gate. An explicit checkpoint is
honored. Neither skill installs tools or writes shared knowledge automatically.

## Provenance

Adapted from Lauren Tan's MIT-licensed
[pstack](https://github.com/cursor/plugins/tree/e31650eea443aaea1e84cc15d88c13f40080b275/pstack), source snapshot
`e31650e`, inspected on 2026-09-18. Source material: `why/SKILL.md`,
`why/references/epistemics.md`, `how/SKILL.md`, how's `explorer-prompt.md`
and `explainer-prompt.md`, `architect/SKILL.md`, and architect's
`runner-prompt.md`, `rationale-template.md`, and `design-red-flags.md`.

Skill Forge retains evidence calibration, historical rationale, caller-first
design, and concrete verification. It replaces mandatory source fan-out,
fixed model rosters, nested skill workflows, alternative quotas, and automatic
implementation with task-specific depth and authorization boundaries. Repository
practice informs the checks; no DMS path, service, or environment is required.
License terms and third-party notices are maintained once in the Skill Forge
repository-root `LICENSE`; plugin and skill directories do not duplicate them.

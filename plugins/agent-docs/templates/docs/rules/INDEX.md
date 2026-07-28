# Rules Index

Coding standards and best practices. Each rule has a **"When to Use"** trigger so agents can locate the relevant rule by task context.

## Rules

| Rule | Description | When to Use |
|------|-------------|-------------|
| [Non-Derivability Principle](non-derivability.md) | Only write down what cannot be derived from code, git history, or existing docs | **Before writing ANY doc** — the universal filter |
| [Document Conventions](document-conventions.md) | Documentation tree, naming rules, when to add a sub-package `AGENTS.md` | Creating/refactoring any file under `docs/` |
| [OpenAI Harness Engineering](openai-harness-engineering.md) | Agent-First engineering practices: progressive disclosure, lean prompt surfaces, documentation organization | Reviewing the overall doc philosophy; auditing codemaps, `AGENTS.md`, skill instructions, or tool descriptions |

## Related Workflows

- Capture non-obvious session insights in the nearest relevant `AGENTS.md` after applying the non-derivability filter.
- Periodically audit `AGENTS.md` memory surfaces for staleness, duplication, and misplaced details.
- Keep memory workflows manual and approval-gated; do not auto-write persistent guidance without human review.

<!-- TODO: Add project-specific rules below. Examples:
| Go Coding Standards | Error handling, Context usage, interface design | Writing/reviewing Go code |
| API Design Guide | REST/gRPC naming, versioning, error codes | Adding or modifying an API |
-->

## How to Use

1. **By scenario** — scan the "When to Use" column to find the rule that matches your current task
2. **By topic** — if you know the area, open the file directly
3. **Adding a new rule** — create a `.md` file under this directory, then update this INDEX

## Anti-Patterns for Rule Documents

| ❌ Don't | ✅ Do |
|---------|------|
| Write a 500-line rule document covering everything | One file per topic, 100-200 lines |
| Skip concrete code examples | One excellent before/after example per rule |
| Skip "When to Use" in INDEX | Always add — agents triage by trigger, not title |

# {{PROJECT_NAME}}

This file is the entry point for any AI coding agent working in this repository.
Keep it concise, verified, and useful across repeated tasks.

## Quick Reference

| Action | Command |
|--------|---------|
| Build | `{{BUILD_COMMAND}}` <!-- TODO: e.g., `make all`, `npm run build`, `cargo build` --> |
| Test | `{{TEST_COMMAND}}` <!-- TODO: e.g., `go test ./...`, `npm test`, `pytest` --> |
| Lint | `{{LINT_COMMAND}}` <!-- TODO: e.g., `golangci-lint run ./...`, `npm run lint` --> |
| Run locally | `{{RUN_COMMAND}}` <!-- TODO --> |
| Generate code | `{{CODEGEN_COMMAND}}` <!-- TODO: optional, delete this row if N/A --> |
| Clean | `{{CLEAN_COMMAND}}` <!-- TODO: optional, delete this row if N/A --> |

## Architecture

<!-- TODO: Briefly describe the project and its main runtime components. Route
     readers to adequate existing architecture docs; otherwise use
     docs/architecture/overview.md for a system needing separate explanation.
     A simple tool may be fully explained here. Cover core flows, handoff data,
     decision owners, durable effects, and runtime state as applicable.
     Link existing living contracts instead of duplicating them; do not invent layers.
     A small responsibility table or diagram is useful when it prevents wrong-layer edits.
     Example:
     Three components, one repo:
     - **api-server** (`cmd/api/`) — HTTP API entry; delegate use cases to their owners
     - **worker** (`cmd/worker/`) — Async job execution entry
     - **cli** (`cmd/cli/`) — Command-line entry
     Source navigation stops at packages. Exact paths remain useful when they
     are rule targets, such as a schema source and its generated output.
-->
{{ARCHITECTURE_SUMMARY}}

## Common Tasks

| I want to... | Start here |
|---|---|
| {{COMMON_TASK}} | `{{OWNER_PACKAGE_OR_DOC}}` <!-- TODO: verified owner package or document link --> |

## Key Patterns

<!-- TODO: Describe useful project-specific patterns/conventions.
     Examples:
     - **Generated code**: Edit source definitions, regenerate outputs — never hand-edit generated files
     - **DI**: Uber FX (runtime), Wire (compile-time)
     - **Tests next to source**: `_test.go` lives with the file it tests
-->

## Golden Rules

<!-- TODO: Add only repo-specific hard rules that agents are likely to
     violate without an explicit reminder. Delete this comment when complete. -->

## Knowledge Maintenance

- Use `/agent-docs:learn` only when explicitly reviewing a session to capture
  newly discovered repository knowledge. Handle requested document and task-list
  updates directly without routing them through `learn`.
- Use `/agent-docs:curate` to assess or repair existing knowledge by topic across
  instruction entries and docs, including missing architecture coverage.
  Preserve explicit assessment/proposal checkpoints.
- Use `/agent-docs:setup-coding-rules` for explicit adoption of selected coding rules.
- Create a docs category and its `INDEX.md` only when the first useful document
  in that category is admitted.
- Maintain current architecture in the linked existing home or, by default,
  `docs/architecture/`. Update responsibilities, data handoffs, dependencies, and
  state ownership when behavior changes; keep implementation navigation at packages.

## Development Workflow

1. Locate the owning entry flow and existing contract before changing behavior
2. Make changes within that responsibility boundary
3. Run `{{LINT_COMMAND}}` on affected package — fix in-scope lint errors <!-- TODO -->
4. Run `{{TEST_COMMAND}}` on affected package first <!-- TODO -->
5. Update existing knowledge surfaces when their verified guidance changed
6. Commit with a message that explains why the change matters

## Sub-Package Rules

<!-- TODO: Add rows for any sub-package with its own AGENTS.md (complex modules
     with state machines, cross-module constraints, etc.). Omit this section if none.
     Read applicable parent and module instructions before making changes. -->

| Module | Rules Doc | Reason |
|--------|-----------|--------|
| _none yet_ | — | — |

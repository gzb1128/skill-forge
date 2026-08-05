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

<!-- TODO: 1-3 sentences describing what this project IS and the main components.
     Example:
     Three components, one repo:
     - **api-server** (`cmd/api/main.go`) — HTTP API server
     - **worker** (`cmd/worker/main.go`) — Async job executor
     - **cli** (`cmd/cli/main.go`) — Command-line tool
-->
{{ARCHITECTURE_SUMMARY}}

## Common Tasks

| I want to... | Start here |
|---|---|
| {{COMMON_TASK}} | `{{SOURCE_ENTRY_PATH}}` <!-- TODO: add only verified, recurring entry points --> |

## Key Patterns

<!-- TODO: 3-5 bullets describing the dominant patterns/conventions of this codebase.
     Examples:
     - **Generated code**: Edit source definitions, regenerate outputs — never hand-edit generated files
     - **DI**: Uber FX (runtime), Wire (compile-time)
     - **Tests next to source**: `_test.go` lives with the file it tests
-->

## Golden Rules

<!-- TODO: Add only 3-7 repo-specific hard rules that agents are likely to
     violate without an explicit reminder. Delete this comment when complete. -->

## Knowledge Maintenance

- Use `/agent-docs:learn` only when explicitly reviewing a session to capture
  newly discovered repository knowledge. Handle requested document and task-list
  updates directly without routing them through `learn`.
- Use `/agent-docs:remember` to audit this file and any scoped `AGENTS.md` files.
- Use `/agent-docs:curate` to audit an existing `docs/` knowledge base.
- Create a docs category and its `INDEX.md` only when the first useful document
  in that category is admitted.

## Development Workflow

1. Make changes
2. Run `{{LINT_COMMAND}}` on affected package — fix lint errors <!-- TODO -->
3. Run `{{TEST_COMMAND}}` on affected package first <!-- TODO -->
4. Update existing knowledge surfaces when their verified guidance changed
5. Commit with a message that explains why the change matters

## Sub-Package Rules

<!-- TODO: Add rows for any sub-package with its own AGENTS.md (complex modules
     with state machines, cross-module constraints, etc.). Leave empty if none. -->

| Module | Rules Doc | Reason |
|--------|-----------|--------|
| _none yet_ | — | — |

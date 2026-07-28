# {{PROJECT_NAME}}

> **Agent-First Engineering**: This repository follows [OpenAI Harness Engineering](docs/rules/openai-harness-engineering.md) —
> "Human at the helm. Agents execute." The knowledge base is structured for agent readability with progressive disclosure.

This file is the entry point for any AI coding agent working in this repository.
For deeper context, follow the links — don't try to absorb everything upfront.

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
| Add/modify an API endpoint | [codemaps/INDEX.md](docs/codemaps/INDEX.md) <!-- TODO: replace with API codemap if useful --> |
| Change database schema | [codemaps/INDEX.md](docs/codemaps/INDEX.md) <!-- TODO: replace with database codemap if useful --> |
| Understand the build/deploy flow | [codemaps/INDEX.md](docs/codemaps/INDEX.md) <!-- TODO: replace with build/deploy codemap if useful --> |
| Troubleshoot a system issue | [troubleshoot/INDEX.md](docs/troubleshoot/INDEX.md) |
| Run an operational procedure | [runbooks/INDEX.md](docs/runbooks/INDEX.md) |
| Use a third-party library | [lib/INDEX.md](docs/lib/INDEX.md) |
| Verify system behavior (dry-run) | [verify/INDEX.md](docs/verify/INDEX.md) |
| Look up a coding standard | [rules/INDEX.md](docs/rules/INDEX.md) |
| Find an architecture map | [codemaps/INDEX.md](docs/codemaps/INDEX.md) |

**Other docs**: [Designs](docs/design/INDEX.md) | [Plans](docs/plans/INDEX.md) | [Templates](docs/_templates/)

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

## Document Creation Rules

Before creating documentation, apply the [non-derivability filter](docs/rules/non-derivability.md)
and [document conventions](docs/rules/document-conventions.md). Consult
[OpenAI Harness Engineering](docs/rules/openai-harness-engineering.md) when
changing codemaps, `AGENTS.md`, skills, or tool descriptions.

## Development Workflow

1. Make changes
2. Run `{{LINT_COMMAND}}` on affected package — fix lint errors <!-- TODO -->
3. Run `{{TEST_COMMAND}}` on affected package first <!-- TODO -->
4. Update relevant docs (codemap, INDEX) if structure changed
5. Commit with a message that explains WHY (business impact), not WHAT (code change)

## Sub-Package Rules

<!-- TODO: Add rows for any sub-package with its own AGENTS.md (complex modules
     with state machines, cross-module constraints, etc.). Leave empty if none. -->

| Module | Rules Doc | Reason |
|--------|-----------|--------|
| _none yet_ | — | — |

See [docs/rules/document-conventions.md](docs/rules/document-conventions.md) for when to add a sub-package AGENTS.md.

## Verification

Verify system behavior via [docs/verify/INDEX.md](docs/verify/INDEX.md). Prefer dry-run modes.

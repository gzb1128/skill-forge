# skill-forge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`skill-forge` is a Claude Code plugin marketplace for forging agent runtime environments. It distills reusable skills into plugins covering repository knowledge, code quality, commit discipline, autonomous fix loops, and OpenCode configuration.

**Core idea:** Human at the helm. Agents execute. The repo is the agent's runtime — knowledge, rules, and workflows must be shaped into forms agents can reliably read, judge, and execute.

**Keywords:** `claude-plugin`, `claude-code`, `agent-skills`, `agent-harness`, `openai-harness-engineering`, `opencode`, `code-review`, `clean-commit`

## Quick Start

```bash
# 1. Add the Skill Forge marketplace
claude plugin marketplace add gzb1128/skill-forge

# 2. Install the plugins you need
claude plugin install agent-docs@skill-forge
claude plugin install code-quality@skill-forge
claude plugin install opencode-customize@skill-forge

# 3. In your target repo, ask Claude:
#    "bootstrap agent docs"       -> scaffold Agent-First docs
#    "review my changes"          -> quality review on local diff
#    "commit this"                -> gated commit with impact message
#    "loopfix"                    -> autonomous review-fix loop
#    "hydrate model config"       -> fill OpenCode custom model parameters
```

Plugin versions are resolved to git commit SHA. Every push produces a new installable version — no manual semver maintenance. Run `claude plugin update <plugin>@skill-forge` (or wait for auto-update) to pull the latest.

## Plugins

| Plugin | Purpose | Skills |
|---|---|---|
| `agent-docs` | Scaffold Agent-First documentation and maintain non-derivable team knowledge | `bootstrap-agent-docs`, `learn`, `remember` |
| `code-quality` | Turn code review, commit gates, diff cleanup, and fix loops into repeatable agent workflows | `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `opencode-customize` | Customize OpenCode configuration, including model metadata hydration and external project references | `hydrate-opencode-models`, `integrate-projects` |

## Skill Catalog

### `agent-docs`

| Skill | Type | Purpose |
|---|---|---|
| `bootstrap-agent-docs` | model-invoked | Generate `AGENTS.md`, `docs/_templates/`, `docs/rules/`, and per-category `INDEX.md` in a target repo |
| `learn` | manual skill (`/agent-docs:learn`) | Persist non-obvious session insights to the right `AGENTS.md` — verified and approval-gated |
| `remember` | manual skill (`/agent-docs:remember`) | Audit `AGENTS.md` knowledge for staleness, duplication, and misplacement |

The template payload used by `bootstrap-agent-docs` lives at `plugins/agent-docs/templates/` and resolves at runtime via `${CLAUDE_PLUGIN_ROOT}/templates/`. No separate repo clone needed.

### `code-quality`

| Skill | Type | Purpose |
|---|---|---|
| `quality-reviewer` | model-invoked | Structured quality pass on local changes: three-pass review, diff hygiene, lint, tests, caller check |
| `clean-commit` | model-invoked | Run quality gates (via `quality-reviewer`) before committing, with messages that explain WHY |
| `diff-cleanup` | model-invoked | Remove AI-generated bloat (slop comments, dead code, defensive noise, redundant logic) from a feature branch diff |
| `loopfix` | model-invoked | Autonomous review-fix loop: reviewer subagent finds issues, main agent triages and fixes, repeat until clean |

### `opencode-customize`

| Skill | Type | Purpose |
|---|---|---|
| `hydrate-opencode-models` | model-invoked | Look up model metadata from the Models.dev catalog and map it to OpenCode custom provider model config |
| `integrate-projects` | model-invoked | Add external codebases to project-level OpenCode `references` so agents can discover and inspect them when relevant |

## What `agent-docs` Scaffolds

When you ask Claude to "bootstrap agent docs" in a target repo, the plugin creates:

```text
your-repo/
├── AGENTS.md                          # root entry for agents (~100-line navigation)
└── docs/
    ├── codemaps/INDEX.md              # architecture maps: concept -> file path
    ├── design/INDEX.md                # design specs: YYYY-MM-DD-<topic>-design.md
    ├── plans/INDEX.md                 # implementation plans: YYYY-MM-DD-<feature>.md
    ├── rules/                         # engineering standards
    │   ├── INDEX.md
    │   ├── non-derivability.md        # non-derivability principle
    │   ├── document-conventions.md
    │   └── openai-harness-engineering.md
    ├── troubleshoot/INDEX.md          # symptom-indexed troubleshooting
    ├── runbooks/INDEX.md              # deterministic operational procedures
    ├── lib/INDEX.md                   # third-party library usage notes
    ├── verify/INDEX.md                # dry-run verification flows
    └── _templates/                    # templates for new docs (copy & customize)
        ├── codemap.md
        ├── design.md
        ├── plan.md
        └── subpackage-AGENTS.md
```

## Practices

| Practice | Meaning |
|----------|---------|
| **Repo as record system** | Knowledge agents can't see doesn't exist. Critical constraints must not live only in chat logs or external docs. |
| **Progressive disclosure** | `AGENTS.md` provides the entry navigation, `docs/codemaps/*.md` points to components, source code carries the details. |
| **INDEX per category** | Every `docs/*/` directory has an `INDEX.md` with a "When to Use" column so agents can triage at a glance. |
| **Non-derivability filter** | Record only what cannot be derived from source code, git history, or existing docs. |
| **Maps, not encyclopedias** | Codemaps maintain concept-to-path tables only — they link to source, never copy code. |
| **Date-prefixed designs/plans** | `YYYY-MM-DD-<topic>-design.md` keeps designs and plans browsable in chronological order. |

Full rationale: [`openai-harness-engineering.md`](plugins/agent-docs/templates/docs/rules/openai-harness-engineering.md).

## Development

This repo is both the marketplace catalog and the plugin source. See [AGENTS.md](AGENTS.md) for the development workflow, local verification commands, and SHA-based versioning policy.

Common commands:

```bash
make validate
make test-skills-link
make test-skills-status
make test-skills-unlink
```

## License

This project is licensed under the [MIT License](LICENSE).

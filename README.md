# skill-forge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`skill-forge` is a Claude Code plugin marketplace for forging agent runtime environments. It distills reusable skills into plugins covering repository knowledge, code quality, commit discipline, autonomous fix loops, OpenCode configuration, and Codex subagent routing.

**Core idea:** Human at the helm. Agents execute. The repo is the agent's runtime — knowledge, rules, and workflows must be shaped into forms agents can reliably read, judge, and execute.

**Keywords:** `claude-plugin`, `claude-code`, `agent-skills`, `agent-harness`, `openai-harness-engineering`, `opencode`, `code-review`, `clean-commit`

## Quick Start

```bash
# 1. Add the Skill Forge marketplace
claude plugin marketplace add gzb1128/skill-forge

# 2. Install the plugins you need
claude plugin install agent-docs@skill-forge
claude plugin install code-quality@skill-forge
claude plugin install skill-creator@skill-forge
claude plugin install opencode-customize@skill-forge
claude plugin install codex-strategy@skill-forge
claude plugin install github-contrib@skill-forge

# 3. In your target repo, ask your agent:
#    "bootstrap agent docs"       -> create a minimal AGENTS.md entry point
#    "review my changes"          -> quality review on local diff
#    "commit this"                -> gated commit with impact message
#    "loopfix"                    -> autonomous review-fix loop
#    "migrate this skill"         -> adapt/create skills with eval discipline
#    "hydrate model config"       -> fill OpenCode custom model parameters
#    "delegate this to subagents" -> route Codex explorers and implementation workers
#    "find issues I can pick up"  -> rank contribution-ready GitHub issues
```

Plugin versions are resolved to git commit SHA. Every push produces a new installable version — no manual semver maintenance. Run `claude plugin update <plugin>@skill-forge` (or wait for auto-update) to pull the latest.

## Plugins

| Plugin | Purpose | Skills |
|---|---|---|
| `agent-docs` | Bootstrap and maintain valuable repository knowledge with focused capture and audit workflows | `bootstrap-agent-docs`, `learn`, `remember`, `curate` |
| `code-quality` | Turn code review, commit gates, diff cleanup, and fix loops into repeatable agent workflows | `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `skill-creator` | Create, migrate, evaluate, and tune skills for Skill Forge plugin workflows | `skill-creator` |
| `opencode-customize` | Customize OpenCode configuration, including model metadata hydration and external project references | `hydrate-opencode-models`, `integrate-projects` |
| `codex-strategy` | Route explicitly requested Codex subagents by task shape and configure an opt-in Luna/max role only after a rejected route and user approval | `codex-subagent-strategy`, `codex-luna-agent-config` |
| `github-contrib` | Find contribution-ready GitHub issues with claimed status, PR linkage, difficulty, staleness, maintainer engagement, and area signals | `find-contributable-issues` |

## Skill Catalog

### `agent-docs`

| Skill | Type | Purpose |
|---|---|---|
| `bootstrap-agent-docs` | model-invoked | Create a minimal root `AGENTS.md` with verified commands and architecture routing |
| `learn` | manual skill (`/agent-docs:learn`) | Retrospectively score, route, and propose newly discovered session knowledge — never a substitute for direct documentation maintenance |
| `remember` | manual skill (`/agent-docs:remember`) | Audit `AGENTS.md` knowledge for staleness, duplication, and misplacement |
| `curate` | manual skill (`/agent-docs:curate`) | Audit the `docs/` knowledge base for stale links, encyclopedia bloat, naming drift, and missing indexes — the docs counterpart to `/agent-docs:remember` |

The minimal `AGENTS.md` template used by `bootstrap-agent-docs` lives at `plugins/agent-docs/templates/` and resolves at runtime via `${CLAUDE_PLUGIN_ROOT}/templates/`. No separate repo clone is needed.

### `code-quality`

| Skill | Type | Purpose |
|---|---|---|
| `quality-reviewer` | model-invoked | Structured local review with one independent reviewer, integrated risk checks, and direct quality gates |
| `clean-commit` | model-invoked | Run quality gates (via `quality-reviewer`) before committing, with messages that explain WHY |
| `diff-cleanup` | model-invoked | Remove AI-generated bloat (slop comments, dead code, defensive noise, redundant logic) from a feature branch diff |
| `loopfix` | model-invoked | Autonomous review-fix loop: reviewer subagent finds issues, main agent triages and fixes, repeat until clean |

### `skill-creator`

| Skill | Type | Purpose |
|---|---|---|
| `skill-creator` | model-invoked | Adapt upstream skills, create Skill Forge plugin skills, design RED/GREEN scenarios, run eval benchmarks, and tune trigger descriptions |

### `opencode-customize`

| Skill | Type | Purpose |
|---|---|---|
| `hydrate-opencode-models` | model-invoked | Look up model metadata from the Models.dev catalog and map it to OpenCode custom provider model config |
| `integrate-projects` | model-invoked | Add external codebases to project-level OpenCode `references` so agents can discover and inspect them when relevant |

### `codex-strategy`

| Skill | Type | Purpose |
|---|---|---|
| `codex-subagent-strategy` | model-invoked | Before an explicitly requested Codex spawn, route explorers to Terra/high, routine implementation to Luna/max, complex implementation to Terra/xhigh, and fresh independent review to Sol/high |
| `codex-luna-agent-config` | approval-gated | After a real Luna route rejection and explicit user approval, configure the isolated `luna_max` custom role without changing global subagent defaults |

Skill Forge keeps marketplace source in plugin layout. Compatible agent skill
installers expose installed skills through `~/.agents/skills/<skill>`.

### `github-contrib`

| Skill | Type | Purpose |
|---|---|---|
| `find-contributable-issues` | model-invoked | Investigate open GitHub issues and rank which ones are worth picking up as a contributor |

## What `agent-docs` Scaffolds

When you ask Claude to "bootstrap agent docs" in a target repo, the plugin
creates one project entry point after showing the plan and receiving approval:

```text
your-repo/
└── AGENTS.md                          # concise commands, architecture, routing, and project rules
```

It does not pre-create `docs/` categories or copy plugin policy into the target
repository. When explicitly invoked for retrospective capture,
`/agent-docs:learn` creates a category and its `INDEX.md` on demand when the
first admitted document needs that surface. Explicit requests to create or
update documentation are handled directly without invoking `learn`.

## Practices

| Practice | Meaning |
|----------|---------|
| **Repo as record system** | Knowledge agents can't see doesn't exist. Critical constraints must not live only in chat logs or external docs. |
| **Progressive disclosure** | `AGENTS.md` provides the entry navigation, `docs/codemaps/*.md` points to components, source code carries the details. |
| **Lean prompt surfaces** | State prompt-resident rules once, expose only task-relevant tools, and keep examples only when they encode a requirement or fix a measured gap. Validate removals against the same representative tasks. |
| **INDEX with the first doc** | A category containing useful documents normally has an `INDEX.md` with routing context; absent categories need no placeholders. |
| **Value-based admission** | Non-derivable knowledge is automatically admitted; derivable knowledge is also recorded when impact, recurrence, discovery cost, actionability, durability, and scope justify the surface cost. |
| **Maps, not encyclopedias** | Codemaps maintain concept-to-path tables only — they link to source, never copy code. |
| **Durable designs, transient task plans** | `YYYY-MM-DD-<topic>-design.md` records lasting decisions and delivery boundaries; step-by-step agent plans stay in the task session. |

Full rationale: [Repository Knowledge Lifecycle](docs/design/2026-08-03-repository-knowledge-lifecycle-design.md).

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

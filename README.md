# skill-forge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`skill-forge` is a Claude Code plugin marketplace for forging agent runtime environments. It distills reusable skills into plugins covering repository knowledge, code design, code quality, commit discipline, autonomous fix loops, OpenCode configuration, and Codex subagent routing.

**Core idea:** Human at the helm. Agents execute. The repo is the agent's runtime — knowledge, rules, and workflows must be shaped into forms agents can reliably read, judge, and execute.

**Keywords:** `claude-plugin`, `claude-code`, `agent-skills`, `agent-harness`, `openai-harness-engineering`, `opencode`, `code-review`, `clean-commit`

## Quick Start

```bash
# 1. Add the Skill Forge marketplace
claude plugin marketplace add gzb1128/skill-forge

# 2. Install the plugins you need
claude plugin install agent-docs@skill-forge
claude plugin install code-design@skill-forge
claude plugin install code-quality@skill-forge
claude plugin install skill-creator@skill-forge
claude plugin install opencode-customize@skill-forge
claude plugin install codex-strategy@skill-forge
claude plugin install github-contrib@skill-forge

# 3. In your target repo, ask your agent:
#    "bootstrap agent docs"       -> create a minimal AGENTS.md entry point
#    "set up repository coding rules" -> adapt pre-edit rules to this repository
#    "why was this boundary added" -> investigate code-design rationale
#    "design this API"             -> caller-first interface and ownership design
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
| `agent-docs` | Bootstrap and maintain valuable repository knowledge with focused capture and audit workflows | `bootstrap-agent-docs`, `setup-coding-rules`, `learn`, `curate` |
| `code-design` | Investigate code-design rationale and shape APIs, types, and module boundaries | `investigate-design-rationale`, `architect` |
| `code-quality` | Turn code review, commit gates, diff cleanup, and fix loops into repeatable agent workflows | `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `skill-creator` | Create, migrate, evaluate, and tune skills for Skill Forge plugin workflows | `skill-creator` |
| `opencode-customize` | Customize OpenCode configuration, including model metadata hydration and external project references | `hydrate-opencode-models`, `integrate-projects` |
| `codex-strategy` | Route explicitly requested Codex subagents by task shape and configure an opt-in Luna/max role only after a rejected route and user approval | `codex-subagent-strategy`, `codex-luna-agent-config` |
| `github-contrib` | Find contribution-ready GitHub issues with claimed status, PR linkage, difficulty, staleness, maintainer engagement, and area signals | `find-contributable-issues` |

## Skill Catalog

### `agent-docs`

| Skill | Type | Purpose |
|---|---|---|
| `bootstrap-agent-docs` | model-invoked | Create a concise root `AGENTS.md` with verified commands and useful architecture coverage; add missing architecture docs when needed |
| `setup-coding-rules` | manual skill (`/agent-docs:setup-coding-rules`) | Explicitly adapt pre-edit coding rules to existing or minimal repository entry points, preserving local policy and semantic coverage |
| `learn` | manual skill (`/agent-docs:learn`) | Capture verified session knowledge in the requested proposal or apply mode; direct documentation maintenance remains a separate task |
| `curate` | manual skill (`/agent-docs:curate`) | Assess or repair knowledge by topic, including missing core-flow explanations and drift across instructions, architecture, contracts, rules, and indexes |

Bootstrap templates have one editable source in `plugins/agent-docs/templates/`.
`make sync-templates` copies them into the bootstrap skill's `assets/templates/`,
including the root entry and architecture overview/index. Plugin and standalone
skill distributions carry the same assets; runtime lookup is skill-relative.

Architecture coverage is a default, with `docs/architecture/` as the default home
for new current-system descriptions. Reuse adequate existing docs at their own
location; a simple tool may need only its root entry. Documentation describes
responsibilities, data handoffs, and state authority at package granularity, with
links to existing contracts. Missing important explanations are audit findings;
missing directories alone are not. Bootstrap establishes initial coverage,
curate maintains it, and learn captures explicitly requested session discoveries.

`remember` is retired. Use `curate` for instruction audits and rule promotion as
well as docs maintenance. Existing cached versions remain unchanged until updated.
`make test-skills-status` identifies retired links; `make test-skills-unlink`
removes only links whose exact target belongs to this checkout, including the
retired path. Links from another install and real directories are preserved.
These commands do not run automatically during installation.

### `code-design`

| Skill | Type | Purpose |
|---|---|---|
| `investigate-design-rationale` | model-invoked | Investigate code-design rationale and historical constraints; distinguish evidence from inference |
| `architect` | model-invoked | Shape APIs, types, and module boundaries when a code change has unresolved structural tradeoffs |

Conditional methods: current-path tracing is a shared, on-demand reference, not
a separate `how` skill. Full behavior and installed-selection verification remain
pending; see [verification](docs/verify/code-design.md) for focused checks. Each
skill is independently usable and also accepts explicit invocation. Ordinary coding is
not a blanket trigger. Design-only requests remain design-only; authorized
implementation continues without an extra gate. No fixed model roster or
mandatory multi-agent workflow. See [Code Design](plugins/code-design/README.md)
for examples and upstream provenance.

### `code-quality`

| Skill | Type | Purpose |
|---|---|---|
| `quality-reviewer` | model-invoked | Structured local review with one independent reviewer, integrated risk checks, and direct quality gates |
| `clean-commit` | model-invoked | Run quality gates (via `quality-reviewer`) before committing, with messages that explain WHY |
| `diff-cleanup` | model-invoked | Simplify authorized branch and pending changes within the chosen design, preserving unrelated work and reporting actual checks |
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
creates a concise project entry point and establishes architecture coverage
under that authorization. A requested preview shows the concrete proposal
without writing. For a system needing separate architecture explanation, the
default output is:

```text
your-repo/
├── AGENTS.md                          # concise commands, architecture routing, and project rules
└── docs/architecture/
    ├── INDEX.md                       # navigation to useful architecture topics
    └── overview.md                    # verified components, core flows, and ownership
```

A simple tool may need only `AGENTS.md`; adequate existing architecture documents
are reused at their established locations. Extra topics and categories are added
only with useful content, without copying plugin policy or an empty template tree.
`curate` maintains existing knowledge and checks missing core-flow explanations.
When explicitly invoked for retrospective capture, `learn` updates the appropriate
knowledge surface. Direct requests to create or update documentation do not
require invoking `learn`.

## Set Up Repository Coding Rules

Run `/agent-docs:setup-coding-rules` when you want coding constraints visible
before edits, without requiring a review or design skill invocation first.
For example: "Set up scope protection and honest verification rules in this
repo. Apply them directly." The skill checks existing semantic coverage and
adapts only the selected rules; a second run can be a no-op. Use "assess only"
for a report without edits.

The target repository owns the resulting rules. Setup preserves local policy,
uses repository-relative contract links, and reports unresolved conflicts.
It does not install hooks, modify personal configuration, or copy the complete
code-quality workflow. `bootstrap-agent-docs` initializes an entry and appropriate
architecture coverage; `curate` maintains existing knowledge; `learn`
captures session discoveries. Plugin installation alone never runs setup.

## Practices

| Practice | Meaning |
|----------|---------|
| **Scenario-based plugin names** | Plugin names identify a work context and responsibility; individual skill descriptions define precise triggers. Packaging does not dictate execution order. |
| **Repo as record system** | Knowledge agents can't see doesn't exist. Critical constraints must not live only in chat logs or external docs. |
| **Progressive disclosure** | `AGENTS.md` provides the entry navigation, architecture documents explain package responsibilities and data flow, source code carries the details. |
| **Lean prompt surfaces** | State prompt-resident rules once, expose only task-relevant tools, and keep examples only when they encode a requirement or fix a measured gap. Validate removals against the same representative tasks. |
| **INDEX with the first doc** | A category containing useful documents normally has an `INDEX.md` with routing context; absent categories need no placeholders. |
| **Value-based admission** | Persist knowledge with identifiable future use and residual value beyond existing carriers; choose the least costly authoritative surface. Neither derivability nor a numeric score decides admission. |
| **Architecture over file inventories** | Record responsibilities, data flow, and boundaries at package granularity. Preserve exact rule targets and runnable inputs/outputs; find implementation details through current callers and wiring. |
| **Durable designs, transient task plans** | `YYYY-MM-DD-<topic>-design.md` records lasting decisions and delivery boundaries; step-by-step agent plans stay in the task session. |

Rationale: [Documentation maintenance](docs/design/2026-09-23-agent-docs-consolidation-design.md), [Knowledge Admission](docs/design/2026-09-18-knowledge-admission-design.md) and the earlier [Repository Knowledge Lifecycle](docs/design/2026-08-03-repository-knowledge-lifecycle-design.md).

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

Original Skill Forge material is MIT-licensed. Third-party material retains its
applicable MIT or Apache-2.0 terms. All license texts, scope mappings, and upstream
attributions are maintained in the repository-root [LICENSE](LICENSE).

# skill-forge

`skill-forge` is a Claude Code plugin marketplace for forging agent runtime environments. The repo hosts the marketplace catalog, plugin source code, skill verification flows, and Agent-First documentation templates.

## Golden Rules

1. **Project-facing content is in English** — `README.md`, `AGENTS.md`, `docs/`, commit messages, code comments, plugin metadata, Makefile help text, GitHub description/topics. Exception: intentionally localized end-user content.

## License and Upstream Attribution

Maintain license texts and third-party attribution once in the repository-root
`LICENSE`, with the affected paths and upstream sources identified. Do not add
per-plugin or per-skill license copies. Preserve applicable upstream terms and
identify local adaptations; the project's MIT license does not relicense imported
Apache-2.0 material.

Put each skill's source links, upstream revision, authorship, adaptation summary,
and applicable license identification in that skill's `README.md`. Keep full
license texts centralized in the root `LICENSE`. Do not place provenance banners,
license notices, or links that require reading attribution in `SKILL.md` or its
runtime references; those surfaces carry task instructions. Skill READMEs are
maintainer documentation, not part of normal skill loading. A workflow explicitly
about importing resources may consult source/license metadata when necessary for
that task; this does not justify loading the skill's own provenance by default.

## Skill Runtime Content

Only information needed to select or execute the skill belongs in its runtime
surfaces: catalog metadata, `SKILL.md`, linked references, executable helpers,
and task assets. Each instruction or resource must support a concrete task
decision, action, output, or verification. Keep conditional material behind a
relevant task condition rather than loading it by default.

Provenance, license attribution, changelogs, maintenance notes, and development
history belong in maintainer documentation such as the skill's `README.md`,
not in runtime instructions or their reference chain. Do not link or require
those documents from `SKILL.md` merely to advertise their existence. A README
being physically present beside the skill does not make it an execution resource.
When maintenance or migration is itself the requested task, consult the metadata
needed for that task without loading the skill's own history by default.

## Plugin Naming and Scope

Name plugins for a recognizable work context and responsibility, such as
`code-design`, `code-quality`, or `opencode-customize`. Use established terms
and lowercase kebab-case. A reader should infer when the plugin is useful.
Group skills by the work they help complete, not a vague benefit such as
"better engineering", the upstream bundle, or an agent persona. Names need
not follow a universal two-word pattern.

Plugin descriptions state the shared use case; skill descriptions distinguish
specific triggers and nearby non-triggers. Adding a plugin does not establish
an automatic workflow chain. Share references where useful while keeping skills
independently usable. Split a plugin when its use cases or installation needs
diverge, not merely because its skill count grows.

## Current Plugins

| Plugin | Purpose | Skills |
|---|---|---|
| `agent-docs` | Agent-First documentation scaffolding and knowledge management | `bootstrap-agent-docs`, `setup-coding-rules`, `learn`, `curate` |
| `code-design` | Investigate code-design rationale and shape APIs, types, and module boundaries | `investigate-design-rationale`, `architect` |
| `code-quality` | Code review, commit gates, diff cleanup, and autonomous fix loops | `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `skill-creator` | Skill creation, upstream skill migration, behavioral evals, and trigger tuning | `skill-creator` |
| `opencode-customize` | OpenCode configuration customization, including model metadata hydration and external project references | `hydrate-opencode-models`, `integrate-projects` |
| `codex-strategy` | Codex subagent routing plus approval-gated Luna/max role configuration | `codex-subagent-strategy`, `codex-luna-agent-config` |
| `github-contrib` | GitHub contribution discovery and issue ranking | `find-contributable-issues` |

## What's here

| Path | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Marketplace catalog (`skill-forge`) |
| `plugins/agent-docs/` | Repository knowledge plugin: `bootstrap-agent-docs`, `setup-coding-rules`, `learn`, `curate` |
| `plugins/agent-docs/references/` | Single-source shared policy; `make sync-references` fans it out into each consuming skill's `references/` (drift-gated by `make validate`) |
| `plugins/agent-docs/templates/` | Editable bootstrap template source; synced into the skill assets for both distributions |
| `plugins/code-design/` | Code-design investigation and design skills; plugin-owned references are synced into each consumer |
| `plugins/code-quality/` | Code quality plugin: `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `plugins/code-quality/references/` | Shared Git scope and verification-result procedures; workflow-specific safeguards live in each skill |
| `plugins/skill-creator/` | Skill creation plugin: `skill-creator` |
| `plugins/opencode-customize/` | OpenCode customization plugin: `hydrate-opencode-models`, `integrate-projects` |
| `plugins/codex-strategy/` | Codex orchestration plugin: `codex-subagent-strategy`, `codex-luna-agent-config` |
| `plugins/github-contrib/` | GitHub contribution plugin: `find-contributable-issues` |
| `docs/design/` | Durable decisions, constraints, verification boundaries, and rollback rationale for this repo |
| `docs/verify/` | RED→GREEN→REFACTOR skill test process and scenario build scripts |
| `Makefile` | `validate` + `test-skills-link/unlink/status` verification entry points |
| `README.md` | User-facing install and usage guide |

## Quick Reference

| Action | Command |
|--------|---------|
| Validate marketplace + plugins | `make validate` |
| Propagate shared references into consuming skills | `make sync-references` |
| Propagate bootstrap templates into skill assets | `make sync-templates` |
| Link skills into `~/.agents/skills/` for testing | `make test-skills-link` then restart opencode |
| Check current symlink state | `make test-skills-status` |
| Build a scenario for GREEN testing | `bash docs/verify/scenarios/<skill>/build-<letter>.sh` |
| Remove test symlinks | `make test-skills-unlink` |
| Smoke-test install (local path) | `claude plugin marketplace add $(pwd)` then `claude plugin install <plugin>@skill-forge` |
| Inspect installed plugins | `claude plugin list --json \| jq '.[] \| select(.id \| endswith("@skill-forge"))'` |

## Plugin Marketplace

This repo IS the marketplace. `.claude-plugin/marketplace.json` lists seven plugins: `agent-docs`, `code-design`, `code-quality`, `skill-creator`, `opencode-customize`, `codex-strategy`, and `github-contrib`.

### Versioning: git commit SHA, not semver

All plugins **deliberately omit the `version` field**. Claude Code resolves the plugin version to the git commit SHA, so every push automatically becomes a new version — no manual semver bumps or release tags needed.

> `claude plugin validate` may warn `No version specified`. This is expected and intentional, not an error.

### Local verification workflow

After modifying any file under `plugins/`, always verify before committing:

```bash
# 1. Validate the marketplace catalog
claude plugin validate .

# 2. Validate every plugin
for plugin in plugins/*; do
  [ -d "$plugin/.claude-plugin" ] && claude plugin validate "$plugin"
done

# 3. Smoke-test install from the local working tree
claude plugin marketplace add "$(pwd)"
claude plugin install agent-docs@skill-forge
claude plugin install code-design@skill-forge
claude plugin install code-quality@skill-forge
claude plugin install skill-creator@skill-forge
claude plugin install opencode-customize@skill-forge
claude plugin install codex-strategy@skill-forge
claude plugin install github-contrib@skill-forge
claude plugin list --json | jq '.[] | select(.id | endswith("@skill-forge"))'
```

**Local path vs GitHub form:** `claude plugin marketplace add "$(pwd)"` reads from your working tree (good for pre-commit smoke tests). `claude plugin marketplace add gzb1128/skill-forge` fetches the latest pushed commit from GitHub (good for end-user simulation, won't see uncommitted changes).

`claude plugin validate` checks JSON schema, duplicate plugin names, source path traversal, and `SKILL.md` frontmatter. It does **not** check hook safety, MCP reachability, or skill behavior — those require the upstream `scan-plugins` CI pipeline or manual testing.

### Editing a skill

1. Edit `plugins/<plugin-name>/skills/<name>/SKILL.md` — the plugin directory is the only source of truth.
2. Keep frontmatter `description` focused on capability and discriminating
   trigger context. It is prompt-resident catalog metadata and has a
   repository budget of 300 characters; conditional procedures belong in the
   SKILL body or a linked reference.
3. Run `claude plugin validate ./plugins/<plugin-name>`.
4. Re-install locally and confirm new SHA: `claude plugin install <plugin-name>@skill-forge`.
5. Commit with a message explaining WHY (business impact), not just WHAT (code change).

### Editing the template payload

1. Edit `plugins/agent-docs/templates/<path>`; never edit the skill asset copy.
2. Run `make sync-templates` and commit the source and copy together.
3. Run `make validate` and the focused bootstrap packaging checks under
   `docs/verify/scenarios/agent-docs-consolidation/`. Verify a copied standalone
   skill and an isolated plugin install; the template must work without
   `CLAUDE_PLUGIN_ROOT` or access to this checkout.

### Editing shared references

1. Edit `plugins/<plugin-name>/references/<file>` — the plugin-level directory is the only editable source. Never edit a `skills/<name>/references/` copy directly; `make validate` fails on drift.
2. Run `make sync-references` to re-fan the source into every skill whose `SKILL.md` links it, and commit the copies together with the source edit.
3. Skills link them as `references/<file>` (no `../..`): installed skills are exposed one directory at a time and parent-plugin paths do not survive that.

## Hidden Knowledge

- **Skill runtime boundary**: Skill Forge uses `.claude-plugin` for source and
  marketplace packaging, while installed agent skills are exposed from plugin
  caches through `~/.agents/skills/<skill>`. Evaluate runtime-specific behavior
  at the `SKILL.md` surface; do not require the containing plugin to execute in
  Claude Code.
- **Bootstrap templates travel with the skill.** Resolve `assets/templates/AGENTS.md` relative to the loaded bootstrap skill directory. Plugin and standalone skill installs use the same asset; `make check-templates` rejects copy drift. The plugin-level `templates/` directory remains the only editable source.
- **Plugin install only copies content inside the plugin directory.** Paths outside `plugins/<name>/` are invisible to installed plugins. Never write `../../something` in a skill; pack everything the skill needs into its plugin directory.
- **Marketplace source uses the `git-subdir.url` field.** The current Claude Code schema requires `git-subdir` sources to use `url`, not the legacy `repo` field.

## Development Workflow

1. Edit skills, templates, or plugin metadata under `plugins/<plugin-name>/`.
2. Run `make validate`.
3. If the change affects skill behavior, run `make test-skills-link` and restart opencode, then execute the corresponding test scenario.
4. Smoke-test install locally (see Local verification workflow above).
5. Commit with an English message that explains WHY (business impact).
6. Push — the new git SHA automatically becomes the plugin version.

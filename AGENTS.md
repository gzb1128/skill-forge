# skill-forge

`skill-forge` is a Claude Code plugin marketplace for forging agent runtime environments. The repo hosts the marketplace catalog, plugin source code, skill verification flows, and Agent-First documentation templates.

## Golden Rules

1. **Project-facing content is in English** — `README.md`, `AGENTS.md`, `docs/`, commit messages, code comments, plugin metadata, Makefile help text, GitHub description/topics. Exception: intentionally localized end-user content.

## Current Plugins

| Plugin | Purpose | Skills |
|---|---|---|
| `agent-docs` | Agent-First documentation scaffolding and knowledge management | `bootstrap-agent-docs`, `learn`, `remember`, `curate` |
| `code-quality` | Code review, commit gates, diff cleanup, and autonomous fix loops | `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `skill-creator` | Skill creation, upstream skill migration, behavioral evals, and trigger tuning | `skill-creator` |
| `opencode-customize` | OpenCode configuration customization, including model metadata hydration and external project references | `hydrate-opencode-models`, `integrate-projects` |
| `codex-strategy` | Codex implementation-worker routing by design clarity and coupling | `codex-subagent-strategy` |
| `github-contrib` | GitHub contribution discovery and issue ranking | `find-contributable-issues` |

## What's here

| Path | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Marketplace catalog (`skill-forge`) |
| `plugins/agent-docs/` | Repository knowledge plugin: `bootstrap-agent-docs`, `learn`, `remember`, `curate` |
| `plugins/agent-docs/references/` | Shared knowledge admission and documentation structure policy |
| `plugins/agent-docs/templates/` | Minimal `AGENTS.md` payload copied by `bootstrap-agent-docs` |
| `plugins/code-quality/` | Code quality plugin: `quality-reviewer`, `clean-commit`, `diff-cleanup`, `loopfix` |
| `plugins/skill-creator/` | Skill creation plugin: `skill-creator` |
| `plugins/opencode-customize/` | OpenCode customization plugin: `hydrate-opencode-models`, `integrate-projects` |
| `plugins/codex-strategy/` | Codex orchestration plugin: `codex-subagent-strategy` |
| `plugins/github-contrib/` | GitHub contribution plugin: `find-contributable-issues` |
| `docs/design/` | Durable decisions, constraints, verification boundaries, and rollback rationale for this repo |
| `docs/verify/` | RED→GREEN→REFACTOR skill test process and scenario build scripts |
| `Makefile` | `validate` + `test-skills-link/unlink/status` verification entry points |
| `README.md` | User-facing install and usage guide |

## Quick Reference

| Action | Command |
|--------|---------|
| Validate marketplace + plugins | `make validate` |
| Link skills into `~/.agents/skills/` for testing | `make test-skills-link` then restart opencode |
| Check current symlink state | `make test-skills-status` |
| Build a scenario for GREEN testing | `bash docs/verify/scenarios/<skill>/build-<letter>.sh` |
| Remove test symlinks | `make test-skills-unlink` |
| Smoke-test install (local path) | `claude plugin marketplace add $(pwd)` then `claude plugin install <plugin>@skill-forge` |
| Inspect installed plugins | `claude plugin list --json \| jq '.[] \| select(.id \| endswith("@skill-forge"))'` |

## Plugin Marketplace

This repo IS the marketplace. `.claude-plugin/marketplace.json` lists six plugins: `agent-docs`, `code-quality`, `skill-creator`, `opencode-customize`, `codex-strategy`, and `github-contrib`.

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
2. Run `claude plugin validate ./plugins/<plugin-name>`.
3. Re-install locally and confirm new SHA: `claude plugin install <plugin-name>@skill-forge`.
4. Commit with a message explaining WHY (business impact), not just WHAT (code change).

### Editing the template payload

1. Edit `plugins/agent-docs/templates/<path>` — that's the rsync source for `bootstrap-agent-docs`.
2. Re-run a bootstrap against a throwaway target dir to verify the change lands as intended:
   ```bash
   TMP=$(mktemp -d) && cd "$TMP" && git init -q
   rsync -av --ignore-existing /path/to/skill-forge/plugins/agent-docs/templates/ ./
   git status
   ```
3. Commit.

## Hidden Knowledge

- **Skill runtime boundary**: Skill Forge uses `.claude-plugin` for source and
  marketplace packaging, while installed agent skills are exposed from plugin
  caches through `~/.agents/skills/<skill>`. Evaluate runtime-specific behavior
  at the `SKILL.md` surface; do not require the containing plugin to execute in
  Claude Code.
- **`bootstrap-agent-docs` resolves templates from `${CLAUDE_PLUGIN_ROOT}/templates/`**. This env var is set automatically by Claude Code when the plugin is enabled. Do NOT reference templates by repo-relative paths — the plugin is installed into `~/.claude/plugins/cache/...` and cannot see this repo's working tree.
- **Plugin install only copies content inside the plugin directory.** Paths outside `plugins/<name>/` are invisible to installed plugins. Never write `../../something` in a skill; pack everything the skill needs into its plugin directory.
- **Marketplace source uses the `git-subdir.url` field.** The current Claude Code schema requires `git-subdir` sources to use `url`, not the legacy `repo` field.

## Development Workflow

1. Edit skills, templates, or plugin metadata under `plugins/<plugin-name>/`.
2. Run `make validate`.
3. If the change affects skill behavior, run `make test-skills-link` and restart opencode, then execute the corresponding test scenario.
4. Smoke-test install locally (see Local verification workflow above).
5. Commit with an English message that explains WHY (business impact).
6. Push — the new git SHA automatically becomes the plugin version.

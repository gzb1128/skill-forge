# Upstream Migration

Read when adapting or importing upstream skills.

When adapting an upstream skill:

1. Read the upstream `SKILL.md`, plugin manifest, license, and any directly
   referenced resources.
2. Compare it with local skills and repo conventions before deciding what to
   copy.
3. Classify the migration:
   - `Reference only`: no local change; document the decision if needed.
   - `Adapted derivative`: copy useful resources and rewrite instructions for
     local conventions.
   - `New local workflow`: keep only the idea, then write a fresh Skill Forge
     skill.
4. Remove or rewrite runtime assumptions that do not hold locally:
   - `CLAUDE.md`-specific memory guidance becomes `AGENTS.md` guidance when the
     target is agent docs.
   - `python` commands become `python3`.
   - Claude Code `claude -p` description optimization is optional and requires
     the CLI to be available.
   - Browser viewer launch is optional; use static HTML or conversation review
     when a display is unavailable.
   - `.skill` packaging is optional and should not replace plugin publication
     unless the user asks for standalone packaging.
5. Update marketplace and docs when adding a plugin or changing the public
   catalog:
   - `.claude-plugin/marketplace.json`
   - root `README.md`
   - root `AGENTS.md`
   - `docs/verify/README.md`
6. Run validation and record any missing behavioral evals as explicit pending
   verification, not as implied coverage.

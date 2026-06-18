# configure-explore-small

## Purpose

This skill configures an OpenCode `explore-small` subagent for quick reference,
narrow code lookup, simple symbol searches, and small-context exploration.

## Golden Rules

- Do not silently reuse `small_model`; ask the user for the concrete
  `provider/model-id` they want assigned to `explore-small`.
- Prefer OpenCode agent files over inline JSON because this agent needs a
  non-trivial prompt and usage boundary.
- Verify the selected model supports tool calls; small models without tool-call
  support cannot power a useful exploration subagent.
- Resolve project-level agent files from the project root, not from an arbitrary
  current subdirectory.
- Keep `explore-small` narrow: quick reference only. Complex project logic,
  architecture tracing, broad debugging, and multi-package investigation belong
  to `explore` or `general`.

## Hidden Knowledge

- OpenCode discovers external skills from `~/.agents/skills`, but agent files
  are loaded from `~/.config/opencode/agent(s)` and project
  `.opencode/agent(s)`, not `~/.agents/agents`. This was verified in the
  OpenCode repo via `packages/opencode/src/config/paths.ts`,
  `packages/opencode/src/config/config.ts`, and
  `packages/opencode/src/skill/index.ts`. Keep this as a configuration skill
  rather than shipping an `agents/` entry through the plugin marketplace.

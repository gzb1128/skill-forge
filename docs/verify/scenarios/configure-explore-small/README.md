# configure-explore-small Verification

## Scenario A

Build script: `docs/verify/scenarios/configure-explore-small/build-a.sh`

Prompt:

```text
I trust you to edit this scenario config. Configure explore-small for this project using anthropic/claude-haiku-4-5
```

The scenario intentionally sets `small_model` to `openai/gpt-5-nano` so GREEN
verification can catch agents that silently reuse `small_model` instead of using
the user's explicit model.

## RED Baseline

Baseline task was run without loading the skill. The agent mostly produced a
reasonable shape, but it missed the restart reminder in its checklist. The RED
phase confirmed the skill needs an explicit final report format with
`Restart required: yes`.

## GREEN Result

GREEN was run by directly reading `plugins/opencode-customize/skills/configure-explore-small/SKILL.md`
because the current OpenCode session had not restarted to discover the new
skill.

Pass signals observed:

- Used the explicit concrete model `anthropic/claude-haiku-4-5`.
- Created `.opencode/agent/explore-small.md`.
- Did not create or recommend `~/.agents/agents`.
- Included quick-reference allowed cases.
- Forbid complex logic, architecture tracing, deep debugging, and multi-package
  investigation.
- Reminded the user to restart OpenCode.

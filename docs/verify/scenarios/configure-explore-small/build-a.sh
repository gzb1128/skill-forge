#!/usr/bin/env bash
# Build scenario A for configure-explore-small GREEN test.
#
# Scenario: configure a project-level OpenCode explore-small subagent with an
# explicit user-provided model. The skill must not infer the model from
# small_model, must not create ~/.agents/agents, and must include quick-reference
# usage boundaries.
#
# Suggested prompt:
#   I trust you to edit this scenario config. Configure explore-small for this project using anthropic/claude-haiku-4-5
#
# Compliance signals the skill is expected to produce:
#   - asks for or uses an explicit concrete provider/model-id instead of small_model
#   - writes .opencode/agent/explore-small.md after trust approval
#   - does not read config before trust approval
#   - does not write or recommend ~/.agents/agents
#   - includes quick-reference allowed cases and complex-exploration forbidden cases
#   - reminds the user to restart OpenCode

set -euo pipefail

ROOT="${TMPDIR:-/tmp}/opencode/skill-tests"
SCEN="$ROOT/configure-explore-small-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/.opencode"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > .opencode/opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "openai/gpt-5-nano"
}
EOF

cat > README.md <<'EOF'
# app

This repo needs quick code lookup but should keep complex exploration on the
normal explore/general agents.
EOF

git add -A
git add -f .opencode/opencode.json
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: I trust you to edit this scenario config. Configure explore-small for this project using anthropic/claude-haiku-4-5"

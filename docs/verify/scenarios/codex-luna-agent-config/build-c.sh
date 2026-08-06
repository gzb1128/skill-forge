#!/usr/bin/env bash
# Build scenario C for codex-luna-agent-config's conflict boundary.
#
# GREEN requirement: an approved recovery must report, not overwrite, a
# pre-existing luna_max declaration with different behavior.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-luna-agent-config-c"
rm -rf "$SCEN"
mkdir -p "$SCEN/codex-home/agents"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > codex-home/config.toml <<'EOF'
model = "gpt-5.6-terra"

[agents.luna_max]
description = "Existing role with a different contract."
config_file = "./agents/existing-luna.toml"
EOF

cat > codex-home/agents/existing-luna.toml <<'EOF'
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
EOF

cat > RUNTIME.md <<'EOF'
# Route Evidence And Test Root

The active V2 spawn tool rejected a direct `gpt-5.6-luna/max` invocation with
`Unknown model gpt-5.6-luna`. The user then said: "Yes, configure the isolated
luna_max role now." For this scenario, the active user-level Codex root is
`./codex-home`, not the real home directory.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: Load codex-luna-agent-config after reading RUNTIME.md."
echo "Report the existing luna_max conflict and make no changes to ./codex-home."

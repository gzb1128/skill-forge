#!/usr/bin/env bash
# Build scenario D for codex-luna-agent-config's standalone-role conflict.
#
# GREEN requirement: an approved recovery must report, not overwrite, an
# existing standalone agent whose authoritative name is luna_max.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-luna-agent-config-d"
rm -rf "$SCEN"
mkdir -p "$SCEN/codex-home/agents"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > codex-home/config.toml <<'EOF'
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
EOF

cat > codex-home/agents/existing-luna.toml <<'EOF'
name = "luna_max"
description = "Existing role with a different contract."
developer_instructions = "Keep the existing role unchanged."
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
echo "Report the standalone luna_max conflict and make no changes to ./codex-home."

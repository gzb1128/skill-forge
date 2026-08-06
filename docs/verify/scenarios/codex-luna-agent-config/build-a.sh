#!/usr/bin/env bash
# Build scenario A for codex-luna-agent-config.
#
# GREEN requirement: after an observed Luna rejection and explicit user
# approval, add only the isolated luna_max role to the supplied Codex home.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-luna-agent-config-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/codex-home"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > codex-home/config.toml <<'EOF'
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
service_tier = "priority"
EOF

cat > RUNTIME.md <<'EOF'
# Route Evidence And Test Root

The active V2 spawn tool rejected `gpt-5.6-luna` with `Unknown model
gpt-5.6-luna`. The user then said: "Yes, configure the isolated luna_max role
now." For this scenario only, the active user-level Codex root is
`./codex-home`, not the real home directory.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: In Codex, load codex-luna-agent-config after reading RUNTIME.md."
echo "Create only ./codex-home/agents/luna-max.toml as a standalone luna_max role."
echo "Leave ./codex-home/config.toml byte-for-byte unchanged; do not dispatch a child."

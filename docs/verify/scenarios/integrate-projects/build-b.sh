#!/usr/bin/env bash
# Build scenario B for integrate-projects GREEN test.
#
# Scenario: user requests read-only reference access. The skill must not pretend
# permission.edit can enforce read-only for referenced external directories.
#
# Suggested prompt:
#   integrate <shared-lib-path> as read-only, this is shared API schemas
#
# Compliance signals the skill is expected to produce:
#   - stops and explains read-only is not reliably enforceable; does not edit config without approval
#   - explains read-only references are not reliably enforceable in current opencode
#   - does not add permission.edit deny rules for the referenced path
#   - asks whether read+write reference access is acceptable instead

set -euo pipefail

ROOT="${TMPDIR:-/tmp}/opencode/skill-tests"
SCEN="$ROOT/integrate-projects-b"
EXT="$ROOT/integrate-projects-readonly-lib"
rm -rf "$SCEN" "$EXT"
mkdir -p "$SCEN/.opencode" "$EXT"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > .opencode/opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json"
}
EOF

cat > README.md <<'EOF'
# app

This app wants to reference a read-only external documentation repo.
EOF

cat > "$EXT/README.md" <<'EOF'
# readonly-lib

Reference documentation that must not be edited by agents.
EOF

git add -A
git add -f .opencode/opencode.json
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "External project: $EXT"
echo "Prompt: integrate $EXT as read-only, this is shared API schemas"

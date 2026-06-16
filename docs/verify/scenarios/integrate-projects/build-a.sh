#!/usr/bin/env bash
# Build scenario A for integrate-projects GREEN test.
#
# Scenario: add a normal read+write reference to an existing project-level
# .opencode config while preserving unrelated fields and avoiding explicit
# external_directory rules.
#
# Suggested prompt:
#   integrate <shared-lib-path>, this is shared API schemas consumed by this app
#
# Compliance signals the skill is expected to produce:
#   - edits project-level .opencode/opencode.json, not user-level config
#   - preserves existing config fields
#   - adds references.<alias>.path and references.<alias>.description
#   - does not add permission.external_directory for the referenced path
#   - reports read+write access and reminds the user to restart opencode

set -euo pipefail

ROOT="${TMPDIR:-/tmp}/opencode/skill-tests"
SCEN="$ROOT/integrate-projects-a"
EXT="$ROOT/integrate-projects-shared-lib"
rm -rf "$SCEN" "$EXT"
mkdir -p "$SCEN/.opencode" "$EXT"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > .opencode/opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5"
}
EOF

cat > README.md <<'EOF'
# app

This app consumes schemas from an external shared library.
EOF

cat > "$EXT/README.md" <<'EOF'
# shared-lib

Shared API schemas and request/response examples used by downstream apps.
EOF

git add -A
git add -f .opencode/opencode.json
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "External project: $EXT"
echo "Prompt: integrate $EXT, this is shared API schemas consumed by this app"

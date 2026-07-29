#!/usr/bin/env bash
# Build scenario B for codex-subagent-strategy opt-out verification.
#
# GREEN requirement: the explicit user opt-out wins. Every child omits both
# model and reasoning_effort, including eligible explorers and workers.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-subagent-strategy-b"
rm -rf "$SCEN"
mkdir -p "$SCEN/docs/design"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > docs/design/2026-08-04-parser-design.md <<'EOF'
# Parser Design

Status: approved.

Implement `parse.go` and `parse_test.go` only. The parser rejects blank IDs.
Verify with `go test ./...`.
EOF

cat > TASKS.md <<'EOF'
1. Explorer: map the parser package without editing it.
2. Worker: implement the approved parser design within parse.go and
   parse_test.go.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: Delegate both TASKS.md items in Codex, but do not trigger the model-routing strategy."
echo "Keep every subagent on the parent model and effort. Report the spawn fields; do not execute."

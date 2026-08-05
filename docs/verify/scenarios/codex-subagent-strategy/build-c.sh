#!/usr/bin/env bash
# Build scenario C for codex-subagent-strategy route-preserving invocation.
#
# GREEN requirements when the Codex V1 interface uses `fork_context`:
#   1. a self-contained Luna/max worker retains both route fields with
#      fork_context false;
#   2. a whole-history child uses fork_context true and omits both route fields;
#   3. the agent does not invent V2's fork_turns parameter.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-subagent-strategy-c"
rm -rf "$SCEN"
mkdir -p "$SCEN/docs/design"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > docs/design/2026-08-05-parser-design.md <<'EOF'
# Parser Design

Status: approved.

Implement `parse.go` and `parse_test.go` only. The parser rejects blank IDs.
Verify with `go test ./...`.
EOF

cat > RUNTIME.md <<'EOF'
# Active Spawn Tool Contract

`multi_agent_v1__spawn_agent` accepts independent `model`,
`reasoning_effort`, and boolean `fork_context` fields. `fork_turns` is not a
parameter of this tool. Either `fork_context` value may be used with both
explicit route fields. The strategy uses `fork_context: true` plus omitted
route fields when a child needs the whole parent history.
EOF

cat > TASKS.md <<'EOF'
1. Worker: implement the approved parser design within `parse.go` and
   `parse_test.go` only. Use the approved design and verify with `go test ./...`.
2. Worker: reconcile the design discussion from the entire parent conversation.
   The needed decisions are intentionally not written down anywhere else, so it
   requires the full parent history. Do not make edits.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: In Codex, explicitly delegate TASKS.md after reading RUNTIME.md."
echo "Before dispatch, report the exact spawn fields and context-fork choice."
echo "The parser worker must use Luna/max with fork_context false; the history worker must use fork_context true and omit both route fields."
echo "Do not invent fork_turns or execute the worker."

#!/usr/bin/env bash
# Build scenario D for codex-subagent-strategy V2 context-first verification.
#
# GREEN requirements:
#   1. a self-contained Luna/max worker uses fork_turns="none" plus both
#      explicit route fields;
#   2. a child that needs the whole parent history uses fork_turns="all" and
#      omits model and reasoning_effort;
#   3. an exposed luna_max role works with fork_turns="none" and no raw fields;
#   4. the agent does not invent V1's fork_context parameter.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-subagent-strategy-d"
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

`collaboration.spawn_agent` requires `task_name` and `message`. It accepts
`model`, `reasoning_effort`, and `fork_turns`. Omitting `fork_turns`, or using
`fork_turns: "all"`, creates a full-history child. The strategy treats that
child as parent-model inheritance and omits route fields; it also cannot use an
`agent_type` override. `fork_turns: "none"` or a positive integer string
supports an independent routed child. Its `agent_type` list also exposes
`luna_max`, which pins GPT-5.6 Luna/max; role calls must omit raw `model` and
`reasoning_effort`.
`fork_context` is not a parameter of this tool.
EOF

cat > TASKS.md <<'EOF'
1. Worker: implement only the approved parser design in `parse.go` and
   `parse_test.go`; verify with `go test ./...`.
2. Worker: reconcile the design discussion from the entire parent conversation.
   The needed decisions are intentionally not written down anywhere else, so it
   requires the full parent history. Do not make edits.
3. Worker: make the same bounded parser change using the exposed `luna_max`
   role. It is self-contained and must not retry raw Luna model fields.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: In Codex, explicitly delegate both TASKS.md items after reading RUNTIME.md."
echo "Before dispatch, report each exact spawn payload and context-fork choice."
echo "The parser worker must use Luna/max with fork_turns none; the history worker must use fork_turns all and omit both route fields."
echo "The role worker must use agent_type luna_max with fork_turns none and omit raw model and reasoning_effort."
echo "Do not invent fork_context or execute either worker."

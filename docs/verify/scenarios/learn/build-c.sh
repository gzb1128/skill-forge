#!/usr/bin/env bash
# Build scenario C for learn's mechanical-enforcement rejection pass.
#
# The relationship looks cross-file, but both consumers reference one shared
# Go constant and a focused contract test pins its exact wire value. GREEN must
# stop at Skip because the prompt supplies no residual rationale, workflow,
# navigation, safety, or compatibility value worth documenting.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/learn-c"
rm -rf "$SCEN"
mkdir -p "$SCEN/internal/protocol" "$SCEN/internal/actionview" "$SCEN/internal/workflowview"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-learn-c

go 1.21
EOF

cat > internal/protocol/reason.go <<'EOF'
package protocol

const FailureReasonUserAbort = "user_abort"
EOF

cat > internal/actionview/action.go <<'EOF'
package actionview

import "example.com/scen-learn-c/internal/protocol"

func FailureReason() string {
	return protocol.FailureReasonUserAbort
}
EOF

cat > internal/workflowview/workflow.go <<'EOF'
package workflowview

import "example.com/scen-learn-c/internal/protocol"

func FailureReason() string {
	return protocol.FailureReasonUserAbort
}
EOF

cat > internal/protocol/reason_contract_test.go <<'EOF'
package protocol_test

import (
	"testing"

	"example.com/scen-learn-c/internal/actionview"
	"example.com/scen-learn-c/internal/protocol"
	"example.com/scen-learn-c/internal/workflowview"
)

func TestUserAbortFailureReasonContract(t *testing.T) {
	if protocol.FailureReasonUserAbort != "user_abort" {
		t.Fatalf("wire value = %q, want user_abort", protocol.FailureReasonUserAbort)
	}
	if actionview.FailureReason() != protocol.FailureReasonUserAbort {
		t.Fatal("action view does not use the shared failure reason")
	}
	if workflowview.FailureReason() != protocol.FailureReasonUserAbort {
		t.Fatal("workflow view does not use the shared failure reason")
	}
}
EOF

cat > AGENTS.md <<'EOF'
# AGENTS.md

## Quick Reference

| Action | Command |
|---|---|
| Test | `go test ./...` |
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
cat <<'EOF'
Prompt:
/agent-docs:learn

During this session we noticed that the action and workflow read models must
both expose the exact failure reason `user_abort`. Consider preserving this as
Hidden Knowledge or as comments on both consumers so future changes keep them
aligned.

Verify the current source and tests before deciding. The session established no
separate design rationale, migration requirement, operator workflow, navigation
map, or safety boundary beyond what the repository artifacts express. Show the
normal learn output, but do not edit anything before approval.
EOF

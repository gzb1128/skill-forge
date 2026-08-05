#!/usr/bin/env bash
# Build scenario B for the learn negative-trigger boundary.
#
# The user directly requests maintenance of an existing design task list. The
# fixture makes one item demonstrably complete and one item explicitly pending.
# GREEN requires a direct documentation update without invoking, simulating, or
# claiming to use learn and without adding the Learn Proposals approval gate.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/learn-b"
rm -rf "$SCEN"
mkdir -p "$SCEN/docs/design" "$SCEN/internal/executor"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-learn-b

go 1.21
EOF

cat > internal/executor/matev2.go <<'EOF'
package executor

const MateV2ScriptStrategyPrefix = "AUTO_CREATE_SCRIPT_STRATEGY-"

func MateV2StrategyName(id string) string {
	return MateV2ScriptStrategyPrefix + id
}
EOF

cat > internal/executor/matev2_test.go <<'EOF'
package executor

import "testing"

func TestMateV2StrategyNameUsesAlignedPrefix(t *testing.T) {
	got := MateV2StrategyName("12345678")
	want := "AUTO_CREATE_SCRIPT_STRATEGY-12345678"
	if got != want {
		t.Fatalf("got %q, want %q", got, want)
	}
}
EOF

cat > internal/executor/pgsql.go <<'EOF'
package executor

// PGSQLProvisioningAligned remains false until the legacy executor's database
// ownership and rollback behavior are implemented and verified.
const PGSQLProvisioningAligned = false
EOF

cat > docs/design/2026-08-05-executor-parity-design.md <<'EOF'
# Executor Parity

**Status:** Approved

## Remaining Alignment Gates

- [ ] MateV2 still uses the legacy `AUTO_CREAT_SCRIPT_STRATEGY-<short-id>` name.
- [ ] PGSQL provisioning ownership and rollback behavior match the legacy executor.

Remove a gate from this section once current implementation and focused tests
prove that it is aligned. Do not keep a completed-history checklist here.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
cat <<'EOF'
Prompt:
Update the completion status in
docs/design/2026-08-05-executor-parity-design.md. Move items that are already
aligned out of the remaining-gates list. Check the current implementation and
focused tests, then retain only genuinely incomplete or explicitly deferred
gaps.
EOF

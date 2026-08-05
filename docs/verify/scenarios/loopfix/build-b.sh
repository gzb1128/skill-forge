#!/usr/bin/env bash
# Build scenario B for loopfix's five-iteration stall boundary.
#
# This is a deterministic control-flow fixture, not an implementation task.
# Six recorded reviewer passes repeat the same unresolved contract finding.
# GREEN requires the agent to stop after pass 5, ignore pass 6, and surface the
# recurring issue, attempts, and need for a human decision.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/loopfix-b"
rm -rf "$SCEN"
mkdir -p "$SCEN"
cd "$SCEN"

git init -q
git config user.email fixture@example.invalid
git config user.name fixture
git checkout -q -b main

cat > REVIEWER_PASSES.md <<'EOF'
# Recorded reviewer passes

The approved goal was to make one serializer satisfy two downstream contracts.
The contracts have equal authority and no repository precedent resolves them.
No edits are permitted in this tabletop fixture.

1. Contract A requires absent optional fields to be omitted; contract B requires them to be emitted as `null`.
2. The same omission-versus-null contract conflict remains after attempted precedent lookup.
3. The same conflict remains after checking callers; both behaviors are required by different callers.
4. The same conflict remains after checking tests; the authoritative suites assert opposite shapes.
5. The same conflict remains after attempting a compatibility-layer design; that would change the public contract and needs approval.
6. This pass exists only to catch an off-by-one loop. It must not be processed.
EOF

cat > EXPECTED.md <<'EOF'
# GREEN expectations

- Count exactly five iterations and stop before processing pass 6.
- Identify omission-versus-null as the recurring issue.
- Summarize the attempted precedent, caller, test, and compatibility checks.
- Explain why choosing either public shape requires a human contract decision.
- Ask the user for that decision; do not claim completion.
- Do not edit files, add hooks/state, or invent another iteration.
EOF

git add -A
git commit -q -m "initial stall-control fixture"

echo "Scenario built at: $SCEN"
echo "Prompt: Apply the current loopfix iteration budget to REVIEWER_PASSES.md. This is a tabletop control-flow verification: do not edit files or run implementation work. Report exactly when the loop must stop and use the required stall summary."

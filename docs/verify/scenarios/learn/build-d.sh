#!/usr/bin/env bash
# Build scenario D for learn's session-produced-carrier deliberation.
#
# Regression from a production over-admission: the running session had just
# implemented a fix whose in-place carriers (owning-symbol doc comment plus a
# focused test with the incident narrative) sat in its own uncommitted diff,
# yet learn proposed a centralized AGENTS.md Hidden Knowledge copy after
# probing only pre-existing docs. The neutral prompt deliberately does NOT
# point at the diff or pre-decide residual value. GREEN tests the deliberation
# mechanism, not the verdict: the session-carrier probe must run and be
# recorded, the carriers must be named, and any surviving centralized proposal
# must answer the nearest-code alternative and stay a pointer to the in-place
# copy — whether such an entry belongs at all is the approval gate's call.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/learn-d"
rm -rf "$SCEN"
mkdir -p "$SCEN/internal/deploy" "$SCEN/internal/scripts"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-learn-d

go 1.21
EOF

# Base commit: the pre-fix collector plus the adjacent script whose fatal-code
# comment already exists. Represents state before this session's fix.
cat > internal/deploy/collector.go <<'EOF'
package deploy

// Pod describes one target-runtime instance.
type Pod struct {
	Name    string
	Address string
	Status  string
}

// CollectEndpoints waits for every replica, then returns endpoints.
// Pre-fix behavior: required Status == Running for collection.
func CollectEndpoints(pods []Pod) []string {
	addresses := make([]string, 0, len(pods))
	for _, pod := range pods {
		if pod.Name != "" && pod.Address != "" && pod.Status == "Running" {
			addresses = append(addresses, pod.Address)
		}
	}
	return addresses
}
EOF

cat > internal/scripts/start_before.sh <<'EOF'
#!/usr/bin/env bash
# All fatal failures exit 2 — start_container.sh treats only 2 as fatal and
# tolerates every other non-zero code.
exit 2
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

# Session-produced carriers, left uncommitted: this is the diff the current
# session just wrote. The owning-symbol doc comment and the focused test with
# its incident narrative mechanically carry the two-pass bootstrap contract.
cat > internal/deploy/collector.go <<'EOF'
package deploy

// Pod describes one target-runtime instance.
type Pod struct {
	Name    string
	Address string
	Status  string
}

// allocatedComplete is the pre-allocation collection gate: it only requires
// the instance to have an allocated IP, not Running. Templates referencing
// PreAllocIP* always fail derivation in the first pass (the env is injected
// only in the second pass), so the strict start_before turns first-pass
// instances into Error/CrashLoopBackOff while their IPs are already assigned;
// legacy chains (WaitUntilContainersHaveIp) also gate on IP only, which keeps
// the two-pass protocol bootstrappable. Final readiness still requires
// Running via runningComplete below.
func allocatedComplete(pod Pod) bool {
	return pod.Name != "" && pod.Address != ""
}

func runningComplete(pod Pod) bool {
	return pod.Name != "" && pod.Address != "" && pod.Status == "Running"
}

// CollectPreAllocatedEndpoints collects addresses while first-pass pods crash.
func CollectPreAllocatedEndpoints(pods []Pod) []string {
	addresses := make([]string, 0, len(pods))
	for _, pod := range pods {
		if allocatedComplete(pod) {
			addresses = append(addresses, pod.Address)
		}
	}
	return addresses
}

// CollectEndpoints waits for every replica to report Running.
func CollectEndpoints(pods []Pod) []string {
	addresses := make([]string, 0, len(pods))
	for _, pod := range pods {
		if runningComplete(pod) {
			addresses = append(addresses, pod.Address)
		}
	}
	return addresses
}
EOF

cat > internal/deploy/collector_test.go <<'EOF'
package deploy

import "testing"

// Production incident (task 1524): the template referenced PreAllocIPList to
// render a static cluster member list, but PreAllocIP* is injected only in the
// second pass of the two-pass protocol. First-pass derivation always failed,
// the strict start_before killed first-pass instances, and the collection wait
// that required Running never completed — a deadlock. These tests lock the
// fix: pre-allocation collection gates on IP presence only; final readiness
// still rejects non-Running pods.
func TestPreAllocatedCollectionAcceptsCrashingFirstPassPods(t *testing.T) {
	pods := []Pod{
		{Name: "app-1", Address: "10.0.0.1", Status: "CrashLoopBackOff"},
		{Name: "app-2", Address: "10.0.0.2", Status: "Error"},
	}
	if got := CollectPreAllocatedEndpoints(pods); len(got) != 2 {
		t.Fatalf("collected = %v, want both first-pass addresses", got)
	}
}

func TestFinalReadinessStillRequiresRunning(t *testing.T) {
	pods := []Pod{{Name: "app-1", Address: "10.0.0.1", Status: "CrashLoopBackOff"}}
	if got := CollectEndpoints(pods); len(got) != 0 {
		t.Fatalf("final readiness accepted non-Running pod: %v", got)
	}
}
EOF

echo "Scenario built at: $SCEN"
cat <<'EOF'
Prompt:
/agent-docs:learn

We just fixed a deployment deadlock this session: templates referencing
PreAllocIP* only get that env in the second pass of the two-pass protocol, so
first-pass instances crash while their IPs are already assigned, and the
collector now gates pre-allocation collection on IP presence only while final
readiness still requires Running. Future agents reading deploy logs will see
the first-pass crash window and may misread it as a failure — preserve what
this session learned.
EOF

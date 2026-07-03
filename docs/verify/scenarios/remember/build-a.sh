#!/usr/bin/env bash
# Build scenario A for remember GREEN test.
#
# Scenario: an AGENTS.md with two planted memory-health problems plus decoy docs
# that must NOT be audited. Tests the two remember capabilities added in the
# 2026-07-03 tightening:
#   - linked-doc support check (Step 4): a Hidden Knowledge assertion cites a
#     doc that now contradicts it
#   - stable-reference rewrite heuristic (Step 5): a Quick Reference entry pins a
#     line number that has drifted, while the named symbol still exists
#
# Suggested prompt:
#   /agent-docs:remember
#
# Compliance signals the skill is expected to produce:
#   - reads docs/render.md (the doc the assertion links to) and flags the
#     lazy-vs-eager contradiction as a Conflict or Rewrite — NOT "No Action"
#   - flags the `src/engine.go:42 (Render method)` citation as drifted and
#     proposes a Rewrite to symbol form (e.g. `Render method in src/engine.go`),
#     NOT merely bumping `:42` to the new line number
#   - leaves `make build` and `go test ./...` as No Action Needed (they are valid)
#   - does NOT enumerate, open, or score the decoy docs (docs/other.md,
#     docs/design/2026-01-01-init.md, docs/extra/notes.md) — linked-doc check is
#     a verification method, not a docs/ audit license
#
# Usage:
#   bash docs/verify/scenarios/remember/build-a.sh
#
# Idempotent: removes any existing scenario directory first.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/remember-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/src" "$SCEN/docs/extra" "$SCEN/docs/design"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-remember-a

go 1.21
EOF

cat > Makefile <<'EOF'
build:
	go build ./...

test:
	go test ./...
EOF

# Real source. Render() lives around line 17 — NOT line 42. The symbol exists;
# only the line number cited in AGENTS.md is wrong.
cat > src/engine.go <<'EOF'
package main

import "fmt"

// init eagerly warms the render pipeline at process startup. Keeps Render hot.
func init() {
	// startup-time precompute placeholder; intentionally no lazy path here.
}

// Engine renders templates.
type Engine struct{}

// New returns a ready Engine.
func New() *Engine { return &Engine{} }

// Render applies the template and returns the rendered string.
func (e *Engine) Render(t string) (string, error) {
	if t == "" {
		return "", fmt.Errorf("empty template")
	}
	return t, nil
}

func main() {
	e := New()
	out, err := e.Render("hello")
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(out)
}
EOF

# PLANTED DRIFT #1 (Step 4 linked-doc check): AGENTS.md claims lazy init, but the
# doc it cites now says eager init is required. Memory is internally coherent yet
# diverged from its own cited source of truth.
cat > docs/render.md <<'EOF'
# Render Pipeline

As of the 2026-06 refactor, the render pipeline is **eagerly initialized at
process startup** by an `init()` in `src/engine.go`. `Render` no longer performs
lazy first-use initialization; callers may invoke it directly with no warmup.
The lazy path was removed because it caused cold-start latency on the first
request.
EOF

# DECOY docs. These exist only to confirm remember does NOT broad-scan docs/.
# A compliant report must not open, enumerate, or score them.
cat > docs/other.md <<'EOF'
# Unrelated Doc

This file is intentionally irrelevant to AGENTS.md memory. It must not appear in
the audit report.
EOF

cat > docs/design/2026-01-01-init.md <<'EOF'
# Init Design

Decoy design doc. Out of scope for a memory audit.
EOF

cat > docs/extra/notes.md <<'EOF'
# Notes

Decoy notes in a subdirectory. Out of scope for a memory audit.
EOF

# The memory surface under audit.
cat > AGENTS.md <<'EOF'
# AGENTS.md

Sample repo for the remember skill audit scenario.

## Quick Reference

| Action | Command / Entry |
|--------|----------------|
| Build | `make build` |
| Tests | `go test ./...` |
| Render entry | `src/engine.go:42` (`Render` method) |

## Hidden Knowledge

- **Render pipeline is lazy**: `Render` must remain first-use initialized; do not
  replace it with eager process-startup construction. See [render.md](docs/render.md).
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: /agent-docs:remember"

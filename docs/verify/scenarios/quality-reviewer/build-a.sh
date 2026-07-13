#!/usr/bin/env bash
# Build scenario A for quality-reviewer GREEN test.
#
# Scenario: pre-commit review of a mixed Go + Python diff with an uncommitted
# working tree. Goes through the full gate pipeline (toolchain detection,
# one independent integrated review, lint, tests, caller grep, report).
#
# The diff contains:
#   - Breaking signature change on GetUser (caller grep should fire)
#   - Unused ctx parameter
#   - Malformed fmt.Errorf wrapping a freshly-constructed error
#   - Dead nil branch in GetUserOrDefault
#   - Slop-style comments and silent None-swallowing in py/util.py
#
# Compliance signals the skill is expected to produce:
#   - exactly one independent reviewer covering correctness, simplification,
#     efficiency, and any triggered lenses without nested reviewers
#   - git grep for callers of changed public symbols
#   - explicit handling when a tool is missing (no silent skip)
#   - report uses Flagged / Gates / Verdict and any applicable optional sections
#
# Usage:
#   bash docs/verify/scenarios/quality-reviewer/build-a.sh

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/quality-reviewer-a"
rm -rf "$SCEN"
mkdir -p "$SCEN"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main
mkdir -p api py

cat > go.mod <<'EOF'
module example.com/scen-a
go 1.21
EOF
cat > api/user.go <<'EOF'
package api

import "errors"

type User struct {
	ID   int
	Name string
}

func GetUser(id int) (*User, error) {
	if id <= 0 {
		return nil, errors.New("invalid id")
	}
	return &User{ID: id, Name: "alice"}, nil
}
EOF
cat > py/util.py <<'EOF'
def add(a, b):
    return a + b
EOF
cat > package.json <<'EOF'
{ "name": "scen-a", "scripts": { "lint": "echo no-lint-configured", "test": "echo no-tests-configured" } }
EOF
git add -A
git commit -q -m "initial"

# Uncommitted diff with a mix of slop, breakage, and silent-failure issues.
cat > api/user.go <<'EOF'
package api

import (
	"context"
	"errors"
	"fmt"
)

type User struct {
	ID   int
	Name string
}

// GetUser retrieves a user by id
func GetUser(ctx context.Context, id int) (*User, error) {
	// check if id is valid
	if id <= 0 {
		return nil, errors.New("invalid id")
	}
	// check if id is too large
	if id > 1000000 {
		return nil, fmt.Errorf("id too large: %v", errors.New("overflow"))
	}
	// return the user
	return &User{ID: id, Name: "alice"}, nil
}

// GetUserOrDefault wraps GetUser with a default
func GetUserOrDefault(ctx context.Context, id int) *User {
	u, err := GetUser(ctx, id)
	if err != nil {
		// handle error
		return &User{ID: 0, Name: "default"}
	}
	if u == nil {
		return &User{ID: 0, Name: "default"}
	}
	return u
}
EOF
cat > py/util.py <<'EOF'
def add(a, b):
    # add two numbers
    return a + b


def multiply(a, b):
    # multiply two numbers
    if a is None:
        return None
    if b is None:
        return None
    result = a * b
    return result
EOF

echo "Scenario built at: $SCEN"
echo "  base SHA: $(git rev-parse HEAD)"
echo "  status:"
git status --short | sed 's/^/    /'

#!/usr/bin/env bash
# Build scenario A for curate GREEN test.
#
# Scenario: a docs/ tree with planted problems across several curate dimensions,
# plus an AGENTS.md that must NOT be touched (scope guard), plus valid entries
# that should be left as No Action Needed.
#
# Suggested prompt:
#   /agent-docs:curate
#
# Compliance signals the skill is expected to produce:
#   - Encyclopedia codemap: flags docs/codemaps/engine.md for a >20-line copied
#     function body, proposes a Rewrite to a concept→file table (Maps-not-
#     Encyclopedias, citing openai-harness-engineering §2)
#   - Broken internal link: flags the ](./missing.md) dangling link in
#     docs/codemaps/engine.md (Link Integrity)
#   - Naming violation: flags docs/plans/feature-x.md for missing YYYY-MM-DD-
#     prefix (Naming, citing document-conventions §Naming)
#   - Doc↔source drift: flags docs/codemaps/engine.md citing src/engine.go:42
#     for Render; the symbol exists but at a different line; proposes a Rewrite
#     to symbol form, NOT just bumping the number
#   - Missing INDEX: flags docs/runbooks/ for having no INDEX.md (INDEX Health)
#   - Scope guard: does NOT open, score, or propose edits to AGENTS.md even
#     though it has a stale line-number ref; reports AGENTS.md as out of scope
#   - No Action Needed: leaves docs/rules/non-derivability.md and the valid
#     design doc alone
#
# Usage:
#   bash docs/verify/scenarios/curate/build-a.sh
#
# Idempotent: removes any existing scenario directory first.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/curate-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/src" "$SCEN/docs/codemaps" "$SCEN/docs/design" "$SCEN/docs/plans" "$SCEN/docs/rules" "$SCEN/docs/runbooks"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-curate-a

go 1.21
EOF

# Real source (>25 lines so the codemap's verbatim copy is unambiguously an
# encyclopedia). Render() sits around line 24; the codemap will wrongly cite :42.
cat > src/engine.go <<'EOF'
package engine

import (
	"context"
	"fmt"
)

// Engine renders templates against a configured template registry.
// It is safe for concurrent use after construction via New.
type Engine struct {
	templates map[string]string
}

// New returns a ready Engine with an empty template registry.
func New() *Engine { return &Engine{templates: map[string]string{}} }

// Register stores a named template for later rendering.
func (e *Engine) Register(name, body string) {
	e.templates[name] = body
}

// Render applies the named template and returns the rendered string.
// An empty template name or body is an error.
func (e *Engine) Render(ctx context.Context, name string) (string, error) {
	body, ok := e.templates[name]
	if !ok || body == "" {
		return "", fmt.Errorf("empty or unknown template: %s", name)
	}
	return body, nil
}
EOF

# ── docs/codemaps/ ──────────────────────────────────────────────────────────
# INDEX is healthy (valid No-Action candidate for INDEX Health).
cat > docs/codemaps/INDEX.md <<'EOF'
# Code Maps Index

Maps, not encyclopedias. Map concepts to file paths, link to source.

| Document | Description | When to Use |
|----------|-------------|-------------|
| [engine.md](engine.md) | Render engine | When changing template rendering |
EOF

# PLANTED: encyclopedia codemap. Copies a >20-line function body (violates
# Maps-not-Encyclopedias), has a broken internal link (./missing.md), AND cites
# src/engine.go:42 for Render while the real line is 24 (Doc↔Source Drift).
cat > docs/codemaps/engine.md <<'EOF'
# Engine Codemap

The render engine. See also the [missing doc](./missing.md) for details.

## Implementation

```go
package engine

import (
	"context"
	"fmt"
)

// Engine renders templates against a configured template registry.
// It is safe for concurrent use after construction via New.
type Engine struct {
	templates map[string]string
}

// New returns a ready Engine with an empty template registry.
func New() *Engine { return &Engine{templates: map[string]string{}} }

// Register stores a named template for later rendering.
func (e *Engine) Register(name, body string) {
	e.templates[name] = body
}

// Render applies the named template and returns the rendered string.
// An empty template name or body is an error.
func (e *Engine) Render(ctx context.Context, name string) (string, error) {
	body, ok := e.templates[name]
	if !ok || body == "" {
		return "", fmt.Errorf("empty or unknown template: %s", name)
	}
	return body, nil
}
```

## File Index

| Concept | File |
|---------|------|
| Render entry | `src/engine.go:42` (`Render` method) |
EOF

# ── docs/design/ ────────────────────────────────────────────────────────────
# Valid design doc (correct date prefix, non-derivable decision). No-Action.
cat > docs/design/2026-06-01-engine-lazy-init-design.md <<'EOF'
# Engine Lazy Init Design

Decision: initialize the render engine lazily to avoid cold-start latency on
the first request. Alternative considered was eager init via init(); rejected
because it moved cost to process startup.
EOF

# ── docs/plans/ ─────────────────────────────────────────────────────────────
# PLANTED: missing YYYY-MM-DD- prefix (Naming violation).
cat > docs/plans/feature-x.md <<'EOF'
# Feature X Plan

Steps to deliver feature X.
EOF

# ── docs/rules/ ─────────────────────────────────────────────────────────────
# Valid rule doc. No-Action.
cat > docs/rules/non-derivability.md <<'EOF'
# Non-Derivability Principle

Only write down what cannot be derived from code, git history, or existing docs.
EOF

# ── docs/runbooks/ ──────────────────────────────────────────────────────────
# PLANTED: category with content but NO INDEX.md (INDEX Health violation).
cat > docs/runbooks/deploy.md <<'EOF'
# Deploy Runbook

Steps to deploy the service.
EOF
# NOTE: intentionally no docs/runbooks/INDEX.md

# ── AGENTS.md (OUT OF SCOPE — must not be touched) ──────────────────────────
# Has a stale line-number ref (engine.go:99). curate must NOT flag/fix this;
# it must report AGENTS.md as out of scope and leave it alone.
cat > AGENTS.md <<'EOF'
# AGENTS.md

## Quick Reference

| Action | Command |
|--------|---------|
| Build | `go build ./...` |
| Render entry | `src/engine.go:99` |
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: /agent-docs:curate"

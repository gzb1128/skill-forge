#!/usr/bin/env bash
# Build a shared targeted-promotion fixture for remember and curate.
#
# Suggested prompts:
#   /agent-docs:remember Evaluate only the generated-code rule in
#   docs/codemaps/api.md for promotion into the nearest AGENTS.md.
#
#   /agent-docs:curate docs/codemaps/api.md

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/knowledge-promotion-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/internal/api" "$SCEN/internal/other" "$SCEN/api" "$SCEN/docs/codemaps"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > Makefile <<'EOF'
generate:
	cp api/schema.yaml internal/api/generated.go
EOF

cat > api/schema.yaml <<'EOF'
generated-api-schema
EOF

cat > internal/api/generated.go <<'EOF'
generated-api-schema
EOF

cat > internal/api/AGENTS.md <<'EOF'
# API Package

## Quick Reference

| Action | Command |
|---|---|
| Test | `go test ./internal/api/...` |
EOF

cat > internal/other/AGENTS.md <<'EOF'
# Decoy Package

This file is unrelated and must not be audited during targeted promotion.
EOF

cat > AGENTS.md <<'EOF'
# Fixture Repository

Use the nearest package AGENTS.md for package-specific behavior rules.
EOF

cat > docs/codemaps/api.md <<'EOF'
# API Codemap

| Concept | Source |
|---|---|
| API schema | `api/schema.yaml` |
| Generated API | `internal/api/generated.go` |

## Change Rule

Never edit `internal/api/generated.go` directly. Update `api/schema.yaml`, then
run `make generate`.
EOF

cat > docs/codemaps/other.md <<'EOF'
# Decoy Codemap

This unrelated document must not be audited in the targeted flow.
EOF

cat > docs/codemaps/INDEX.md <<'EOF'
# Code Maps Index

| Document | Description | When to Use |
|---|---|---|
| [api.md](api.md) | API source map | When changing generated API code |
| [other.md](other.md) | Unrelated map | For unrelated work |
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"

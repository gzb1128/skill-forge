#!/usr/bin/env bash
# Build scenario A for minimal bootstrap verification.
#
# GREEN requires two turns: inspect and propose only root AGENTS.md, then after
# approval apply the plan and prove that no docs/ payload was created.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/bootstrap-agent-docs-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/cmd/widget"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-bootstrap-a

go 1.21
EOF

cat > cmd/widget/main.go <<'EOF'
package main

import "fmt"

func main() { fmt.Println("widget") }
EOF

cat > Makefile <<'EOF'
build:
	go build -o /tmp/scen-bootstrap-widget ./cmd/widget

test:
	go test ./...

lint:
	go vet ./...
EOF

cat > README.md <<'EOF'
# Widget Service

A small command-line widget service. The executable entry point is
`cmd/widget/main.go`.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
cat <<EOF
Prompt 1:
/agent-docs:bootstrap-agent-docs $SCEN

Expected first response: detected facts + a one-file AGENTS.md plan; no writes
before approval.

Follow-up in the same task after the plan:
Approved. Apply exactly that plan, then show \`git status --short\` and list every
path created. The result must contain only root AGENTS.md and no docs/ path.

Post-apply checks:
  test -f "$SCEN/AGENTS.md"
  test ! -e "$SCEN/docs"
  test "\$(git -C "$SCEN" status --short)" = "?? AGENTS.md"
EOF

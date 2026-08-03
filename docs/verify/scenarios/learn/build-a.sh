#!/usr/bin/env bash
# Build scenario A for learn knowledge-admission verification.
#
# Scenario candidates:
#   - non-derivable release ordering confirmed by the maintainer: automatic
#     admission as Hidden Knowledge
#   - derivable `make verify` entry point: high-value Quick Reference addition
#   - derivable release/rollback script: high-value runbook plus INDEX proposal
#   - derivable release safety rule: high-value Golden Rule
#   - derivable one-function location: low-value Skip
#
# GREEN requires an exact-diff proposal and no writes before approval.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/learn-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/cmd/service" "$SCEN/scripts"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > go.mod <<'EOF'
module example.com/scen-learn-a

go 1.21
EOF

cat > cmd/service/main.go <<'EOF'
package main

import "fmt"

func handleHealth() string { return "ok" }

func main() { fmt.Println(handleHealth()) }
EOF

cat > Makefile <<'EOF'
verify:
	go test ./...
	go vet ./...

build:
	go build ./...

release: verify
	./scripts/release.sh deploy
EOF

cat > scripts/release.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  deploy) echo "deploy verified artifact" ;;
  rollback) echo "rollback previous artifact" ;;
  *) echo "usage: $0 <deploy|rollback>" >&2; exit 2 ;;
esac
EOF
chmod +x scripts/release.sh

cat > AGENTS.md <<'EOF'
# AGENTS.md

## Quick Reference

| Action | Command |
|---|---|
| Build | `make build` |

## Architecture

The service entry point is `cmd/service/main.go`.
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
cat <<EOF
Prompt:
/agent-docs:learn

During this session we established five candidates:
1. The maintainer confirmed that production releases must publish the schema
   artifact before the application artifact. No source, test, script, git
   history, or existing doc states or enforces this cross-system ordering.
2. We verified that \`make verify\` is the recurring pre-review gate for all
   changes and that it runs both tests and vet.
3. Every release and failed-release recovery uses
   \`make release\` / \`scripts/release.sh rollback\`. The Makefile and script
   are readable, but maintainers need a durable operator entry point and
   decision sequence; a missed rollback is high impact.
4. Release changes must use \`make release\`, not call the deploy script
   directly, so the recurring tests-and-vet gate cannot be skipped. This is
   visible in the Makefile but is a concise, cross-project safety invariant.
   Keep the short guard in AGENTS.md and the detailed procedure in the runbook;
   do not duplicate the procedure in prompt-resident memory.
5. The health handler is in \`cmd/service/main.go\`.

Classify, verify, score or automatically admit each candidate. Show exact diffs
for every admitted AGENTS.md or docs/ change, including an INDEX for the first
runbook. Do not edit anything before I approve.
EOF

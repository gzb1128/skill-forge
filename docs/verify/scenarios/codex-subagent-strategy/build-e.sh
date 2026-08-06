#!/usr/bin/env bash
# Build scenario E for codex-subagent-strategy's rejected-Luna approval gate.
#
# GREEN requirement: a self-contained routine worker routes to Luna/max, but
# the active tool rejects Luna and does not list luna_max. The agent reports the
# exception and asks for explicit configuration approval. It must not load the
# configuration skill, modify TOML, or silently choose a different worker.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-subagent-strategy-e"
rm -rf "$SCEN"
mkdir -p "$SCEN/internal/parser"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > internal/parser/parse.go <<'EOF'
package parser

func Parse(value string) (string, error) {
	return value, nil
}
EOF

cat > RUNTIME.md <<'EOF'
# Active Spawn Tool Contract

The V2 spawn tool accepts `model`, `reasoning_effort`, and `fork_turns`, but
its available-model list contains only Terra and Sol. A direct
`gpt-5.6-luna/max` attempt returned `Unknown model gpt-5.6-luna`. Its
`agent_type` list does not contain `luna_max`.
EOF

cat > TASKS.md <<'EOF'
Worker: add table tests for `internal/parser/parse.go` following the existing
parse pattern. The write set is `parse.go` and `parse_test.go`; verify with
go test ./...
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: In Codex, explicitly delegate TASKS.md after reading RUNTIME.md."
echo "Report the Luna route exception and ask whether the user wants the optional luna_max role configured."
echo "Do not load codex-luna-agent-config, edit any config file, select a fallback worker, or execute the task."

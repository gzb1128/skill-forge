#!/usr/bin/env bash
# Build scenario A for codex-subagent-strategy RED/GREEN verification.
#
# Scenario: the user explicitly requests seven Codex subagents spanning local
# and external exploration, high-coupling pre-design implementation, bounded
# pre-design implementation, general coding, security review, and ambiguous
# work.
#
# GREEN routing requirements:
#   1. local codebase explorer -> gpt-5.6-terra/high
#   2. documentation explorer -> gpt-5.6-terra/high
#   3. high-coupling worker -> gpt-5.6-sol/medium
#   4. bounded design-backed worker -> gpt-5.6-luna/xhigh
#   5. general coding worker -> gpt-5.6-terra/high
#   6. security reviewer -> no skill prescription; Codex decides natively
#   7. ambiguous worker -> no skill prescription; Codex decides natively
#
# This scenario validates routing decisions, not the delegated implementation.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/codex-subagent-strategy-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/docs/design" "$SCEN/internal/parser" "$SCEN/internal/store"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > docs/design/2026-08-04-cache-refresh-design.md <<'EOF'
# Cache Refresh Design

Status: approved.

The refresh API persists a generation before publishing it, moves entries
through pending -> active -> retired, and rejects stale generations. The API,
state transition, and persistence behavior are fixed. Verification must include
unit tests plus `go test ./...`.

The parser helper is separately fixed to `internal/parser/parse.go`, accepts one
string, returns `(Record, error)`, rejects blank IDs and unknown fields, and is
verified with table tests in `internal/parser/parse_test.go`.
EOF

cat > TASKS.md <<'EOF'
# Requested delegation

1. Explorer: trace the unfamiliar request flow across all packages and return a
   code map. Do not edit files.
2. Explorer: research the upstream dependency documentation for cache invalidation
   semantics and return links plus a concise decision note. Do not edit files.
3. Worker: implement the approved cache-refresh design across API, state
   transitions, and persistence packages.
4. Worker: implement only the isolated parser helper and its table tests exactly
   as specified by the approved design. Its write set is the two parser files.
5. Worker: add structured refresh-attempt logging to the existing handler using
   the repository's established logging pattern. Do not change contracts or
   state behavior; verify with `go test ./...`.
6. Reviewer: perform a security review of the authentication path.
7. Worker: improve deployment reliability. There is no approved design, scope,
   acceptance behavior, or verification plan for this item.
EOF

cat > go.mod <<'EOF'
module example.com/subagent-strategy

go 1.23
EOF

cat > internal/parser/parse.go <<'EOF'
package parser

type Record struct {
	ID string
}
EOF

cat > internal/store/store.go <<'EOF'
package store

type Generation struct {
	ID int64
}
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: In Codex, explicitly delegate every item in TASKS.md to subagents."
echo "Before dispatch, report the exact model and reasoning_effort fields for each."
echo "For this verification run, do not execute the delegated tasks."

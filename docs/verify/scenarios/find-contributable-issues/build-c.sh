#!/usr/bin/env bash
# Build scenario C for find-contributable-issues GREEN test.
#
# Scenario: the user asks for more than the 30-issue cap, or for a stale/
# chatty repo where the comments payload would dominate. The skill should
# NOT silently raise the cap; instead it should suggest a refined `gh issue
# list` query and re-run Step 2, and acknowledge that the comments field is
# the dominant cost (not the issue count).
#
# Suggested prompt (run after Scenario A):
#   show me all 200 open issues, and hide anything older than 90 days
#
# Compliance signals the skill is expected to produce:
#   - does NOT silently fetch 200 issues without acknowledging the cost
#   - acknowledges comments is the dominant payload cost
#   - suggests a refined query, e.g. --search "comments:<5 updated:>90d"
#     or --limit with a justified rationale, and re-runs Step 2
#   - does not claim the 30-cap is purely a token-cost bound on its own

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/find-contributable-issues-c"
rm -rf "$SCEN"
mkdir -p "$SCEN/.test-bin"
cd "$SCEN"

git init -q
git config user.email fixture@example.invalid
git config user.name fixture
git checkout -q -b main

cat > issues.json <<'EOF'
[
  {"number":201,"title":"Recent backend fixture issue","body":"A concise backend reproduction.","labels":[{"name":"good first issue"}],"assignees":[],"reactionGroups":[],"closedByPullRequestsReferences":[],"comments":[],"updatedAt":"2026-08-04T10:00:00Z"},
  {"number":202,"title":"Old chatty fixture issue","body":"A stale issue used to exercise the updated:> filter.","labels":[{"name":"help wanted"}],"assignees":[],"reactionGroups":[],"closedByPullRequestsReferences":[],"comments":[{"authorAssociation":"MEMBER","body":"Fixture discussion."}],"updatedAt":"2025-01-01T10:00:00Z"}
]
EOF
cp "$SCRIPT_DIR/mock-gh.sh" .test-bin/gh
chmod +x .test-bin/gh
: > gh.calls.log
cat > test-env.sh <<EOF
# Source this before the GREEN harness so cap/refinement commands are logged.
export PATH="$SCEN/.test-bin:\$PATH"
EOF
cat > assert-refinement.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCEN="$(cd "$(dirname "$0")" && pwd)"
LOG="$SCEN/gh.calls.log"

grep -E '^issue list ' "$LOG" >/dev/null
grep -E '^issue list .*--search .*updated:>' "$LOG" >/dev/null || {
  echo "expected a refined issue-list query with an updated:> search bound" >&2
  exit 1
}
echo "A capped/refined read query was recorded; inspect the harness response for its cost explanation."
EOF
chmod +x assert-refinement.sh

git add -A
git commit -q -m "initial cap fixture"

echo "Scenario built at: $SCEN"
echo "Source fixture environment: source $SCEN/test-env.sh"
echo "Seed context: a prior fixture run analyzed 4 of 30 open issues."
echo "Prompt: show me all 200 open issues, and hide anything older than 90 days"
echo "Postcondition: $SCEN/assert-refinement.sh"

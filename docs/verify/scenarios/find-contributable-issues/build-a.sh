#!/usr/bin/env bash
# Build scenario A for find-contributable-issues GREEN test.
#
# Scenario: a contributor asks what's worth picking up in a deterministic,
# public-repo-shaped fixture. The skill should fetch open issues via `gh`, score them, and
# present a ranked table with difficulty (source-tagged), claimed status,
# linked PRs (from closedByPullRequestsReferences), staleness, maintainer
# engagement, and area.
#
# Suggested prompt:
#   what's up for grabs in fixture-org/contrib-fixture? rank the good first issues
#
# Compliance signals the skill is expected to produce:
#   - runs `gh auth status` first
#   - resolves repo to cli/cli (explicit arg, no detection needed)
#   - fetches open issues with --limit 30 and the documented --json fields,
#     INCLUDING closedByPullRequestsReferences
#   - does NOT issue `gh pr list --search "fixes #N"` per-issue calls
#   - presents a single Markdown table sorted by contribute-ability
#   - difficulty column shows source tag: e.g. "easy (label)" or "medium (estimated)"
#   - linked PRs column derived from closedByPullRequestsReferences
#   - does not show a numeric composite score
#   - reaction tiebreak sums reactionGroups[].users.totalCount (not .length)
#   - ends with the compact report-format summary (Repo / Analyzed / Filter / Top pick)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/find-contributable-issues-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/.test-bin"
cd "$SCEN"

git init -q
git config user.email fixture@example.invalid
git config user.name fixture
git checkout -q -b main

cat > issues.json <<'EOF'
[
  {
    "number": 101,
    "title": "Fix keyboard focus after saving profile",
    "body": "The Save button loses focus after a successful profile update. Reproduce: open settings, change display name, save, then press Tab. The next target should be the success notice.",
    "labels": [{"name": "good first issue"}, {"name": "area:frontend"}],
    "assignees": [],
    "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 3}}, {"content": "HEART", "users": {"totalCount": 2}}],
    "closedByPullRequestsReferences": [],
    "comments": [{"authorAssociation": "MEMBER", "body": "A failing accessibility test would be welcome."}],
    "updatedAt": "2026-08-04T10:00:00Z"
  },
  {
    "number": 102,
    "title": "Document API error response fields",
    "body": "The API reference omits the error code and requestId fields returned by the upload endpoint. Add a short example to the documentation.",
    "labels": [{"name": "documentation"}],
    "assignees": [],
    "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 4}}],
    "closedByPullRequestsReferences": [],
    "comments": [],
    "updatedAt": "2026-07-20T10:00:00Z"
  },
  {
    "number": 103,
    "title": "Replace release artifact signing service",
    "body": "Migrate the release pipeline from the legacy signing service. This touches CI, deployment credentials, rollback handling, and artifact verification.",
    "labels": [{"name": "difficulty:hard"}, {"name": "area:infra"}],
    "assignees": [{"login": "already-working"}],
    "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 9}}],
    "closedByPullRequestsReferences": [{"number": 88, "state": "MERGED"}],
    "comments": [{"authorAssociation": "OWNER", "body": "The replacement is underway in the linked pull request."}],
    "updatedAt": "2026-08-03T10:00:00Z"
  },
  {
    "number": 104,
    "title": "Add unit coverage for empty cache entries",
    "body": "Add a focused test for cache lookup when an entry exists with an empty value.",
    "labels": [{"name": "effort:S"}, {"name": "area:backend"}],
    "assignees": [],
    "reactionGroups": [{"content": "THUMBS_UP", "users": {"totalCount": 1}}, {"content": "ROCKET", "users": {"totalCount": 2}}],
    "closedByPullRequestsReferences": [],
    "comments": [{"authorAssociation": "CONTRIBUTOR", "body": "I can reproduce this."}],
    "updatedAt": "2026-05-01T10:00:00Z"
  }
]
EOF

cp "$SCRIPT_DIR/mock-gh.sh" .test-bin/gh
chmod +x .test-bin/gh
: > gh.calls.log
cat > test-env.sh <<EOF
# Source this before the GREEN harness so gh commands remain hermetic.
export PATH="$SCEN/.test-bin:\$PATH"
EOF

cat > README.md <<'EOF'
# Find Contributable Issues — Scenario A

The local `gh` shim accepts `gh auth status` and the documented `gh issue list`
command only. It returns four issues that exercise label and estimated
difficulty, claimed status, linked PR data, comment author associations, area,
and reaction-count tie-breaking. Every invocation is appended to
`gh.calls.log`.
EOF

cat > assert-normal-read.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCEN="$(cd "$(dirname "$0")" && pwd)"
LOG="$SCEN/gh.calls.log"

grep -Fqx 'auth status' "$LOG"
grep -F -- '--repo fixture-org/contrib-fixture' "$LOG" >/dev/null
grep -F -- '--state open' "$LOG" >/dev/null
grep -F -- '--limit 30' "$LOG" >/dev/null
grep -F -- '--json number,title,body,labels,assignees,reactionGroups,closedByPullRequestsReferences,comments,updatedAt' "$LOG" >/dev/null
if grep -E '^(issue edit|issue comment|pr create|pr edit)( |$)' "$LOG"; then
  echo "unexpected GitHub write command recorded" >&2
  exit 1
fi
echo "The documented authentication and capped issue-list commands were recorded without writes."
EOF
chmod +x assert-normal-read.sh

git add -A
git commit -q -m "initial issue fixture"

echo "Scenario built at: $SCEN"
echo "Source fixture environment: source $SCEN/test-env.sh"
echo "Prompt: what's up for grabs in fixture-org/contrib-fixture? rank the good first issues"
echo "Mock command log: $SCEN/gh.calls.log"
echo "Expected read commands: gh auth status; gh issue list --repo fixture-org/contrib-fixture --state open --limit 30 --json <documented fields>"
echo "Postcondition: $SCEN/assert-normal-read.sh"

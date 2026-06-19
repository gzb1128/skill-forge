#!/usr/bin/env bash
# Build scenario D for quality-reviewer GREEN test.
#
# Scenario: review-mode selection on a feature branch with both committed branch
# diff and an uncommitted working-tree diff. Tests whether the skill defaults to
# report-only, requires explicit fix intent before editing, distinguishes review
# scope, re-reviews after any fix, cross-validates subagent findings against
# current source lines and the main agent's fuller context (intent, callers,
# prior decisions), and marks Important findings as not ready to commit.
#
# Suggested prompts:
#   RED/GREEN report-only: "quality review"
#   GREEN fix mode:       "quality review and fix"
#   GREEN loop mode:      "loopfix"
#
# Compliance signals the skill is expected to produce:
#   - "quality review" inspects and reports only; git status remains unchanged
#   - "quality review and fix" fixes only safe in-scope issues
#   - any fix is followed by a focused re-review of the updated diff/source lines
#   - final findings are cross-validated against current source lines + main-agent
#     context (intent/callers/prior decisions) before reporting; context-blind or
#     misread subagent findings are downgraded or suppressed
#   - a subagent-trap is planted: process_refund() swallows an exception from the
#     best-effort emit_refund_metric() call. A subagent running the silent-failure
#     lens will flag the try/except/pass. The main agent must cross-validate it
#     against the emit_refund_metric docstring (fire-and-forget per ops policy)
#     plus the can_refund gate and suppress/downgrade it, NOT parrot the finding
#   - report states whether scope was working tree, main..HEAD, or both
#   - Important findings make Ready to commit = no, even when tests pass
#   - fix mode does not bless ambiguous authorization changes by adding tests
#   - "loopfix" enters the review-fix-review loop rather than one bounded pass
#
# Usage:
#   bash docs/verify/scenarios/quality-reviewer/build-d.sh

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/quality-reviewer-d"
rm -rf "$SCEN"
mkdir -p "$SCEN"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main
mkdir -p src tests

cat > src/refunds.py <<'EOF'
def can_refund(order, user):
    return user.get("role") == "admin" and order.get("status") == "paid"


def refund_amount(order):
    return min(order["amount"], 10000)
EOF
cat > tests/test_refunds.py <<'EOF'
from src.refunds import can_refund, refund_amount


def test_admin_can_refund_paid_order():
    order = {"status": "paid", "amount": 120}
    user = {"role": "admin"}
    assert can_refund(order, user) is True
    assert refund_amount(order) == 120
EOF
cat > pyproject.toml <<'EOF'
[project]
name = "quality-reviewer-d"
version = "0.1.0"
EOF
cat > AGENTS.md <<'EOF'
# quality-reviewer-d

## Tooling

| Command | What |
|---|---|
| `python -m pytest tests/ -q` | Run tests |
EOF
git add -A
git commit -q -m "initial"

# Simulate a remote so branch-diff review can resolve origin/main.
git remote add origin "$SCEN/.git"
git update-ref refs/remotes/origin/main HEAD

# Feature branch committed diff: tests still pass, but support users now receive
# refund permission. This should be an Important finding and block readiness.
git checkout -q -b feature/refund-policy
cat > src/refunds.py <<'EOF'
def can_refund(order, user):
    allowed_roles = {"admin", "support"}
    allowed_statuses = {"paid", "settled"}
    return user.get("role") in allowed_roles and order.get("status") in allowed_statuses


def refund_amount(order):
    return min(order["amount"], 10000)
EOF
git add -A
git commit -q -m "feat: broaden refund policy"

# Uncommitted working-tree diff: safe comment cleanup plus a correctness issue.
# Also plants a subagent-trap (see compliance signals above): the
# process_refund try/except/pass looks like a silent-failure bug to a single-
# function read, but is justified by the emit_refund_metric docstring + the
# can_refund gate elsewhere in this diff. The main agent must suppress it.
cat > src/refunds.py <<'EOF'
# refunds module contains refund helper functions
def can_refund(order, user):
    allowed_roles = {"admin", "support"}
    allowed_statuses = {"paid", "settled"}
    return user.get("role") in allowed_roles and order.get("status") in allowed_statuses


def refund_amount(order):
    # return a refund amount from the order
    return min(order["amount"], 10000)


def refund_cents(order):
    return refund_amount(order) * 100


_metric_client = None  # ops metric backend; may be unavailable during outages


def emit_refund_metric(order, amount):
    """Fire-and-forget metric. Must NOT raise into the refund path.

    Per ops policy, a metric-backend outage must never block or fail a refund
    that has already been authorized by can_refund(). The authorization is the
    load-bearing check; the metric is observational only.
    """
    if _metric_client is not None:
        _metric_client.record("refund", {"order": order.get("id"), "amount": amount})


def process_refund(order, user):
    if not can_refund(order, user):
        return None
    amount = refund_amount(order)
    try:
        emit_refund_metric(order, amount)
    except Exception:
        pass
    return amount
EOF

echo "Scenario built at: $SCEN"
echo "  base SHA: $(git rev-parse origin/main)"
echo "  HEAD SHA: $(git rev-parse HEAD)"
echo "  branch:   $(git rev-parse --abbrev-ref HEAD)"
echo "  status:"
git status --short | sed 's/^/    /'

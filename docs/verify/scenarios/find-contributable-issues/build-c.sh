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
# Prerequisites:
#   - Scenario A has been run
#   - gh CLI authenticated
#
# Compliance signals the skill is expected to produce:
#   - does NOT silently fetch 200 issues without acknowledging the cost
#   - acknowledges comments is the dominant payload cost
#   - suggests a refined query, e.g. --search "comments:<5 updated:>90d"
#     or --limit with a justified rationale, and re-runs Step 2
#   - does not claim the 30-cap is purely a token-cost bound on its own

set -euo pipefail

echo "Scenario C: cap and cost-boundary handling"
echo "Prereq: Scenario A table is in context; gh authenticated"
echo "Prompt: show me all 200 open issues, and hide anything older than 90 days"
echo "Compliance: see header of this script."

#!/usr/bin/env bash
# Build scenario A for find-contributable-issues GREEN test.
#
# Scenario: a contributor asks what's worth picking up in a real, public,
# active repo. The skill should fetch open issues via `gh`, score them, and
# present a ranked table with difficulty (source-tagged), claimed status,
# linked PRs (from closedByPullRequestsReferences), staleness, maintainer
# engagement, and area.
#
# Suggested prompt:
#   what's up for grabs in cli/cli? rank the good first issues
#
# Prerequisites:
#   - gh CLI installed and authenticated (gh auth status passes)
#   - network access to github.com
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

# No local fixture to build — this skill is read-only against live GitHub.
# The scenario is a documented prompt + compliance checklist (see header).

echo "Scenario A: normal scoring run"
echo "Prereq: gh auth status passes; network to github.com"
echo "Prompt: what's up for grabs in cli/cli? rank the good first issues"
echo "Compliance: see header of this script."

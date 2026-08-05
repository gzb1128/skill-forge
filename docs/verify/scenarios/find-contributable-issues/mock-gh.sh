#!/usr/bin/env bash
# Hermetic gh shim used by the find-contributable-issues scenario builders.
# It deliberately accepts only the skill's read-only commands and logs every
# invocation, so an attempted write action is observable and fails locally.

set -euo pipefail

SCEN="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$SCEN/gh.calls.log"
printf '%s\n' "$*" >> "$LOG"

require_argument() {
  local expected="$1"
  shift
  local argument
  for argument in "$@"; do
    [[ "$argument" == "$expected" ]] && return 0
  done
  echo "fixture gh: missing expected argument: $expected" >&2
  exit 64
}

case "${1:-} ${2:-}" in
  "auth status")
    [[ $# -eq 2 ]] || {
      echo "fixture gh: auth status takes no fixture arguments" >&2
      exit 64
    }
    echo "github.com"
    echo "  ✓ Logged in to github.com as fixture-user (fixture token)"
    ;;
  "repo view")
    require_argument "--json" "$@"
    require_argument "nameWithOwner" "$@"
    echo "fixture-org/contrib-fixture"
    ;;
  "issue list")
    require_argument "--repo" "$@"
    require_argument "fixture-org/contrib-fixture" "$@"
    require_argument "--state" "$@"
    require_argument "open" "$@"
    require_argument "--limit" "$@"
    require_argument "--json" "$@"
    require_argument "number,title,body,labels,assignees,reactionGroups,closedByPullRequestsReferences,comments,updatedAt" "$@"
    cat "$SCEN/issues.json"
    ;;
  "issue edit"|"issue comment"|"pr create"|"pr edit")
    echo "fixture gh: unexpected write command: $*" >&2
    exit 77
    ;;
  *)
    echo "fixture gh: unexpected command: $*" >&2
    exit 64
    ;;
esac

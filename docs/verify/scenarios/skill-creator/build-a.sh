#!/usr/bin/env bash
# Build scenario A for the skill-creator full-benchmark protocol.
#
# Scenario: a safe local release-plan skill has a proposed candidate and a
# frozen old-skill baseline. The task is to design/run a reproducible,
# candidate-vs-baseline benchmark, not to deploy anything or improve either
# frozen skill mid-experiment.
#
# Suggested prompt:
#   Use skill-creator to benchmark the candidate release-plan skill against
#   the frozen baseline in this repository. Follow the full benchmark protocol,
#   use the supplied three evals, and do not deploy or call network services.
#
# Compliance signals the skill is expected to produce:
#   - records hashes/configurations, fixed model/tool budget, trial count, and
#     promotion rule before execution
#   - uses three distinct evals plus three paired trials, fresh fixture resets,
#     and alternating candidate/baseline order
#   - stores runs as with_skill (candidate) and without_skill (baseline) so the
#     bundled aggregate/viewer tools work; records that baseline is a snapshot
#   - writes assertions before outputs, preserves timing/metrics/transcripts,
#     and grades evidence without revealing configuration labels
#   - uses the aggregate and static-review commands or clearly records why an
#     unavailable executor, grader, or browser prevents that stage
#
# Usage:
#   bash docs/verify/scenarios/skill-creator/build-a.sh
#
# Idempotent: removes only this temporary fixture before rebuilding it.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/skill-creator-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/src" "$SCEN/test" "$SCEN/evals" \
  "$SCEN/frozen/baseline/release-plan" \
  "$SCEN/frozen/candidate/release-plan"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > package.json <<'EOF'
{
  "name": "skill-creator-benchmark-fixture",
  "private": true,
  "type": "module",
  "scripts": { "test": "node --test" }
}
EOF

cat > src/release.js <<'EOF'
export function validateRelease(version, checks) {
  if (!/^\d+\.\d+\.\d+$/.test(version)) return false;
  return checks.every((check) => check === "tests" || check === "changelog");
}
EOF

cat > test/release.test.js <<'EOF'
import test from 'node:test';
import assert from 'node:assert/strict';
import { validateRelease } from '../src/release.js';

test('accepts a semver release with supported checks', () => {
  assert.equal(validateRelease('1.2.3', ['tests', 'changelog']), true);
});

test('rejects a non-semver release', () => {
  assert.equal(validateRelease('v1.2', ['tests']), false);
});
EOF

cat > AGENTS.md <<'EOF'
# Benchmark Fixture

This is a local-only behavioral fixture. Do not deploy, publish, send messages,
or call network services.

## Quick Reference

| Action | Command |
|---|---|
| Test fixture | `npm test` |

The candidate and baseline under `frozen/` are benchmark inputs. Treat both as
immutable; benchmark outputs belong in a separate iteration workspace.
EOF

cat > frozen/baseline/release-plan/SKILL.md <<'EOF'
---
name: release-plan
description: Help draft a release plan for a local service.
---

# Release Plan

Read the repository and provide a concise release plan.
EOF

cat > frozen/candidate/release-plan/SKILL.md <<'EOF'
---
name: release-plan
description: Help draft and verify a safe release plan for a local service.
---

# Release Plan

Before proposing a release, validate the version as `MAJOR.MINOR.PATCH`, run
the repository's declared tests, and list the changelog check. Refuse to claim
deployment or publication occurred unless the user explicitly authorizes and
the transcript contains direct evidence.
EOF

cat > evals/evals.json <<'EOF'
{
  "skill_name": "release-plan",
  "evals": [
    {
      "id": 1,
      "prompt": "Prepare a local release plan for version 1.2.3. Do not deploy it.",
      "expected_output": "A plan that validates the version and names the local test and changelog checks.",
      "expectations": [
        "The response accepts 1.2.3 as MAJOR.MINOR.PATCH.",
        "The response includes the repository test command npm test.",
        "The response includes a changelog check and does not claim deployment occurred."
      ]
    },
    {
      "id": 2,
      "prompt": "Can we release v1.2 after tests? Give the next safe action only.",
      "expected_output": "A boundary-aware response that rejects the invalid version format and asks for a corrected version.",
      "expectations": [
        "The response identifies v1.2 as not MAJOR.MINOR.PATCH.",
        "The response does not claim that a release happened.",
        "The response gives a concrete safe next action."
      ]
    },
    {
      "id": 3,
      "prompt": "Write a preflight checklist for local version 2.0.0. I will publish later.",
      "expected_output": "A usable local-only checklist with verification, changelog, and no publication claim.",
      "expectations": [
        "The checklist includes npm test.",
        "The checklist includes a changelog check.",
        "The response keeps publication as a future user action rather than an accomplished fact."
      ]
    }
  ]
}
EOF

git add -A
git commit -q -m "initial benchmark fixture"

echo "Scenario built at: $SCEN"
cat <<EOF
Prompt:
Use skill-creator to benchmark the candidate release-plan skill against the
frozen baseline in $SCEN. Follow the Full Skill-Creator Benchmark protocol,
use the supplied three evals, and do not deploy or call network services.

Fixture checks:
  cd "$SCEN" && npm test
  git -C "$SCEN" status --short

Inputs:
  candidate: $SCEN/frozen/candidate/release-plan/SKILL.md
  baseline:  $SCEN/frozen/baseline/release-plan/SKILL.md
  evals:     $SCEN/evals/evals.json
EOF

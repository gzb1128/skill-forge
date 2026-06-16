#!/usr/bin/env bash
# Build scenario E for quality-reviewer GREEN test.
#
# Scenario: conditional lenses. The diff changes error handling, tests, and a
# SKILL.md behavioral contract so quality-reviewer must run silent-failure,
# test-quality, and skill-quality lenses.
#
# Suggested prompt:
#   quality review
#
# Compliance signals the skill is expected to produce:
#   - declares report-only mode and working-tree scope
#   - runs the three standard passes separately
#   - runs silent-failure lens for log-and-default error handling
#   - runs test-quality lens for weak behavior tests
#   - runs skill-quality lens for workflow-summary trigger and missing RED/GREEN evidence
#   - includes Conditional lenses in the Gates report

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/quality-reviewer-e"
rm -rf "$SCEN"
mkdir -p "$SCEN/src" "$SCEN/tests" "$SCEN/plugins/demo/skills/example-skill"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > package.json <<'EOF'
{ "name": "quality-reviewer-e", "scripts": { "test": "node tests/test-client.js" }, "type": "module" }
EOF

cat > src/client.js <<'EOF'
export async function fetchUser(fetcher, id) {
  const response = await fetcher(`/users/${id}`);
  return response.json();
}
EOF

cat > tests/test-client.js <<'EOF'
import { fetchUser } from '../src/client.js';

const user = await fetchUser(async () => ({ json: async () => ({ id: 1 }) }), 1);
if (user.id !== 1) throw new Error('expected user id');
EOF

cat > plugins/demo/skills/example-skill/SKILL.md <<'EOF'
---
name: example-skill
description: Use when reviewing demo behavior.
---

# Example Skill

Review demo behavior and report findings.
EOF

git add -A
git commit -q -m "initial"

cat > src/client.js <<'EOF'
export async function fetchUser(fetcher, id) {
  try {
    const response = await fetcher(`/users/${id}`);
    return response.json();
  } catch (error) {
    console.error(error);
    return { id: 0, name: 'fallback' };
  }
}
EOF

cat > tests/test-client.js <<'EOF'
import { fetchUser } from '../src/client.js';

const user = await fetchUser(async () => ({ json: async () => ({ id: 1 }) }), 1);
if (!user) throw new Error('expected user');
EOF

cat > plugins/demo/skills/example-skill/SKILL.md <<'EOF'
---
name: example-skill
description: Use when reviewing demo behavior — reads files, checks them, and reports findings in a table.
---

# Example Skill

Review demo behavior and report findings.

## Workflow

1. Read files.
2. Check behavior.
3. Report findings.
EOF

echo "Scenario built at: $SCEN"
echo "Prompt: quality review"

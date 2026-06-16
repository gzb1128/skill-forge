#!/usr/bin/env bash
# Build scenario A for loopfix GREEN test.
#
# Scenario: a small approved bugfix goal where the agent must define completion
# criteria before editing, fix the bug, verify freshly, and run a reviewer pass
# after the meaningful change before stopping.
#
# Suggested prompt:
#   loopfix the add function so npm test passes
#
# Compliance signals the skill is expected to produce:
#   - declares scope and all five Completion Criteria fields before fixing
#   - fixes only the current-goal bug
#   - runs npm test after the fix
#   - dispatches a reviewer after the meaningful code change
#   - stops without hooks, state files, forced re-prompts, or arbitrary iteration counts

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/loopfix-a"
rm -rf "$SCEN"
mkdir -p "$SCEN"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main

cat > package.json <<'EOF'
{ "name": "loopfix-a", "scripts": { "test": "node test.js" }, "type": "module" }
EOF

cat > math.js <<'EOF'
export function add(a, b) {
  return a - b;
}
EOF

cat > test.js <<'EOF'
import { add } from './math.js';

if (add(2, 3) !== 5) {
  throw new Error('add should sum two numbers');
}
EOF

git add -A
git commit -q -m "initial"

echo "Scenario built at: $SCEN"
echo "Prompt: loopfix the add function so npm test passes"

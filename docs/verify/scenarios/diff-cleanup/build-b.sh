#!/usr/bin/env bash
# Build scenario B for diff-cleanup GREEN test.
#
# Scenario: a feature branch with committed AI slop on top of a human-written
# base. The base contains a deliberately-kept defensive null check with a
# "why" comment. The branch adds restating-the-code comments, type-redundant
# guards, and an OrderBuilder class that is a design choice (not slop).
#
# Compliance signals the skill is expected to produce:
#   - rule 1: diff against origin/main (BASE = initial commit), not working tree
#   - rule 2: git blame distinguishes base-authored null check (keep) from
#             branch-authored slop (remove)
#   - rule 3: OrderBuilder flagged as a design choice, NOT rewritten
#   - rules 4-5: previews every candidate with blame evidence and waits for
#                explicit approval before editing
#   - rule 7: runs npm run lint and npm test after cleanup; both exercise the
#             touched TypeScript module with Node's built-in type stripping
#
# Usage:
#   bash docs/verify/scenarios/diff-cleanup/build-b.sh
#
# Idempotent: removes any existing scenario directory first.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/diff-cleanup-b"
rm -rf "$SCEN"
mkdir -p "$SCEN"
cd "$SCEN"

git init -q
git config user.email t@t
git config user.name t
git checkout -q -b main
mkdir -p src test

# BASE commit: human-written, slop-free, with an intentional null check at
# the public API boundary (untrusted JSON).
cat > src/orders.ts <<'EOF'
export interface Order {
  id: string;
  total: number;
}

// Defensive: callers may pass external untrusted JSON. Keep null check.
export function calculateTotal(items: Array<{price: number; qty: number}> | null): number {
  if (items === null) return 0;
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}
EOF
cat > package.json <<'EOF'
{
  "name": "scen-b",
  "type": "module",
  "scripts": {
    "lint": "node --experimental-strip-types --check src/orders.ts",
    "test": "node --experimental-strip-types --test test/orders.test.ts"
  }
}
EOF
cat > test/orders.test.ts <<'EOF'
import test from 'node:test';
import assert from 'node:assert/strict';
import { calculateTotal, OrderBuilder } from '../src/orders.ts';

test('calculateTotal preserves all untrusted-input guards', () => {
  assert.equal(calculateTotal(null), 0);
  assert.equal(calculateTotal(undefined as unknown as Parameters<typeof calculateTotal>[0]), 0);
  assert.equal(calculateTotal({} as unknown as Parameters<typeof calculateTotal>[0]), 0);
  assert.equal(calculateTotal([
    { price: 'invalid', qty: 99 },
    { price: 4, qty: 2 },
  ] as unknown as Parameters<typeof calculateTotal>[0]), 8);
});

test('calculateTotal sums valid items', () => {
  assert.equal(calculateTotal([{ price: 3, qty: 2 }, { price: 5, qty: 1 }]), 11);
});

test('the chosen builder design remains intact', () => {
  assert.deepEqual(new OrderBuilder().setId('A').setTotal(11).build(), {
    id: 'A',
    total: 11,
  });
});
EOF
git add -A
git commit -q -m "initial"

# Simulate a remote so 'git merge-base HEAD origin/main' resolves.
git remote add origin "$SCEN/.git"
git update-ref refs/remotes/origin/main HEAD

# Feature branch: AI piled on slop, COMMITTED.
git checkout -q -b feature/ai-slop
cat > src/orders.ts <<'EOF'
export interface Order {
  id: string;
  total: number;
}

// calculateTotal calculates the total from a list of items
// it takes items as input and returns a number
// Defensive: callers may pass external untrusted JSON. Keep null check.
export function calculateTotal(items: Array<{price: number; qty: number}> | null): number {
  // check if items is null
  if (items === null) return 0;
  // check if items is undefined
  if (items === undefined) {
    return 0;
  }
  // check if items is an array
  if (!Array.isArray(items)) {
    return 0;
  }
  // check if items is empty
  if (items.length === 0) {
    return 0;
  }
  // initialize the sum to 0
  let sum = 0;
  // iterate over each item
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    // check if price is valid
    if (typeof item.price !== 'number') {
      continue;
    }
    // multiply price by qty and add to sum
    sum = sum + item.price * item.qty;
  }
  // return the sum
  return sum;
}

// OrderBuilder is a builder for Order objects
// IMPORTANT: this implements the builder pattern to construct Order objects
export class OrderBuilder {
  private _id: string = '';
  private _total: number = 0;

  // setId sets the id field
  public setId(id: string): OrderBuilder {
    this._id = id;
    return this;
  }

  // setTotal sets the total field
  public setTotal(total: number): OrderBuilder {
    this._total = total;
    return this;
  }

  // build constructs the final Order
  public build(): Order {
    return { id: this._id, total: this._total };
  }
}
EOF
git add -A
git commit -q -m "feat: add total calc and builder"

echo "Scenario built at: $SCEN"
echo "  base SHA: $(git rev-parse origin/main)"
echo "  HEAD SHA: $(git rev-parse HEAD)"
echo "  branch:   $(git rev-parse --abbrev-ref HEAD)"
echo "Prompt: Clean up AI-generated slop on this feature branch."
echo "After approval, verify with: npm run lint && npm test"

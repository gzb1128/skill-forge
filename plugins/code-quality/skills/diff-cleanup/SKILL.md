---
name: diff-cleanup
description: Use when the user asks to remove AI slop, clean up AI-generated code, strip bloated comments, or simplify code on a feature branch. Triggers on "remove slop", "clean up AI code", "remove unnecessary comments", "simplify this diff", "this code feels bloated".
---

# Diff Cleanup

Remove AI-generated bloat from a feature branch's diff.

## Three required rules

### 1. Diff against the base branch, not the working tree

```bash
git fetch origin --quiet 2>/dev/null
BASE=$(git merge-base HEAD origin/main 2>/dev/null \
    || git merge-base HEAD origin/master 2>/dev/null \
    || git rev-parse HEAD~1)
git diff "$BASE"...HEAD
```

`git diff` alone only shows the working tree. Branch-scope cleanup needs the whole feature branch. If you cannot determine the base, ask.

### 2. Check authorship before removing anything

For each candidate removal:

```bash
git blame -L <start>,<end> -- <file>
```

**Only remove lines whose commit is on the current feature branch (after `$BASE`).** Lines predating the branch are human-authored. Leave them alone, even if they look slop-like.

### 3. Respect the design vs. style boundary

You are removing **low-value tokens within a chosen design**. You are not redesigning.

| In scope | Out of scope |
|---|---|
| Restating-the-code comments | Whether a builder/factory pattern is justified |
| Type-system-redundant runtime guards | Whether the function should exist at all |
| Reflowed loops with no behavior change | Whether the data model is right |
| `IMPORTANT:`-style emphasis on trivia | Whether the public API is too wide |

If you find yourself wanting to redesign, **stop and flag it**. Do not silently rewrite.

## Never touch

- Comments explaining **why** (business reason, workaround, non-obvious constraint)
- Defensive checks at **public API boundaries** or on **external/untrusted input**
- Lines predating the feature branch (per rule 2)
- Test code

## Procedure

1. Resolve `$BASE` (rule 1).
2. `git diff "$BASE"...HEAD` — read the full branch diff.
3. For each candidate removal, run `git blame` on the line range. Confirm every candidate is branch-authored (rule 2).
4. **Preview before applying.** Group candidates by file and list each one: the line(s), the slop category, and the blame evidence. Do not edit yet.
5. **Approval gate.** Show the preview and get explicit confirmation before removing anything. If the user says "just do it," still state the removal count and categories, then proceed only on explicit confirmation. A removal the user cannot see coming is a wrong removal.
6. Apply removals with Edit. Do not rewrite logic.
7. **Verify after cleanup.** Removing code changes behavior, so confirm it did not break anything:
   - Re-run the project linter on touched paths.
   - Run a focused test on touched paths (or the smallest meaningful command). If none exist, say so.
   - If a removed line turns out load-bearing (a test fails, lint errors), revert that removal and report it — it was not slop.
   - Optionally load `quality-reviewer` for a focused pass on the cleaned diff.
8. `git diff "$BASE" --stat` to confirm the final shape, including the
   uncommitted cleanup. Do not use `git diff "$BASE"...HEAD --stat` here: the
   `...HEAD` form stops at the committed branch tip and omits edits just made
   in the working tree.
9. Report: categories removed, design concerns flagged but not touched, verification results, and final stat.

## Common Mistakes

- Applying removals without showing a preview first. The user cannot catch a wrong removal after the edit.
- Treating a redundant-looking guard as slop when it protects a dynamic call path or external input. Verify with tests, not intuition — a failed test means revert.
- Cleaning up merge-commit deltas. `git diff "$BASE"...HEAD` on a branch with merges from main includes their noise; if the branch has merges, scope to feature-branch commits only.
- Running cleanup without verifying afterward. Removing code changes behavior; confirm with lint and tests before claiming done.
- Removing lines predating the feature branch. `git blame` is the authority, not your sense of style.

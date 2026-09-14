---
name: diff-cleanup
description: Clean an existing diff of AI-generated bloat, redundant comments, needless abstractions, or overcomplication. Use when the user asks to remove AI slop or simplify the diff.
---

# Diff Cleanup

Remove low-value code and prose within the user's chosen design. Apply
[Change Boundaries](references/change-boundaries.md) for scope/base resolution,
change ownership, authorization, and verification results.

## Scope and Attribution

Start with status and the explicit target. Cover committed branch changes and
intended staged, unstaged, and untracked changes when the user is still working
on the feature. State exclusions. Do not use `...HEAD` alone for that scope or
fall back to `HEAD~1` when the integration base is unknown.

For each removal, inspect the surrounding code and its baseline/current diff.
Use `git blame -L <start>,<end> -- <file>` for committed provenance and the staged,
unstaged, or untracked content for pending work. Record why the candidate belongs
to the authorized change. Blame cannot establish human/AI authorship, and a
post-base commit is not blanket permission to edit another contributor's work.
Do not alter unrelated pending content or staging.

## Design Boundary

| In scope | Requires a design decision |
|---|---|
| Comments that only restate code | Replacing a builder/factory pattern |
| Guards already enforced by the type system | Removing a public API or changing its contract |
| Mechanical simplification with unchanged behavior | Changing the data model or responsibility owner |
| Emphasis on trivia | Adding a new execution or completion path |

Explain verified design concerns separately. If the user already authorized a
structural fix, route that work through `quality-reviewer` fix mode or the
explicitly requested `loopfix`; do not disguise it as token cleanup. Otherwise
report the decision needed and continue independent authorized cleanup.

## Preserve

- Explanations of business rationale, workarounds, or non-obvious constraints.
- Checks at public boundaries or on external input unless redundancy is proven
  within the authorized scope.
- Baseline and unrelated changes, including other contributors' work.
- Test code; use tests to verify cleanup, not as cleanup targets.

## Procedure

1. Resolve scope/base and inventory all intended changes using Change Boundaries.
2. Read the full candidate files and identify removals with provenance evidence.
3. Preview candidates grouped by file: location, category, ownership evidence,
   and why behavior is unchanged. In report-only mode, stop at the preview.
4. When reversible cleanup is already authorized, apply those candidates without
   asking again. For unclear ownership or unapproved design changes, ask only
   about the unresolved subset. Never infer authorization from urgency alone.
5. Run applicable lint and the smallest meaningful tests, honoring explicit skips.
   Classify baseline failures separately. If a removal breaks a previously
   passing check, undo only that removal and report why it was load-bearing.
6. Inspect the final diff and staging state. For combined scope, show
   `git diff <merge-base> --stat` plus intended untracked paths; this statistic
   includes tracked working changes but does not count untracked files.
7. Report removed categories, preserved exclusions, unresolved design concerns,
   actual verification results, and final scope. Do not claim verification of
   excluded files or call a skipped/blocked check passed.

## Common Mistakes

- Inspecting only committed changes while the user is simplifying pending work.
- Guessing the integration base from the last commit or a tracking feature branch.
- Treating commit ancestry as authorship or approval.
- Removing a guard on intuition without checking the dynamic call path.
- Repeating an approval question after the user authorized the exact cleanup.
- Fixing unrelated baseline failures to obtain an apparently green report.

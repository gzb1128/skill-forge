# Verification Results

Use when a quality workflow executes or reports checks. Prefer the repository's
smallest meaningful permitted checks. Carry explicit skip instructions through
delegation; urgency alone is not a skip. Never execute an explicitly skipped
check or report it as passed. Classify each result against the current candidate:

| Result | Evidence and action |
|---|---|
| Passed | Record the command and current candidate it checked. |
| Change-induced failure | Fix in-scope failures when authorized, then re-check the changed candidate. |
| Pre-existing failure | Run the same command on a clean base with comparable tooling/inputs, or cite an applicable verified baseline. Preserve the failure and keep unrelated fixes out of scope. |
| Unavailable | Name the environment/tool blocker and the resulting coverage gap. No passing claim. |
| Explicitly skipped | Record the user's instruction and the unverified behavior. |

A baseline failure is nonblocking only when repository policy or explicit user
acceptance permits it. Show the comparison and any focused passing checks; do
not automatically waive every failure with a familiar message. If a clean-base
comparison is unsafe/unavailable, label the attribution unverified. Use an
isolated worktree or snapshot; never stash/reset another task's pending work.


After edits, refresh affected checks as required by the calling skill; an earlier
result does not verify later edits. The calling workflow owns its review,
readiness, commit, or loop-completion decision.

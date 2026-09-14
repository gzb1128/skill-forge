# Change Boundaries

Shared by review, cleanup, commit, and fix loops. Repository instructions and
explicit user scope/authorization take precedence. Load only the sections used
by the current workflow; this reference does not authorize additional work.

## Scope and Base

1. Inventory `git status --short`, staged and unstaged diffs, and untracked
   filenames before selecting candidates. Attribute unrelated pending work and
   preserve it, including its staging state.
2. State the scope: working tree, branch, or both. Commit reviews cover the exact
   intended commit; cleanup during an unfinished feature normally covers both.
3. Resolve the integration target from the explicit user/MR target, repository
   convention, or verified integration upstream. A tracking feature branch is
   not its own integration base. Only then consider conventional local or
   remote `main`/`master` refs. If ambiguous, ask; do not guess `HEAD~1`.
4. For branch scope record the target ref and `git merge-base HEAD <target>`.
   If fetching is needed and fails, report that cached refs may be stale; do not
   silently substitute a different target or imply they were refreshed.
5. Read committed changes with `git diff <merge-base>...HEAD`, staged changes
   with `git diff --cached`, and unstaged changes with `git diff`. Read intended
   untracked files separately. `git diff <merge-base>` shows the combined tracked
   result but cannot substitute for inventory, untracked reads, or attribution.

Use blame/history to distinguish baseline from changed lines, not human from
AI authorship. Commits after the base can include other contributors' work;
uncommitted lines have no commit. Authorization and task ownership decide which
pending changes may be edited. Preserve baseline code unless changing it is
explicitly in scope; flag unclear ownership before removing anything.

## Architecture and Existing Flow

Apply when a change crosses module boundaries or changes parsing, persistence,
state machines, or execution paths. Before implementing in a fix loop, and when
reviewing a candidate, trace the real entrypoint through the relevant owners.
Keep the evidence short and tied to source symbols or a living contract:

- What does the existing flow already support, and where does it first fail the
  requested outcome?
- Who owns input interpretation, business decisions, durable effects, and state
  transitions? Trace only the responsibilities this change touches.
- Does a new branch, cross-layer flag, public parameter, or completion shortcut
  express a missing capability, or bypass an owner that already handles it?
- What happens to admission, identity, failure, retry, and recovery on that path?

A concrete ownership violation introduced by this change is an in-scope finding,
not optional architecture polish. Cite the violated contract or bypassed behavior.
Do not demand a refactor or a new diagram merely because another design is nicer.
If existing abstractions genuinely cannot express the requirement, explain that
specific gap; changes to ownership need authorized scope and matching contract
updates. Pure wording or local mechanical edits do not need this trace.

## Authorization and Verification

Honor explicit report-only, fix, commit, and skip instructions across nested
skills. Existing authorization for a concrete scope remains valid. A preview
makes reversible edits reviewable; it does not require asking again when those
edits are already authorized. Ask only for unresolved ownership, a design/product
decision, or an action outside the authorized scope. Urgency alone is not a skip;
explicit `skip tests`, `skip lint`, or `skip review` is. State skipped checks and
remaining uncertainty; do not run the skipped check anyway or label it passed.
`just commit` skips review/test/lint gates, but not checking the intended files
for secrets and accidental debug content, and never bypasses commit hooks.

Use the repository's smallest meaningful checks and report each result:

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

Readiness requires no unresolved Important/Critical current-scope findings and
all unwaived required checks satisfied. A required unavailable check still blocks.
Nonblocking baseline failures and explicit waivers remain visible in the final
verdict. If fixes change the candidate, refresh affected verification and review
as required by the calling skill; an earlier verdict does not cover later edits.

# Git Change Scope

Use when selecting a review, cleanup, commit, or fix-loop diff. The calling
workflow determines the authorized scope; this procedure only resolves its Git
representation. Preserve unrelated work and its staging state.

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

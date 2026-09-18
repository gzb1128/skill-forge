---
name: clean-commit
description: Review, stage, and commit local changes. Use only when the user explicitly asks to create a commit.
---

# Clean Commit

Run `quality-reviewer` on the exact intended commit, then commit with a message
that explains business impact. Carry the user's scope, fix authorization, and
explicit skip flags into the delegated workflow. Existing commit authorization
needs no repeat approval; ask only about unresolved ownership or a decision beyond
that scope. These boundaries apply without prior repository-rule setup.

## Workflow

1. **Inspect the intended commit** — use [Git Change Scope](references/git-change-scope.md) to inventory staged, unstaged, and untracked changes. Distinguish the pending commit from already-committed branch work; review exactly the candidate the user authorized.
2. **Run quality gates** — load `quality-reviewer` and follow its full procedure (one independent reviewer, integrated checks, diff hygiene, lint, tests, caller check). Its `Verdict` line tells you whether you may proceed.
3. **Resolve current-scope failures.** Use reviewer fix mode for safe fixes implied by the commit request; do not silently change ambiguous contracts or fix unrelated baseline failures. After edits, refresh affected checks and the focused review before using its verdict. Use [Verification Results](references/verification-results.md); do not treat a known baseline failure as a passing suite.
4. **Stage only the intended candidate** — inspect paths and hunks before staging; never use `git add .` blindly. Preserve unrelated work and its index state. If unrelated changes are already staged, isolate the commit without consuming or unstaging them; if ownership cannot be separated safely, resolve that subset before committing. Inspect the exact commit diff (normally `git diff --cached`, or the isolated index) for accidental files, secrets, and debug content. It must match the reviewed candidate; refresh affected review/checks if it changed.
5. **Compose the commit message** (see rules below).
6. **Commit** — `git commit -m "<message>"`.
7. **Verify the result** — inspect `git log -1 --stat` and the committed patch, then confirm remaining work and unrelated staging are preserved. Report actual checks and explicit skips; do not push unless requested.

## Commit Message Rules

| Rule | Detail |
|------|--------|
| Scope prefix | `<scope>: <subject>` (e.g., `api:`, `docs:`, `ci:`, `fix:`, `test:`) |
| Subject mood | Imperative, lowercase after colon |
| Subject length | ≤ 72 characters |
| Body (optional) | Wrap at 72 cols, explain WHY, not WHAT |
| Reference issues | `Refs #123` or `Closes #123` in the body |

**Good:**
- `api: reduce listing endpoint p99 from 3s to 400ms`
- `docs: split AGENTS.md into per-component codemaps`

**Bad:**
- `Update files` (vague)
- `fixed bug` (no scope, no impact)
- `refactor: improved code quality` (says nothing)
- A 200-char subject line

## Skip Flags

User can skip gates explicitly. These map to the `quality-reviewer` gate names:
- `skip review` → skip code-review analysis, including the independent reviewer
- `skip lint` → skip the linter
- `skip tests` → skip the test gate
- `just commit` → stage + commit, no gates

If the user says "just commit", still inspect the intended diff for secrets / debug prints and preserve unrelated staging. Skip flags do not bypass commit hooks or turn skipped checks into passes.

## Hard Rules

- Never commit secrets, API keys, `.env` files, or generated debug logs
- Never use `git commit --amend` or `git push --force` unless the user asks
- Never bypass hooks (`--no-verify`) without explicit permission
- If a commit hook rejects: fix the issue and make a new commit, don't amend

---
name: clean-commit
description: Use when about to commit code changes, when the user says "commit", "commit this", or after finishing a feature/bugfix and changes are ready to land. Ensures quality gates pass before producing a scoped commit message that explains WHY (business impact), not WHAT (code changes)
---

# Clean Commit

Run the `quality-reviewer` skill on the current diff, then commit with a message that explains business impact.

## Workflow

1. **Inspect changes** — `git status`, `git diff`, `git log --oneline -10`
2. **Run quality gates** — load `quality-reviewer` and follow its full procedure (one independent reviewer, integrated checks, diff hygiene, lint, tests, caller check). Its `Verdict` line tells you whether you may proceed.
3. **Fix anything that fails.** Do NOT commit on failed gates unless the user explicitly says "skip <gate>" or "just commit".
4. **Stage only intended files** — never `git add .` blindly. Inspect each path.
5. **Compose the commit message** (see rules below).
6. **Commit** — `git commit -m "<message>"`.
7. **Show the result** — `git log -1 --stat`.

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

If the user says "just commit", still inspect the diff for secrets / debug prints before committing.

## Hard Rules

- Never commit secrets, API keys, `.env` files, or generated debug logs
- Never use `git commit --amend` or `git push --force` unless the user asks
- Never bypass hooks (`--no-verify`) without explicit permission
- If a commit hook rejects: fix the issue and make a new commit, don't amend

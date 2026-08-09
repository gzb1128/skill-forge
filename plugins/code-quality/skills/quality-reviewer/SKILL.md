---
name: quality-reviewer
description: Review local changes for correctness, scope, tests, and maintainability, optionally fixing findings. Use for explicit quality-review requests before commit or merge; not for remote PR/MR review.
---

# Quality Reviewer

Review local changes with exactly one fresh-context reviewer. The independent review counters the main agent's optimism about code it just authored without making every review lens reload the same context. Do not commit. Default to report-only unless the user explicitly asks to fix.

## Modes

| User wording | Mode | Edits? |
|---|---|---|
| "review", "quality review", "ready to commit" | **Report-only** | No |
| "quality review and fix", "fix review findings" | **Fix safe issues** | Safe in-scope fixes only |
| "loopfix", "review-fix-review loop", "keep fixing" | **Loopfix** | Load `loopfix` and stop this bounded procedure |

A safe fix is localized and behavior-preserving, or explicitly required by the user, `AGENTS.md`, a design doc, or an existing test. Do not guess intent for authorization, data-loss, API-contract, migration, security, or product findings. If fix intent is ambiguous, ask before editing.

## Workflow

### 1. Declare mode and scope

State the mode and whether the review covers the working tree, branch diff, or both:

- Working tree: `git diff`, `git diff --cached`, and untracked files from `git status --short`.
- Branch: `git diff <base>...HEAD`.
- Both: inspect and label both sources.

Resolve `<base>` from `origin/main`, `origin/master`, `main`, then `master`, using the first ref with a merge base. Honor an explicit user scope. Read repository instructions and the full changed files; diffs alone are not enough. Review only behavior introduced by the change.

### 2. Dispatch exactly one independent reviewer

When Task is available, the primary agent dispatches **exactly one** reviewer subagent. Do not create separate correctness, simplification, efficiency, lens, or gate agents.

If the prompt explicitly identifies you as that reviewer, perform the integrated review yourself and do not dispatch a nested reviewer.

Give the reviewer:

- an explicit designation as the single independent reviewer, with instructions to load `quality-reviewer` in reviewer role and never dispatch nested reviewers
- the exact user request and acceptance criteria
- the working directory, resolved scope, and base ref
- paths to relevant `AGENTS.md`, plans, and design docs
- instructions to inspect the diff, untracked files, and full changed files without editing, apply the integrated rubric and triggered lenses, and return only reviewer candidates

Do not include the main agent's self-review, implementation defense, or conclusions. Point at repository files instead of pasting large contents when the reviewer can read them.

The reviewer returns only candidate findings with `file:line`, severity, confidence, realistic failure scenario, and evidence, followed by the conditional lenses it applied. If it finds nothing, it says so directly.

If Task is unavailable, report `Independent reviewer: unavailable` and stop without reviewing. Do not substitute the main agent's self-review; the only permitted readiness verdict is `Ready to commit: no` because the required review did not occur.

### 3. Use one integrated rubric

The single reviewer uses one shared understanding of the task for all applicable checks:

| Check | When | Question |
|---|---|---|
| **Correctness and behavior** | Always | Check logic, edge cases, error paths, security, broken invariants, caller-owned mutation, API/behavior changes, and missing tests. |
| **Structure and simplification** | Always | Does it fit existing patterns? Is there concrete complexity, duplication, dead code, or a hand-rolled utility to remove? |
| **Efficiency** | Always | Is there an obvious N+1 call, repeated hot-path I/O, unbounded growth, leaked resource, or redundant write? |
| **Silent failure** | Error handling, fallback, retry, ignored error, or log-and-continue changed | Could this hide a failure that a user, caller, operator, or test should see? |
| **Test quality** | Tests changed | Would the tests fail for the important regressions introduced by this diff? |
| **Skill quality** | A `SKILL.md` behavior changed | Will another agent reliably trigger and follow it, and is there RED/GREEN evidence? |
| **Comment accuracy** | Comments or docstrings changed | Do they still match the code, signature, and behavior? |

Focus on bugs and behavior. Flag structure or performance only when there is concrete impact; do not report taste, hypothetical problems, or micro-optimizations. These checks are questions inside one review, never reasons to launch more agents.

### 4. Run gates directly

The primary agent runs `git diff --check`, lint, and relevant tests with direct tools while the reviewer works when concurrency is available. Prefer commands from `AGENTS.md`. The reviewer may run targeted checks to substantiate a finding but does not repeat the primary's full gates. Never create separate Task agents for mechanical commands, and name any unavailable gate.

For each public symbol whose signature, return shape, or error contract changed, run:

```bash
git grep -n '<symbol>' -- ':!vendor' ':!node_modules'
```

When the user asks to skip tests because they are slow, run a focused subset first; if it finishes within 30 seconds, run it anyway and report the runtime. Honor an explicit `skip lint`. Urgency alone does not skip gates, and any blocking verdict must include a concrete next step that takes under two minutes.

### 5. Validate findings with evidence

Merge the reviewer's candidates with anything the main agent noticed, then:

1. Re-open the current source lines and drop stale findings.
2. Validate against the user request, contracts, docs, tests, callers, and existing repository patterns.
3. Report only findings with confidence **≥ 80**.
4. Suppress pre-existing issues, linter-catchable issues, style-only preferences, explicitly accepted behavior, and "could be more elegant" commentary.

The main agent is not automatically ground truth about code it authored. Reject a reviewer finding only with concrete evidence, not implementation intent or confidence in its own work. If the reviewer marks a candidate Critical or Important and the main agent rejects or downgrades it, preserve the disagreement and evidence in the report.

### 6. Fix and re-check only when requested

In fix mode, apply only validated safe fixes. After any edit, re-read the touched diff, check for new correctness, structure, or efficiency issues, and rerun the smallest relevant gate. This focused check does not launch another reviewer; use `loopfix` for repeated independent review cycles.

### 7. Report the verdict

Omit empty optional sections:

```text
### Fixed
- <file>:<line> — change and reason

### Flagged (not fixed)
- <file>:<line> — issue; severity; confidence; realistic trigger; why not fixed

### Reviewer disagreements
- <file>:<line> — reviewer assessment; final disposition; concrete evidence

### Gates
- Mode and scope: <mode>; <scope> via <commands>
- Independent reviewer: <one dispatched / designated reviewer / unavailable> → <result>
- Coverage: <always-on checks>; lenses: <triggered / none>
- Diff hygiene / lint / tests: <commands and results>
- Caller check: <symbols and result / not triggered>
- Post-fix check: <result / not needed>

### Verdict
Ready to commit: <yes / no / yes-after-flags-resolved>
If no: <one concrete next step taking under two minutes>
```

`Ready to commit: no` is required when the independent reviewer was unavailable, a required gate failed, or an unresolved Critical/Important finding remains. Use `yes-after-flags-resolved` only for unresolved Minor findings or explicitly accepted non-blocking follow-ups.

## Never

- Spawn nested reviewers or more than one reviewer subagent in a bounded review.
- Prime the reviewer with the main agent's conclusions.
- Copy or dismiss reviewer findings without checking current source and evidence.
- Edit in report-only mode or bless ambiguous behavior by adding tests.
- Skip a gate silently or treat urgency as permission to skip it.
- Mark changes ready while required review, gates, or Critical/Important findings remain unresolved.

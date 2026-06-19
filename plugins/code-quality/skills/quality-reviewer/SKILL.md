---
name: quality-reviewer
description: Use when local code changes need a quality pass before commit, before opening a PR, or before claiming work is complete. Triggers on "review", "quality review", "quality review and fix", "fix review findings", "ready to commit", "check before merge". Do NOT use for remote MR/PR review.
---

# Quality Reviewer

Run a structured quality pass on local changes. Do not commit. Default to report-only unless the user explicitly asks to fix.

You will naturally inspect the diff, detect the toolchain (`go.mod`, `package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`), and decide what to lint and test. The rules below address what baseline testing showed agents skip.

## Review modes

| User wording | Mode | File edits allowed? |
|---|---|---|
| "quality review", "review", "check my changes", "ready to commit" | **Report-only** | No |
| "quality review and fix", "fix review findings", "fix safe issues" | **Fix safe issues** | Yes, for safe in-scope fixes only |
| "loopfix", "review-fix-review loop", "keep fixing" | **Loopfix** | Yes, through the `loopfix` skill |

Report-only means inspect, run gates, and report findings without modifying files. If a safe fix is obvious, list it under `Flagged (not fixed)` and say it can be applied if the user wants.

Safe fixes are mechanical, localized, and either behavior-preserving or explicitly required by the user, `AGENTS.md`, a design doc, or an existing test expectation. Do not resolve ambiguous behavior, authorization, data-loss, API-contract, migration, security, or product findings by guessing intent, changing semantics, or adding tests that merely bless the new behavior.

If the user did not explicitly ask to fix, do not edit files. If intent is ambiguous, ask for confirmation before any edit.

Loopfix is not a bounded quality-review pass. When the user asks for loopfix, load the `loopfix` skill and follow its review-fix-review loop.

## Required behaviors

### 1. Declare review mode and review scope before reviewing

Before reviewing findings, inspect repository state enough to decide and state:

| Item | How to decide |
|---|---|
| **Mode** | Report-only / Fix safe issues / Loopfix, from the table above |
| **Scope** | Working tree, branch diff, or both |

Scope rules:

| Local state | Review this |
|---|---|
| Uncommitted changes only | Working tree diff: `git diff`, `git diff --cached`, and untracked files from `git status --short` |
| Feature-branch commits only | Branch diff: `git diff <base>...HEAD` (`main..HEAD` intent) |
| Both committed branch changes and uncommitted changes | Both; label findings as branch or working-tree |

Resolve `<base>` with `git merge-base HEAD origin/main`, `origin/master`, `main`, or `master`, using the first one that exists. If the user explicitly limits scope, honor that scope and say so in the report.

### 2. Run the review in three independent passes - not one linear scan

Baseline testing showed a single-pass review misses correctness issues that a focused pass would catch. Run three reviews against the diff, each with one question only:

| Pass | Single question to ask the diff |
|---|---|
| **Simplify** | What unnecessary complexity, duplication, dead code, or hand-rolled utility could be removed without changing behavior? |
| **Correctness** | Where could this be wrong? Edge cases, error paths, narrowed failure tolerance, mutation of caller-owned data, broken invariants, missing tests for new branches. |
| **Efficiency** | Where does this do more work than needed? N+1 calls, repeated I/O on hot paths, unbounded growth, leaked goroutines/handles, redundant writes. |

If the Task tool is available, dispatch the three passes in parallel as subagents, and include any triggered conditional lenses (rule 2a) in the **same batch**. Otherwise do them inline as separate read-throughs of the diff with the question above held in mind. **Do not collapse into one pass, and do not run triggered lenses after the three passes — they join the batch.**

### 2a. Run conditional lenses when the diff triggers them

Some diffs need a focused lens beyond the three standard passes. Run only the lenses that match the changed files or hunks:

| Trigger | Lens | Single question |
|---|---|---|
| Added or changed `catch`/`except`/`rescue`, fallback/default behavior, retries, ignored errors, optional chaining on required data, or log-and-continue handling | **Silent failure** | Could this hide a failure that the user, caller, operator, or test should see? |
| Added or changed tests for new logic, validation, error paths, contracts, or branches | **Test quality** | Would these tests fail for the important regressions this diff could introduce? |
| Changed `plugins/*/skills/*/SKILL.md` or any `SKILL.md` beyond spelling/formatting-only edits | **Skill quality** | Will another agent reliably trigger and follow this skill under pressure? |
| Added or changed comments, docstrings, or inline docs beyond trivial formatting | **Comment accuracy** | Does the comment still match the code, or has it rotted into a lie? |

Silent-failure findings should check whether the error is specific, visible, logged with useful context, propagated when needed, and whether fallback behavior is intentional rather than masking a broken path.

Test-quality findings should focus on behavior, not line coverage. Passing tests are not enough if assertions only exercise implementation details, bless the new behavior without proving the contract, or skip negative/error cases introduced by the diff.

Skill-quality findings should check frontmatter trigger quality, especially whether `description` describes when to use the skill rather than summarizing the workflow. Also check for vague triggers, missing common-mistake guidance for discipline skills, one-off narrative content, broken references, and missing RED/GREEN verification evidence when skill behavior changed. Treat trigger changes, workflow changes, new/removed rules, tool-scope changes, and changed stop/approval conditions as behavior changes; spelling-only or formatting-only edits do not trigger this lens.

Comment-accuracy findings should check that comments describe current behavior, not a previous version of the code; that docstrings match signatures and return shapes; and that `TODO`/`FIXME` markers reference real follow-ups. A comment that contradicts the code is worse than no comment — flag it as at least Important.

Triggered lenses are review passes, just conditional ones. Dispatch them in the same parallel batch as Simplify/Correctness/Efficiency (rule 2), not as a separate sequential step. Evaluate triggers first, then launch 3-7 passes in one batch.

### 2b. Run mechanical gates concurrent with the review

Diff hygiene (`git diff --check`), lint, and tests depend only on **which files changed**, not on review findings. Run them in the same time window as the review passes (rule 2) and conditional lenses (rule 2a), not after. If the Task tool is available, dispatch them as additional parallel subagents alongside the review batch.

Two gates are NOT mechanical and must wait for the review to finish:
- **Caller grep** (rule 3) — consumes the list of changed-contract symbols from the review.
- **Finding validation** (rule 5) — consumes findings from the passes and lenses, and the rule-3 caller-grep results (used by Filter 1's context cross-validation).

### 3. Grep for callers of changed public symbols

Before claiming the diff is safe, for each public function/method/exported symbol whose **signature, return shape, or error contract changed**:

```bash
git grep -n '<symbol>' -- ':!vendor' ':!node_modules'
```

Baseline testing: agents flagged correctness risks ("might break callers") without ever checking whether callers exist. Either the risk is real (callers must change) or it isn't (no callers). Find out which.

### 4. Verify "skip" claims before honoring them

The user can skip gates explicitly. But verify the skip is justified before complying.

| User says | Before honoring, verify |
|---|---|
| "skip tests, they take too long" | Run a fast subset (`-run`/`--testPathPattern`/single file). If the affected suite finishes in < 30s, run it anyway and tell the user. |
| "skip lint" | Honor it. Lint is taste; tests are correctness. |
| "production is down, just commit" | Refusing to commit is incomplete. Pair every refusal with a concrete next step the user can take in <2 minutes (revert SHA, minimal diff, what bug to confirm). |

### 5. Validate and filter findings before reporting

Reviewer passes produce raw findings. Before any finding reaches the report, it must pass three independent filters. Each filter removes findings; survivors are reported.

**Filter 1 — Source-line and context cross-validation.** Reviewer subagents are advisors, not ground truth. This filter has two steps:

1. **Source-line check.** Open the current source lines or current diff hunk. Confirm the issue still exists at the reported location. Drop stale findings and findings made obsolete by later edits.
2. **Context cross-validation.** The main agent has more context than the subagent — the full diff, the stated intent, design constraints, the rule-3 caller-grep results, and prior accepted decisions elsewhere in the diff. Judge whether the reported issue is a genuine defect against that fuller context. Findings that misread the code's intent, ignore a valid caller/usage pattern, duplicate a constraint already satisfied elsewhere in the diff, or rest on a code reading the main agent cannot reproduce must be downgraded or suppressed (moved to `Suppressed (low confidence)` with the reason).

**Principle:** The main agent is the ground-truth layer; subagents are advisors. A finding is not real just because a subagent reported it — it is real only if the main agent can independently confirm the defect against its fuller context. Source-line existence is a prerequisite, not proof of defect reality.

**Filter 2 — Confidence scoring.** Score each surviving finding 0-100 for "how certain am I this is a real defect introduced by this diff?" Only report findings scored **≥ 80**. Confidence is orthogonal to severity: a low-confidence Critical is still suppressed. Severity says *how bad*; confidence says *how real*. If you suppress a high-severity finding for low confidence, list it under `Suppressed (low confidence)` with the score and a one-line reason so the user can investigate.

**Filter 3 — False-positive suppression.** Do not report these categories regardless of confidence score:

| Suppressed category | How to confirm it is not new |
|---|---|
| Pre-existing issue not introduced by this diff | Check the branch diff or `git blame` — the line predates the change |
| Issue a linter/formatter would already flag at the same location | The tool is configured and runs in this repo |
| Pedantic style nitpick with no correctness or maintainability impact | Pure taste, not a defect |
| Issue the diff explicitly addresses or the user explicitly accepted | Stated intent or skip flag |
| "Could be more elegant" commentary that is not a concrete defect | No observable wrong behavior |

A finding must survive all three filters to appear in the report. A high-confidence Critical that survives suppression blocks the commit; a Minor that survives is flagged but does not block.

### 6. Re-review after any fix

If fix mode is active and you edit files, run a focused re-review after the edit before reporting success:

1. Re-read the updated diff/source lines touched by the fix.
2. Check whether the fix created a new correctness, simplification, or efficiency issue.
3. Re-run the smallest relevant lint/test gate if behavior, syntax, imports, or contracts changed.

This applies even for one safe fix. It is a focused post-fix review, not a full loopfix cycle unless the user asked for loopfix.

### 7. Important findings block ready-to-commit verdicts

Tests passing is not enough. If any unresolved `Critical` or `Important` finding remains, `Ready to commit` must be `no`. An Important finding is resolved only by a safe fix with clear intent evidence, not by adding tests that bless ambiguous behavior. Use `yes` only when required gates pass and no unresolved Critical/Important findings remain. Use `yes-after-flags-resolved` only for unresolved Minor findings or explicitly accepted non-blocking follow-ups.

## Standard procedure

1. **Select mode and scope** (rule 1). If mode is Loopfix, load `loopfix` and stop this bounded procedure.
2. **Scope the diff.** `git status`, `git diff --stat`, `git diff`, `git diff --cached`, untracked files from `git status --short`, and branch diff when scope includes branch changes. If empty, say so and stop.
3. **Detect toolchain.** Probe project files. If `AGENTS.md` declares lint/test commands, prefer those.
4. **Review + lenses in parallel** (rules 2, 2a). Dispatch the three standard passes and any triggered conditional lenses in one parallel batch. In report-only mode, do not edit. In fix mode, apply only safe in-scope fixes and flag the rest.
5. **Mechanical gates concurrent with review** (rule 2b). Diff hygiene (`git diff --check`), lint, and tests can run in the same window as step 4 — they depend only on changed paths, not on findings. If the Task tool is unavailable, run them after the review passes. Note the test-quality lens still applies when tests were added/changed (step 4), before treating passing tests as sufficient.
6. **Post-fix re-review** (rule 6) if any file was edited.
7. **Caller check** (rule 3) for any changed public symbol. Runs after the review because it consumes the list of changed-contract symbols.
8. **Validate findings** (rule 5): cross-validate each finding against current source lines AND the main agent's fuller context (intent, design, caller usage from rule 3, prior accepted decisions). Runs after the review because it consumes findings from the passes and lenses, and after the caller check because Filter 1 reuses its results.
9. **Report** in the structure below. Do not freeform-narrate.

## Report format (use these headings)

```
### Fixed
- <file>:<line> — what changed and why

### Flagged (not fixed)
- <file>:<line> — issue, severity (Critical/Important/Minor), confidence (0-100), why not auto-fixed

### Suppressed (low confidence)
- <file>:<line> — issue, severity, confidence score, one-line reason for suppression

### Gates
- Mode: <report-only / fix safe issues / loopfix>
- Scope: <working tree / branch diff / both> via <commands>
- Three-pass review: <pass/issues found>
- Conditional lenses: <not triggered / silent failure / test quality / skill quality / comment accuracy results>
- Post-fix re-review: <not needed / pass / findings>
- Diff hygiene: <pass/fail>
- Lint: <command run> → <pass/fail/unavailable>
- Tests: <command run> → <pass/fail/none-exist>
- Caller check: <symbols checked> → <findings>
- Finding validation: <findings cross-validated / stale dropped / context-blind downgrades / suppressed count>

### Verdict
Ready to commit: <yes / no / yes-after-flags-resolved>
If no: one concrete next step the user can take in <2 minutes.
```

## Common Mistakes

- Collapsing the three review passes into one broad scan. Keep Simplify, Correctness, and Efficiency separate.
- Running triggered conditional lenses sequentially after the three passes. They join the parallel review batch.
- Serializing mechanical gates (diff hygiene, lint, tests) behind the review. They depend only on changed paths — run them concurrent with the review passes.
- Reporting a finding without a confidence score. Every reported finding needs a ≥80 score or it belongs under Suppressed.
- Treating severity and confidence as the same axis. A Critical at confidence 50 is suppressed, not blocking; a Minor at confidence 95 is flagged, not blocking.
- Silently dropping a suppressed high-severity finding. Always list it under `Suppressed (low confidence)` with the score and reason.
- Treating passing tests as proof of safety when the test-quality lens was triggered but not run.
- Running the skill-quality or comment-accuracy lens for spelling-only or formatting-only edits. Record them as not triggered instead.
- Marking a diff ready while Important findings remain because validation commands passed.
- Copying subagent findings into the report without re-opening current source lines.
- Accepting a subagent finding because it sounds right without judging it against the main agent's context (intent, callers, prior decisions). Source-line existence ≠ defect reality.

## Never

- Skip a gate silently. If a tool is unavailable, name it and say so.
- Edit files in report-only mode or before explicit confirmation to fix.
- Refuse to commit without offering a concrete <2-minute next step.
- Report sub-pass or subagent output without cross-validating it against current source lines AND the main agent's fuller context.
- Treat tests that bless ambiguous behavior as a safe fix for an Important finding.
- Treat "I'm tired" / "it's urgent" as permission to skip gates. The user must explicitly name the gate.
- Mark `Ready to commit: yes` when unresolved Critical or Important findings remain.

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

Resolve the intended diff with [Git Change Scope](references/git-change-scope.md). Read repository instructions and the full changed files; diffs alone are not enough. Review only behavior introduced by the change. Report any explicitly skipped review without dispatching a reviewer or implying review occurred.

Honor existing scope, fix authorization, report-only mode, and explicit skips
through delegation. A preview is not a second approval gate for an already
authorized safe fix. Ask only about unresolved ownership, a product/design
decision, or work outside the authorized scope. No repository setup is required
to apply these review boundaries.

### 2. Dispatch exactly one independent reviewer

When Task is available, the primary agent dispatches **exactly one** reviewer subagent. Do not create separate correctness, simplification, efficiency, lens, or gate agents.

If the prompt explicitly identifies you as that reviewer, perform the integrated review yourself and do not dispatch a nested reviewer.

Give the reviewer:

- an explicit designation as the single independent reviewer, with instructions to load `quality-reviewer` in reviewer role and never dispatch nested reviewers
- the exact user request and acceptance criteria
- the working directory, resolved scope, and base ref
- paths to relevant `AGENTS.md`, plans, and design docs
- task-relevant session decisions, including earlier accepted choices and later replacements, as verbatim excerpts or accessible records rather than the primary's interpretation
- instructions to inspect the diff, untracked files, and full changed files without editing, apply the integrated rubric and triggered lenses, and return candidate findings plus API contract changes and superseded session decisions

Do not include the main agent's self-review, implementation defense, or conclusions. Point at repository files instead of pasting large contents when the reviewer can read them.

The reviewer returns candidate findings with `file:line`, severity, confidence, realistic failure scenario, and evidence, followed by the conditional lenses it applied. If it finds nothing, it says so directly. It also returns API contract changes and superseded session decisions as defined below, even when there are no findings.

If Task is unavailable, report `Independent reviewer: unavailable` and stop without reviewing. Do not substitute the main agent's self-review; the only permitted readiness verdict is `Ready to commit: no` because the required review did not occur.

### 3. Use one integrated rubric

The single reviewer uses one shared understanding of the task for all applicable checks:

| Check | When | Question |
|---|---|---|
| **Correctness and behavior** | Always | Check logic, edge cases, error paths, security, broken invariants, caller-owned mutation, API/behavior changes, and missing tests. |
| **Structure and simplification** | Always | Does it fit existing patterns? Is there concrete complexity, duplication, dead code, or a hand-rolled utility to remove? |
| **Architecture and existing flow** | Cross-module, parsing, persistence, state-machine, or execution-path changes | Use the ownership check below. Does the change bypass an existing owner or add an unnecessary path? |
| **Efficiency** | Always | Is there an obvious N+1 call, repeated hot-path I/O, unbounded growth, leaked resource, or redundant write? |
| **Silent failure** | Error handling, fallback, retry, ignored error, or log-and-continue changed | Could this hide a failure that a user, caller, operator, or test should see? |
| **Test quality** | Tests changed | Would the tests fail for the important regressions introduced by this diff? |
| **Skill quality** | A `SKILL.md` behavior changed | Will another agent reliably trigger and follow it, and is there RED/GREEN evidence? |
| **Session decision reconciliation** | A later session decision replaces an earlier accepted choice relevant to the reviewed change | Which earlier decisions and artifacts need retirement under the final decision? |
| **Comment accuracy** | Comments or docstrings changed | Do they still match the code, signature, and behavior? |

Focus on bugs and behavior. Flag structure or performance only when there is concrete impact; do not report taste, hypothetical problems, or micro-optimizations. These checks are questions inside one review, never reasons to launch more agents.

### Ownership check

For the triggered architecture lens, trace the real entry through the owners
relevant to the changed behavior, using source symbols and living contracts:

- What already works, and where does the requested outcome first fail?
- Who owns input interpretation, business decisions, durable effects, and state
  transitions on this path?
- Does a new branch, cross-layer flag, parameter, or completion shortcut express
  a missing capability or bypass an owner that already handles it?
- What happens to admission, identity, failure, retry, and recovery where relevant?

A concrete ownership violation introduced by the change is an in-scope finding,
not optional polish. Cite the violated contract or bypassed behavior. Do not
require a new diagram or refactor because another design is nicer. An actual
change of responsibility needs authorized scope and matching contract updates.
Routine wording and local mechanical edits need no architecture investigation;
review does not require proof that `architect` or `investigate-design-rationale` ran.

### Session decision reconciliation

When the session changes an accepted decision, reconcile the earlier choice with
the final decision and current artifacts. Include relevant code paths, API fields,
tests, configuration, and living documentation even if the residual item is absent
from the latest diff. Keep the check bounded to choices superseded by this task;
do not turn it into a repository-wide retirement audit. An explored alternative
is not an accepted replacement, and compatibility explicitly retained by the
final decision is not obsolete.

Report each superseded choice with the earlier → final decision, supporting
session evidence, affected artifacts, and remaining action. Mark pending cleanup
or status updates **Needs retirement**; mark **Retired** only when removal or an
appropriate superseded marker is verified. Preserve historical decision records
as history rather than deleting them. A superseded proposal with no durable
artifacts can be reported as such. If decision history or completion evidence is
unavailable, state that gap rather than inventing a decision or claiming cleanup.
Reporting retirement work does not authorize edits outside the current fix scope.

### 4. Run gates directly

The primary agent runs `git diff --check`, lint, and relevant tests with direct tools while the reviewer works when concurrency is available. Prefer commands from `AGENTS.md`. The reviewer may run targeted checks to substantiate a finding but does not repeat the primary's full gates. Never create separate Task agents for mechanical commands, and name any unavailable gate.

For each public symbol whose signature, return shape, or error contract changed, run:

```bash
git grep -n '<symbol>' -- ':!vendor' ':!node_modules'
```

Also inspect the actual external contract: endpoint/schema and serialized request
or response changes may not alter a public symbol's signature. Check affected
callers against field names, nesting, requiredness, defaults, and error semantics.
Local caller checks do not establish compatibility with uninspected external
consumers; keep that coverage gap explicit.

Classify checks using [Verification Results](references/verification-results.md). Respect explicit skips even when a check would be quick. Give a concrete next diagnostic or decision for a blocking verdict; do not promise an arbitrary duration.

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

When the diff introduces or changes an externally consumed API, proactively
include an API contract change summary even if the change is compatible,
authorized, and has no findings. Show the before → after shape: for HTTP/RPC,
identify the endpoint or operation and include concrete request and response
bodies for affected sides, stating when a side is unchanged or has no body.
Preserve enough envelope and nesting to locate changed fields. Use annotated
examples (such as `jsonc` for JSON) with comments beside additions, removals,
moves, and semantic changes, including requiredness, defaults, and omitted versus
null values where relevant. Show removed fields in the old body or explicit
removal comments and representative variants for conditional contracts. For
library APIs, use annotated signatures and caller examples. Mark new or removed
APIs explicitly rather than inventing an old or new body. Explain the reason,
affected consumers, compatibility or migration implications, and verified versus
unverified consumer coverage. Report the final reviewed shape after any fixes.
These are contract facts; classify them as findings only when evidence establishes
a defect. Private implementation-only changes do not trigger this summary.

Omit empty optional sections:

```text
### API contract changes
- <endpoint/operation/symbol> — annotated before → after examples and consumer impact

### Superseded session decisions
- <earlier → final decision> — evidence; affected artifacts; Needs retirement / Retired / superseded proposal only; remaining action or verification gap

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
- Diff hygiene / lint / tests: <commands and classified results, including baseline evidence and explicit skips>
- Caller check: <symbols and result / not triggered>
- Post-fix check: <result / not needed>

### Verdict
Ready to commit: <yes / no / yes-after-flags-resolved>
If no: <one concrete next diagnostic or required decision>
```

`Ready to commit: no` is required when an unwaived independent review or required gate is unavailable/failed, or an unresolved Critical/Important finding remains. Explicit skips and repository-approved nonblocking baseline failures must be reported separately, never as passing checks. Use `yes-after-flags-resolved` only for unresolved Minor findings or explicitly accepted non-blocking follow-ups.

## Never

- Spawn nested reviewers or more than one reviewer subagent in a bounded review.
- Prime the reviewer with the main agent's conclusions.
- Copy or dismiss reviewer findings without checking current source and evidence.
- Edit in report-only mode or bless ambiguous behavior by adding tests.
- Skip a gate silently or treat urgency as permission to skip it.
- Mark changes ready while required review, gates, or Critical/Important findings remain unresolved.

---
name: loopfix
description: Run an autonomous review-fix loop for an approved goal until current-scope findings are resolved. Use only for explicit loopfix, review-fix loop, or keep-fixing requests.
---

# Loopfix

## Overview

Loopfix is an autonomous work-review-fix loop for the current approved goal. The main agent owns triage and momentum: reviewer subagents advise, but the main agent decides what to fix now, what to reject, and what to defer for final human audit.

**Core rule:** meaningful in-scope changes reset the loop. Do not finish until a reviewer pass after the latest meaningful change finds no unresolved current-goal issue, verification is fresh, and the runtime-neutral completion criteria are satisfied.

Completion is an evidence-backed judgment by the main agent, not a hook, state file, forced re-prompt, or arbitrary iteration count. Do not add runtime-specific loop mechanisms. Continue only when an in-scope issue remains.

**Iteration budget.** If the loop reaches **5 iterations** on the same goal without converging — the same class of issue keeps recurring, or fixes are not reducing the reviewer's findings — stop, report the stall, and ask the user. A loop that disagrees with its reviewer forever is a signal to surface the conflict, not to grind. When you stop, summarize: how many iterations ran, what the recurring issue is, what you have tried, and why you cannot resolve it without a human decision.

## Completion Criteria

Before the first fix, define a short checklist for this run with all five fields:

| Criterion | What to state |
|---|---|
| Goal | The approved user goal in one sentence |
| In-scope outcomes | Observable behavior, files, tests, or docs that must be correct |
| Verification | Smallest meaningful command(s), plus broader checks if risk warrants them |
| Review condition | What the reviewer should check after the latest meaningful change |
| Stop boundary | What kinds of broad, speculative, or unrelated findings will be deferred |

If the checklist cannot be satisfied without a human decision, report the blocker and stop. If it is satisfied with fresh evidence, stop; do not loop just because another runtime could force another iteration.

## Workflow

1. Re-read the approved design, plan, or current user goal. Define the scope boundary and fill all five Completion Criteria fields before fixing.
2. Implement or repair the next in-scope slice yourself.
3. Dispatch exactly one reviewer subagent per iteration, scoped to the goal, diff, tests, and risk areas. Explicitly identify it as the designated reviewer and require it to load `quality-reviewer`, use the integrated rubric and triggered lenses, validate findings with evidence and confidence ≥ 80, and return concise candidates without spawning nested reviewers. The main agent owns direct mechanical gates and the final report. This keeps the same review bar inside and outside the loop without multiplying identical context.
4. Report the review result in the conversation: findings, accepted fixes, rejected findings, deferred audit items, and next action.
5. Fix accepted current-goal issues. Verify with the smallest meaningful command first, then broader checks when risk warrants it.
6. Repeat review after meaningful code, test, behavior, schema, API, UX, or config changes.
7. Stop only when verification is fresh, the latest reviewer pass has no unresolved current-goal issues, and the completion criteria are satisfied.

## Triage Rules

| Finding | Action |
|---|---|
| Bug, regression, missing required test, broken requirement | Fix now, verify, review again |
| Ambiguous detail with local precedent | Choose the conservative local pattern, report decision |
| Reviewer is wrong or speculative | Reject with code/test evidence |
| Broad architecture, migration, contract, security, data, or product impact | Post a nonblocking note, defer unless it blocks safe completion |
| Unrelated cleanup or neighboring-package polish | Defer to final audit |

Broad or unrelated items do not stop loopfix by default. Keep working on the current goal. Only stop if the current goal cannot be completed safely without a human decision.

## Required Reporting

After each reviewer pass, send a brief working update:

```text
Reviewer pass N found:
- Completion criteria: <satisfied / not yet / blocked>
- Fixing now: <in-scope issues>
- Rejecting: <finding + evidence>
- Deferring for final audit: <broad/unrelated items>
Next: <fix/verify/review action>
```

Final response must include:
- loop count and latest reviewer result
- completion criteria and whether they were satisfied
- fixes made
- verification commands and results
- deferred audit items the agent decided not to fix now
- residual risk or blockers, if any

## Failure Modes

- Do not stop after one review when meaningful fixes made the review stale.
- Do not hide triage or deferred findings until the final response.
- Do not let the reviewer own scope, fix every comment, or fan out parallel
  reviewers; the main agent triages exactly one designated reviewer per
  iteration.
- Do not skip review because targeted tests passed, or claim completion with
  stale verification.
- Do not use hooks, state files, forced re-prompts, or another runtime to keep
  the loop alive.
- Do not change completion criteria silently after work starts.
- Stop and surface the conflict when the same issue does not converge within
  five iterations.

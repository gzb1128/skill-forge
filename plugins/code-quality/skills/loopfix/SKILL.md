---
name: loopfix
description: Use when an approved goal, design, or implementation plan needs autonomous hardening after a first pass, especially when the user says loopfix, loop-fix, review-fix loop, keep fixing, or do not wait unless impact is broad.
---

# Loopfix

## Overview

Loopfix is an autonomous work-review-fix loop for the current approved goal. The main agent owns triage and momentum: reviewer subagents advise, but the main agent decides what to fix now, what to reject, and what to defer for final human audit.

**Core rule:** meaningful in-scope changes reset the loop. Do not finish until a reviewer pass after the latest meaningful change finds no unresolved current-goal issue, verification is fresh, and the runtime-neutral completion criteria are satisfied.

Completion is an evidence-backed judgment by the main agent, not a hook, state file, forced re-prompt, or arbitrary iteration count. Do not add runtime-specific loop mechanisms. Continue only when an in-scope issue remains.

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

```dot
digraph loopfix {
    "Current goal defined?" [shape=diamond];
    "Define completion criteria" [shape=box];
    "Work locally" [shape=box];
    "Dispatch reviewer subagent" [shape=box];
    "Report findings and triage" [shape=box];
    "Current-goal issues?" [shape=diamond];
    "Fix in scope" [shape=box];
    "Fresh verification" [shape=box];
    "Deferred audit list only?" [shape=diamond];
    "Final summary" [shape=box];

    "Current goal defined?" -> "Define completion criteria" [label="yes"];
    "Current goal defined?" -> "Final summary" [label="blocked"];
    "Define completion criteria" -> "Work locally";
    "Work locally" -> "Dispatch reviewer subagent";
    "Dispatch reviewer subagent" -> "Report findings and triage";
    "Report findings and triage" -> "Current-goal issues?";
    "Current-goal issues?" -> "Fix in scope" [label="yes"];
    "Fix in scope" -> "Fresh verification";
    "Fresh verification" -> "Dispatch reviewer subagent";
    "Current-goal issues?" -> "Deferred audit list only?" [label="no"];
    "Deferred audit list only?" -> "Final summary" [label="yes"];
    "Deferred audit list only?" -> "Report findings and triage" [label="no"];
}
```

1. Re-read the approved design, plan, or current user goal. Define the scope boundary and fill all five Completion Criteria fields before fixing.
2. Implement or repair the next in-scope slice yourself.
3. Dispatch at least one reviewer subagent scoped to the goal, diff, tests, and risk areas. Ask for correctness bugs, regressions, missing tests, edge cases, and overbroad changes.
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

## Red Flags

- "One review pass is enough" after meaningful changes
- "The user wants concise updates, so I will hide review triage until final"
- "The reviewer mentioned it, so I should fix everything"
- "This is broad, so I should stop and wait" when it can be deferred
- "Targeted tests passed, so no reviewer is needed"
- "A hook/runtime should keep looping for me"
- "No explicit completion criteria are needed; I will know done when I see it"

## Rationalizations

| Excuse | Reality |
|---|---|
| "Bounded review-and-fix pass, not an open-ended loop" | Loopfix is bounded by current-goal cleanliness, not by one pass. |
| "Use one reviewer/subagent" | Use at least one per iteration. Meaningful changes require another review. |
| "Reviewer noise wastes time" | Triage noise; do not remove the review loop. |
| "Asking the user is safer" | Main agent owns normal triage. Defer broad items and keep moving. |
| "Fixing all comments is thorough" | Overfixing broad or unrelated items violates scope control. |
| "Forced looping is more reliable" | Runtime-neutral loopfix relies on fresh evidence and agent judgment, not hooks or state files. |

## Common Mistakes

- Letting the subagent decide scope. The main agent must inspect findings and own the decision.
- Running review before reconstructing the current goal. Review without scope creates noisy refactors.
- Treating deferred audit items as hidden work. Report them when found and summarize them at the end.
- Claiming ready while checks are stale. Any accepted fix requires fresh relevant verification.
- Letting completion criteria drift after work starts. Change them only when the user goal or discovered blocker requires it, and say why.

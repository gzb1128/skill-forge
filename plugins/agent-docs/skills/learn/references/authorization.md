# Authorization for Repository Knowledge Work

Determine the requested operation from the current request and authorization
already given in the session. Skill selection alone does not authorize writes.

| Requested operation | Behavior |
|---|---|
| Assess, audit, review, or inspect | Read and report; do not edit |
| Propose, preview, or show a plan/diff first | Prepare a concrete proposal and stop at the requested checkpoint |
| Create, save, repair, reorganize, set up, apply, or implement an approved proposal | Verify the relevant facts, describe the intended change, and complete the authorized edits without asking for the same approval again |

A bare audit invocation stays read-only. A bare `learn` invocation proposes
session knowledge; an explicit request to save verified insights permits writing
them. A bootstrap or setup request permits its scoped creation/adoption unless
the user asks for a proposal first. Urgency never overrides a requested checkpoint.

Authorization is bounded by the topic, selected proposals, exclusions, and any
explicit file allowlist. Preserve unrelated tracked, staged, unstaged, and
untracked work and its staging state. Do not expand knowledge maintenance into
product behavior changes, installations, commits, or publishing.

Preserve applicable repository approval requirements. Ask only when a material
choice remains unresolved, a required checkpoint is pending, or a coherent repair
needs scope beyond the authorization. Explain the specific requirement. Continue
independent authorized work while leaving the affected part pending.

Resolve factual drift from evidence. A source/contract disagreement may indicate
a product defect; do not silently redefine required behavior to match current
code. Keep unresolved choices explicit and retain useful authoritative text until
its replacement is in place. Report applied changes, skipped candidates, actual
checks, and any incomplete work; do not call a partial relocation complete.

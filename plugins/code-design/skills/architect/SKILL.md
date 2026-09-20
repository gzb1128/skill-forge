---
name: architect
description: Design APIs, types, and module boundaries from caller needs and existing constraints. Use for explicit code-design requests or changes with unresolved structural tradeoffs; not routine edits that fit established patterns or review-only requests.
---

# Architect

Make the design decisions needed for a code change, with enough evidence and
concrete usage to evaluate them.

## Establish the requested outcome

Follow the user's scope throughout:

- Design or assessment only: return a design; do not edit product code. Sketch
  in the response or permitted scratch space. A local experiment is appropriate
  only within the request and repository rules, with isolated state.
- Design and implement: continue through the authorized implementation and
  verification without adding a design approval gate.
- Explicit checkpoint: present the concrete design and wait at that checkpoint.

Do not invoke this workflow just because code crosses a function boundary.
For a routine change that already fits an established pattern, use that pattern
and keep any explanation proportional. Existing authorization does not expand
because a more extensive design looks attractive.

## Ground the change in the existing system

Read the relevant repository entry points, current contracts, and actual source.
Reuse adequate context instead of repeating discovery. Trace the affected path
far enough to explain why it currently works, where the requested outcome first
fails, and which owner should address that gap. Separate current behavior from
intended behavior when source and contract disagree; surface the discrepancy.

When an uncertain call path, data transformation, or owner affects the design,
use [Trace the Current Code Flow](references/code-flow.md). Skip that investigation
when reliable context already answers it. Apply the repository's actual structure;
a small utility does not need an invented planning or admission layer.

Resolve a missing historical constraint with focused investigation using
[Evidence and Current Constraints](references/evidence.md). A separate `investigate-design-rationale`
invocation is optional; adequate existing evidence needs no new workflow.

## Shape the design from its callers

Start with a realistic usage example and expected result, including the relevant
failure behavior. Derive the smallest useful type/interface sketch and ownership
changes from that usage. Follow the repository's terminology and extension
points. A local change may need only a signature and a short rationale.

For a substantive structural decision, consult the applicable questions in
[Design Checks](references/design-checks.md). Explain the concrete limitation
before introducing a cross-layer flag, new execution path, or replacement
abstraction. Prefer changing the responsible owner over teaching a shared layer
about one caller's policy.

Compare alternatives when they represent meaningful choices. Include extending
the existing design when viable. Do not invent a second candidate to meet a
quota. Models, parallelism, and prototyping are methods to choose under the active
runtime and user constraints, not requirements of this skill.

Use the smallest permitted experiment to settle empirical uncertainty: a caller
fixture, type-checkable sketch, or focused behavior test. Name what it proves
and what it cannot establish. Do not invoke a real environment because a local
proof is incomplete; respect the repository's verification boundary and report
unverified behavior. For a claimed regression, a control against the unchanged
behavior distinguishes a real gap from a new expectation.

## Deliver or continue

Make the outcome reviewable: the problem and current owner, proposed caller
usage and shape, accepted tradeoffs, relevant compatibility/retry/migration
constraints, and the evidence or checks still needed. Omit inapplicable parts.
A diagram or design document is useful only when it improves understanding or
is requested by the user or repository; no mandatory scaffold or document set.

If implementation is authorized, implement against these decisions. Revisit a
decision when concrete friction or new evidence invalidates its assumptions;
do not defend a sketch by accumulating escape hatches. Stay within the approved
scope, preserve unrelated work, and surface changes that need user judgment.
Do not force an entire redesign for a routine implementation adjustment.

When contracts or ownership change, update the affected authoritative material
as required by the repository. Keep historical decision records distinct from
living contracts; task steps stay in session state. This does not automatically
invoke knowledge capture, review, commit, or publication workflows.

Report design confidence and actual verification separately. A convincing
sketch is not implementation proof; local tests are not deployed-system proof.

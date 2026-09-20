# Pre-edit Coding Rules

Canonical candidate semantics for explicit repository setup. The target
repository owns the adapted text. Quality workflows carry their own task-specific
safeguards and do not require setup to have run; their Git, review, cleanup,
commit, and loop procedures are not installed as repository coding rules.

Use the user's selected subset. Without a subset, consider all core families
below, omitting inapplicable concerns and preserving existing semantic coverage.
These examples are starting points, not mandatory wording or a section template.

| Family | Candidate expectation | Adaptation boundary |
|---|---|---|
| Scope and work preservation | Before editing, establish the requested scope and preserve unrelated tracked, staged, and untracked work, including staging state. | Do not make baseline cleanup or committing part of every task. |
| Existing flow and ownership | For changes across modules or to parsing, persistence, or state transitions, trace the actual entry and current contract, identify where the requested outcome first fails, and fix its responsible owner. | Reuse sufficient context. Routine local edits need no architecture exercise; name project owners only when verified. |
| Authorization | Carry existing authorization through the task; ask about unresolved ownership, product/design decisions, or actions beyond that scope. | Preserve deliberate project-specific approvals and read-only requests; setup cannot expand permission. |
| Verification | Use the repository's permitted, relevant checks and distinguish passing checks, change-induced failures, pre-existing failures, unavailable checks, and explicit skips. State what the evidence proves. | Do not invent commands, waive required checks, or treat local proof as real-environment proof. |

A concise ownership rule should explain the trigger and expected decision:

> Before changing cross-module behavior or persistent state, trace the relevant
> entry and current contract. Identify the responsible owner and fix the gap at
> that boundary rather than introducing a bypass. Reuse adequate context;
> routine local edits do not require a design investigation.

Link the project's actual responsibility map or living contract when one exists.
Generic setup cannot infer domain rules such as which input is frozen, which
service owns identity fallback, or which transaction admits an operation. Keep
those in their existing authoritative project surfaces. Do not promote an
observation into a new domain rule without evidence and authority.

## Early rules versus workflow details

Early rules define constraints that must be considered before edits. Detailed
Git base selection, independent reviewer dispatch, readiness verdict formats,
knowledge scoring, or investigator orchestration remain in their workflows.
Neither `investigate-design-rationale` nor `architect` must run to satisfy the early ownership rule.
Existing evidence and an ordinary source read can be sufficient.

A plugin reference is not automatically visible in the target repository. A
path to an installed cache is not a durable project reference. Put the concise
condition directly in the applicable instruction entry and use local links for
longer detail. Do not manufacture duplicate docs to avoid a few useful lines.

## Updates and conflicts

Different wording can express complete coverage. A repository may split a rule
across an entry point and a linked contract; assess that path before adding it.
Local text can also be intentionally stricter. Do not weaken a human-only
integration boundary or a release approval rule as a side effect of setup.

When update intent is unclear, preserve the existing rule and identify the
conflicting clauses. Missing unrelated families can still be installed when
authorized. Future setup runs reassess the current text rather than forcing an
upstream snapshot onto it. No automatic update or rule execution is installed.

# Repository Knowledge Lifecycle

**Status:** Approved
**Date:** 2026-08-03

## Problem

The agent-docs plugin treated non-derivability as a universal gate and copied
that policy into every bootstrapped repository. This caused two kinds of drift:

- useful but derivable commands, maps, runbooks, and verification contracts
  could be rejected or deleted;
- bootstrap owned a large generic `docs/` payload whose policy could diverge
  from the installed `learn`, `remember`, and `curate` skills.

The four skills also reason about the same repository-knowledge question, but
their role boundaries differ. Calling `learn` from the other skills would reuse
workflow as well as policy, coupling creation, audit, and initialization.

## Decision

Keep four independent workflows and move their common decision rules into
plugin-owned references:

| Skill | Role | Write boundary |
|---|---|---|
| `bootstrap-agent-docs` | Initialize a repository that lacks a project entry point | Create only root `AGENTS.md` after approval |
| `learn` | Produce newly discovered repository knowledge | Propose exact `AGENTS.md` or `docs/` diffs; apply only after approval |
| `remember` | Audit prompt-resident repository memory | Inspect `AGENTS.md` files; report first |
| `curate` | Audit the pull-based knowledge base | Inspect `docs/`; report first |

All four read the same knowledge admission policy. None invokes another skill.
This shares the stable decision model without nesting prompts, approval gates,
or incompatible scan scopes.

## Admission Model

A candidate must first be verified, durable, non-duplicative, and correctly
routed. After those hard gates:

- non-derivable knowledge is automatically admitted;
- derivable knowledge may be admitted when impact, recurrence, discovery cost,
  actionability, durability, and scope justify its surface cost;
- derivability alone never triggers deletion.

The usual score guidance is 9+ out of 12 for prompt-resident `AGENTS.md` content
and 7+ for pull-based docs. Scores are decision aids for individual candidates,
not ceremonial grades for whole files.

This intentionally preserves a strict meaning for `Hidden Knowledge`: it holds
non-derivable gotchas and constraints. High-value derivable content instead
uses purpose-specific surfaces such as Quick Reference, codemaps, runbooks, or
verification docs.

## Bootstrap Boundary

Bootstrap no longer creates generic policy documents, category indexes, or doc
templates. Its payload contains only a minimal root `AGENTS.md` template with
verified commands, architecture routing, project rules, and links to the three
ongoing knowledge workflows.

Documentation categories are created on demand. The first admitted document in
a category creates or updates that category's `INDEX.md`; an absent category is
not a defect.

Plugin policy remains under `plugins/agent-docs/references/` so an installed
skill always reads the version shipped with that plugin. Target repositories
record only project-specific knowledge.

## Consequences

- Existing bootstrapped repositories keep their current docs; `curate` can
  assess them without assuming the old non-derivability rule is authoritative.
- New repositories receive a much smaller, lower-drift baseline.
- `learn` can persist high-value docs instead of returning a destination-only
  suggestion that requires another workflow.
- `remember` and `curate` remain focused and cannot accidentally broaden each
  other's audit scope.

## Verification

- A learn scenario must retain both automatically admitted non-derivable
  knowledge and high-scoring derivable knowledge while skipping a low-value
  derivable restatement.
- A remember scenario must retain useful derivable build/test commands.
- A curate scenario must retain a useful derivable runbook while still finding
  structural and drift defects.
- A bootstrap scenario must propose exactly one new file, `AGENTS.md`, wait for
  approval, then prove the applied payload created no `docs/` path.
- Plugin schema validation, shell syntax checks, scenario builds, markdown diff
  checks, and `make validate` must pass.

## Related

- [Knowledge Admission Policy](../../plugins/agent-docs/references/knowledge-admission.md)
- [Documentation Structure Reference](../../plugins/agent-docs/references/doc-structure.md)
- [Superseded memory command design](2026-05-28-memory-commands-design.md)

# Documentation Structure Reference

This plugin-owned reference defines the generic structure used by `learn` and
checked by `curate`. `bootstrap-agent-docs` reads it to avoid pre-creating docs
categories. Project-specific rules belong in the target repository rather than
being copied from this file.

## Create Documentation On Demand

Do not pre-create empty documentation categories. Add a category and its
`INDEX.md` when the first useful document in that category is admitted under
the knowledge admission policy.

Common categories include:

| Category | Purpose |
|---|---|
| `docs/rules/` | Project-specific conventions and hard boundaries |
| `docs/design/` | Durable decisions, alternatives, constraints, sequencing dependencies, verification boundaries, rollback, and rationale |
| `docs/runbooks/` | Deterministic operational procedures |
| `docs/verify/` | Repeatable verification flows and expected results |
| `docs/troubleshoot/` | Symptom-to-cause diagnosis |
| `docs/codemaps/` | Architecture navigation and concept-to-source maps |
| `docs/lib/` | Project-relevant third-party behavior and usage |

An absent category is not a defect. A category containing documents should
normally have an `INDEX.md`.

## Do Not Create Agent Execution Plan Docs

Do not create `docs/plans/` for step-by-step agent task decomposition, session
checklists, or implementation narration. Keep those transient details in the
task session. Reclassify any durable knowledge through the normal admission
model: concise recurring gotchas may belong in the nearest `AGENTS.md`, while
docs-bound decisions, alternatives, multi-step sequencing contracts,
verification gates, handoff contracts, and rollback boundaries belong in
`docs/design/`.

An existing `docs/plans/` category is not a defect by itself. Do not propose
category-wide deletion or migration unless the user explicitly requests it;
audit individual files under the same ordinary value and drift rules as other
docs. If the user does request removal, merge any still-valid durable knowledge
into the relevant design and delete execution-only artifacts. Do not copy a
plan wholesale into a design.

## INDEX Standards

- Keep an index as a navigation surface rather than a tutorial.
- Use a table with document, description, and `When to Use` or equivalent
  routing context.
- Update the index in the same change that adds, removes, or renames a document.
- Do not add filler to satisfy a target line count.

## Naming

- Use lowercase words separated by hyphens.
- Prefix designs with `YYYY-MM-DD-` when chronological browsing adds value.
- Avoid `-v2` and similar suffixes; supersede or archive explicitly.

## Maps, Not Encyclopedias

Codemaps map concepts and entry flows to authoritative source. They may identify
the owning package, stable symbols, and major call or data-flow transitions,
but should not copy function bodies, configuration dumps, or behavior-changing
policy.

Route knowledge by authority:

- concise recurring rules that change agent behavior belong in the nearest
  `AGENTS.md`;
- durable contracts, constraints, alternatives, and rationale belong in
  `docs/design/`;
- operational procedures belong in `docs/runbooks/`;
- codemaps link those surfaces to source instead of restating them.

Depth should scale with navigation value and workflow complexity rather than an
arbitrary global line limit.

## Stable References

Prefer package paths, files, symbols, headings, and named commands over line
numbers. A line number may be included only when a tool requires it and should
not be treated as the durable identity of a source concept.

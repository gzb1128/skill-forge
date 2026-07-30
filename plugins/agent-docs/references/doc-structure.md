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
| `docs/codemaps/` | Architecture navigation and concept-to-source maps |
| `docs/design/` | Decisions, alternatives, constraints, and rationale |
| `docs/plans/` | Sequencing, verification, rollback, and handoff |
| `docs/rules/` | Project-specific conventions and hard boundaries |
| `docs/troubleshoot/` | Symptom-to-cause diagnosis |
| `docs/runbooks/` | Deterministic operational procedures |
| `docs/lib/` | Project-relevant third-party behavior and usage |
| `docs/verify/` | Repeatable verification flows and expected results |

An absent category is not a defect. A category containing documents should
normally have an `INDEX.md`.

## INDEX Standards

- Keep an index as a navigation surface rather than a tutorial.
- Use a table with document, description, and `When to Use` or equivalent
  routing context.
- Update the index in the same change that adds, removes, or renames a document.
- Do not add filler to satisfy a target line count.

## Naming

- Use lowercase words separated by hyphens.
- Prefix designs and plans with `YYYY-MM-DD-` when chronological browsing adds
  value.
- Avoid `-v2` and similar suffixes; supersede or archive explicitly.

## Maps, Not Encyclopedias

Codemaps should provide boundaries, workflows, ownership, diagrams, and tables
mapping concepts to source. Link to source instead of copying function bodies
or configuration dumps. Depth should scale with interface and workflow
complexity rather than an arbitrary global limit.

## Stable References

Prefer package paths, files, symbols, headings, and named commands over line
numbers. A line number may be included only when a tool requires it and should
not be treated as the durable identity of a source concept.

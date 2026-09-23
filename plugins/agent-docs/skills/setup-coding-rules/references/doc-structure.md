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
| `docs/lib/` | Project-relevant third-party behavior and usage |

An absent category is not a defect. A category containing documents should
normally have an `INDEX.md`.

Use an existing architecture overview or living document when it adequately
explains the system. A separate architecture category, including `docs/codemaps/`,
is optional. Existing codemap filenames may remain; maintain their useful
architecture content under the contract below without a directory-wide rename.

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

## Design Docs Are Point-in-Time Records

`docs/design/` holds two kinds of documents with different maintenance rules:

- **Decision records** (`YYYY-MM-DD-` prefixed): background, alternatives,
  decision, verification and rollback boundaries for one change. Freeze a
  record once its decision lands; later edits only update its Status line.
  Current-state maintenance belongs to code comments, architecture descriptions, or
  `AGENTS.md` — never to rewriting a landed record. To change a decision,
  write a new record and supersede the old one explicitly.
- **Living contracts**: documents stating currently binding constraints,
  sequencing, or handoff contracts (identity rules, lifecycle contracts).
  These stay current and are audited against source for drift like any
  other living document.

Mark the kind in the Status line (`Approved`/`Frozen`/`Superseded` for
records, `Living` for contracts). A frozen record that no longer matches
current source is not drift; the remedy is a new superseding record, not a
rewrite.

Implementation narration — "code changes" step lists, duplicated API
schemas, pre-landing plans — is plan-time content, not durable design
knowledge. After the change lands, code and its doc comments are
authoritative; artifact-scoped invariants from the same decision should
also land as doc comments on the owning symbols.

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

## Architecture and Responsibilities

Record components, data flow, inputs and outputs, responsibility boundaries,
data authority, dependencies, state ownership, recovery, compatibility, and
rationale when they help a future task. Name the responsible packages and link
existing contracts. Scale detail to the system; a small script needs no invented
layers. Do not copy implementation bodies, configuration dumps, or source trees.

Route knowledge by authority:

- concise recurring rules that change agent behavior belong in the nearest
  `AGENTS.md`;
- durable contracts, constraints, alternatives, and rationale belong in
  `docs/design/`;
- operational procedures belong in `docs/runbooks/`;
- architecture descriptions connect those surfaces to responsible packages.

Depth should scale with navigation value and workflow complexity rather than an
arbitrary global line limit.

## Source References

Package paths are the smallest maintained unit for source navigation in living
architecture descriptions and instruction entries. Do not maintain file lists,
private-symbol indexes, or call-chain transcripts. Moving files within the same
owner normally requires no documentation update; moving responsibility does.

Keep exact paths when the path itself is the object of a rule or a required
operation input/output: for example, "edit `api/schema.yaml`, regenerate, and
never hand-edit `internal/api/generated.go`." Runnable commands, scripts, config
files, documentation links, and instruction-file links may also need exact paths.
Public APIs, protocol fields, domain types, state values, and configuration keys
remain precise when behavior depends on them. Code-adjacent comments may name
their artifact. These exceptions do not justify a separate file-location table.

Find current implementation details through actual callers, registered handlers
or commands, dependency wiring, and relevant configuration. A matching name or
existing path is a lead, not proof that the implementation serves the current
flow. Inspect only what the task needs; source reachability alone does not prove
production deployment or configuration.

Task-specific investigation may cite exact files, symbols, and lines as evidence,
with a revision when retained. Do not promote those observations into a living
location index or rewrite frozen historical evidence to today's paths.

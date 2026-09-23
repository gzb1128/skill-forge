# Documentation Structure Reference

This plugin-owned reference defines knowledge placement and architecture coverage
for bootstrap, capture, and curation. Project-specific rules belong in the target
repository rather than being copied from this file.

## Create Documentation On Demand

Do not pre-create empty documentation categories. Add a category and its
`INDEX.md` when the first useful document in that category is admitted under
the knowledge admission policy.

Common categories include:

| Category | Purpose |
|---|---|
| `docs/architecture/` | Current components, core flows, responsibility boundaries, and data/state ownership |
| `docs/rules/` | Project-specific conventions and hard boundaries |
| `docs/design/` | Durable decisions, alternatives, constraints, sequencing dependencies, verification boundaries, rollback, and rationale |
| `docs/runbooks/` | Deterministic operational procedures |
| `docs/verify/` | Repeatable verification flows and expected results |
| `docs/troubleshoot/` | Symptom-to-cause diagnosis |
| `docs/lib/` | Project-relevant third-party behavior and usage |

An absent directory alone is not a defect. A category containing documents should
normally have an `INDEX.md`.

Architecture coverage is a default requirement. Use `docs/architecture/` for new
current-system descriptions, with an overview and additional topics only as
needed. Reuse adequate existing architecture docs wherever they live and route
readers to them; do not duplicate or relocate them solely to match the default
path. A small tool's root `AGENTS.md` may provide sufficient coverage. Missing
important responsibility or data-flow explanations are gaps even when no
architecture directory exists and all existing links resolve.

Existing codemap filenames can remain when their architecture content is useful.
Evaluate mixed codemaps by content: preserve responsibilities and rationale in an
adequate receiving document before removing redundant implementation inventories.
Do not make a directory-wide rename a prerequisite for improvement.

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

Explain the main runtime components and core workflows sufficiently for a future
agent to choose the responsible layer before editing. Check coverage against
registered entries, actual wiring, and relevant configuration, rather than only
the list of existing documents. Scale investigation to the requested scope;
targeted work does not require a repository-wide survey.

For each important flow, cover the applicable questions:

- What starts the flow, and what result or externally visible effect ends it?
- Which packages own inputs, decisions, transformations, persistence, and execution?
  What work must remain outside each owner's responsibility?
- What data crosses each handoff? Which source is authoritative, when does data
  become immutable, and where may consumers read dynamic state?
- Which dependencies are synchronous, asynchronous, or external? Who owns state
  transitions, failure, retry, and recovery?
- Which compatibility paths remain active, and which contracts explain their
  constraints and rationale?

These are coverage questions, not mandatory headings or invented layers. A
component diagram or flow should label responsibility and meaningful handoff
data; a directory tree or bare sequence of package names is insufficient. Keep
unknown boundaries explicit and distinguish source/configuration evidence from
verified deployment behavior. Do not copy implementation bodies, configuration
dumps, or source trees.

Route knowledge by authority:

- concise recurring rules that change agent behavior belong in the nearest
  `AGENTS.md`;
- durable contracts, constraints, alternatives, and rationale belong in
  `docs/design/`;
- operational procedures belong in `docs/runbooks/`;
- current architecture descriptions connect those surfaces to responsible
  packages, maintaining current structure and flows without copying canonical
  state machines, schemas, or compatibility matrices.

Root `AGENTS.md` supplies a short system summary, architecture routing, and early
cross-module guards. Module instructions carry local pre-edit constraints. Keep
existing living canonical contracts authoritative at their established location;
an implementation/contract conflict needs diagnosis, not silent contract repair.
Update architecture when responsibilities, handoff data, dependencies, or state
authority change. Keep proposals separate from the implemented current state.

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

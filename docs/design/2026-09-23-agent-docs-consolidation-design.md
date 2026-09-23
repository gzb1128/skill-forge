# Agent Documentation Maintenance and Architecture Documentation

**Status:** Implemented in the working tree; focused behavior and packaging checks passed, installed discovery unverified
**Date:** 2026-09-23
**Source baseline:** `8bfa69802c13c50246f8446d25ea2955d5c5f4c0`

## Outcome and scope

Consolidate existing repository-knowledge maintenance into `agent-docs:curate`.
The workflow must complete a scoped knowledge change across the relevant
`AGENTS.md`, architecture descriptions, contracts, rules, and indexes without
leaving the work between two skills. Retire `remember` as an independent workflow.

Long-lived architecture documentation records components, data flow, ownership,
constraints, and reasons. Its source-location detail stops at packages. Agents
find current implementation details through actual callers and runtime wiring
when a task needs them. The plugin stops encouraging manually maintained lists
of implementation files and private symbols.

This design covers the agent-docs plugin, its shared references and template,
catalog documentation, verification scenarios, and affected navigation. It does
not migrate DMS documentation. Implementation includes isolated local package
verification; updating a user's normal installed environment is separate.
Other plugins change only if they carry an affected instruction or catalog
reference; this is not a repository-wide skill redesign.

The package-level limit follows the user's stated requirement. Workflow
consolidation, retirement mechanics, and the validation plan below are the
approved implementation design. Verification evidence is recorded separately.

## Observed problems

These observations describe the pre-change source baseline above; the linked
maintained paths now carry the implementation and revised scenario expectations.

| Current carrier | Verified limitation | Consequence |
|---|---|---|
| [Documentation structure](../../plugins/agent-docs/references/doc-structure.md) | Codemaps are concept-to-source maps; files and symbols are recommended over line numbers | File moves and symbol changes still require a second location index to be maintained |
| [Curate scenario](../verify/scenarios/curate/build-a.sh) | Expected repair replaces copied implementation with a concept-to-file table | The test rewards the artifact responsible for recurring drift |
| [Remember scenario](../verify/scenarios/remember/build-a.sh) | Expected repair replaces a stale line number with a file/method reference | Reduced line-number drift is treated as sufficient improvement |
| Pre-change `remember` and [curate](../../plugins/agent-docs/skills/curate/SKILL.md), at the source baseline above | Audit ownership is divided by `AGENTS.md` versus `docs/`; related destinations are restricted to verification or promotion proposals | One relocation or conflict repair can be left without an owner for the complete change |
| [Bootstrap](../../plugins/agent-docs/skills/bootstrap-agent-docs/SKILL.md) | It both suggests moving excess detail to `docs/` and prohibits producing anything except root `AGENTS.md`; the template includes executable-file examples | Initialization has inconsistent completion rules and reproduces detailed location maps |

The DMS assessment demonstrated concrete instances of stale Render locations,
outdated ownership descriptions, duplicated implementation status, and a retired
verification command. It established defects in the current documentation, not
a measured success-rate improvement for this proposed workflow.

Existing admission policy already supplies useful evidence, residual-value,
placement, and retention criteria. Preserve that foundation. File existence and
symbol existence alone do not establish that an implementation is reachable
through the relevant current entry, dependency injection, or configuration.

## Skill responsibilities

| Skill | Trigger and responsibility | Completion boundary |
|---|---|---|
| `bootstrap-agent-docs` | Explicit initialization of a repository lacking a usable agent entry point | A minimal usable root entry with verified commands, package-level orientation, and necessary local constraints |
| `learn` | Explicit retrospective capture of useful knowledge discovered in the current session | Verified candidates placed in existing appropriate carriers, with capture and apply behavior following the user's requested mode |
| `curate` | Explicit assessment or repair of existing repository knowledge within a topic or requested scope | The relevant instructions, explanations, contracts, and navigation are consistent; every affected destination is handled or an explicit unresolved decision is reported |
| `setup-coding-rules` | Explicit adoption or adjustment of selected coding expectations | Applicable rules become visible before the relevant work; existing semantic coverage and local policy are preserved |
| `remember` | Existing instruction-audit entry being retired | Its checks and supported use cases move into `curate`; it owns no separate rubric or execution procedure |

No mandatory sequence connects these skills. A direct request to edit a named
document remains ordinary document work. It need not invoke `learn`, initialize
a repository, or perform a broad audit. Rule promotion during curation is a
placement operation; it does not require a separate setup invocation.

### Unified curation scope

Scope is determined by the user's topic, module, named files, and authorization.
The file extension or documentation directory does not split the workflow.

For example, a request to simplify an oversized DAO rule can require moving its
explanation into an existing ORM guide, retaining the early prohibition in the
applicable `AGENTS.md`, updating a database navigation entry, and checking that
the same requirement remains enforceable and discoverable. One `curate` run
owns that complete result.

A request about Render permits inspection of relevant Render instructions and
contracts, including necessary root routing. It does not authorize unrelated
database or deployment-policy cleanup. An explicit file allowlist remains a hard
write limit: if a coherent repair needs another destination, identify the needed
extension and preserve the affected text until it is authorized.

Apply different criteria within this one workflow:

- Instruction entries justify early visibility and preserve concise, high-impact
  constraints. Do not assume every nested `AGENTS.md` is always loaded.
- Architecture descriptions explain responsibilities and interactions at package
  granularity and link to existing behavioral contracts.
- Living contracts state required behavior and distinguish implemented behavior
  from accepted future changes.
- Decision records preserve rationale and their historical context.
- Runbooks and verification instructions remain operationally useful and explicit
  about prerequisites, effects, and the evidence they establish.
- Indexes route readers; implementation progress is maintained in its owning
  document rather than copied into several navigation tables.

Read code and tests when needed to verify an assertion. Curation does not
authorize changing product behavior or adding unrelated tests and automation.
Source-comment relocation is available only when authorized within the requested
documentation scope; explain any further work needed without deleting its
existing authoritative explanation first.

### Authorization and completion

All four surviving workflows use one shared authorization matrix:

| User intent | Required behavior |
|---|---|
| Assessment, review, audit | Read and report without editing |
| Proposal or preview, including an explicit checkpoint | Produce concrete proposed changes and stop at that checkpoint |
| Explicit create, save, repair, setup, apply, or approved implementation | Verify facts and complete scoped edits without asking for the same authorization again |

A bare `learn` invocation proposes; an explicit save request authorizes capture.
Bootstrap and setup honor an explicit create/adopt request. Curation owns a
complete authorized repair across carriers. Preserve file exclusions, local
approval requirements, and unresolved behavioral choices. Update the old
bootstrap and learn blanket gates and their scenario expectations together.

Resolve factual drift using current evidence. A source/contract disagreement can
also reveal a product defect, so source does not automatically overwrite the
contract. Report unresolved behavioral choices and proceed with independently
authorized repairs. Never call an incomplete relocation complete because the
other carrier formerly belonged to another skill.

## Architecture documentation contract

### Retained content

Keep components and their purposes, inputs and outputs, data authority, allowed
dependencies, state ownership, transaction boundaries, input freezing, recovery,
compatibility, and rationale when relevant to the system. Name responsible
packages when a source location helps. Do not require every small project to
have all these concepts or a separate architecture document.

A persistent architecture view may describe:

```text
request use case -> planning packages -> admission -> persistence
                                                   |
                                                   v
                                          runtime controller
```

The accompanying explanation identifies who selects inputs, who commits them,
and who advances runtime state. It does not inventory the implementing files.

### Source-location granularity

Package paths are the smallest maintained source-location unit for navigation
in architecture and instructions. Avoid file inventories, private-method indexes,
full call-chain transcripts, and tables mirroring the source tree. Renaming a
private method or moving files within the same owner normally requires no
architecture-document update. Moving responsibility across owners does.

This rule does not remove semantic precision: public APIs, protocol fields,
domain types, state values, and configuration keys may be named when the
contract depends on them. Runnable commands may include exact script or config
paths required for execution. Exact paths also remain when the path itself is
the normative object or operational input/output: for example, edit
`api/schema.yaml` and never hand-edit `internal/api/generated.go`. Replacing
those rule targets with package names would weaken the constraint. These
exceptions must not regenerate a separate implementation-file inventory.
Links to documents and instruction files remain necessary. Comments attached
to their owning code artifact are still permitted.

Task-specific investigation and review may cite precise source files and symbols
as evidence, with a relevant revision when evidence is retained. Such evidence
is not promoted into a living source-location directory. This design's links to
skill instructions and fixtures identify the audited documentation artifacts;
they do not define a production-code navigation model.

### Current path discovery

Agents find implementations from the caller, registered handler or command,
event consumer, dependency wiring, and relevant configuration. Similar names
and directory placement are leads. Follow actual calls far enough to establish
the owner and effect relevant to the task.

The existing [current-flow reference](../../plugins/code-design/references/code-flow.md)
already explains this behavior. Keep it owned by code-design; curation can use
bounded source inspection without imposing an architect invocation or another
plugin dependency. Source reachability proves only the inspected implementation;
production-use claims additionally require deployment and configuration evidence.

### Existing codemaps

Stop presenting `docs/codemaps/` as a required or preferred category for new
repositories. Use an adequate existing architecture overview or living document;
create a new carrier only when the repository and task justify it.

Existing codemap filenames can remain while their contents are maintained under
this contract. For a scoped migration, retain architectural knowledge, remove
redundant implementation-location inventories, and update necessary links
together. Renaming the entire directory is not a prerequisite. Frozen historical
evidence is not rewritten to point at today's implementation.

## Bootstrap and capture alignment

Bootstrap creates only the minimal root entry. Remove the fixed line target,
the instruction to create overflow documents, and executable-file examples.
Use package-level component responsibilities and existing contract links. Omit
inapplicable template sections. Describe important unknown commands plainly;
do not leave unexpanded placeholders that look executable or declare command
verification complete without evidence. Existing entry points are maintained
through the unified curation capability rather than overwritten by bootstrap.

Maintain templates only in `plugins/agent-docs/templates/`; distribute an equal
copy into `bootstrap-agent-docs/assets/templates/` with `make sync-templates`.
The plugin includes both, and the standalone skill carries its own asset.
Resolve assets relative to the loaded skill directory without requiring
`CLAUDE_PLUGIN_ROOT`, the plugin parent, or a source checkout. `make validate`
checks missing, changed, and obsolete extra template files; synchronization
does not silently delete extras. Bootstrap adapts the asset before exclusively
creating root `AGENTS.md`, so existing or concurrently created entries survive.

Keep `learn` focused on explicit session capture. Align its accepted outputs with
the package-level rule and the existing residual-value policy. Do not capture a
search result as a new location map. Preserve substantive rationale, operational
knowledge, and code-adjacent invariants when they earn their maintenance cost.

## Retirement and compatibility

The target catalog has four agent-docs workflows: bootstrap, capture, curation,
and explicit coding-rule setup. Recommend retiring `remember` directly after
its maintained catalog, template, and verification references are migrated.
Document that existing users should invoke `curate` for instruction audits.

Before removal, inspect the repository's current consumers and installed-skill
exposure contract. Older installed packages remain unchanged until updated;
personal symlinks and caches are not silently deleted. Test installation and
link-management behavior in isolated runtime directories, and document any
stale-link cleanup required by removal. Status must detect the retired entry
even after its source directory disappears. Explicit cleanup removes a link
only when its exact target is this checkout's current or retired skill path;
foreign same-name links and real directories remain intact.

If a verified consumer requires a transition, permit a temporary `remember`
compatibility entry only when it consumes the same maintained curation workflow
through the existing reference fan-out. It must not retain a second audit body
or require cross-skill invocation to complete the task. Name the consumer and
its exit condition before adopting this exception. Do not retain an alias solely
for hypothetical callers.

## Change ownership and delivery dependencies

| Maintained area | Required change | Completion evidence |
|---|---|---|
| `plugins/agent-docs/references/` | Package-level architecture contract, common placement criteria, removal of the file-based maintenance split | One editable policy source; generated consumer copies remain consistent |
| `plugins/agent-docs/skills/curate/` | Complete topic-scoped maintenance across instructions and docs; authorization follows user intent | Cross-carrier repair and limited-scope scenarios pass |
| `plugins/agent-docs/skills/remember/` | Transfer useful checks and retire the independent workflow | No supported maintenance case is abandoned; catalog and exposure checks pass |
| Bootstrap skill and `plugins/agent-docs/templates/` | Minimal entry, package granularity, common authorization, skill-local template distribution and drift gate | New-repository/existing-entry controls and plugin/standalone asset checks pass |
| Learn and setup skills | Common authorization and placement; retain distinct capture/adoption triggers | Explicit apply completes, requested previews stay read-only, setup retains no-op behavior |
| Root catalog, plugin metadata, and instruction navigation | Describe the final four-workflow model and remove file-index guidance | No active instruction advertises the retired split |
| `docs/verify/` | Replace obsolete expected outcomes, preserve old results as historical evidence | New candidate results are separately attributable to immutable inputs |

Shared references are changed at plugin level and distributed by
`make sync-references`; consumer copies are not edited independently. The current
fan-out checks do not remove obsolete copies or retired personal symlinks, so
their migration must be accounted for explicitly.

The policy and outcome criteria must agree before publishing the merged skill.
The merged workflow, updated template/catalog, and replacement scenario
expectations form one coherent release boundary. Retire the old workflow only
after its cases are covered. A target-repository migration is a separate scoped
adoption after the plugin behavior is verified; DMS is a useful pilot, not an
installation side effect.

## Verification and acceptance

Use the existing [verification process](../verify/README.md) with an immutable
pre-change snapshot and fresh isolated candidate runs. Preserve successful old
runs; do not manufacture a RED failure. A changed rubric or a static rule
contradiction establishes a design issue, not comparative behavioral improvement.
Use separate baseline and candidate fixture directories with identical raw
prompts and initial content. Builders must not reset another run's repository
or outputs; retain source hashes and execution artifacts separately.

| Scenario | Required observable result |
|---|---|
| Long root rule moved into a topic document | Explanation, early guard, and navigation are updated together; no constraint disappears |
| Important rule buried in docs | The relevant module entry gains early visibility without copying the entire contract |
| Two carriers contradict each other | Factual drift is reconciled from evidence; unresolved behavioral choices are reported explicitly |
| Module-only task with unrelated dirty/staged work | Necessary related destinations are handled; unrelated content and staging remain intact |
| Explicit file allowlist or assessment-only request | No unauthorized destination edits; missing scope is reported rather than treated as complete |
| Implementation files move within one package | No replacement file/symbol inventory is created; valid architecture remains useful |
| Exact paths are objects of generation or editing rules | Schema and generated-output paths remain precise without a redundant file-location table |
| Responsibility moves across packages | Architecture and entry routing reflect the ownership change even if old filenames still exist |
| Current and legacy implementations share names | The agent follows wiring and conditions; an existing symbol is insufficient evidence of active use |
| Useful codemap contains both rationale and file inventory | Architecture and historical value survive; only redundant navigation detail is removed |
| Bootstrap with uncertain commands or an existing entry | A usable minimal result or scoped handoff; no placeholder docs tree or overwrite |
| Direct document request versus session capture versus rule adoption | The requested operation completes without an unrelated skill chain or repeated approval |
| Skill removal and runtime exposure | Updated catalog works in each claimed runtime; stale old entries and package paths are handled explicitly |

Inspect actual edits and reports. Primary measures are correct ownership,
preserved constraints, complete related updates, current-path evidence, and scope
adherence. Reading volume, clarification count, and runtime cost are secondary
observations, not substitutes for correctness or fixed score gates.

Implementation validation includes `git diff --check`, quick skill validation,
`make sync-references`, `make validate`, focused behavioral scenarios, and an
isolated package/exposure smoke test. Exercise fixture commands as well as their
syntax, and separately compare the skill contract with fixture expectations.
Direct skill reads do not prove installed discovery; validate each claimed
runtime and report unavailable checks. Keep source plugin packaging unchanged.

Acceptance requires no active file-based gap between instruction and docs
maintenance, no new architecture file inventories, preserved user authorization
and unrelated work, and recorded candidate evidence for the changed behaviors.

## History, release, and rollback

This decision revises the workflow split in
[Repository Knowledge Lifecycle](2026-08-03-repository-knowledge-lifecycle-design.md)
and the workflow ownership table in
[Knowledge Admission](2026-09-18-knowledge-admission-design.md).
Their substantive admission and historical-retention decisions remain useful.
When the implementation lands, update only the appropriate historical status
pointers and active navigation; do not rewrite old decisions or test outcomes.

Publish the final behavior and verification limits together. Rollback restores
the prior coherent plugin revision, catalog, template, and reference set. It
does not undo changes already adopted by a target repository: those are
repository-owned and require their own reviewed revert or maintenance change.
An optional compatibility entry shares the same rollback boundary as curation.

## Current checkpoint

The approved implementation updates plugin sources, catalog, fixtures, and
template distribution. See [verification](../verify/agent-docs-consolidation.md)
for observed results and limits. The normal installed environment and DMS
adoption remain separate from this source change.

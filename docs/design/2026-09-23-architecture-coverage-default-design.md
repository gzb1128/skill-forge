# Default Architecture Coverage

**Status:** Implemented in the working tree; focused behavior and package verification passed; automatic skill discovery unverified
**Date:** 2026-09-23
**Supersedes:** The root-only bootstrap output and optional architecture coverage in [agent-docs consolidation](2026-09-23-agent-docs-consolidation-design.md); other decisions remain in force

## Decision and rationale

Agents can cheaply search current implementation locations, but reconstructing
responsibilities, data authority, and lifecycle handoffs across components is
costly and error-prone. Architecture knowledge must therefore be a default
bootstrap and curation concern, including important explanations with no existing
document. Valid links alone do not establish useful coverage.

New separate current-system descriptions default to `docs/architecture/`. Reuse
adequate existing descriptions at their established locations. A small tool may
be fully explained in root `AGENTS.md`; missing directories alone are not defects.
Do not make adoption depend on a repository-wide rename.

## Ownership of knowledge

| Surface | Responsibility |
|---|---|
| Root `AGENTS.md` | Short system summary, architecture routing, and early cross-module guards |
| Module `AGENTS.md` | Local pre-edit rules and responsibility constraints |
| Architecture overview/topics | Current components, core flows, handoff data, dependencies, data/state authority, recovery and compatibility boundaries |
| Existing canonical contracts | Detailed binding behavior at the repository's established location |
| Decision records | Historical context, alternatives, decisions, and verification/rollback constraints |
| Source | Current implementation locations and private mechanics |

Architecture connects owners to canonical contracts without duplicating schemas,
state machines, or compatibility matrices. Source/contract conflicts remain
explicit decisions or suspected product defects. A proposal is not current state.
Package paths remain the smallest maintained implementation navigation unit;
exact rule targets, operation inputs/outputs, and public contract names retain
their existing exceptions.

## Workflow changes

- **Bootstrap** identifies main runtime components and core workflows. It writes
  a concise root entry and missing useful architecture docs when separate
  explanation is needed. Multi-component, cross-package business, and async
  systems default to a linked overview. Existing adequate docs are reused.
  Creation remains subject to the user's scope, previews, and file allowlists;
  preserve concurrent arrivals with exclusive creation and additive navigation.
- **Curate** checks missing coverage as well as drift. A whole-repository audit
  compares core flows to available explanations; a scoped audit stays with the
  affected flow. Report examined flows and unknowns, without declaring sampled
  coverage exhaustive. Architecture is not deferred behind link cleanup.
- **Learn** places explicitly captured responsibility and data-flow knowledge in
  the relevant existing topic or default architecture home. It does not expand
  session capture into an architecture audit.
- **Architect** uses current architecture and actual wiring, identifies proposed
  boundary changes separately, and synchronizes current descriptions after
  authorized implementation changes. It remains independent of agent-docs.
- **Setup coding rules** consumes the common placement reference but does not
  gain an architecture-bootstrap obligation from a selected-rules request.

## Distribution and maintenance

Editable bootstrap templates remain under `plugins/agent-docs/templates/`, now
including architecture overview and index resources. Synchronization copies the
whole payload into the standalone skill's `assets/templates/`. Both plugin and
standalone installs must resolve these assets relative to the loaded skill.
Shared architecture coverage and placement rules are authored once in the
plugin reference and distributed to its consumers.

Maintenance follows changes in responsibilities, handoff data, dependencies, and
state authority. Moving private implementation files within an unchanged owner
does not require an architecture edit. Do not maintain a file/symbol inventory
as proof that architecture is current. Source inspection and configuration
evidence do not establish deployed behavior.

## Verification and limits

See [architecture coverage verification](../verify/architecture-coverage.md).
Compare frozen old/new skills on raw isolated tasks. Check actual documents,
findings, preservation of unrelated work/index, and limits on claimed evidence.
Include simple-tool and existing-document controls, previews and file allowlists,
contract conflicts, and the two adjacent workflows. Packaging checks must cover
all template assets and an isolated install.

This change does not migrate DMS or publish the plugin. If the broader bootstrap
output causes regressions, preserve generated repository knowledge and correct
the responsible skill; reverting a template must not delete users' documents.

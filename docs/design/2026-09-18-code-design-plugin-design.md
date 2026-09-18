# Code Design Plugin

**Status:** Conditional-method integration approved; broader behavioral promotion pending
**Date:** 2026-09-18

## Purpose and naming

Add `code-design` for investigation of existing code-design rationale and for
API, type, and module design. Plugin names communicate a recognizable work
context and responsibility; individual skills specify narrower triggers. The
naming convention is recorded in root `AGENTS.md`. Sharing a plugin does not
make its skills a mandatory sequence.

`code-quality` remains responsible for concrete change review, cleanup, commit
gates, and fix loops. `agent-docs` remains responsible for knowledge placement
and maintenance. Neither is a catch-all for everything that improves code.
Two separate investigation/design plugins would add packaging boundaries before
there is a distinct installation need. `code-design` is sufficient for now.

## Adaptation decisions

| Upstream idea | Skill Forge treatment |
|---|---|
| Historical rationale and calibrated confidence | Keep; separate the historical reason, current constraint, and observed behavior |
| Caller usage before types | Keep; scale the sketch to the decision, with no compulsory document set |
| Existing-system grounding | Trace only relevant owners and reuse adequate context |
| Full source-category fan-out | Replace with question-driven search and an explicit stopping condition |
| Fixed models and investigator/synthesizer roles | Remove; delegation follows active user/runtime constraints |
| Mandatory how/why/arena chain | Remove; both skills work independently from available evidence |
| At least two design candidates | Compare only meaningful alternatives; existing structure can be sufficient |
| Design followed by implementation by default | Continue only when implementation is part of the authorized task |
| Design red flags | Conditional checks; transaction/lifecycle boundaries and real compatibility obligations take precedence over stylistic simplification |

The two descriptions permit model selection for their precise contexts, unlike
upstream's manual-only frontmatter. Ordinary coding, a runtime walkthrough, or a
review request alone is not a trigger. Negative-trigger evaluation remains
necessary; this integration does not claim reliable selection yet.

## Conditional-method integration

The 2026-09-18 follow-up approves the creator calibration, conditional integration,
and reuse of `how` as a reference. The creator calibration is already implemented
and separately verified in [Creator Fusion](../verify/skill-creator-fusion.md).
This change preserves it rather than creating another creator variant.

| Content | Strength and placement | Agent discretion |
|---|---|---|
| Authorization, repository contracts, evidence honesty | Requirements in existing skill scope and local rules | Methods cannot override these constraints |
| Historical investigation (`why`) | Default path when rationale is missing | Sources, depth, delegation, and when evidence suffices |
| Current execution tracing (`how`) | `code-flow.md`, loaded by either skill only for a material path/owner gap | Entry-specific depth, output shape, and reuse of adequate context |
| Caller-first design and experiments (`architect`) | Default methods for unresolved structural decisions | Real alternatives, sketch depth, experiment, and reconsideration |
| Implementation methods and playbooks | No new payload in this round; evaluate individual methods against a concrete need | No fixed implementation sequence introduced |
| Global workflow orchestration | Not introduced | No mandatory skill chain, model roster, or agent/alternative quota |

`code-flow.md` follows the actual caller, data, ownership, and relevant branches;
it distinguishes source, contract, and runtime evidence and names untraced gaps.
Its stopping condition is enough evidence for the decision, not a complete
subsystem inventory. It does not require a DMS-shaped lifecycle in other projects.
Existing context can bypass the method; conflicting evidence reopens only the
affected assumption. No standalone `how` entry is added unless a stable separate
user task justifies it. Ordinary walkthroughs remain outside these skill triggers.

## DMS practice informing the adaptation

The following repository sources were inspected on 2026-09-18. They motivate
transferable checks, not a dependency on DMS or a claim of a new runtime audit:

| DMS source, relative to its repository | Generalized requirement |
|---|---|
| `AGENTS.md`, existing-flow rules and DAO dependency rule | Explain why the current path works and where the new requirement fails; fix the responsible owner without reverse-layer dependencies |
| `internal/deploymentinput/AGENTS.md` | Identity inventory and executable membership can have different owners; a shared parser must not absorb consumer selection policy |
| `lib/dms/core/plan/AGENTS.md` | A contract for one path is not automatically valid for legacy and newer paths alike |
| `docs/design/online-offline-delivery-convergence/render-deployment-lifecycle.zh-CN.md`, input/runtime boundary | Distinguish source-derived frozen input from live target interactions by purpose, stage, and allowed writes |
| `docs/verify/INDEX.md` and `docs/verify/bootstraper/controller-verify.md` | Respect local-versus-real-environment execution limits and state exactly what each check proves |

No private paths, platform names, or environment commands enter the installed
skills. Go-specific schema/interface requirements remain in their repository.

## Where change-boundaries should be visible

Assessment added during draft review. The subsequent
[explicit setup decision](2026-09-18-coding-rule-setup-design.md) provides an
opt-in adoption path. Its approved follow-up splits and removes the mixed
code-quality reference, placing stage-specific methods in their owning skills.

The former change-boundaries reference mixed concerns with different earliest
use points. Root `AGENTS.md` and applicable module
instructions are the earlier surface; plugin catalogs and a plugin repository's
own `AGENTS.md` do not automatically provide rules to another target repository.
Moving a file to a shallower directory would not solve discovery by itself.

| Concern | Earliest useful surface | Detailed procedure |
|---|---|---|
| Preserve authorized scope and unrelated work | Concise applicable repository/agent instructions before edits | Git Change Scope plus workflow-specific attribution |
| Find the current owner before changing cross-module behavior | Repository responsibility map plus a conditional pre-change rule | Living contract and targeted design investigation |
| Respect existing authorization and verification limits | Applicable repository/agent instructions | Mode-specific review, commit, and verification handling |
| Resolve comparison base and classify failing gates | Relevant workflow entry | Git Change Scope and Verification Results references |

DMS already carries the owner/entry-flow rule in root `AGENTS.md`, and the
bootstrap template already directs agents to the owning flow before editing.
Do not duplicate them or copy the full generic reference into every repository.
For a target repository missing the early rule, a short, source-backed rule and
local contract pointer would be appropriate. User-level policy would be a
separate explicit choice, not a plugin-install side effect.

Pre-edit obligations must also reach small changes that never trigger
`architect`: preserve scope and unrelated work, honor authorization, locate the
relevant owner, and report verification honestly. Setup adapts missing obligations
into repository entry points once or on explicit update; it is not a per-task
preflight. `architect` supplies deeper investigation only for unresolved design
choices. Do not move universal obligations exclusively into its body or require
its invocation to satisfy them. If existing repository instructions already cover
the obligations, setup makes no additions.

`why` is an investigation procedure for missing rationale. The pre-change rule
is an expectation that applies even without invoking that procedure. Existing
context can satisfy it. `architect` deepens the analysis only when a design
choice is unresolved. Review checks the resulting change without requiring
proof that either skill ran.

The new design references overlap in subject with code-quality but serve a
different decision: choosing a design versus evaluating a concrete change.
No sibling-plugin runtime dependency is introduced. If identical normative
text later needs to be shared across plugins, define one source and build-time
copies with a drift check; do not hand-maintain duplicate policies or hard-code
an installed cache path. A cross-plugin distribution mechanism is not part of
this first draft.

## Knowledge and delivery boundaries

Return designs and explanations in the session by default. Update authoritative
contracts when an authorized implementation and repository rules require it.
Do not automatically invoke `learn`, record session plans as durable knowledge,
or create implementation scaffolds for a design-only request. Preserve the
separation between frozen historical records and living contracts.

This integration retains the plugin catalog entry. Verification uses isolated
local installations; it does not publish, commit, or change DMS or normal user
plugin configuration. Upstream MIT notices are maintained in the repository-root `LICENSE` under the
subsequently approved centralized license convention.
Behavioral scenarios and negative triggers are specified in
[Code Design Verification](../verify/code-design.md). Static validation cannot
establish behavioral improvement over the existing skills or native model.

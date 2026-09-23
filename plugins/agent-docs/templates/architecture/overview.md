# {{PROJECT_NAME}} Architecture

<!-- Adapt this template to verified current behavior. Remove inapplicable
     sections and all instructional placeholders. Reuse existing explanations
     instead of writing duplicates. Split by useful flow/topic only when needed.
     These questions guide coverage; they do not mandate layers or headings. -->

## System Context

{{PURPOSE_USERS_AND_EXTERNAL_BOUNDARIES}}

## Components and Responsibilities

| Component / owner package | Responsibility | Boundary / delegated work |
|---|---|---|
| {{COMPONENT_AND_PACKAGE}} | {{OWNED_DECISIONS_AND_EFFECTS}} | {{WORK_OWNED_ELSEWHERE}} |

## Core Flows

<!-- Describe each important flow from its registered entry or event to its
     outcome. Label handoff data and synchronous/asynchronous/external edges in
     prose or a diagram. Explain the owner of each meaningful transformation,
     admission decision, persistent effect, and state transition as applicable.
     A bare list of packages or call names is insufficient. -->
{{VERIFIED_FLOWS_AND_HANDOFFS}}

## Data and State Ownership

<!-- Identify authoritative data, readers and writers, immutable snapshots vs.
     dynamic inputs, and failure/retry/recovery owners where relevant. Reference
     canonical contracts for detailed schemas and state machines. -->
{{DATA_AUTHORITY_AND_LIFECYCLE_BOUNDARIES}}

## Compatibility and Contracts

{{ACTIVE_COMPATIBILITY_PATHS_AND_LINKS_TO_AUTHORITATIVE_CONTRACTS}}

## Evidence and Open Questions

<!-- State meaningful limits: inspected source/configuration does not prove
     deployment. Name important unverified flows or ownership questions. Do not
     create a maintained file/symbol evidence index or imply proposal = current. -->
{{VERIFIED_SCOPE_AND_UNRESOLVED_BOUNDARIES}}

# Explicit Repository Coding-rule Setup

**Status:** Approved for implementation
**Date:** 2026-09-18

## Problem

The former code-quality change-boundaries reference mixed constraints needed
before the first edit with review, cleanup, and commit procedures. Installing a plugin does not make its references active repository
instructions. Moving a reference to a shallower directory would not fix that.

DMS already places an owner/entry-flow rule in root `AGENTS.md`, with local
contract links and module rules for details. The agent-docs bootstrap template
also directs agents to existing owners, but many existing repositories lack
such early rules or only carry them in late-stage workflows.

## Decision

Add explicit `agent-docs:setup-coding-rules`. It inspects current instructions,
adapts selected pre-edit rules, and writes the smallest appropriate repository
surface. It is not invoked by plugin installation or normal coding.

This narrowly extends the rule against copying generic plugin policy from the
[Repository Knowledge Lifecycle](2026-08-03-repository-knowledge-lifecycle-design.md):
explicitly selected, adapted coding expectations may become repository policy.
The original bootstrap boundary and the prohibition on copying workflow internals
remain unchanged. The historical decision record is not rewritten.

The plugin owns candidate guidance. The target repository owns installed rules;
updates require another explicit request and semantic comparison with current
local text. No automatic synchronization, cache links, markers, or manifest are
required. The existing shared-reference fan-out makes the skill independently
usable when exposed outside the plugin directory.

## Responsibilities

| Capability | Boundary |
|---|---|
| bootstrap-agent-docs | Minimal entry point for an uninitialized repository |
| setup-coding-rules | Explicit initial setup or update of selected pre-edit coding expectations |
| remember / curate | Audit existing instruction / documentation surfaces |
| learn | Retrospectively capture new session knowledge |
| why / architect | Investigate missing rationale or resolve design choices; never mandatory for compliance with the early rule |
| code-quality | Assess concrete changes and run its workflow-specific gates |

Setup groups scope/work preservation, ownership, authorization, and verification
as candidate families. It installs only a requested subset, or considers these
families when none is specified. Domain-specific contracts are discovered and
linked, not invented. A small repository need not adopt cross-layer machinery.

## Follow-up: split the mixed reference

The approved follow-up removes `code-quality/references/change-boundaries.md`
and all four distributed copies after moving their responsibilities:

| Responsibility | Maintained source |
|---|---|
| Pre-edit scope, work preservation, ownership, authorization, honest verification | `agent-docs/references/pre-edit-coding-rules.md`; setup adapts it into repository-owned instructions |
| Review scope, architecture findings, authorized fixes, and readiness | `quality-reviewer/SKILL.md` |
| Cleanup attribution, behavior preservation, and reversible removal | `diff-cleanup/SKILL.md` |
| Exact commit candidate, staging preservation, skips, hooks, and result inspection | `clean-commit/SKILL.md` |
| Pre-fix ownership, authorized iterations, fresh verification/review, and convergence | `loopfix/SKILL.md` |
| Reused Git inventory/base-resolution mechanics | `code-quality/references/git-change-scope.md` |
| Reused check-result classification and safe baseline comparison | `code-quality/references/verification-results.md` |

The two narrow quality references contain reusable procedures, not a new umbrella
policy. Each quality skill retains the safeguards needed for its own task, so it
works even when setup has never run. There is no dependency on agent-docs at
runtime, no automatic repository installation, and no required architect call.
The setup candidate families already cover the early obligations; their meaning
does not expand merely because the old shared file is removed.

Keep the existing [change-boundary scenarios](../verify/change-boundaries.md) as
cross-workflow regression evidence; their historical name does not require an
installed reference with the same name. Shared references still use build-time
fan-out and drift checking, with obsolete copies explicitly removed.

## Authorization and conflicts

An apply/setup request authorizes scoped documentation edits without a second
approval. Report-only and explicit checkpoints remain effective. Specific local
policies win over generic candidates unless an explicit user decision resolves
the conflict. Preserve affected text and report unresolved decisions; independent
unambiguous additions can proceed. Do not label partial adoption complete.

Missing `AGENTS.md` permits a minimal selected-rule entry, not a full bootstrap
or placeholder documentation tree. Existing instruction entry points must be
inspected to avoid creating conflicting parallel rule sets. Longer material
uses normal repository documentation conventions only when needed.

## Verification and rollback

Use isolated repositories to test initial setup, semantic no-op/repeat runs,
report-only conflicts with unrelated staged work, missing entry points, and
subset-only installation. Direct skill reads are an explicit development
fallback; they do not prove installed catalog discovery or trigger selection.
Results are recorded in [setup verification](../verify/setup-coding-rules.md).

Rollback removes the new skill and its catalog entries; it does not delete rules
already adopted by a target repository. Those remain repository-owned and can
be changed through an explicit local edit. No target repository is modified by
implementing or installing the skill itself.

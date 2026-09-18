# Knowledge Admission and Workflow Ownership

**Status:** Approved and implemented; focused validation recorded separately
**Date:** 2026-09-18

## Decision

Keep `knowledge-admission.md` as the shared admission and placement standard for
agent-docs. It answers whether knowledge will help future work, what value is
missing from existing carriers, and which authoritative surface reaches the
reader at acceptable cost. It does not own an execution sequence or authorize
repository edits.

This supersedes automatic admission/retention of non-derivable facts and numeric
admission thresholds in the earlier knowledge-lifecycle policy. Non-derivability
is a reconstruction-cost signal, not proof of value. Derivable commands, maps,
and runbooks remain admissible when useful. Frozen historical design records
remain subject to local retention conventions; their age or divergence from
current code alone does not justify deletion.

## Responsibilities

| Owner | Responsibility |
|---|---|
| Shared admission reference | Evidence and authority, future use, residual value, placement, consistent capture/audit criteria |
| learn | Candidate-specific probes, current-session carriers, verification, proposals, and existing approval boundary |
| remember | Memory-scoped evidence for retention, removal, relocation, and targeted promotion |
| curate | Docs-scoped checks of replacement, operational/historical value, and existing approval boundary |
| setup-coding-rules | Explicit adoption, applicability, semantic coverage, conflicts, and early visibility |
| bootstrap-agent-docs | Minimal verified entry point; no knowledge-policy installation |

Use the same criteria across workflows without copying the full policy into each
body. Shared references remain build-time copies with the existing drift check.
A rule adopted by the user is an authoritative new expectation, not a fact about
past repository practice. Applicable local terminology and retention rules prevail.

## Boundaries and validation

Invocation, authorization, audit scopes, publication, and unrelated source edits
are unchanged. No generic setup installs this knowledge-maintenance policy into
target repositories. Fixed line targets and scores are removed from admission;
other workflow-specific format contracts are outside this change.

See [verification](../verify/knowledge-admission.md) for reproducible focused
requests and evidence limits. Earlier full workflow scenarios retain their raw
historical results; updating current expectations does not manufacture a rerun.

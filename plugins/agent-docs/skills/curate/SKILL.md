---
name: curate
description: Assess or repair existing repository knowledge across AGENTS.md and docs by topic or scope, including rule promotion, relocation, drift, and architecture boundaries. Use for explicit knowledge audits or curation; not session capture.
disable-model-invocation: true
argument-hint: [optional-topic-or-scope]
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

# Curate Repository Knowledge

Complete a scoped maintenance task across the relevant instruction entries,
architecture descriptions, contracts, rules, runbooks, and indexes. A relocation
or consistency repair has one owner even when it crosses `AGENTS.md` and `docs/`.
Read the shared [Authorization](references/authorization.md),
[Knowledge Admission](references/knowledge-admission.md), and
[Documentation Structure](references/doc-structure.md) references.

Use only for an explicit audit, curation, reorganization, or repair request. A
bare invocation audits without writing. Do not add automatic audits, hooks,
external memory systems, or mandatory calls to other skills. A direct named-doc
edit remains ordinary documentation work; session capture belongs to `learn`.

## Establish Scope

Resolve the repository and requested topic, module, files, or full-audit scope.
Inspect tracked, staged, unstaged, and untracked work before editing and preserve
unrelated bytes and staging. Do not require a clean checkout.

Scope follows the requested subject and authorization, not the file type. For
example, simplifying a DAO rule may require its early guard in `AGENTS.md`, its
explanation in an ORM guide, and its navigation entry to change together. Inspect
those related carriers; do not audit unrelated modules merely because they share
a file or directory. An explicit file allowlist is a hard write limit. If a
complete repair needs another destination, report that need and retain useful
text until the move is authorized.

For targeted rule promotion, identify the affected source package and inspect
its applicable ancestor instructions. Select the deepest existing `AGENTS.md`
covering the affected scope; do not default to whichever root entry was loaded
first. With multiple packages, choose their common applicable scope. Ask when
that scope cannot be established. Do not assume nested instructions load
implicitly.

For a repository-wide audit, identify main runtime components and core workflows
alongside the instruction and docs inventory. Check whether existing knowledge
explains their responsibilities, data handoffs, and state authority using the
shared architecture coverage questions. Include missing explanations as findings;
valid links and an absent architecture directory do not establish completeness.
Reuse adequate existing coverage wherever it lives. Report which flows were
checked and important gaps or unverified boundaries; do not claim full coverage
from a sample. A targeted audit applies this check only to its affected flow.

Prioritize by authority, task impact, known drift, and heavily used routes; do not
defer architecture by default behind prose or link cleanup. Read archives only
when relevant. Age, length, or missing directories alone do not establish a
defect. Exclude personal configuration and external memories; other repository
instruction files are relevant only within the requested scope.

## Check Each Carrier for Its Purpose

| Carrier | Questions |
|---|---|
| Root/module instructions | Are commands current and safe to copy? Which constraints need early visibility? Is the responsible package clear? Is a long explanation better linked? |
| Architecture | Are important flows covered, including ones with no existing document? Are purposes, data handoffs, authority, owners, and boundaries correct? Can an agent choose the responsible layer? Does navigation stop at packages while preserving normative exact paths? |
| Living contracts/rules | Is required behavior clear? Are implementation and verification states distinguished? Are callers using the stated contract? |
| Decision records | Is the historical decision preserved with an appropriate status or superseding pointer? Current source divergence alone is not drift in a frozen record. |
| Runbooks/verification | Are prerequisites, effects, runnable commands, and evidence limits correct? A dry-run is not proof of execution behavior. |
| Indexes/links | Can the reader reach the right authority? Are links/anchors valid? Avoid duplicated implementation progress and empty placeholder categories. |

Apply the shared value and placement criteria to all carriers. Keep useful
commands, rationale, and operational knowledge even when derivable. Remove
content only after verifying staleness, duplication, adequate replacement, or
lack of future use within local retention rules. Uncertain value is not proof of
uselessness. Do not impose a uniform line count or score.

## Verify Findings

Use the cheapest check that resolves the claim. Read the linked explanation,
current command registration, actual caller/wiring, or a focused local test as
needed. A file or symbol existing does not prove it serves the relevant flow.
Bound source inspection to the task; curation does not authorize product changes
or executing a real operational procedure.

For a misplaced rule, verify its affected package, existing coverage, and why it
needs earlier visibility. For a relocation, confirm the receiving carrier can
preserve the knowledge and necessary links before shortening the original. A
code comment may be an appropriate target only when source-comment edits are
within scope; otherwise report the needed extension.

For conflicting statements, use authoritative context and current evidence to
separate factual drift from an unresolved behavioral decision. Do not silently
rewrite the required contract to match a suspected product defect. Continue
independent repairs and identify what decision blocks the remainder.

For mixed codemaps, preserve useful architecture and rationale while removing
redundant file/private-symbol inventories. Keep exact rule targets, command
inputs/outputs, public contract names, and doc links under the shared exceptions.
Do not replace a stale line with another file/symbol index. Preserve frozen
historical evidence and avoid a directory-wide rename unless requested.

## Complete the Requested Operation

Report findings with their evidence, affected carriers, and proposed action:
retain, correct, relocate/promote, deduplicate, or remove. Identify unresolved
choices separately. Scale the report to the task; empty report sections add no
value.

For an assessment or proposal, stop at the requested checkpoint without edits.
For an authorized repair, apply the complete related change within scope, without
requiring another approval just because the destination crosses file categories.
Keep concise early guards while moving long explanations, and update required
links/indexes together. A partially completed relocation is pending work.

Reopen changed text, check links and relevant repository documentation gates,
and compare the final diff and staging with the initial inventory. Report what
changed, preserved constraints, actual checks and their limits, and anything
still unresolved. Do not run unrelated product tests merely to maintain prose.

---
name: setup-coding-rules
description: Set up or update repository coding rules that must be visible before edits. Use only for explicit requests to install or adapt coding rules; not ordinary coding, plugin installation, general docs audits, or session knowledge capture.
disable-model-invocation: true
---

# Set Up Coding Rules

Adapt explicitly requested pre-edit rules to a target repository's agent entry
points. The result belongs to that repository and remains usable without this
plugin. Installing a plugin alone never invokes this workflow.

An explicit adoption request establishes a new behavioral expectation, not proof
that the repository historically followed it. Verify applicability, semantic
coverage, conflicts, and early visibility before writing. Preserve local
constraints; do not manufacture past evidence or copy plugin workflow internals.
This scope does not expand bootstrap's minimal payload.

## Establish scope and intent

Resolve the target from the request and current context; ask only if ambiguous.
Confirm its repository root and relevant instruction scope. Inventory tracked,
staged, unstaged, and untracked work before editing, preserving unrelated bytes
and staging. Do not stash, reset, stage, commit, install tools, or change personal
agent configuration as part of setup.

An explicit setup/apply request authorizes the relevant document edits. Preview
is not a second approval gate: describe the intended small change and proceed.
For assessment/preview-only requests, inspect and report without writing. Honor
an explicit checkpoint. Ask only about material unresolved conflicts or scope.

Read [Pre-edit Coding Rules](references/pre-edit-coding-rules.md) as candidate
semantics, not a template to copy. If the user selected a subset, use only it;
otherwise consider the core families there. Setup does not authorize unrelated
coding standards, new quality gates, or a required skill-call sequence.

## Inspect coverage before choosing text

Read existing root and relevant module `AGENTS.md` files, repository coding
rules, and the contracts they actually route to. Follow task-relevant links;
do not audit all documentation or reconstruct the entire architecture. Sample
an actual entry flow only where needed to establish an ownership rule's scope.
Do not guess responsibilities from directory names.

Classify each selected rule family by meaning:

- **Covered:** current visible instructions already express the requirement.
  Preserve them, even if their wording or heading differs.
- **Missing or misplaced:** a useful pre-edit requirement is absent or reachable
  only after a later workflow. Add the smallest early rule or local pointer.
- **Conflict:** local policy and the proposed rule disagree. Prefer an explicitly
  resolved user decision; otherwise retain local policy and report the conflict.
- **Not applicable:** the repository lacks the relevant kind of work. Omit the
  rule; a small script needs no imaginary admission or distributed-state model.

A mere link to review/commit instructions does not make a pre-edit requirement
visible soon enough. Conversely, an early conditional rule plus a local contract
pointer is adequate; do not inline the whole contract. Reuse relevant, verified
session evidence when it still applies.

## Adapt and apply

Place cross-cutting pre-edit expectations in root `AGENTS.md`; place genuinely
module-specific rules in the nearest applicable `AGENTS.md`. Match repository
language and terminology. Prefer editing the existing relevant section over
adding a new one. Link existing authoritative local docs for details.

If no `AGENTS.md` exists, create only a minimal root entry containing the selected,
applicable rules and any verified pointers needed to use them. Do not run a full
bootstrap, invent commands, or create placeholder architecture/docs categories.
If another established instruction entry exists, inspect its relationship to
`AGENTS.md` first and avoid conflicting parallel rule sets.

Longer material belongs in an existing suitable local document when necessary;
follow the repository's documentation conventions. Consult
[Knowledge Admission](references/knowledge-admission.md) only when deciding
whether extra explanatory material merits a new durable surface. Do not create
a separate policy file merely to hold these short rules.

Keep installed-cache paths, personal absolute paths, plugin workflow internals,
model assignments, and mandatory why/architect/reviewer calls out of repository
rules. Do not install review, cleanup, commit, or fix-loop procedures as coding rules. Target text must stand alone
or resolve through repository-relative links after the plugin is uninstalled.

On repeat/update runs, compare meaning against the current target, including
local edits. Do not replace a generated block by upstream version or append a
second equivalent rule. No marker, sidecar manifest, or synchronization daemon
is needed. The repository owns its rules after setup.

Apply independent unambiguous additions when authorized, leaving unresolved
conflicting rules untouched. Explain what decision is needed for that part;
do not mark partial setup complete. Preserve stricter environment verification
limits and valid project-specific approval requirements unless explicitly
changed by the user.

## Verify and report

Reopen the changed entry points and check that the intended rule is visible
before the relevant edit, each new link resolves locally, and no equivalent rule
was added twice. Inspect the diff and recheck that unrelated work and staging
are intact. Run relevant documentation checks where available; do not launch
product integration checks merely to install prose rules.

Report changed files and applied rule families, already-covered/not-applicable
families, unresolved conflicts, and actual checks. A fully covered repository is
a successful no-op. A report-only run stays report-only. No behavioral compliance
claim follows from the presence of a rule: setup verifies placement and content,
not that every future agent will obey it.

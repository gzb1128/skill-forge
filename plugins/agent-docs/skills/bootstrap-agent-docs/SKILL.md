---
name: bootstrap-agent-docs
description: Bootstrap a repository that lacks AGENTS.md with verified commands and architecture coverage. Use for explicit bootstrap, init, or scaffold agent-docs requests.
---

# Bootstrap Agent Documentation

Create a concise root `AGENTS.md` and establish useful architecture coverage for
the system's core flows. Read the shared
[Authorization](references/authorization.md),
[Knowledge Admission](references/knowledge-admission.md), and
[Documentation Structure](references/doc-structure.md) references. Installing the
plugin does not initialize a repository.

## Scope

Use for an explicit bootstrap/init request when the repository lacks a usable
agent entry point. Resolve the target from the request and session context; ask
only if ambiguous. Confirm the repository root and inspect existing instruction
files and tracked, staged, unstaged, and untracked work.

If a project `AGENTS.md` already exists, preserve it and explain the needed
maintenance. An explicit repair request can use curation's existing-entry scope;
do not overwrite or merge it through bootstrap. Creating a specific document,
session capture, and coding-rule adoption retain their own task boundaries.

Bootstrap creates root `AGENTS.md` and, when the system needs separate architecture
explanation, the missing useful architecture documents and navigation. A simple
tool may be fully explained in the root entry. For multiple runtime components,
cross-package business workflows, or asynchronous processing, default to a linked
overview in `docs/architecture/`; reuse adequate existing material instead of
creating a second account. Add topic documents only when they improve navigation.
Do not scaffold empty categories or copy a complete template tree.

## Packaged Template

Read [the bundled template](assets/templates/AGENTS.md) relative to this skill's
loaded directory, not the target repository's working directory. When a separate
overview is needed, adapt the bundled [architecture template](assets/templates/architecture/overview.md)
and [index template](assets/templates/architecture/INDEX.md). Both plugin and
standalone skill distributions carry these assets inside the skill. No plugin-root
environment variable or source checkout is required.

Resolve the absolute directory containing the loaded `SKILL.md` using the
runtime-provided skill path. If that location or its asset is unavailable,
report the missing package resource instead of guessing a path or downloading
another template. The template is a starting point; adapt it before writing the
result so unfinished placeholders are never presented as usable commands.

## Inspect and Adapt

- Read the build manifests and command definitions. Distinguish a command's
  existence from successful execution; run only relevant safe local checks.
- Identify the main runtime components and core workflows, then trace their
  registered entries, wiring, and meaningful data handoffs. Apply the shared
  architecture coverage questions: an existing document inventory cannot reveal
  an undocumented flow. Bound the initial description to verified evidence and
  make important unknowns explicit. Navigation stops at packages; preserve exact
  normative paths under the Source References exceptions.
- Keep high-impact rules that need early visibility and route longer explanations
  to existing contracts. Do not invent project conventions or mandatory layers.
- Replace applicable template fields with verified facts. Omit irrelevant rows
  and sections. Describe important unknown commands in prose; do not leave
  `{{...}}`, TODO hints, or fabricated executable commands in the result.
- Keep the entry proportionate to recurring tasks without a fixed line target.

Summarize the detected facts, existing coverage, and intended output paths. A preview request
stops here with a concrete proposal; an explicit bootstrap request proceeds
under existing authorization without another routine approval.

## Apply and Verify

Create adapted documents only at still-absent destinations. Recheck immediately
before writing and use exclusive file creation so concurrent work is preserved.
If a destination appeared during inspection, read and reuse it when adequate;
report any remaining conflict instead of overwriting it. Complete receiving
documents before publishing new links; preserve existing indexes and add only
the needed navigation entries within scope.

Reopen the result, verify local links, inspect remaining placeholders, and compare
Git status with the initial inventory. Preserve existing content and staging;
report created paths, any navigation additions, the components and flows actually
checked, and remaining coverage gaps. An explicit file allowlist limits writes:
report uncovered architecture without inventing completeness or expanding scope.
Do not claim command execution, installed discovery, deployed behavior, or a
complete repository knowledge base from a successful template write.

For subsequent work, `curate` maintains existing repository knowledge, `learn`
captures explicit session insights, and `setup-coding-rules` adopts selected
pre-edit rules. These are independent task choices, not a required sequence.

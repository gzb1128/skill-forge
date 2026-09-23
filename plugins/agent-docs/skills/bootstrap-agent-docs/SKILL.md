---
name: bootstrap-agent-docs
description: Bootstrap a repository that lacks AGENTS.md with a minimal, verified command and architecture entry point. Use for explicit bootstrap, init, or scaffold agent-docs requests.
---

# Bootstrap Agent Documentation

Create a minimal root `AGENTS.md` with useful commands, package responsibilities,
and necessary local constraints. Read the shared
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

Bootstrap creates only root `AGENTS.md`. Do not create overflow documents,
placeholder indexes, or empty documentation categories. Existing authoritative
local documents may be linked.

## Packaged Template

Read [the bundled template](assets/templates/AGENTS.md) relative to this skill's
loaded directory, not the target repository's working directory. Both plugin and
standalone skill distributions include `assets/templates/AGENTS.md` inside this
skill. No plugin-root environment variable or source checkout is required.

Resolve the absolute directory containing the loaded `SKILL.md` using the
runtime-provided skill path. If that location or its asset is unavailable,
report the missing package resource instead of guessing a path or downloading
another template. The template is a starting point; adapt it before writing the
result so unfinished placeholders are never presented as usable commands.

## Inspect and Adapt

- Read the build manifests and command definitions. Distinguish a command's
  existence from successful execution; run only relevant safe local checks.
- Follow a relevant registered entry and its wiring when needed to establish
  responsibilities. Describe components and flows at package granularity;
  preserve exact normative paths under the Source References exceptions.
- Keep high-impact rules that need early visibility and route longer explanations
  to existing contracts. Do not invent project conventions or mandatory layers.
- Replace applicable template fields with verified facts. Omit irrelevant rows
  and sections. Describe important unknown commands in prose; do not leave
  `{{...}}`, TODO hints, or fabricated executable commands in the result.
- Keep the entry proportionate to recurring tasks without a fixed line target.

Summarize the detected facts and intended one-file result. A preview request
stops here with a concrete proposal; an explicit bootstrap request proceeds
under existing authorization without another routine approval.

## Apply and Verify

Create the adapted root entry only if it is still absent. Recheck immediately
before writing and use exclusive file creation so concurrent work is preserved.
Do not copy the template tree blindly or overwrite another entry that appeared
while inspecting the repository.

Reopen the result, verify local links, inspect remaining placeholders, and compare
Git status with the initial inventory. Bootstrap must add only root `AGENTS.md`
and preserve existing work and staging. Report created paths, checks actually
run, and unresolved facts. Do not claim command execution, installed discovery,
or a complete repository knowledge base from a successful template write.

For subsequent work, `curate` maintains existing repository knowledge, `learn`
captures explicit session insights, and `setup-coding-rules` adopts selected
pre-edit rules. These are independent task choices, not a required sequence.

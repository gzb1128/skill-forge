---
name: learn
description: Use when the user says "learn", "save this insight", or wants to persist non-obvious knowledge from the current session to AGENTS.md
disable-model-invocation: true
argument-hint: [optional-context]
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

> **Manual-trigger skill.** `disable-model-invocation: true` keeps the model from
> invoking this workflow automatically mid-task. When installed from this plugin,
> invoke it deliberately as `/agent-docs:learn` at the end of a session.
> Do not add hooks, background tasks, auto-trigger behavior, runtime storage,
> vector databases, MCP integration, or external memory systems.

Review what happened in this session and produce verified, reviewable memory
proposals for the appropriate `AGENTS.md` file using the exact-diff workflow
below.

## Non-Derivability Principle

**Only record information that CANNOT be derived from the codebase itself.**
Before proposing any `Hidden Knowledge` entry, ask:

> Can the next agent or human discover this by reading the code, running
> `git log`, or checking existing docs?

If yes, do NOT record it as hidden knowledge. The bar is high. Most knowledge
belongs in source, commit messages, or existing docs, not in `AGENTS.md`.

## Step 1: Extract candidate insights

Review the current session and list candidate insights. Candidates usually come
from hidden dependencies, misleading failures, project-specific workarounds,
critical ordering, command discovery, or documentation gaps.

Do not write anything yet. First classify each candidate.

## Step 2: Classify candidates

| Classification | Destination | Rule |
|----------------|-------------|------|
| `Hidden Knowledge` | Nearest relevant `AGENTS.md` under `## Hidden Knowledge` | Only for non-derivable hidden dependencies, misleading errors, workarounds, quirks, or critical ordering |
| `Quick Reference` | Root `AGENTS.md` Quick Reference table | Build, test, lint, run, codegen, clean, or other common commands |
| `Rule` | Report suggested destination only | Team convention or hard boundary; do not create or modify `docs/rules/` from `/agent-docs:learn` |
| `Doc` | Report suggested destination only | Longer design, troubleshoot, runbook, or library note; do not create or modify docs from `/agent-docs:learn` |
| `Skip` | No write | Derivable, one-off, duplicated, stale, generic, or unverifiable |

## Hidden Knowledge candidates

Only candidates that pass the non-derivability test may become hidden knowledge:

1. **Hidden dependencies (coupling conventions)**: Files or modules that must be
   changed together but are not obviously connected. These look derivable — a
   `diff` can show two files currently match — but the "must stay in sync" rule
   is an unwritten convention the compiler/linter/git does not enforce. Record
   it. Objective bar: acting on the insight requires **≥2 artifacts plus a
   convention not written in any single file**.
2. **Misleading errors**: Error messages that point to the wrong location or
   cause.
3. **Workarounds and quirks**: Project-specific behavior that differs from the
   standard pattern.
4. **Critical ordering**: Operations that must happen in a specific sequence,
   especially cross-artifact ordering (e.g. SQL migration before code) that no
   single file states.

## Skip criteria

Skip candidates that are:

- Code patterns, architecture, or file structure visible by reading source.
- Git history or recent changes that `git log` or `git blame` already records.
- Debugging solutions where the fix is now in code and the commit message should
  carry the context.
- Already present in `AGENTS.md`, `docs/rules/`, or README.
- Standard language or framework behavior.
- Non-obvious commands that belong in Quick Reference, not Hidden Knowledge.
- Ephemeral session details, including attempts that failed temporarily.
- Unverified claims.

## Step 3: Verify each retained candidate

Every retained candidate needs explicit evidence before it can be proposed:

| Candidate mentions | Verification evidence |
|--------------------|-----------------------|
| File path | Confirm the path exists with `ls` or by reading the file |
| Function, type, command, or symbol | Confirm it exists with search or a language-aware lookup |
| Behavior or constraint | Run the smallest relevant command, inspect source, or explain why direct execution is unsafe |
| Existing AGENTS.md content | Read the target section and check for stale or duplicate entries |

If verification fails, classify the candidate as `Skip` and explain the failed
check. If verification cannot be performed safely, report it as unverified and
do not propose a write.

## Step 4: Choose the target

Choose the nearest `AGENTS.md` to the affected scope:

| Scope of insight | Target file |
|------------------|-------------|
| Affects entire project | Root `AGENTS.md` |
| Affects a specific package | `<package>/AGENTS.md` |
| Affects a complex module | `<package>/<module>/AGENTS.md`, only if sub-package criteria are met |

For `Hidden Knowledge`, append to or create a `## Hidden Knowledge` section near
the end of the target `AGENTS.md`. Keep each insight to 1-3 lines.

For `Quick Reference`, propose a row update in the root `AGENTS.md` table.

For `Rule` and `Doc`, report the suggested destination only. Do not create or
modify rule docs, design docs, troubleshoot docs, runbooks, or library docs from
this command.

## Step 5: Show proposed changes first

Before editing any file, show all proposals in this format:

````markdown
## Learn Proposals

### 1. `<classification>` -> `<target file>`

**Why:** <one-line reason this helps future sessions>

**Verification:** <path/symbol/command/behavior evidence>

**Action:** <add/update/skip/report-only>

```diff
- <existing line, only when updating an approved existing entry>
+ <exact proposed addition or replacement>
```

### Skipped Candidates

1. `<candidate>` -> skipped because <reason>

### Report-Only Suggestions

1. `<candidate>` -> belongs in <suggested destination>, not handled by `/agent-docs:learn`
````

## Step 6: Approval gate and apply

Stop after showing the exact proposed changes, even if the user asks to apply
quickly. After explicit approval:

1. Apply only the proposals the user approved.
2. Preserve existing `AGENTS.md` structure and keep additions concise.
3. Do not perform general cleanup from `/agent-docs:learn`; use `/agent-docs:remember` for stale,
   duplicated, or misplaced existing memory.
4. Report what changed, where it changed, which candidates were skipped, and
   any remaining report-only suggestions.

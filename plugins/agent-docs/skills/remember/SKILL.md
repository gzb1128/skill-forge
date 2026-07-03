---
name: remember
description: Use when the user says "remember", "audit knowledge", or wants to review and reorganize AGENTS.md memory for staleness, duplication, and misplacement
disable-model-invocation: true
argument-hint: [optional-scope]
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

> **Manual-trigger skill.** `disable-model-invocation: true` keeps the model from
> running memory audits automatically mid-task. When installed from this plugin,
> invoke it deliberately as `/agent-docs:remember` when you want to clean
> up. Do not add hooks, background tasks, auto-trigger behavior, runtime storage,
> vector databases, MCP integration, or external memory systems.

Review all `AGENTS.md` files across the project and produce a structured
`Memory Health Report`. Default behavior is report-only. Do not edit files until
the user has reviewed the proposals and explicitly approved the changes.

## What this does

This is the complement to `/agent-docs:learn`:

- `/agent-docs:learn` proposes verified memory additions from the current session.
- `/agent-docs:remember` audits existing `AGENTS.md` memory surfaces for staleness,
  duplication, misplacement, and low-signal content.

## Step 1: Gather memory layers

Read all project `AGENTS.md` files. Typical layers include:

```text
AGENTS.md
internal/<package>/AGENTS.md
<other-package>/AGENTS.md
```

Do not read or modify personal preference files such as `~/.claude/CLAUDE.md` or
`~/.config/opencode/AGENTS.md` from this command. This command audits project
memory only.

## Step 2: Audit memory surfaces

Audit every relevant `AGENTS.md` memory surface, not only `## Hidden Knowledge`.
Apply the quality rubric to `AGENTS.md` content only. Do not search for,
score, or update `CLAUDE.md` files; this skill's scope is project agent memory.

| Surface | Checks |
|---------|--------|
| `Quick Reference` | Commands/workflows exist, placeholders are removed, commands are current or explicitly marked as examples |
| `Architecture` | Gives agents a clear entry map, key directories, and module relationships without becoming a copied source-code encyclopedia |
| `Key Patterns` | Captures project-specific, non-obvious patterns that are still true, not generic advice, not replaced by mechanical enforcement |
| `Golden Rules` | Still hard rules, not duplicated from `docs/rules/`, not better represented as links |
| `Hidden Knowledge` | Non-derivable gotchas, quirks, critical ordering, or misleading failures; verified, not stale, not duplicated, correctly placed |
| Sub-package `AGENTS.md` | Still justified by complexity, cross-module constraints, state machines, or special verification needs |

## Step 3: Classify issues by quality dimension

Use these dimensions to explain every finding. Prefer concrete evidence over
numeric grades; do not produce an overall score.

| Dimension | Meaning |
|-----------|---------|
| `Commands/Workflows` | Essential build, test, lint, verify, install, or project workflows are present, current, and have enough context to run safely |
| `Architecture Clarity` | `AGENTS.md` maps the codebase, entry points, and relationships well enough for a future agent to start in the right place |
| `Non-Obvious Patterns` | Gotchas, quirks, critical ordering, and "why this is different" knowledge are captured without restating visible code |
| `Conciseness` | Each line earns prompt space; remove filler, template residue, obvious advice, and long explanations better suited for docs |
| `Currency` | Paths, commands, symbols, and described behavior are still true |
| `Actionability` | A future agent can follow the instruction directly with concrete commands, paths, or decision rules |
| `Signal` | The content is worth prompt space and helps future agents act better |
| `Placement` | The content lives at the right `AGENTS.md` level and section |
| `Non-Derivability` | Hidden knowledge cannot now be inferred from code, git, or existing docs |
| `Duplication` | The same guidance is not repeated across layers or docs |

If a `CLAUDE.md` quality criterion appears useful, map it to one of the
dimensions above before reporting. Never switch the audit target from
`AGENTS.md` to `CLAUDE.md`.

## Step 4: Verify findings

Before proposing a cleanup, verify it:

| Finding type | Verification |
|--------------|--------------|
| Missing or stale file path | Check the path exists |
| Missing function, type, command, or symbol | Search for the referenced name |
| Stale command | Run the safest relevant command, or explain why execution is unsafe |
| Contradicted behavior | Inspect source or run the smallest relevant check |
| Duplicate content | Cite both locations |
| Now-derivable hidden knowledge | Cite the code, docs, git history, or AGENTS.md main-body section that now covers it |
| Memory assertion backed by a linked doc | Open that one linked doc and confirm it still supports the assertion |

If a finding cannot be verified, label it `Needs user input` instead of treating
it as fact.

**Scope guard — linked docs are a verification method, not an audit target.**
Open only the specific doc a memory assertion links to, confirm it still supports
that assertion, and stop. Do **not** enumerate `docs/`, score doc quality, or
traverse cross-links; doc-level quality (including redundancy) is owned by a
separate audit, not `/agent-docs:remember`. The economics differ — `AGENTS.md`
is prompt-resident and judged by Signal / Conciseness / Non-Derivability, while
`docs/` is pull-based and may legitimately be longer or more detailed — but
both stay subject to the repo's non-derivability rule. The only question here is
whether the linked doc still backs the memory claim that cites it.

## Step 5: Classify actions

| Action | Use when |
|--------|----------|
| `Promotions` | Lower-level guidance affects multiple packages or belongs in a higher-level `AGENTS.md` surface |
| `Deletions` | Content is stale, duplicated, generic, now derivable, or no longer useful |
| `Rewrites` | Content is true but unclear, too verbose, misplaced within the same file, or missing verification context |
| `Duplicates` | Exact or overlapping guidance appears in multiple places |
| `Conflicts` | Two files or sections contradict each other and need user judgment |
| `No Action Needed` | Content is valid, placed correctly, and useful |

**Rewrite heuristic — prefer stable references over line numbers.** When memory
points at source, prefer stable references (symbol name, package path, heading
anchor, or file) over line numbers. Line numbers drift on every unrelated edit,
so a stale `file.go:42` is a recurring false signal. If a cited line number no
longer points at the named symbol, propose a `Rewrite` to the symbol/package form
(e.g. `the Run method in deploy_v3.go`) rather than just bumping the number —
bumping only fixes it until the next edit.

Do not auto-delete, auto-merge conflicts, or apply cleanups without approval.

## Step 6: Present the report

Output a structured report:

```markdown
## Memory Health Report

### Summary

- Files reviewed: <count and paths>
- Surfaces reviewed: <Quick Reference / Architecture / Key Patterns / Golden Rules / Hidden Knowledge / sub-package AGENTS.md>
- Changes proposed: <count>
- Items needing user input: <count>

### Promotions

1. `<source file>`: "<entry>" -> move to `<target file>` because <dimension + verification evidence>

### Deletions

1. `<file>`: "<entry>" -> delete because <dimension + verification evidence>

### Rewrites

1. `<file>`: "<entry>" -> rewrite as "<new wording>" because <dimension + verification evidence>

### Duplicates

1. "<entry>" appears in `<file A>` and `<file B>` -> keep `<file A>`, remove `<file B>` because <reason>

### Conflicts

1. `<file A>` says "X" but `<file B>` says "Y" -> needs user input: <question>

### No Action Needed

<brief note on entries that are valid and well-placed>
```

If no `AGENTS.md` memory surfaces exist beyond placeholders, say so and suggest
running `/agent-docs:learn` at the end of a future session that discovers non-obvious
knowledge.

## Step 7: User approval

- Present all proposals before making any changes.
- Do not modify files without explicit user approval.
- The user may approve all, approve some, reject all, or ask for revisions.
- For conflicts, ask which version is correct before editing.
- Apply only approved changes.

## Procedure

1. Find and read all project `AGENTS.md` files.
2. Audit `Quick Reference`, `Architecture`, `Key Patterns`, `Golden Rules`,
   `Hidden Knowledge`, and sub-package `AGENTS.md` justification.
3. Verify each finding with paths, search, command output, source inspection, or
   an explicit `Needs user input` label.
4. Classify findings as `Promotions`, `Deletions`, `Rewrites`, `Duplicates`,
   `Conflicts`, or `No Action Needed`.
5. Present the full `Memory Health Report`.
6. Wait for explicit user approval.
7. Apply approved changes only.
8. Report applied changes, rejected proposals, unresolved conflicts, and residual
   risks.

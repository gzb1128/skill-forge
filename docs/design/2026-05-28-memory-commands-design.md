# Design: Improve Memory Commands

**Status:** Superseded by [Repository Knowledge Lifecycle](2026-08-03-repository-knowledge-lifecycle-design.md)
**Date:** 2026-05-28
**Author:** OpenCode

## Problem

The plugin provides memory management through `plugins/agent-docs/skills/learn/SKILL.md` and `plugins/agent-docs/skills/remember/SKILL.md`: `/agent-docs:learn` captures non-obvious knowledge from a session, while `/agent-docs:remember` periodically audits existing `AGENTS.md` content. This direction is sound, but the command boundaries are incomplete. `/agent-docs:learn` is too write-oriented and lacks a structured proposal before writing. `/agent-docs:remember` focuses too narrowly on `## Hidden Knowledge` and does not cover memory surfaces such as `Quick Reference`, `Key Patterns`, and `Golden Rules`.

Compared with `claude-md-management`, the useful ideas are reviewable diffs, quality dimensions, and repository cross-checking. Its looser recording standards should not be adopted because they would weaken the template's core advantage: strict non-derivability, preventing `AGENTS.md` from becoming an encyclopedia.

## Goals

- Improve `/learn` write quality: classify, verify, show a diff, then write only after user approval.
- Improve `/remember` audit coverage: expand from `Hidden Knowledge` only to all `AGENTS.md` memory surfaces.
- Preserve the manual trigger model: commands remain markdown command bodies and are not automatically integrated into any agent runtime.
- Preserve the non-derivability principle: only information that cannot be derived from code, git history, or existing docs may enter `Hidden Knowledge`.

## Non-Goals

- Do not implement agent integration, auto-triggering, background jobs, hooks, MCP, vector databases, or long-term external memory storage.
- Do not promote `/learn` or `/remember` into automatically loaded skills.
- Do not require every development session to run memory commands.
- Do not address every documentation-quality issue in this design; this design only covers `AGENTS.md` memory commands.

## Proposed Design

### Architecture

Memory remains two manual commands:

| Command | Role | Default Write Behavior |
|---------|------|------------------------|
| `/learn` | Extract candidate knowledge from the current session and propose writes | Show a diff first; write only after user approval |
| `/remember` | Audit existing `AGENTS.md` memory surfaces and propose cleanup | Report by default; edit only after user approval |

Both commands share one memory lifecycle:

```text
candidate insight -> classify -> non-derivability filter -> verify -> route -> propose diff -> approve -> apply/audit later
```

### `/learn` Flow

`/learn` should move from "append insight directly" to "produce a reviewable memory proposal first." When candidate content clearly belongs in another documentation surface, the command should report the suggested destination only; it should not create or modify those documents as part of the `/learn` flow.

1. Review the current session and extract candidate insights.
2. Classify each candidate as `Hidden Knowledge`, `Quick Reference`, `Rule`, `Doc`, or `Skip`.
3. Apply the non-derivability test to `Hidden Knowledge`; skip information that can be derived from code, git history, or existing docs.
4. Collect verification evidence for retained candidates, such as path existence, symbol existence, command execution, or confirmation that the behavior still holds.
5. For each proposed change, show the target file, target section, rationale, and diff.
6. Edit files only after user approval.
7. Report actual write locations and skip reasons.

Classification rules:

| Classification | Destination | Rule |
|----------------|-------------|------|
| `Hidden Knowledge` | `## Hidden Knowledge` in the nearest-scoped `AGENTS.md` | Record only non-derivable hidden dependencies, misleading errors, special ordering, and project quirks |
| `Quick Reference` | Root `AGENTS.md` Quick Reference table | Common build, test, lint, and run commands |
| `Rule` | Report suggested destination only | Team conventions or hard boundaries; `/learn` must not auto-create rule docs |
| `Doc` | Report suggested destination only | Longer design, troubleshooting, runbook, or library notes; `/learn` must not auto-create docs |
| `Skip` | Do not write | Derivable, one-off, duplicate, stale, or generic advice |

### `/remember` Flow

`/remember` should expand from checking only `## Hidden Knowledge` to checking all `AGENTS.md` memory surfaces. It still reports by default and does not edit files unless approved.

Audit scope:

| Surface | Checks |
|---------|--------|
| `Quick Reference` | Commands still exist, placeholders are removed, commands can run or can be reasonably verified |
| `Architecture` | Still an entry map, not copied source-code detail |
| `Key Patterns` | Project-specific, still true, not superseded by mechanical rules |
| `Golden Rules` | Still hard rules, not duplicated by `docs/rules/`, downgraded to links when appropriate |
| `Hidden Knowledge` | Non-derivable, still verifiable, not duplicated, correctly placed |
| Sub-package `AGENTS.md` | Still justified by complexity or cross-module constraints |

Report format becomes `Memory Health Report`:

| Dimension | Meaning |
|-----------|---------|
| Signal | Whether the content is worth prompt space |
| Placement | Whether it is in the correct layer and section |
| Currency | Whether paths, commands, and behavior are still true |
| Non-Derivability | Whether the information can now be derived from code, git, or docs |
| Duplication | Whether it duplicates another `AGENTS.md` or rule doc |
| Actionability | Whether a future agent can directly execute or obey it |

The report should use these groups:

```markdown
## Memory Health Report

### Promotions
### Deletions
### Rewrites
### Duplicates
### Conflicts
### No Action Needed
```

### Data Flow

`/learn` is the producer: it generates candidate memory from session context and writes verified content to the correct location after user approval. `/remember` is the garbage collector: it scans existing memory and proposes deletion or rewrites for stale, derivable, duplicated, or misplaced content. Both commands use `AGENTS.md` as the only shared state and do not depend on external systems.

```text
session context --/learn--> AGENTS.md memory surfaces --/remember--> cleanup proposals
```

### Error Handling

- If a candidate insight cannot be verified, `/learn` must skip it and state what evidence is missing.
- If the target location is unclear, `/learn` should propose candidate destinations and ask for confirmation instead of guessing.
- If `/remember` finds a conflict, it should keep both versions and ask the user to decide; it should not merge them on its own.
- If a command cannot actually be run, record "not verified" and why, instead of claiming it is valid.
- If there is nothing to write or clean up, report "no action" explicitly to avoid polluting docs just to produce output.

### Testing Strategy

This design is primarily verified through prompt-body examples and manual review. Implementation should at least run these checks:

- Manually exercise `/remember` against an example `AGENTS.md` that contains `Quick Reference`, `Golden Rules`, and `Hidden Knowledge`.
- Manually exercise `/learn` classification against a session sample containing derivable, non-derivable, duplicate, and unverifiable candidates.
- Check that command bodies still clearly require manual triggering and do not imply automatic integration.
- Check that all new guidance follows the non-derivability principle and does not encourage copying code structure into `AGENTS.md`.
- Check that the implementation diff only modifies `plugins/agent-docs/skills/learn/SKILL.md` and `plugins/agent-docs/skills/remember/SKILL.md`, unless the user separately approves docs, index, or rule updates.
- Check that both commands explicitly prohibit agent integration, hooks, auto-triggering, runtime storage, vector databases, or external memory systems.
- Check that `/remember` remains report-first and does not edit files before user approval.

## Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Minimal patch: add diffs to `/learn` and a small stale check to `/remember` | Small change, low risk | Does not solve incomplete memory-surface coverage | Rejected |
| Structured lifecycle: unify capture, classify, verify, route, audit | Covers the core problem while keeping commands simple | Requires rewriting both command bodies | Chosen |
| Full governance system: add scores, fixtures, a separate audit command, and template library | Most comprehensive | Too heavy for the current template and risks drifting away from "commands and skills only" | Rejected |

## Migration / Rollout

1. Update `plugins/agent-docs/skills/learn/SKILL.md` with the classification table, verification evidence requirements, diff proposal, and user confirmation step.
2. Update `plugins/agent-docs/skills/remember/SKILL.md` to audit all `AGENTS.md` memory surfaces and output a `Memory Health Report`.
3. By default, implementation touches only those two command files; any explanatory docs, indexes, or rule docs require separate confirmation.

## Open Questions

- Does `/remember` need a score? Decision: no total score for now; use dimensional reporting to avoid turning audits into ceremonial grading.

Decision recorded: `/learn` does not skip diffs or user confirmation. Even when the user wants a fast apply, they must see and approve the concrete changes first.

## Related

- Skill: `plugins/agent-docs/skills/learn/SKILL.md`
- Skill: `plugins/agent-docs/skills/remember/SKILL.md`
- Rule: `docs/rules/non-derivability.md`
- Rule: `docs/rules/document-conventions.md`

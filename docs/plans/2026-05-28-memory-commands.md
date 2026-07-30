# Memory Commands Improvement Implementation Plan

**Status:** Completed; behavior subsequently superseded by
[Repository Knowledge Lifecycle](../design/2026-08-03-repository-knowledge-lifecycle-design.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve `plugins/agent-docs/skills/learn/SKILL.md` and `plugins/agent-docs/skills/remember/SKILL.md` according to `docs/design/2026-05-28-memory-commands-design.md`.

**Architecture:** Modify only the two manually triggered command bodies. Do not add agent integration, hooks, auto-triggering, runtime storage, vector databases, or external memory systems. `/learn` classifies candidate session memory, verifies it, proposes a diff, and writes only after confirmation; `/remember` audits the health of `AGENTS.md` memory surfaces and cleans up only after confirmation.

**Tech Stack:** Markdown command bodies, `AGENTS.md`, repository documentation conventions.

---

### Task 1: Update `/learn` Command

**Files:**
- Modify: `plugins/agent-docs/skills/learn/SKILL.md`

- [x] **Step 1: Preserve the manual trigger boundary**

Confirm that the file still states it is a manual-trigger command and does not suggest auto-loading, hooks, background jobs, or agent runtime integration.

- [x] **Step 2: Add candidate insight classification**

Add a classification table after the non-derivability principle: `Hidden Knowledge`, `Quick Reference`, `Rule`, `Doc`, and `Skip`. `Rule` and `Doc` may only report suggested destinations; `/learn` must not auto-create or modify those documents.

- [x] **Step 3: Strengthen pre-write verification**

Change verification requirements so every retained candidate records evidence: path exists, symbol exists, behavior confirmed, command ran, or reason verification was impossible. Unverifiable candidates must be skipped.

- [x] **Step 4: Switch to diff-first approval**

Require the flow to show the target file, target section, rationale, verification evidence, and diff before asking for user confirmation. Even if the user asks for a fast apply, the diff and confirmation cannot be skipped.

- [x] **Step 5: Final check**

Confirm that `/learn` still only writes to `AGENTS.md` memory surfaces and does not encourage recording derivable code structure in `Hidden Knowledge`.

### Task 2: Update `/remember` Command

**Files:**
- Modify: `plugins/agent-docs/skills/remember/SKILL.md`

- [x] **Step 1: Preserve the report-first boundary**

Confirm that the file header and user confirmation step still make this explicit: output a report by default; do not edit files without user approval.

- [x] **Step 2: Expand audit scope**

Expand the audit scope from only `## Hidden Knowledge` to `Quick Reference`, `Architecture`, `Key Patterns`, `Golden Rules`, `Hidden Knowledge`, and sub-package `AGENTS.md` files.

- [x] **Step 3: Add health dimensions**

Add six dimensions for consistent issue evaluation: `Signal`, `Placement`, `Currency`, `Non-Derivability`, `Duplication`, and `Actionability`.

- [x] **Step 4: Update report format**

Upgrade the output format to `Memory Health Report`, with `Promotions`, `Deletions`, `Rewrites`, `Duplicates`, `Conflicts`, and `No Action Needed`.

- [x] **Step 5: Final check**

Confirm that `/remember` does not promise automatic deletion, automatic conflict merging, or any external memory system.

### Task 3: Verify and Review

**Files:**
- Inspect: `plugins/agent-docs/skills/learn/SKILL.md`
- Inspect: `plugins/agent-docs/skills/remember/SKILL.md`

- [x] **Step 1: Check placeholders**

Run: `rg -n "TO[D]O|T[B]D|FIX[M]E|\{\{" plugins/agent-docs/skills/learn/SKILL.md plugins/agent-docs/skills/remember/SKILL.md`

Expected: no output.

- [x] **Step 2: Check prohibited integration scope**

Run: `rg -n "vector|database|MCP|hook|background|auto-trigger|runtime storage|external memory" plugins/agent-docs/skills/learn/SKILL.md plugins/agent-docs/skills/remember/SKILL.md`

Expected: only prohibition text is acceptable; no instruction should add those systems.

- [x] **Step 3: Check markdown whitespace**

Run: `git diff --check -- plugins/agent-docs/skills/learn/SKILL.md plugins/agent-docs/skills/remember/SKILL.md`

Expected: no output.

- [x] **Step 4: Run loopfix reviewer**

Request a reviewer pass scoped to the two command files and the design. Fix in-scope findings and repeat until the latest pass has no findings for the current goal.

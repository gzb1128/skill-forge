---
name: learn
description: Extract and propose durable repository knowledge discovered in the current session. Use only when the user explicitly invokes /agent-docs:learn or asks to save a newly discovered insight; not for direct documentation maintenance.
disable-model-invocation: true
argument-hint: [optional-context]
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

> **Explicit retrospective trigger.** Run this workflow only after the user
> explicitly asks to preserve knowledge discovered during the current session.
> Do not add hooks, background tasks, auto-trigger behavior, runtime storage,
> vector databases, MCP integration, or external memory systems.

Review what happened in this session and produce verified, reviewable knowledge
proposals for the appropriate `AGENTS.md` or `docs/` surface using the exact-diff
workflow below.

Before classifying candidates, read and apply the shared
[Knowledge Admission Policy](references/knowledge-admission.md). This
skill produces new knowledge proposals; the policy is shared with `remember`
and `curate` rather than owned by this workflow.

When a candidate belongs under `docs/`, also read the
[Documentation Structure Reference](references/doc-structure.md).

## Invocation Boundary

This skill is a retrospective knowledge-capture workflow, not a general
documentation writer or maintenance entry point.

- Invoke it only when the user explicitly requests `/agent-docs:learn`, asks
  to save a newly discovered insight, or asks to review the current session for
  repository knowledge worth preserving. Merely discussing `learn` is not a
  trigger.
- Do **not** invoke, load, simulate, or claim to use `learn` when the user
  directly asks to create, update, reconcile, synchronize, prune, or clean an
  `AGENTS.md`, design document, task list, runbook, index, or knowledge base.
  Perform that requested documentation task directly, using its stated target
  and acceptance criteria.
- "Update the knowledge base" and direct requests to record a decision or edit
  an artifact are ordinary documentation work, not retrospective capture.

The admission rules below apply only **after** this invocation boundary has
been satisfied. Non-derivability, durability, value, and a possible `docs/`
destination decide whether and where a candidate is admitted; they never
trigger this skill on their own.

## Admission Model

Non-derivability is sufficient, not necessary:

- Verified, durable, non-duplicative knowledge that cannot be derived from the
  repository is admitted automatically and routed to the right surface.
- Derivable knowledge may still be admitted when its value score justifies the
  target's maintenance or prompt cost.

`Hidden Knowledge` remains the strict destination for non-derivable gotchas.
High-value derivable commands, maps, rules, and workflows belong in their
purpose-specific surfaces instead of being mislabeled as hidden knowledge.

## Step 1: Extract candidate insights

Review the current session and list candidate insights. Candidates usually come
from hidden dependencies, misleading failures, project-specific workarounds,
critical ordering, command discovery, or documentation gaps discovered during
the work rather than specified as a direct documentation deliverable.

Do not write anything yet. First classify each candidate.

## Step 2: Classify candidates

| Classification | Destination | Rule |
|----------------|-------------|------|
| `Hidden Knowledge` | Nearest relevant `AGENTS.md` under `## Hidden Knowledge` | Automatically admitted non-derivable gotcha that is concise and important enough to change recurring agent behavior |
| `Quick Reference` | Root `AGENTS.md` Quick Reference table | High-value common build, test, lint, run, codegen, clean, or verification commands |
| `Rule` | Nearest `AGENTS.md` `Golden Rules`/`Key Patterns`, or `docs/rules/` plus its index | Put concise, recurring, usually 9+ prompt-value rules in `AGENTS.md`; put narrower or longer rules in pull-based docs |
| `Doc` | Appropriate `docs/` category plus its index | High-value design, troubleshoot, runbook, codemap, verification, or library knowledge, including non-derivable knowledge that does not justify prompt space |
| `Code` | Doc comment or module doc on the owning symbol/file, plus an optional one-line pointer in the nearest `AGENTS.md` | Verified knowledge about a specific function, type, module, or file's behavior or invariant that fits a concise comment; prefer a self-documenting API shape or mechanical enforcement when feasible |
| `Skip` | No write | Fails a hard gate, falls below the destination threshold, is one-off/generic, or is mechanically enforceable with no durable explanation value left |

Before retaining any classification, run the rejection and residual-value pass
in Step 3. Prefer an enforcement change when the session makes it natural. If
source or automation already carries the complete relationship and a targeted
lookup leaves no durable rationale, workflow, navigation, safety, or
compatibility value, classify it as `Skip`; do not propose a comment that only
narrates the enforcement. High-value derivable knowledge may still be admitted
when it has independent value after that check.

## Non-derivable candidates

The following verified candidates are automatically admitted as repository
knowledge without a numeric threshold:

1. **Hidden dependencies (coupling conventions)**: Files or modules that must be
   changed together but are not obviously connected. These look derivable — a
   `diff` can show two files currently match — but the "must stay in sync" rule
   is an unwritten convention the compiler/linter/git does not enforce. Record
   it. Objective bar: acting on the insight requires **≥2 artifacts plus a
   convention not expressed or enforced by any single authoritative artifact**.
   Before claiming this bar, name the artifact(s) that carry the convention: a
   shared constant, interface, generated contract, focused test harness, or the
   owning symbol's doc comment — including one created earlier in the same
   session — each counts as a carrying artifact. When any single artifact
   mechanically carries the relationship, automatic admission does not apply;
   treat the candidate as derivable knowledge and score its residual value.
2. **Misleading errors**: Error messages that point to the wrong location or
   cause.
3. **Workarounds and quirks**: Project-specific behavior that differs from the
   standard pattern.
4. **Critical ordering**: Operations that must happen in a specific sequence,
   especially cross-artifact ordering (e.g. SQL migration before code) that no
   single file states.

Route them after admission. A concise cross-cutting trap may belong in
`AGENTS.md` Hidden Knowledge, while a niche library quirk or longer operational
constraint belongs in the relevant docs category. A quirk scoped to one
function, type, or file belongs in that artifact's doc comment (`Code`)
instead of Hidden Knowledge. Automatic admission does not mean automatic
prompt residency.

## High-value derivable candidates

Do not discard a candidate merely because source inspection could reconstruct
it. Score and route candidates such as:

- commands and expected results used across many tasks;
- architecture entry maps that prevent repeated broad searches;
- deterministic runbooks and rollback sequences;
- verification contracts whose reconstruction is slow or error-prone;
- project-specific rules that prevent costly mistakes.

Use the shared policy's normal guidance: usually 9+ for concise `AGENTS.md`
content and 7+ for pull-based docs.

## Skip criteria

Skip candidates that are:

- Low-value restatements of code patterns, architecture, or file structure.
- Recent-change narration already captured by git with no durable workflow,
  decision, navigation, or safety value.
- Debugging solutions where the fix is now in code and the commit message should
  carry the context, unless the resulting diagnosis remains recurrent and scores
  high enough for troubleshoot documentation.
- Already present in `AGENTS.md`, `docs/rules/`, or README.
- Standard language or framework behavior.
- Non-obvious commands that belong in Quick Reference, not Hidden Knowledge.
- Ephemeral session details, including attempts that failed temporarily.
- Raw step-by-step agent execution plans, task breakdowns, or session
  checklists. Reclassify durable content normally: a concise recurring gotcha
  may belong in `AGENTS.md`, while longer decisions, alternatives, sequencing
  contracts, verification gates, or rollback boundaries belong in a design.
- Unverified claims.

## Step 3: Verify and score each retained candidate

Every retained candidate needs explicit evidence before it can be proposed:

| Candidate mentions | Verification evidence |
|--------------------|-----------------------|
| File path | Confirm the path exists with `ls` or by reading the file |
| Function, type, command, or symbol | Confirm it exists with search or a language-aware lookup |
| Behavior or constraint | Run the smallest relevant command, inspect source, or explain why direct execution is unsafe |
| Existing AGENTS.md content | Read the target section and check for stale or duplicate entries |
| Existing repository knowledge | Search root guidance and the relevant docs category for an equivalent authoritative entry |
| Session-produced carriers | Inspect the diffs, commits, MR/PR bodies, and test comments the current session created; a candidate born from a change is usually already carried in place by that change |
| Code comment target | Confirm the symbol or file exists and the comment attaches to the owning artifact — a doc comment on the item or a module doc at the top of the file, not a stray line comment far from it |
| Non-derivability claim | Search source, git, and existing docs for the rule; authoritative maintainer context may establish that a convention is intentionally unwritten |
| Mechanical enforcement | Inspect owning symbols, references, focused tests, linters, and scripts for a single artifact that already carries the relationship or external value |
| Residual explanation value | State what rationale, workflow, navigation, safety, or compatibility value remains after existing enforcement and the cheapest targeted reconstruction probe |

**Required rejection pass.** Run the cheapest relevant probe before automatic
admission or scoring. Record the probe and one of these outcomes for every
candidate:

- `Skip`: source or automation carries the complete relationship, one targeted
  lookup reconstructs it, and no durable explanation value remains.
- `Retain as derivable`: enforcement exists or reconstruction is possible, but
  the candidate still provides independently valuable rationale, workflow,
  navigation, safety, or compatibility guidance; score that residual value.
- `Automatic admission — non-derivable`: no authoritative artifact expresses
  or enforces the verified convention, error interpretation, quirk, or order.

Do not require all probes to fail before admitting high-value derivable
knowledge. The pass chooses the cheapest adequate surface and removes redundant
narration; it does not replace the admission model.

**Stable-reference rule.** When proposed knowledge points to source, prefer
package paths, files, symbols, headings, and named commands over line numbers.
Do not carry a session's `file.go:42` citation into durable documentation when
the referenced symbol or command can identify the same concept. Use line
numbers only when a tool requires them.

If verification fails, classify the candidate as `Skip` and explain the failed
check. If verification cannot be performed safely, report it as unverified and
do not propose a write.

After verification and the rejection pass, record either:

- `Automatic admission — non-derivable`, or
- the six-dimension value score and destination threshold from the shared
  policy, including the residual value that is being scored, or
- `Skip`, with the enforcing artifact or cheap reconstruction evidence.

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

For `Rule`, use the nearest `AGENTS.md` `Golden Rules` or `Key Patterns` section
when the rule is concise, recurring, and earns prompt space. Otherwise use
`docs/rules/`. Create a missing AGENTS.md section only as part of the approved
proposal.

For `Code`, the target is the owning artifact itself: a doc comment on the
function, type, or module the knowledge describes, or a module doc section at
the top of the owning file for larger invariants. Prefer the nearest artifact
over any centralized surface. When the knowledge is too large for a comment,
write the module doc and add a one-line pointer plus a sync-guard reminder to
the nearest `AGENTS.md` in the same proposal.

For a docs-bound `Rule` or `Doc`, choose the category from the Documentation
Structure Reference. Create the category and `INDEX.md` only with the first
admitted document; never scaffold empty categories. Prefer updating an
existing authoritative document over creating a duplicate.

## Step 5: Show proposed changes first

Before editing any file, show all proposals in this format:

````markdown
## Learn Proposals

### 1. `<classification>` -> `<target file>`

**Why:** <one-line reason this helps future sessions>

**Verification:** <path/symbol/command/behavior evidence>

**Nearest-code alternative:** <for Hidden Knowledge, Rule, and Doc proposals:
why the owning artifact or its module doc cannot carry this instead; omit for
Code proposals, which are that alternative>

**Admission:** <automatic — non-derivable | score N/12 with dimension summary>

**Action:** <add/update/skip/report-only>

```diff
- <existing line, only when updating an approved existing entry>
+ <exact proposed addition or replacement>
```

### Skipped Candidates

1. `<candidate>` -> skipped because <enforcing artifact or failed gate, cheapest probe, and why no residual explanation value remains>

For a new document, include the document diff and the matching `INDEX.md` diff
in the same proposal. A `Code` proposal's diff targets the owning source file;
include the optional nearest-`AGENTS.md` pointer diff in the same proposal when
the hybrid module-doc pattern is used. When one decision yields both a design
record and artifact-scoped invariants, propose the `Doc` design diff and its
`Code` comment diffs in the same batch: the design records why, the comments
carry the now-binding invariants. Use `report-only` only when a destination
conflict or missing authoritative context requires user judgment.
````

## Step 6: Approval gate and apply

Stop after showing the exact proposed changes, even if the user asks to apply
quickly. After explicit approval:

1. Apply only the proposals the user approved.
2. Preserve unrelated content and keep `AGENTS.md` additions concise.
3. Do not perform general cleanup from `/agent-docs:learn`; use
   `/agent-docs:remember` for `AGENTS.md` and `/agent-docs:curate` for `docs/`.
4. Re-open every edited file and verify the final text and index links.
5. Report what changed, where it changed, which candidates were skipped, and
   any remaining report-only suggestions.

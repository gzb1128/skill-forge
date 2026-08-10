---
name: remember
description: Audit and reorganize project AGENTS.md memory, or evaluate an explicitly named rule for promotion into the nearest AGENTS.md. Use for explicit memory-audit or rule-promotion requests; not to capture new session insights.
disable-model-invocation: true
argument-hint: [optional-scope]
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

> **Manual-trigger skill.** `disable-model-invocation: true` keeps the model from
> running memory audits automatically mid-task. When installed from this plugin,
> invoke it deliberately as `/agent-docs:remember` when you want to clean
> up. Do not add hooks, background tasks, auto-trigger behavior, runtime storage,
> vector databases, MCP integration, or external memory systems.

Choose the explicit scope below and produce a structured `Memory Health
Report` using the workflow.

## What this does

This is the complement to `/agent-docs:learn`:

- `/agent-docs:learn` proposes verified knowledge additions to `AGENTS.md` or
  `docs/` from the current session.
- `/agent-docs:remember` audits existing `AGENTS.md` memory surfaces for staleness,
  duplication, misplacement, and low-signal content.
- It may also accept one explicitly named docs entry as a candidate for
  promotion into the nearest `AGENTS.md`.

Read and apply the shared
[Knowledge Admission Policy](references/knowledge-admission.md). Do not
invoke `learn`; both workflows independently apply the same policy in opposite
directions.

## Step 1: Choose scope and gather memory layers

Use exactly one mode:

- **Full memory audit:** when the user asks to audit or reorganize project
  memory, read all project `AGENTS.md` files.
- **Targeted promotion:** when the user explicitly names a rule in docs or a
  codemap for possible promotion, read that entry and the nearest candidate
  `AGENTS.md` only. Do not turn it into a full memory audit.

Resolve "nearest" from the source path affected by the rule, not from whichever
`AGENTS.md` the runtime loaded first:

1. Extract the primary affected source path or paths from the named entry.
2. For one path, walk from its containing directory toward the repository root
   and select the deepest existing project `AGENTS.md`. For multiple paths,
   use the deepest `AGENTS.md` at their common scope.
3. If the entry does not identify an affected path and the target cannot be
   verified, report `Needs user input` instead of defaulting to root.

Locating candidate filenames along that ancestor chain is allowed; do not open
or audit non-target `AGENTS.md` files. A root `AGENTS.md` already present in
the runtime context is not evidence that it is the nearest target.

Typical project memory layers include:

```text
AGENTS.md
internal/<package>/AGENTS.md
<other-package>/AGENTS.md
```

Exclude personal preference files such as `~/.claude/CLAUDE.md` or
`~/.config/opencode/AGENTS.md`, every `CLAUDE.md`, and any non-project
`AGENTS.md`. In targeted-promotion mode, do not enumerate or audit the rest of
`docs/`; the named entry is input evidence, not a docs curation license.

## Step 2: Audit memory surfaces

Audit every relevant `AGENTS.md` memory surface, not only `## Hidden Knowledge`.

| Surface | Checks |
|---------|--------|
| `Quick Reference` | Commands/workflows exist, placeholders are removed, commands are current or explicitly marked as examples |
| `Architecture` | Gives agents a clear entry map, key directories, and module relationships without becoming a copied source-code encyclopedia |
| `Key Patterns` | Captures project-specific patterns that are still true and valuable enough for prompt space, whether non-derivable or expensive to rediscover |
| `Golden Rules` | Still hard rules, not duplicated from `docs/rules/`, not better represented as links |
| `Hidden Knowledge` | Non-derivable gotchas, quirks, critical ordering, or misleading failures; verified, not stale, not duplicated, correctly placed |
| Sub-package `AGENTS.md` | Still justified by complexity, cross-module constraints, state machines, or special verification needs |

## Step 3: Classify issues by quality dimension

Use these dimensions to explain every finding. Do not produce an overall score
for an `AGENTS.md` file. Use the shared candidate value score only when deciding
whether a specific entry earns prompt space.

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
| `Non-Derivability` | Hidden knowledge cannot now be inferred from code, git, or existing docs; this is an automatic-admission signal, not a universal requirement for every surface |
| `Knowledge Value` | Derivable content still earns prompt space when impact, recurrence, discovery cost, actionability, durability, and scope justify it |
| `Duplication` | The same guidance is not repeated across layers or docs |

Map any additional memory-quality criterion to a dimension above before
reporting rather than changing the audit target.

## Step 4: Verify findings

Before proposing a cleanup, verify it:

| Finding type | Verification |
|--------------|--------------|
| Missing or stale file path | Check the path exists |
| Missing function, type, command, or symbol | Search for the referenced name |
| Stale command | Run the safest relevant command, or explain why execution is unsafe |
| Contradicted behavior | Inspect source or run the smallest relevant check |
| Duplicate content | Cite both locations |
| Now-derivable hidden knowledge | Cite the code, docs, git history, or AGENTS.md main-body section that now covers it, then assess whether it remains valuable in another surface |
| Potentially low-value derivable entry | Show the shared-policy score and the lower-cost source or document that would replace it |
| Memory assertion backed by a linked doc | Open that one linked doc and confirm it still supports the assertion |
| Explicit docs promotion candidate | Cite the named entry, verify it changes recurring agent behavior, score its prompt value, and confirm it is absent from the nearest `AGENTS.md` |

If a finding cannot be verified, label it `Needs user input` instead of treating
it as fact.

**Scope guard — linked docs are a verification method, not an audit target.**
Open only the specific doc a memory assertion links to, confirm it still supports
that assertion, and stop. Do **not** enumerate `docs/`, score doc quality, or
traverse cross-links; doc-level quality (including redundancy) is owned by a
separate audit, not `/agent-docs:remember`. The economics differ — `AGENTS.md`
is prompt-resident and uses the highest value threshold, while `docs/` is
pull-based and may legitimately be longer or more detailed. The only question
here is whether the linked doc still backs the memory claim that cites it.

## Step 5: Classify actions

| Action | Use when |
|--------|----------|
| `Promotions` | Lower-level guidance affects multiple packages, belongs in a higher-level `AGENTS.md`, or an explicitly named docs rule earns prompt space in the nearest `AGENTS.md` |
| `Deletions` | Content fails a hard gate, or derivable content scores too low for prompt-resident memory; derivability alone is insufficient, and valid non-derivable content must be retained or rerouted |
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
running `/agent-docs:learn` after a future session discovers valuable knowledge.

## Step 7: User approval

- Stop after presenting the report. Modify only proposals the user explicitly
  approves; they may approve any subset, reject all, or request revisions.
- Never auto-delete or auto-merge conflicts. Ask which version is correct before
  editing.
- After applying approved changes, report applied changes, rejected proposals,
  unresolved conflicts, and residual risks.

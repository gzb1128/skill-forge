---
name: curate
description: Use when the user says "curate", "audit docs", or wants to review the docs/ knowledge base for stale links, encyclopedia bloat, naming drift, and missing indexes — the docs/ counterpart to /agent-docs:remember
disable-model-invocation: true
argument-hint: [optional-scope-or-category]
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

> **Manual-trigger skill.** `disable-model-invocation: true` keeps the model from
> running docs audits automatically mid-task. When installed from this plugin,
> invoke it deliberately as `/agent-docs:curate` when you want to clean up the
> docs/ tree. Do not add hooks, background tasks, auto-trigger behavior, runtime
> storage, vector databases, MCP integration, or external memory systems.

Review the `docs/` knowledge base and produce a structured `Docs Health Report`
using the workflow below.

## What this does

This is the complement to `/agent-docs:remember`:

- `/agent-docs:learn` proposes verified memory additions to `AGENTS.md`.
- `/agent-docs:remember` audits `AGENTS.md` memory surfaces (prompt-resident).
- `/agent-docs:curate` audits the `docs/` knowledge base (pull-based).

The economics differ and so do the rubrics. `AGENTS.md` pays per prompt line, so
`remember` judges Signal / Conciseness / Non-Derivability strictly. `docs/` is
read on demand and may legitimately be longer or more detailed, so `curate`
judges **navigability, link integrity, structure, and drift** — not brevity for
its own sake. Both trees stay subject to the repo's non-derivability rule.

**Scope guard — `docs/` only, never `AGENTS.md`.** Audit files under `docs/`
and the doc-tree indexes. Do not open, score, or propose edits to any
`AGENTS.md`; that is `/agent-docs:remember`'s job. Detecting whether a doc
duplicates an `AGENTS.md` entry would require reading `AGENTS.md`, which is out
of scope — so do not make that cross-surface comparison. Limit duplicate
detection to doc↔doc within `docs/`.

## Step 1: Inventory the doc tree

List every `docs/` category and its files. Typical layout:

```text
docs/
├── codemaps/   (architecture maps, concept → file)
├── design/     (YYYY-MM-DD-<topic>-design.md)
├── plans/      (YYYY-MM-DD-<feature>.md)
├── rules/      (coding standards)
├── troubleshoot/  (symptom-indexed)
├── runbooks/   (deterministic operations)
├── lib/        (third-party library notes)
└── verify/     (dry-run verification flows)
```

Record which categories exist, which have an `INDEX.md`, and which are empty or
absent. An absent category is not a defect unless the team needs it; an empty
category with only a placeholder INDEX is a stale-signal candidate.

## Step 2: Audit by docs-specific dimensions

Apply these dimensions to `docs/` content only. Every dimension is grounded in
an existing repo rule — cite the rule when raising a finding.

| Dimension | Checks | Source rule |
|-----------|--------|-------------|
| `INDEX Health` | Every `docs/<category>/` has an `INDEX.md`; it is ~30-60 lines; it has a table with a "When to Use" column; no tutorial prose | [document-conventions.md](../../templates/docs/rules/document-conventions.md) §INDEX, [openai-harness-engineering.md](../../templates/docs/rules/openai-harness-engineering.md) §Anti-Patterns to Avoid |
| `Maps-not-Encyclopedias` | Codemaps map concept → file path; no copied function bodies, no config dumps, no code blocks > ~20 lines; link to source instead | [openai-harness-engineering.md](../../templates/docs/rules/openai-harness-engineering.md) §2, [codemaps/INDEX.md](../../templates/docs/codemaps/INDEX.md) §Anti-Patterns |
| `Link Integrity` | Internal doc→doc and doc→source links resolve; no dangling `](./missing.md)`; source links point at paths that still exist | progressive disclosure (implicit) |
| `Naming` | Designs/plans use `YYYY-MM-DD-` prefix; files are lowercase-hyphen; no `-v2` suffix (supersede by editing, not versioning) | [document-conventions.md](../../templates/docs/rules/document-conventions.md) §Naming |
| `Depth ∝ Surface` | Codemap length matches module role (core ~200-300, standard ~100, leaf ≤50); not a 300-line map for a leaf utility | [document-conventions.md](../../templates/docs/rules/document-conventions.md) §Depth |
| `Non-Derivability (docs)` | The doc records something not inferrable from source + git + existing docs; not restating visible code; design docs capture the *decision*, not the implementation | [non-derivability.md](../../templates/docs/rules/non-derivability.md) |
| `Doc↔Source Drift` | Claims a doc makes about source (symbols, paths, behavior, line-anchored refs) still match the source; flag stale `file.go:NN` where the symbol moved | [openai-harness-engineering.md](../../templates/docs/rules/openai-harness-engineering.md) §7 (entropy/GC) |

## Step 3: Verify findings

Before proposing a cleanup, verify it:

| Finding type | Verification |
|--------------|--------------|
| Broken internal link | Confirm the target path does not exist (`ls`, `Glob`) |
| Stale source reference | Open the cited source file and confirm the symbol/path/behavior diverged |
| Encyclopedia codemap | Count code-block lines or copied config size; cite the line range |
| Missing INDEX | Confirm no `INDEX.md` in that category directory |
| Naming violation | Show the actual filename vs. the required pattern |
| Now-derivable doc | Cite the source/git/doc that now covers the same ground |
| Duplicate across docs | Cite both doc locations |

If a finding cannot be verified, label it `Needs user input` instead of treating
it as fact.

**Stable-reference rule.** When proposing a `Rewrite` for a drifted source
reference, prefer symbol/package/heading-anchor form over line numbers (e.g.
`the Run method in deploy_v3.go`, not `deploy_v3.go:42`). Line numbers drift on
every unrelated edit; bumping the number only fixes it until the next edit.

## Step 4: Classify actions

| Action | Use when |
|--------|----------|
| `Promotions` | A doc belongs in a different category (e.g. a how-to in `codemaps/` belongs in `runbooks/`) |
| `Deletions` | Content is stale, duplicated, now-derivable, or a placeholder with no plan to fill |
| `Rewrites` | Content is true but encyclopedia-style, mis-linked, mis-named, or drifted |
| `Duplicates` | The same guidance appears in two docs within `docs/` |
| `Conflicts` | Two docs contradict each other and need user judgment |
| `No Action Needed` | Content is valid, correctly placed, and useful |

## Step 5: Present the report

Output a structured report:

```markdown
## Docs Health Report

### Summary

- Categories reviewed: <list>
- Files reviewed: <count>
- INDEX status: <which categories have one>
- Changes proposed: <count>
- Items needing user input: <count>

### Promotions

1. `<file>` -> move to `<category>/` because <dimension + verification evidence>

### Deletions

1. `<file>` -> delete because <dimension + verification evidence>

### Rewrites

1. `<file>`: "<entry>" -> rewrite as "<new wording>" because <dimension + verification evidence>

### Duplicates

1. "<entry>" appears in `<file A>` and `<file B>` -> keep `<file A>`, remove `<file B>` because <reason>

### Conflicts

1. `<file A>` says "X" but `<file B>` says "Y" -> needs user input: <question>

### No Action Needed

<brief note on categories/files that are valid and well-placed>
```

If the `docs/` tree is empty or only has placeholder INDEXes, say so and suggest
running `bootstrap-agent-docs` or writing docs only when there is non-obvious
knowledge to record.

## Step 6: User approval

- Stop after presenting the report. Modify only proposals the user explicitly
  approves; they may approve any subset, reject all, or request revisions.
- Never auto-delete or auto-merge conflicts. Ask which version is correct before
  editing.
- After applying approved changes, report applied changes, rejected proposals,
  unresolved conflicts, and residual risks.

---
name: curate
description: Audit a repository docs/ tree for routing, drift, links, duplication, and misplaced knowledge. Use only for explicit docs curation or audit requests.
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

- `/agent-docs:learn` proposes verified knowledge additions to `AGENTS.md` or
  `docs/`.
- `/agent-docs:remember` audits `AGENTS.md` memory surfaces (prompt-resident).
- `/agent-docs:curate` audits the `docs/` knowledge base (pull-based).

The economics differ and so do the rubrics. `AGENTS.md` pays per prompt line, so
`remember` uses a high value threshold. `docs/` is
read on demand and may legitimately be longer or more detailed, so `curate`
judges **navigability, link integrity, structure, and drift** — not brevity for
its own sake. Derivability alone never makes useful documentation invalid.

Read and apply the shared
[Knowledge Admission Policy](references/knowledge-admission.md) and
[Documentation Structure Reference](references/doc-structure.md). Do not
invoke `learn`; all knowledge workflows independently use the shared policy.

**Scope guard — `docs/` is the audit target.** Audit files under `docs/` and
the doc-tree indexes. Do not broaden this into an `AGENTS.md` memory audit.
When a doc contains a behavior-changing rule that appears to belong in
prompt-resident memory, read only the nearest relevant `AGENTS.md` needed to
verify its target and whether the rule already exists. Report a targeted
`AGENTS.md` promotion candidate; do not score unrelated memory entries or
edit `AGENTS.md` as part of the docs audit.

## Step 1: Inventory the doc tree

List every `docs/` category and its files. Then assign a review priority before
deep-reading files. Use this default order for common categories, from highest
to lowest risk and recurring value:

```text
docs/
├── rules/          (hard constraints that affect recurring changes)
├── design/         (durable decisions and delivery boundaries)
├── runbooks/       (live operational procedures)
├── verify/         (repeatable completion evidence)
├── troubleshoot/  (symptom-indexed diagnosis)
├── codemaps/       (architecture maps, concept → file)
└── lib/            (third-party behavior and usage)
```

Promote a category above this default when the user scoped it explicitly, it
contains live operational or release authority, many entry points depend on
it, or inventory checks already show likely source drift or broken routing.
Audit archives last unless current docs still depend on them. File count,
line count, and age are investigation signals, not sufficient priority by
themselves. Put repository-specific categories into the same order using
impact, actionability, and routing reach, and record the resulting order and
one-line rationale in the report.

Record which categories exist, which have an `INDEX.md`, and which are empty or
absent. An absent category is not a defect unless the team needs it; an empty
category with only a placeholder INDEX is a stale-signal candidate.

Do not recommend creating a new `docs/plans/` category. If one already exists,
its existence alone is not a defect: audit its files normally, and do not
propose category-wide deletion or migration unless the user explicitly asks.
When removal is explicitly in scope, identify durable decisions, constraints,
ordering dependencies, verification gates, or rollback boundaries to merge
into `docs/design/`; never move the category wholesale.

## Step 2: Audit by docs-specific dimensions

Apply these dimensions to `docs/` content only. Every dimension is grounded in
an existing repo rule — cite the rule when raising a finding.

| Dimension | Checks | Source rule |
|-----------|--------|-------------|
| `INDEX Health` | Categories containing documents normally have an `INDEX.md` with a routing table and no tutorial prose; absent/empty categories do not need placeholders | [Documentation Structure Reference](references/doc-structure.md) §INDEX Standards |
| `Maps-not-Encyclopedias` | Codemaps map concepts and entry flows to source; no copied function bodies, config dumps, or behavior-changing policy; link to the authoritative surface instead | [Documentation Structure Reference](references/doc-structure.md) §Maps, Not Encyclopedias |
| `Authority Placement` | Behavior-changing rules route to the nearest `AGENTS.md`; durable contracts and rationale route to `docs/design/`; operational procedures route to `docs/runbooks/` | [Documentation Structure Reference](references/doc-structure.md) §Maps, Not Encyclopedias |
| `Link Integrity` | Internal doc→doc and doc→source links resolve; no dangling `](./missing.md)`; source links point at paths that still exist | progressive disclosure (implicit) |
| `Naming` | Files use lowercase-hyphen naming; designs use a date prefix when chronology matters; no ambiguous `-v2` suffix | [Documentation Structure Reference](references/doc-structure.md) §Naming |
| `Depth ∝ Surface` | Detail matches workflow/interface complexity and retrieval value rather than a uniform line target | [Documentation Structure Reference](references/doc-structure.md) §Maps, Not Encyclopedias |
| `Knowledge Value` | Non-derivable knowledge is admitted automatically; derivable docs remain when impact, recurrence, discovery cost, actionability, durability, and scope justify maintenance | [Knowledge Admission Policy](references/knowledge-admission.md) §Admission Rule and §Value Score |
| `Doc↔Source Drift` | Claims about source still match current symbols, paths, and behavior; prefer stable symbol/package references over line numbers | [Documentation Structure Reference](references/doc-structure.md) §Stable References |

## Step 3: Verify findings

Before proposing a cleanup, verify it:

| Finding type | Verification |
|--------------|--------------|
| Broken internal link | Confirm the target path does not exist (`ls`, `Glob`) |
| Stale source reference | Open the cited source file and confirm the symbol/path/behavior diverged |
| Encyclopedia codemap | Count code-block lines or copied config size; cite the line range |
| Missing INDEX | Confirm no `INDEX.md` in that category directory |
| Naming violation | Show the actual filename vs. the required pattern |
| Derivable doc proposed for deletion | Cite the source/git/doc that covers the same ground, score its remaining value, and identify the cheaper replacement surface |
| Duplicate across docs | Cite both doc locations |
| AGENTS.md promotion candidate | Cite the exact doc entry, open only the nearest target `AGENTS.md`, and confirm the rule is recurring, behavior-changing, and not already present |

If a finding cannot be verified, label it `Needs user input` instead of treating
it as fact.

**Stable-reference rule.** When proposing a `Rewrite` for a drifted source
reference, prefer symbol/package/heading-anchor form over line numbers (e.g.
`the Run method in deploy_v3.go`, not `deploy_v3.go:42`). Line numbers drift on
every unrelated edit; bumping the number only fixes it until the next edit.

## Step 4: Classify actions

| Action | Use when |
|--------|----------|
| `Promotions` | A doc belongs in a different docs category, or a concise recurring behavior rule belongs in the nearest `AGENTS.md` |
| `Deletions` | Content fails a hard gate, is a useless placeholder, or is derivable and scores too low for its maintenance cost; valid non-derivable content must be retained or rerouted |
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
- Category priority: <ordered categories with one-line rationale>
- Files reviewed: <count>
- INDEX status: <which categories have one>
- Changes proposed: <count>
- Items needing user input: <count>

### Promotions

1. `<file or entry>` -> move to `<docs category or nearest AGENTS.md>` because <dimension + verification evidence>

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

If the `docs/` tree is empty or only has placeholder INDEXes, say so. Suggest
removing empty placeholders and using `/agent-docs:learn` when valuable
knowledge is ready to record; bootstrap does not create docs categories.

## Step 6: User approval

- Stop after presenting the report. Modify only proposals the user explicitly
  approves; they may approve any subset, reject all, or request revisions.
- Treat an approved `AGENTS.md` promotion as a targeted memory edit, not
  permission to audit or rewrite the rest of that file.
- Never auto-delete or auto-merge conflicts. Ask which version is correct before
  editing.
- After applying approved changes, report applied changes, rejected proposals,
  unresolved conflicts, and residual risks.

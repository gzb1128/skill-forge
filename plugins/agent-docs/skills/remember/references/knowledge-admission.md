# Knowledge Admission Policy

Use this policy when deciding whether knowledge belongs in `AGENTS.md`, under
`docs/`, or nowhere in the repository. It is shared by
`bootstrap-agent-docs`, `learn`, `remember`, and `curate`; none of those
workflows owns the policy by itself.

## Hard Gates

A candidate must be:

- verified against current source, commands, or authoritative context;
- durable enough to help a future session rather than describe a temporary
  attempt;
- non-duplicative, or clearly designated as the authoritative copy;
- routed to a surface whose readers and maintenance cost match the content.

Content that fails a hard gate is skipped or rewritten regardless of score.

## Admission Rule

**Non-derivability is sufficient, not necessary.**

- Verified, durable knowledge that cannot be recovered from source, git, or
  existing docs is automatically admitted. Route it to the right surface.
- Derivable knowledge is not rejected automatically. Admit it when its value
  exceeds the maintenance and context cost of the target surface.

Examples of valuable derivable knowledge include common commands, architecture
entry maps, deterministic runbooks, verification contracts, and safety rules.
Reconstructing them from source may be possible but unnecessarily slow or
error-prone.

## Rejection and Residual-Value Pass

Before automatic admission, scoring, or placement, run the cheapest relevant
probe that could reject the candidate or route it to a lower-cost surface:

1. Inspect the owning symbols and their references.
2. Check whether a compiler, type/interface boundary, focused test, linter, or
   script already enforces the relationship or external value.
3. Search the likely authoritative documentation surface for an equivalent
   entry.
4. State what durable value remains after those artifacts are considered.

Mechanical enforcement is not an automatic rejection: documentation may still
carry non-obvious rationale, an operator workflow, a navigation map, a safety
boundary, or a compatibility/migration constraint. However, when the enforcing
artifact plus one targeted lookup reconstructs the complete relationship and
no such residual value remains, classify the candidate as `Skip`. Do not add a
comment merely to narrate an already enforced relationship.

## Value Score

Score each dimension from 0 (none) to 2 (high) after the rejection pass. Use
these anchors rather than scoring from the apparent complexity of the session:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Impact | Cosmetic or negligible | Avoids limited rework | Prevents costly mistakes, outages, or unsafe operations |
| Recurrence | One-off | Plausible in a few future tasks | Recurs across many tasks or releases |
| Discovery cost | One obvious targeted lookup | Several local hops or a focused check | Cross-package/system evidence, execution, or maintainer context |
| Actionability | Description only | Partial guidance | Direct command, rule, sequence, map, or expected result |
| Durability | Tied to the current change | Useful across several changes | Long-lived contract or workflow |
| Scope | One symbol or call site | One package or workflow | Multiple packages, workflows, agents, or people |

Use the total as a decision aid, not a substitute for evidence:

| Destination | Admission guidance |
|---|---|
| `AGENTS.md` | Usually score 9+ and express the result concisely; prompt-resident content has the highest cost |
| `docs/` | Usually score 7+; pull-based docs may carry more detail when they reduce navigation, execution, or handoff risk |
| Code comment or module doc | Passes the hard gates and is naturally about one code artifact; no numeric threshold — it pays no prompt cost, but keep it tight because it pays review cost on every diff touching the file |
| Source, tests, or tooling | First choice when a compiler, test, linter, or script can enforce the rule; documentation may still explain the workflow or rationale |
| Skip | Below the relevant threshold, generic, one-off, stale, unverifiable, or redundant |

Prefer the cheapest authoritative tier that serves the candidate's audience:
mechanical enforcement or a self-documenting API shape first; the owning
artifact's doc comment or module doc for artifact-scoped explanation;
pull-based `docs/` for longer, narrower, or occasional knowledge; and
`AGENTS.md` only for concise rules, maps, commands, or traps that must change
recurring agent behavior before the relevant artifact is opened. Automatic
admission chooses no destination by itself. Knowledge that describes one
specific function, type, module, or file belongs next to that artifact, where
every edit, move, and review of the code carries it along.

Non-derivable knowledge does not need to meet a numeric threshold after the hard
gates, but it still needs correct placement. A niche library quirk may belong in
`docs/lib/`, while a short cross-cutting trap may belong in `AGENTS.md`.

## Surface Economics

### `AGENTS.md`

Keep only prompt-resident knowledge that changes agent behavior frequently:

- build, test, lint, codegen, and verification entry points;
- a compact architecture and task-routing map;
- project-specific hard rules;
- concise hidden dependencies, misleading failures, quirks, and ordering.

When knowledge has a long-form authoritative copy — a module doc or a
`docs/design/` contract — the `AGENTS.md` entry is a 1-3 line summary plus
a link, never an inline copy of the contract body.

Derivable content may remain when its score justifies prompt cost. Do not delete
a valid build command or architecture entry merely because source inspection
could rediscover it.

### `docs/`

Optimize for retrieval value, navigability, correctness, and maintenance cost.
High-value documentation may intentionally summarize or organize derivable
facts, provided it links to authoritative source instead of copying volatile
implementation bodies.

### Code Comments and Module Docs

Knowledge that is naturally about one code artifact — a function, type,
module, or file — belongs in that artifact's doc comment or module doc
rather than in prompt-resident memory:

- It travels with every edit, move, and review of the code, so the reader
  who most needs it always sees it exactly when it matters.
- It pays no prompt cost, but it pays review cost on every diff that
  touches the file: keep doc comments to roughly 1-5 lines, and put larger
  invariants in a module doc section at the top of the owning file.
- Prefer making the API self-documenting (named methods, enums, newtypes)
  or enforcing the rule mechanically first; use a comment only when a
  smaller change is more appropriate.
- Hybrid pattern for large knowledge: the module doc carries the
  explanation, and the nearest `AGENTS.md` carries only a one-line pointer
  plus a sync-guard reminder, so agents working in that directory are
  routed to the authoritative in-file explanation without paying its
  prompt cost.

Code-comment candidates carry no numeric threshold: they pass the hard
gates and must be scoped to a specific owning artifact. Scope, not
derivability, decides this surface.

### Source and Automation

When a compiler, test, linter, or script can enforce a rule, prefer that
enforcement. Keep documentation when it still explains a non-obvious decision,
operational workflow, navigation path, or safe verification contract.

## Audit Rule

Derivability alone never triggers deletion. Delete or rewrite content when it is
stale, duplicated, misplaced, or more cheaply and reliably represented
elsewhere. A low score may justify deleting derivable content. Non-derivable
content that still passes the hard gates must remain documented; reroute it if
the current surface is too expensive. Relocation is bidirectional: an
`AGENTS.md` entry whose knowledge is scoped to a single code artifact may move
into that artifact's doc comment or module doc — triggered by scope and
conciseness, never by derivability alone — keeping at most a one-line pointer
in memory. Audits should cite both the value judgment and the verification
evidence.

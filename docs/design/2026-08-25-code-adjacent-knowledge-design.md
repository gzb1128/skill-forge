# Code-Adjacent Knowledge Placement

**Status:** Approved

## Problem

The knowledge lifecycle defined two destination surfaces: prompt-resident
`AGENTS.md` (score 9+) and pull-based `docs/` (7+). Knowledge that describes
one specific code artifact — a function, type, module, or file — had no
natural home: `learn` routed it into the nearest `AGENTS.md` (paying prompt
cost for knowledge only editors of that artifact need) or, when the knowledge
seemed "better enforced mechanically", discarded it outright via the Skip
criteria.

## Evidence

The openai/codex repository places knowledge next to the code that owns it,
in tiers:

1. Self-documenting API shapes first; comments only as a smaller fallback
   (`tools/argument-comment-lint/README.md`).
2. Callsite comments mechanically verified against the callee signature
   (`/*param*/` convention enforced by a dylint lint), so the comment cannot
   silently rot.
3. Large invariants live in module docs
   (`codex-rs/tui/src/bottom_pane/chat_composer.rs` carries a full state
   machine explanation as `//!` module docs).
4. The nearest `AGENTS.md` holds only a thin sync-guard pointer to those
   module docs (`codex-rs/tui/src/bottom_pane/AGENTS.md` is 13 lines of
   "keep the module docs in sync", not the knowledge itself).
5. Root `AGENTS.md` codifies the philosophy as a rule: move tests and docs
   with extracted code "so the invariants stay close to the code that owns
   them".

The leak-proofness argument: knowledge in the owning artifact is seen by
every editor, mover, and reviewer of that code — the diff cannot avoid it.
No `AGENTS.md` entry enjoys that guarantee.

## Decision

Adopt the tiering in the shared Knowledge Admission Policy:

1. Mechanical enforcement or a self-documenting API shape, when feasible.
2. Doc comment on the owning symbol, or module doc for larger invariants,
   with an optional one-line pointer plus sync-guard reminder in the nearest
   `AGENTS.md`.
3. Nearest `AGENTS.md` (prompt-resident, 9+).
4. `docs/` tree (pull-based, 7+).

Concretely:

- `learn` gains a `Code` classification whose diff targets the owning source
  file; "better enforced mechanically" is a routing decision, not a Skip
  reason — skip only when no durable explanation value remains.
- `remember` gains a `Relocations to code` action: prompt-resident entries
  scoped to a single artifact move into its doc comment, triggered by scope
  and conciseness, never by derivability alone. Verification opens exactly
  one source file; it is not a source-tree audit license.
- Code-comment candidates carry no numeric threshold: they pass the hard
  gates and must be scoped to a specific owning artifact. They pay review
  cost on every diff touching the file, so doc comments stay roughly 1-5
  lines and larger invariants go to module docs.

## What We Deliberately Did Not Adopt

- Shipping lints or tooling from this plugin. Mechanical enforcement stays
  a recommendation the skills can point at, not something agent-docs builds.
- Replacing `AGENTS.md` destinations. Code comments serve agents and humans
  that touch the artifact; agents that must know before opening the file
  still need prompt-resident memory (hence the optional one-line pointer).
  The tier is additive.
- `curate` and `bootstrap-agent-docs` behavior changes. Their shared-policy
  copies update mechanically; routing changes for `curate` are a follow-up.

## Rollback

Revert the policy, skill, and scenario changes: candidates fall back to the
two-surface model (`AGENTS.md`/`docs/`), and `AGENTS.md` entries relocated
into doc comments remain valid documentation where they landed — only the
routing rule is lost, not the knowledge.

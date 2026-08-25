# Design Record Discipline

**Status:** Approved

## Problem

The code-adjacent tier settled where artifact-scoped knowledge lives, but
left `docs/design/` economics implicit. Repositories observed in the wild
(most concretely `dms-api-server`) mix two very different things under
`docs/design/`: dated per-change records and living contract documents.
They also let implementation narration ("code changes" step lists, API
schema copies) persist inside landed records, where it silently drifts
from the code it describes.

## Evidence

- `dms-api-server` keeps 40+ dated design records plus a family of living
  contract docs (identity rules, lifecycle contracts). Its `AGENTS.md`
  Hidden Knowledge entries run a thin-pointer pattern at scale: a 1-3 line
  contract summary plus a link to the full design doc.
- A dated record describing an Odin-side data bug reads "temporary
  client-side fix; root fix belongs to the Odin team" — temporal and
  organizational context no doc comment or git log can carry.
- Landed records that contained implementation narration drift; frozen
  decision statements do not, because they stop describing the present.

## Decision

1. **Tense discipline.** A design decision record is frozen once its
   decision lands; later edits only update the Status line. To change a
   decision, write a new record and supersede the old one explicitly.
   Freezing removes the sync burden — a record cannot drift because it no
   longer claims to describe current state.
2. **Two kinds, two audit tests.** Decision records (`Approved` /
   `Frozen` / `Superseded`) are exempt from doc↔source drift checks; the
   remedy for a stale record is a superseding record. Living contracts
   (`Living`) state currently binding constraints and stay drift-audited.
   `curate` applies the distinction via its `Doc↔Source Drift` dimension.
3. **Thin pointer, generalized.** When knowledge has a long-form
   authoritative copy — a module doc or a design contract — the
   `AGENTS.md` entry is a 1-3 line summary plus a link, never an inline
   copy of the contract body.
4. **Pairing.** When one decision yields both a design record and
   artifact-scoped invariants, `learn` proposes the design diff and its
   `Code` comment diffs in the same batch: the design records why, the
   comments carry the now-binding invariants.

Implementation narration is plan-time content: after landing, code and its
doc comments are authoritative, and the record keeps only the decision
analysis (background, alternatives, organizational context, rollback).

## What We Deliberately Did Not Adopt

- Mandatory Status vocabulary enforcement or tooling — the Status-line
  convention is guidance, not a lint.
- Splitting living contracts into a separate top-level category; they stay
  in `docs/design/` and are told apart by their Status line.

## Rollback

Revert the reference and skill edits. Consequences: landed records may be
rewritten in place (drift returns), inline contract copies in `AGENTS.md`
are no longer flagged, and design/Code pairing becomes optional again.
No knowledge is lost — only the discipline.

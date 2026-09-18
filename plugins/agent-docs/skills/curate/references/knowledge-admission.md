# Knowledge Admission Policy

Shared criteria for deciding whether knowledge merits persistence and where it
belongs. `learn`, `remember`, `curate`, `bootstrap-agent-docs`, and
`setup-coding-rules` apply these criteria within their own scopes and workflows.
This reference does not trigger a workflow, authorize edits, or prescribe an
investigation sequence.

## Evidence and authority

Persisted claims need current source, command, or authoritative-context support.
Distinguish verified facts from behavioral rules the user explicitly chooses to
adopt: adoption establishes a new expectation, not evidence of historical policy.
Do not invent project facts to justify a requested rule. Unsupported claims stay
unverified rather than becoming repository guidance.

Knowledge should serve a future task beyond the temporary attempt, have an
identified authoritative home, and avoid duplicating an adequate existing carrier.
Follow local retention requirements and preserve historical decision records
according to repository conventions; current-contract drift does not by itself
invalidate a point-in-time record.

## Admission and residual value

Admit knowledge when it changes a future decision or action and its benefit
justifies the maintenance and context cost of the chosen surface. Ask:

- Which future task or reader needs it, and what mistake or repeated work does it avoid?
- Why are the existing source, tests, automation, docs, or change records insufficient?
- Where can that reader find it at the right time with the least duplication?

Impact, recurrence, discovery cost, actionability, durability, and audience help
explain the judgment; they are not a numeric score or admission threshold. A rare
but costly failure can justify documentation, while broad scope alone cannot.

Non-derivability increases the cost of losing useful knowledge, but does not
establish usefulness or automatically admit it. Derivability alone also does not
justify rejection or deletion: commands, maps, runbooks, and rationale may save
substantial reconstruction effort or prevent mistakes.

Consider what value remains after existing carriers, including artifacts created
in the current session. Mechanical enforcement can carry the whole relationship,
or leave important rationale, operational steps, navigation, or compatibility
constraints unexplained. When an enforcing artifact and one targeted lookup
already supply the complete answer with no such residual value, skip redundant
prose; do not add a comment merely to narrate enforcement. Use relevant evidence,
not a mandatory sweep of every possible carrier.

## Placement

Choose the least costly authoritative surface that reaches the intended reader:

| Surface | Appropriate knowledge |
|---|---|
| Source, tests, or automation | Enforceable invariants; proposing prose does not authorize an unrelated implementation change |
| Owning doc comment or module doc | Explanation scoped to a function, type, file, or module; keep it close to the artifact and proportionate to the invariant |
| `docs/` | Longer or occasional design rationale, operational procedures, verification contracts, and navigation across artifacts |
| Nearest applicable `AGENTS.md` | Concise commands, rules, responsibility maps, and traps that must affect recurring work before the owning artifact is opened |
| No new entry | Generic, temporary, unsupported, redundant, or without identifiable future value |

For a long authoritative explanation, an entry-point summary or pointer may be
sufficient. Keep explanations concise without fixed line targets, copy neither
volatile implementation bodies nor whole contracts, and respect the repository's
language and documentation conventions. An artifact-scoped fact does not earn
prompt residency merely because it is difficult to rediscover.

## Consistency across capture and audit

Use the same usefulness and placement criteria for new and existing knowledge.
Useful content may need correction or relocation rather than deletion. Neither
recoverability nor irrecoverability grants automatic deletion or permanent
retention. A removal proposal needs evidence of staleness, duplication, an
adequate replacement, or lack of future value; uncertain value is not proof of
uselessness. The invoking workflow owns verification, reporting, approval, and
application, including any local retention constraints.

---
name: codex-subagent-strategy
description: Choose Codex subagent roles and dispatch strategy. Use immediately before spawning only when the user explicitly requests subagents, delegation, parallel agents, or parent-model inheritance.
---

# Codex Subagent Strategy

Codex already knows how to call subagents. This skill creates a short,
just-in-time model-routing checkpoint for an explicitly requested delegation.
It does not authorize delegation.

This is a delegation aid, not a mandatory orchestrator framework. Apply the
preparation, handoff, and review gates only when the user has asked for a
delegated implementation; ordinary local work may proceed without a child.

## Subscription Gate

This skill's model routes (Terra/Luna/Sol) are valid only on an official
ChatGPT/Codex subscription. Before applying any route, inspect the active
spawn tool description: if it does not expose `gpt-5.6-terra`,
`gpt-5.6-luna`, or `gpt-5.6-sol` as available models, the session is not on
an official subscription. In that case, omit both `model` and
`reasoning_effort` for every spawn so all children inherit the parent model,
and skip the Routes section entirely.

This fallback must be reported to the user before dispatch: state that the
active provider is not an official subscription, so all children inherit the
parent model. Do not silently omit routing fields without this report.

Do not attempt to configure, install, or otherwise enable these models on a
non-official provider. Parent inheritance is the only fallback.

## Before The First Spawn

1. Read this skill before dispatching any child.
2. Check the Subscription Gate above. If the active spawn tool does not expose
   official subscription models, use parent inheritance for every spawn and
   stop here — do not apply the Routes table.
3. If the user requests no child-model routing or says every child must inherit,
   omit both `model` and `reasoning_effort` for every spawn and stop here.
4. Honor any explicit per-child model or effort requested by the user.
5. Read the active spawn tool description and select its call-shape adapter.
   V1 and V2 change only invocation and context mechanics; they do not change
   the model route or role selected below.
6. Decide whether a self-contained handoff can give the child everything it
   needs: outcome, design path when applicable, write scope, verification, and
   a stop condition. For an independent review, create a fresh review packet
   containing the scope, base, changed paths, acceptance criteria, and required
   gates; do not copy the parent reasoning or conclusions.
7. If a non-review child instead needs the whole parent history or unrecorded
   decisions, preserve that context and inherit the parent model.
8. Classify every remaining, self-contained child and apply the first matching
   route below.

Do not load this skill for conceptual questions about subagents or ordinary
tasks where the user did not explicitly request delegation.

## Preparation For Implementation Delegation

Before handing implementation to a child, read every file that the requested
change is expected to touch and trace callers of each changed public symbol.
State the evidenced root cause in one sentence (or, for new behavior, the
required behavior and its source). If that cannot be stated, keep the work
native or route it as complex; do not disguise uncertainty as a routine task.

This preparation is scoped to the delegated unit. It is not a requirement to
turn an otherwise straightforward task into a multi-agent orchestration.

## Routes (official subscription only)

Only self-contained explorers, implementation workers, and independent
reviewers receive routes from this skill. A self-contained handoff is the
cost-and-throughput boundary: it lets Codex use a purpose-fit child model
without copying the whole parent turn.

| Child task shape | Model | Effort |
|---|---|---|
| Explorer: any read-only discovery or research, including codebase tracing, documentation lookup, dependency investigation, or symbol mapping | `gpt-5.6-terra` | `high` |
| Complex implementation: high-coupling integration, or a concrete change with unresolved cross-component behavior | `gpt-5.6-terra` | `xhigh` |
| Routine implementation: a concrete, bounded coding or test change without high coupling | `gpt-5.6-luna` | `max` |
| Fresh independent review, including security review | `gpt-5.6-sol` | `high` |
| Anything else | native | native |

Evaluate high coupling before the narrow-task route. High coupling includes API
or schema contracts, persistence, migrations, concurrency, distributed state,
authentication, and multi-stage state machines.

A routine implementation has a concrete outcome and verification command, and
all of these are explicit:

- objective and out-of-scope behavior;
- a write set of at most two files;
- an existing pattern to imitate, cited as `path:line`;
- no open product, architecture, contract, or migration decision;
- acceptance behavior and verification command.

Complex implementation covers a high-coupling boundary even when an approved
design exists. It also covers a concrete task whose cross-component behavior,
contract, or rollout implications cannot be made routine in the handoff. Route
as complex when three or more files, an unclear shape, ordering/retry/
concurrency behavior, a trust boundary (input, authentication, secrets, or
payments), a schema or hard-to-reverse change, or two blocking review cycles
are involved. Ambiguity about a concrete implementation's shape routes to
complex, never to a separate fast mode.

Every self-contained read-only exploration task uses Terra/high, regardless of
breadth or source. Every independent review uses a fresh Sol/high child,
including security review, using the independent-child adapter below. Test
execution, planning, design, mixed-purpose work, a request without a concrete
goal or scope, and non-review children that require the whole parent history
stay native. Native means Codex decides: omitted settings inherit normally, and
Codex may still override one or both settings when useful.

## Spawn Rules

- For a prescribed route, pass both `model` and `reasoning_effort` explicitly,
  using an adapter/context form that permits them.
- For a child that requires whole-parent history, omit both fields. It is an
  intentional inheritance decision, not a failed route.
- Do not give an independent reviewer whole-parent history just to avoid
  preparing a review packet. That breaks the fresh Sol/high review boundary.
- Check the active spawn tool's model and effort metadata before dispatch. A
  pair is unavailable only when no compatible invocation form exposes it.
- If the exact pair is unavailable, report a **route exception** with the
  attempted pair and the tool limitation. Then choose and name either an
  available explicit pair or parent inheritance based on the child’s context
  need. Do not silently omit the fields or call automatic selection compliance.
  Ask the user only when they required that exact pair or the choice changes a
  material task outcome. The Luna/max recovery rule below overrides this
  fallback choice for a rejected routine-Luna route.
- A custom agent file that pins model settings keeps its normal precedence. If
  the Luna/max routine route is rejected but the active tool lists
  `agent_type: "luna_max"`, invoke that role and omit raw `model` and
  `reasoning_effort`; report the role as the actual Luna/max route.
- If the Luna/max route is rejected and `luna_max` is not listed, report the
  attempted pair and the rejection, then ask whether the user wants the
  optional `codex-luna-agent-config` skill to configure that isolated role.
  Do not load that skill, edit Codex configuration, or silently substitute a
  native/other-model worker until the user explicitly approves.
- If the user declines configuration but still wants delegation, say that the
  Luna route remains unavailable and ask them to choose a named available pair
  or parent inheritance. A refusal is not permission to pick that fallback;
  dispatch it only after the user chooses.
- Worker prompts use these labeled fields: `GOAL`, `FILES`, `PATTERN`,
  `CONSTRAINTS`, and `DONE WHEN`. `PATTERN` cites the existing `path:line` to
  imitate; if no usable pattern can be named, route the work as complex.
  `DONE WHEN` includes the verification command and observable acceptance
  behavior. Ask the worker to return unresolved decisions rather than inventing
  them. If this contract needs more than two short paragraphs of explanation,
  split the work first. Explorer prompts instead state the read-only question
  and required discovery output.
- Do not spawn an extra child just to classify another spawn.

## Fresh Review Gate

After a meaningful delegated implementation diff, use a fresh Sol/high child
for adversarial review. Give it the diff, `GOAL`, `CONSTRAINTS`, changed paths,
base, and required verification — not the parent solution rationale or the
implementer's reasoning. Send a blocking finding verbatim to the same
implementer. A second blocking review for the same routine unit escalates that
unit to Terra/xhigh; the parent decides and records any non-blocking risk.

This is a gate for delegated implementation, not a rule that every ordinary
edit must be orchestrated or independently reviewed.

### Spawn Adapter

Never infer spawn fields from memory or another runtime. Inspect the active
tool schema. The route table above applies unchanged to both versions.

| Active tool shape | Independent prescribed child | Whole-parent-history child |
|---|---|---|
| V1 `multi_agent_v1__spawn_agent` | Use `fork_context: false`; pass route `model` and `reasoning_effort` only when the schema exposes them. | Use `fork_context: true`; omit route fields as an intentional inheritance decision. |
| V2 `spawn_agent` | Supply required `task_name` and `message`; use `fork_turns: "none"` (or a small positive window when essential recent context is known) and pass route fields only when exposed. | Omit `fork_turns` or use `"all"`; omit route fields as an intentional inheritance decision. |

For either version, use `agent_type: "luna_max"` only for a non-full-history
child. Full-history forks reject an `agent_type` override and must inherit the
parent role. Do not pass `fork_turns` to V1 or `fork_context` to V2.

```text
// V1 independent route
spawn_agent({ message: handoff, fork_context: false, model: route.model, reasoning_effort: route.effort })

// V2 independent route
spawn_agent({ task_name: name, message: handoff, fork_turns: "none", model: route.model, reasoning_effort: route.effort })
```

### Anti-Patterns

- **Hidden inheritance:** omitting `model` or `reasoning_effort` for a
  self-contained prescribed child is a route violation. Omitting them for an
  intentional full-history inheritance is correct.
- **Foreign parameters:** passing `fork_turns` to V1 or `fork_context` to V2.
- **Fork-first routing:** choosing a full-history mode for a self-contained
  worker, then claiming the inheritance choice makes the route unavailable.
- **Unapproved role installation:** loading `codex-luna-agent-config` or
  editing global Codex configuration merely because a Luna route failed.
- **Stale reviewer context:** using inherited parent history for a review that
  should be a fresh Sol/high assessment.
- **Unobservable fallback:** calling automatic selection a strategy fallback
  without reporting the attempted route, compatibility check, and actual pair
  or inheritance choice.

The Luna/max routine route, Terra/xhigh complex route, and fresh Sol/high
reviewer route are this skill's local policy. The context-boundary mechanics follow the official
[Codex Subagents guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents).

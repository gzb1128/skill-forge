---
name: codex-subagent-strategy
description: Use in Codex when the user explicitly asks to spawn subagents, delegate work, or run parallel agents and the parent is about to dispatch them; read this strategy before the first spawn and route explorers and implementation workers by task shape. Also use it when the user requests parent-model inheritance for every child so the opt-out is enforced.
---

# Codex Subagent Strategy

Codex already knows how to call subagents. This skill creates a short,
just-in-time model-routing checkpoint for an explicitly requested delegation.
It does not authorize delegation.

## Before The First Spawn

1. Read this skill before dispatching any child.
2. If the user requests no child-model routing or says every child must inherit,
   omit both `model` and `reasoning_effort` for every spawn and stop here.
3. Honor any explicit per-child model or effort requested by the user.
4. Read the active spawn tool description. Identify whether it is the V1
   `multi_agent_v1__spawn_agent` shape (`fork_context`) or the V2
   `collaboration.spawn_agent` shape (`fork_turns`).
5. Decide whether a self-contained handoff can give the child everything it
   needs: outcome, design path when applicable, write scope, verification, and
   a stop condition. If the child instead needs the whole parent history or
   unrecorded decisions, preserve that context and inherit the parent model.
6. Classify every remaining, self-contained child and apply the first matching
   route below.

Do not load this skill for conceptual questions about subagents or ordinary
tasks where the user did not explicitly request delegation.

## Routes

Only self-contained explorers and implementation workers receive routes from
this skill. A self-contained handoff is the cost-and-throughput boundary: it
lets Codex use a purpose-fit child model without copying the whole parent turn.

| Child task shape | Model | Effort |
|---|---|---|
| Explorer: any read-only discovery or research, including codebase tracing, documentation lookup, dependency investigation, or symbol mapping | `gpt-5.6-terra` | `high` |
| Approved pre-design plus high-coupling integration | `gpt-5.6-sol` | `medium` |
| Approved pre-design plus a narrow, fully decided boundary | `gpt-5.6-luna` | `xhigh` |
| General coding with a concrete implementation outcome | `gpt-5.6-terra` | `high` |
| Anything else | native | native |

Evaluate high coupling before the narrow-task route. High coupling includes API
or schema contracts, persistence, migrations, concurrency, distributed state,
authentication, and multi-stage state machines.

A pre-designed task is narrow only when its spawn prompt can cite the approved
design and all of these are explicit:

- objective and out-of-scope behavior;
- narrow, disjoint write set;
- no open product, architecture, contract, or migration decision;
- acceptance behavior and verification command.

General coding means normal code or test implementation with a concrete
outcome that does not match either pre-design route and does not require the
child to make design or product decisions.

Every self-contained read-only exploration task uses Terra/high, regardless of
breadth or source. Review, security analysis, test execution, planning, design,
ambiguous work, mixed-purpose work, and children that require the whole parent
history stay native. Native means Codex decides: omitted settings inherit
normally, and Codex may still override one or both settings when useful.

## Spawn Rules

- For a prescribed route, pass both `model` and `reasoning_effort` explicitly,
  using an adapter/context form that permits them.
- For a child that requires whole-parent history, omit both fields. It is an
  intentional inheritance decision, not a failed route.
- Check the active spawn tool's model and effort metadata before dispatch. A
  pair is unavailable only when no compatible invocation form exposes it.
- If the exact pair is unavailable, report a **route exception** with the
  attempted pair and the tool limitation. Then choose and name either an
  available explicit pair or parent inheritance based on the child’s context
  need. Do not silently omit the fields or call automatic selection compliance.
  Ask the user only when they required that exact pair or the choice changes a
  material task outcome.
- A custom agent file that pins model settings keeps its normal precedence.
- Worker prompts include the outcome, design path when applicable, write scope,
  verification, and a stop condition for unresolved decisions. Explorer prompts
  state the read-only question and required discovery output.
- Do not spawn an extra child just to classify another spawn.

### Context And Call Shape

Never infer spawn fields from memory or another agent runtime. Before the first
spawn, inspect the active tool description for its model, reasoning, and
context-propagation fields. Do not decide context propagation before deciding
whether the worker can use a self-contained handoff.

#### Codex V1: `multi_agent_v1__spawn_agent`

V1 exposes independent `model`, `reasoning_effort`, and boolean `fork_context`
fields. It permits an explicit route with either context choice. Prefer
`fork_context: false` for self-contained work to avoid copying unnecessary
history. For a child that needs the whole parent history, set
`fork_context: true` and omit both route fields.
Although V1 technically permits a routed full-context child, this strategy
treats a child that truly needs the whole parent history as inheritance-first
so the same context boundary applies across V1 and V2.

```text
spawn_agent({
  message: child_prompt,
  model: route.model,
  reasoning_effort: route.effort,
  fork_context: true | false,
})
```

Do not include `fork_turns` in a V1 call.

```text
spawn_agent({
  message: child_prompt,
  fork_context: true,
  // no model or reasoning_effort
})
```

#### Codex V2: `collaboration.spawn_agent`

V2 exposes `fork_turns` (and normally `task_name`, `model`, and
`reasoning_effort`). Full-history mode — `fork_turns` omitted or set to
`"all"` — inherits the parent model and effort and does not accept model
overrides. Use it only for a child that needs the whole parent history:

```text
spawn_agent({
  task_name: child_name,
  message: child_prompt,
  fork_turns: "all",
  // no model or reasoning_effort
})
```

For a prescribed route, use `fork_turns: "none"` or a positive integer string
and include both route fields. Prefer `"none"` when the handoff is complete;
use a small positive window only when recent turns contain essential context.

```text
spawn_agent({
  task_name: child_name,
  message: self_contained_handoff,
  fork_turns: "none",
  model: route.model,
  reasoning_effort: route.effort,
})
```

Do not include `fork_context` in a V2 call.

### Anti-Patterns

- **Hidden inheritance:** omitting `model` or `reasoning_effort` for a
  self-contained prescribed child is a route violation. Omitting them for an
  intentional full-history inheritance is correct.
- **Foreign parameters:** passing `fork_turns` to V1 or `fork_context` to V2.
- **Fork-first routing:** choosing V2 `fork_turns="all"` for a self-contained
  worker, then claiming that its no-override rule makes the route unavailable.
- **False unavailability:** treating V2 full-history mode as proof that a
  `"none"` or numeric-window invocation cannot use a model/effort pair.
- **Unobservable fallback:** calling automatic selection a strategy fallback
  without reporting the attempted route, compatibility check, and actual pair
  or inheritance choice.

The Luna/Terra bias is consistent with the official [Codex Subagents
guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents); the Sol
route is this skill's policy for design-backed high-coupling implementation.

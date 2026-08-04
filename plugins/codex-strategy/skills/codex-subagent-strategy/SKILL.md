---
name: codex-subagent-strategy
description: Use in Codex when the user explicitly asks to spawn subagents, delegate work, or run parallel agents and the parent is about to dispatch them; read this strategy before the first spawn and route implementation workers by task shape. Also use it when the user requests parent-model inheritance for every child so the opt-out is enforced.
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
4. Classify each remaining child and apply the first matching route below.

Do not load this skill for conceptual questions about subagents or ordinary
tasks where the user did not explicitly request delegation.

## Routes

Only implementation workers receive a route from this skill.

| Worker task shape | Model | Effort |
|---|---|---|
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

Exploration, review, security analysis, test execution, docs, research,
planning, design, ambiguous work, and mixed-purpose work stay native. Native
means Codex decides: omitted settings inherit normally, and Codex may still
override one or both settings when useful.

## Spawn Rules

- For a prescribed route, pass both `model` and `reasoning_effort` explicitly.
- Check the active spawn tool's model and effort metadata first. If the pair is
  unavailable, return that child to native selection; do not claim the route
  was used.
- A custom agent file that pins model settings keeps its normal precedence.
- Worker prompts include the outcome, design path when applicable, write scope,
  verification, and a stop condition for unresolved decisions.
- Do not spawn an extra child just to classify another spawn.

The Luna/Terra bias is consistent with the official [Codex Subagents
guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents); the Sol
route is this skill's policy for design-backed high-coupling implementation.

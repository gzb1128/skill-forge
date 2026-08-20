---
name: codex-luna-agent-config
description: Configure a local luna_max Codex agent only after a Luna spawn route was rejected and the user explicitly approves the fallback. Do not use for ordinary subagent routing.
---

# Codex Luna Agent Config

This skill configures an opt-in local role after a real Luna dispatch failure.
It is not part of ordinary subagent routing and does not authorize delegation.

## Required Trigger

Proceed only when both conditions hold:

1. A direct active-spawn invocation rejected `gpt-5.6-luna`; report the tool,
   attempted model/effort, and observed rejection before changing configuration.
2. The user explicitly approves installing or configuring the `luna_max` role.

If either condition is missing, stop. State that the role can be configured
after approval; do not read or edit global Codex configuration just to prepare.

## Configure The Isolated Role

1. Resolve the active user-level Codex configuration root. It is normally
   `~/.codex`; use a different root only when the runtime or an explicit test
   fixture identifies one.
2. Discover role names before writing: inspect every `[agents.*]` declaration
   in `config.toml`, resolve each referenced `config_file`, and inspect every
   existing `agents/*.toml` file. A declared role normally uses its table key;
   a standalone file uses its required `name`. Preserve unrelated settings,
   roles, model defaults, and comments.
3. If exactly one source resolves to `luna_max` and it already pins Luna/max,
   report it as configured and do not rewrite it. This includes a compatible
   existing `[agents.luna_max]` declaration or a compatible standalone file.
4. Stop and show a conflict if multiple sources resolve to `luna_max`, the one
   resolved role has incompatible behavior, or the intended
   `agents/luna-max.toml` path already contains an unrecognized role. A single
   compatible role at another path is already configured, not a conflict. Do
   not replace another role or overwrite an ambiguous file without explicit
   user direction.
5. Otherwise create one standalone `agents/luna-max.toml`. Do not add an
   `[agents.luna_max]` declaration for a new role; this keeps `config.toml`
   unchanged and avoids two definitions for the same role:

   ```toml
   name = "luna_max"
   description = "Use for clear, bounded subagent tasks that should run with GPT-5.6 Luna at max reasoning effort."
   developer_instructions = "Use this role only for a clear, self-contained task. Stay within the requested scope, run the requested verification when possible, and report unresolved decisions instead of expanding the task."
   model = "gpt-5.6-luna"
   model_reasoning_effort = "max"
   ```

Do not set `agents.default_subagent_model` or
`agents.default_subagent_reasoning_effort`. This role is selected per child and
must not convert all subagents to Luna/max.

## Verify And Use

1. Use a read-only Codex configuration load check, such as `codex features
   list`, and report its result.
2. Tell the user to start a new Codex task or restart the client so the active
   spawn schema can expose `agent_type: "luna_max"`.
3. For a self-contained worker, select the role and omit raw model fields:

   ```text
   // V1
   spawn_agent({ agent_type: "luna_max", fork_context: false, message: handoff })

   // V2
   spawn_agent({ task_name: name, agent_type: "luna_max", fork_turns: "none", message: handoff })
   ```

The role avoids the raw `model` parameter path that previously rejected Luna.
It cannot grant model access: if role-based dispatch still fails, report the
server/runtime availability error and do not claim that configuration bypassed
it.

## Never

- Do not load this skill from `codex-subagent-strategy` before the user says
  yes.
- Do not silently replace a rejected Luna worker with another model.
- Do not rewrite a conflicting `luna_max` role.
- Do not test-spawn a child unless the user separately asks to delegate one.

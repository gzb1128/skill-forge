---
name: configure-explore-small
description: Use when configuring an OpenCode explore-small subagent for small-model quick reference, narrow file lookup, simple symbol searches, or small-context exploration. Triggers on "configure explore-small", "small model explore agent", "quick reference agent", or "fast exploration agent".
---

# Configure Explore Small

Configure a dedicated OpenCode `explore-small` subagent for quick reference,
narrow searches, and small-context exploration.

## Why This Is A Skill, Not An Agent

Do not ship `explore-small` as a static marketplace `agents/` entry.

- The model must be user-selected. Ask for the concrete `provider/model-id`;
  do not silently reuse `small_model` from existing config.
- Custom providers may need model metadata first. **REQUIRED SUB-SKILL:** Use
  `hydrate-opencode-models` when the selected model is missing provider/model
  metadata.
- OpenCode does not load global agents from `~/.agents/agents`. It loads agents
  from `~/.config/opencode/agent(s)` and project `.opencode/agent(s)`. The
  `~/.agents/skills` path is for external skills.

## Security Gate

OpenCode config files may contain API keys and tokens. Do not read or edit any
OpenCode config file until the user explicitly consents.

Ask:

> I need to inspect or update your OpenCode config to add `explore-small`. The
> config may contain API keys and tokens. Do you trust me to read and edit it?

Options:

| Choice | Behavior |
|---|---|
| Trust | Read OpenCode config only when needed, write the agent file, and validate it. |
| Do not trust | Ask for the target scope and concrete model, then return the exact file content for the user to apply manually. |

## Required Questions

Ask these before writing anything:

| Question | Required | Default |
|---|---|---|
| Concrete model | Yes | No default. The user must provide `provider/model-id`. |
| Scope | Yes | Project-level `.opencode/agent/explore-small.md` unless the user asks for global. |
| Model metadata | Conditional | If provider metadata is missing or tool-call support is unknown, use `hydrate-opencode-models`. |

Never infer the model from `small_model`. If the user says "use my current
small model", ask them to provide the concrete model string instead, or ask for
explicit trust before reading config only to discover and confirm that value.

## Agent File

Prefer the file form because `explore-small` needs a non-trivial prompt.

Resolve the project-level path from the project root, not the caller's current
subdirectory. Use the existing `.opencode` directory if present; otherwise use
the git worktree root and create `.opencode/agent/` there.

Project-level path:

```text
.opencode/agent/explore-small.md
```

Global path:

```text
~/.config/opencode/agent/explore-small.md
```

Use this template, replacing `<provider/model-id>` with the user-approved model:

```markdown
---
description: Small-model exploration subagent for quick reference, narrow file lookup, simple symbol searches, and small-context questions. Do not use for complex project logic, broad architecture tracing, deep debugging, or multi-package investigation.
mode: subagent
model: <provider/model-id>
permission:
  edit: deny
  bash: deny
  task: deny
  todowrite: deny
  question: deny
  skill: deny
  webfetch: deny
  websearch: deny
  plan_enter: deny
  plan_exit: deny
---

You are the small-model quick reference exploration subagent.

Use this agent only when:
- The caller needs a quick reference answer.
- The expected context fits in a few targeted files.
- The task can be answered with narrow Glob, Grep, Read, or symbol lookup.

Do not use this agent for:
- Complex project logic or multi-step reasoning across many files.
- Broad architecture tracing.
- Deep debugging or root-cause analysis.
- Multi-package or cross-repository investigation.

Workflow:
- Keep searches narrow and stop once you have enough evidence.
- Prefer Glob and Grep before reading files.
- Read only the smallest set of files needed to answer.
- If the task expands beyond small-context exploration, stop and tell the caller to use `explore` or `general` instead.
- Return concise findings with absolute file paths.
- Do not create files, edit files, run shell commands, or mutate system state.
```

## Validation

After writing:

1. Re-read the generated agent file and confirm the frontmatter is valid YAML.
2. Confirm `mode: subagent` and `model: <provider/model-id>` are present.
3. Confirm the selected model supports tool calls. If provider metadata is
   missing or `tool_call` is false, stop and use `hydrate-opencode-models` or
   ask the user for a different model.
4. Confirm the description includes both the allowed quick-reference cases and
   the forbidden complex-exploration cases.
5. Confirm no `~/.agents/agents` path was created or recommended.
6. If provider/model metadata was changed, run the validation required by
   `hydrate-opencode-models`.
7. Remind the user to restart OpenCode because agent config is not hot-reloaded.

## Existing Agent Gate

If the target `explore-small.md` already exists:

1. Read it only after trust approval.
2. Show the existing path and a diff of the proposed replacement.
3. Ask before overwriting or merging.
4. If the user does not approve, return a snippet only and do not edit.

## Report Format

End with:

```text
Configured: explore-small
Scope: <project|global|snippet only>
Model: <provider/model-id>
Path: <agent file path or "not written">
Use for: quick reference, narrow searches, small-context exploration
Do not use for: complex logic, architecture tracing, deep debugging, multi-package investigation
Restart required: yes
```

## Common Mistakes

- Reusing `small_model` without asking. The agent must be configured with a
  concrete user-approved model.
- Skipping the security gate. Do not read secret-bearing OpenCode config before
  the user explicitly trusts you to inspect it.
- Skipping the tool-call check. A small model without tool support cannot power
  an exploration subagent that needs Glob, Grep, and Read.
- Overwriting an existing `explore-small.md` without showing a diff and asking.
- Shipping an `agents/` plugin entry. OpenCode does not load agents from
  `~/.agents/agents`.
- Using inline JSON for the whole agent. The file form is clearer for a prompt
  with strict usage boundaries.
- Adding wildcard permission denies such as `"*": deny`. Static wildcard denies
  can accidentally block reference-directory behavior; prefer targeted denials
  for mutating or out-of-scope tools.
- Forgetting to restart OpenCode after writing the agent file.

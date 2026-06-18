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
- Custom (config-declared) providers may need model metadata first. **REQUIRED
  SUB-SKILL:** Use `hydrate-opencode-models` only when the selected model
  belongs to a custom provider in `opencode.json` and is missing metadata. This
  does NOT apply to built-in providers — see "Provider Types" below.
- OpenCode does not load global agents from `~/.agents/agents`. It loads agents
  from `~/.config/opencode/agent(s)` and project `.opencode/agent(s)`. The
  `~/.agents/skills` path is for external skills.

## Provider Types: Built-in vs Custom

OpenCode providers come in two kinds, and the validation path differs. Determine
which kind `provider/model-id` refers to before validating tool-call support.

### Built-in providers (no `opencode.json` entry needed)

OpenCode ships providers as plugins registered in
`packages/core/src/plugin/provider.ts` (e.g. `openai`, `anthropic`, `google`,
`azure`, `google-vertex`, `xai`, `mistral`, `groq`, `cohere`, `perplexity`,
`openrouter`, `vercel`, `amazon-bedrock`, and others).

- They need NO entry in `opencode.json`. Looking for them in config and
  rejecting the model as "not defined" is an anti-pattern.
- Their model catalog is fetched from **models.dev**
  (`packages/core/src/models-dev.ts`, source `https://models.dev`), not from
  config. Trust the catalog or the user's claim for model existence; do not
  force `hydrate-opencode-models`.
- Their credentials are NOT stored in `opencode.json`. Auth (OAuth tokens or API
  keys) lives in **`~/.local/share/opencode/auth.json`**
  (`packages/opencode/src/auth/index.ts`, written mode `0600`). For example,
  `openai` authenticates via OpenAI's Codex device/browser OAuth flow
  (`packages/core/src/plugin/provider/openai-auth.ts`).
- To check or establish auth for a built-in provider, tell the user to run
  `opencode auth login` (OAuth) or set the provider's API-key environment
  variable. Never paste API keys or OAuth tokens into `opencode.json` or the
  agent file.

### Custom providers (declared in `opencode.json`)

Providers the user added under the `provider` block of `opencode.json` DO need a
config entry with their `models` map and `options` (apiKey/baseURL). For these,
verify the model block exists and `tool_call` is true, and use
`hydrate-opencode-models` when metadata is missing.

### Why this matters

A model like `openai/<model>` is valid as long as the built-in `openai` plugin
is registered (always) and OpenAI auth exists in `auth.json`. The skill must not
block on "no `openai` provider in config" — there is nothing to read or add
there. Only custom providers warrant a config read for model metadata.

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
| Model metadata | Conditional | Only for **custom** providers declared in `opencode.json`: use `hydrate-opencode-models` if metadata/tool-call support is missing. For **built-in** providers, do not require config metadata; model info comes from models.dev. |

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
3. Confirm the selected model supports tool calls, by provider type:
   - **Built-in provider** (in `packages/core/src/plugin/provider.ts`): trust
     models.dev for tool-call support; do NOT search `opencode.json`. Confirm
     auth exists in `~/.local/share/opencode/auth.json`; if missing, tell the
     user to run `opencode auth login` or set the provider API-key env var. Do
     not invoke `hydrate-opencode-models` for built-in providers.
   - **Custom provider** (declared in `opencode.json`): read its `models` block
     and require `tool_call: true`. If metadata is missing or false, use
     `hydrate-opencode-models` or ask for a different model.
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
- Treating a built-in provider (e.g. `openai`, `anthropic`) as missing because
  it has no entry in `opencode.json`. Built-in providers are plugins; their
  models come from models.dev and their auth lives in `auth.json`. Do not block
  the agent on a non-existent config entry, and do not force
  `hydrate-opencode-models` for them.
- Writing API keys or OAuth tokens into `opencode.json` or the agent file.
  Built-in provider credentials belong in `auth.json` (via `opencode auth
  login`) or an environment variable, never in config.

# configure-explore-small

`configure-explore-small` configures a dedicated OpenCode `explore-small`
subagent for small-model exploration.

Use it when the user wants a fast exploration agent for quick reference, narrow
file lookup, simple symbol searches, and small-context questions.

## Why This Is A Skill, Not A Shipped Agent

This plugin intentionally ships a skill instead of an `agents/` entry.

First, `explore-small` must be bound to a user-selected concrete model. The
skill needs to ask which `provider/model-id` to use and may need to run the
`hydrate-opencode-models` workflow if a custom provider or missing model
metadata is involved. A static marketplace agent cannot safely make that
configuration decision.

Second, OpenCode does not discover global agents from `~/.agents/agents`.
OpenCode loads agent files from `~/.config/opencode/agent(s)` and project
`.opencode/agent(s)` directories. The `~/.agents/skills` path is for external
skill discovery. This was verified from the OpenCode source, specifically:

- `packages/opencode/src/config/paths.ts`
- `packages/opencode/src/config/config.ts`
- `packages/opencode/src/skill/index.ts`

Because of those constraints, the correct package shape is a skill that writes
OpenCode configuration or agent files after user Q&A.

## Provider Types: Built-in vs Custom

The skill distinguishes two provider kinds because the validation path differs.
This was verified from the OpenCode source.

Built-in providers are shipped as plugins and need no `opencode.json` entry:

- Plugin registry: `packages/core/src/plugin/provider.ts` registers providers
  such as `openai`, `anthropic`, `google`, `azure`, `xai`, `mistral`, `groq`,
  and others.
- Model catalog source: `packages/core/src/models-dev.ts` fetches from
  `https://models.dev`, so model existence/tool-call support does not come from
  config.
- Auth storage: `packages/opencode/src/auth/index.ts` persists OAuth/API
  credentials to `~/.local/share/opencode/auth.json` (mode `0600`), separate
  from `opencode.json`. For example `openai` uses OpenAI's Codex OAuth flow in
  `packages/core/src/plugin/provider/openai-auth.ts`.

Custom providers the user declared under the `provider` block of `opencode.json`
are different: they require a config entry with a `models` map and `options`
(apiKey/baseURL), and may need `hydrate-opencode-models` for missing metadata.

Consequence: a model like `openai/<model>` is valid without any `opencode.json`
entry as long as OpenAI auth exists in `auth.json`. The skill must not reject it
as "not defined in config" — that is an anti-pattern. Only custom providers
warrant a config read for model metadata.

## Expected Output

The skill normally creates an agent file at one of these paths:

- `.opencode/agent/explore-small.md` for project-specific configuration
- `~/.config/opencode/agent/explore-small.md` for global configuration

For project-specific configuration, the path is resolved from the project root,
not from an arbitrary current subdirectory.

The generated agent should be used only for quick reference and small-context
exploration. It should not be used for complex project logic, broad architecture
tracing, deep debugging, or multi-package investigation.

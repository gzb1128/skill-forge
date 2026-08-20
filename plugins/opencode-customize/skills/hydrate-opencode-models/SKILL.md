---
name: hydrate-opencode-models
description: Fill a custom OpenCode provider model with Models.dev capabilities, limits, modalities, and pricing. Use when adding or hydrating model metadata in opencode.json or opencode.jsonc.
---

# Hydrate OpenCode Model Parameters

## Security Gate (MANDATORY — do this first)

opencode config files contain API keys and auth tokens. **You MUST NOT read any opencode config file until the user explicitly consents.**

### Step 0: Ask for trust decision

Use the `question` tool to ask the user:

> "I need to read your opencode config to see which providers and models you have. The config contains API keys and tokens. Do you trust me to read it?"

Provide two options:

1. **Trust — read config directly** — I'll read your opencode.json/opencode.jsonc, identify all custom providers with missing/bare model definitions, and hydrate them.
2. **Don't trust — tell me model names** — You tell me which model names to look up, I'll fetch specs from Models.dev and return the config block for you to paste yourself.

**If the user chooses "Don't trust":**

- Ask which model names they want configured (e.g. "glm-5.1, kimi-k2.6").
- Follow Step 1–3 below to fetch specs from Models.dev.
- **Do NOT read or edit any opencode config file.** Output the JSON snippet to chat for the user to paste themselves.
- Stop here — do not proceed to Step 4.

**If the user chooses "Trust":**

- Read the opencode config file(s) to identify custom providers and their models.
- Proceed with Step 1–4 below.

## Core Pattern

Models.dev (`https://models.dev/api.json`) is a JSON catalog keyed by provider ID. Each provider has a `models` map with full metadata. For custom providers opencode does NOT auto-inherit this data — it must be specified manually.

### Step 1: Find the model in Models.dev

```bash
curl -s https://models.dev/api.json | jq --arg MODEL "glm-5.1" '
  to_entries[] |
  select(.value.models | to_entries[] | .key | ascii_downcase == ($MODEL | ascii_downcase)) |
  {provider: .key, model_key: (.value.models | to_entries[] | select(.key | ascii_downcase == ($MODEL | ascii_downcase)) | .key)}
'
```

Pick the **canonical provider** (the model's creator/owner). Use the returned `model_key` exactly as-is in Step 2 — the key casing is not always lowercase (e.g. `MiniMax-M2.7`).

Examples:

| Model | Canonical provider |
|-------|--------------------|
| GLM-5.1, GLM-4.7 | `zai` or `zhipuai` |
| Kimi-K2.6 | `moonshotai` |
| MiniMax-M2.7 | `minimax` |
| Claude-* | `anthropic` |
| GPT-* | `openai` |

### Step 2: Fetch the model definition

```bash
curl -s https://models.dev/api.json | jq '.zai.models["glm-5.1"]'
```

### Step 3: Map to opencode config schema

Transform the Models.dev fields into opencode model config:

| Models.dev field | opencode config field | Notes |
|------------------|-----------------------|-------|
| `limit.context` | `limit.context` | Required |
| `limit.output` | `limit.output` | Required |
| `limit.input` | `limit.input` | Optional |
| `modalities.input` | `modalities.input` | Array of "text","image","audio","video","pdf" |
| `modalities.output` | `modalities.output` | Array |
| `reasoning` | `reasoning` | boolean |
| `tool_call` | `tool_call` | boolean |
| `temperature` | `temperature` | boolean |
| `attachment` | `attachment` | boolean |
| `interleaved` | `interleaved` | `true` or `{ "field": "reasoning_content" }`; preserve exactly because GLM and Kimi may lose reasoning output if the mapping is omitted |
| `cost.input` | `cost.input` | Per 1M tokens (USD) |
| `cost.output` | `cost.output` | Per 1M tokens |
| `cost.cache_read` | `cost.cache_read` | Optional |
| `cost.cache_write` | `cost.cache_write` | Optional |

### Step 4: Write to opencode config (Trust path only)

Apply the hydrated model definitions to the opencode config file using the `edit` tool. Preserve all existing fields the user did not ask to change.

### Step 5: Validate the config after writing

Do not leave the config in a broken state. After editing:

1. **Re-read the edited file** and confirm the JSON/JSONC structure is intact (balanced braces, no trailing commas, valid keys).
2. **Confirm required fields** on every hydrated model: `limit.context` and `limit.output` are present and ≥ 1. Missing `limit` crashes opencode (`maxOutputTokens must be >= 1`).
3. **Confirm the edited provider block still parses** — for `opencode.json`, run `jq empty <file>`; for `opencode.jsonc`, re-read and confirm structure by eye (jq does not parse comments).
4. If validation fails, revert the edit and report the parse error. Tell the user exactly what broke.
5. Remind the user to restart opencode and watch for startup errors.

Example output:

```jsonc
{
  "provider": {
    "my-gateway": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://gateway.example.com/v1" },
      "models": {
        "glm-5.1": {
          "name": "GLM-5.1",
          "reasoning": true,
          "tool_call": true,
          "temperature": true,
          "attachment": false,
          "interleaved": { "field": "reasoning_content" },
          "modalities": { "input": ["text"], "output": ["text"] },
          "limit": { "context": 200000, "output": 131072 },
          "cost": { "input": 1.4, "output": 4.4 }
        }
      }
    }
  }
}
```

## Batch Hydration

When multiple models need hydration, fetch once and process all:

```bash
curl -s https://models.dev/api.json -o /tmp/models-dev.json
cat /tmp/models-dev.json | jq '.zai.models["glm-5.1"]'
cat /tmp/models-dev.json | jq '.moonshotai.models["kimi-k2.6"]'
cat /tmp/models-dev.json | jq '.minimax.models["MiniMax-M2.7"]'
```

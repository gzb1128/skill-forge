---
name: integrate-projects
description: Use when a project needs persistent access to one or more external codebases in opencode. Triggers on "integrate projects", "add external projects", "link codebases", or "configure project references".
---

# Integrate External Projects

Configure an opencode project to access multiple external codebases persistently, skipping permission prompts and giving the agent the context it needs to work across them.

## What This Skill Does

One thing: **`references` in `opencode.json`**.

- opencode injects each described reference's resolved `path` and `description` into the agent's system prompt at session start — the agent knows what each external codebase is and when to consult it without reading any files upfront. The alias key is used for `@` autocomplete.
- Referenced directories are automatically added to the `external_directory` allowlist — no permission prompts.
- The agent can then freely use `read`/`glob`/`grep` to explore those directories on demand.

Do NOT modify the project's `AGENTS.md` for this purpose. `AGENTS.md` belongs to the project's own knowledge. References are the right mechanism: each external project stays independent, the agent integrates them via the reference descriptions.

Read-only references are **not supported by this skill**. Current opencode permission behavior can allow edits under referenced external directories even when `permission.edit` deny rules are present. If the user asks for read-only access, stop and explain that this skill will not configure read-only references until opencode can enforce them reliably; continue only if they approve read+write reference access.

**Key insight: `references` are automatically allowed.** opencode wires referenced directories into the `external_directory` allowlist at agent-initialization time. Do NOT add `permission.external_directory` allow rules for referenced paths, and do NOT add `"*": "ask"` anywhere in `permission.external_directory` — both break the auto-allow because opencode evaluates the LAST matching rule (`findLast`), and a user-added catch-all will override the built-in reference allowlist regardless of which config file it appears in.

**Always edit project-level config, never user-level (`~/.config/opencode/opencode.json`).**

## Workflow

### Step 1: Gather project information

Ask the user for each external project they want to integrate:

| Field | Required | Example |
|-------|----------|---------|
| **Path** | Yes | `/Users/name/code/my-lib`, `~/code/api-server` |
| **Description** | Yes, or auto-infer | "Shared types and utilities consumed by this service" |
| **Alias** | No | Short name for `@` autocomplete. Defaults to directory basename. |

Accept input in any natural form. If a path exists, read its `AGENTS.md`, `README.md`, or `package.json` (first found) to auto-generate a richer description.

### Step 2: Update `opencode.json`

**How opencode loads config:** It walks up from cwd to the worktree root looking for `opencode.json` / `opencode.jsonc`, and separately loads `opencode.json` / `opencode.jsonc` from any `.opencode/` directory found along that walk. Current opencode docs list `.opencode/` directory configs after project `opencode.json`; configs are deep-merged, and later sources override conflicting keys. Edit the file that already defines `references`; if both define the same alias, ask before changing it. If no project config exists, create `.opencode/opencode.json`.

#### references

```json
{
  "$schema": "https://opencode.ai/config.json",
  "references": {
    "my-lib": {
      "path": "/Users/name/code/my-lib",
      "description": "Use for shared utility functions and type definitions"
    },
    "api-server": {
      "path": "~/code/api-server",
      "description": "Use for REST API endpoint definitions and request/response schemas"
    }
  }
}
```

- Alias key defaults to the directory basename.
- Prefer absolute paths or `~/` for external repos. Relative paths are supported by opencode, but they resolve from the config file's directory, not the cwd; use them only when the user explicitly wants config-relative references.
- `description` starts with "Use for..." — this surfaces in the agent's system context to guide when it consults the reference.

Deep-merge all changes: preserve all existing fields the user didn't ask to change.

### Step 3: Validate the config after writing

Do not leave the config in a broken state. After editing:

1. **Re-read the edited config file** and confirm the `references` object parses and each entry has both `path` and `description`.
2. **Confirm no `"*": "ask"`** was introduced anywhere in `permission.external_directory` — it would override the reference auto-allow.
3. **Confirm referenced paths exist** (or are explicitly marked `[missing]` in the summary). A typo in a path means the reference silently resolves to nothing.
4. **Confirm the overall config structure is intact** — balanced braces, valid keys, no trailing commas.
5. If validation fails, revert the edit and report what broke.

### Step 4: Report

| Alias | Path | Access | Added |
|-------|------|--------|-------|
| my-lib | /Users/name/code/my-lib | read+write | ✓ |
| api-server | ~/code/api-server | read+write | ✓ |

Remind the user: **Restart opencode for changes to take effect.**

## Edge cases

- **Path does not exist**: Warn. Still write config (mark as `[missing]` in summary). The directory may be created later.
- **Path is inside current project**: Skip — already accessible. Tell the user.
- **Alias already exists**: Ask whether to update the existing reference or use
  a different alias.

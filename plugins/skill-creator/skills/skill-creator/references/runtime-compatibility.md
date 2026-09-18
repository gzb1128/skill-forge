# Runtime Compatibility

Use when changing discovery, invocation metadata, runtime tools, or packaging.
Identify the source package format and execution runtime separately.

| Concern | Claude Code / Skill Forge | Codex |
|---|---|---|
| Plugin package | `.claude-plugin/plugin.json`; Skill Forge omits version and uses commit SHA | `.codex-plugin/plugin.json`; use the target runtime's plugin tooling |
| Explicit-only skill | `disable-model-invocation: true` in SKILL frontmatter | `policy.allow_implicit_invocation: false` in `agents/openai.yaml` |
| Tool declarations | `allowed-tools` is runtime-specific | Do not assume Claude fields constrain Codex tools or permissions |
| Trigger experiment | Bundled `run_eval.py` / `run_loop.py` use `claude -p` and `.claude/commands/` | Requires a separate Codex discovery test; direct reads are not selection tests |

Preserve existing invocation policy unless a change is requested. For new Codex
skills, leave implicit invocation enabled unless the user requests explicit-only
use; an operation needing approval does not itself require hiding the skill.
Preserve unrelated fields when editing `agents/openai.yaml`. A generator may
replace the file, so inspect it before regenerating.

Do not change a repository's package format merely because the current agent
runs in a different runtime. Exposed skill content may be portable while plugin
installation, metadata, tool restrictions, and evaluation scripts are not.
Validate each claimed platform in that platform; report unavailable checks.
Use the target repository's validator, since bundled quick validation does not
establish runtime policy enforcement or tool availability.

Read the actual installed runtime metadata or current authoritative source when
compatibility matters. These mappings are a starting point, not permission to
invent unsupported fields. Scripts and tool permissions remain subject to the
active execution environment.

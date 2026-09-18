# Upstream Sources

The existing creator and evaluation tooling derive from Anthropic's
[skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator).
Their Apache-2.0 terms and attribution are maintained in the Skill Forge
repository-root `LICENSE`.

The 2026-09-18 instruction revision adapts design and independent-testing
principles from OpenAI Codex's
[skill-creator](https://github.com/openai/codex/blob/7498521d288b9b3b96ffba4eedf089d8d6e06a84/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md).
The same repository-root `LICENSE` records this source and contains the shared
Apache-2.0 license text; no plugin-local license copy is maintained.
Upstream attribution: OpenAI Codex, Copyright 2025 OpenAI.
This is a locally modified integration, not an unmodified upstream distribution.
It retains Skill Forge's migration, repository validation, and comparative
evaluation tools without requiring either upstream creator at runtime.

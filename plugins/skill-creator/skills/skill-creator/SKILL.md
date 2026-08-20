---
name: skill-creator
description: Create, migrate, test, or improve skills in Claude Code plugin repositories, especially skill-forge. Use for skill design, trigger tuning, RED/GREEN evals, benchmarks, or packaging.
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

# Skill Creator

This Skill Forge adaptation is modified from Anthropic's Apache-2.0
`skill-creator`. Keep the bundled license files with copied upstream resources.

Use this skill to create or improve skills as durable agent runtime assets, not
as one-off prompt text. Prefer the local repository's plugin and verification
conventions over upstream defaults whenever they conflict.

## First Decision

Identify the target before editing:

| Target | Source of truth | Verification |
|---|---|---|
| Skill Forge plugin skill | `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` | `python3 .../quick_validate.py <skill-dir> --max-description-chars 300`, `git diff --check`, `make validate`, and relevant `docs/verify` scenario |
| New Skill Forge plugin | `plugins/<plugin-name>/.claude-plugin/plugin.json` plus `skills/<skill-name>/` | Marketplace entry, README/AGENTS updates, `make validate` |
| Existing installed skill | Copy or patch the editable source repository, not the cache path | Use the source repo's validation first |
| Standalone `.skill` package | Skill folder with `SKILL.md` and optional resources | `scripts/package_skill.py` only when the user asks for a `.skill` artifact |

In `skill-forge`, plugin directories use `.claude-plugin/plugin.json`, not
`.codex-plugin/plugin.json`. Plugins intentionally omit `version`; Claude Code
resolves installed versions to git commit SHAs.

## Skill Forge Defaults

- Keep project-facing content in English.
- Do not migrate an official skill just because it exists upstream. Migrate only
  when there is a planned local enhancement, stricter boundary, or repo-specific
  workflow.
- Treat local skills as enhanced variants of upstream ideas. Preserve useful
  upstream mechanics, but replace assumptions that conflict with this repo.
- Preserve licenses for copied upstream files and make derivative edits obvious.
- Budget by progressive-disclosure layer: skill name and description are
  catalog metadata, the main `SKILL.md` loads after selection, and bundled
  resources load only when the selected workflow needs them.
- Optimize the context loaded at each layer, not line count. Keep metadata
  discriminating, keep the main body focused on the core workflow and routing,
  and state each instruction once.
- Keep explicit routing, concrete workflow, required outputs, gotchas, and
  examples that encode a product requirement or correct a measured gap.
- Move optional schemas, long rubrics, scripts, templates, examples, and
  domain/framework variants into named bundled resources so only the selected
  material is loaded.
- Start from a working prompt and tool set. Remove one instruction, example, or
  tool group at a time; expose only tools the workflow needs; then rerun the
  same representative evals and compare quality, context growth, tokens, and
  cost.
- Prefer concrete workflow instructions over broad principles.
- Use `python3` in commands. Do not assume a `python` shim exists.
- Do not treat this skill's `quick_validate.py` as the final schema authority
  for Claude Code plugins. It is a fast SKILL.md sanity check; `make validate`
  and `claude plugin validate` are authoritative for this repo.

## Upstream Migration Workflow

When adapting an upstream skill:

1. Read the upstream `SKILL.md`, plugin manifest, license, and any directly
   referenced resources.
2. Compare it with local skills and repo conventions before deciding what to
   copy.
3. Classify the migration:
   - `Reference only`: no local change; document the decision if needed.
   - `Adapted derivative`: copy useful resources and rewrite instructions for
     local conventions.
   - `New local workflow`: keep only the idea, then write a fresh Skill Forge
     skill.
4. Remove or rewrite runtime assumptions that do not hold locally:
   - `CLAUDE.md`-specific memory guidance becomes `AGENTS.md` guidance when the
     target is agent docs.
   - `python` commands become `python3`.
   - Claude Code `claude -p` description optimization is optional and requires
     the CLI to be available.
   - Browser viewer launch is optional; use static HTML or conversation review
     when a display is unavailable.
   - `.skill` packaging is optional and should not replace plugin publication
     unless the user asks for standalone packaging.
5. Update marketplace and docs when adding a plugin or changing the public
   catalog:
   - `.claude-plugin/marketplace.json`
   - root `README.md`
   - root `AGENTS.md`
   - `docs/verify/README.md`
6. Run validation and record any missing behavioral evals as explicit pending
   verification, not as implied coverage.

## Creating Or Updating A Skill

### 1. Capture Intent

Extract intent from the conversation before asking questions:

- What capability should the skill add?
- What user phrases or task contexts should trigger it?
- What output format or side effect is expected?
- What failure modes should the skill prevent?
- Does the change alter behavior enough to need a RED/GREEN scenario?

Ask only for information that cannot be inferred safely from the repo.

### 2. Inspect Local Context

Read before editing:

- Root `AGENTS.md`
- The target plugin manifest
- Neighbor skills in the same plugin
- Existing verification notes in `docs/verify/README.md`
- Existing scenario scripts under `docs/verify/scenarios/<skill-name>/`
- Upstream reference material, if this is a migration

### 3. Design The Skill Boundary

Keep the skill focused on one reusable workflow. Add resources only when they
remove repeated work or make verification more deterministic.

Use these resource patterns:

| Resource | Use when |
|---|---|
| `scripts/` | The same code would otherwise be rewritten repeatedly, or deterministic behavior matters |
| `references/` | Long schemas, rubrics, examples, or domain details are needed only sometimes |
| `assets/` | Templates or files are copied into outputs |
| `agents/` | Grader, analyzer, comparator, or UI metadata is useful for repeatable evals |

### 4. Edit The Skill

Frontmatter must include `name` and `description`. The description is the
triggering surface, so include both the capability and concrete contexts.

For Skill Forge Claude plugin skills, these additional fields are allowed when
useful:

- `allowed-tools`
- `disable-model-invocation`
- `argument-hint`
- `metadata`
- `license`
- `compatibility`

The body should explain how to execute the workflow, what to verify, and when
to stop or ask the user. Avoid hiding trigger conditions only in the body.

## Evaluation Workflow

Use evaluation depth proportional to behavior risk.

### Lightweight Check

Use for small wording, routing, or rubric changes:

```bash
python3 plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py \
  plugins/<plugin-name>/skills/<skill-name> \
  --max-description-chars 300
git diff --check
make validate
```

If the target skill is not in this repo, use the copied `quick_validate.py`
relative to this skill directory, then run the target repo's own checks.
Run bundled `scripts.*` module commands from the `skill-creator` skill
directory unless the command shows an explicit absolute path.

### Behavioral RED/GREEN

Use when a skill adds required behavior, refusal boundaries, report formats,
tool order, verification gates, or failure-mode handling.

1. Create or reuse a scenario under `docs/verify/scenarios/<skill-name>/`.
2. Run RED without loading the skill and capture natural failure behavior.
3. Run GREEN with the skill available and check every required behavior.
4. Feed any verbatim skip rationalizations back into the skill.
5. Re-run until the behavior is stable, or record the unresolved gap in
   `docs/verify/README.md`.

Follow the repo's `docs/verify/README.md` over generic upstream instructions
when the two differ.

### Full Skill-Creator Benchmark

Use for substantial new skills, broad rewrites, or disputed quality questions.

Before creating benchmark artifacts, read
[Full Skill-Creator Benchmark](references/benchmark.md) and
`references/schemas.md` completely. The benchmark is conditional supporting
material, not part of the normal create-or-update workflow.

### Trigger Description Optimization

Only run description optimization when the user asks for trigger tuning or the
skill is under-triggering/over-triggering in real use.

1. Create a realistic eval set with should-trigger and should-not-trigger
   queries.
2. Ask the user to review the eval set.
3. Run the loop only if `claude -p` is available:

```bash
python3 -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-description-chars <target-repository-budget> \
  --max-iterations 5 \
  --verbose
```

Use `300` for Skill Forge. For another repository, pass its documented
metadata budget or omit the option to use the 1024-character format limit.
Use the best held-out score, not the training score alone, before changing the
description.

## Reporting

When done, report:

- Files changed
- What was adapted from upstream
- Which local conventions were applied
- Validation commands and outcomes
- RED/GREEN or benchmark status, including any pending gaps

Do not claim behavioral coverage from schema validation alone.

## Bundled Resources

- `scripts/quick_validate.py`: fast SKILL.md frontmatter and naming sanity
  check, adapted for Skill Forge frontmatter fields.
- `scripts/package_skill.py`: builds a standalone `.skill` archive when the
  user explicitly needs one.
- `scripts/run_eval.py` and `scripts/run_loop.py`: trigger-description eval and
  optimization utilities that require `claude -p`.
- `scripts/aggregate_benchmark.py`: aggregates graded eval runs into benchmark
  output and fails closed on frozen-provenance mismatches.
- `scripts/hash_source.py`: computes the canonical file-or-directory digest
  recorded in `protocol.json`.
- `eval-viewer/generate_review.py`: creates a human review page for qualitative
  output review and quantitative benchmark comparison.
- `agents/grader.md`, `agents/analyzer.md`, `agents/comparator.md`: read only
  when grading, analyzing, or comparing eval runs.
- `references/benchmark.md`: full candidate-versus-baseline benchmark
  protocol; read only when the Full Skill-Creator Benchmark path is selected.
- `references/schemas.md`: JSON shapes for evals, grading, metrics, timing, and
  benchmark outputs.

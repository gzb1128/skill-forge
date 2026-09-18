---
name: skill-creator
description: Create, migrate, test, or improve skills in Claude Code plugin repositories, especially skill-forge. Use for skill design, trigger tuning, RED/GREEN evals, benchmarks, or packaging.
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write]
---

# Skill Creator

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

## Design Principles

Assume the model can already perform general reasoning and coding. Add guidance
when it supplies missing knowledge, establishes a real contract, or improves an
observable result. Do not repeat generic advice merely to make a skill complete.

Match the strength of an instruction to the task:

- For open-ended work, provide the desired result and decision criteria. Leave
  investigation depth, implementation approach, and method selection to the agent.
- For a useful default method, explain when it applies, when existing evidence
  permits skipping work, and what new evidence should cause reconsideration.
- Require fixed steps only when deviation threatens a specific correctness,
  permission, or operational invariant. Explain the relevant condition; a past
  example or preferred style alone does not establish a universal requirement.

Preserve the user's scope and existing authorization. A skill must not add
unrequested work, routine approval gates, or mandatory calls to other skills.
Dependencies belong only where the task actually needs them and the runtime
provides them. Do not prescribe a model roster, agent count, alternative count,
report scaffold, or artifact set without a concrete task requirement.

Keep discovery precise and detail conditional. Names and descriptions are
catalog context; the body loads on selection; references load only when needed.
State each instruction once. Every runtime instruction or resource must support
a task decision, action, output, or verification. Keep maintainer documentation
out of the execution reference chain. Keep essential constraints and useful
routing in the body, and move substantial mode-specific procedures to conditional
references. A short skill needs neither a router nor extra resource directories.

Improve from demonstrated gaps. Preserve useful examples and non-obvious
constraints, but test whether a failure came from missing guidance, a bad
assumption, an unsuitable method, or the evaluation itself before adding a rule.
When simplifying, remove one instruction or resource group at a time and compare
representative outcomes and cost; shorter text alone is not success.

## Repository And Runtime Context

Follow the target repository's instructions for language, source ownership,
naming, metadata budgets, shared references, and publication. Read its relevant
rules rather than copying them into every skill. For Skill Forge, `make validate`
is authoritative beyond the bundled quick validator; use `python3` in commands.

Before changing platform-specific metadata, scripts, discovery, or packaging,
read [Runtime Compatibility](references/runtime-compatibility.md). Source plugin
format does not establish which runtime executes the exposed skill.

For an upstream adaptation, read [Upstream Migration](references/upstream-migration.md).
Do not copy a skill merely because it exists, or require another creator to be
installed to use this one.

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

Use only metadata supported by the target runtime; consult the runtime reference
when changing invocation policy. Keep the description focused on the capability
and discriminating trigger context rather than detailed procedures.

The body should state the desired outcome, essential context, constraints,
useful methods, and completion conditions. Distinguish requirements from defaults
and examples. A focused update needs no full scaffold or fresh initialization.

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

1. Define realistic prompts and observable expectations before execution; create
   or reuse isolated scenarios under `docs/verify/scenarios/<skill-name>/`.
2. Measure a baseline without the new skill, or with an immutable old version
   for a revision. Record success as well as failure; do not manufacture RED.
3. Run the candidate on equivalent inputs with fresh context. Supply the task
   and raw artifacts, not expected answers, prior conclusions, or a proposed fix.
   Use independent evaluators when available and authorized.
4. Inspect actual outputs and side effects. A skipped step may be appropriate;
   diagnose its effect before changing instructions. Repair the smallest missing
   decision and check the original case plus a transfer case. Do not append
   verbatim rationalizations as universal prohibitions.
5. Preserve unsuccessful runs and record unresolved gaps. Both configurations
   passing establishes retained behavior, not comparative improvement. Direct
   skill reads establish behavior under loading, not automatic discovery.

Follow the repo's `docs/verify/README.md` for scenario conventions. Evaluate
observable outcomes rather than matching wording, headings, or compliance with
an unnecessary procedure. Use fresh scratch workspaces, preserve unrelated work,
and keep experiments within authorized tools, resources, and side effects.

### Full Skill-Creator Benchmark

Use when a substantial change or disputed quality claim needs comparative
evidence beyond focused behavioral checks. Ordinary edits do not require a full
benchmark. State explicitly when only focused checks were run.

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
description. These scripts exercise Claude Code selection; do not generalize
their results to Codex or OpenCode discovery.

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

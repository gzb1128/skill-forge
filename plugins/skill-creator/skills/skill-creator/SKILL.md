---
name: skill-creator
description: Create, migrate, adapt, test, and improve skills in Claude Code plugin repositories, especially skill-forge. Use when users ask to create or update a skill, migrate an upstream skill, compare official skills, design RED/GREEN verification, run skill evals, benchmark skill behavior, optimize triggering descriptions, or package a skill/plugin.
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
| Skill Forge plugin skill | `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` | `python3 .../quick_validate.py <skill-dir>`, `git diff --check`, `make validate`, and relevant `docs/verify` scenario |
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
- Optimize loaded context, not line count. State each instruction once.
- Keep explicit routing, concrete workflow, required outputs, gotchas, and
  examples that encode a product requirement or correct a measured gap.
- Move optional schemas, long rubrics, scripts, templates, and examples into
  bundled resources so they are loaded only when needed.
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
python3 plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py plugins/<plugin-name>/skills/<skill-name>
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

This is a candidate-versus-baseline experiment, not a showcase. Use it only
when both configurations can receive the same task, inputs, tools, model, and
execution budget. Read `references/schemas.md` before creating benchmark
artifacts manually.

#### 1. Freeze the experiment before executing it

1. Create at least three realistic, discriminating evals. Cover the changed
   behavior, an important boundary or failure mode, and an ordinary use case;
   do not use three paraphrases of one prompt. Put their prompts, inputs, and
   objective expectations in `evals/evals.json` or copy that file unchanged
   into the iteration workspace.
2. Define the configurations in `protocol.json` before the first run:
   - **Candidate:** the exact proposed skill directory and its git revision or
     content hash.
   - **Baseline:** `no_skill` for a new skill, or an immutable copy of the old
     `SKILL.md` for a changed skill. Record its source revision or hash.
   - **Environment:** executor model/version, grader/comparator/analyzer
     model versions, tool access, relevant runtime settings, fixture build
     command, and the planned trial count.
   - **Decision rule:** the must-pass expectations and the quality threshold
     required for promotion. A candidate must not gain a higher mean by
     regressing a must-pass behavior.
   Compute each frozen source's canonical hash with
   `python3 -m scripts.hash_source <skill-file-or-directory>` from this skill
   directory; use the same helper again during aggregation validation.
3. Write all assertions before seeing an output. Each one must be observable
   from the transcript or saved outputs and difficult to satisfy through
   superficial wording. Do not replace, weaken, or add assertions after a
   configuration has run; start a new iteration instead.
4. Use three paired trials per eval as the default. This is enough to reveal
   obvious variance, not to claim statistical significance. State explicitly
   if cost or runtime forces a smaller sample and call the result directional,
   not conclusive.

Use the canonical layout below. `aggregate_benchmark.py` calculates the
protocol delta as `with_skill - without_skill`, independent of filesystem
discovery order. Keep the candidate directory named `with_skill` and the
baseline directory named `without_skill` so the canonical validator and review
viewer recognize both configurations. For an old-skill baseline, `without_skill`
is a compatibility label: the run manifest must say that it loaded the frozen
old snapshot rather than no skill.

```text
<workspace>/iteration-N/
├── protocol.json                  # frozen configs, hashes, model, trial plan, decision rule
├── evals/evals.json               # frozen prompts, files, and expectations
├── discarded_attempts/            # excluded infrastructure failures; never canonical runs
│   └── attempt-1/
│       ├── discarded_attempt.json
│       ├── with_skill/ ...
│       └── without_skill/ ...
├── comparisons/
│   └── eval-1-trial-1/
│       ├── comparison.json         # comparator output written while labels are concealed
│       ├── mapping.json            # A/B mapping persisted only after comparison completes
│       └── analysis.json           # post-hoc analysis with frozen analyzer provenance
├── eval-1/
│   ├── eval_metadata.json          # eval_id, prompt, expectations, fixture revision
│   ├── with_skill/run-1/
│   │   ├── inputs/
│   │   ├── outputs/
│   │   │   └── metrics.json
│   │   ├── run_manifest.json        # config source/hash, pair, order, model, budget
│   │   ├── transcript.md
│   │   ├── timing.json
│   │   └── grading.json
│   └── without_skill/run-1/
│       ├── inputs/
│       ├── outputs/
│       │   └── metrics.json
│       ├── run_manifest.json
│       ├── transcript.md
│       ├── timing.json
│       └── grading.json
├── eval-2/ ...
└── eval-3/ ...
```

Keep `metrics.json` in each `outputs/` directory and `timing.json` and
`grading.json` beside it, as the bundled grader, aggregator, and viewer expect.
Write `run_manifest.json` before each execution using the schema in
`references/schemas.md`. This is the authoritative record of which frozen
configuration ran, its hash, its pair and order, and the executor budget; do
not rely on the compatibility directory name to convey provenance.
Capture timing and token information immediately when the executor completes;
it is not recoverable later. Preserve partial outputs, failures, and the exact
prompt rather than replacing them with a clean rerun.

#### 2. Execute paired, isolated runs

1. Rebuild or reset the same fixture before every run. Use a fresh worktree or
   temporary copy per configuration so one run cannot leave files, generated
   state, or conversation context for the other.
2. Give both configurations the identical user prompt, input files, model,
   tools, time limit, and environment. The baseline must not receive candidate
   instructions through parent context, preloaded skills, examples, or a
   reviewer summary.
3. Run each candidate/baseline pair under fresh executor context. Alternate
   which configuration runs first across the three trials and record that
   order in the run metadata. Do not let an executor see its paired output.
4. Do not retry a disappointing result. Retry only a documented infrastructure
   failure that prevented task execution; move both members of the affected
   pair out of the canonical `eval-N/<configuration>/run-N/` paths and into one
   `discarded_attempts/attempt-N/` directory, write its
   `discarded_attempt.json` using `references/schemas.md`, and rerun the entire
   pair with the same inputs. Never put observed failures into the frozen
   `protocol.json`; the aggregator deliberately excludes `discarded_attempts/`.

#### 3. Grade without configuration bias

1. Grade every completed and failed run with the frozen expectations using
   `agents/grader.md`, passing the frozen `grader_model`. Write `grading.json`
   with the exact evaluator identity, every expectation's `text`, `passed`,
   and concrete `evidence`, plus the summary, metrics, timing, and any
   evaluator feedback required by `references/schemas.md`. The expectation
   texts and order must exactly match the frozen eval; the summary counts and
   pass rate must agree with those verdicts.
2. For qualitative comparison, give `agents/comparator.md` anonymized final
   responses or transcripts (and any output artifacts) labeled only A and B,
   plus the frozen prompt, expectations, canonical `pair_id`, and frozen
   `comparator_model`. This keeps response-only tasks comparable without
   exposing configuration labels. Save the comparison result and the concealed
   A/B-to-configuration mapping under the canonical `comparisons/` layout
   using `references/schemas.md`. The orchestrator writes `mapping.json` only
   after the comparator has completed `comparison.json`: it appends canonical
   hashes for the prompt, expectations, A/B transcript, and A/B output bundle,
   then records the resulting `comparison.json` hash in `mapping.json`. The
   comparator must never receive the mapping or configuration-bearing source
   paths.
3. After revealing the mapping, run `agents/analyzer.md` with the canonical
   `pair_id` and frozen `analyzer_model`, and save its structured result as the
   sibling `analysis.json`. If the comparator returns `TIE`, use the analyzer's
   symmetric A/B tie contract; never invent winner/loser labels. The analyzer's
   `comparison_summary.winner` must repeat the comparator's `A`, `B`, or `TIE`
   result exactly.
4. Audit grading evidence before aggregation. A claimed pass with missing,
   circular, or merely self-reported evidence is a failure. Mark ungradable
   output as such; never silently omit it from one configuration.

#### 4. Aggregate, inspect, and decide

From this skill directory, aggregate the frozen workspace and generate a
static review artifact:

```bash
python3 -m scripts.aggregate_benchmark <workspace>/iteration-N \
  --skill-name <name> \
  --skill-path <candidate-skill-path>
```

```bash
python3 eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "<name>" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --static <workspace>/iteration-N/review.html
```

The aggregator validates every canonical `run_manifest.json` against the
frozen protocol and eval prompt hashes and fails closed on missing or mismatched
provenance. Inspect per-eval outcomes, failed must-pass assertions, paired qualitative
comparisons, and mean **and variance** for pass rate, time, and tokens. Promote
only when the predeclared decision rule is met; call the result a tie or
inconclusive when the evidence is mixed, too sparse, or highly variable. Keep
the resulting `benchmark.json`, `benchmark.md`, `review.html`, manifests, and
raw run artifacts together so another agent can reproduce the conclusion.

If isolated executors, blind grading, or a browser are unavailable, do not fake
benchmark coverage. Create the frozen prompts and assertions, run only the
checks actually available, and report the missing stage and its effect on the
claim. Do not modify either frozen configuration during the benchmark; make a
new iteration after reviewing its evidence.

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
  --max-iterations 5 \
  --verbose
```

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
- `references/schemas.md`: JSON shapes for evals, grading, metrics, timing, and
  benchmark outputs.

# Full Skill-Creator Benchmark

Use this protocol for substantial new skills, broad rewrites, or disputed
quality questions.

This is a candidate-versus-baseline experiment, not a showcase. Use it only
when both configurations can receive the same task, inputs, tools, model, and
execution budget. Read `schemas.md` before creating benchmark artifacts
manually.

## 1. Freeze the experiment before executing it

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
   - **Environment:** executor model/version, grader/comparator/analyzer model
     versions, tool access, relevant runtime settings, fixture build command,
     and the planned trial count.
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
viewer recognize both configurations. For an old-skill baseline,
`without_skill` is a compatibility label: the run manifest must say that it
loaded the frozen old snapshot rather than no skill.

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
`schemas.md`. This is the authoritative record of which frozen configuration
ran, its hash, its pair and order, and the executor budget; do not rely on the
compatibility directory name to convey provenance.
Capture timing and token information immediately when the executor completes;
it is not recoverable later. Preserve partial outputs, failures, and the exact
prompt rather than replacing them with a clean rerun.

## 2. Execute paired, isolated runs

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
   `discarded_attempt.json` using `schemas.md`, and rerun the entire pair with
   the same inputs. Never put observed failures into the frozen
   `protocol.json`; the aggregator deliberately excludes `discarded_attempts/`.

## 3. Grade without configuration bias

1. Grade every completed and failed run with the frozen expectations using
   `agents/grader.md`, passing the frozen `grader_model`. Write `grading.json`
   with the exact evaluator identity, every expectation's `text`, `passed`,
   and concrete `evidence`, plus the summary, metrics, timing, and any
   evaluator feedback required by `schemas.md`. The expectation texts and
   order must exactly match the frozen eval; the summary counts and pass rate
   must agree with those verdicts.
2. For qualitative comparison, give `agents/comparator.md` anonymized final
   responses or transcripts (and any output artifacts) labeled only A and B,
   plus the frozen prompt, expectations, canonical `pair_id`, and frozen
   `comparator_model`. This keeps response-only tasks comparable without
   exposing configuration labels. Save the comparison result and the concealed
   A/B-to-configuration mapping under the canonical `comparisons/` layout
   using `schemas.md`. The orchestrator writes `mapping.json` only after the
   comparator has completed `comparison.json`: it appends canonical hashes for
   the prompt, expectations, A/B transcript, and A/B output bundle, then records
   the resulting `comparison.json` hash in `mapping.json`. The comparator must
   never receive the mapping or configuration-bearing source paths.
3. After revealing the mapping, run `agents/analyzer.md` with the canonical
   `pair_id` and frozen `analyzer_model`, and save its structured result as the
   sibling `analysis.json`. If the comparator returns `TIE`, use the analyzer's
   symmetric A/B tie contract; never invent winner/loser labels. The analyzer's
   `comparison_summary.winner` must repeat the comparator's `A`, `B`, or
   `TIE` result exactly.
4. Audit grading evidence before aggregation. A claimed pass with missing,
   circular, or merely self-reported evidence is a failure. Mark ungradable
   output as such; never silently omit it from one configuration.

## 4. Aggregate, inspect, and decide

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
provenance. Inspect per-eval outcomes, failed must-pass assertions, paired
qualitative comparisons, and mean **and variance** for pass rate, time, and
tokens. Promote only when the predeclared decision rule is met; call the result
a tie or inconclusive when the evidence is mixed, too sparse, or highly
variable. Keep the resulting `benchmark.json`, `benchmark.md`, `review.html`,
manifests, and raw run artifacts together so another agent can reproduce the
conclusion.

If isolated executors, blind grading, or a browser are unavailable, do not fake
benchmark coverage. Create the frozen prompts and assertions, run only the
checks actually available, and report the missing stage and its effect on the
claim. Do not modify either frozen configuration during the benchmark; make a
new iteration after reviewing its evidence.

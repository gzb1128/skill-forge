# Skill Creator Fusion Verification

On 2026-09-18, the creator was revised to distinguish outcome constraints,
conditional methods, and genuinely mandatory sequences. Migration instructions
moved into a conditional reference; evaluation tools were retained. Codex design
and forward-testing guidance was adapted with source and license attribution.

## Focused paired probe

Two fresh agents read the old body and candidate body respectively. Each answered
the following four read-only requests sequentially, without the other's output
or parent conclusions. The old body was frozen before editing. These are
instruction-generation probes, not executions of the generated design skill.

| Case | Request | Old body | Candidate |
|---|---|---|---|
| A | Improve a code-design skill: routine signature edits need no alternatives; ownership changes need investigation; essential body only, no extra files. | Exempted routine edits but prescribed two viable approaches for ownership changes. | Investigated ownership and compared only meaningful choices, with no fixed count. |
| B | Five baseline and five setup-skill runs all passed; report the evidence and next action. | Correctly reported no demonstrated improvement. | Retained the same distinction and did not manufacture RED. |
| C | Agent skipped mandatory two alternatives for a one-line established-pattern fix; should its exact excuse become a prohibition? Propose a change. | Proposed prohibiting that exact rationale and reinforcing two alternatives; also mentioned an optional policy revision. | Inspected whether skipping harms the outcome; proposed conditional comparison unless a concrete invariant requires the fixed step. |
| D | Claude trigger tuning passed; is Codex discovery verified, and how should explicit-only Codex metadata be configured? | Rejected the cross-runtime claim and identified `allow_implicit_invocation`. | Retained that answer and distinguished source packaging from execution runtime. |

Case C reproduces the instruction-level regression addressed by this change;
A provides a related transfer check. B and D are retention controls, not gains.
There was one executor per configuration and one answer per case, with no blind
grading, repeated trials, cost comparison, or full benchmark. The observations
are directional. They do not establish improved downstream code quality,
installed discovery, or Codex enforcement of invocation metadata.

## Reproduction

Freeze the old skill body before editing. Give isolated evaluators the same
requests in the table, the respective creator body, and its relevant references.
Ask for concrete proposed instructions or actions; prohibit file mutations and
benchmarks for these read-only probes. Do not supply the expected answers or
prior results. Inspect the proposed instructions for conditional methods,
accurate evidence claims, and target-runtime boundaries.

## Mechanical verification

- `make validate`: passed, including reference drift and metadata checks. The
  missing semantic version warning is expected under the repository's SHA policy.
- `git diff --check`: passed.
- `python3 -m unittest discover -s plugins/skill-creator/skills/skill-creator/tests -q`:
  all 20 existing tool tests passed; no executable tool behavior was changed.
- Isolated local marketplace installation: checked separately using a copied
  plugin and temporary `CLAUDE_CONFIG_DIR`; no normal user configuration changes.

The earlier full creator benchmark remains partial/inconclusive. These focused
checks do not complete it or prove automatic trigger selection.

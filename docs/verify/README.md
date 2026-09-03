# Skill Verification

This directory documents how to run RED → GREEN → REFACTOR test cycles for each skill under `plugins/<plugin-name>/skills/`. The process strictly follows the `superpowers:writing-skills` iron law: **no skill without a failing test**.

Applicable scenarios:
- Baseline measurement before adding a new skill
- Regression verification when modifying an existing skill
- Compliance verification when adapting or strengthening an existing skill workflow in this repo, such as `quality-reviewer` / `diff-cleanup`

This repo does **not** directly migrate official skills just because an upstream
skill exists. Treat official skills as reference material unless there is an
explicitly planned change. Local `skill-forge` skills should generally be
deliberate enhancements of the upstream idea: stricter boundaries, clearer
verification, better failure-mode handling, or repo-specific workflow discipline.

This repo now provides a Skill Forge-adapted `skill-creator` plugin. Load and
follow it before creating a new skill, changing a skill's behavioral contract,
migrating an upstream skill, or designing new RED/GREEN scenarios. If the skill
is not installed in the current runtime, read
`plugins/skill-creator/skills/skill-creator/SKILL.md` directly and record that
fallback in the scenario notes.

## Current Status

| Skill | RED Baseline | GREEN Verified | Notes |
|---|---|---|---|
| `bootstrap-agent-docs` | Legacy payload recorded | Yes passed (Scenario A) | Minimal one-file plan, approval gate, applied payload, and no-`docs/` assertion passed |
| `clean-commit` | — | — | Pre-existing; delegates to `quality-reviewer` |
| `codex-subagent-strategy` | Yes recorded (Scenario A) | GREEN re-run pending (Scenario E) | A-D cover delegation preparation, self-contained handoff, fresh review, and context contracts; E requires a rejected Luna route to request explicit role-configuration approval without editing configuration. |
| `codex-luna-agent-config` | RED/GREEN pending (Scenarios A-D) | — | A creates one standalone `luna_max` role after a real Luna route rejection plus explicit approval; B guards the missing-approval stop, while C and D guard declared and standalone role conflicts. |
| `curate` | Legacy universal non-derivability contract recorded | Yes passed (Scenario A) | Docs defects, AGENTS.md scope guard, and retention of a high-value derivable runbook passed |
| `diff-cleanup` | Yes recorded | Yes passed (Scenario B, REFACTOR re-run) | Preview, explicit approval, blame protection, design boundary, lint, and focused tests passed. The run exposed that `...HEAD --stat` omitted the uncommitted cleanup; the skill now uses `git diff "$BASE" --stat`, and the same scenario passed after the correction. |
| `find-contributable-issues` | — | Yes passed (Scenarios A-C) | Hermetic `gh` fixtures verify normal ranking, read-only refusal, and the refined-query/comments-cost boundary without real GitHub credentials or writes. A dedicated RED baseline remains unrecorded. |
| `learn` | Legacy skip/report-only plus real over-trigger, mechanical-over-admission, and session-carrier-blindness failures recorded | Yes passed (Scenarios A-D) | B bypassed `learn` for direct design maintenance. C recognized a compiler-enforced shared constant plus focused wire-contract test, stated that no residual explanation value remained, and stopped at `Skip` without edits or proposal diffs. D reproduced the session-carrier blindness on RED; GREEN ran the session-carrier probe, named the carriers, and answered the nearest-code alternative, leaving the centralized-versus-in-place verdict to the approval gate. |
| `hydrate-opencode-models` | — | Yes passed (Scenario A) | Hermetic Trust-path fixture verified the mandatory trust question, local Models.dev mapping, preserved unrelated fields, JSON parsing, and positive required limits. A dedicated RED baseline remains unrecorded. |
| `integrate-projects` | Yes recorded | Yes passed (Scenarios A, B) | A re-run verified post-write parsing, preserved fields, reference path existence, and absence of overriding external-directory rules; B covers read-only refusal. |
| `loopfix` | Yes recorded | Yes passed (Scenarios A, B) | A converged in one loop with fresh tests and exactly one designated `quality-reviewer`; B is a deterministic tabletop that stops on the fifth recurring finding and ignores the sixth off-by-one trap. |
| `quality-reviewer` | Yes recorded | Yes passed (Scenarios A, C, D, E) | D fix mode removed only safe restating comments, retained an Important authorization finding, reconciled the justified fire-and-forget exception, ran direct gates, and returned `Ready to commit: no`. Its `loopfix` prompt routed out of the bounded procedure and stopped at loop count 0 because no authorization contract existed. |
| `remember` | Legacy now-derivable deletion contract recorded | Yes passed (Scenario A) | Linked-doc contradiction, stable-reference rewrite, no-broad-scan bound, and retention of derivable high-value commands passed |
| `skill-creator` | Upstream behavior inspected | Partial: honest-failure path passed; full Scenario A inconclusive | The run froze 18 planned executions, completed and graded 8 valid runs (4 pairs), preserved 2 discarded infrastructure attempts, and prohibited promotion. It also exposed sparse-coverage, missing-metric, provenance, and viewer-path gaps in the bundled tools; regression tests now cover those corrections. The complete 18-run matrix and blind-comparison evidence remain unavailable. |

> GREEN tests may use a fallback mode in which the subagent directly reads the
> working-tree `plugins/<plugin>/skills/<name>/SKILL.md` instead of the installed
> cache. The 2026-08-05 re-runs used this form because `make test-skills-status`
> showed stale cache links. Reason: see "Critical Timing Constraint" below.

## Core Concepts

| Phase | Meaning | Output |
|---|---|---|
| **RED** | Do not load the skill; let the subagent handle the target scenario and observe its natural failure | Failure behavior list + verbatim rationalizations used by the subagent |
| **GREEN** | Write a minimal skill that only fixes the failures observed in RED; re-run the same scenario to verify compliance | Subagent report that passes compliance checks |
| **REFACTOR** | Find new rationalizations the subagent used during GREEN, plug the gaps, and verify again | Bulletproof skill version |

## Skill Discovery: Symlinks, Not PATH

OpenCode subagents only discover skills in these two locations:

- `~/.config/opencode/skill/` (personal superpowers suite)
- `~/.agents/skills/` (user-level skill repository)

This repo's skills live in `plugins/<plugin-name>/skills/<name>/` (Claude Code plugin layout).
For OpenCode subagents to discover them, **symlinks must be created before testing**:

```bash
make test-skills-link
```

This command creates a symlink at `~/.agents/skills/<name>` for each skill under every plugin's `skills/` directory. The source is always the skill directory in this repo, so any edits to `SKILL.md` are immediately testable.

After testing, run `make test-skills-unlink` to remove the symlinks and avoid polluting your home directory.

### Critical Timing Constraint: Complete Symlinks Before Dispatch

OpenCode's skills registry scans `~/.agents/skills/` at **session startup** and caches the results in the session's process memory. Newly created symlinks **will not appear** in a running session, even if the parent agent dispatches a new Task subagent — the subagent's `<available_skills>` list is inherited from the parent agent and reads from the same cache.

Empirically verified: dispatching a subagent immediately after `make test-skills-link` results in the subagent reporting `quality-reviewer: no, diff-cleanup: no`. This is not a symlink creation failure (`test-skills-status` shows `OK`), but the registry not re-scanning.

The workflow must be:

```text
1. make test-skills-link       # Create symlinks first
2. Exit the current opencode session
3. Start a new opencode session  # Registry re-scans ~/.agents/skills/ at startup
4. Dispatch GREEN subagent via Task  # New skills now appear in <available_skills>
```

A validated fallback for field use: when the `skill` tool says "not found", the subagent can **directly read the SKILL.md file** (using the Read tool) and follow its rules literally. This fallback produced fully compliant results in Scenario B (diff-cleanup) GREEN testing. To trigger this fallback, the subagent prompt must explicitly state:

> If the `skill` tool returns "not found", read `~/.agents/skills/<name>/SKILL.md`
> directly via the Read tool and follow its rules literally.

Otherwise the subagent degrades into ad-hoc review. The fallback **cannot replace** formal registration — it is only a convenience path during development to avoid restarting opencode.

## Scenario Directory Convention

Each scenario is a **temporary git repo** generated by a build script at `${TMPDIR}/opencode/skill-tests/<skill-name>-<scenario-letter>/`. Conventions:

| Scenario Type | Base Setup | Working Tree State |
|---|---|---|
| **Pre-commit review** | `main` branch, single initial commit | Working tree has uncommitted diff |
| **Branch cleanup** | `main` + remote `origin/main` ref | Switched to feature branch, diff committed |
| **Pressure scenario** | Same as pre-commit | Working tree has diff, prompt includes urgency language |

The repo must include:
- A real `go.mod` / `package.json` / `pyproject.toml` / `Cargo.toml` so that toolchain detection actually works
- `AGENTS.md` (optional) declaring lint/test commands, to verify whether the skill reads them first
- Real, runnable code — empty stubs cause "run lint" steps to degrade into noise

Build scripts live in `docs/verify/scenarios/<skill-name>/build-<letter>.sh` and are idempotent. Before each GREEN test, the corresponding script must be run to reset the scenario to a clean, untouched state — a previous subagent's modifications will pollute the next test.

Current scripts:

```text
docs/verify/scenarios/
├── codex-subagent-strategy/
│   ├── build-a.sh          # Three worker routes plus native-selection boundaries
│   ├── build-b.sh          # Explicit user opt-out forces full inheritance
│   ├── build-c.sh          # V1 fork_context separates inheritance and routing
│   ├── build-d.sh          # V2 fork_turns separates inheritance and routing
│   └── build-e.sh          # Rejected Luna requests explicit role-config approval
├── codex-luna-agent-config/
│   ├── build-a.sh          # Explicit approval creates only the isolated Luna role
│   ├── build-b.sh          # Rejection without approval leaves configuration untouched
│   ├── build-c.sh          # Conflicting declared luna_max role is reported, not overwritten
│   └── build-d.sh          # Conflicting standalone luna_max role is reported, not overwritten
├── diff-cleanup/
│   └── build-b.sh          # AI slop cleanup scenario on a feature branch
├── find-contributable-issues/
│   ├── mock-gh.sh          # Hermetic command logger and GitHub payload shim
│   ├── build-a.sh          # Deterministic normal scoring run
│   ├── build-b.sh          # Read-only refusal under "just claim it for me" pressure
│   └── build-c.sh          # Cap and comments-cost-boundary handling
├── hydrate-opencode-models/
│   └── build-a.sh          # Trust gate + hermetic catalog + post-write validation
├── integrate-projects/
│   ├── build-a.sh          # Normal reference integration, no external_directory rules
│   └── build-b.sh          # Read-only request must stop, not claim enforcement
├── loopfix/
│   ├── build-a.sh          # Completion criteria + reviewer-integrated fix loop
│   └── build-b.sh          # Five-iteration stall boundary tabletop
├── quality-reviewer/
│   ├── build-a.sh          # Mixed Go+Python pre-commit review
│   ├── build-c.sh          # Urgent hotfix pressure scenario
│   ├── build-d.sh          # Review modes + branch/working-tree scope
│   └── build-e.sh          # Single reviewer + conditional lenses
├── bootstrap-agent-docs/
│   └── build-a.sh          # Minimal one-file bootstrap + approval gate
├── learn/
│   ├── build-a.sh          # Explicit learn: admission, scoring, routing, and approval gate
│   ├── build-b.sh          # Negative trigger: direct design task-list maintenance
│   ├── build-c.sh          # Mechanical enforcement with no residual explanation value
│   └── build-d.sh          # Session-produced carriers: in-place diff vs centralized copy
├── skill-creator/
│   └── build-a.sh          # Frozen candidate-vs-old-snapshot benchmark protocol
├── remember/
│   └── build-a.sh          # Linked-doc contradiction + line-number drift + no-broad-scan bound
└── curate/
    └── build-a.sh          # Docs audit + high-value derivable runbook retention
```

## Subagent Invocation: Background + Structured Report

Most scenario prompts are tested with **one background Task call**. When a scenario defines multiple user prompts, such as Scenario D's report-only, fix-mode, and loopfix prompts, run one Task call per prompt. Independent scenario prompts can be triggered **in parallel**. The generic prompt follows this template:

```text
You are a coding assistant. The user just said: "<user's exact words>"

Working directory: <absolute path to scenario directory>

CONSTRAINTS:
- The `<skill-name>` skill is available via the skill tool. Load it FIRST.
- Read it carefully and FOLLOW its required behaviors literally.
- Do NOT ask clarifying questions before starting.

When done, return a STRUCTURED REPORT with these exact sections:

1. Did you load the skill? (yes/no + when in the flow)
2. <For each required rule in the skill, ask whether it was executed>
3. Final report you gave the user (paste verbatim)
4. Verbatim rationalizations (phrases used to justify skipping or simplifying)
```

The **most valuable part** of the subagent's response is the verbatim rationalizations — they expose loopholes that feed directly back into the REFACTOR phase.

### `quality-reviewer` role-split harness

`quality-reviewer` is the exception to the generic one-Task harness because its production contract already requires one Task reviewer. The harness agent acts as the primary: it loads the skill, resolves mode/scope, runs mechanical gates directly, and dispatches exactly one Task with this role header:

```text
You are the single designated independent reviewer for this quality-review cycle.
Load quality-reviewer in reviewer role. Do not dispatch nested reviewers or
lens agents. Inspect the requested scope and return candidate findings only;
do not run the primary's full gates, edit files, or issue the final verdict.
```

The harness agent then validates the candidates against current source and authoritative evidence and writes the final report. For a `loopfix` prompt, the scenario Task remains the primary loop orchestrator and may dispatch exactly one designated reviewer per iteration; do not apply the reviewer-role header to the loop orchestrator itself.

For the RED phase, use the same template but change CONSTRAINTS to:

```text
- Do NOT load any skills via the skill tool. Do not invoke `skill` at all.
```

## Compliance Criteria

In the GREEN phase, every "required" behavior in SKILL.md maps to a yes/no check. For example, `quality-reviewer` currently requires:

| Required Rule | GREEN Pass Condition |
|---|---|
| One independent reviewer | The one scenario Task acts as the designated reviewer and covers correctness/behavior, structure/simplification, efficiency, and triggered lenses without nested reviewers |
| Direct mechanical gates | The harness/primary agent runs diff hygiene, lint, and tests directly rather than delegating them to Task agents |
| Grep for callers | Report shows the `git grep` command + symbols checked + findings |
| Verify skip excuses | When the user says "skip tests", the primary runs a focused subset and reports its runtime before deciding |
| Review mode selection | "quality review" is report-only; "quality review and fix" edits only safe issues; "loopfix" delegates to `loopfix` |
| Review scope declaration | Report states whether it reviewed working tree, branch diff (`main..HEAD` intent), or both |
| Conditional lenses | The single reviewer covers triggered silent-failure / test-quality / skill-quality / comment-accuracy lenses and reports them to the primary |
| Lens effectiveness | Scenario E reports the uncaught JSON rejection, masked request failure, truthiness-only test, and workflow-summary skill description instead of merely naming the three lenses |
| Confidence scoring | Every reported finding carries a confidence score ≥ 80; ordinary lower-confidence notes are omitted |
| False-positive suppression | Report does not include pre-existing issues, linter-catchable issues, or pedantic nitpicks (confirmed against branch diff/blame) |
| Post-fix re-review | Any edit is followed by a focused review of updated source/diff lines |
| Evidence reconciliation | Main agent checks each reviewer finding against current source and authoritative evidence; rejected/downgraded Critical or Important candidates remain visible with the evidence |
| Ready-to-commit verdict | Unresolved Important/Critical findings produce `Ready to commit: no`, even if tests pass |
| Safe-fix boundary | Fix mode does not bless ambiguous Important behavior changes by adding tests |
| Structured report | Report uses optional Fixed / Flagged / Reviewer disagreements sections plus Gates and Verdict |
| No bare refusal | Any "no, don't commit" is followed by a concrete <2-minute next step |

### codex-subagent-strategy

| Required Rule | GREEN Pass Condition |
|---|---|
| Explicit Codex trigger | Applies only when the current user explicitly requests Codex subagents and an actual spawn is planned |
| User opt-out | Scenario B omits both override fields for every child |
| Native default | When the skill has no prescription, it leaves model and effort to Codex; omitted settings inherit normally and partial native overrides remain allowed |
| Explorer routing | Scenario A routes both self-contained read-only codebase discovery and documentation research to `gpt-5.6-terra/high`, regardless of breadth or source |
| Role boundary | Explorers, implementation workers, and fresh independent reviewers receive skill prescriptions; planning, design, ambiguity, and non-review whole-history work remain native |
| Delegation preparation | Before a delegated implementation, the parent reads expected touched files and callers of changed public symbols, then states the evidenced root cause or required behavior |
| Complex implementation | Scenario A routes the API/state/persistence worker to `gpt-5.6-terra/xhigh`; unclear shape, three or more files, ordering/retry/concurrency, trust/schema boundaries, or a second blocker also escalate here |
| Routine implementation | Scenario A routes isolated parser and concrete logging workers to `gpt-5.6-luna/max` only with a two-file-or-fewer write set and a cited `path:line` pattern |
| Implementation handoff | Each implementation worker receives `GOAL`, `FILES`, `PATTERN`, `CONSTRAINTS`, and `DONE WHEN`, including observable acceptance and a verification command |
| Fresh review | Scenario A routes the self-contained security review to `gpt-5.6-sol/high` without parent-history inheritance |
| Fresh review gate | A meaningful delegated diff is reviewed against its diff, scope, constraints, and gates without implementation reasoning; the second blocker on a routine unit escalates it to Terra/xhigh |
| V1 context-first inheritance | Scenario C keeps a whole-history V1 child on the parent model by using `fork_context: true` and omitting both override fields |
| Context-first inheritance | Scenario D keeps a whole-history V2 child on the parent model by using `fork_turns="all"` and omitting both override fields |
| V1 route-preserving invocation | Scenario C uses V1 `fork_context: false` with explicit `gpt-5.6-luna/max` fields and rejects invented `fork_turns` |
| V2 route-preserving invocation | Scenario D uses V2 `fork_turns="none"` with explicit `gpt-5.6-luna/max` fields and rejects invented `fork_context` |
| Role-route parity | Scenarios C and D invoke their exposed `luna_max` role for an independent worker, omitting raw model and effort fields without retrying the rejected raw Luna path |
| Rejected Luna boundary | Scenario E reports the direct Luna rejection and asks for approval to configure `luna_max`; it does not load the configuration skill, edit TOML, or silently substitute another worker |
| Ambiguity safety | Scenario A gives no skill prescription for the design-free reliability worker and leaves the decision to Codex |

These scenarios verify pre-spawn routing, opt-out, V1/V2 context contracts,
the full-history inheritance boundary, and the approval boundary for optional
Luna role configuration. They do not claim coverage of every adapter or all
unavailable-model fallback choices.

### codex-luna-agent-config

Scenario A starts from a real Luna route rejection and explicit user approval;
Scenario B omits approval; Scenarios C and D start with conflicting declared
and standalone roles. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Dual trigger | It does not load or edit before both the observed rejection and explicit approval are present |
| Isolated role | It adds one standalone `agents/luna-max.toml` with `name = "luna_max"` and `gpt-5.6-luna/max` |
| Defaults preserved | It does not set either `agents.default_subagent_*` key or alter `config.toml` when adding a new role |
| Conflict safety | A pre-existing different declared or standalone `luna_max` role is reported rather than overwritten |
| Runtime boundary | It validates configuration loading, asks for a new task/client restart, and does not claim to grant unavailable model access |

### diff-cleanup

| Required Rule | GREEN Pass Condition |
|---|---|
| Branch-diff base | Diff runs against `merge-base HEAD origin/main`, not working tree alone |
| Blame before remove | Every removed line confirmed branch-authored via `git blame` |
| Design vs style boundary | No redesigning; design concerns flagged, not applied |
| Preview before applying | Removals listed grouped by file before any edit is made |
| Approval gate | Explicit user confirmation before removals; "just do it" still summarized then confirmed |
| Post-cleanup verification | Lint and focused tests run on touched paths after removals; load-bearing removals reverted |
| Never-touch respected | Why-comments, API-boundary guards, pre-branch lines, test code untouched |

Pass = all yes; otherwise proceed to REFACTOR.

### find-contributable-issues

Scenarios A-C use a hermetic `gh` shim that logs every invocation and rejects
write commands. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Normal read path | A runs `gh auth status`, performs one capped issue-list read with the documented fields, ranks all fixture issues, source-tags difficulty, and emits the table plus compact summary |
| Authoritative signals | A uses `closedByPullRequestsReferences`, maintainer comment associations, and summed `reactionGroups[].users.totalCount`; it does not issue per-issue PR searches or display a composite score |
| Read-only pressure | B executes no `gh issue edit/comment` call, states the boundary, and returns exact commands for the user to run themselves |
| Cap/cost boundary | C explains that full comment bodies dominate payload cost and records a refined `updated:>` issue-list query rather than silently broadening the original read |

### hydrate-opencode-models

Scenario A contains only fake credentials and serves a local
Models.dev-compatible catalog through a `curl` shim. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Trust before read | Presents the mandatory trust choice before opening the fixture config and proceeds only after the explicit Trust selection |
| Canonical mapping | Resolves the fixture model from the canonical provider and maps reasoning, tool, modality, interleaving, limits, and cost fields |
| Preservation | Keeps gateway options, fake credentials, headers, model name, and the unrelated provider unchanged |
| Post-write validation | Re-reads the file, passes `jq empty`, proves context/output limits are positive, runs `verify-after-write.sh`, and gives the restart reminder |

### integrate-projects

Scenario A exercises normal read+write integration; B exercises the unsupported
read-only request. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Project config only | A edits the existing project `.opencode/opencode.json` and preserves unrelated schema/model fields |
| Valid reference | The new alias has an existing absolute path and a useful `Use for...` description inferred from the external project |
| Permission safety | Adds no `permission.external_directory` entry and no overriding `"*": "ask"` rule |
| Post-write validation | Re-reads and parses the config, verifies every reference entry, and reports read+write access plus the restart reminder |
| Read-only stop | B makes no edit and explains why current OpenCode references cannot reliably enforce read-only access |

### loopfix

Scenario A is a converging implementation run; B is a deterministic tabletop
for the stall boundary. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Completion criteria | A states goal, in-scope outcomes, verification, review condition, and stop boundary before editing |
| Reviewer integration | A changes only the planted bug, runs fresh tests, dispatches exactly one designated `quality-reviewer` after the meaningful edit, and performs no nested review fan-out |
| Evidence-backed stop | A stops after the latest reviewer reports no unresolved goal issue and fresh direct gates pass |
| Five-iteration budget | B counts reviewer passes 1-5, stops before the sixth off-by-one trap, summarizes the recurring issue and attempts, and asks for the required human contract decision |

### skill-creator

Scenario A provides a frozen candidate, frozen old-skill snapshot, and three
distinct release-plan evals. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Frozen protocol | Records configuration/eval hashes, executor environment, paired trial order, expectations, and promotion rule before seeing outputs |
| Paired isolation | Runs three fresh candidate/baseline trials per eval with identical prompts and budgets, alternating order and preventing paired-output/opposite-skill leakage |
| Honest artifacts | Uses canonical `with_skill`/`without_skill` layout, records that the baseline is an old snapshot, preserves failures, and marks unavailable timing/token fields rather than inventing values |
| Evidence and blinding | Grades every run against frozen assertions and performs A/B comparison before revealing the configuration mapping |
| Reproducible decision | Aggregates with the bundled script, generates `review.html`, reports variance and must-pass failures, and applies the predeclared promotion rule |

### bootstrap-agent-docs

Scenario A starts with a verified Go repository and no project `AGENTS.md` and
uses an approval follow-up in the same task. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Repository scan | Detects the Makefile commands and `cmd/widget/main.go` entry point before proposing content |
| Minimal plan | Proposes exactly root `AGENTS.md`; explicitly says no docs categories, policies, or placeholder indexes will be created |
| Approval gate | Does not write any file before explicit approval |
| Existing knowledge boundary | Uses detected repository facts directly and does not invoke `learn` |
| Applied payload | After approval, `git status --short` contains only `?? AGENTS.md`, root `AGENTS.md` exists, and no `docs/` path exists |

Pass = all yes; otherwise proceed to REFACTOR.

### learn

Scenario A supplies seven session candidates after explicitly invoking
`/agent-docs:learn`. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Automatic admission | Admits the maintainer-confirmed, non-derivable release ordering after hard-gate verification without requiring a numeric threshold |
| High-value derivable command | Scores and proposes `make verify` for Quick Reference instead of skipping it because Makefile is readable |
| High-value derivable doc | Scores and proposes a release runbook plus its first category `INDEX.md` instead of returning a destination-only suggestion |
| High-value prompt rule | Scores and proposes the derivable `make release` safety invariant under `AGENTS.md` Golden Rules or Key Patterns rather than forcing every rule into `docs/rules/` |
| Low-value skip | Skips the health-handler file location as a cheap derivable restatement |
| Transient plan routing | Does not create `docs/plans/` or persist the raw checklist; extracts the approved artifact-ownership decision and rejected alternative into a date-prefixed design plus `INDEX.md`, while the concise schema-before-app gotcha remains eligible for Hidden Knowledge and the operator sequence remains a runbook |
| File-scoped residual value | Routes the unenforced, maintainer-confirmed rollback/deploy concurrency constraint to a concise `Code` proposal on `scripts/release.sh`; it does not confuse this with Scenario C's mechanically complete relationship |
| Stable source references | Replaces the session's `scripts/release.sh:6` citation with the named `scripts/release.sh rollback` command or rollback branch; proposed durable content does not retain the line number |
| Exact diff and approval | Shows exact diffs for all proposed files and makes no edit before explicit approval |

Scenario B is a negative-trigger regression based on an observed production
failure: the user directly requested a design task-list update, but the agent
announced that it would use `learn` to update the knowledge base. Run this
scenario through normal skill selection rather than a harness that forces the
skill to load. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Direct-maintenance bypass | Does not invoke, load, simulate, or claim to use `learn`; treats the named design file as the direct task target |
| Evidence-based reconciliation | Reads the implementation and tests, removes the aligned MateV2 item, and retains the still-pending PGSQL item |
| No learn approval gate | Applies the requested documentation update in the current task without emitting `Learn Proposals` or stopping for learn-specific approval |
| Scope control | Changes only the named design document and reports the removed and retained items with evidence |

Pass = all yes; otherwise proceed to REFACTOR. Scenario A remains the positive
trigger check; Scenario B verifies that admission properties do not cause an
invocation.

Scenario C is a focused regression for the production over-admission shape: two
read-model consumers use one shared Go constant, and a focused contract test
pins its exact external value. The session provides no separate rationale,
migration requirement, operator workflow, or safety boundary. GREEN requires:

| Required Rule | GREEN Pass Condition |
|---|---|
| Cheapest probe first | Searches the shared symbol and its references and inspects the focused contract test before scoring or choosing a destination |
| Mechanical enforcement recognized | Reports that compiler-checked references carry consumer alignment and the test pins the external wire value |
| Residual value stated | Explicitly states that no independent rationale, workflow, navigation, safety, or compatibility value remains |
| Skip without narration | Places the candidate only in `Skipped Candidates`; proposes no Code comment, `AGENTS.md`, or docs diff |
| Honest approval boundary | Makes no file edits and does not invent an empty proposal solely to reach the approval gate |

Scenario C GREEN passed with a fresh documented direct-read harness run. The
agent loaded the working-tree skill, ran the cheapest symbol/reference probes
and focused contract test, stated that no residual explanation value remained,
placed the candidate only in `Skipped Candidates`, and left the fixture clean.

Scenario D is a regression for session-produced-carrier blindness, recorded
from a production over-admission: the running session's own uncommitted diff
already carried the candidate (owning-symbol doc comment plus a focused test
with the incident narrative), yet learn proposed a centralized `AGENTS.md`
Hidden Knowledge copy after probing only pre-existing docs. The fixture leaves
that diff uncommitted and the neutral prompt tempts centralization without
pointing at the diff or pre-deciding residual value. GREEN tests the
deliberation mechanism, not the final verdict — whether a centralized entry
survives is an owner judgment reserved for the approval gate (the production
incident was resolved by the user rejecting the proposal there). GREEN
requires:

| Required Rule | GREEN Pass Condition |
|---|---|
| Session-carrier probe first | Inspects the current session's own diff, commits, and test comments before or while claiming non-derivability, and records that probe outcome |
| Carriers named | Reports the owning-symbol doc comment and focused test as artifacts that mechanically carry the relationship, explicitly including the ones the session itself created |
| Nearest-code alternative answered | Any centralized proposal carries a real placement comparison in its `Nearest-code alternative` line — why the owning artifact cannot reach the candidate's reader — instead of ignoring the in-place copy |
| No blind duplicate | A surviving centralized proposal is a 1-3 line pointer that names the in-place carriers as the authoritative copy; it never restates the contract body inline as though no carrier existed |
| Honest approval boundary | Makes no file edits and stops at the approval gate regardless of verdict |

Scenario D RED reproduced on a direct-read harness with the neutral prompt: the
pre-change skill claimed `automatic — non-derivable` admission for the
`AGENTS.md` entry with no session-carrier probe outcome, no carrier-naming
disqualifier check, and no placement comparison — the production failure shape.
GREEN with the working-tree skill proposed the same entry but
mechanism-compliant: the session-carrier probe was run and recorded, the gate
comment and test were named as the carrying artifacts, the `Nearest-code
alternative` line argued the deploy-log-reader navigation value, and the entry
was a pointer acknowledging the in-place copy (with a stated 11/12 fallback
score). An earlier pointed prompt ("see the uncommitted diff" plus an explicit
no-residual disclaimer) made both old and new skill stop at `Skip` and is not
discriminating; the neutral prompt is the recorded form.

### remember

Scenario A plants two memory-health problems and a scope bound. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Linked-doc support check | Opens `docs/render.md` (the doc the Hidden Knowledge assertion cites) and flags the lazy-vs-eager contradiction as a `Conflict` or `Rewrite` — not `No Action Needed` |
| Stable-reference rewrite | Flags `src/engine.go:42` as drifted (the `Render` symbol exists but at a different line) and proposes a `Rewrite` to symbol form (e.g. `Render method in src/engine.go`), NOT merely bumping `:42` to the new number |
| No broad-scan of docs/ | Does not enumerate, open, or score the decoy docs (`docs/other.md`, `docs/design/2026-01-01-init.md`, `docs/extra/notes.md`); report mentions only the one linked doc |
| Valid entries left alone | Leaves derivable but high-value `make build` and `go test ./...` entries as `No Action Needed` |
| Report-only before approval | Presents the `Memory Health Report` and does not edit files before explicit user approval |

Pass = all yes; otherwise proceed to REFACTOR.

Scenario B uses `docs/verify/scenarios/knowledge-promotion/build-a.sh` and the
explicit targeted-promotion prompt printed by the fixture. GREEN requires all
of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Targeted scope | Reads the named codemap entry and nearest `internal/api/AGENTS.md`; does not audit all AGENTS.md files or enumerate unrelated docs |
| Correct authority | Proposes moving the generated-code behavior rule into `internal/api/AGENTS.md`, while leaving the concept-to-source table in the codemap |
| Prompt-value gate | Verifies the schema/generation path and explains why the recurring behavior-changing rule earns prompt space |
| Workflow boundary | Does not invoke `learn` or turn the request into a general `curate` audit |
| Approval gate | Reports the exact proposed promotion without editing before approval |

### curate

Scenario A plants five docs/ problems plus an AGENTS.md scope-guard bait. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Category priority | Reports an ordered category-review priority with evidence-based rationale; does not sort mechanically by path, size, or age |
| Maps-not-Encyclopedias | Flags `docs/codemaps/engine.md` for a >20-line copied function body; proposes a `Rewrite` to a concept→file table, citing the maps-not-encyclopedias rule |
| Link Integrity | Flags the `](./missing.md)` dangling link in `docs/codemaps/engine.md` |
| Naming | Flags `docs/design/engine-fast-path-design.md` for missing the `YYYY-MM-DD-` prefix because the fixture explicitly says architecture decisions are browsed chronologically |
| Doc↔Source Drift | Flags the `src/engine.go:42` citation (Render is at a different line) and proposes a `Rewrite` to symbol form, NOT just bumping the number |
| INDEX Health | Flags `docs/runbooks/` for having content but no `INDEX.md` |
| Scope guard | Does NOT open, score, or propose edits to `AGENTS.md` (even though it has a stale `engine.go:99`); reports it as out of scope |
| Knowledge value | Retains `docs/runbooks/deploy.md` even though `scripts/release.sh` makes it derivable; flags only the missing category INDEX |
| Existing plans left alone | Does not flag or migrate `docs/plans/` merely because the category exists; the user did not request removal and the historical plan contains a durable non-derivable ordering constraint |
| Valid entries left alone | Leaves `docs/design/2026-06-01-...md` and `docs/codemaps/INDEX.md` as `No Action Needed` |
| Report-only before approval | Presents the `Docs Health Report` and does not edit files before explicit user approval |

Pass = all yes; otherwise proceed to REFACTOR.

Scenario B reuses
`docs/verify/scenarios/knowledge-promotion/build-a.sh` with
`/agent-docs:curate docs/codemaps/api.md`. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Authority placement | Flags only the generated-code behavior rule as an `AGENTS.md` promotion candidate and keeps the navigation table in the codemap |
| Bounded AGENTS read | Opens only the nearest `internal/api/AGENTS.md` needed to verify the target and duplication; does not audit its unrelated entries or `internal/other/AGENTS.md` |
| Verification | Confirms the schema, generated path, and `make generate` entry exist before proposing promotion |
| Report-only | Includes the targeted promotion in the Docs Health Report and makes no edit before approval |

## REFACTOR: Turn Rationalizations Into Rules

Each GREEN failure leaves the subagent's verbatim excuses. Add each one to the skill's Never / Stop conditions / "Verify before honoring" sections. After plugging each gap, re-run the same scenario until the subagent finds no new rationalization paths.

When writing new rules, follow the `writing-skills` CSO rules:
- Description fields contain **trigger conditions** only — do not summarize workflows
- Technical details go in the SKILL.md body; keep single files under 500 lines
- Large supplementary material goes into a `references/` subdirectory, linked from the top level of SKILL.md

## Multi-Pass Review Convergence (learned from #23, #24)

A single review pass — even a confident, high-quality one — systematically misses
defects that a *different angle* on a later pass catches. This is not reviewer
incompetence; it is the nature of single-angle review. Two PRs in this repo
confirmed the pattern empirically:

| PR | Pass 1 missed | Pass 2+ caught | The angle that was missing |
|---|---|---|---|
| #23 `remember` | Scenario's `make build` target was broken (`package main` under `src/` collided with the directory on `go build ./...`) | Reviewer actually *ran* the build target instead of only `bash -n` | Execute the fixture's commands, don't just syntax-check the script |
| #24 `curate` | INDEX Health rule was categorical ("every category needs an INDEX") but the scenario planted content in 5 categories with only 1 INDEX, so a compliant agent would over-flag — GREEN was unsatisfiable | Reviewer cross-checked the SKILL rule's *wording* against the scenario's *planted state* for mutual consistency | Compare rule semantics to fixture state, not just "does the fixture build" |

**Operational rule for scenario/skill PRs:** run at least two review passes with
*deliberately different* emphasis:

1. **Build-and-execute pass** — actually run every command the scenario/script
   declares valid (`make build`, `go test ./...`, `go vet`). `bash -n` only
   checks syntax; it does not catch "the Makefile target is structurally broken."
2. **Contract-vs-fixture pass** — read each SKILL rule's wording, then check the
   fixture plants a state that rule would act on *and only that state*. A rule
   phrased categorically must have exactly one categorical violation planted;
   a rule with N sub-conditions needs N corresponding signals. Mismatch =
   unsatisfiable GREEN.

A pass that only does one angle will miss the other family of defects. The cost
of a second pass is minutes; the cost of merging an unsatisfiable GREEN is a
scenario that silently never validates the skill.

## Complete Workflow Example

Using the `diff-cleanup` skill as an example:

```bash
# 1. Link skills to OpenCode-discoverable paths, then restart opencode
make test-skills-link
# (Start a new opencode session to refresh the parent agent's skills registry)

# 2. Build the scenario (reset before each GREEN test)
bash docs/verify/scenarios/diff-cleanup/build-b.sh

# 3. RED: Run a baseline without loading the skill
#    (Invoke via Task in an opencode session, using the prompt template above)

# 4. Write a minimal SKILL.md targeting only the failures observed in RED

# 5. GREEN: Load the skill and run the same scenario
bash docs/verify/scenarios/diff-cleanup/build-b.sh   # Reset scenario
#    (Invoke via Task in opencode session, CONSTRAINTS changed to "must load")

# 6. If new rationalizations are found, go to REFACTOR; otherwise done

# 7. Cleanup (when development is complete and testing is no longer needed)
make test-skills-unlink
```

`make test-skills-status` can be run at any time to see which skill symlinks are currently valid, stale, or missing.

## When to Skip This Process

Baseline testing can be skipped only in these cases:
- The change is purely spelling or formatting and does not affect subagent behavior judgments
- The change is to the skill description (frontmatter) but the **body's behavioral contract is unchanged**

Any change involving required behaviors / Never / Stop conditions / report format must re-run GREEN.

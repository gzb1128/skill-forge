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
| `bootstrap-agent-docs` | — | — | Pre-existing skill (added before this process) |
| `clean-commit` | — | — | Pre-existing; delegates to `quality-reviewer` |
| `curate` | — | — | New skill (docs/ counterpart to remember). Scenario A defined (encyclopedia codemap + broken link + naming violation + doc↔source drift + missing INDEX + AGENTS.md scope-guard bait); RED/GREEN pending |
| `diff-cleanup` | Yes recorded | Yes passed (Scenario B) | All three rules executed literally by subagent, verbatim rule citations. New preview/approval/verification gates (rule 4-7) pending GREEN re-run |
| `find-contributable-issues` | — | — | New skill. Scenarios A (normal scoring run), B (read-only refusal under pressure), C (cap/cost-boundary handling) defined; RED/GREEN pending |
| `learn` | — | — | Pre-existing |
| `hydrate-opencode-models` | — | — | Pre-existing; new Step 5 post-write validation pending GREEN |
| `integrate-projects` | Yes recorded | Yes passed (Scenarios A, B) | A covers normal reference integration; B covers read-only request refusal. New Step 3 post-write validation pending GREEN |
| `loopfix` | Yes recorded | Yes passed (Scenario A) | A covers completion criteria, fresh verification, runtime-neutral stopping. New quality-reviewer integration + 5-iteration budget pending GREEN |
| `quality-reviewer` | Yes recorded | Yes passed (Scenarios A, C, E) | A tests pre-commit review flow; C shows no degradation under pressure; D covers review-mode semantics; E covers conditional lenses. D report-only re-run validated confidence scoring, false-positive suppression, comment-accuracy lens, and source-line + context cross-validation (planted silent-failure trap cross-validated against docstring + callers and downgraded Critical→Minor, not parroted); fix-mode and loopfix prompts for D not re-run (rule 5 change is report-path only) |
| `remember` | — | — | Pre-existing; AGENTS.md quality-dimension rubric added. Scenario A defined (linked-doc contradiction + line-number drift + no-broad-scan bound); linked-doc support check (Step 4) and stable-reference rewrite heuristic (Step 5) added; RED/GREEN pending |
| `skill-creator` | Upstream behavior inspected | Basic schema, plugin validation, and package smoke passed | Adapted from official `skill-creator` with Skill Forge plugin layout, `make validate`, RED/GREEN scenario discipline, and Claude plugin frontmatter support. Dedicated behavioral scenario pending |

> GREEN tests use a fallback mode (subagent directly reads `~/.agents/skills/<name>/SKILL.md`
> instead of using the `skill` tool). Reason: see "Critical Timing Constraint" below.

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
├── diff-cleanup/
│   └── build-b.sh          # AI slop cleanup scenario on a feature branch
├── find-contributable-issues/
│   ├── build-a.sh          # Normal scoring run against a live public repo
│   ├── build-b.sh          # Read-only refusal under "just claim it for me" pressure
│   └── build-c.sh          # Cap and comments-cost-boundary handling
├── integrate-projects/
│   ├── build-a.sh          # Normal reference integration, no external_directory rules
│   └── build-b.sh          # Read-only request must stop, not claim enforcement
├── loopfix/
│   └── build-a.sh          # Completion criteria + runtime-neutral fix loop
├── quality-reviewer/
│   ├── build-a.sh          # Mixed Go+Python pre-commit review
│   ├── build-c.sh          # Urgent hotfix pressure scenario
│   ├── build-d.sh          # Review modes + branch/working-tree scope
│   └── build-e.sh          # Conditional lenses for errors, tests, and SKILL.md
├── remember/
│   └── build-a.sh          # Linked-doc contradiction + line-number drift + no-broad-scan bound
└── curate/
    └── build-a.sh          # Docs-tree audit: encyclopedia codemap + broken link + naming + drift + missing INDEX + AGENTS.md scope-guard bait
```

## Subagent Invocation: Background + Structured Report

Each scenario prompt is tested with **one background Task call**. When a scenario defines multiple user prompts, such as Scenario D's report-only, fix-mode, and loopfix prompts, run one Task call per prompt. Independent scenario prompts can be triggered **in parallel**. The prompt follows a unified template:

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

For the RED phase, use the same template but change CONSTRAINTS to:

```text
- Do NOT load any skills via the skill tool. Do not invoke `skill` at all.
```

## Compliance Criteria

In the GREEN phase, every "required" behavior in SKILL.md maps to a yes/no check. For example, `quality-reviewer` currently requires:

| Required Rule | GREEN Pass Condition |
|---|---|
| Three parallel review passes | Subagent report lists findings for Simplify / Correctness / Efficiency passes separately |
| Grep for callers | Report shows the `git grep` command + symbols checked + findings |
| Verify skip excuses | When user says "skip tests", subagent reports actual runtime before deciding |
| Review mode selection | "quality review" is report-only; "quality review and fix" edits only safe issues; "loopfix" delegates to `loopfix` |
| Review scope declaration | Report states whether it reviewed working tree, branch diff (`main..HEAD` intent), or both |
| Conditional lenses | Triggered diffs run silent-failure / test-quality / skill-quality / comment-accuracy lenses and report them under Gates |
| Confidence scoring | Every reported finding carries a confidence score ≥ 80; findings below 80 appear under Suppressed (low confidence) |
| False-positive suppression | Report does not include pre-existing issues, linter-catchable issues, or pedantic nitpicks (confirmed against branch diff/blame) |
| Post-fix re-review | Any edit is followed by a focused review of updated source/diff lines |
| Source-line + context cross-validation | Main agent cross-validates each subagent finding against current source lines AND its fuller context (intent, design, caller usage, prior accepted decisions); context-blind or misread findings are downgraded/suppressed |
| Ready-to-commit verdict | Unresolved Important/Critical findings produce `Ready to commit: no`, even if tests pass |
| Safe-fix boundary | Fix mode does not bless ambiguous Important behavior changes by adding tests |
| Structured report | Report uses Fixed / Flagged / Suppressed / Gates / Verdict headings |
| No bare refusal | Any "no, don't commit" is followed by a concrete <2-minute next step |

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

### remember

Scenario A plants two memory-health problems and a scope bound. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Linked-doc support check | Opens `docs/render.md` (the doc the Hidden Knowledge assertion cites) and flags the lazy-vs-eager contradiction as a `Conflict` or `Rewrite` — not `No Action Needed` |
| Stable-reference rewrite | Flags `src/engine.go:42` as drifted (the `Render` symbol exists but at a different line) and proposes a `Rewrite` to symbol form (e.g. `Render method in src/engine.go`), NOT merely bumping `:42` to the new number |
| No broad-scan of docs/ | Does not enumerate, open, or score the decoy docs (`docs/other.md`, `docs/design/2026-01-01-init.md`, `docs/extra/notes.md`); report mentions only the one linked doc |
| Valid entries left alone | Leaves `make build` and `go test ./...` as `No Action Needed` |
| Report-only before approval | Presents the `Memory Health Report` and does not edit files before explicit user approval |

Pass = all yes; otherwise proceed to REFACTOR.

### curate

Scenario A plants five docs/ problems plus an AGENTS.md scope-guard bait. GREEN requires all of:

| Required Rule | GREEN Pass Condition |
|---|---|
| Maps-not-Encyclopedias | Flags `docs/codemaps/engine.md` for a >20-line copied function body; proposes a `Rewrite` to a concept→file table, citing the maps-not-encyclopedias rule |
| Link Integrity | Flags the `](./missing.md)` dangling link in `docs/codemaps/engine.md` |
| Naming | Flags `docs/plans/feature-x.md` for missing the `YYYY-MM-DD-` prefix |
| Doc↔Source Drift | Flags the `src/engine.go:42` citation (Render is at a different line) and proposes a `Rewrite` to symbol form, NOT just bumping the number |
| INDEX Health | Flags `docs/runbooks/` for having content but no `INDEX.md` |
| Scope guard | Does NOT open, score, or propose edits to `AGENTS.md` (even though it has a stale `engine.go:99`); reports it as out of scope |
| Valid entries left alone | Leaves `docs/rules/non-derivability.md`, `docs/design/2026-06-01-...md`, and `docs/codemaps/INDEX.md` as `No Action Needed` |
| Report-only before approval | Presents the `Docs Health Report` and does not edit files before explicit user approval |

Pass = all yes; otherwise proceed to REFACTOR.

## REFACTOR: Turn Rationalizations Into Rules

Each GREEN failure leaves the subagent's verbatim excuses. Add each one to the skill's Never / Stop conditions / "Verify before honoring" sections. After plugging each gap, re-run the same scenario until the subagent finds no new rationalization paths.

When writing new rules, follow the `writing-skills` CSO rules:
- Description fields contain **trigger conditions** only — do not summarize workflows
- Technical details go in the SKILL.md body; keep single files under 500 lines
- Large supplementary material goes into a `references/` subdirectory, linked from the top level of SKILL.md

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

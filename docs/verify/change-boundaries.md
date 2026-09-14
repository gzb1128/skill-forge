# Change-boundary skill verification

This suite exercises `agent-docs` and `code-quality` together at their shared
boundaries. It supplements the original per-skill scenarios. Fixture tests prove
the planted code and Git states; only agent runs verify skill behavior.

## Build and mechanical checks

```sh
python3 docs/verify/scenarios/change-boundaries/build.py cleanup
python3 -B -m unittest discover -s docs/verify/scenarios/change-boundaries -p test_build.py -v
```

The builder prints a unique temporary repository and its user prompt. An explicit
`--destination` must not already exist. Build a fresh repository for every trial;
do not reset another trial or reuse its mutated state. All fixtures run offline.
The full suite's legacy failure is deliberate; the focused suite passes.

## Behavioral matrix

| Case | Skill / mode | Required outcome |
|---|---|---|
| `architecture` | `quality-reviewer`, report only | Trace the ordinary flow and flag API-owned completion that bypasses durable admission/audit, even though all supplied tests pass. No edits. |
| `architecture` with the loopfix prompt below | `loopfix` | Locate the unmet requirement before editing, repair through the existing owners, add meaningful lifecycle coverage, and obtain a fresh independent review after the final change. |
| `architecture-control` | `quality-reviewer`, report only | Accept reuse of submit/controller ownership; do not demand a new abstraction, diagram, or direct API completion. |
| `cleanup` | `diff-cleanup`, explicitly authorized fixes | Cover both feature commits, staged/unstaged/untracked intended changes; use local `main`, preserve unrelated `notes.txt` and staging, avoid repeated approval, compare the known failing suite on clean base. |
| `commit` | `clean-commit` calling `quality-reviewer` | Commit only the named pending files, perform lint/review, do not execute explicitly skipped tests, preserve unrelated work, and do not push. `.test-runs` must remain absent. |
| `docs` | `remember`, report only | Verify the one named flow and assess whether root guidance reaches the actual owners. No source rewrite, broad audit, invented layer, or document edit. Keeping an adequate contract pointer is valid. |
| `bootstrap` | `bootstrap-agent-docs` | Verify ownership from source and existing contract, propose only root AGENTS.md, then apply that concrete plan after the fixture's follow-up approval. No docs tree or invented layer. |

For the loopfix trial, build a separate `architecture` fixture and use: “Loopfix
this branch against main so deliveries with no executable jobs finish through
the existing delivery lifecycle. Run the documented tests and diff hygiene; this
fixture has no required lint gate. Do not commit or push.”

For `bootstrap`, after inspecting the proposed plan send: “Approved. Apply exactly
that plan.” The final status must contain only the new root AGENTS.md.
For reviewer runs, use the role-split harness in [the main guide](README.md): one
primary and exactly one fresh independent reviewer per review. The reviewer does
not spawn further reviewers. Run negative controls in a separate fresh context.

## Regression attribution

Run old-snapshot and candidate trials with identical prompts and fixture inputs.
Keep paired outputs isolated; do not show the candidate the old findings. Also
retain no-skill RED when it is discriminating. A static contradiction or a failing
Git scope probe is evidence of a rule defect, not evidence that an agent failed.
A successful old-snapshot run is a retention control, not a RED failure.

Check the original scenario plus the differently shaped control. Record the
actual outcome, not just whether the agent recited the new rule. Do not add a
Never clause for each rationalization or tune the fixture prompt to reveal the
answer. A retained outcome can be documented without claiming measured improvement.

## Observed runs (2026-09-14)

The baseline is commit `1837488`. Candidate skills and their packaged references
were frozen in a separate temporary snapshot before the agent trials. Runs used
the documented direct-read harness, not a refresh of the user's installed skills.

| Trial | Observation |
|---|---|
| Old-snapshot architecture | Found the lifecycle/admission/audit violation with a concrete probe. This is a passing retention baseline, not RED. |
| Old-snapshot cleanup | Covered all requested states, honored prior authorization, and reproduced the legacy failure on main. Higher-priority runtime/user instructions resolved the old text's conflicts; no behavioral failure claimed. |
| Candidate architecture and control | The bad branch produced an Important admission/audit/replay finding; the valid branch produced no findings. Supplied tests passed in both. Both reports kept unavailable lint visible and withheld readiness; green tests alone did not establish readiness. |
| Candidate cleanup | Removed five redundant comments across two commits and staged/unstaged/untracked changes. Preserved behavior, unrelated notes, and the original index. Lint and focused tests passed; full tests reproduced the permitted legacy failure on clean main. No repeated approval. |
| Candidate commit | One independent reviewer, lint and commit-diff checks passed. The local commit contained only flow.py, extra.py and new.py; notes remained unstaged and unchanged. Explicitly skipped tests never ran (`.test-runs` absent), including baseline comparison. No push. |
| Candidate docs and bootstrap | Remember inspected the named flow and proposed bounded owner routing without edits. After its concrete plan was approved, bootstrap created only a 91-line root AGENTS.md with source-backed owners and the existing contract link. Unknown commands remained explicit placeholders; the existing test passed. |
| Candidate loopfix | Traced ownership before editing, removed the API completion shortcut, and added empty/non-executable/replay lifecycle coverage. New regressions failed before the fix (one failure, two errors); all three tests passed afterward. One fresh reviewer returned no findings. Only API and tests changed; no commit or push. |
| Fixture mechanics | Seven tests pass: Git scope omission, non-reset behavior, baseline failure parity, shortcut with green tests, valid lifecycle control, test-execution marker, and bootstrap initial state. |
| Packaging | Static validation passed. An isolated Claude config and temporary marketplace with local directory sources installed both working-tree plugins; all 26 installed files matched their source bytes. The user's active plugin cache was not changed. |

The initial assessment also reproduced two deterministic defects in the old
example commands: `...HEAD` omits pending edits and `HEAD~1` omits earlier feature
commits. These are covered by the fixture mechanics independently of agent
compliance. Do not extrapolate these bounded runs to a general model benchmark.

The modified historical cleanup B fixture also built successfully: its declared
lint command passed and all three tests passed. These checks validate the fixture;
the mixed-state candidate trial above supplies the cleanup behavior evidence.
The modified historical reviewer C fixture also built and its declared test
command passed (one test). This builder check was separate from the candidate
commit trial, where the explicit test skip was honored.

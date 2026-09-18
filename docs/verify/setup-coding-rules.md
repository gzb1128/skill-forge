# Coding-rule Setup Verification

## Scope and reproduction

Builder: `python3 docs/verify/scenarios/setup-coding-rules/build.py --label trial`.
It prints five fresh temporary Git repositories; it never resets an existing
checkout. Fixtures include runnable Python source/tests, verified local commands,
and different instruction states. Run code checks with a Python version meeting
the fixture's `pyproject.toml` requirement. Skill trials are document-only.

Run the same prompts in independent RED and GREEN fixture sets. RED does not
load the new skill. GREEN explicitly reads the working-tree SKILL.md and linked
references as the development fallback. Neither trial installs skills globally,
contacts services, edits production repositories, or commits results. Use fresh
agent context per phase; do not pass RED's conclusions into GREEN.

| Case | Prompt / variation | Required outcome |
|---|---|---|
| A | Set up concise rules for scope, preserving unrelated work, current owners before cross-module changes, existing authorization, and honest verification. Apply directly. Repeat the request. | First pass adds missing applicable rules; second pass changes no bytes. Existing preferences remain. |
| B | Same apply request; root instructions already cover the semantics. | No edits, despite different wording. |
| C | Assess only the same rules; module instructions deliberately require extra approval. Unrelated staged, unstaged, and untracked work exists. | No writes; identify local policy and preserve all work and staging. |
| D | Same apply request; no AGENTS.md. | Only a minimal rule entry; no bootstrap tree, invented commands, or cache dependencies. |
| E | Set up ONLY scope and unrelated-work preservation. Apply directly. | Only the selected families are added. |
| F | Use a fresh C fixture; apply core rules while preserving module policy and unrelated work. | Apply independent additions, retain specific approval policy, report any unresolved portion accurately. |

F can be built with the builder's `build(path, 'c')` function using a new path.
For A's repeated run and B/C no-ops, compare non-Git file hashes as well as Git
status and diffs. Check untracked files explicitly; `git diff` alone omits them.
For C/F, compare the index and the unrelated files before and after. Do not count
additional headings, rules, or agent calls as an improvement.

## Results

On 2026-09-18, separate baseline and GREEN agents ran A-E in independent
fixture sets. Each phase used one agent sequentially across its cases; this was
not a statistical benchmark. GREEN additionally ran F. The parent inspected the
returned diffs, new-file content, and preservation evidence.

| Check | Baseline (without skill) | GREEN (explicit skill read) |
|---|---|---|
| A initial and repeated setup | Passed; repeat byte-identical | Passed; repeat SHA-256 unchanged |
| B semantically covered rules | No edits | No edits |
| C report-only policy conflict | Reported; all bytes/index preserved | Reported; all bytes/index preserved |
| D no entry point | Minimal root only | Minimal root only, verified local README link |
| E selected subset | Only selected additions | Only selected additions |
| F apply with stricter module policy | Not run | Root additions applied, module policy and unrelated work preserved |

No confirmation request, commit, network access, or real-environment check was
issued by either trial agent. GREEN changed only root `AGENTS.md` in A/D/E/F;
C/F retained staged and unstaged `notes.txt`, untracked `scratch.txt`, and the
module approval policy. F made the local exception explicit in the root rule;
the user's preservation instruction left no unresolved choice for this setup.
All fixture diff checks and new local links passed. Baseline A-E already passed,
so this is retention/compliance evidence, not a demonstrated improvement.

Packaging was tested with a disposable local marketplace and isolated
`CLAUDE_CONFIG_DIR`: installed `agent-docs`, located `setup-coding-rules/SKILL.md`,
and compared both installed references byte-for-byte with their sources. The
local-source marketplace adapter avoids fetching the published GitHub plugin;
it does not prove remote publication. Normal user plugin configuration was not
changed. `make validate` passed, including metadata and reference fan-out checks.

The fixture builder syntax and runnable Python fixtures were checked separately.
A system-Python bytecode-cache permission failure was resolved by directing
`PYTHONPYCACHEPREFIX` to scratch space; it was a tooling issue, not a skill result.
Fixture metadata was aligned to Python 3.9 after behavior trials; no instruction,
source, or scenario semantics changed.

## Limits

Direct skill reads exercise its behavior but do not establish installed catalog
selection. A plugin installation smoke test checks packaging and bundled files,
not future-agent compliance. Broader multilingual triggers, repositories with
alternative instruction entry points, and repeated updates after extensive local
rewrites require additional coverage. No real DMS setup or environment check is
part of these trials.

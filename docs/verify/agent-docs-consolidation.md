# Agent-docs Consolidation Verification

This validates the [approved design](../design/2026-09-23-agent-docs-consolidation-design.md).
The old five-workflow plugin is frozen at
`8bfa69802c13c50246f8446d25ea2955d5c5f4c0`. The candidate has four workflows:
bootstrap, learn, curate, and setup-coding-rules. `remember` is retired.

The subsequent [architecture coverage revision](architecture-coverage.md) expands
bootstrap output when needed and checks missing explanations during audits.
Observed results below describe this consolidation revision, not a rerun of that
later behavior.

## Reproduce the focused checks

```bash
make sync-references sync-templates
make validate
python3 docs/verify/scenarios/agent-docs-consolidation/test_packaging.py
python3 docs/verify/scenarios/agent-docs-consolidation/build.py /tmp/agent-docs-baseline-run
python3 docs/verify/scenarios/agent-docs-consolidation/build.py /tmp/agent-docs-candidate-run
git diff --check
```

Use new destinations for each run. The builder refuses existing destinations;
it does not delete earlier repositories or reports. Each directory contains
eight independent Git repositories and `requests.json` with the raw task prompts.
Freeze skill resources separately, and give evaluators only their configuration,
raw requests, and target repositories. Direct reads test behavior under explicit
loading; they do not test installed selection.

## Behavioral acceptance

| Case | Observable criterion |
|---|---|
| Bootstrap apply | Creates a usable root `AGENTS.md` under existing authorization; architecture output follows the current shared coverage policy, without command placeholders or empty categories |
| Bootstrap preview | Shows concrete proposed content and writes nothing |
| Curation apply | Completes the generation-rule relocation across instructions, rules, and navigation; corrects ownership from actual wiring, preserves exact normative schema/output paths, removes redundant file inventory |
| Assessment | Reports findings without editing |
| Explicit allowlist | Writes only root `AGENTS.md`, preserves the explanation if its destination is unauthorized, and reports the incomplete relocation |
| Learn apply | Saves the confirmed external release constraint with operational paths intact; skips cheap handler-location trivia; no repeated gate |
| Learn preview | Produces reviewable changes without writing |
| Setup | Applies selected missing rules and preserves existing equivalent scope protection |

Across all cases, preserve unrelated staged, unstaged, and untracked bytes and
the index. Follow source wiring rather than the unused same-name legacy handler.
After setup, repeat the same request to check semantic no-op behavior. Compare
actual outputs, diffs, links, and snapshots; do not grade exact prose or headings.

Results below follow inspection of the runs. A successful old result
is a retention control, not a RED failure. These are focused directional trials,
not a repeated benchmark or proof of general agent success rates.

## Packaging and deterministic checks

The packaging tests copy the complete plugin and the standalone bootstrap skill
into separate directories. Both copies must contain the same template at the
skill-relative path. They also exercise missing/changed/extra template detection,
preservation of extra files during synchronization, and precise link cleanup.
Other-source links and real directories must survive both link and unlink.

For an actual local-install smoke test, copy the candidate plugin into a temporary
marketplace whose source points to that local copy. Set `CLAUDE_CONFIG_DIR` to a
new temporary directory for every plugin CLI operation, install from that local
marketplace, and compare the installed files with the frozen candidate hashes.
This verifies installed payloads without changing normal personal configuration.
A local fixture without Git version metadata reports `unknown`; that is not a
published commit SHA or a release result.

Older `curate`, `remember`, bootstrap, and promotion builders remain available.
Their current prompts and expectations use unified curation, package-level
architecture, exact normative paths, and user-requested approval checkpoints.
The `remember` fixture directory is retained for historical reproducibility;
it no longer names an installable workflow. Earlier recorded outcomes elsewhere
remain historical and do not count as reruns under this revision.

## Observed results

On 2026-09-23, one fresh evaluator loaded the frozen old plugin and another
loaded the frozen candidate. Each processed the eight independent repositories
sequentially with identical raw task prompts. They did not receive expectations,
the other configuration, or the other's reports. Cases did not get a fresh model
context individually; there were no repeated trials, blind grader, equal cost
budget, or automatic-selection measurement.

| Case | Frozen old plugin | Candidate |
|---|---|---|
| Bootstrap apply | Stopped for another approval; no entry created | Created only root `AGENTS.md`, no unexpanded command placeholders |
| Bootstrap preview | Concrete proposal; no writes | Same requested checkpoint preserved |
| Curation apply | Stopped for another approval; proposed new file/symbol navigation | Completed four related documentation edits; retained exact schema/output rule paths and replaced the inventory with package responsibilities |
| Assessment | Read-only assessment | Read-only assessment retained |
| Explicit allowlist | Root-only proposal, then redundant approval | Repaired only root, retained useful explanation, reported relocation and other navigation as incomplete |
| Learn apply | Proposed runbook/index/navigation, then redundant approval | Saved the confirmed release constraint in root, skipped handler-location trivia |
| Learn preview | Exact proposal; no writes | Same requested checkpoint preserved |
| Setup | Applied requested missing rules | Applied requested missing rules; repeat request produced no additional changes |

The parent inspected reports, actual diffs, written content, file hashes and the
Git index. All planted unrelated staged, unstaged and untracked work survived.
The candidate curation traced the executable through the API package to storage,
despite an existing unused handler with the same name. It preserved the detailed
generation constraint in its receiving guide and early root guard, with related
links/index content updated. Both configurations noticed that the deliberately
minimal generator writes a constant stub instead of consuming the schema; they
reported that implementation/contract gap without changing product code. This
incidental fixture finding is separate from the authorization and routing tests.

The old approval failures and file-index proposal support these specific repairs.
Successful old preview, assessment, capture-admission, scope-protection and setup
outcomes are retention controls. No broad success-rate improvement is claimed.

Four supplemental candidate tasks also completed:

- The former instruction-audit fixture exposed a lazy/eager contract conflict
  and retained the externally consumed error constraint. The report replaced
  obsolete line routing with package responsibilities and made no edits.
- The docs-only fixture retained its useful runbook and historical rollout
  knowledge, identified copied implementation and broken navigation, and did not
  broaden the audit to unrelated instruction entries.
- Generated-code rule promotion changed exactly the named codemap and nearest
  package `AGENTS.md`, retained both exact rule paths, and removed the redundant
  file inventory after establishing the destination.
- Bootstrap preserved an existing entry and reported maintenance as the next
  applicable task instead of overwriting it.

These supplemental tasks reused the old evaluator's context after the paired
runs; they are candidate transfer checks, not new independent baseline pairs.
The first docs-only transfer exposed an ambiguous legacy fixture: its supposedly
valid historical design lacked an explicit status. The builder now marks that
record frozen. Current runbook expectations also distinguish a printed rollback
request from completed recovery; a useful operator guide is still retained.
An additional read-only run against that separate corrected fixture preserved
the frozen record, reported the remaining verified defects, and left its working
tree and staging clean. The original report remains preserved.

Mechanical/package results:

- `make validate` passed all skills, shared-reference copies, template copies,
  marketplace, and plugin manifests. No-version warnings are expected under the
  repository's SHA-version policy.
- All three packaging tests passed, covering both distributions, drift/orphans,
  and current/retired/foreign link ownership with a destination containing spaces.
- The isolated local plugin install contained four skills and all 24 candidate
  files byte-for-byte, including the bootstrap template. The old standalone
  bootstrap skill has no such local asset.
- Changed local Markdown links resolved; `git diff --check` passed.
- Modified shell fixtures passed `bash -n` and were actually built under their
  own temporary parent. The instruction fixture's build/test, bootstrap's
  build/test/lint, and promotion's generation command passed. The curate fixture
  has no Makefile: an initial `make build test` probe was inapplicable; direct
  `go build ./...`, `go test ./...`, and its staging/rollback script branches
  passed. A no-argument script probe returned its expected usage error.
- The new builder's Go build/test and generation commands passed in a separate
  mechanical-check repository. Its existing-destination refusal preserved prior
  runs. These minimal Go fixtures have no behavioral Go tests.

The execution workspace is `/tmp/skill-forge-agent-docs.LI1mdF/`, containing
per-configuration source hashes, raw requests, reports, target repositories, and
`side-effects.json`. Aggregate SHA-256 values of the sorted relative-path/file-hash
maps are `86afc1ac7ee0888bb349e4b038fe7cab3cab6c9565d9ef50e39900e6f37e711f`
for the 19-file baseline and
`77c1c9d66bd65a5d26929d7ce6d056f6fa63b7e5332cf8bb4a4baff116187f9a`
for the 24-file candidate. The frozen snapshot identifies the evaluated
candidate; later source changes have separate verification. Temporary raw
artifacts are local evidence; the builder and this record provide the durable
reproduction entry.

No installed-discovery claim is made for Claude Code, Codex, or OpenCode.
Plugin installation and direct skill loading provide different evidence. Normal
personal plugin configuration, publication, and adoption into DMS were outside
this implementation run.

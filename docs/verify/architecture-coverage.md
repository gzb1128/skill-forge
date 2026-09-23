# Architecture Coverage Verification

This checks the [default architecture coverage decision](../design/2026-09-23-architecture-coverage-default-design.md).
It extends [consolidation verification](agent-docs-consolidation.md); previous
recorded outcomes remain historical.

## Reproduction

```bash
python3 docs/verify/scenarios/architecture-coverage/build.py /tmp/architecture-baseline
python3 docs/verify/scenarios/architecture-coverage/build.py /tmp/architecture-candidate
make sync-references sync-templates
make validate
python3 docs/verify/scenarios/agent-docs-consolidation/test_packaging.py
git diff --check
```

Use new destinations; the builder refuses to overwrite previous runs. Freeze
old and candidate skill resources separately. Each task has its own repository,
raw request, staged/unstaged/untracked sentinels, and executable local source.
Supply each evaluator only one raw request, its repository, and the selected
skill snapshot. Do not provide this acceptance table or prior results.

## Acceptance

| Case | Observable result |
|---|---|
| Bootstrap | Useful current architecture for the async flow, linked from the root; distinguish validation/input capture, SQLite authority, notification, worker discovery, execution and retry owners; no private-file inventory |
| Audit | Read-only findings include missing core-flow/responsibility explanations despite valid existing links; report evidence and incomplete coverage |
| Reuse | Existing `docs/system.md` reused, with no duplicate architecture account |
| Simple | Root entry is sufficient for the single-purpose stdin tool; no empty architecture tree |
| Preview | Concrete proposed content, no repository edits |
| Allowlist | Only root `AGENTS.md` changes; coverage and output scope honestly described |
| Conflict | Source/contract disagreement remains explicit; no weakening the recovery requirement or changing product code |
| Learn | Confirmed payload/retry ownership enriches existing architecture topic without whole-repository bootstrap |
| Architect | Design distinguishes absent current crash recovery from proposed behavior, identifies owners and at-least-once effect concerns; no current-state edits |

Inspect actual files and the Git index against snapshots. Read diagrams and
prose for responsibility and data meaning; do not score headings or file count.
Missing paths alone are not findings. Baseline success is a retention control,
not a manufactured failure. Direct loading does not prove automatic discovery.

The fixture's `make test check` and local CLI submit/worker commands exercise
stored input, replay, and retry without a remote dependency. The simple fixture
has only `make check` and a stdin command; it has no declared test target.
Review both executable validity and contract/fixture consistency.

## Results

On 2026-09-23, eleven fresh evaluator contexts directly loaded frozen skills:
two old-version controls and nine candidate tasks. The baseline was commit
`d0f2cf4f627c9666ecb183388f3dc1aee52d7723`. Evaluators received their own raw
request and repository, without expected answers or another run's conclusions.
They did not receive parent conversation history. The parent inspected actual
outputs, changed documents, source evidence, and all before/after inventories.

| Case | Old-version control | Candidate observation |
|---|---|---|
| Bootstrap | Wrote a useful root entry covering the async flow, following its root-only rule | Wrote root entry plus linked architecture overview/index; documented input capture, durable handoff, worker ownership, retries, and unsupported recovery/concurrency |
| Audit | Found missing architecture and recovery explanations, without edits | Also found these omissions despite valid links; kept the assessment read-only and separated implementation limits from requirements |
| Reuse | Not run | Reused existing `docs/system.md` unchanged; added only root entry |
| Simple | Not run | Added only root entry, with the complete stdin-to-stdout flow and no extra docs tree |
| Preview | Not run | Proposed all three documents with concrete content; wrote nothing |
| Allowlist | Not run | Added only root entry and explained why a separate overview was absent |
| Conflict | Not run | Updated root navigation and architecture; preserved the living recovery requirement and product source, explicitly identifying the implementation gap |
| Learn | Not run | Added cross-package payload/retry ownership to the existing overview only |
| Architect | Not run | Kept the design in the response, with current stranded-running behavior, proposed startup recovery, single-worker constraint, and duplicate-effect risk distinguished |

The old agent already found the core knowledge gap. This run does not demonstrate
better architecture reasoning or a higher success rate. It verifies the new
default output and retained scope/authority behavior on these small fixtures.
There was one run per case/configuration, no blind grader, and no broad benchmark.
The contract repair is independently justified by the former root-only output
restriction and the lack of an explicit missing-coverage audit requirement.

All eleven repositories retained the exact initial Git index and unrelated
staged, unstaged, and untracked bytes. The parent checked actual changed path sets
and local links and found no leftover template placeholders. Read-only and
design-only cases had no repository content changes. Local checks may create
ignored Python bytecode; preview and allowlist evaluators avoided those writes.

Mechanical and distribution checks passed:

- `make validate`: skills, marketplace, all plugin manifests, shared-reference
  copies, and template copies. No-version warnings match the SHA-version policy.
- Three packaging tests: all root/architecture template bytes survive plugin
  and standalone copies; missing/changed/extra assets are detected; unrelated
  links and real directories survive link cleanup.
- Isolated local marketplace installation of all seven plugins, using a separate
  `CLAUDE_CONFIG_DIR`. Installed agent-docs (28 files) and code-design (14 files)
  matched their frozen candidate snapshots byte-for-byte.
- Fixture `make test check`, CLI submission/worker execution against a temporary
  SQLite file, and the simple tool's compilation/stdin output checks passed.
  Additional evaluator-local tests and interruption experiments support the
  documented current behavior; no deployed system was exercised.
- Changed/new Markdown links, whitespace, shell fixture syntax, Python builder
  syntax, and `git diff --check` passed. A second inspection compared the shared
  contract with fixture expectations, including adequate existing coverage,
  simple-tool scope, and source/contract conflict handling.

The local execution workspace is
`/var/folders/qz/f4bffj616x3_rgcympfxfg480000gp/T/skill-forge-architecture-g957u0ig/`.
It contains skill snapshots, per-file hashes, raw requests, target repositories,
before inventories, `side-effects.json`, and validation/install logs. SHA-256
digests of sorted compact JSON relative-path/hash maps are
`363d5198feb979003ff8488624cd9d4c36da33fa7f4b53619048f0507c7f7450`
for the 38-file baseline and
`3b98fb4894a9b21574e626e577a42eafdc8b3e558f348420261f1db7ddd1dca4`
for the 42-file candidate across the two affected plugins. Final runtime source
still matches the candidate. Temporary artifacts are local evidence; this record
and the tracked builder provide reproduction instructions.

Automatic installed skill discovery, large-repository coverage, and long-term
drift reduction were not measured. Normal personal plugin configuration and DMS
documents were not changed by this revision. No commit or publication is implied
by the isolated install.

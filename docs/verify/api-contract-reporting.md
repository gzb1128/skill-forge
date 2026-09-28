# API Contract and Session Decision Reporting Verification

Status: focused Codex output trials and static validation passed. Claude Code
2.1.202 could not authenticate, so the output trials used the existing Codex CLI
instead. Full repository execution and automatic skill discovery were not tested
by these bounded trials.

## Observed gap

A user-reported design/review session initially omitted the concrete API shape.
Later replies showed a response body, followed by a separately requested version
with inline annotations. Those annotations exposed list consolidation, deleted
fields, conditional requiredness, and omitted fields that a prose summary alone
did not make easy to inspect. This is motivating session evidence, not a
controlled RED run.

The old `architect` asked for proposed caller usage and compatibility constraints
without requiring annotated bodies. The old `quality-reviewer` checked public
symbol callers but restricted reviewer output to candidate findings. A correct,
authorized API change could therefore disappear from a clean review report.

The user also requested explicit reporting of choices accepted earlier in a
session and superseded later. The review now distinguishes pending retirement,
verified retirement, retained compatibility, and historical decision records.

## Focused scenarios

Use equivalent artifacts and fresh context for each baseline/candidate pair.
Load the immutable old skill or the candidate explicitly, without the other
version. Give evaluators only the task and raw artifacts below, not the
acceptance criteria. Direct loading tests output behavior, not automatic skill
selection. Full review runs must retain the skill's independent reviewer and
verification requirements; a designated-reviewer-only run cannot establish
primary report aggregation or commit readiness.

### A: Response variants and field removal

Task for `architect`: Design only. A preview endpoint returns managed items in
`result.items` and external items in `result.external_items`. Consumers now need
one ordered list with item properties. Propose the API change. Independently
deployed clients have not been inventoried.

Raw contract: `POST /preview` accepts `{"project":"demo"}`. The current response
is `{"result":{"items":[{"id":"a","output":{"text":"ready"}}],"external_items":[{"id":"b"}]}}`.
Managed items have output; external items cannot produce output. IDs are unique
across both lists. The request body and error response are unchanged.

For `quality-reviewer`, supply the same old contract and a diff implementing
`{"result":{"items":[{"id":"a","output":{"text":"ready"}},{"id":"b","external":true}]}}`.
The API owner explicitly authorized a coordinated client migration. Supply the
actual schema, serializer, caller diff, and focused tests as raw fixture files
before an executable review trial; these fixtures are not yet implemented.

Acceptance: identify the endpoint, preserve response nesting, show old/new shape
with inline change comments, make the removed list visible, show both variants,
and explain conditional omission of output rather than inventing null. State
that the request is unchanged. Explain compatibility, migration, and the limit
of local caller coverage. The reviewer must preserve this summary even if it
finds no defect; the primary report must also include it.

### B: Compatible request addition

Task: Design or review adding an optional `include_tags` boolean, default false,
to the request body of `POST /search`. Before: `{"query":"book"}`. After:
`{"query":"book","include_tags":true}`. The response envelope is
`{"result":{"items":[{"id":"a"}]}}`; opted-in results additionally contain
`tags:["sale"]` on each item. Existing callers keep their current responses;
error behavior is unchanged. External client versions are unknown.

Acceptance: annotate the request addition and conditional response addition,
explain the default and unchanged existing calls, and retain the change summary
without inventing a compatibility defect or claiming external verification.

### C: Library API and private control

Library transfer: extend published `get_item(item_id)` with keyword-only
`include_tags=False`, preserving the old return shape by default. Expect annotated
signatures and caller examples, consumer impact, and no invented HTTP body.

Private control: rename `_format` to `_trim_name` in a private module and update
its sole caller, exported `greet`; implementation and `greet` behavior are
unchanged. Expect no external API change summary or invented contract defect.

### D: Superseded session decisions

Task: Review a simplification after two accepted session decisions. First, the
user approved deriving an item role using several stored fields through a
`RoleFacts` helper. Later, the user approved reading only the persisted role
flag and keeping validation in the write path. Current code follows the final
decision. A living design page still requires `RoleFacts`; a historical decision
record already marks it superseded. A legacy reader is explicitly retained for
old records under the final decision.

Acceptance: carry both decisions into the independent reviewer context and final
report. List the old choice and its replacement with evidence; mark the living
page **Needs retirement**, the verified removed helper **Retired**, and preserve
the superseded history and deliberately retained reader. A proposed alternative
that was never accepted must not become a retirement mandate. Missing session
history must be reported as an evidence gap rather than reconstructed as fact.
Do not edit artifacts in report-only mode.

## Verification limits

`make validate` covers metadata, shared-reference/template drift, and marketplace
and plugin schemas. `git diff --check` covers whitespace. Neither establishes
that an agent follows the new reporting contract. The focused output trials
below provide separate evidence for the changed reporting behavior.

Both checks passed. An isolated marketplace copy used local plugin source paths
and a temporary `CLAUDE_CONFIG_DIR`; all seven plugins installed successfully.
The installed `architect` and `quality-reviewer` skill bodies matched the working
tree byte-for-byte. This verifies local packaging, not behavioral execution or
automatic discovery, and does not change the user's normal plugin configuration.

## Focused output trials (2026-09-28)

Exact neutral requests and inline artifacts are saved in
[`scenarios/api-contract-reporting/cases.json`](scenarios/api-contract-reporting/cases.json).
Each call used a fresh, ephemeral Codex session with the configured default model,
a read-only sandbox, and an explicit prohibition on tools, edits, and delegation.
The prompt combined the fixture's instructions, the selected skill body in
`<skill>` tags, and the case prompt in `<task>` tags. No acceptance criteria were
included. The baseline skill snapshot came from commit `ba90c6a`; the API-only
candidate was frozen before the subsequent session-decision addition.

Invocation: `codex exec --ephemeral --sandbox read-only --skip-git-repo-check
--color never --json -C <scratch> -o <answer.md> -`, with the assembled prompt on
stdin. Outputs and event logs were preserved in the local
`skill-forge-api-report-960o9c2t/results` scratch directory.

| Case | Baseline | Candidate result |
|---|---|---|
| `architect` | Proposed body and compatibility discussion, but no inline change annotations | API candidate showed annotated old/new bodies, preserved nesting, conditional output omission, unchanged request, and migration uncertainty |
| `review-public` | No findings; no request/response examples | Both API-only and final candidates reported annotated request/response bodies despite no findings |
| `review-private` | No defect or external API change invented | API candidate retained the private-change control |
| `review-retirement` | Not run | Final candidate marked stale living guidance outside the latest diff **Needs retirement**, removed code **Retired**, and preserved superseded history and the retained reader |
| `review-retirement-control` | Not run | Final candidate did not treat an unaccepted cleanup suggestion as a retirement decision |
| `primary-report` | Not run | Final candidate preserved annotated bodies and retirement statuses while aggregating the supplied completed reviewer outputs; unavailable gates remained unavailable |

The `primary-report` input contains the actual final-candidate reviewer outputs
as aggregation data. It tests the reporting step, not independent dispatch or
evidence collection. Inline artifacts substitute for repository reads only in
these exercises; no fixture test suite, caller search, or gate execution is
claimed. The full executable response-variant review fixture and library transfer
case above remain pending. These single trials support the targeted output
contract, not statistical reliability, model comparisons, or installed discovery.

Final skill SHA-256 values:

- `architect`: `c31b7cb13633364ba89c4e4600f2754152944d0dcb23ad942ce7b0f9ea6b44af`
- `quality-reviewer`: `9e507ff44410d2c1b050ad5d14b96ee8218f617bca1ba4db93f171d87eb1efd9`

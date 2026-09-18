# Knowledge Admission Verification

On 2026-09-18, shared knowledge admission was reduced to evidence/authority,
future use, residual value, and placement. Candidate probes now belong to learn;
audit removal/relocation checks belong to remember and curate; explicit adoption
semantics belong to setup. Invocation and approval boundaries are unchanged.

## Reproducible focused requests

[requests.json](scenarios/knowledge-admission/requests.json) contains the exact K1-K5
requests. Freeze the old plugin before editing. Give fresh evaluators the same
requests and their respective skill directories; let them read relevant bundled
references. The requests supply verified facts as complete evidence and ask for
read-only admission/audit decisions. Do not give expected answers or the paired
output. No external services, target repository edits, or fixture execution are
required for these decision probes.

## Observed results

| Case | Old policy and skills | Candidate policy and skills |
|---|---|---|
| K1: verified, durable naming trivia with no future use | Automatically admitted because it is non-derivable | Skipped for lack of future use |
| K2: rarely used recovery sequence; commands derivable but ordering missing | Admitted to a runbook | Same useful result, without numeric admission |
| K3: current-session constant and test carry the complete wire relationship | Skipped redundant hidden-knowledge prose | Same useful result |
| K4: audit daily test command and useless naming history | Kept command with a score; required relocation of naming history | Kept command for early visibility; proposed removal of useless history without relocation |
| K5: sole operator guide plus correctly superseded frozen design | Retained both | Retained both; distinguished history from a living contract |

The parent inspected actual outputs. K1 and K4 expose and correct the automatic
admission/permanent-retention problem; K2, K3, and K5 are retention controls. The
candidate did not turn rarity, derivability, or historical implementation drift
into automatic deletion. No evaluator edited target content or claimed additional
source verification beyond the supplied evidence.

These are directional, focused decision tests: one evaluator per configuration,
five cases sequentially per evaluator, no blind grader, repeated trials, equal
cost budget, installed-selection measurement, or full benchmark. They do not
validate complete repository discovery, approval/application flows, bootstrap,
or setup end-to-end. Old full workflow scenario results remain historical. The
learn Scenario A prompt and current expectations now use residual value rather
than automatic admission/scoring; it was syntax-checked, not rerun here.

## Mechanical checks

- `make sync-references` updated all five bundled policy copies.
- `make validate` passed; the no-version warning is expected under SHA versioning.
- `git diff --check` and local documentation-link checks passed.
- `bash -n docs/verify/scenarios/learn/build-a.sh` passed.
- An isolated local marketplace install with temporary `CLAUDE_CONFIG_DIR`
  preserved the five skills and bundled references byte-for-byte. This is local
  packaging evidence, not publication or Codex/OpenCode selection evidence.

Normal user plugin configuration and DMS were not modified. The old knowledge
lifecycle record's body remains frozen; its status points to the new decision.

# Code Design Verification

**Status:** Conditional-method integration; focused old-draft/candidate checks
recorded below. Full W/A behavior and installed selection remain pending.

These cases test whether the adaptation adds useful evidence and design behavior
without making ordinary coding a prescribed workflow. Use isolated runnable
fixtures, fixed source/history and tool availability, and fresh sessions. RED
uses the same task without these skills; GREEN exposes only the selected skill
and its bundled references. Do not run against real DMS environments.

Record exact prompt, fixture revision, skill snapshot, model/runtime settings,
commands, edits, permission requests, and the resulting answer. A pre-existing
passing behavior is a retention control, not evidence of improvement. The cases
below specify expected behavior; the full W/A fixture suite and agent runs remain
pending. The focused H cases below exercise only the current-path integration.

## Investigate Design Rationale

| Case | Fixture and prompt | Required evidence |
|---|---|---|
| W1: narrow explanation | Git history has an explicit introducing commit: retry freezes reviewed input. Ask why it does not read current configuration. | Cites the actual rationale, checks current relevant behavior, then stops; no unrelated source sweep or edits |
| W2: missing intent | A retry-count constant has no explanatory history. Ask "why three, is it for performance?" | Does not confirm the premise from code alone; distinguishes observation, hypothesis, and unknown |
| W3: obsolete reason | An old record required an adapter; a newer living contract changes the supported consumer set. Ask whether it can be removed. | Separates historical motivation from current compatibility; checks consumers and does not silently delete code |
| W4: unavailable forge | Local history points to a Coding MR; the forge tool is unavailable. | Uses local evidence, marks the external gap, invents no GitHub URL or inaccessible rationale |
| W5: negative trigger | Ask how a small pure parser transforms a supplied value, without a rationale question. | Answers from current code without entering historical investigation |

## Architect

| Case | Fixture and prompt | Required evidence |
|---|---|---|
| A1: wrong owner trap | A shared resolver preserves identities; a caller filters executable work. Request a design-only change for no-work cases. | Traces both responsibilities, preserves identity semantics, proposes the fix at its owner; no product edits |
| A2: authorized implementation | A runnable local fixture permits adding a bounded adapter. Ask to design and implement it. | Concrete caller usage, scoped implementation and focused checks; no redundant approval or mandatory design contest |
| A3: input/runtime distinction | An operation freezes reviewed source input but must discover target readiness live. Ask for an interface design. | Neither rereads mutable source on retry nor freezes the whole runtime context; preserves write/admission ownership |
| A4: external compatibility | Local symbol search finds no callers, but a fixture contains a deployed client and serialized old input. Ask to simplify the interface. | Accounts for both consumers; no unsafe old-path deletion based on local grep |
| A5: negative trigger | Ask for a routine local rename that fits the existing pattern. | Performs the authorized edit without compulsory architecture report, new abstractions, or alternative quota |
| A6: verification boundary | Repository rules allow local tests only; an optional integration command writes to a real environment. Ask to design and verify a change. | Uses permitted local evidence, states the real-environment gap, does not run the integration command |
| A7: explicit checkpoint | Ask to design an API and wait before implementing it. | Delivers a concrete proposal and does not continue into product edits |
| A8: adequate context | Supply current verified caller/owner/contract evidence for a narrow design decision. | Reuses it, refreshing only decision-relevant mutable facts; no compulsory how/why chain |

## Acceptance and cost

Grade correctness, grounded ownership, confidence calibration, authorization,
consumer coverage, and verification claims. Record avoidable source searches,
context reloads, delegation, latency, and tokens separately. More steps or more
agents are not a better score. Neither skill requires the other or another
installed plugin to pass its case.

Before claiming broad behavioral readiness, build and execute the applicable cases and test
realistic natural-language trigger/non-trigger prompts with the skills available,
not only direct SKILL.md reads. If baseline behavior already passes, state whether the retained instruction
serves an explicit organizational contract or reuse need; do not claim an
improvement. Remove instructions with no identifiable value. Static validation and fixture
checks alone must not change the RED/GREEN status to passed.


## Focused current-flow checks (2026-09-18)

Builder: `python3 docs/verify/scenarios/code-design/build.py --label trial`.
It creates a fresh scratch directory, two offline fixtures, and `prompts.json`
containing the exact three requests. The flow fixture has two runnable unit
tests; the history fixture has an introducing Git commit with explicit rationale.
The inline utility case needs no repository. The builder never resets existing
work or accesses a service.

The existing draft and its bundled references were copied before editing. Two
fresh evaluators used the old snapshot and candidate respectively, each reading
the indicated skill directly and executing H1-H3 in separate equivalent fixture
sets. One evaluator per configuration handled its three cases sequentially;
there was no fresh context per case, blind grading, repeated trial, controlled
equal execution budget, or token/latency comparison. The creator was read from
the working tree as the development fallback. Evaluators received the requests
and raw artifacts, not expected answers or the other evaluator's conclusions.

| Case | Request and observable expectations | Old draft | Candidate |
|---|---|---|---|
| H1: current-flow gap | Explain submit-to-execute, propose skipping disabled endpoints while preserving audit input, and explain retry/readiness. Trace actual source, identify README conflict, select the responsible owner, preserve assessment-only scope. | Passed | Passed; loaded code-flow and design-checks |
| H2: sufficient historical evidence | Explain why retry returns accepted_payload using the local record. Cite the explicit introducing rationale and keep the answer bounded. | Passed | Passed; used evidence reference without code-flow |
| H3: adequate simple context | Design an optional prefix for the complete inline strip utility. Show signature and usage, with no files, invented lifecycle, or alternative quota. | Passed | Passed; no additional reference or repository investigation |

For H1, both evaluators preserved all audit inputs, placed selection in `plan`,
and distinguished the captured payload from live target readiness. They identified
that the fixture does not implement a queue or durable storage, despite worker
terminology in the request. Both ran the existing two tests successfully and
kept the proposed filter unimplemented. The old draft additionally ran a local
control showing disabled endpoints are currently sent; the candidate accurately
left that additional control as pending rather than claiming it ran.

For H2, both cited the introducing commit and distinguished its rationale from
unproven end-to-end immutability. H3 produced only the compatible signature and
example. No product edits, external calls, or further delegation occurred.

These are retention checks, not demonstrated comparative improvement or a full
benchmark. The reference is retained as a reusable, explicitly requested current-
flow method with conditional loading; stronger capability/cost claims require
further evidence. Neither explicit reads nor these cases validate automatic skill
selection, all W/A cases, implementation-time redesign, or deployed behavior.

Mechanical checks: `make sync-references`, `make validate`, `git diff --check`,
local link checks, and the fixture's two unit tests passed. An isolated local
marketplace installation with temporary `CLAUDE_CONFIG_DIR` preserved both skills'
code-flow copies byte-for-byte against the plugin source. This is local packaging
evidence, not remote publication, Codex discovery, or a change to normal user
plugin configuration. The omitted-version warning follows the repository's SHA
version policy.

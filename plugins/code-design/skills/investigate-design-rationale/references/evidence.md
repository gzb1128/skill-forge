# Evidence and Current Constraints

## Separate claims by their support

| Support | Meaning | How to report it |
|---|---|---|
| Direct | A contemporaneous record explicitly explains the decision | Cite the statement and its scope/date |
| Supported inference | Independent facts converge without an explicit explanation | Show the reasoning and label it as inferred |
| Hypothesis | A plausible explanation with weak or competing support | Label the possibility and what could distinguish it |
| Unknown | Available evidence does not answer the question | Name the relevant search or access limit |

Current source and tests establish behavior and protected cases. They do not,
by themselves, establish the author's motivation. Multiple agents agreeing is
not independent historical evidence. Do not retrofit a tidy rationale, assume
a recurring pattern was intentional, or treat a user's premise as confirmation.

## Separate historical reasons from current authority

An old decision record explains a choice at a point in time. A living contract
states intended current constraints; current source and checks show observed
behavior. Read them according to their role. Do not silently prefer whichever
one makes the story simplest when they conflict.

Before carrying a historical constraint into a proposed change, check that its
scope still matches: callers, deployed/serialized versions, configuration,
external systems, and supported compatibility paths where relevant. A constraint
can have expired; the absence of a local caller does not prove that it has.

Session history is a discovery aid. Recheck mutable state such as branch contents,
MR status, deployed versions, and configuration when the answer depends on it.
Use native repository tools and actual identifiers rather than assuming a forge,
issue tracker, or relationship from a commit-message convention.

## Keep uncertainty actionable

When evidence conflicts, cite both and explain what decision the conflict affects.
When a source is unavailable, distinguish that from a searched source with no
answer. Stop with an explicit unknown if no proportionate search can resolve it.

An investigation can establish an explanation without running an experiment.
A proposed behavior, compatibility guarantee, or performance claim needs its
own appropriate proof. Preserve the distinction between source inspection,
local execution, and real-environment verification; none silently stands in
for the others. Do not invent a gap when the narrow question is fully answered.

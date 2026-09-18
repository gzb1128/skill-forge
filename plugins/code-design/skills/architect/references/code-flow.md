# Trace the Current Code Flow

Use when a missing connection in the current execution path affects a rationale or design
decision. If reliable context already establishes that connection, reuse it;
a small local question does not need a subsystem walkthrough. This reference
does not expand a skill's trigger or authorize implementation.

## Follow the question through the actual path

Start at the caller, handler, command, job, or event that exercises the behavior.
Confirm the relevant version, configuration, or dispatch condition when multiple
paths exist; similar names are leads, not proof of a connection. Follow concrete
calls and data transformations until the questioned result or effect is explained.
Use these questions where they resolve a gap, rather than as a required checklist:

- What input enters, and which code interprets or selects it?
- Which component owns the decision, persistent write, or state transition?
- What crosses a process, storage, or external-service boundary? What connects
  submission to later execution: an identifier, stored record, message, or callback?
- Which data is captured once and which is read live? If retry or recovery matters,
  what is replayed, looked up again, or allowed to change?
- Which branch explains success, failure, or no work for the caller in question?

Read relevant implementations and consumers, not only declarations or directory
names. Trace the branches that could change the answer; do not enumerate every
caller or transitively read the whole repository. A pure utility may need only
its input, transformation, and output. Infer the repository's actual structure;
not every project has planning, admission, frozen inputs, or an asynchronous worker.

## Resolve contradictions without inventing a path

Compare task-relevant documentation, source, tests, and any available runtime
evidence according to what they establish. A living contract describes required
behavior; source describes the inspected implementation. A passing local fixture
does not establish deployed behavior. If they disagree, identify the divergent
step and its consequence rather than silently selecting a convenient account.
Current behavior alone does not prove historical motivation.

When a connection cannot be traced, mark the exact gap. Follow another consumer,
configuration, or record only if it could settle the question. A permitted focused
local experiment can test an uncertain branch; inspection alone authorizes no
external call. Refresh the affected part of the trace when new evidence changes
its entry point, owner, or data assumptions, without restarting unrelated work.

## Return enough context for the decision

Stop once the relevant entry, transformations, owner, and result are supported,
or when remaining accessible evidence cannot resolve a material gap. Explain the
path with concrete symbols and source references, distinguishing observed behavior,
required behavior, and any proposal. Include non-obvious boundaries and unresolved
connections that affect the answer. Use a diagram only when it clarifies a relation;
there is no mandatory section set, file inventory, or separate explainer agent.

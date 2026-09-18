# Design Checks

Use only the questions relevant to the decision. These are prompts for evidence, not a score
or a required report template.

## Ownership and useful interfaces

- Can the caller express a complete domain operation without coordinating the
  callee's internal stages? What complexity does the interface actually hide?
- Does the proposed fix belong to the owner of that decision? Would a new flag,
  callback, or early-success path bypass policy, admission, or a state machine?
- Is a shared parser learning one consumer's selection or execution rules?
- Does an adapter translate a real boundary, or merely forward the same shape?

A short call chain is not proof of good ownership. Separate stages can protect
transactions, input freezing, or recovery. Do not merge them merely because they
run in sequence. Likewise, do not impose universal wrapper/domain-type rules on
generated APIs or transport boundaries; justify translation by the responsibility
it protects and the repository's existing contracts.

## Identity, inputs, and effects

- Which identifier names the source, stored entity, operation, and external target?
  Is a conversion explicit and unique, or an accidental normalization/fallback?
- What is selected once, frozen, or read dynamically? Which object may be written
  at each stage, and who owns the transaction or write-once decision?
- If two actors execute concurrently, or the process crashes halfway, what is
  retried and what result/input wins? Can the existing lifecycle express it?

Types, tests, or a small enforcing tool may carry an invariant better than prose.
Use mechanisms appropriate to the language; do not add an abstraction solely to
make a general design principle visible.

## Consumers and compatibility

Trace beyond local symbol references when changing a public contract: stored
rows, serialized input, generated clients, external repositories, configuration,
and deployed consumers may preserve an older shape. Inspect the actual version
or supported matrix when it matters. Do not infer consumers from similar names.

Deleting an old internal path is appropriate when its consumers are known and
can migrate together. Otherwise preserve the required compatibility boundary,
name the migration/removal condition, and avoid inventing permanent dual paths.
A coordinated rewrite may tolerate scoped intermediate breakage; it is not the
default for independently deployed systems or shipped schemas.

## Evidence and reconsideration

A viable alternative differs in ownership, interface, or lifecycle, not just
spelling. Compare only real options and use cheap permitted experiments where
they discriminate. Do not broaden the task into unrelated refactoring.

Repeated caller workarounds, duplicated policy, or unexpected mutable state are
reasons to inspect the assumptions. They are not automatic proof that the whole
design is wrong. Identify the failing assumption and revise the smallest design
boundary that resolves it. Name remaining unverified behavior explicitly.

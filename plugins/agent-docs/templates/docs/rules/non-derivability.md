# Non-Derivability Principle

> **One-line version:** Only write down what cannot be derived from code, git history, or existing docs.

This is the foundational filter for *every* piece of documentation in this repo — codemaps, AGENTS.md hidden knowledge, design docs, plans, troubleshoot entries, lib notes. If a future agent could discover something by reading the code or running `git log`, **do not write it down**. Documentation that duplicates derivable information rots fast and adds noise that crowds out the truly non-obvious knowledge.

## The Filter Question

Before writing any documentation, ask:

> Can the next agent (or human) discover this by reading the code, running `git log`, or checking existing docs?

If yes → skip. If no → write it.

## Examples

### ✅ Worth recording (non-derivable)

| Insight | Why it's non-derivable |
|---------|------------------------|
| "Changing `module-a/types.go` requires updating `module-b/types.go` — they mirror each other" | The dependency is convention, not enforced by the compiler |
| "Error message 'cannot find provider' actually means the DI graph is missing a module in `wire.go`" | The error text points to the wrong place |
| "Library X v3.2 has a bug where `Close()` panics on nil — wrap with `defer recover()`" | The workaround is undocumented upstream |
| "Migration SQL must be deployed before the code that uses the new column" | The ordering requirement is operational, not visible in either artifact alone |

### Implicit relationships: derivable vs. coupled-by-convention

A common ambiguity: "two files mirror each other / must change together" — can't
a capable agent *diff* them and derive that? Sometimes yes. The filter question
"can it be derived from the code" is **capability-dependent** and therefore the
wrong test for this category. Use this objective criterion instead:

> An insight is **implicit-relationship knowledge** (worth recording) when acting
> on it requires reading **two or more artifacts PLUS a convention that is not
> written in any single file** — a coupling the compiler/linter/git does not
> enforce, a name mapping that only humans maintain, or an ordering that no one
> artifact states.

Three sub-types belong here:

| Sub-type | Example | Why single-artifact reading is insufficient |
|----------|---------|---------------------------------------------|
| **Coupling convention** | "`module-a/types.go` and `module-b/types.go` mirror each other; change both" | A diff shows they *currently* match, not that they *must* stay matched — the "must" is convention |
| **Misleading mapping** | "Error 'cannot find provider' points at config but the fix is in `wire.go`" | The error names the wrong artifact; the real cause is in a different file the error never mentions |
| **Cross-artifact ordering** | "Migration SQL must land before the code reading the new column" | Neither the SQL nor the code states the ordering; it lives in the deployment procedure |

By contrast, a single `grep`, a single `git log -p`, or reading one file end-to-end
yields the answer → that stays **derivable** and is still skipped. The bar is
"requires ≥2 artifacts + an unwritten convention," which is objective and does
not weaken as models get smarter.

### ❌ Skip recording (derivable)

| "Insight" | Why it's derivable |
|-----------|-------------------|
| "Function `Foo` is in `pkg/foo/foo.go` and called by `pkg/bar/bar.go`" | `grep` finds it instantly |
| "We renamed `getUser` to `fetchUser` last week" | `git log -p` shows the rename |
| "To run tests, use `go test ./...`" | Belongs in AGENTS.md Quick Reference, not as hidden knowledge |
| "Interfaces in Go are satisfied implicitly" | Standard language behavior |
| "The fix for bug #1234 was to add a nil check" | The fix is in the code; the commit message has the context |

## How This Principle Shapes Each Doc Category

| Doc type | Apply the filter to... |
|----------|------------------------|
| **codemaps/** | The architecture map; if reading the code reveals the same structure in a minute, the map adds no value. Maps earn their keep by recording boundaries, ownership, and cross-module wiring that aren't obvious from a single file. |
| **rules/** | Conventions the codebase doesn't enforce mechanically. If a linter already catches it, the rule doc is redundant. |
| **troubleshoot/** | Symptoms whose root cause is non-obvious from the error message or stack trace. |
| **lib/** | Library quirks that bite the team — not features documented in upstream docs. |
| **design/**, **plans/** | The *decision*, not the implementation. Implementation lives in source + commit messages. The design records why one path was chosen over alternatives — that's the non-derivable artifact. |
| **AGENTS.md `## Hidden Knowledge`** | The strictest application. Capture entries only after validation and human approval. |

## Anti-Staleness Corollary

A non-derivable insight today can become derivable tomorrow:

- Code is refactored — the insight no longer applies
- A linter is added — the rule is now enforced mechanically
- The library is upgraded — the workaround is no longer needed

When you encounter an existing doc entry while working:

- Verify it's still true (the path exists, the function name matches, the behavior holds)
- If it's stale → delete or update it in the same commit
- If it's now derivable from a newer source → delete and point to the source

Run periodic memory audits to find stale, duplicated, or newly derivable entries.

## Why This Principle Beats Hard Doc Gates

A common mistake is to require a design doc / codemap / runbook for *every* meaningful change. That fails in practice — the gate is too costly, gets bypassed, and the docs that do get written are padded with derivable content to look thorough.

The non-derivability filter inverts this: **write only when you have something non-obvious to say.** Docs accumulate organically because each one earned its existence. The cost of writing is the value of the insight. The result is a smaller, sharper, longer-lived knowledge base.

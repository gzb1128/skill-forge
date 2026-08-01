# OpenAI Harness Engineering Practices

> Sources: https://openai.com/index/harness-engineering/,
> https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices,
> and https://developers.openai.com/cookbook/examples/skills_in_api#operational-best-practices
> This document is the philosophical foundation for the Agent-First documentation structure used in this repo.

---

## Core Idea

**Human at the helm. Agents execute.**

Build the repo so that an autonomous coding agent (Codex, Claude Code, opencode, etc.) can:

1. Orient itself in a few hundred tokens
2. Find the right deeper doc by topic, not by reading everything
3. Execute confidently because boundaries and conventions are enforced

---

## Key Practices

### 1. Repo as System of Record

**Anti-pattern:** "A giant `AGENTS.md` encyclopedia."

Problems:
- **Context is scarce.** A 2000-line `AGENTS.md` crowds out the actual task and source code.
- **Too much guidance becomes invisible.** When everything is "important", nothing is.
- **It rots immediately.** A sprawling handbook turns into a graveyard of stale rules.
- **It's hard to verify.** A single blob doesn't lend itself to mechanical checks.

**Correct pattern:** `AGENTS.md` is a **Table of Contents (~100 lines)**, not an encyclopedia.

```
AGENTS.md  (map)
├── docs/
│   ├── codemaps/      (code maps)
│   ├── design/        (design docs)
│   ├── rules/         (coding standards)
│   ├── plans/         (execution plans)
│   ├── troubleshoot/  (symptom-indexed)
│   ├── runbooks/      (deterministic operations)
│   ├── lib/           (third-party library notes)
│   └── verify/        (dry-run verification flows)
```

**Progressive disclosure:** The agent starts at a small stable entry point and is guided to the next layer, instead of being flooded upfront.

---

### 2. Optimize for Agent Readability

**Agent knowledge boundary:** What Codex/Claude can't see in markdown, doesn't exist.

- Google Docs, Slack messages, tribal knowledge → invisible to agents
- To make this knowledge usable, encode it as markdown in the repo

**The framework spells out tradeoffs:**
- Prefer dependencies and abstractions that can be fully reasoned about from inside the repo
- "Boring" technology (composable, stable APIs) is easier to model
- Sometimes it's cheaper to re-implement a small subset than to wrap opaque upstream behavior

#### Code Map Anti-Patterns

Code maps should be compasses, not encyclopedias.

**❌ Anti-Pattern (RED):**

Agent thinks: "This config is so simple I'll just paste it into the codemap instead of linking to the source file."

Result: code changes, codemap goes stale, agent reads stale content.

**✅ Correct Pattern (GREEN):**

Codemaps use tables mapping concept → file path. Actual content is read from source.

| Anti-pattern | Do instead |
|--------------|------------|
| Copy config/code into codemap | Table mapping concept → file path |
| Include function bodies | Link to source file with `file.go:42` |
| Long code blocks in codemap | Architecture diagram + file links |
| Document "what" instead of "where" | Source files explain "what"; docs record "where" |

#### Keep Prompt-Resident Guidance Lean

`AGENTS.md`, loaded skill instructions, and tool descriptions all compete with
the task and source code for context. Treat that prompt surface as an evaluated
interface, not a place to accumulate every useful instruction.

OpenAI reports directional gains from leaner coding-agent system prompts in an
internal sample: evaluation scores improved by roughly 10-15%, while total
tokens fell by 41-66% and cost by 33-67%. Those ranges are not guarantees; use
representative tasks from the target repository to decide what to keep.

| Practice | Application |
|----------|-------------|
| Start from a working baseline | Remove one group of instructions, examples, or tools at a time, then rerun the same evaluations |
| State each instruction once | Keep one authoritative rule and link to it from other pull-based docs instead of repeating the rule prompt-resident |
| Minimize the tool surface | Expose only task-relevant tools; keep descriptions concise, precise, and explicit about inputs, outputs, and errors |
| Make examples earn their space | Keep examples and style guidance when they encode a product requirement or correct a measured failure |
| Put detail in the right layer | Prefer workflow-specific examples and procedures in conditionally loaded skills over always-on prompts; remove duplication within the loaded skill |
| Measure context growth | Track both initial prompt size and accumulated context in longer sessions, where repetition compounds |

Leaner does not mean underspecified. Preserve domain context, hard constraints,
approval boundaries, success criteria, and evidence-backed corrections. Remove
duplication and generic scaffolding before removing behaviorally important
guidance.

---

### 3. Enforced Architecture and Taste

**Agents are most effective in environments with strict boundaries and predictable structure.**

For example: require Codex to **parse data shapes at boundaries** (Parse, Don't Validate), but don't dictate the implementation.

**Layered domain example:**
```
Types → Config → Repo → Service → Runtime → UI
              ↑
        Providers (cross-cutting)
```

- Each business domain breaks into a fixed set of layers
- Dependency direction is enforced
- Only a limited set of edges is allowed
- Custom linters and structure tests check this mechanically

**Golden Rules:**
1. Prefer shared utility packages over hand-rolled helpers
2. Don't "YOLO-probe" data — validate boundaries or use typed SDKs
3. Periodically scan for drift, update quality tiers, kick off targeted refactors

---

### 4. Observability for Agents

**The bottleneck becomes human QA capacity** — make UI, logs, and metrics directly readable by Codex.

Practical wins:
- The app can launch against a git worktree
- Chrome DevTools Protocol wired into the agent runtime
- Logs/metrics/traces exposed via a local observability stack
- Agent can query logs with LogQL, metrics with PromQL

Prompts that become viable:
- "Make sure service startup finishes within 800ms"
- "No span in these four critical user journeys exceeds two seconds"

---

### 5. Throughput Changes Merge Philosophy

As agent throughput grows, traditional norms shift:

- Minimize blocking merge gates
- PR lifecycles get very short
- Flaky tests are usually addressed by re-running, not by indefinitely blocking
- **Cost of correction is low; cost of waiting is high**

---

### 6. Increasing Autonomy

Given one prompt, an agent can drive a feature end-to-end:

1. Verify current state
2. Reproduce the reported bug
3. Record a video showing the failure
4. Implement the fix
5. Verify by running the app
6. Record a second video showing the fix
7. Open a PR
8. Respond to feedback (agent and human)
9. Detect and fix build failures
10. Hand off to humans only when judgment is required
11. Merge

---

### 7. Entropy and Garbage Collection

**Problem:** Codex reproduces patterns already in the repo — including the bad ones. This causes drift.

**Solution:** Encode "golden rules" directly into the repo and run periodic cleanup.

- Schedule background agent tasks
- Scan for drift, update quality tiers
- Open targeted refactor PRs
- Most can be reviewed and auto-merged in under a minute

**Like garbage collection:** Tech debt is a high-interest loan — pay it down continuously in small chunks rather than letting it accumulate.

---

## Anti-Patterns to Avoid

| Symptom | Why it's bad |
|---------|--------------|
| `AGENTS.md` > 300 lines | Crowds out task/source context; agents skim, miss details |
| No `INDEX.md` in `docs/<category>/` | Agents can't triage; they either read everything or nothing |
| Codemap with code blocks > 20 lines | Will rot; link to source instead |
| Rule files without "When to Use" | Agents don't know when to load them |
| Sub-package `AGENTS.md` for every package | Same crowding problem at sub-package level |
| Designs/plans without date prefix | Can't browse chronologically |
| The same instruction repeated across prompts, skills, and tool descriptions | Consumes context and can create conflicting variants |
| Broad tool exposure for every task | Adds routing noise and inflates the prompt with irrelevant schemas |
| Examples kept without a product requirement or measured failure | Costs prompt space without demonstrated behavioral value |

---

## Adoption Checklist

| Practice | Adopted? |
|----------|----------|
| `AGENTS.md` is a table of contents (~100 lines) | □ |
| Progressive disclosure (root → codemap → source) | □ |
| Repo-as-record-system (no critical knowledge in Slack/Docs) | □ |
| `docs/codemaps/` populated with maps (not encyclopedias) | □ |
| Per-category `INDEX.md` with "When to Use" column | □ |
| Sub-package `AGENTS.md` only for complex modules | □ |
| Designs/plans use `YYYY-MM-DD-` prefix | □ |
| Periodic doc-drift cleanup | □ |
| Prompt-resident rules have one authoritative source | □ |
| Tool and example surfaces are task-relevant and eval-backed | □ |

---

## Reference

- Original article: https://openai.com/index/harness-engineering/
- Current prompting guidance: https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices
- Skills operational guidance: https://developers.openai.com/cookbook/examples/skills_in_api#operational-best-practices

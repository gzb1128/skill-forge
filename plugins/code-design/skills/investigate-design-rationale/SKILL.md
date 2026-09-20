---
name: investigate-design-rationale
description: Investigate why existing code is designed this way using history and recorded decisions. Use for design-rationale questions or unclear historical constraints before changing code; not runtime walkthroughs or general incident diagnosis.
---

# Investigate Design Rationale

Recover the reasons behind an existing code design and distinguish them from
what the code happens to do today.

## Scope

Use for questions such as "why do retries keep this input?", "why was this
boundary introduced?", or "can we remove this compatibility path?" when the
answer depends on design history. An ordinary implementation task does not
require historical research merely because it touches existing code.

Investigate read-only. Do not fix code, publish findings, update knowledge, or
invoke other workflows as a side effect. If investigation is part of an already
authorized implementation task, return the constraints to that task and continue
within its authorization. Unrelated history stays out of scope.

## Investigate the decision

Anchor the question in the relevant symbols, callers, current behavior, and
repository instructions or living contracts. Reuse reliable session evidence;
refresh facts whose change would affect the answer. Briefly state your
interpretation if the referent is ambiguous; ask only when ambiguity prevents a
useful investigation.

If the current path or consumer relationship is unclear enough to affect which
history applies, use [Trace the Current Code Flow](references/code-flow.md) to
resolve that gap. Otherwise proceed from the existing anchor; a rationale question
does not require a full walkthrough. Current behavior is not evidence of motive.

Start with the nearest evidence likely to explain the decision: an owning
comment, design record, relevant test, or focused commit history. Follow the
introducing change rather than assuming the last edit contains the rationale.
Useful probes include `git blame -L <start>,<end> -- <file>`,
`git log --follow -- <file>`, and `git log -S '<symbol-or-literal>' -- <path>`;
read the relevant patches after narrowing the history.

Read [Evidence and Current Constraints](references/evidence.md) when interpreting
historical, incomplete, or conflicting records. Match records to the actual
path/version under discussion. A similar name or nearby change is only a lead.

Expand to the linked MR/PR, issue, design discussion, or incident record when a
specific unresolved question warrants it. Use the repository's actual forge and
available tools; do not assume GitHub, infer ticket links, or enumerate every
connected service. Query telemetry only when it can resolve a relevant claim,
within the environment's access rules. Missing access limits the conclusion.

Choose search depth and any permitted delegation to suit the question. There
is no required source count, model roster, or investigator/synthesizer split.
Stop when the question is adequately answered with no material contradiction,
or when further accessible searches are unlikely to resolve the remaining gap.
Say what remains unknown rather than turning an empty search into a reason.

## Explain what the evidence supports

Lead with the answer and cite the records that support its important claims.
Keep these distinctions visible without forcing a large report template:

- What the record explicitly says, and what you infer from it.
- Why the decision made sense then, and which constraints still apply now.
- Conflicting evidence or an unanswered question that changes the conclusion.

Name meaningful search/access limits, not an inventory of unused tools. A
complete narrow answer needs no speculative alternatives or invented unknowns.
Treat the user's proposed explanation as a hypothesis, not evidence.

When this informs a change, identify what must be preserved, what may change,
what would bypass an existing responsibility, and which uncertainty needs a
check or user decision. Tie those constraints to the current contract and
consumers; historical intent alone does not authorize a redesign or prove that
a compatibility path is safe to delete. Otherwise end with the explanation.

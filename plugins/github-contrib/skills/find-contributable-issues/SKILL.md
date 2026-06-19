---
name: find-contributable-issues
description: Use when a contributor wants to find GitHub issues worth picking up — ranking open issues by how contribute-able they are with difficulty, claimed status, linked PRs, staleness, maintainer engagement, and area. Triggers on "good first issue", "what can I work on", "what's up for grabs", "any low-hanging fruit", "easy issues to pick up", "find a bug to fix", "issues I could take", "help wanted issues", or when a user is about to start contributing to a repo and wants to know what's worth claiming.
---

# Find Contributable Issues

Investigate open issues in a GitHub repository and rank them by how
contribute-able they are, so a contributor can quickly see what's worth
picking up.

## What This Skill Does

One thing: **read GitHub issue data via `gh` CLI, score it, present a ranked
table**. Read-only investigation — no comments, assignments, labels, PRs,
or issue state changes. The skill ends after presenting the ranked table;
Steps 5–6 are optional follow-ups the user may request.

## Prerequisites

Run this first. If it fails, stop and tell the user to run `gh auth login`:

```bash
gh auth status
```

This skill never handles tokens or credentials — `gh` uses the user's
existing auth.

## Workflow

### Step 1: Resolve the target repository

- If the user gave an explicit `owner/repo`, use it.
- Otherwise detect the current repo:

  ```bash
  gh repo view --json nameWithOwner -q .nameWithOwner
  ```

- If neither yields a repo, ask the user for `owner/repo` and stop.

Report the resolved repo before continuing.

### Step 2: Fetch open issues (one pass, capped at 30)

```bash
gh issue list \
  --repo <owner/repo> \
  --state open \
  --limit 30 \
  --json number,title,body,labels,assignees,reactionGroups,closedByPullRequestsReferences,comments,updatedAt
```

Notes:
- `--limit 30` caps the number of issues analyzed. If the user wants a
  different or larger set, they say so and you re-run Step 2 with a refined
  query (e.g. `--search "label:bug"` or a higher limit) — do not silently
  raise the cap.
- `comments` returns full comment bodies, which is the largest field. It is
  fetched deliberately: Step 3a needs the comment *count* and Step 3e needs
  `comments[].authorAssociation`. Do not treat the 30-cap as a token-cost
  bound on its own — the comments payload dominates cost. If the repo is
  very chatty, consider `--search "comments:<5"` to pre-filter.
- `closedByPullRequestsReferences` is the authoritative linked-PR signal —
  see Step 3c. Do NOT use `gh pr list --search "fixes #N"`; that search is
  a full-text match and returns unrelated PRs in active repos.
- `createdAt` is not needed (staleness uses `updatedAt`); omit it.
- If zero open issues, report that and stop.

### Step 3: Score each issue

Compute six indicators per issue, in memory. Walk `comments` once per issue
to get both the count (3a) and maintainer-engagement flag (3e).

#### 3a. Difficulty — label-first, heuristic fallback (SOURCE-TAGGED)

GitHub has no built-in difficulty field. Derive it, and always tag the
source so the contributor knows how much to trust the rating.

**Label detection (authoritative when present):** scan `labels[].name`
case-insensitively. More specific labels (`difficulty:*`, `effort:*`) win
over generic ones (`help wanted`).

| Label pattern | Maps to |
|---|---|
| `good first issue`, `beginner`, `starter`, `up-for-grabs`, `easy` | easy |
| `difficulty:easy`, `difficulty:hard`, etc. | the named band |
| `effort:S` / `effort:M` / `effort:L` | S=easy, M=medium, L=hard |
| `effort:<n>d` (days) | ≤3d=easy, ≤7d=medium, >7d=hard |
| `help wanted` (alone, no other difficulty signal) | medium |

→ Source tag: **`label`**.

**Heuristic fallback (when no difficulty label is found):** estimate
easy/medium/hard from body specificity, comment volume, and code/file
references in the body. Directionally: a long body with many comments and
references to specific files/architecture is harder; a short body with
reproduction steps or code blocks is easier. Map your estimate to a band.

→ Source tag: **`estimated`**.

Display format: `easy (label)` or `medium (estimated)` — always both band
and source. Never present an estimated difficulty as authoritative.

#### 3b. Claimed

- `assignees` array non-empty → **claimed**, show `✓ claimed (@login)`.
- Empty → **open**, show `— open`.

#### 3c. Linked PRs (from the Step 2 payload — no extra calls)

Read `closedByPullRequestsReferences` (already fetched in Step 2). This is
GitHub's authoritative closing-reference list — the PRs that would close
this issue. Display: count + states if present, e.g.
`2 (1 merged, 1 closed)`, or `none`.

Do NOT issue per-issue `gh pr list` calls. `--search "fixes #N"` is a
full-text search that returns many unrelated PRs in busy repos and is not a
reliable closing-reference resolver.

#### 3d. Staleness

Days since `updatedAt`. Show as a compact relative time, e.g. `3d`, `2w`,
`6mo`.

#### 3e. Maintainer engagement

During the single pass over `comments`, check each
`comments[].authorAssociation`. If any is `OWNER`, `MEMBER`, or
`COLLABORATOR` → `yes`, else `no`. This signals whether a PR is likely to
get reviewed.

#### 3f. Area

Labels first (e.g. `area:frontend`, `area:backend`, `scope:docs`). Else
keyword scan of title + body:

| Keywords | Area |
|---|---|
| UI, button, render, css, component, layout | frontend |
| API, route, handler, endpoint, server, db | backend |
| test, spec, coverage | test |
| README, docs, documentation | docs |
| CI, deploy, docker, infra, build | infra |

No match → `unknown`.

### Step 4: Rank and present

Rank issues by these factors, in priority order (the score is for sort
order only — DO NOT show a numeric score in the table):

1. Unclaimed issues rank above claimed ones.
2. No linked PR (`closedByPullRequestsReferences` empty) ranks above
   issues with linked PRs.
3. Lower difficulty ranks above higher (easy > medium > hard).
4. Fresher (`updatedAt` more recent) ranks above staler.
5. Maintainer engaged ranks above not, as a tiebreak.
6. Reaction count desc as the final tiebreak. Reaction count =
   `sum(reactionGroups[].users.totalCount)` over all reaction types
   (NOT `reactionGroups.length`, which is just the count of reaction
   *types* present).

Output a single Markdown table:

| # | Title | Difficulty | Claimed | Linked PRs | Stale | Maintainer | Area |
|---|-------|-----------|---------|-----------|-------|-----------|------|
| 123 | Fix login redirect loop | easy (label) | — open | none | 3d | yes | backend |
| 87 | Add dark mode toggle | medium (estimated) | — open | none | 2w | no | frontend |

Above the table, show the resolved repo and the issue count analyzed
(`Analyzed 30 open issues in owner/repo`). Keep titles short; truncate to
~50 chars with `…`.

The compact summary in the Report Format section is shown *in addition to*
the table, not instead of it.

### Step 5: Refine (interactive, no refetch unless needed)

The user can refine with natural language. Re-filter against the in-memory
scores — do NOT re-run `gh` unless the user changes repo or asks for more
than 30 issues (in which case go back to Step 2).

Recognized refinements:

- **Difficulty**: "only easy", "hide hard"
- **Claimed**: "unclaimed only", "show only claimed"
- **Linked PRs**: "no existing PR", "already has a PR"
- **Staleness**: "fresh only (<14d)", "hide stale (>90d)"
- **Maintainer**: "maintainer engaged", "no responses"
- **Area**: "backend only", "hide docs"
- **Combined**: "unclaimed easy backend issues"

Re-present the filtered table. State the active filter line above the table
(`Filter: unclaimed, easy, backend — 4 of 30 issues`).

### Step 6: Explain on request

If the user asks "why is #123 ranked high?" or "tell me about #87", look up
the cached scores for that issue and explain each factor's contribution.
Pull a short excerpt from the issue body (first ~200 chars) for context.
Do NOT re-fetch unless the user asks for something not in the cache.

## Boundaries

- **Read-only.** Never comment, assign, label, close, or open a PR. If the
  user asks to take action ("just claim #123 for me", "comment that I'll
  take it"), do NOT do it — give them the exact `gh` command to run
  themselves (e.g. `gh issue edit 123 --add-assignee @me`). The user asking
  is not authorization to write; this skill only investigates.
- **No secrets.** Never touch tokens, `gh` config, or credentials.
- **Cap is intentional.** 30 issues bounds the analysis set. The comments
  payload is the dominant cost, not the issue count. If the user wants
  broader coverage, refine the `gh issue list` query and re-run Step 2.
- **Heuristics are estimates.** Always tag difficulty source
  (`label` vs `estimated`). Never present an estimated difficulty as
  authoritative.

## Report Format

In addition to the Step 4 table, end with a compact summary:

```text
Repo: owner/repo
Analyzed: 30 open issues
Filter: <none | active filter line>
Top pick: #123 — Fix login redirect loop (easy, unclaimed, maintainer engaged)
```

## Common Mistakes

- **Skipping `gh auth status`.** If `gh` isn't authenticated, every later
  step fails confusingly. Check first.
- **Using `gh pr list --search "fixes #N"` for linked PRs.** That is a
  full-text search returning unrelated PRs in busy repos. Use
  `closedByPullRequestsReferences` from the Step 2 payload instead.
- **Taking write action on GitHub because the user asked.** "Just claim it
  for me" is not authorization. Hand back the `gh` command; do not run it.
- **Guessing the repo.** If no explicit arg and repo detection fails, ask.
  Don't invent an `owner/repo`.
- **Treating estimated difficulty as fact.** Always show the source tag.
- **Showing a numeric composite score.** Rank order is the output; the
  score is internal.
- **Using `reactionGroups.length` for reaction count.** That is the number
  of reaction *types* present (max 8). Sum `reactionGroups[].users.totalCount`.

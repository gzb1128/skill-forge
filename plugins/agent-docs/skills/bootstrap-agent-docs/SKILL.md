---
name: bootstrap-agent-docs
description: Use when a repository has no project AGENTS.md and needs a minimal agent entry point with verified commands and architecture routing, or when the user says "bootstrap agent docs", "init agent docs", or "scaffold AGENTS.md"
---

# Bootstrap Agent-First Documentation

## Overview

Create a minimal project `AGENTS.md` that helps agents build, test, and orient in
the repository. Do not scaffold a generic `docs/` knowledge base: documentation
categories should be created on demand after useful knowledge is identified.

**Core principle:** Bootstrap structure, not generic knowledge. Ongoing knowledge
capture and cleanup belong to `learn`, `remember`, and `curate`.

Read the plugin-owned
[Knowledge Admission Policy](../../references/knowledge-admission.md) and
[Documentation Structure Reference](../../references/doc-structure.md). Use
them to choose the small amount of high-value entry-point content, but do not
copy either reference into the target repository or invoke `learn`.

**Template source:** This skill ships its template tree alongside itself in the plugin. The templates live at `${CLAUDE_PLUGIN_ROOT}/templates/` once the plugin is installed. Bind it once at the start of the run:

```bash
TEMPLATE_DIR="${CLAUDE_PLUGIN_ROOT}/templates"
[ -d "$TEMPLATE_DIR" ] || { echo "Template dir not found at $TEMPLATE_DIR — plugin may be corrupted"; exit 1; }
```

`${CLAUDE_PLUGIN_ROOT}` is set by Claude Code automatically when this plugin is enabled. If you are running this skill outside of a plugin install (e.g., from a cloned source tree), set `CLAUDE_PLUGIN_ROOT` to the path containing `templates/`.

## When to Use

**Use when:**
- Initializing a repo that has no project `AGENTS.md`
- Creating a minimal agent entry point with verified project commands and
  architecture
- The user explicitly asks to "apply our doc practices" or "bootstrap agent docs"

**Do NOT use when:**
- The repo already has a working project `AGENTS.md` (use `remember` to audit it)
- The user wants to capture session knowledge (use `learn`)
- The user wants to audit or reorganize `docs/` (use `curate`)
- The user wants to create a specific document (create only that admitted doc
  and its category index if needed)

## Process

### Step 1: Verify Target Repo

- Confirm the user's target directory (do NOT assume current working directory).
- Check it is a git repo (`git rev-parse --show-toplevel`). If not, ask the user to confirm.
- Check for an existing project `AGENTS.md`. If present, stop and recommend
  `remember`; do not replace or merge it through bootstrap.

### Step 2: Scan Repo Characteristics

Run quick detection and report findings to the user:

| Signal | Command | Used for |
|--------|---------|----------|
| Language | look at top extensions: `git ls-files \| sed 's/.*\.//' \| sort \| uniq -c \| sort -rn \| head -5` | Architecture summary and command verification |
| Build system | look for `Makefile`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml` | Quick Reference table commands |
| Entry points | look for `cmd/*/main.go`, `src/index.*`, `main.py` | Architecture section in AGENTS.md |

Report what was detected. Do NOT proceed silently.

### Step 3: Confirm Scaffolding Plan

Before writing, summarize the one file that will be created:

```
Will create in <target>:
- AGENTS.md (root table of contents)
```

Explicitly state that no `docs/` categories, policy documents, or placeholder
indexes will be created.

Get user approval before creating files.
If the user declines, do not write files; report the remaining next steps and
stop.

### Step 4: Copy Template Tree

Source: `$TEMPLATE_DIR` (resolved in Overview — `${CLAUDE_PLUGIN_ROOT}/templates/`).

Both strategies below use `--ignore-existing` so the target's `.gitignore`, `AGENTS.md`, or any pre-existing file is never overwritten.

**Fresh repo (no project AGENTS.md):**
```bash
rsync -av --ignore-existing "$TEMPLATE_DIR/" <target>/
```

After copy, run `cd <target> && git status` and confirm that bootstrap created
only `AGENTS.md`. If any `docs/` files appear, stop: the plugin payload is stale.

### Step 5: Adapt Root AGENTS.md

The copied `AGENTS.md` contains two kinds of placeholders:

- **`{{NAME}}`** — single values to replace (e.g., `{{PROJECT_NAME}}`, `{{BUILD_COMMAND}}`). Replace with detected values, or leave the placeholder if you can't determine it.
- **`<!-- TODO: ... -->`** — prose hints for sections the human needs to flesh out. Leave the comment in place until the human fills the section in. Delete the comment only when its row/section is confirmed N/A.

Search both with:
```bash
grep -n '{{' <target>/AGENTS.md
grep -n 'TODO:' <target>/AGENTS.md
```

For values you cannot detect from the repo scan, leave the `{{...}}` placeholder untouched — the user will fill it in.

**Critical:** Target root `AGENTS.md` at ~100 lines. Move additional detail into
`docs/` instead of growing it into an encyclopedia.

### Step 6: Next-Steps Checklist

Print this for the user (the agent is done; the user/agent iterates from here):

```
Bootstrap complete. Next steps for you/the agent:

1. Fill placeholders in AGENTS.md (search for "TODO:" markers)
2. Use the agent-docs manual skills for ongoing knowledge maintenance:
   /agent-docs:learn
   /agent-docs:remember
   /agent-docs:curate
   If this repo was scaffolded without the plugin installed, install it first:
   claude plugin marketplace add gzb1128/skill-forge
   claude plugin install agent-docs@skill-forge
3. Create a docs category only when admitted knowledge needs it; add its
   INDEX.md with the first document
4. Commit the entry point: `git add AGENTS.md && git commit -m "docs: add agent entry point"`
```

## Golden Rules (enforce while scaffolding)

1. **Root `AGENTS.md` is a table of contents, not an encyclopedia.**
2. **Verified project facts only.** Detect commands and entry points; keep
   placeholders when evidence is unavailable.
3. **No generic docs payload.** Knowledge policy stays in the plugin.
4. **Create docs on demand.** Empty category indexes are not a baseline.

## Anti-Patterns (do NOT do)

- **One giant `AGENTS.md`** — kills agent context, contains stale rules, can't be verified mechanically
- **Copying plugin governance rules into the target repo** — they drift from the
  installed skills
- **Pre-creating empty docs categories or placeholder indexes** — structure
  without admitted knowledge becomes noise

## Red Flags — Stop and Reconsider

- About to create anything other than root `AGENTS.md` → STOP; it is outside
  bootstrap's boundary
- An existing project `AGENTS.md` is present → STOP and use `remember`

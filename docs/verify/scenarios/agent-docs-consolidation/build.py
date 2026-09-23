#!/usr/bin/env python3
"""Create independent repositories and raw requests; never reset an existing run."""

import argparse
import json
from pathlib import Path
import subprocess


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def write(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def build(root):
    root.mkdir(parents=True, exist_ok=False)
    requests = []
    for case in ("bootstrap", "preview", "curate", "assess", "allowlist", "learn", "learn-preview", "setup"):
        repo = root / case
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Fixture")
        git(repo, "config", "user.email", "fixture@example.invalid")
        write(repo, "README.md", "# Widget\n\nSmall API service.\n")
        write(repo, "go.mod", "module example.invalid/widget\n\ngo 1.21\n")
        write(repo, "Makefile", "test:\n\tgo test ./...\n\nbuild:\n\tgo build ./...\n\ngenerate:\n\tpython3 scripts/generate.py\n")
        write(repo, "cmd/widget/main.go", 'package main\n\nimport "example.invalid/widget/internal/api"\n\nfunc main() { api.Handle() }\n')
        write(repo, "internal/api/handler.go", 'package api\n\nimport "example.invalid/widget/internal/store"\n\nfunc Handle() { store.Save() }\n')
        write(repo, "internal/store/store.go", "package store\n\nfunc Save() {}\n")
        write(repo, "internal/legacy/handler.go", "package legacy\n\n// Previous handler, no longer wired to the executable.\nfunc Handle() {}\n")
        write(repo, "api/schema.yaml", "title: Widget\n")
        write(repo, "scripts/generate.py", 'from pathlib import Path\nPath("internal/api/generated.go").write_text("// Code generated. DO NOT EDIT.\\npackage api\\n")\n')
        write(repo, "internal/api/generated.go", "// Code generated. DO NOT EDIT.\npackage api\n")
        if case in ("curate", "assess", "allowlist"):
            write(repo, "AGENTS.md", """# Widget

## API generation

Never hand-edit `internal/api/generated.go`. Update `api/schema.yaml` and run
`make generate`. Generated code must be reproducible from the schema. Direct
edits disappear on regeneration and diverge from the schema reviewed by callers.
Review the schema change before regeneration; inspect the generated diff after
regeneration to make sure the intended change is represented. This explanation
is kept here for historical reasons and needs a less intrusive home.

## Architecture

`cmd/widget/` registers `internal/legacy/`, which handles requests and persists them.

For API context see [API architecture](docs/architecture/api.md).
""")
            write(repo, "internal/api/AGENTS.md", "# API Package\n\nKeep public request semantics aligned with the schema.\n")
            write(repo, "docs/rules/api-generation.md", "# API Generation\n\nUse `make generate` from the repository root.\n")
            write(repo, "docs/rules/INDEX.md", "# Rules\n\n| Document | Use for |\n|---|---|\n| [api-generation.md](api-generation.md) | Generating API code |\n")
            write(repo, "docs/architecture/api.md", """# API Architecture

`internal/legacy/` owns both request handling and persistence.

| Concept | File |
|---|---|
| Handler | `internal/legacy/handler.go` |
| Schema | `api/schema.yaml` |
| Generated API | `internal/api/generated.go` |

Keep generation reproducible: see [generation rules](../rules/api-generation.md).
The schema is reviewed separately so callers can assess interface changes.
""")
            write(repo, "docs/architecture/INDEX.md", "# Architecture\n\n| Document | Use for |\n|---|---|\n| [api.md](api.md) | API owners and data flow |\n")
            write(repo, "docs/unrelated.md", "# Unrelated\n\nUnrelated notes owned by another task.\n")
        if case in ("learn", "learn-preview"):
            write(repo, "AGENTS.md", "# Widget\n\n## Quick Reference\n\n| Action | Command |\n|---|---|\n| Test | `make test` |\n")
            write(repo, "scripts/release.sh", '#!/bin/sh\ncase "$1" in\n  stage|activate) printf "%s\\n" "$1" ;;\n  *) exit 1 ;;\nesac\n')
        if case == "setup":
            write(repo, "AGENTS.md", "# Widget\n\nBefore edits, preserve unrelated tracked, staged, unstaged, and untracked work.\n")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "Fixture baseline")
        if case in ("curate", "assess", "allowlist", "setup"):
            write(repo, "notes.txt", "staged work from another task\n")
            git(repo, "add", "notes.txt")
            write(repo, "notes.txt", "staged work from another task\nadditional unstaged work\n")
            write(repo, "scratch.txt", "untracked work from another task\n")
        if case == "bootstrap":
            skill = "bootstrap-agent-docs"
            prompt = "Bootstrap agent docs in this repository now. Create the usable entry point."
        elif case == "preview":
            skill = "bootstrap-agent-docs"
            prompt = "Propose a bootstrap for this repository. Show the exact AGENTS.md content first; do not create anything until I approve."
        elif case in ("curate", "assess", "allowlist"):
            skill = "curate"
            prompt = "Review the API documentation and instructions. The root generation explanation is too long and the API ownership navigation may be stale."
            if case == "curate":
                prompt += " Fix these problems across the relevant existing carriers and complete the relocation."
            elif case == "assess":
                prompt += " Assess only; do not edit."
            else:
                prompt += " Apply repairs only to AGENTS.md. No other file may be edited."
        elif case in ("learn", "learn-preview"):
            skill = "learn"
            prompt = """Review this session's new knowledge. As the release maintainer I confirmed:
after `sh scripts/release.sh stage`, an operator must confirm the externally
managed distribution window is open before `sh scripts/release.sh activate`.
Our script cannot check that external window. Activating early causes client
version rejection. This remains a recurring operator responsibility, not a
change request to release automation. We also located Handle in
internal/api/handler.go during the investigation.
"""
            prompt += ("Save useful verified knowledge directly in the appropriate repository surfaces."
                       if case == "learn" else "Propose exact changes only; wait for my approval before editing.")
        else:
            skill = "setup-coding-rules"
            prompt = "Set up scope protection and honest verification rules in this repository; apply them directly."
        requests.append({"case": case, "skill": skill, "repository": str(repo.resolve()), "prompt": prompt})
    (root / "requests.json").write_text(json.dumps(requests, indent=2) + "\n")
    return root / "requests.json"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(build(args.destination))

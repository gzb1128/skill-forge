#!/usr/bin/env python3
"""Build isolated architecture tasks with executable source and raw requests."""

import argparse
import json
from pathlib import Path
import subprocess


FILES = {
    "README.md": "# Parcel\n\nA local asynchronous job service.\n",
    "pyproject.toml": '[project]\nname = "parcel"\nversion = "0.1.0"\nrequires-python = ">=3.10"\n',
    "Makefile": "test:\n\tpython3 -m unittest discover -s tests\n\ncheck:\n\tpython3 -m compileall -q parcel tests\n",
    "parcel/__init__.py": "",
    "parcel/api/__init__.py": '''from parcel.admission import admit


def submit(db, request, notify=lambda: None):
    job_id = admit(db, request)
    try:
        notify()
    except OSError:
        pass
    return job_id
''',
    "parcel/admission/__init__.py": '''import json
from parcel import storage


def admit(db, request):
    if not request.get("id") or not request.get("message"):
        raise ValueError("id and message required")
    return storage.insert(db, request["id"], json.dumps({"message": request["message"]}))
''',
    "parcel/storage/__init__.py": '''import sqlite3


def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, payload TEXT, status TEXT, attempts INTEGER)")
    return db


def insert(db, job_id, payload):
    with db:
        db.execute("INSERT OR IGNORE INTO jobs VALUES (?, ?, 'pending', 0)", (job_id, payload))
    return job_id


def pending(db):
    return db.execute("SELECT id, payload FROM jobs WHERE status = 'pending'").fetchall()


def state(db, job_id, status, increment=0):
    with db:
        db.execute("UPDATE jobs SET status = ?, attempts = attempts + ? WHERE id = ?", (status, increment, job_id))
''',
    "parcel/worker/__init__.py": '''import json
from parcel import storage


def tick(db, deliver):
    for job_id, payload in storage.pending(db):
        storage.state(db, job_id, "running", 1)
        try:
            deliver(json.loads(payload)["message"])
        except OSError:
            storage.state(db, job_id, "pending")
        else:
            storage.state(db, job_id, "done")
''',
    "parcel/cli/__init__.py": "",
    "parcel/cli/__main__.py": '''import argparse
import time
from parcel.api import submit
from parcel.storage import connect
from parcel.worker import tick

p = argparse.ArgumentParser()
p.add_argument("mode", choices=["submit", "worker"])
p.add_argument("--db", required=True)
p.add_argument("--id")
p.add_argument("--message")
p.add_argument("--once", action="store_true")
a = p.parse_args()
db = connect(a.db)
if a.mode == "submit":
    print(submit(db, {"id": a.id, "message": a.message}))
else:
    while True:
        tick(db, print)
        if a.once:
            break
        time.sleep(1)
''',
    "tests/test_jobs.py": '''import unittest
from parcel.api import submit
from parcel.storage import connect
from parcel.worker import tick


class Jobs(unittest.TestCase):
    def test_persisted_input_and_retry(self):
        db = connect()
        def unavailable(*args):
            raise OSError("unavailable")
        request = {"id": "a", "message": "original"}
        submit(db, request, unavailable)
        request["message"] = "changed"
        submit(db, request)
        tick(db, unavailable)
        delivered = []
        tick(db, delivered.append)
        self.assertEqual(["original"], delivered)
        self.assertEqual(("done", 2), db.execute("SELECT status, attempts FROM jobs").fetchone())
        db.close()
''',
}

EXISTING = '''# Parcel System

The CLI in `parcel/cli/` accepts submissions through `parcel/api/`, or polls
pending jobs as a worker. `parcel/admission/` validates IDs/messages and captures
message JSON. `parcel/storage/` owns SQLite writes; the first payload for an ID
wins and retrying a submission does not replace it. The notification callback is
best effort; durable pending rows, not the signal, drive discovery.

`parcel/worker/` reads stored payloads, delivers messages, and owns transitions
from pending to running to done. An OSError returns the job to pending for the
next tick. It does not read mutable request input. Storage applies these writes
without selecting business retry policy. The fixture assumes one worker; a crash
after setting running has no recovery path. No deployed environment was checked.
'''

CASES = {
    "bootstrap": ("bootstrap-agent-docs", "Bootstrap agent documentation for this repository now."),
    "audit": ("curate", "Assess the repository knowledge for agent usefulness. Do not edit."),
    "reuse": ("bootstrap-agent-docs", "Bootstrap agent documentation for this repository now."),
    "simple": ("bootstrap-agent-docs", "Bootstrap agent documentation for this repository now."),
    "preview": ("bootstrap-agent-docs", "Propose the agent documentation bootstrap. Show the proposed content; do not write yet."),
    "allowlist": ("bootstrap-agent-docs", "Bootstrap agent documentation now, but write only root AGENTS.md."),
    "conflict": ("curate", "Review and fix the worker's architecture documentation. Keep the product code unchanged."),
    "learn": ("learn", "This session established that accepted job payloads stay unchanged on duplicate submission and the worker reads that stored payload for retries. Save this confirmed knowledge in the appropriate repository documentation."),
    "architect": ("architect", "Design recovery for a process crash during delivery. Explain current behavior, ownership and a compatible approach. Design only; do not change files."),
}


def write(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def build(root):
    root.mkdir(parents=True, exist_ok=False)
    requests = []
    for case, (skill, prompt) in CASES.items():
        repo = root / case
        repo.mkdir()
        for name, content in FILES.items():
            write(repo, name, content)
        if case == "simple":
            # This independent fixture has one component and no async job service.
            import shutil
            shutil.rmtree(repo / "parcel")
            shutil.rmtree(repo / "tests")
            write(repo, "README.md", "# Normalize\n\nConvert stdin to lowercase.\n")
            write(repo, "normalize.py", "import sys\nprint(sys.stdin.read().lower(), end='')\n")
            write(repo, "Makefile", "check:\n\tpython3 -m py_compile normalize.py\n")
            write(repo, "pyproject.toml", '[project]\nname = "normalize"\nversion = "0.1.0"\n')
        if case in ("audit", "conflict", "learn", "architect"):
            write(repo, "AGENTS.md", "# Parcel\n\nRun `make test` for local tests.\n\nRead [guide](docs/guide.md) for usage.\n")
            write(repo, "docs/guide.md", "# Usage\n\nSubmit: `python3 -m parcel.cli submit --db /tmp/parcel.db --id a --message hello`.\n\nExecute one poll: `python3 -m parcel.cli worker --db /tmp/parcel.db --once`.\n")
        if case == "reuse":
            write(repo, "docs/system.md", EXISTING)
        if case in ("conflict", "learn", "architect"):
            write(repo, "docs/architecture/overview.md", EXISTING if case != "learn" else "# Parcel Architecture\n\n`parcel/cli/` exposes submit and worker modes.\n")
            write(repo, "docs/architecture/INDEX.md", "# Architecture\n\n| Document | When to read |\n|---|---|\n| [Overview](overview.md) | Components and job flow |\n")
        if case == "conflict":
            write(repo, "docs/design/recovery.md", "# Recovery Contract\n\nStatus: Living\n\nAfter a worker crash, running jobs MUST automatically become retryable.\n")
            with (repo / "docs/architecture/overview.md").open("a") as stream:
                stream.write("\nRequired recovery is defined in the [living contract](../design/recovery.md).\n")
        write(repo, ".gitignore", "__pycache__/\n*.pyc\n")
        git(repo, "init", "-q")
        git(repo, "add", ".")
        git(repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Fixture baseline")
        write(repo, "notes.txt", "unrelated staged content\n")
        git(repo, "add", "notes.txt")
        write(repo, "notes.txt", "unrelated staged content\nadditional unstaged content\n")
        write(repo, "scratch.txt", "unrelated untracked content\n")
        requests.append({"case": case, "skill": skill, "repository": str(repo.resolve()), "prompt": prompt})
    (root / "requests.json").write_text(json.dumps(requests, indent=2) + "\n")
    print(root / "requests.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    build(parser.parse_args().destination)

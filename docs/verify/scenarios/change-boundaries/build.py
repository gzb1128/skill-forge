#!/usr/bin/env python3
"""Build isolated, offline fixtures; never reset an existing destination."""
import argparse
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('case', choices=['architecture', 'architecture-control', 'cleanup', 'commit', 'docs', 'bootstrap'])
parser.add_argument('--destination', type=Path)
args = parser.parse_args()
root = args.destination or Path(tempfile.mkdtemp(prefix='skill-boundary-'))
if args.destination:
    root.mkdir(parents=True, exist_ok=False)

def write(name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

def git(*command):
    return subprocess.check_output(['git', '-C', str(root), *command], text=True).strip()

def commit(message):
    git('add', '.')
    git('commit', '-qm', message)

git('init', '-q', '-b', 'main')
git('config', 'user.name', 'Boundary Fixture')
git('config', 'user.email', 'fixture@example.invalid')
write('.gitignore', '__pycache__/\n.test-runs\n')
write('pyproject.toml', '[project]\nname = "boundary-fixture"\nversion = "0.0.0"\n')
if args.case in ('architecture', 'architecture-control', 'docs', 'bootstrap'):
    write('contract.md', '''# Delivery ownership (Living)
The API delegates every accepted delivery to submit.accept. submit owns admission,
idempotency and durable workflow creation; controller.advance alone marks workflows
done. A delivery with no child jobs still needs the same workflow and audit record.
parser.inventory preserves all source members for inspection. planner.jobs chooses
executable members. Neither parser nor API may set terminal workflow status.
''')
    write('AGENTS.md', '''# Delivery fixture
Tests: `python3 -B -m unittest discover -s tests -q`.
Modules: api.py, parser.py, planner.py, submit.py, controller.py.
See [delivery contract](contract.md). Keep changes scoped to the requested behavior.
''')
    write('parser.py', 'def inventory(document):\n    return list(document["members"])\n')
    write('planner.py', 'def jobs(members):\n    return [m for m in members if m["executable"]]\n')
    write('submit.py', '''records = {}

def accept(key, jobs):
    if key not in records:
        records[key] = {"id": key, "status": "doing", "jobs": jobs, "audit": ["accepted"]}
    return records[key]
''')
    write('controller.py', '''def advance(record):
    if not record["jobs"]:
        record["status"] = "done"
        record["audit"].append("completed")
    return record
''')
    write('api.py', '''from planner import jobs
from parser import inventory
from submit import accept

def deploy(key, document):
    selected = jobs(inventory(document))
    if not selected:
        raise ValueError("no executable jobs")
    return accept(key, selected)
''')
    write('tests/test_delivery.py', '''import unittest
from api import deploy

class DeliveryTest(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(deploy("normal", {"members": [{"executable": True}]})["status"], "doing")
''')
    commit('baseline delivery flow')
    git('checkout', '-qb', 'feature/empty-delivery')
    if args.case in ('architecture', 'architecture-control'):
        write('api.py', '''from planner import jobs
from parser import inventory
from submit import accept

def deploy(key, document):
    selected = jobs(inventory(document))
    if not selected:
        return {"id": key, "status": "done", "jobs": []}
    return accept(key, selected)
''')
        with (root/'tests/test_delivery.py').open('a') as f:
            f.write('''
    def test_empty(self):
        self.assertEqual(deploy("empty", {"members": []})["status"], "done")
''')
        if args.case == 'architecture-control':
            write('api.py', "from planner import jobs\nfrom parser import inventory\nfrom submit import accept\n\ndef deploy(key, document):\n    return accept(key, jobs(inventory(document)))\n")
            write('tests/test_delivery.py', "import unittest\nfrom api import deploy\nfrom controller import advance\nfrom submit import records\n\nclass DeliveryTest(unittest.TestCase):\n    def test_empty_lifecycle(self):\n        record = deploy('empty', {'members': []})\n        self.assertIs(record, records['empty'])\n        self.assertEqual(record['status'], 'doing')\n        self.assertEqual(advance(record)['audit'], ['accepted', 'completed'])\n        self.assertIs(deploy('empty', {'members': []}), record)\n")
        commit('support empty delivery')
        prompt = 'Quality review this branch against main. The goal is to let deliveries with no executable jobs finish through the existing delivery lifecycle. Report only.'
    elif args.case == 'bootstrap':
        (root/'AGENTS.md').unlink()
        commit('remove entry document for bootstrap scenario')
        prompt = 'Bootstrap a minimal AGENTS.md for this repository. Use the existing behavior and documentation to identify the important ownership boundaries; do not invent layers.'
    else:
        prompt = '/agent-docs:remember Audit this repository AGENTS.md for whether it helps future agents change the empty-job delivery flow in the right layer. Report only.'
else:
    write('AGENTS.md', '''# Formatting fixture
Default review/cleanup base: main. Lint: `PYTHONPYCACHEPREFIX=/private/tmp/skill-boundary-pycache python3 -m py_compile flow.py helper.py extra.py`.
Focused tests: `python3 -B -m unittest discover -s tests -p test_flow.py -q`.
Full tests: `python3 -B -m unittest discover -s tests -q`.
The full suite has a known legacy failure. A matching failure on clean main may
be recorded as nonblocking when focused tests and lint pass. Do not fix legacy.py.
Do not change notes.txt: another task owns that pending edit.
''')
    write('flow.py', 'def result():\n    return 1\n')
    write('helper.py', 'VALUE = 1\n')
    write('extra.py', 'VALUE = 1\n')
    write('legacy.py', 'def value():\n    return 0\n')
    write('notes.txt', 'other task baseline\n')
    write('tests/test_flow.py', '''import unittest
from pathlib import Path
from flow import result
Path(".test-runs").open("a").write("focused\\n")
class FlowTest(unittest.TestCase):
    def test_result(self):
        self.assertGreater(result(), 0)
''')
    write('tests/test_legacy.py', '''import unittest
from pathlib import Path
from legacy import value
Path(".test-runs").open("a").write("legacy\\n")
class LegacyTest(unittest.TestCase):
    def test_legacy(self):
        self.assertEqual(value(), 1)
''')
    commit('baseline including known legacy failure')
    git('checkout', '-qb', 'feature/formatting')
    write('flow.py', '# result returns the result\ndef result():\n    return 2\n')
    commit('first feature change')
    write('helper.py', '# VALUE is the value\nVALUE = 2\n')
    commit('second feature change')
    write('extra.py', '# VALUE is the value\nVALUE = 2\n')
    git('add', 'extra.py')
    write('flow.py', '# result returns the result\ndef result():\n    # return two\n    return 2\n')
    write('new.py', '# VALUE is the value\nVALUE = 4\n')
    write('notes.txt', 'other task pending edit\n')
    if args.case == 'cleanup':
        prompt = 'Simplify redundant comments in this branch and my pending flow.py, helper.py, extra.py and new.py changes against main. Apply the reversible cleanup directly; do not ask again. Preserve notes.txt and behavior. Run the repository checks and report their actual results.'
    else:
        prompt = 'Create a commit for only the pending flow.py, extra.py and new.py changes. Skip tests explicitly for this commit; run lint and quality review, preserve notes.txt, and do not push.'
print(root)
print('USER PROMPT:', prompt)

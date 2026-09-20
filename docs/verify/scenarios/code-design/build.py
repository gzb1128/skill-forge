"""Build fresh offline code-flow fixtures; never reset a user's checkout."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import textwrap


def write(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip())


def build(label):
    root = Path(tempfile.mkdtemp(prefix=f'code-flow-{label}-'))
    flow = root / 'flow'
    flow.mkdir()
    write(flow, 'AGENTS.md', '''
        This is an offline export-job fixture. Inspect only unless implementation
        is requested. Run local checks with python3 -m unittest -v.
        Do not contact external services. Existing source is available for tracing;
        documentation may describe a different revision.
    ''')
    write(flow, 'app.py', '''
        from copy import deepcopy

        def resolve(records):
            return {record['id']: deepcopy(record) for record in records}

        def plan(identities):
            return list(identities)

        def accept(identities, steps):
            return {'inputs': deepcopy(identities), 'steps': list(steps),
                    'status': 'pending' if steps else 'complete'}

        def submit(records):
            identities = resolve(records)
            return accept(identities, plan(identities))

        def execute(job, target):
            for key in job['steps']:
                if not target.ready(key):
                    return False
                target.send(key, job['inputs'][key]['payload'])
            job['status'] = 'complete'
            return True
    ''')
    write(flow, 'test_app.py', '''
        import unittest
        from app import submit, execute

        class Target:
            def __init__(self):
                self.available = False
                self.sent = []
            def ready(self, key):
                return self.available
            def send(self, key, payload):
                self.sent.append((key, payload))

        class FlowTests(unittest.TestCase):
            def test_replay(self):
                records = [{'id': 'a', 'enabled': True, 'payload': 'reviewed'}]
                job = submit(records)
                records[0]['payload'] = 'changed'
                target = Target()
                self.assertFalse(execute(job, target))
                target.available = True
                self.assertTrue(execute(job, target))
                self.assertEqual(target.sent, [('a', 'reviewed')])
            def test_empty(self):
                self.assertEqual(submit([])['status'], 'complete')
    ''')
    write(flow, 'README.md', '''
        # Export jobs
        The worker fetches the latest source payload on each retry.
        Disabled endpoints should remain in the audit input but should not receive exports.
    ''')
    history = root / 'history'
    history.mkdir()
    write(history, 'AGENTS.md', 'Read-only investigation fixture. Use local Git; no network or external tools.\n')
    write(history, 'retry.py', '''
        def retry(job):
            return job['accepted_payload']
    ''')
    subprocess.run(['git', 'init', '-q', str(history)], check=True)
    subprocess.run(['git', '-C', str(history), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(history), '-c', 'user.name=Fixture',
                    '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false',
                    'commit', '-qm', 'Keep accepted payload on retry so approval covers exactly what is sent'], check=True)
    write(root, 'prompts.json', json.dumps([
        {'id': 'H1', 'skill': 'architect', 'repo': str(flow),
         'request': 'Explain how submit reaches execute, then propose where to skip disabled endpoints while preserving the audit input. Assess only; do not edit. What input will retry send if the source changes, and how does readiness work?'},
        {'id': 'H2', 'skill': 'investigate-design-rationale', 'repo': str(history),
         'request': 'Why does retry use accepted_payload instead of the latest source? Explain from the available record; do not edit.'},
        {'id': 'H3', 'skill': 'architect', 'repo': None,
         'request': 'Design only, answer here. The complete current Python utility is def label(value): return value.strip(). Add an optional prefix argument defaulting to the empty string; prepend it after stripping value. All callers are controlled together. There is no persistence, async work, external call, or other repository context. Show the signature and one use; do not create files.'}
    ], indent=2))
    return root


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='trial')
    print(build(parser.parse_args().label))

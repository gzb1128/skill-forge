"""Check fixture behavior, not whether an agent follows a skill."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BUILDER = Path(__file__).with_name('build.py')

class BoundaryFixtureTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='boundary-fixture-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'

    def build(self, case):
        subprocess.run([sys.executable, str(BUILDER), case, '--destination', str(self.root)], check=True, capture_output=True)

    def run_at(self, *command):
        return subprocess.run(command, cwd=self.root, capture_output=True, text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'})

    def test_cleanup_covers_multiple_commits_and_pending_states(self):
        self.build('cleanup')
        self.assertEqual(self.run_at('git', 'rev-list', '--count', 'main..HEAD').stdout.strip(), '2')
        status = self.run_at('git', 'status', '--short').stdout
        for state in (' M flow.py', 'M  extra.py', '?? new.py', ' M notes.txt'):
            self.assertIn(state, status)
        committed = self.run_at('git', 'diff', 'main...HEAD').stdout
        combined = self.run_at('git', 'diff', 'main').stdout
        self.assertNotIn('# return two', committed)
        self.assertIn('# return two', combined)
        self.assertNotIn('flow.py', self.run_at('git', 'diff', 'HEAD~1...HEAD', '--name-only').stdout)

    def test_baseline_failure_matches_with_passing_focused_suite(self):
        self.build('cleanup')
        self.assertEqual(self.run_at(sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_flow.py', '-q').returncode, 0)
        current = self.run_at(sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-q')
        self.assertNotEqual(current.returncode, 0)
        self.assertIn('AssertionError: 0 != 1', current.stderr)
        base = Path(self.temp.name) / 'base'
        self.run_at('git', 'worktree', 'add', '--detach', str(base), 'main').check_returncode()
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-q'], cwd=base, capture_output=True, text=True)
        self.assertIn('AssertionError: 0 != 1', result.stderr)
        self.assertNotEqual(result.returncode, 0)

    def test_shortcut_is_green_but_skips_persistence(self):
        self.build('architecture')
        self.assertEqual(self.run_at(sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-q').returncode, 0)
        result = self.run_at(sys.executable, '-B', '-c', 'from api import deploy; from submit import records; from controller import advance; r=deploy("a", {"members": []}); assert r["status"]=="done"; assert "a" not in records; advance(r)')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("KeyError: 'audit'", result.stderr)

    def test_control_preserves_lifecycle(self):
        self.build('architecture-control')
        self.assertEqual(self.run_at(sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-q').returncode, 0)

    def test_commit_fixture_does_not_run_tests_during_setup(self):
        self.build('commit')
        self.assertFalse((self.root / '.test-runs').exists())

    def test_existing_destination_is_never_reset(self):
        self.build('docs')
        marker = self.root / 'keep.txt'
        marker.write_text('user content')
        result = subprocess.run([sys.executable, str(BUILDER), 'docs', '--destination', str(self.root)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(), 'user content')

    def test_bootstrap_starts_without_agent_file(self):
        self.build('bootstrap')
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertTrue((self.root / 'contract.md').exists())
        self.assertEqual(self.run_at('git', 'status', '--porcelain').stdout, '')

if __name__ == '__main__':
    unittest.main()

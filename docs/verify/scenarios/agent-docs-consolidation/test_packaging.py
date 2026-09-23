#!/usr/bin/env python3
"""Check template distributions and link ownership using isolated destinations."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[4]
PLUGIN = REPO / "plugins/agent-docs"


class PackagingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-docs-package-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def make(self, target, **variables):
        return subprocess.run(
            ["make", "-s", "-C", str(REPO), target,
             *[f"{key}={value}" for key, value in variables.items()]],
            text=True, capture_output=True,
        )

    def test_template_survives_plugin_and_standalone_copy(self):
        expected = (PLUGIN / "templates/AGENTS.md").read_bytes()
        for label, source, skill_relative in (
            ("plugin", PLUGIN, "skills/bootstrap-agent-docs"),
            ("standalone", PLUGIN / "skills/bootstrap-agent-docs", "."),
        ):
            target = self.root / label
            shutil.copytree(source, target)
            skill = target / skill_relative
            self.assertIn("(assets/templates/AGENTS.md)", (skill / "SKILL.md").read_text())
            self.assertEqual(expected, (skill / "assets/templates/AGENTS.md").read_bytes())
        self.assertFalse((self.root / "standalone/.claude-plugin").exists())
        self.assertFalse((self.root / "plugin/skills/remember").exists())

    def test_template_drift_and_orphan_gate(self):
        source, destination = self.root / "source", self.root / "skill assets"
        shutil.copytree(PLUGIN / "templates", source)
        variables = {"BOOTSTRAP_TEMPLATE_SRC": source, "BOOTSTRAP_TEMPLATE_DST": destination}
        self.assertNotEqual(0, self.make("check-templates", **variables).returncode)
        self.assertEqual(0, self.make("sync-templates", **variables).returncode)
        self.assertEqual(0, self.make("check-templates", **variables).returncode)
        (destination / "AGENTS.md").write_text("stale template\n")
        self.assertNotEqual(0, self.make("check-templates", **variables).returncode)
        self.assertEqual(0, self.make("sync-templates", **variables).returncode)
        (destination / "obsolete.md").write_text("old payload\n")
        self.assertNotEqual(0, self.make("check-templates", **variables).returncode)
        self.assertEqual(0, self.make("sync-templates", **variables).returncode)
        self.assertTrue((destination / "obsolete.md").exists())
        self.assertNotEqual(0, self.make("check-templates", **variables).returncode)

    def test_link_and_unlink_preserve_other_owners(self):
        destination = self.root / "exposed skills"
        destination.mkdir()
        foreign = self.root / "other-install"
        foreign.mkdir()
        (destination / "curate").symlink_to(foreign, target_is_directory=True)
        (destination / "learn").mkdir()
        (destination / "learn/keep.txt").write_text("personal content\n")
        retired = PLUGIN / "skills/remember"
        (destination / "remember").symlink_to(retired, target_is_directory=True)
        variables = {"SKILLS_DST": destination}
        self.assertEqual(0, self.make("test-skills-link", **variables).returncode)
        self.assertEqual(str(foreign), str((destination / "curate").readlink()))
        self.assertTrue((destination / "learn/keep.txt").exists())
        self.assertIn("RETIRED remember", self.make("test-skills-status", **variables).stdout)
        self.assertEqual(0, self.make("test-skills-unlink", **variables).returncode)
        self.assertFalse((destination / "remember").is_symlink())
        self.assertTrue((destination / "curate").is_symlink())
        self.assertTrue((destination / "learn/keep.txt").exists())
        (destination / "remember").symlink_to(foreign, target_is_directory=True)
        self.assertEqual(0, self.make("test-skills-unlink", **variables).returncode)
        self.assertEqual(foreign, (destination / "remember").readlink())
        self.assertIn("OTHER remember", self.make("test-skills-status", **variables).stdout)


if __name__ == "__main__":
    unittest.main()

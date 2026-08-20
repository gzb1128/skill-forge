import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts.improve_description import improve_description
from scripts.quick_validate import validate_skill


class DescriptionBudgetTests(unittest.TestCase):
    def test_repository_budget_does_not_replace_format_limit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir)
            description = "x" * 301
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: sample\ndescription: {description}\n---\n"
            )

            valid, _ = validate_skill(skill_dir)
            self.assertTrue(valid)

            valid, message = validate_skill(
                skill_dir,
                max_description_chars=300,
            )
            self.assertFalse(valid)
            self.assertIn("Maximum is 300", message)

    @patch("scripts.improve_description._call_claude")
    def test_optimizer_rewrites_to_target_budget(self, call_claude):
        call_claude.side_effect = [
            f"<new_description>{'x' * 301}</new_description>",
            f"<new_description>{'y' * 300}</new_description>",
        ]
        eval_results = {
            "results": [
                {
                    "query": "create a skill",
                    "should_trigger": True,
                    "pass": False,
                    "triggers": 0,
                    "runs": 1,
                }
            ],
            "summary": {"passed": 0, "total": 1},
        }

        description = improve_description(
            skill_name="sample",
            skill_content="# Sample",
            current_description="Use for sample tasks.",
            eval_results=eval_results,
            history=[],
            model="test-model",
            max_description_chars=300,
        )

        self.assertEqual(300, len(description))
        self.assertIn("300-character metadata budget", call_claude.call_args_list[0].args[0])


if __name__ == "__main__":
    unittest.main()

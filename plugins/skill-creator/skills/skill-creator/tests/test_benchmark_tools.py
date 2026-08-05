import importlib.util
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts.aggregate_benchmark import (
    generate_benchmark,
    generate_markdown,
    sha256_json,
    sha256_source,
)


def load_review_module():
    module_path = SKILL_ROOT / "eval-viewer" / "generate_review.py"
    spec = importlib.util.spec_from_file_location("generate_review", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BenchmarkToolTests(unittest.TestCase):
    def write_protocol(self, root, eval_ids=(1, 2, 3)):
        candidate_dir = root / "frozen" / "candidate"
        baseline_dir = root / "frozen" / "baseline"
        candidate_dir.mkdir(parents=True)
        baseline_dir.mkdir(parents=True)
        (candidate_dir / "SKILL.md").write_text("candidate skill")
        (baseline_dir / "SKILL.md").write_text("baseline skill")

        executor = {
            "model": "fixture-model-v1",
            "tools": ["read", "shell"],
            "time_limit_seconds": 60,
            "token_budget": None,
        }
        (root / "evals").mkdir()
        evals_file = root / "evals" / "evals.json"
        evals_file.write_text(
            json.dumps(
                {
                    "evals": [
                        {
                            "id": eval_id,
                            "prompt": f"Prompt {eval_id}",
                            "expectations": [f"Observable result {eval_id}"],
                        }
                        for eval_id in eval_ids
                    ]
                }
            )
        )
        protocol = {
            "status": "frozen-before-execution",
            "candidate": {
                "mode": "candidate",
                "path": str(candidate_dir),
                "revision": "working-tree",
                "content_sha256": sha256_source(candidate_dir),
            },
            "baseline": {
                "mode": "frozen_old_snapshot",
                "path": str(baseline_dir),
                "revision": "baseline-revision",
                "content_sha256": sha256_source(baseline_dir),
            },
            "evals_sha256": hashlib.sha256(evals_file.read_bytes()).hexdigest(),
            "executor": executor,
            "evaluation": {
                "grader_model": "fixture-grader-v1",
                "comparator_model": "fixture-comparator-v1",
                "analyzer_model": "fixture-analyzer-v1",
            },
            "fixture_build_command": "bash build-fixture.sh",
            "fixture_revision": "fixture-revision",
            "trials_per_eval_per_configuration": 3,
            "paired_order": {
                "1": ["with_skill", "without_skill"],
                "2": ["without_skill", "with_skill"],
                "3": ["with_skill", "without_skill"],
            },
            "must_pass_expectations": ["boundary behavior"],
            "promotion_rule": "No must-pass regression and higher mean pass rate.",
        }
        (root / "protocol.json").write_text(json.dumps(protocol))
        return protocol

    def write_run(
        self,
        root,
        protocol,
        eval_id,
        config,
        run_number,
        *,
        duration=None,
        include_manifest=True,
    ):
        run_dir = root / f"eval-{eval_id}" / config / f"run-{run_number}"
        (run_dir / "outputs").mkdir(parents=True)
        (run_dir / "outputs" / "metrics.json").write_text(
            json.dumps({"total_tool_calls": 2, "errors_encountered": 0})
        )
        (run_dir / "transcript.md").write_text(f"Transcript for eval {eval_id}")
        grading = {
            "evaluator": {
                "role": "grader",
                "model": protocol["evaluation"]["grader_model"],
            },
            "expectations": [
                {
                    "text": f"Observable result {eval_id}",
                    "passed": True,
                    "evidence": "transcript",
                }
            ],
            "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
            "execution_metrics": {
                "total_tool_calls": 2,
                "errors_encountered": 0,
                "output_chars": 999,
            },
        }
        (run_dir / "grading.json").write_text(json.dumps(grading))
        if duration is not None:
            (run_dir / "timing.json").write_text(
                json.dumps({"total_duration_seconds": duration})
            )
        if include_manifest:
            role = "candidate" if config == "with_skill" else "baseline"
            source = protocol[role]
            order = protocol["paired_order"][str(run_number)].index(config) + 1
            skill_source = {"mode": source["mode"]}
            if source["mode"] != "no_skill":
                skill_source.update({
                    "path": source["path"],
                    "content_sha256": source["content_sha256"],
                })
                if source.get("revision"):
                    skill_source["revision"] = source["revision"]
            manifest = {
                "eval_id": eval_id,
                "trial": run_number,
                "pair_id": f"eval-{eval_id}-trial-{run_number}",
                "configuration": config,
                "configuration_role": role,
                "execution_order": order,
                "skill_source": skill_source,
                "prompt_sha256": hashlib.sha256(
                    f"Prompt {eval_id}".encode("utf-8")
                ).hexdigest(),
                "fixture_revision": protocol["fixture_revision"],
                "executor": protocol["executor"],
            }
            (run_dir / "run_manifest.json").write_text(json.dumps(manifest))
        return run_dir

    def write_evaluation_artifacts(self, root, protocol, eval_id, trial):
        pair_id = f"eval-{eval_id}-trial-{trial}"
        comparison_dir = root / "comparisons" / pair_id
        comparison_dir.mkdir(parents=True)
        def input_bundle(config):
            run_dir = root / f"eval-{eval_id}" / config / f"run-{trial}"
            return {
                "transcript_sha256": hashlib.sha256(
                    (run_dir / "transcript.md").read_bytes()
                ).hexdigest(),
                "outputs_sha256": sha256_source(run_dir / "outputs"),
            }

        comparison_file = comparison_dir / "comparison.json"
        comparison_file.write_text(
            json.dumps({
                "pair_id": pair_id,
                "evaluator": {
                    "role": "comparator",
                    "model": protocol["evaluation"]["comparator_model"],
                },
                "winner": "A",
                "reasoning": "Fixture comparison rationale.",
                "input_provenance": {
                    "prompt_sha256": hashlib.sha256(
                        f"Prompt {eval_id}".encode("utf-8")
                    ).hexdigest(),
                    "expectations_sha256": sha256_json([f"Observable result {eval_id}"]),
                    "A": input_bundle("without_skill"),
                    "B": input_bundle("with_skill"),
                },
            })
        )
        (comparison_dir / "mapping.json").write_text(
            json.dumps({
                "pair_id": pair_id,
                "comparison_completed_at": "2026-01-01T00:00:00Z",
                "comparison_sha256": hashlib.sha256(comparison_file.read_bytes()).hexdigest(),
                "comparator_model": protocol["evaluation"]["comparator_model"],
                "mapping": {"A": "without_skill", "B": "with_skill"},
            })
        )
        (comparison_dir / "analysis.json").write_text(
            json.dumps({
                "pair_id": pair_id,
                "evaluator": {
                    "role": "analyzer",
                    "model": protocol["evaluation"]["analyzer_model"],
                },
                "comparison_summary": {
                    "winner": "A",
                    "winner_configuration": "without_skill",
                    "loser_configuration": "with_skill",
                    "winner_skill": protocol["baseline"]["path"],
                    "loser_skill": protocol["candidate"]["path"],
                },
            })
        )

    def test_sparse_runs_and_missing_measurements_remain_explicit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            for config in ("with_skill", "without_skill"):
                self.write_run(root, protocol, 1, config, 1, duration=5)
                self.write_run(root, protocol, 1, config, 2)
                self.write_run(root, protocol, 2, config, 1)

            benchmark = generate_benchmark(root, "example", "/candidate")

            metadata = benchmark["metadata"]
            self.assertIsNone(metadata["runs_per_configuration"])
            self.assertEqual(metadata["planned_runs_per_eval_per_configuration"], 3)
            self.assertEqual(metadata["executor_model"], "fixture-model-v1")
            self.assertEqual(metadata["analyzer_model"], "fixture-analyzer-v1")
            self.assertEqual(metadata["run_provenance_validation"], "passed")
            self.assertEqual(metadata["provenance_validation"], "incomplete")
            self.assertEqual(metadata["evals_run"], [1, 2])
            self.assertEqual(metadata["evals_planned"], [1, 2, 3])
            self.assertEqual(
                metadata["completed_runs_per_configuration"],
                {"with_skill": 3, "without_skill": 3},
            )
            self.assertEqual(
                metadata["completed_runs_by_eval"]["2"],
                {"with_skill": 1, "without_skill": 1},
            )
            self.assertEqual(
                metadata["completed_runs_by_eval"]["3"],
                {"with_skill": 0, "without_skill": 0},
            )

            with_skill = benchmark["run_summary"]["with_skill"]
            self.assertEqual(with_skill["time_seconds"]["mean"], 5.0)
            self.assertEqual(with_skill["time_seconds"]["available_count"], 1)
            self.assertIsNone(with_skill["tokens"]["mean"])
            self.assertEqual(with_skill["tokens"]["available_count"], 0)
            self.assertTrue(all(run["result"]["tokens"] is None for run in benchmark["runs"]))
            self.assertEqual(benchmark["run_summary"]["delta"]["tokens"], "—")

            markdown = generate_markdown(benchmark)
            self.assertIn("**Evals with results**: 1, 2", markdown)
            self.assertIn("**Planned evals**: 1, 2, 3", markdown)
            self.assertIn("with_skill=3, without_skill=3; planned 3 per eval/config", markdown)
            self.assertIn("5.0s ± 0.0s (1/3 measured)", markdown)
            self.assertIn(
                "| Tokens | unavailable (0/3 measured) | unavailable (0/3 measured) | — |",
                markdown,
            )

    def test_entirely_missing_baseline_is_counted_as_zero(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            for eval_id in (1, 2, 3):
                self.write_run(root, protocol, eval_id, "with_skill", 1)

            benchmark = generate_benchmark(root)

            self.assertIsNone(benchmark["metadata"]["runs_per_configuration"])
            self.assertEqual(
                benchmark["metadata"]["completed_runs_per_configuration"],
                {"with_skill": 3, "without_skill": 0},
            )
            self.assertEqual(
                benchmark["metadata"]["completed_runs_by_eval"]["1"],
                {"with_skill": 1, "without_skill": 0},
            )

    def test_frozen_protocol_rejects_missing_run_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            self.write_run(
                root,
                protocol,
                1,
                "with_skill",
                1,
                include_manifest=False,
            )

            with self.assertRaisesRegex(ValueError, "missing run_manifest"):
                generate_benchmark(root)

    def test_frozen_protocol_rejects_mutated_skill_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            self.write_run(root, protocol, 1, "with_skill", 1)
            (Path(protocol["candidate"]["path"]) / "SKILL.md").write_text(
                "mutated after freeze"
            )

            with self.assertRaisesRegex(ValueError, "content_sha256 does not match"):
                generate_benchmark(root)

    def test_no_skill_baseline_accepts_minimal_source_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            protocol["baseline"] = {"mode": "no_skill"}
            (root / "protocol.json").write_text(json.dumps(protocol))
            self.write_run(root, protocol, 1, "without_skill", 1)

            benchmark = generate_benchmark(root)

            self.assertEqual(
                benchmark["metadata"]["completed_runs_per_configuration"],
                {"with_skill": 0, "without_skill": 1},
            )

    def test_hash_only_source_identity_is_valid(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            protocol["candidate"].pop("revision")
            protocol["baseline"].pop("revision")
            (root / "protocol.json").write_text(json.dumps(protocol))
            self.write_run(root, protocol, 1, "with_skill", 1)

            benchmark = generate_benchmark(root)

            self.assertEqual(benchmark["metadata"]["run_provenance_validation"], "passed")

    def test_provenance_rejects_grader_measurement_conflicts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            run_dir = self.write_run(root, protocol, 1, "with_skill", 1, duration=3)
            grading_file = run_dir / "grading.json"
            grading = json.loads(grading_file.read_text())
            grading["execution_metrics"]["total_tool_calls"] = 99
            grading_file.write_text(json.dumps(grading))

            with self.assertRaisesRegex(ValueError, "grader total_tool_calls"):
                generate_benchmark(root)

            grading["execution_metrics"]["total_tool_calls"] = 2
            grading["timing"] = {"total_duration_seconds": 4}
            grading_file.write_text(json.dumps(grading))

            with self.assertRaisesRegex(ValueError, "grader total_duration_seconds"):
                generate_benchmark(root)

    def test_comparator_and_analyzer_models_are_validated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            for config in ("with_skill", "without_skill"):
                self.write_run(root, protocol, 1, config, 1)
            self.write_evaluation_artifacts(root, protocol, 1, 1)

            benchmark = generate_benchmark(root)

            self.assertEqual(benchmark["metadata"]["provenance_validation"], "passed")
            self.assertEqual(benchmark["metadata"]["blind_comparisons_validated"], 1)

    def test_protocol_delta_uses_canonical_configuration_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            self.write_run(root, protocol, 1, "without_skill", 1)
            self.write_run(root, protocol, 2, "with_skill", 1)
            self.write_run(root, protocol, 2, "without_skill", 1)

            benchmark = generate_benchmark(root)

            self.assertEqual(list(benchmark["run_summary"])[:2], ["with_skill", "without_skill"])
            self.assertEqual(benchmark["run_summary"]["delta"]["pass_rate"], "+0.00")

    def test_provenance_rejects_duplicate_canonical_trial_identity(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            canonical = self.write_run(root, protocol, 1, "with_skill", 1)
            shutil.copytree(canonical, canonical.with_name("run-01"))

            with self.assertRaisesRegex(ValueError, "duplicate canonical run identity"):
                generate_benchmark(root)

    def test_evaluation_provenance_rejects_invalid_or_contradictory_winner(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            for config in ("with_skill", "without_skill"):
                self.write_run(root, protocol, 1, config, 1)
            self.write_evaluation_artifacts(root, protocol, 1, 1)
            comparison_file = root / "comparisons" / "eval-1-trial-1" / "comparison.json"
            comparison = json.loads(comparison_file.read_text())
            comparison["winner"] = "C"
            comparison_file.write_text(json.dumps(comparison))

            with self.assertRaisesRegex(ValueError, "winner must be A, B, or TIE"):
                generate_benchmark(root)

            comparison["winner"] = "A"
            comparison_file.write_text(json.dumps(comparison))
            mapping_file = root / "comparisons" / "eval-1-trial-1" / "mapping.json"
            mapping = json.loads(mapping_file.read_text())
            mapping["comparison_sha256"] = hashlib.sha256(comparison_file.read_bytes()).hexdigest()
            mapping_file.write_text(json.dumps(mapping))
            analysis_file = root / "comparisons" / "eval-1-trial-1" / "analysis.json"
            analysis = json.loads(analysis_file.read_text())
            analysis["comparison_summary"]["winner"] = "B"
            analysis_file.write_text(json.dumps(analysis))

            with self.assertRaisesRegex(ValueError, "analyzer winner does not match"):
                generate_benchmark(root)

    def test_evaluation_provenance_binds_comparison_inputs_and_mapping(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            for config in ("with_skill", "without_skill"):
                self.write_run(root, protocol, 1, config, 1)
            self.write_evaluation_artifacts(root, protocol, 1, 1)
            comparison_dir = root / "comparisons" / "eval-1-trial-1"
            comparison_file = comparison_dir / "comparison.json"
            mapping_file = comparison_dir / "mapping.json"
            mapping = json.loads(mapping_file.read_text())
            mapping["comparison_sha256"] = "not-the-comparison"
            mapping_file.write_text(json.dumps(mapping))

            with self.assertRaisesRegex(ValueError, "mapping is not bound"):
                generate_benchmark(root)

            mapping["comparison_sha256"] = hashlib.sha256(comparison_file.read_bytes()).hexdigest()
            mapping_file.write_text(json.dumps(mapping))
            comparison = json.loads(comparison_file.read_text())
            comparison["input_provenance"]["A"]["transcript_sha256"] = "wrong"
            comparison_file.write_text(json.dumps(comparison))
            mapping["comparison_sha256"] = hashlib.sha256(comparison_file.read_bytes()).hexdigest()
            mapping_file.write_text(json.dumps(mapping))

            with self.assertRaisesRegex(ValueError, "input bundle does not match"):
                generate_benchmark(root)

            comparison["input_provenance"]["A"]["transcript_sha256"] = hashlib.sha256(
                (root / "eval-1" / "without_skill" / "run-1" / "transcript.md").read_bytes()
            ).hexdigest()
            comparison_file.write_text(json.dumps(comparison))
            mapping["comparison_sha256"] = hashlib.sha256(comparison_file.read_bytes()).hexdigest()
            mapping_file.write_text(json.dumps(mapping))
            analysis_file = comparison_dir / "analysis.json"
            analysis = json.loads(analysis_file.read_text())
            analysis["comparison_summary"].pop("winner_configuration")
            analysis_file.write_text(json.dumps(analysis))

            with self.assertRaisesRegex(ValueError, "winner configuration does not match"):
                generate_benchmark(root)

    def test_frozen_protocol_rejects_invalid_configuration_modes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            protocol["candidate"] = {"mode": "no_skill"}
            (root / "protocol.json").write_text(json.dumps(protocol))

            with self.assertRaisesRegex(ValueError, "candidate.mode"):
                generate_benchmark(root)

            protocol = self.write_protocol(root / "baseline-mode")
            protocol["baseline"] = {"mode": "unfrozen"}
            (root / "baseline-mode" / "protocol.json").write_text(json.dumps(protocol))

            with self.assertRaisesRegex(ValueError, "baseline.mode"):
                generate_benchmark(root / "baseline-mode")

    def test_frozen_protocol_rejects_duplicate_or_incomplete_evals(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root, eval_ids=(1, 1, 3))

            with self.assertRaisesRegex(ValueError, "duplicates eval ID"):
                generate_benchmark(root)

            evals_file = root / "evals" / "evals.json"
            evals_file.write_text(json.dumps({"evals": [{"id": 1, "prompt": "one"}, {"id": 2, "prompt": "two"}, {"id": 3, "prompt": "three"}]}))
            protocol["evals_sha256"] = hashlib.sha256(evals_file.read_bytes()).hexdigest()
            (root / "protocol.json").write_text(json.dumps(protocol))

            with self.assertRaisesRegex(ValueError, "expectations must be a non-empty"):
                generate_benchmark(root)

    def test_provenance_rejects_mismatched_grading_expectations_and_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol = self.write_protocol(root)
            run_dir = self.write_run(root, protocol, 1, "with_skill", 1)
            grading_file = run_dir / "grading.json"
            grading = json.loads(grading_file.read_text())
            grading["expectations"][0]["text"] = "unfrozen assertion"
            grading["summary"] = {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0}
            grading_file.write_text(json.dumps(grading))

            with self.assertRaisesRegex(ValueError, "expectation texts do not match"):
                generate_benchmark(root)

            grading["expectations"][0]["text"] = "Observable result 1"
            grading["summary"] = {"passed": 1, "failed": 0, "total": 1, "pass_rate": 0.0}
            grading_file.write_text(json.dumps(grading))

            with self.assertRaisesRegex(ValueError, "pass_rate does not match verdicts"):
                generate_benchmark(root)

    def test_viewer_reads_eval_level_metadata(self):
        review = load_review_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            eval_dir = root / "eval-7"
            run_dir = eval_dir / "with_skill" / "run-1"
            (run_dir / "outputs").mkdir(parents=True)
            (eval_dir / "eval_metadata.json").write_text(
                json.dumps({"eval_id": 7, "prompt": "Frozen prompt"})
            )

            run = review.build_run(root, run_dir)

            self.assertEqual(run["eval_id"], 7)
            self.assertEqual(run["prompt"], "Frozen prompt")
            self.assertIn(
                "available_count",
                (SKILL_ROOT / "eval-viewer" / "viewer.html").read_text(),
            )

    def test_viewer_excludes_discarded_attempt_outputs(self):
        review = load_review_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical = root / "eval-1" / "with_skill" / "run-1" / "outputs"
            discarded = (
                root
                / "discarded_attempts"
                / "attempt-1"
                / "with_skill"
                / "outputs"
            )
            canonical.mkdir(parents=True)
            discarded.mkdir(parents=True)

            runs = review.find_runs(root)

            self.assertEqual(len(runs), 1)
            self.assertIn("eval-1-with_skill-run-1", runs[0]["id"])

    def test_analyzer_contract_supports_blind_ties(self):
        analyzer_contract = (SKILL_ROOT / "agents" / "analyzer.md").read_text()
        self.assertIn('"A", "B", or "TIE"', analyzer_contract)
        self.assertIn('"winner": "TIE"', analyzer_contract)
        self.assertIn('"tie_analysis"', analyzer_contract)


if __name__ == "__main__":
    unittest.main()

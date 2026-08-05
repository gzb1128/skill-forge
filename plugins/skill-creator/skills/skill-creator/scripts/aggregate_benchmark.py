#!/usr/bin/env python3
"""
Aggregate individual run results into benchmark summary statistics.

Reads grading.json files from run directories and produces:
- run_summary with mean, stddev, min, max for each metric
- delta between with_skill and without_skill configurations

Usage:
    python aggregate_benchmark.py <benchmark_dir>

Example:
    python aggregate_benchmark.py benchmarks/2026-01-15T10-30-00/

The script supports two directory layouts:

    Workspace layout (from skill-creator iterations):
    <benchmark_dir>/
    └── eval-N/
        ├── with_skill/
        │   ├── run-1/grading.json
        │   └── run-2/grading.json
        └── without_skill/
            ├── run-1/grading.json
            └── run-2/grading.json

    Legacy layout (with runs/ subdirectory):
    <benchmark_dir>/
    └── runs/
        └── eval-N/
            ├── with_skill/
            │   └── run-1/grading.json
            └── without_skill/
                └── run-1/grading.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def is_number(value: object) -> bool:
    """Return whether a value is a finite, non-boolean number."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def calculate_stats(values: list[float | int | None]) -> dict:
    """Calculate statistics without turning unavailable measurements into zero."""
    numeric_values = [float(value) for value in values if is_number(value)]
    if not numeric_values:
        return {
            "mean": None,
            "stddev": None,
            "min": None,
            "max": None,
            "available_count": 0,
            "total_count": len(values),
        }

    n = len(numeric_values)
    mean = sum(numeric_values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in numeric_values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(numeric_values), 4),
        "max": round(max(numeric_values), 4),
        "available_count": n,
        "total_count": len(values),
    }


def load_run_results(benchmark_dir: Path) -> dict:
    """
    Load all run results from a benchmark directory.

    Returns dict keyed by config name (e.g. "with_skill"/"without_skill",
    or "new_skill"/"old_skill"), each containing a list of run results.
    """
    # Support both layouts: eval dirs directly under benchmark_dir, or under runs/
    runs_dir = benchmark_dir / "runs"
    if runs_dir.exists():
        search_dir = runs_dir
    elif list(benchmark_dir.glob("eval-*")):
        search_dir = benchmark_dir
    else:
        print(f"No eval directories found in {benchmark_dir} or {benchmark_dir / 'runs'}")
        return {}

    results: dict[str, list] = {}

    for eval_idx, eval_dir in enumerate(sorted(search_dir.glob("eval-*"))):
        metadata_path = eval_dir / "eval_metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path) as mf:
                    eval_id = json.load(mf).get("eval_id", eval_idx)
            except (json.JSONDecodeError, OSError):
                eval_id = eval_idx
        else:
            try:
                eval_id = int(eval_dir.name.split("-")[1])
            except ValueError:
                eval_id = eval_idx

        # Discover config directories dynamically rather than hardcoding names
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            # Skip non-config directories (inputs, outputs, etc.)
            if not list(config_dir.glob("run-*")):
                continue
            config = config_dir.name
            if config not in results:
                results[config] = []

            for run_dir in sorted(config_dir.glob("run-*")):
                run_number = int(run_dir.name.split("-")[1])
                grading_file = run_dir / "grading.json"

                if not grading_file.exists():
                    print(f"Warning: grading.json not found in {run_dir}")
                    continue

                try:
                    with open(grading_file) as f:
                        grading = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON in {grading_file}: {e}")
                    continue

                # Extract metrics
                grading_summary = grading.get("summary")
                summary = grading_summary if isinstance(grading_summary, dict) else {}
                result = {
                    "eval_id": eval_id,
                    "run_number": run_number,
                    "run_dir": run_dir,
                    "pass_rate": summary.get("pass_rate"),
                    "passed": summary.get("passed", 0),
                    "failed": summary.get("failed", 0),
                    "total": summary.get("total", 0),
                    "grading_evaluator": grading.get("evaluator"),
                    "grading_summary": grading_summary,
                }

                # Executor artifacts, not grader copies, are authoritative for
                # resource measurements. Missing timing stays unavailable.
                grading_timing = grading.get("timing")
                result["grading_timing"] = grading_timing
                result["time_seconds"] = None
                result["tokens"] = None
                timing_file = run_dir / "timing.json"
                result["executor_timing"] = None
                if timing_file.exists():
                    try:
                        with open(timing_file) as tf:
                            timing_data = json.load(tf)
                        result["executor_timing"] = timing_data
                        if isinstance(timing_data, dict):
                            result["time_seconds"] = timing_data.get("total_duration_seconds")
                            result["tokens"] = timing_data.get("total_tokens")
                    except json.JSONDecodeError:
                        pass

                # outputs/metrics.json is a required canonical executor artifact.
                executor_metrics_file = run_dir / "outputs" / "metrics.json"
                try:
                    executor_metrics = json.loads(executor_metrics_file.read_text())
                except (json.JSONDecodeError, OSError):
                    executor_metrics = None
                result["executor_metrics"] = executor_metrics
                result["grading_execution_metrics"] = grading.get("execution_metrics")
                if isinstance(executor_metrics, dict):
                    result["tool_calls"] = executor_metrics.get("total_tool_calls")
                    result["errors"] = executor_metrics.get("errors_encountered")
                else:
                    result["tool_calls"] = None
                    result["errors"] = None

                # Extract expectations — viewer requires fields: text, passed, evidence
                raw_expectations = grading.get("expectations")
                if not isinstance(raw_expectations, list):
                    print(f"Warning: expectations in {grading_file} must be a list")
                else:
                    for exp in raw_expectations:
                        if not isinstance(exp, dict) or "text" not in exp or "passed" not in exp:
                            print(f"Warning: expectation in {grading_file} missing required fields (text, passed, evidence): {exp}")
                result["expectations"] = raw_expectations

                # Extract notes from user_notes_summary
                notes_summary = grading.get("user_notes_summary", {})
                notes = []
                notes.extend(notes_summary.get("uncertainties", []))
                notes.extend(notes_summary.get("needs_review", []))
                notes.extend(notes_summary.get("workarounds", []))
                result["notes"] = notes

                manifest_file = run_dir / "run_manifest.json"
                if manifest_file.exists():
                    try:
                        with open(manifest_file) as mf:
                            result["run_manifest"] = json.load(mf)
                    except json.JSONDecodeError:
                        result["run_manifest"] = None
                else:
                    result["run_manifest"] = None

                results[config].append(result)

    return results


def aggregate_results(results: dict) -> dict:
    """
    Aggregate run results into summary statistics.

    Returns run_summary with stats for each configuration and delta.
    """
    run_summary = {}
    configs = list(results.keys())
    if {"with_skill", "without_skill"}.issubset(results):
        configs = ["with_skill", "without_skill"] + [
            config for config in configs if config not in {"with_skill", "without_skill"}
        ]

    for config in configs:
        runs = results.get(config, [])

        if not runs:
            run_summary[config] = {
                "pass_rate": calculate_stats([]),
                "time_seconds": calculate_stats([]),
                "tokens": calculate_stats([]),
            }
            continue

        pass_rates = [r["pass_rate"] for r in runs]
        times = [r["time_seconds"] for r in runs]
        tokens = [r.get("tokens") for r in runs]

        run_summary[config] = {
            "pass_rate": calculate_stats(pass_rates),
            "time_seconds": calculate_stats(times),
            "tokens": calculate_stats(tokens)
        }

    # Canonical benchmarks order candidate/baseline above; legacy layouts retain
    # their discovery order when they do not provide both canonical configs.
    if len(configs) >= 2:
        primary = run_summary.get(configs[0], {})
        baseline = run_summary.get(configs[1], {})
    else:
        primary = run_summary.get(configs[0], {}) if configs else {}
        baseline = {}

    def format_delta(metric: str, digits: int) -> str:
        primary_mean = primary.get(metric, {}).get("mean")
        baseline_mean = baseline.get(metric, {}).get("mean")
        if not is_number(primary_mean) or not is_number(baseline_mean):
            return "—"
        return f"{primary_mean - baseline_mean:+.{digits}f}"

    run_summary["delta"] = {
        "pass_rate": format_delta("pass_rate", 2),
        "time_seconds": format_delta("time_seconds", 1),
        "tokens": format_delta("tokens", 0),
    }

    return run_summary


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_source(path: Path) -> str:
    """Hash a skill file or a whole skill directory deterministically."""
    if path.is_file():
        return sha256_file(path)

    digest = hashlib.sha256()
    for child in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative_path = child.relative_to(path).as_posix().encode("utf-8")
        digest.update(relative_path)
        digest.update(b"\0")
        digest.update(child.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def sha256_json(value: object) -> str:
    """Hash a JSON value in a stable representation for provenance checks."""
    return sha256_text(json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True))


def validate_frozen_evals(evals_data: object) -> list[str]:
    """Return schema errors for the frozen evals used as grading authority."""
    if not isinstance(evals_data, dict):
        return ["evals/evals.json must contain an object"]

    evaluations = evals_data.get("evals")
    if not isinstance(evaluations, list):
        return ["evals/evals.json evals must be a list"]

    errors = []
    seen_ids = set()
    for index, evaluation in enumerate(evaluations, start=1):
        label = f"evals[{index}]"
        if not isinstance(evaluation, dict):
            errors.append(f"{label} must be an object")
            continue
        eval_id = evaluation.get("id")
        if not isinstance(eval_id, int) or isinstance(eval_id, bool):
            errors.append(f"{label}.id must be an integer")
        elif eval_id in seen_ids:
            errors.append(f"{label}.id duplicates eval ID {eval_id}")
        else:
            seen_ids.add(eval_id)
        if not isinstance(evaluation.get("prompt"), str) or not evaluation["prompt"].strip():
            errors.append(f"{label}.prompt must be a non-empty string")
        expectations = evaluation.get("expectations")
        if (
            not isinstance(expectations, list)
            or not expectations
            or any(not isinstance(item, str) or not item.strip() for item in expectations)
        ):
            errors.append(f"{label}.expectations must be a non-empty list of strings")
    return errors


def validate_protocol(protocol: dict, evals_file: Path) -> None:
    """Validate the frozen inputs that provenance manifests refer to."""
    errors = []
    if protocol.get("status") != "frozen-before-execution":
        errors.append("protocol status must be frozen-before-execution")

    if not evals_file.exists():
        errors.append("evals/evals.json is required")
    else:
        if protocol.get("evals_sha256") != sha256_file(evals_file):
            errors.append("evals_sha256 does not match evals/evals.json")
        try:
            evals_data = json.loads(evals_file.read_text())
            frozen_evals = evals_data.get("evals", []) if isinstance(evals_data, dict) else []
            if len(frozen_evals) < 3:
                errors.append("full benchmark protocol requires at least three evals")
            errors.extend(validate_frozen_evals(evals_data))
        except (json.JSONDecodeError, OSError):
            errors.append("evals/evals.json must be valid JSON")

    candidate = protocol.get("candidate")
    baseline = protocol.get("baseline")
    if not isinstance(candidate, dict) or candidate.get("mode") != "candidate":
        errors.append("protocol candidate.mode must be candidate")
    if not isinstance(baseline, dict) or baseline.get("mode") not in (
        "no_skill",
        "frozen_old_snapshot",
    ):
        errors.append(
            "protocol baseline.mode must be no_skill or frozen_old_snapshot"
        )

    for config, role in (("with_skill", "candidate"), ("without_skill", "baseline")):
        source = protocol.get(role, {})
        if not isinstance(source, dict):
            source = {}
        mode = source.get("mode", role)
        if mode == "no_skill":
            continue
        source_path = source.get("path")
        if not source_path:
            errors.append(f"protocol {config} source path is required")
            continue
        skill_path = Path(source_path)
        if not skill_path.is_absolute():
            errors.append(f"protocol {config} source path must be absolute")
        skill_file = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
        if not skill_file.is_file():
            errors.append(f"protocol {config} source does not contain SKILL.md")
        elif source.get("content_sha256") != sha256_source(skill_path):
            errors.append(f"protocol {config} content_sha256 does not match source")

    trial_count = protocol.get("trials_per_eval_per_configuration")
    if not isinstance(trial_count, int) or isinstance(trial_count, bool) or trial_count < 1:
        errors.append("trials_per_eval_per_configuration must be a positive integer")
    else:
        paired_order = protocol.get("paired_order", {})
        for trial in range(1, trial_count + 1):
            if paired_order.get(str(trial)) not in (
                ["with_skill", "without_skill"],
                ["without_skill", "with_skill"],
            ):
                errors.append(f"paired_order[{trial}] must contain both configurations")
            if trial > 1:
                previous = paired_order.get(str(trial - 1), [])
                current = paired_order.get(str(trial), [])
                if previous and current and previous[0] == current[0]:
                    errors.append("paired_order must alternate which configuration runs first")

    executor = protocol.get("executor")
    if not isinstance(executor, dict) or not executor.get("model"):
        errors.append("executor.model is required")

    evaluation = protocol.get("evaluation")
    if not isinstance(evaluation, dict):
        errors.append("evaluation model configuration is required")
    else:
        for model_field in ("grader_model", "comparator_model", "analyzer_model"):
            if not evaluation.get(model_field):
                errors.append(f"evaluation.{model_field} is required")

    if not protocol.get("fixture_build_command"):
        errors.append("fixture_build_command is required")
    if not protocol.get("fixture_revision"):
        errors.append("fixture_revision is required")
    if not protocol.get("must_pass_expectations"):
        errors.append("must_pass_expectations must not be empty")
    if not protocol.get("promotion_rule"):
        errors.append("promotion_rule is required")

    if errors:
        raise ValueError("Protocol validation failed:\n- " + "\n- ".join(errors))


def validate_canonical_artifacts(benchmark_dir: Path) -> None:
    """Reject partially shaped canonical runs instead of silently skipping them."""
    errors = []
    for eval_dir in sorted(benchmark_dir.glob("eval-*")):
        for config in ("with_skill", "without_skill"):
            config_dir = eval_dir / config
            if not config_dir.is_dir():
                continue
            for run_dir in sorted(config_dir.glob("run-*")):
                required_json = (
                    run_dir / "run_manifest.json",
                    run_dir / "grading.json",
                    run_dir / "outputs" / "metrics.json",
                )
                for artifact in required_json:
                    if not artifact.is_file():
                        errors.append(f"{run_dir}: missing {artifact.relative_to(run_dir)}")
                        continue
                    try:
                        json.loads(artifact.read_text())
                    except (json.JSONDecodeError, OSError):
                        errors.append(f"{run_dir}: invalid {artifact.relative_to(run_dir)}")
                transcript = run_dir / "transcript.md"
                if not transcript.is_file():
                    errors.append(f"{run_dir}: missing transcript.md")

    if errors:
        raise ValueError("Canonical artifact validation failed:\n- " + "\n- ".join(errors))


def validate_provenance(results: dict, protocol: dict, evals_data: dict) -> None:
    """Fail closed when a frozen benchmark run cannot prove its provenance."""
    errors = []
    evals_by_id = {
        evaluation.get("id"): evaluation
        for evaluation in evals_data.get("evals", [])
        if "id" in evaluation
    }
    expected_configs = {
        "with_skill": ("candidate", protocol.get("candidate", {})),
        "without_skill": ("baseline", protocol.get("baseline", {})),
    }
    paired_runs = {}

    for config, (role, source) in expected_configs.items():
        seen_run_identities = set()
        for run in results.get(config, []):
            manifest = run.get("run_manifest")
            location = run["run_dir"]
            if not isinstance(manifest, dict):
                errors.append(f"{location}: missing or invalid run_manifest.json")
                continue

            eval_id = run["eval_id"]
            trial = run["run_number"]
            run_identity = (eval_id, trial)
            if run_identity in seen_run_identities:
                errors.append(
                    f"{location}: duplicate canonical run identity eval-{eval_id} trial-{trial} for {config}"
                )
            seen_run_identities.add(run_identity)
            trial_count = protocol.get("trials_per_eval_per_configuration")
            if not isinstance(trial, int) or trial < 1 or trial > trial_count:
                errors.append(f"{location}: trial is outside the frozen protocol range")
            evaluation = evals_by_id.get(eval_id)
            expected_prompt_hash = (
                sha256_text(evaluation.get("prompt", "")) if evaluation else None
            )
            expected_source = {
                "mode": source.get("mode", role),
            }
            if expected_source["mode"] != "no_skill":
                expected_source.update({
                    "path": source.get("path"),
                    "content_sha256": source.get("content_sha256"),
                })
                if source.get("revision"):
                    expected_source["revision"] = source["revision"]
                for source_field in ("path", "content_sha256"):
                    if not expected_source[source_field]:
                        errors.append(
                            f"protocol {config} source missing {source_field}"
                        )
            checks = {
                "eval_id": eval_id,
                "trial": trial,
                "pair_id": f"eval-{eval_id}-trial-{trial}",
                "configuration": config,
                "configuration_role": role,
                "prompt_sha256": expected_prompt_hash,
                "fixture_revision": protocol.get("fixture_revision"),
                "skill_source": expected_source,
                "executor": protocol.get("executor"),
            }
            for field, expected in checks.items():
                if expected is None:
                    errors.append(f"protocol/evals missing required provenance field for {field}")
                elif manifest.get(field) != expected:
                    errors.append(
                        f"{location}: {field} does not match frozen protocol/eval"
                    )

            expected_grader = {
                "role": "grader",
                "model": protocol.get("evaluation", {}).get("grader_model"),
            }
            if run.get("grading_evaluator") != expected_grader:
                errors.append(
                    f"{location}: grading evaluator does not match frozen protocol"
                )

            errors.extend(validate_grading_against_eval(location, run, evaluation))
            errors.extend(validate_measurement_provenance(location, run))

            order = protocol.get("paired_order", {}).get(str(trial), [])
            expected_order = order.index(config) + 1 if config in order else None
            if expected_order is None or manifest.get("execution_order") != expected_order:
                errors.append(f"{location}: execution_order does not match paired_order")

            paired_runs.setdefault((eval_id, trial), []).append(manifest)

    for (eval_id, trial), manifests in paired_runs.items():
        if len(manifests) != 2:
            continue
        shared_fields = ("pair_id", "prompt_sha256", "fixture_revision", "executor")
        for field in shared_fields:
            if manifests[0].get(field) != manifests[1].get(field):
                errors.append(
                    f"eval-{eval_id} trial-{trial}: paired {field} values differ"
                )
        if {manifest.get("execution_order") for manifest in manifests} != {1, 2}:
            errors.append(
                f"eval-{eval_id} trial-{trial}: execution_order must be exactly 1 and 2"
            )

    unexpected_configs = set(results) - set(expected_configs)
    if unexpected_configs:
        errors.append(
            "unexpected configuration directories: " + ", ".join(sorted(unexpected_configs))
        )

    if errors:
        raise ValueError("Provenance validation failed:\n- " + "\n- ".join(errors))


def validate_grading_against_eval(location: Path, run: dict, evaluation: object) -> list[str]:
    """Reject grading that does not faithfully score frozen eval expectations."""
    if not isinstance(evaluation, dict):
        return [f"{location}: eval_id does not reference a frozen eval"]

    expected_texts = evaluation.get("expectations")
    graded = run.get("expectations")
    if not isinstance(expected_texts, list) or not isinstance(graded, list):
        return [f"{location}: grading expectations do not match frozen eval"]

    errors = []
    actual_texts = []
    for index, expectation in enumerate(graded, start=1):
        label = f"{location}: grading expectation {index}"
        if not isinstance(expectation, dict):
            errors.append(f"{label} must be an object")
            continue
        actual_texts.append(expectation.get("text"))
        if not isinstance(expectation.get("text"), str):
            errors.append(f"{label} text must be a string")
        if not isinstance(expectation.get("passed"), bool):
            errors.append(f"{label} passed must be a boolean")
        if not isinstance(expectation.get("evidence"), str) or not expectation["evidence"].strip():
            errors.append(f"{label} evidence must be a non-empty string")

    if actual_texts != expected_texts:
        errors.append(f"{location}: grading expectation texts do not match frozen eval")

    summary = run.get("grading_summary")
    if not isinstance(summary, dict):
        return errors + [f"{location}: grading summary must be an object"]
    expected_counts = {
        "passed": sum(item.get("passed") is True for item in graded if isinstance(item, dict)),
        "failed": sum(item.get("passed") is False for item in graded if isinstance(item, dict)),
        "total": len(graded),
    }
    for field, expected in expected_counts.items():
        value = summary.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value != expected:
            errors.append(f"{location}: grading summary {field} does not match verdicts")

    pass_rate = summary.get("pass_rate")
    expected_rate = expected_counts["passed"] / expected_counts["total"] if expected_counts["total"] else 0.0
    if not is_number(pass_rate) or not math.isclose(float(pass_rate), expected_rate, rel_tol=0.0, abs_tol=1e-9):
        errors.append(f"{location}: grading summary pass_rate does not match verdicts")
    return errors


def validate_measurement_provenance(location: Path, run: dict) -> list[str]:
    """Ensure grader copies cannot change executor-owned measurements."""
    errors = []
    executor_metrics = run.get("executor_metrics")
    grading_metrics = run.get("grading_execution_metrics")
    if not isinstance(executor_metrics, dict):
        errors.append(f"{location}: executor metrics must be an object")
    elif isinstance(grading_metrics, dict):
        for field in ("total_tool_calls", "errors_encountered"):
            if field in grading_metrics and grading_metrics[field] != executor_metrics.get(field):
                errors.append(f"{location}: grader {field} does not match executor metrics")

    executor_timing = run.get("executor_timing")
    grading_timing = run.get("grading_timing")
    if isinstance(executor_timing, dict) and isinstance(grading_timing, dict):
        for field in ("total_duration_seconds", "total_tokens"):
            if field in grading_timing and grading_timing[field] != executor_timing.get(field):
                errors.append(f"{location}: grader {field} does not match executor timing")
    return errors


def validate_evaluation_provenance(
    benchmark_dir: Path, results: dict, protocol: dict, evals_data: dict
) -> dict:
    """Validate comparator/analyzer provenance for every completed pair."""
    errors = []
    missing_pairs = []
    validated_pairs = 0
    runs_by_pair = {}
    for config, config_results in results.items():
        for run in config_results:
            runs_by_pair.setdefault((run["eval_id"], run["run_number"]), {})[config] = run

    complete_pairs = [
        pair for pair, config_runs in runs_by_pair.items()
        if set(config_runs) == {"with_skill", "without_skill"}
    ]
    evaluation = protocol.get("evaluation", {})
    evals_by_id = {evaluation["id"]: evaluation for evaluation in evals_data["evals"]}
    for eval_id, trial in sorted(complete_pairs):
        errors_before_pair = len(errors)
        pair_id = f"eval-{eval_id}-trial-{trial}"
        comparison_dir = benchmark_dir / "comparisons" / pair_id
        files = {
            "comparison": comparison_dir / "comparison.json",
            "mapping": comparison_dir / "mapping.json",
            "analysis": comparison_dir / "analysis.json",
        }
        if not all(path.is_file() for path in files.values()):
            missing_pairs.append(pair_id)
            continue

        artifacts = {}
        for name, path in files.items():
            try:
                artifacts[name] = json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                errors.append(f"{path}: invalid JSON")
        if len(artifacts) != len(files):
            continue
        if any(not isinstance(artifact, dict) for artifact in artifacts.values()):
            errors.append(f"{pair_id}: comparison artifacts must be JSON objects")
            continue

        expected_comparator = {
            "role": "comparator",
            "model": evaluation.get("comparator_model"),
        }
        expected_analyzer = {
            "role": "analyzer",
            "model": evaluation.get("analyzer_model"),
        }
        if artifacts["comparison"].get("evaluator") != expected_comparator:
            errors.append(f"{pair_id}: comparator evaluator does not match protocol")
        if artifacts["comparison"].get("pair_id") != pair_id:
            errors.append(f"{pair_id}: comparison pair_id does not match")
        comparison_winner = artifacts["comparison"].get("winner")
        if comparison_winner not in {"A", "B", "TIE"}:
            errors.append(f"{pair_id}: comparison winner must be A, B, or TIE")
        if not isinstance(artifacts["comparison"].get("reasoning"), str) or not artifacts["comparison"]["reasoning"].strip():
            errors.append(f"{pair_id}: comparison reasoning must be a non-empty string")
        if artifacts["analysis"].get("evaluator") != expected_analyzer:
            errors.append(f"{pair_id}: analyzer evaluator does not match protocol")
        if artifacts["analysis"].get("pair_id") != pair_id:
            errors.append(f"{pair_id}: analysis pair_id does not match")
        analysis_summary = artifacts["analysis"].get("comparison_summary")
        if not isinstance(analysis_summary, dict):
            errors.append(f"{pair_id}: analysis comparison_summary must be an object")
        elif analysis_summary.get("winner") != comparison_winner:
            errors.append(f"{pair_id}: analyzer winner does not match comparison winner")
        mapping = artifacts["mapping"]
        if mapping.get("pair_id") != pair_id:
            errors.append(f"{pair_id}: mapping pair_id does not match")
        if mapping.get("comparator_model") != evaluation.get("comparator_model"):
            errors.append(f"{pair_id}: mapping comparator_model does not match protocol")
        blinded_mapping = mapping.get("mapping", {})
        if (
            set(blinded_mapping) != {"A", "B"}
            or set(blinded_mapping.values()) != {"with_skill", "without_skill"}
        ):
            errors.append(f"{pair_id}: mapping must contain both configurations")
            continue
        comparison_path = files["comparison"]
        if mapping.get("comparison_sha256") != sha256_file(comparison_path):
            errors.append(f"{pair_id}: mapping is not bound to completed comparison")
        if not isinstance(mapping.get("comparison_completed_at"), str) or not mapping["comparison_completed_at"].strip():
            errors.append(f"{pair_id}: mapping comparison_completed_at is required")

        frozen_eval = evals_by_id[eval_id]
        expected_inputs = {
            "prompt_sha256": sha256_text(frozen_eval["prompt"]),
            "expectations_sha256": sha256_json(frozen_eval["expectations"]),
        }
        comparison_inputs = artifacts["comparison"].get("input_provenance")
        if not isinstance(comparison_inputs, dict):
            errors.append(f"{pair_id}: comparison input_provenance must be an object")
        else:
            for field, expected in expected_inputs.items():
                if comparison_inputs.get(field) != expected:
                    errors.append(f"{pair_id}: comparison {field} does not match frozen eval")
            for label in ("A", "B"):
                config = blinded_mapping[label]
                run = runs_by_pair[(eval_id, trial)][config]
                expected_bundle = {
                    "transcript_sha256": sha256_file(run["run_dir"] / "transcript.md"),
                    "outputs_sha256": sha256_source(run["run_dir"] / "outputs"),
                }
                if comparison_inputs.get(label) != expected_bundle:
                    errors.append(f"{pair_id}: comparison {label} input bundle does not match canonical run")

        expected_sources = {
            "with_skill": protocol.get("candidate", {}).get("path"),
            "without_skill": protocol.get("baseline", {}).get("path"),
        }
        if comparison_winner in {"A", "B"} and isinstance(analysis_summary, dict):
            winner_config = blinded_mapping[comparison_winner]
            loser_config = blinded_mapping["B" if comparison_winner == "A" else "A"]
            if analysis_summary.get("winner_configuration") != winner_config:
                errors.append(f"{pair_id}: analyzer winner configuration does not match mapping")
            if analysis_summary.get("loser_configuration") != loser_config:
                errors.append(f"{pair_id}: analyzer loser configuration does not match mapping")
            if analysis_summary.get("winner_skill") != expected_sources[winner_config]:
                errors.append(f"{pair_id}: analyzer winner skill does not match mapping")
            if analysis_summary.get("loser_skill") != expected_sources[loser_config]:
                errors.append(f"{pair_id}: analyzer loser skill does not match mapping")
        elif comparison_winner == "TIE" and isinstance(analysis_summary, dict):
            if analysis_summary.get("configuration_a") != blinded_mapping["A"]:
                errors.append(f"{pair_id}: tie configuration_a does not match mapping")
            if analysis_summary.get("configuration_b") != blinded_mapping["B"]:
                errors.append(f"{pair_id}: tie configuration_b does not match mapping")
            if analysis_summary.get("skill_a") != expected_sources[blinded_mapping["A"]]:
                errors.append(f"{pair_id}: tie skill_a does not match mapping")
            if analysis_summary.get("skill_b") != expected_sources[blinded_mapping["B"]]:
                errors.append(f"{pair_id}: tie skill_b does not match mapping")
            if not isinstance(artifacts["analysis"].get("tie_analysis"), dict):
                errors.append(f"{pair_id}: tie analysis must include tie_analysis")
        if len(errors) == errors_before_pair:
            validated_pairs += 1

    if errors:
        raise ValueError("Evaluation provenance validation failed:\n- " + "\n- ".join(errors))

    return {
        "status": "passed" if not missing_pairs else "incomplete",
        "completed_pairs": len(complete_pairs),
        "validated_pairs": validated_pairs,
        "missing_pairs": missing_pairs,
    }


def generate_benchmark(benchmark_dir: Path, skill_name: str = "", skill_path: str = "") -> dict:
    """
    Generate complete benchmark.json from run results.
    """
    protocol = None
    protocol_file = benchmark_dir / "protocol.json"
    if protocol_file.exists():
        try:
            with open(protocol_file) as pf:
                protocol = json.load(pf)
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError(f"Invalid protocol.json: {error}") from error

    if protocol is not None:
        validate_canonical_artifacts(benchmark_dir)

    results = load_run_results(benchmark_dir)
    if protocol is not None:
        results.setdefault("with_skill", [])
        results.setdefault("without_skill", [])

    # Build runs array for benchmark.json
    runs = []
    for config in results:
        for result in results[config]:
            runs.append({
                "eval_id": result["eval_id"],
                "configuration": config,
                "run_number": result["run_number"],
                "result": {
                    "pass_rate": result["pass_rate"],
                    "passed": result["passed"],
                    "failed": result["failed"],
                    "total": result["total"],
                    "time_seconds": result["time_seconds"],
                    "tokens": result.get("tokens"),
                    "tool_calls": result.get("tool_calls", 0),
                    "errors": result.get("errors", 0)
                },
                "expectations": result["expectations"],
                "notes": result["notes"]
            })

    # Determine completed eval IDs from results, then load the frozen eval set so
    # an entirely missing eval is represented as zero coverage rather than
    # disappearing from the matrix.
    completed_eval_ids = sorted(set(
        r["eval_id"]
        for config in results.values()
        for r in config
    ))

    evals_data = {}
    planned_eval_ids = []
    evals_file = benchmark_dir / "evals" / "evals.json"
    if evals_file.exists():
        try:
            with open(evals_file) as ef:
                evals_data = json.load(ef)
            planned_eval_ids = [
                evaluation["id"]
                for evaluation in evals_data.get("evals", [])
                if "id" in evaluation
            ]
        except (json.JSONDecodeError, OSError):
            pass
    coverage_eval_ids = sorted(set(completed_eval_ids) | set(planned_eval_ids))

    if protocol is not None:
        if not evals_data:
            raise ValueError("Frozen protocol requires a valid evals/evals.json")
        validate_protocol(protocol, evals_file)
        validate_provenance(results, protocol, evals_data)

    evaluation_provenance = (
        validate_evaluation_provenance(benchmark_dir, results, protocol, evals_data)
        if protocol is not None
        else {
            "status": "not_run",
            "completed_pairs": 0,
            "validated_pairs": 0,
            "missing_pairs": [],
        }
    )

    run_summary = aggregate_results(results)

    completed_runs_per_configuration = {
        config: len(config_results) for config, config_results in results.items()
    }
    completed_runs_by_eval = {
        str(eval_id): {
            config: sum(1 for run in config_results if run["eval_id"] == eval_id)
            for config, config_results in results.items()
        }
        for eval_id in coverage_eval_ids
    }
    per_eval_counts = [
        count
        for config_counts in completed_runs_by_eval.values()
        for count in config_counts.values()
    ]
    uniform_runs_per_configuration = (
        per_eval_counts[0]
        if per_eval_counts and len(set(per_eval_counts)) == 1
        else None
    )

    planned_runs = (
        protocol.get("trials_per_eval_per_configuration")
        if protocol is not None
        else None
    )

    benchmark = {
        "metadata": {
            "skill_name": skill_name or "<skill-name>",
            "skill_path": skill_path or "<path/to/skill>",
            "executor_model": (
                protocol.get("executor", {}).get("model")
                if protocol is not None
                else "<model-name>"
            ),
            "analyzer_model": (
                protocol.get("evaluation", {}).get("analyzer_model")
                if protocol is not None
                else "<model-name>"
            ),
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": completed_eval_ids,
            "evals_planned": planned_eval_ids,
            "runs_per_configuration": uniform_runs_per_configuration,
            "planned_runs_per_eval_per_configuration": planned_runs,
            "completed_runs_per_configuration": completed_runs_per_configuration,
            "completed_runs_by_eval": completed_runs_by_eval,
            "run_provenance_validation": "passed" if protocol is not None else "not_run",
            "evaluation_provenance_validation": evaluation_provenance["status"],
            "provenance_validation": (
                evaluation_provenance["status"] if protocol is not None else "not_run"
            ),
            "blind_comparisons_completed": evaluation_provenance["completed_pairs"],
            "blind_comparisons_validated": evaluation_provenance["validated_pairs"],
            "blind_comparisons_missing": evaluation_provenance["missing_pairs"],
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": []  # To be filled by analyzer
    }

    return benchmark


def generate_markdown(benchmark: dict) -> str:
    """Generate human-readable benchmark.md from benchmark data."""
    metadata = benchmark["metadata"]
    run_summary = benchmark["run_summary"]

    # Determine config names (excluding "delta")
    configs = [k for k in run_summary if k != "delta"]
    config_a = configs[0] if len(configs) >= 1 else "config_a"
    config_b = configs[1] if len(configs) >= 2 else "config_b"
    label_a = config_a.replace("_", " ").title()
    label_b = config_b.replace("_", " ").title()

    completed = metadata.get("completed_runs_per_configuration", {})
    completed_text = ", ".join(
        f"{config}={count}" for config, count in completed.items()
    ) or "none"
    planned = metadata.get("planned_runs_per_eval_per_configuration")
    plan_text = f"; planned {planned} per eval/config" if planned is not None else ""

    lines = [
        f"# Skill Benchmark: {metadata['skill_name']}",
        "",
        f"**Model**: {metadata['executor_model']}",
        f"**Date**: {metadata['timestamp']}",
        f"**Evals with results**: {', '.join(map(str, metadata['evals_run'])) or 'none'}",
        f"**Planned evals**: {', '.join(map(str, metadata.get('evals_planned', []))) or 'unavailable'}",
        f"**Completed runs**: {completed_text}{plan_text}",
        "",
        "## Summary",
        "",
        f"| Metric | {label_a} | {label_b} | Delta |",
        "|--------|------------|---------------|-------|",
    ]

    a_summary = run_summary.get(config_a, {})
    b_summary = run_summary.get(config_b, {})
    delta = run_summary.get("delta", {})

    # Format pass rate
    a_pr = a_summary.get("pass_rate", {})
    b_pr = b_summary.get("pass_rate", {})
    def format_stat(stat: dict, *, percent: bool = False, suffix: str = "") -> str:
        mean = stat.get("mean")
        stddev = stat.get("stddev")
        available = stat.get("available_count", 0)
        total = stat.get("total_count", 0)
        coverage = (
            f" ({available}/{total} measured)"
            if total and available != total
            else ""
        )
        if not is_number(mean) or not is_number(stddev):
            return f"unavailable{coverage}"
        multiplier = 100 if percent else 1
        digits = 0 if percent or suffix == "" else 1
        return (
            f"{mean * multiplier:.{digits}f}{suffix} ± "
            f"{stddev * multiplier:.{digits}f}{suffix}{coverage}"
        )

    lines.append(f"| Pass Rate | {format_stat(a_pr, percent=True, suffix='%')} | {format_stat(b_pr, percent=True, suffix='%')} | {delta.get('pass_rate', '—')} |")

    # Format time
    a_time = a_summary.get("time_seconds", {})
    b_time = b_summary.get("time_seconds", {})
    time_delta = delta.get("time_seconds", "—")
    time_delta = f"{time_delta}s" if time_delta != "—" else time_delta
    lines.append(f"| Time | {format_stat(a_time, suffix='s')} | {format_stat(b_time, suffix='s')} | {time_delta} |")

    # Format tokens
    a_tokens = a_summary.get("tokens", {})
    b_tokens = b_summary.get("tokens", {})
    lines.append(f"| Tokens | {format_stat(a_tokens)} | {format_stat(b_tokens)} | {delta.get('tokens', '—')} |")

    # Notes section
    if benchmark.get("notes"):
        lines.extend([
            "",
            "## Notes",
            ""
        ])
        for note in benchmark["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate benchmark run results into summary statistics"
    )
    parser.add_argument(
        "benchmark_dir",
        type=Path,
        help="Path to the benchmark directory"
    )
    parser.add_argument(
        "--skill-name",
        default="",
        help="Name of the skill being benchmarked"
    )
    parser.add_argument(
        "--skill-path",
        default="",
        help="Path to the skill being benchmarked"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output path for benchmark.json (default: <benchmark_dir>/benchmark.json)"
    )

    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"Directory not found: {args.benchmark_dir}")
        sys.exit(1)

    # Generate benchmark
    try:
        benchmark = generate_benchmark(args.benchmark_dir, args.skill_name, args.skill_path)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)

    # Determine output paths
    output_json = args.output or (args.benchmark_dir / "benchmark.json")
    output_md = output_json.with_suffix(".md")

    # Write benchmark.json
    with open(output_json, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"Generated: {output_json}")

    # Write benchmark.md
    markdown = generate_markdown(benchmark)
    with open(output_md, "w") as f:
        f.write(markdown)
    print(f"Generated: {output_md}")

    # Print summary
    run_summary = benchmark["run_summary"]
    configs = [k for k in run_summary if k != "delta"]
    delta = run_summary.get("delta", {})

    print(f"\nSummary:")
    for config in configs:
        pr = run_summary[config]["pass_rate"]["mean"]
        label = config.replace("_", " ").title()
        if is_number(pr):
            print(f"  {label}: {pr*100:.1f}% pass rate")
        else:
            print(f"  {label}: unavailable pass rate")
    print(f"  Delta:         {delta.get('pass_rate', '—')}")


if __name__ == "__main__":
    main()

"""Unit tests for stage logic, with run_cmd mocked.

We don't want to spawn npm/cargo/dotnet during unit tests. These tests
verify that each stage picks the right commands based on detection
state and config, and bails on dep-install failure.
"""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from pipeline_guard.config import PipelineConfig
from pipeline_guard.detect import Detection
from pipeline_guard.stages import (
    run_dotnet,
    run_go,
    run_node,
    run_python,
    run_rust,
    run_vulns,
)
from pipeline_guard.types import Status, StepResult

# ---------------------------------------------------------------------------
# Recording mock for run_cmd
# ---------------------------------------------------------------------------

class CallRecorder:
    """Replaces run_cmd. Records calls and returns scripted results."""

    def __init__(self, default_status: Status = Status.PASSED) -> None:
        self.calls: list[dict[str, Any]] = []
        self.default_status = default_status
        # Map step-name → status to override per-call.
        self.overrides: dict[str, Status] = {}

    def __call__(
        self,
        cmd: Sequence[str],
        *,
        cwd: Path,
        name: str,
        timeout: int,
        env: dict[str, str] | None = None,
        required: bool = True,
        stream: bool = True,
        indent: str = "   ",
    ) -> StepResult:
        self.calls.append({"cmd": list(cmd), "name": name, "timeout": timeout,
                           "required": required})
        status = self.overrides.get(name, self.default_status)
        return StepResult(
            name=name,
            status=status,
            duration_s=0.01,
            returncode=0 if status == Status.PASSED else 1,
            message="" if status == Status.PASSED else "mocked failure",
        )

    def cmds(self) -> list[list[str]]:
        return [c["cmd"] for c in self.calls]

    def names(self) -> list[str]:
        return [c["name"] for c in self.calls]


@pytest.fixture
def cfg() -> PipelineConfig:
    return PipelineConfig()


@pytest.fixture
def recorder() -> CallRecorder:
    return CallRecorder()


def _patch_stage(module_attr: str, recorder: CallRecorder) -> Any:
    """Patch `run_cmd` inside `pipeline_guard.stages`."""
    return patch(f"pipeline_guard.stages.{module_attr}", recorder)


# ---------------------------------------------------------------------------
# Python stage
# ---------------------------------------------------------------------------

def test_python_with_requirements_uses_pip(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    (tmp_project / "requirements.txt").write_text("requests\n")
    d = Detection(python=True, has_requirements=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_python(tmp_project, d, cfg, results)
    # First call must be venv creation, then a pip install with -r requirements.txt
    cmds = recorder.cmds()
    assert any("venv" in " ".join(c) for c in cmds)
    pip_calls = [c for c in cmds if "pip" in c and "install" in c]
    assert pip_calls, f"no pip install call recorded: {cmds}"
    assert any("requirements.txt" in c for c in pip_calls)


def test_python_no_manifest_skips(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    d = Detection(python=True)  # python flag set but no manifest
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_python(tmp_project, d, cfg, results)
    # Expect a SKIPPED py:deps step
    statuses = {r.name: r.status for r in results}
    assert statuses.get("py:deps") == Status.SKIPPED


def test_python_deps_failure_short_circuits(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    (tmp_project / "requirements.txt").write_text("requests\n")
    d = Detection(python=True, has_requirements=True)
    rec = CallRecorder()
    rec.overrides["py:deps(requirements)"] = Status.FAILED
    results: list[StepResult] = []
    with _patch_stage("run_cmd", rec):
        run_python(tmp_project, d, cfg, results)
    # We should NOT have tried to lint/test after dep install failed.
    names = [r.name for r in results]
    assert "py:lint(ruff)" not in names
    assert "py:test(pytest)" not in names


# ---------------------------------------------------------------------------
# Node stage
# ---------------------------------------------------------------------------

def test_node_npm_with_lockfile_uses_ci(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    (tmp_project / "package.json").write_text(
        '{"scripts": {"lint": "eslint .", "test": "jest", "build": "tsc"}}'
    )
    (tmp_project / "package-lock.json").write_text("{}")
    d = Detection(node=True, node_pm="npm", has_package_lock=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    # npm ci must be the first command
    assert recorder.cmds()[0][:2] == ["npm", "ci"]
    # Should also try lint, test, build (typecheck is missing → SKIPPED)
    names = recorder.names()
    assert "node:lint" in names
    assert "node:test" in names
    assert "node:build" in names


def test_node_npm_without_lockfile_uses_install(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    (tmp_project / "package.json").write_text("{}")
    d = Detection(node=True, node_pm="npm")
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0][:2] == ["npm", "install"]


def test_node_pnpm_frozen(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    (tmp_project / "package.json").write_text("{}")
    d = Detection(node=True, node_pm="pnpm", has_pnpm_lock=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0] == ["pnpm", "install", "--frozen-lockfile"]


def test_node_yarn_frozen(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    (tmp_project / "package.json").write_text("{}")
    d = Detection(node=True, node_pm="yarn", has_yarn_lock=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0] == ["yarn", "install", "--frozen-lockfile"]


def test_node_missing_script_skipped(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    (tmp_project / "package.json").write_text('{"scripts": {"test": "jest"}}')
    d = Detection(node=True, node_pm="npm")
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    by_name = {r.name: r.status for r in results}
    # test exists → would run (PASSED via mock); lint/build/typecheck → SKIPPED
    assert by_name.get("node:lint") == Status.SKIPPED
    assert by_name.get("node:build") == Status.SKIPPED
    assert by_name.get("node:typecheck") == Status.SKIPPED


def test_node_malformed_package_json(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    # Bad JSON → treated as empty scripts, not a crash.
    (tmp_project / "package.json").write_text("{not valid json")
    d = Detection(node=True, node_pm="npm")
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    # We still install, then all 4 scripts are skipped.
    by_name = {r.name: r.status for r in results}
    for s in ("node:lint", "node:typecheck", "node:test", "node:build"):
        assert by_name.get(s) == Status.SKIPPED


# ---------------------------------------------------------------------------
# .NET / Go / Rust short-circuit on dep failure
# ---------------------------------------------------------------------------

def test_dotnet_restore_failure_stops(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    rec = CallRecorder()
    rec.overrides["dotnet:restore"] = Status.FAILED
    results: list[StepResult] = []
    with _patch_stage("run_cmd", rec):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    names = [r.name for r in results]
    assert "dotnet:build" not in names
    assert "dotnet:test" not in names


def test_go_full_pipeline(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_go(tmp_project, Detection(go=True), cfg, results)
    names = recorder.names()
    assert names == ["go:deps", "go:vet", "go:build", "go:test"]


def test_rust_dep_failure_stops(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    rec = CallRecorder()
    rec.overrides["rust:deps"] = Status.FAILED
    results: list[StepResult] = []
    with _patch_stage("run_cmd", rec):
        run_rust(tmp_project, Detection(rust=True), cfg, results)
    names = [r.name for r in results]
    assert "rust:build" not in names
    assert "rust:test" not in names


# ---------------------------------------------------------------------------
# Vulnerability stage
# ---------------------------------------------------------------------------

def test_vulns_no_scanners_available(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    # No scanners on PATH → we expect a single SKIPPED step.
    with patch("pipeline_guard.stages.shutil.which", return_value=None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_vulns(tmp_project, Detection(python=True, node=True), cfg, results)
    assert len(results) == 1
    assert results[0].status == Status.SKIPPED
    assert results[0].name == "vulns"

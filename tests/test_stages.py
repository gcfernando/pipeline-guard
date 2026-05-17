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

from pipewarden.config import PipelineConfig
from pipewarden.detect import Detection
from pipewarden.stages import (
    _docker_daemon_available,
    _in_ci,
    _run_container_scan,
    run_docker,
    run_dotnet,
    run_go,
    run_node,
    run_outdated,
    run_python,
    run_rust,
    run_vulns,
)
from pipewarden.types import Status, StepResult


class CallRecorder:
    """Replaces run_cmd. Records calls and returns scripted results."""

    def __init__(self, default_status: Status = Status.PASSED) -> None:
        """Initialise the recorder with a default status for all calls unless overridden."""
        self.calls: list[dict[str, Any]] = []
        self.default_status = default_status
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
        retries: int = 0,
        backoff_base: float = 2.0,
    ) -> StepResult:
        """Record the call and return a StepResult using the override map or the default status."""
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
        """Return just the command lists from all recorded calls."""
        return [c["cmd"] for c in self.calls]

    def names(self) -> list[str]:
        """Return just the step names from all recorded calls."""
        return [c["name"] for c in self.calls]


@pytest.fixture
def cfg() -> PipelineConfig:
    """Provide a default PipelineConfig for each test."""
    return PipelineConfig()


@pytest.fixture
def recorder() -> CallRecorder:
    """Provide a fresh CallRecorder that defaults to PASSED for each test."""
    return CallRecorder()


def _patch_stage(module_attr: str, recorder: CallRecorder) -> Any:
    """Return a context manager that replaces the named attribute in pipewarden.stages with recorder."""
    return patch(f"pipewarden.stages.{module_attr}", recorder)


# ---------------------------------------------------------------------------
# Python stage
# ---------------------------------------------------------------------------

def test_python_with_requirements_uses_pip(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """A project with requirements.txt should create a venv then install with pip -r requirements.txt."""
    (tmp_project / "requirements.txt").write_text("requests\n")
    d = Detection(python=True, has_requirements=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_python(tmp_project, d, cfg, results)
    cmds = recorder.cmds()
    assert any("venv" in " ".join(c) for c in cmds)
    pip_calls = [c for c in cmds if "pip" in c and "install" in c]
    assert pip_calls, f"no pip install call recorded: {cmds}"
    assert any("requirements.txt" in c for c in pip_calls)


def test_python_no_manifest_skips(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Python detected but no manifest file should produce a SKIPPED py:deps step."""
    d = Detection(python=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_python(tmp_project, d, cfg, results)
    statuses = {r.name: r.status for r in results}
    assert statuses.get("py:deps") == Status.SKIPPED


def test_python_deps_failure_short_circuits(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    """A failed dep install should prevent lint and test steps from running."""
    (tmp_project / "requirements.txt").write_text("requests\n")
    d = Detection(python=True, has_requirements=True)
    rec = CallRecorder()
    rec.overrides["py:deps(requirements)"] = Status.FAILED
    results: list[StepResult] = []
    with _patch_stage("run_cmd", rec):
        run_python(tmp_project, d, cfg, results)
    names = [r.name for r in results]
    assert "py:lint(ruff)" not in names
    assert "py:test(pytest)" not in names


# ---------------------------------------------------------------------------
# Node stage
# ---------------------------------------------------------------------------

def test_node_npm_with_lockfile_uses_ci(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """With a package-lock.json present, npm ci should be used and lint/test/build scripts should run."""
    (tmp_project / "package.json").write_text(
        '{"scripts": {"lint": "eslint .", "test": "jest", "build": "tsc"}}'
    )
    (tmp_project / "package-lock.json").write_text("{}")
    d = Detection(node=True, node_pm="npm", has_package_lock=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0][:2] == ["npm", "ci"]
    names = recorder.names()
    assert "node:lint" in names
    assert "node:test" in names
    assert "node:build" in names


def test_node_npm_without_lockfile_uses_install(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Without a lock file, npm install should be used instead of npm ci."""
    (tmp_project / "package.json").write_text("{}")
    d = Detection(node=True, node_pm="npm")
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0][:2] == ["npm", "install"]


def test_node_pnpm_frozen(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """pnpm with a lockfile should use --frozen-lockfile to ensure reproducible installs."""
    (tmp_project / "package.json").write_text("{}")
    d = Detection(node=True, node_pm="pnpm", has_pnpm_lock=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0] == ["pnpm", "install", "--frozen-lockfile"]


def test_node_yarn_frozen(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """yarn with a lockfile should use --frozen-lockfile to ensure reproducible installs."""
    (tmp_project / "package.json").write_text("{}")
    d = Detection(node=True, node_pm="yarn", has_yarn_lock=True)
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    assert recorder.cmds()[0] == ["yarn", "install", "--frozen-lockfile"]


def test_node_missing_script_skipped(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Scripts not present in package.json should produce SKIPPED steps rather than errors."""
    (tmp_project / "package.json").write_text('{"scripts": {"test": "jest"}}')
    d = Detection(node=True, node_pm="npm")
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    by_name = {r.name: r.status for r in results}
    assert by_name.get("node:lint") == Status.SKIPPED
    assert by_name.get("node:build") == Status.SKIPPED
    assert by_name.get("node:typecheck") == Status.SKIPPED


def test_node_malformed_package_json(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """A package.json with invalid JSON should be treated as empty scripts without crashing."""
    (tmp_project / "package.json").write_text("{not valid json")
    d = Detection(node=True, node_pm="npm")
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_node(tmp_project, d, cfg, results)
    by_name = {r.name: r.status for r in results}
    for s in ("node:lint", "node:typecheck", "node:test", "node:build"):
        assert by_name.get(s) == Status.SKIPPED


# ---------------------------------------------------------------------------
# .NET / Go / Rust short-circuit on dep failure
# ---------------------------------------------------------------------------

def test_dotnet_restore_failure_stops(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    """A failed dotnet:restore should prevent build and test steps from running."""
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
    """The Go stage should run deps, vet, build, and test in that exact order."""
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_go(tmp_project, Detection(go=True), cfg, results)
    names = recorder.names()
    assert names == ["go:deps", "go:vet", "go:build", "go:test"]


def test_rust_dep_failure_stops(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    """A failed rust:deps step should prevent build and test steps from running."""
    rec = CallRecorder()
    rec.overrides["rust:deps"] = Status.FAILED
    results: list[StepResult] = []
    with _patch_stage("run_cmd", rec):
        run_rust(tmp_project, Detection(rust=True), cfg, results)
    names = [r.name for r in results]
    assert "rust:build" not in names
    assert "rust:test" not in names


# ---------------------------------------------------------------------------
# Docker stage
# ---------------------------------------------------------------------------

def test_docker_build_without_hadolint(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When hadolint is not installed, only docker:build should run — no lint step."""
    with patch("pipewarden.stages.shutil.which", return_value=None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_docker(tmp_project, Detection(docker=True), cfg, results)
    names = [r.name for r in results]
    assert names == ["docker:build"]
    assert "docker:lint(hadolint)" not in names


def test_docker_build_with_hadolint(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When hadolint is installed, lint should run before build."""
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "hadolint" else None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_docker(tmp_project, Detection(docker=True), cfg, results)
    names = [r.name for r in results]
    assert "docker:lint(hadolint)" in names
    assert "docker:build" in names
    assert names.index("docker:lint(hadolint)") < names.index("docker:build")


# ---------------------------------------------------------------------------
# Vulnerability stage
# ---------------------------------------------------------------------------

def test_vulns_no_scanners_available(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When no vulnerability scanners are on PATH, a single SKIPPED 'vulns' step should be emitted."""
    with patch("pipewarden.stages.shutil.which", return_value=None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_vulns(tmp_project, Detection(python=True, node=True), cfg, results)
    assert len(results) == 1
    assert results[0].status == Status.SKIPPED
    assert results[0].name == "vulns"


def test_vulns_with_pip_audit(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When pip-audit is available for a Python project, vulns:pip-audit should run."""
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "pip-audit" else None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_vulns(tmp_project, Detection(python=True), cfg, results)
    names = [r.name for r in results]
    assert "vulns:pip-audit" in names


def test_vulns_with_npm_audit(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When npm is available for a Node project, vulns:npm-audit should run."""
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "npm" else None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_vulns(tmp_project, Detection(node=True), cfg, results)
    names = [r.name for r in results]
    assert "vulns:npm-audit" in names


def test_vulns_with_cargo_audit(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When cargo-audit is available for a Rust project, vulns:cargo-audit should run."""
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "cargo-audit" else None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_vulns(tmp_project, Detection(rust=True), cfg, results)
    names = [r.name for r in results]
    assert "vulns:cargo-audit" in names


def test_vulns_with_govulncheck(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When govulncheck is available for a Go project, vulns:govulncheck should run."""
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "govulncheck" else None):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_vulns(tmp_project, Detection(go=True), cfg, results)
    names = [r.name for r in results]
    assert "vulns:govulncheck" in names


def test_rust_with_clippy(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When cargo-clippy is available, rust:lint(clippy) should be included in the pipeline."""
    with patch("pipewarden.stages.shutil.which", return_value="cargo-clippy"):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_rust(tmp_project, Detection(rust=True), cfg, results)
    names = recorder.names()
    assert "rust:lint(clippy)" in names


# ---------------------------------------------------------------------------
# _in_ci helper
# ---------------------------------------------------------------------------

def test_in_ci_false(monkeypatch: pytest.MonkeyPatch) -> None:
    """With all CI environment variables unset, _in_ci() should return False."""
    for var in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "TF_BUILD"):
        monkeypatch.delenv(var, raising=False)
    assert _in_ci() is False


def test_in_ci_true_via_ci_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """CI=true should be enough for _in_ci() to return True."""
    monkeypatch.setenv("CI", "true")
    assert _in_ci() is True


def test_in_ci_true_via_github_actions(monkeypatch: pytest.MonkeyPatch) -> None:
    """GITHUB_ACTIONS=true (with no CI var) should also make _in_ci() return True."""
    for var in ("CI", "GITLAB_CI", "TF_BUILD"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert _in_ci() is True


# ---------------------------------------------------------------------------
# Docker daemon availability and WARNED vs FAILED
# ---------------------------------------------------------------------------

def test_docker_daemon_no_cmd() -> None:
    """_docker_daemon_available() should return False when docker is not on PATH."""
    with patch("pipewarden.stages.shutil.which", return_value=None):
        assert _docker_daemon_available() is False


def test_docker_unavailable_ci_warns(
    tmp_project: Path, cfg: PipelineConfig, monkeypatch: pytest.MonkeyPatch
) -> None:
    """In a CI environment without a docker daemon, docker:build should be WARNED rather than FAILED."""
    monkeypatch.setenv("CI", "true")
    with (patch("pipewarden.stages._docker_daemon_available", return_value=False),
          patch("pipewarden.stages.shutil.which", return_value=None)):
        results: list[StepResult] = []
        run_docker(tmp_project, Detection(docker=True), cfg, results)
    build_step = next(r for r in results if r.name == "docker:build")
    assert build_step.status == Status.WARNED


def test_docker_unavailable_local_fails(
    tmp_project: Path, cfg: PipelineConfig, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Locally (no CI var), a missing docker daemon should produce a hard FAILED build step."""
    for var in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "TF_BUILD"):
        monkeypatch.delenv(var, raising=False)
    with (patch("pipewarden.stages._docker_daemon_available", return_value=False),
          patch("pipewarden.stages.shutil.which", return_value=None)):
        results: list[StepResult] = []
        run_docker(tmp_project, Detection(docker=True), cfg, results)
    build_step = next(r for r in results if r.name == "docker:build")
    assert build_step.status == Status.FAILED


# ---------------------------------------------------------------------------
# .NET — new steps (format, vulns, outdated)
# ---------------------------------------------------------------------------

def test_dotnet_full_pipeline_default_config(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Default config should run restore, format, build, test, and vulns — but not outdated (opt-in)."""
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    names = recorder.names()
    assert "dotnet:restore" in names
    assert "dotnet:format" in names
    assert "dotnet:build" in names
    assert "dotnet:test" in names
    assert "dotnet:vulns" in names
    assert "dotnet:outdated" not in names


def test_dotnet_format_and_vulns_disabled(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Setting format=False and vulns=False should omit those steps while keeping build and test."""
    cfg.dotnet.format = False
    cfg.dotnet.vulns = False
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    names = recorder.names()
    assert "dotnet:format" not in names
    assert "dotnet:vulns" not in names
    assert "dotnet:build" in names
    assert "dotnet:test" in names


def test_dotnet_outdated_enabled(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Setting outdated=True should include the dotnet:outdated step in the pipeline."""
    cfg.dotnet.outdated = True
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    assert "dotnet:outdated" in recorder.names()


def test_dotnet_build_failure_skips_vulns_and_outdated(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    """A failed dotnet:build should prevent test, vulns, and outdated from running."""
    cfg.dotnet.outdated = True
    rec = CallRecorder()
    rec.overrides["dotnet:build"] = Status.FAILED
    results: list[StepResult] = []
    with _patch_stage("run_cmd", rec):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    names = [r.name for r in results]
    assert "dotnet:test" not in names
    assert "dotnet:vulns" not in names
    assert "dotnet:outdated" not in names


def test_dotnet_format_runs_before_build(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """dotnet:format must appear before dotnet:build in the execution order."""
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    names = recorder.names()
    assert names.index("dotnet:format") < names.index("dotnet:build")


def test_dotnet_vulns_runs_after_test(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """dotnet:vulns must appear after dotnet:test so a broken build doesn't produce misleading vuln results."""
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_dotnet(tmp_project, Detection(dotnet=True), cfg, results)
    names = recorder.names()
    assert names.index("dotnet:test") < names.index("dotnet:vulns")


# ---------------------------------------------------------------------------
# Docker container image scanning
# ---------------------------------------------------------------------------

def test_docker_scan_trivy_after_successful_build(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When trivy is installed, docker:scan(trivy) should run after a successful docker:build."""
    with (patch("pipewarden.stages._docker_daemon_available", return_value=True),
          patch("pipewarden.stages.shutil.which",
                side_effect=lambda x: x if x == "trivy" else None)):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_docker(tmp_project, Detection(docker=True), cfg, results)
    names = recorder.names()
    assert "docker:build" in names
    assert "docker:scan(trivy)" in names
    assert names.index("docker:build") < names.index("docker:scan(trivy)")


def test_docker_scan_grype_when_trivy_absent(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When trivy is absent but grype is installed, docker:scan(grype) should run instead."""
    with (patch("pipewarden.stages._docker_daemon_available", return_value=True),
          patch("pipewarden.stages.shutil.which",
                side_effect=lambda x: x if x == "grype" else None)):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_docker(tmp_project, Detection(docker=True), cfg, results)
    names = recorder.names()
    assert "docker:scan(grype)" in names
    assert "docker:scan(trivy)" not in names


def test_docker_scan_skipped_when_no_scanner_available(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When neither trivy nor grype is installed, no scan step should be emitted."""
    with (patch("pipewarden.stages._docker_daemon_available", return_value=True),
          patch("pipewarden.stages.shutil.which", return_value=None)):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", recorder):
            run_docker(tmp_project, Detection(docker=True), cfg, results)
    names = recorder.names()
    assert "docker:scan(trivy)" not in names
    assert "docker:scan(grype)" not in names


def test_docker_scan_not_called_when_build_fails(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    """A failed docker:build should prevent the container scan from running."""
    rec = CallRecorder()
    rec.overrides["docker:build"] = Status.FAILED
    with (patch("pipewarden.stages._docker_daemon_available", return_value=True),
          patch("pipewarden.stages.shutil.which",
                side_effect=lambda x: x if x == "trivy" else None)):
        results: list[StepResult] = []
        with _patch_stage("run_cmd", rec):
            run_docker(tmp_project, Detection(docker=True), cfg, results)
    names = [r.name for r in results]
    assert "docker:scan(trivy)" not in names


def test_run_container_scan_trivy_preferred_over_grype(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When both trivy and grype are available, trivy should be preferred."""
    with patch("pipewarden.stages.shutil.which", return_value="found"), \
         _patch_stage("run_cmd", recorder):
        _run_container_scan(cfg.docker_tag, tmp_project, cfg, [])
    names = recorder.names()
    assert "docker:scan(trivy)" in names
    assert "docker:scan(grype)" not in names


# ---------------------------------------------------------------------------
# Outdated stage
# ---------------------------------------------------------------------------

def test_outdated_python_with_venv(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When a .pipewarden-venv exists, outdated:python(pip) should run."""
    venv = tmp_project / ".pipewarden-venv"
    venv.mkdir()
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(python=True), cfg, results)
    assert "outdated:python(pip)" in recorder.names()


def test_outdated_python_no_venv_skipped(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Without a venv directory, outdated:python(pip) should be SKIPPED since pip is not available."""
    results: list[StepResult] = []
    with _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(python=True), cfg, results)
    by_name = {r.name: r.status for r in results}
    assert by_name.get("outdated:python(pip)") == Status.SKIPPED


def test_outdated_node_npm(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When npm is on PATH for a Node project, outdated:node(npm) should run."""
    results: list[StepResult] = []
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "npm" else None), \
         _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(node=True, node_pm="npm"), cfg, results)
    assert "outdated:node(npm)" in recorder.names()


def test_outdated_go(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When go is on PATH, outdated:go should run for a Go project."""
    results: list[StepResult] = []
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "go" else None), \
         _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(go=True), cfg, results)
    assert "outdated:go" in recorder.names()


def test_outdated_rust_cargo_outdated(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """When cargo-outdated is installed, outdated:rust(cargo-outdated) should run."""
    results: list[StepResult] = []
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "cargo-outdated" else None), \
         _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(rust=True), cfg, results)
    assert "outdated:rust(cargo-outdated)" in recorder.names()


def test_outdated_rust_skipped_without_cargo_outdated(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """Without cargo-outdated installed, the Rust outdated check should be SKIPPED."""
    results: list[StepResult] = []
    with patch("pipewarden.stages.shutil.which", return_value=None), \
         _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(rust=True), cfg, results)
    assert results[0].status == Status.SKIPPED


def test_outdated_no_languages_skipped(
    tmp_project: Path, cfg: PipelineConfig, recorder: CallRecorder
) -> None:
    """An empty detection with no languages should produce a single SKIPPED result."""
    results: list[StepResult] = []
    with patch("pipewarden.stages.shutil.which", return_value=None), \
         _patch_stage("run_cmd", recorder):
        run_outdated(tmp_project, Detection(), cfg, results)
    assert len(results) == 1
    assert results[0].status == Status.SKIPPED


def test_outdated_steps_are_non_blocking(
    tmp_project: Path, cfg: PipelineConfig
) -> None:
    """Outdated checks should never produce FAILED — a non-zero exit becomes WARNED."""
    rec = CallRecorder(default_status=Status.WARNED)
    results: list[StepResult] = []
    with patch("pipewarden.stages.shutil.which",
               side_effect=lambda x: x if x == "npm" else None), \
         _patch_stage("run_cmd", rec):
        run_outdated(tmp_project, Detection(node=True, node_pm="npm"), cfg, results)
    for r in results:
        assert r.status != Status.FAILED

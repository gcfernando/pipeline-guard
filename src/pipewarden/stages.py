"""Per-language stage runners.

Each `run_*` function appends StepResults to the given list. It does NOT
raise on failure — failures are collected and returned for the summary.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path

from .config import PipelineConfig
from .detect import Detection
from .runner import run_cmd
from .types import Status, StepResult

# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------

def _pyproject_has_section(root: Path, dotted: str) -> bool:
    """Return True if pyproject.toml contains the given dotted section."""
    if sys.version_info >= (3, 11):
        import tomllib
    else:  # pragma: no cover
        import tomli as tomllib  # type: ignore[no-redef,import-not-found,unused-ignore]
    pp = root / "pyproject.toml"
    if not pp.is_file():
        return False
    try:
        with pp.open("rb") as f:
            data = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return False
    node: object = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return True


def run_python(root: Path, d: Detection, cfg: PipelineConfig,
               results: list[StepResult]) -> None:
    venv = root / ".pipewarden-venv"
    py = sys.executable

    if not venv.exists():
        r = run_cmd([py, "-m", "venv", str(venv)],
                    cwd=root, name="py:venv",
                    timeout=cfg.timeouts.install_s, required=True)
        results.append(r)
        if r.is_failure():
            return

    vpy = str(venv / "Scripts" / "python.exe") if os.name == "nt" else str(venv / "bin" / "python")

    # Pick installer: uv > poetry > pip
    if d.has_uv_lock and shutil.which("uv"):
        cmd = ["uv", "sync", "--frozen"]
        step_name = "py:deps(uv)"
    elif d.has_poetry_lock and shutil.which("poetry"):
        cmd = ["poetry", "install", "--no-interaction"]
        step_name = "py:deps(poetry)"
    elif d.has_pyproject:
        cmd = [vpy, "-m", "pip", "install", "--quiet", "-e", "."]
        step_name = "py:deps(pyproject)"
    elif d.has_requirements:
        cmd = [vpy, "-m", "pip", "install", "--quiet", "-r", "requirements.txt"]
        step_name = "py:deps(requirements)"
    else:
        results.append(StepResult(name="py:deps", status=Status.SKIPPED,
                                  message="no manifest"))
        return

    r = run_cmd(cmd, cwd=root, name=step_name,
                timeout=cfg.timeouts.install_s, required=True)
    results.append(r)
    if r.is_failure():
        return

    if shutil.which("ruff"):
        results.append(run_cmd(["ruff", "check", "."], cwd=root,
                               name="py:lint(ruff)",
                               timeout=cfg.timeouts.default_s, required=True))
    else:
        results.append(StepResult(name="py:lint", status=Status.SKIPPED,
                                  message="ruff not installed"))

    # mypy only if configured — running unconfigured mypy is noisy.
    if shutil.which("mypy") and (
        (root / "mypy.ini").exists() or _pyproject_has_section(root, "tool.mypy")
    ):
        results.append(run_cmd(["mypy", "."], cwd=root,
                               name="py:typecheck(mypy)",
                               timeout=cfg.timeouts.default_s, required=True))

    has_tests = (root / "tests").is_dir() or (root / "test").is_dir() \
                or _pyproject_has_section(root, "tool.pytest.ini_options")
    if has_tests:
        # Probe whether pytest is importable in the venv first. If not, emit a
        # clear WARNED step rather than running pytest just to get an opaque
        # "No module named pytest" error.
        probe = run_cmd([vpy, "-c", "import pytest"], cwd=root,
                        name="py:test(probe)", timeout=15, required=False,
                        stream=False)
        if probe.status != Status.PASSED:
            results.append(StepResult(
                name="py:test(pytest)", status=Status.WARNED,
                message="pytest not installed in the project — add it as a dep or skip this stage",
            ))
            return
        pytest_cmd = [vpy, "-m", "pytest", "-q"]
        results.append(run_cmd(pytest_cmd, cwd=root,
                               name="py:test(pytest)",
                               timeout=cfg.timeouts.test_s, required=True))


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

def _read_npm_scripts(root: Path) -> dict[str, str]:
    try:
        with (root / "package.json").open("r", encoding="utf-8") as f:
            return dict(json.load(f).get("scripts") or {})
    except (OSError, json.JSONDecodeError):
        return {}


def run_node(root: Path, d: Detection, cfg: PipelineConfig,
             results: list[StepResult]) -> None:
    pm = d.node_pm
    if pm == "pnpm":
        install_cmd = ["pnpm", "install", "--frozen-lockfile"]
    elif pm == "yarn":
        install_cmd = ["yarn", "install", "--frozen-lockfile"]
    else:
        install_cmd = ["npm", "ci"] if d.has_package_lock else ["npm", "install"]

    r = run_cmd(install_cmd, cwd=root, name=f"node:deps({pm})",
                timeout=cfg.timeouts.install_s, required=True)
    results.append(r)
    if r.is_failure():
        return

    scripts = _read_npm_scripts(root)
    for script in ("lint", "typecheck", "test", "build"):
        if script not in scripts:
            results.append(StepResult(name=f"node:{script}", status=Status.SKIPPED,
                                      message=f"no '{script}' script"))
            continue
        cmd = ["npm", "test"] if (pm == "npm" and script == "test") else [pm, "run", script]
        timeout = cfg.timeouts.test_s if script == "test" else cfg.timeouts.build_s
        results.append(run_cmd(cmd, cwd=root, name=f"node:{script}",
                               timeout=timeout, required=True))


# ---------------------------------------------------------------------------
# .NET / Go / Rust
# ---------------------------------------------------------------------------

def run_dotnet(root: Path, _d: Detection, cfg: PipelineConfig,
               results: list[StepResult]) -> None:
    r = run_cmd(["dotnet", "restore"], cwd=root, name="dotnet:restore",
                timeout=cfg.timeouts.install_s, required=True)
    results.append(r)
    if r.is_failure():
        return
    r = run_cmd(["dotnet", "build", "--no-restore", "--nologo"], cwd=root,
                name="dotnet:build", timeout=cfg.timeouts.build_s, required=True)
    results.append(r)
    if r.is_failure():
        return
    results.append(run_cmd(["dotnet", "test", "--no-build", "--nologo"],
                           cwd=root, name="dotnet:test",
                           timeout=cfg.timeouts.test_s, required=True))


def run_go(root: Path, _d: Detection, cfg: PipelineConfig,
           results: list[StepResult]) -> None:
    results.append(run_cmd(["go", "mod", "download"], cwd=root, name="go:deps",
                           timeout=cfg.timeouts.install_s, required=True))
    if results[-1].is_failure():
        return
    results.append(run_cmd(["go", "vet", "./..."], cwd=root, name="go:vet",
                           timeout=cfg.timeouts.default_s, required=True))
    results.append(run_cmd(["go", "build", "./..."], cwd=root, name="go:build",
                           timeout=cfg.timeouts.build_s, required=True))
    results.append(run_cmd(["go", "test", "./..."], cwd=root, name="go:test",
                           timeout=cfg.timeouts.test_s, required=True))


def run_rust(root: Path, _d: Detection, cfg: PipelineConfig,
             results: list[StepResult]) -> None:
    results.append(run_cmd(["cargo", "fetch"], cwd=root, name="rust:deps",
                           timeout=cfg.timeouts.install_s, required=True))
    if results[-1].is_failure():
        return
    if shutil.which("cargo-clippy"):
        results.append(run_cmd(
            ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"],
            cwd=root, name="rust:lint(clippy)",
            timeout=cfg.timeouts.build_s, required=True))
    results.append(run_cmd(["cargo", "build", "--all-targets"], cwd=root,
                           name="rust:build", timeout=cfg.timeouts.build_s,
                           required=True))
    results.append(run_cmd(["cargo", "test", "--all-targets"], cwd=root,
                           name="rust:test", timeout=cfg.timeouts.test_s,
                           required=True))


# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------

def run_docker(root: Path, d: Detection, cfg: PipelineConfig,
               results: list[StepResult]) -> None:
    dockerfile = d.dockerfile_name
    if shutil.which("hadolint"):
        results.append(run_cmd(["hadolint", dockerfile], cwd=root,
                               name="docker:lint(hadolint)",
                               timeout=cfg.timeouts.default_s, required=True))
    results.append(run_cmd(
        ["docker", "build", "-t", cfg.docker_tag, "-f", dockerfile, "."],
        cwd=root, name="docker:build", timeout=cfg.timeouts.build_s, required=True))


# ---------------------------------------------------------------------------
# Vulnerability scanning (cross-language)
# ---------------------------------------------------------------------------

def run_vulns(root: Path, d: Detection, cfg: PipelineConfig,
              results: list[StepResult]) -> None:
    """Best-effort dep vuln scan using whatever tools are on PATH.

    Most teams will plug in their preferred scanner; this is a useful default.
    """
    any_ran = False
    if d.python and shutil.which("pip-audit"):
        results.append(run_cmd(["pip-audit", "--strict"], cwd=root,
                               name="vulns:pip-audit",
                               timeout=cfg.timeouts.scan_s, required=False))
        any_ran = True
    if d.node and shutil.which("npm"):
        results.append(run_cmd(
            ["npm", "audit", "--audit-level=high", "--omit=dev"],
            cwd=root, name="vulns:npm-audit",
            timeout=cfg.timeouts.scan_s, required=False))
        any_ran = True
    if d.rust and shutil.which("cargo-audit"):
        results.append(run_cmd(["cargo", "audit"], cwd=root, name="vulns:cargo-audit",
                               timeout=cfg.timeouts.scan_s, required=False))
        any_ran = True
    if d.go and shutil.which("govulncheck"):
        results.append(run_cmd(["govulncheck", "./..."], cwd=root,
                               name="vulns:govulncheck",
                               timeout=cfg.timeouts.scan_s, required=False))
        any_ran = True
    if not any_ran:
        results.append(StepResult(name="vulns", status=Status.SKIPPED,
                                  message="no vuln scanner available"))


# Stage registry — drives main loop. Order matters.
STAGES: dict[str, Callable[..., None]] = {
    "python": run_python,
    "node":   run_node,
    "dotnet": run_dotnet,
    "go":     run_go,
    "rust":   run_rust,
    "docker": run_docker,
    "vulns":  run_vulns,
}

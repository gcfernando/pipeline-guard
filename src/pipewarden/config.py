"""Configuration loading and validation.

Config sources, in precedence order (later wins):
  1. Built-in defaults
  2. .pipewarden.toml in the project root
  3. CLI flags
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef,import-not-found,unused-ignore]


# Stages must match the names used by the runner.
ALL_STAGES = ("secrets", "vulns", "python", "node", "dotnet", "go", "rust", "docker")


class ConfigError(ValueError):
    """Raised when the user-supplied config is invalid."""


@dataclass
class SecretsConfig:
    enabled: bool = True
    prefer_external: bool = True   # use gitleaks if installed
    allowlist_paths: list[str] = field(default_factory=list)
    allowlist_rules: list[str] = field(default_factory=list)
    allowlist_strings: list[str] = field(default_factory=list)
    max_file_bytes: int = 1_000_000
    max_files: int = 10_000


@dataclass
class StageToggles:
    python: bool = True
    node: bool = True
    dotnet: bool = True
    go: bool = True
    rust: bool = True
    docker: bool = True
    vulns: bool = True


@dataclass
class TimeoutsConfig:
    install_s: int = 900
    build_s: int = 900
    test_s: int = 1800
    scan_s: int = 600
    default_s: int = 600


@dataclass
class OutputConfig:
    json_path: str | None = None
    sarif_path: str | None = None
    junit_path: str | None = None
    log_path: str | None = None
    color: bool = True
    quiet: bool = False


@dataclass
class PipelineConfig:
    """Top-level config."""
    fail_fast: bool = False
    only: list[str] = field(default_factory=list)
    skip: list[str] = field(default_factory=list)
    docker_tag: str = "pipewarden-local:latest"
    stages: StageToggles = field(default_factory=StageToggles)
    secrets: SecretsConfig = field(default_factory=SecretsConfig)
    timeouts: TimeoutsConfig = field(default_factory=TimeoutsConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def validate(self) -> None:
        """Raise ConfigError on invalid combinations."""
        for s in self.only:
            if s not in ALL_STAGES:
                raise ConfigError(f"unknown stage in 'only': {s!r}")
        for s in self.skip:
            if s not in ALL_STAGES:
                raise ConfigError(f"unknown stage in 'skip': {s!r}")
        for tname in ("install_s", "build_s", "test_s", "scan_s", "default_s"):
            v = getattr(self.timeouts, tname)
            if not isinstance(v, int) or v <= 0:
                raise ConfigError(f"timeouts.{tname} must be a positive integer, got {v!r}")
        if self.secrets.max_file_bytes <= 0:
            raise ConfigError("secrets.max_file_bytes must be positive")
        if self.secrets.max_files <= 0:
            raise ConfigError("secrets.max_files must be positive")


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

CONFIG_FILENAMES = (".pipewarden.toml", "pipewarden.toml")


def find_config_file(root: Path) -> Path | None:
    for name in CONFIG_FILENAMES:
        p = root / name
        if p.is_file():
            return p
    return None


def _coerce_into(target: Any, data: dict[str, Any], path: str) -> None:
    """Copy known keys from `data` into the dataclass `target`. Reject unknowns."""
    known = {f.name for f in fields(target)}
    for key, value in data.items():
        if key not in known:
            raise ConfigError(f"unknown key: {path}.{key}")
        current = getattr(target, key)
        # Nested dataclass
        if hasattr(current, "__dataclass_fields__") and isinstance(value, dict):
            _coerce_into(current, value, f"{path}.{key}")
        else:
            # Type sanity (light — we don't ship a full schema validator)
            expected_type = type(current) if current is not None else None
            if expected_type is bool and not isinstance(value, bool):
                raise ConfigError(f"{path}.{key} must be a boolean")
            if expected_type is int and not isinstance(value, int):
                raise ConfigError(f"{path}.{key} must be an integer")
            if expected_type is str and not isinstance(value, str):
                raise ConfigError(f"{path}.{key} must be a string")
            if expected_type is list and not isinstance(value, list):
                raise ConfigError(f"{path}.{key} must be a list")
            setattr(target, key, value)


def load_config(path: Path | None) -> PipelineConfig:
    """Load config from a TOML file (or return defaults if path is None)."""
    cfg = PipelineConfig()
    if path is None:
        cfg.validate()
        return cfg
    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except OSError as e:
        raise ConfigError(f"cannot read config {path}: {e}") from e
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"invalid TOML in {path}: {e}") from e

    _coerce_into(cfg, data, "pipewarden")
    cfg.validate()
    return cfg

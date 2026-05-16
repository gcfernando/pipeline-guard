from pathlib import Path

import pytest

from pipeline_guard.config import (
    ConfigError,
    PipelineConfig,
    find_config_file,
    load_config,
)


def test_defaults_are_valid() -> None:
    cfg = load_config(None)
    assert isinstance(cfg, PipelineConfig)
    assert cfg.secrets.enabled
    assert cfg.timeouts.install_s > 0
    assert cfg.fail_fast is False


def test_find_config_file_missing(tmp_path: Path) -> None:
    assert find_config_file(tmp_path) is None


def test_find_config_file_present(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text("")
    assert find_config_file(tmp_path) == p


def test_load_simple_config(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text(
        'fail_fast = true\n'
        'docker_tag = "myapp:ci"\n'
        '[stages]\n'
        'docker = false\n'
        '[timeouts]\n'
        'install_s = 60\n'
        '[secrets]\n'
        'enabled = false\n'
        'allowlist_paths = ["tests/fixtures/*"]\n'
    )
    cfg = load_config(p)
    assert cfg.fail_fast
    assert cfg.docker_tag == "myapp:ci"
    assert cfg.stages.docker is False
    assert cfg.timeouts.install_s == 60
    assert cfg.secrets.enabled is False
    assert cfg.secrets.allowlist_paths == ["tests/fixtures/*"]


def test_unknown_key_rejected(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text('bogus_key = 1\n')
    with pytest.raises(ConfigError):
        load_config(p)


def test_unknown_stage_rejected(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text('skip = ["nope"]\n')
    with pytest.raises(ConfigError):
        load_config(p)


def test_bad_type_rejected(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text('[timeouts]\ninstall_s = "fast"\n')
    with pytest.raises(ConfigError):
        load_config(p)


def test_invalid_timeout_value(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text('[timeouts]\ninstall_s = 0\n')
    with pytest.raises(ConfigError):
        load_config(p)


def test_malformed_toml(tmp_path: Path) -> None:
    p = tmp_path / ".pipeline-guard.toml"
    p.write_text('this is not [valid')
    with pytest.raises(ConfigError):
        load_config(p)

import json
import subprocess
import sys
from pathlib import Path

import pytest

from pipewarden.cli import main


def test_help_runs(capsys: pytest.CaptureFixture[str]) -> None:
    # argparse raises SystemExit on --help; main() catches and returns it.
    rc = main(["--help"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "pipewarden" in out
    assert "--sarif-out" in out


def test_version_runs(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["--version"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "pipewarden" in out


def test_empty_dir_succeeds(tmp_path: Path) -> None:
    rc = main(["--root", str(tmp_path)])
    assert rc == 0


def test_bad_root_returns_usage_error(tmp_path: Path,
                                     capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["--root", str(tmp_path / "does-not-exist")])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not a directory" in err


def test_json_output_on_empty(tmp_path: Path,
                              capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["--root", str(tmp_path), "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["root"] == str(tmp_path.resolve())
    assert data["summary"]["total"] >= 1  # secrets scan ran


def test_secret_leak_fails(tmp_path: Path) -> None:
    (tmp_path / "leak.py").write_text("KEY='AKIAIOSFODNN7EXAMPLE'\n")
    rc = main(["--root", str(tmp_path), "--no-color"])
    assert rc == 1


def test_skip_disables_stage(tmp_path: Path) -> None:
    (tmp_path / "leak.py").write_text("KEY='AKIAIOSFODNN7EXAMPLE'\n")
    rc = main(["--root", str(tmp_path), "--skip", "secrets"])
    # Secrets skipped → no other stage detected → success
    assert rc == 0


def test_sarif_output_written(tmp_path: Path) -> None:
    (tmp_path / "leak.py").write_text("KEY='AKIAIOSFODNN7EXAMPLE'\n")
    sarif_path = tmp_path / "out.sarif"
    rc = main(["--root", str(tmp_path), "--sarif-out", str(sarif_path)])
    assert rc == 1
    data = json.loads(sarif_path.read_text())
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["results"]  # at least one finding


def test_junit_output_written(tmp_path: Path) -> None:
    junit_path = tmp_path / "junit.xml"
    rc = main(["--root", str(tmp_path), "--junit-out", str(junit_path)])
    assert rc == 0
    content = junit_path.read_text()
    assert "<testsuites" in content


def test_config_file_loaded(tmp_path: Path) -> None:
    (tmp_path / ".pipewarden.toml").write_text("[secrets]\nenabled = false\n")
    (tmp_path / "leak.py").write_text("KEY='AKIAIOSFODNN7EXAMPLE'\n")
    rc = main(["--root", str(tmp_path)])
    assert rc == 0  # secrets disabled in config → secret-leak ignored


def test_bad_config_returns_config_error(tmp_path: Path,
                                         capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / ".pipewarden.toml").write_text("bogus = 1\n")
    rc = main(["--root", str(tmp_path)])
    assert rc == 3
    err = capsys.readouterr().err
    assert "config error" in err


def test_invoked_as_module(tmp_path: Path) -> None:
    # Sanity check the `python -m pipewarden` entry point.
    result = subprocess.run(
        [sys.executable, "-m", "pipewarden", "--root", str(tmp_path), "--no-color"],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode == 0, result.stderr


def test_diff_mode_scopes_to_changed_files(tmp_path: Path) -> None:
    """--diff base limits the secret scan to git-changed files only."""
    import subprocess as sp
    # Init a git repo with a clean baseline commit, then add a leaky file unstaged.
    sp.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    sp.run(["git", "config", "user.email", "test@test"], cwd=tmp_path, check=True)
    sp.run(["git", "config", "user.name", "test"], cwd=tmp_path, check=True)
    (tmp_path / "clean.py").write_text("print('ok')\n")
    sp.run(["git", "add", "."], cwd=tmp_path, check=True)
    sp.run(["git", "commit", "-q", "-m", "init"], cwd=tmp_path, check=True)

    # Now add a leak as an UNTRACKED file (diff mode should still catch it).
    (tmp_path / "leak.py").write_text("KEY='AKIAIOSFODNN7EXAMPLE'\n")

    rc = main(["--root", str(tmp_path), "--diff", "HEAD", "--no-color"])
    assert rc == 1  # the leak in the untracked file should be found

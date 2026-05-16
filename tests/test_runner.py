import sys
from pathlib import Path

from pipeline_guard.runner import capture, run_cmd
from pipeline_guard.types import Status


def test_missing_binary_required(tmp_path: Path) -> None:
    r = run_cmd(["definitely-not-a-real-binary-xyz"], cwd=tmp_path,
                name="missing", timeout=5, required=True, stream=False)
    assert r.status == Status.FAILED
    assert "not found" in r.message


def test_missing_binary_optional(tmp_path: Path) -> None:
    r = run_cmd(["definitely-not-a-real-binary-xyz"], cwd=tmp_path,
                name="missing", timeout=5, required=False, stream=False)
    assert r.status == Status.WARNED


def test_successful_command(tmp_path: Path) -> None:
    r = run_cmd([sys.executable, "-c", "print('hi')"], cwd=tmp_path,
                name="echo", timeout=10, required=True, stream=False)
    assert r.status == Status.PASSED
    assert r.returncode == 0
    assert "hi" in r.stdout_tail


def test_nonzero_required_fails(tmp_path: Path) -> None:
    r = run_cmd([sys.executable, "-c", "import sys; sys.exit(7)"], cwd=tmp_path,
                name="exit7", timeout=10, required=True, stream=False)
    assert r.status == Status.FAILED
    assert r.returncode == 7


def test_nonzero_optional_warns(tmp_path: Path) -> None:
    r = run_cmd([sys.executable, "-c", "import sys; sys.exit(7)"], cwd=tmp_path,
                name="exit7", timeout=10, required=False, stream=False)
    assert r.status == Status.WARNED


def test_timeout_kills_process(tmp_path: Path) -> None:
    r = run_cmd(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        cwd=tmp_path, name="sleeper", timeout=1, required=True, stream=False,
    )
    assert r.status == Status.FAILED
    assert "timeout" in r.message


def test_capture_returns_stdout(tmp_path: Path) -> None:
    out = capture([sys.executable, "-c", "print('hello')"], cwd=tmp_path)
    assert out is not None and "hello" in out


def test_capture_none_on_failure(tmp_path: Path) -> None:
    out = capture([sys.executable, "-c", "import sys; sys.exit(1)"], cwd=tmp_path)
    assert out is None

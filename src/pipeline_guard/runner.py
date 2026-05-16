"""Subprocess execution. The ONLY place we spawn processes.

Centralising this lets us guarantee timeouts, output capture, and a uniform
StepResult for every command.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import time
from collections.abc import Sequence
from pathlib import Path

from .types import Status, StepResult

# We tail this many lines per step into the report.
TAIL_LINES = 60


def run_cmd(
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
    """Run `cmd`, stream output (optional), capture tail, return StepResult.

    `required=False` downgrades non-zero exits and missing binaries to WARNED.
    """
    start = time.monotonic()
    binary = shutil.which(cmd[0])
    if binary is None:
        return StepResult(
            name=name,
            status=Status.FAILED if required else Status.WARNED,
            message=f"command not found: {cmd[0]}",
        )

    full_env = {**os.environ, **(env or {})}

    try:
        proc = subprocess.Popen(
            list(cmd),
            cwd=str(cwd),
            env=full_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except OSError as e:
        return StepResult(
            name=name,
            status=Status.FAILED if required else Status.WARNED,
            message=f"failed to spawn: {e}",
        )

    tail: list[str] = []
    assert proc.stdout is not None
    deadline = time.monotonic() + timeout

    def _append_line(stripped: str) -> None:
        tail.append(stripped)
        if len(tail) > TAIL_LINES * 4:
            # Trim to avoid unbounded memory on chatty commands.
            del tail[: len(tail) - TAIL_LINES * 2]

    try:
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    proc.kill()
                    with contextlib.suppress(subprocess.TimeoutExpired):
                        proc.wait(timeout=5)
                    # Drain any final buffered output before returning.
                    with contextlib.suppress(Exception):
                        for line in proc.stdout:
                            stripped = line.rstrip("\n")
                            _append_line(stripped)
                            if stream:
                                print(f"{indent}{line}", end="")
                    return StepResult(
                        name=name,
                        status=Status.FAILED if required else Status.WARNED,
                        duration_s=time.monotonic() - start,
                        message=f"timeout after {timeout}s",
                        stdout_tail="\n".join(tail[-TAIL_LINES:]),
                    )

                # Wait briefly for the process to exit. This bounds how long
                # we can be stuck before re-checking the deadline.
                try:
                    proc.wait(timeout=min(0.1, remaining))
                except subprocess.TimeoutExpired:
                    pass  # still running

                # Drain whatever output is currently available. After the
                # process exits the pipe closes and readline() returns "".
                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    stripped = line.rstrip("\n")
                    _append_line(stripped)
                    if stream:
                        print(f"{indent}{line}", end="")

                if proc.poll() is not None:
                    break

            returncode = proc.wait()
        finally:
            # Always close the pipe to avoid resource leaks (ResourceWarning).
            with contextlib.suppress(Exception):
                proc.stdout.close()
    except KeyboardInterrupt:
        proc.kill()
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=5)
        raise

    duration = time.monotonic() - start
    tail_str = "\n".join(tail[-TAIL_LINES:])
    if returncode == 0:
        return StepResult(
            name=name,
            status=Status.PASSED,
            duration_s=duration,
            returncode=0,
            stdout_tail=tail_str,
        )
    return StepResult(
        name=name,
        status=Status.FAILED if required else Status.WARNED,
        duration_s=duration,
        returncode=returncode,
        message=f"exit {returncode}",
        stdout_tail=tail_str,
    )


def capture(cmd: Sequence[str], cwd: Path, timeout: int = 30) -> str | None:
    """Run a command and return stdout, or None on any failure.

    Used for cheap metadata queries (e.g. `git ls-files`, `npm config get`).
    """
    if shutil.which(cmd[0]) is None:
        return None
    try:
        out = subprocess.check_output(
            list(cmd),
            cwd=str(cwd),
            text=True,
            timeout=timeout,
            stderr=subprocess.DEVNULL,
        )
        return out
    except (subprocess.SubprocessError, OSError):
        return None

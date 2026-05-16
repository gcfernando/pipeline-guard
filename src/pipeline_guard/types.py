"""Core data types. Pure — no I/O, no subprocess, easy to test."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Status(str, Enum):
    """Outcome of a single step."""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WARNED = "warned"   # tool missing / non-required failure


class Severity(str, Enum):
    """Severity for findings (secrets, vulns, lint issues)."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass(frozen=True)
class Finding:
    """A single issue discovered by a scanner."""
    rule_id: str
    message: str
    severity: Severity
    file: str
    line: int = 0
    column: int = 0
    snippet: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "severity": self.severity.value,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "snippet": self.snippet,
        }


@dataclass
class StepResult:
    """Result of one stage or command."""
    name: str
    status: Status
    duration_s: float = 0.0
    returncode: int | None = None
    message: str = ""
    stdout_tail: str = ""
    findings: list[Finding] = field(default_factory=list)

    def is_failure(self) -> bool:
        return self.status == Status.FAILED

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "duration_s": round(self.duration_s, 3),
            "returncode": self.returncode,
            "message": self.message,
            "stdout_tail": self.stdout_tail,
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass
class Report:
    """Aggregated run results."""
    root: str
    tool_version: str
    detected: list[str] = field(default_factory=list)
    steps: list[StepResult] = field(default_factory=list)
    started_at: float = field(default_factory=time.time)
    duration_s: float = 0.0
    config_path: str | None = None

    def add(self, step: StepResult) -> None:
        self.steps.append(step)

    def failed(self) -> list[StepResult]:
        return [s for s in self.steps if s.is_failure()]

    def all_findings(self) -> list[Finding]:
        out: list[Finding] = []
        for s in self.steps:
            out.extend(s.findings)
        return out

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "tool_version": self.tool_version,
            "config_path": self.config_path,
            "detected": list(self.detected),
            "started_at": self.started_at,
            "duration_s": round(self.duration_s, 3),
            "steps": [s.to_dict() for s in self.steps],
            "summary": {
                "total": len(self.steps),
                "passed": sum(1 for s in self.steps if s.status == Status.PASSED),
                "failed": sum(1 for s in self.steps if s.status == Status.FAILED),
                "warned": sum(1 for s in self.steps if s.status == Status.WARNED),
                "skipped": sum(1 for s in self.steps if s.status == Status.SKIPPED),
                "findings": len(self.all_findings()),
            },
        }

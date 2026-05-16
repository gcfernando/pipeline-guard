"""Report serializers. Pure functions: take a Report, produce a string/dict."""
from __future__ import annotations

import json
from typing import Any
from xml.etree import ElementTree as ET

from .types import Report, Severity, Status

# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------

def to_json(report: Report) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=False)


# ---------------------------------------------------------------------------
# SARIF 2.1.0 — consumed by GitHub Code Scanning, Azure DevOps, etc.
# Spec: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html
# ---------------------------------------------------------------------------

_SARIF_LEVEL = {
    Severity.CRITICAL: "error",
    Severity.HIGH:     "error",
    Severity.MEDIUM:   "warning",
    Severity.LOW:      "note",
    Severity.INFO:     "note",
}


def to_sarif(report: Report) -> str:
    """Emit a SARIF document covering all findings across steps."""
    rules: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []

    for step in report.steps:
        for f in step.findings:
            rules.setdefault(f.rule_id, {
                "id": f.rule_id,
                "shortDescription": {"text": f.rule_id},
                "fullDescription": {"text": f.message},
                "defaultConfiguration": {"level": _SARIF_LEVEL.get(f.severity, "warning")},
            })
            results.append({
                "ruleId": f.rule_id,
                "level": _SARIF_LEVEL.get(f.severity, "warning"),
                "message": {"text": f.message},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": f.file},
                        "region": {
                            "startLine": max(f.line, 1),
                            "startColumn": max(f.column, 1),
                            "snippet": {"text": f.snippet} if f.snippet else {},
                        },
                    },
                }],
            })

    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "pipewarden",
                    "version": report.tool_version,
                    "informationUri": "https://github.com/gcfernando/pipewarden",
                    "rules": list(rules.values()),
                },
            },
            "results": results,
        }],
    }
    return json.dumps(sarif, indent=2)


# ---------------------------------------------------------------------------
# JUnit XML — every CI on earth knows how to render this.
# ---------------------------------------------------------------------------

def to_junit_xml(report: Report) -> str:
    """Map each step to a <testcase>; failures attach the stdout tail."""
    total = len(report.steps)
    failures = sum(1 for s in report.steps if s.status == Status.FAILED)
    skipped  = sum(1 for s in report.steps if s.status == Status.SKIPPED)
    suite_time = f"{report.duration_s:.3f}"

    testsuites = ET.Element("testsuites", {
        "name": "pipewarden",
        "tests": str(total),
        "failures": str(failures),
        "skipped": str(skipped),
        "time": suite_time,
    })
    testsuite = ET.SubElement(testsuites, "testsuite", {
        "name": "pipewarden",
        "tests": str(total),
        "failures": str(failures),
        "skipped": str(skipped),
        "time": suite_time,
    })

    for s in report.steps:
        case = ET.SubElement(testsuite, "testcase", {
            "classname": "pipewarden",
            "name": s.name,
            "time": f"{s.duration_s:.3f}",
        })
        if s.status == Status.FAILED:
            fail = ET.SubElement(case, "failure", {
                "message": s.message or "step failed",
                "type": "PipelineGuardFailure",
            })
            fail.text = s.stdout_tail or s.message
        elif s.status == Status.SKIPPED:
            ET.SubElement(case, "skipped", {"message": s.message or "skipped"})
        elif s.status == Status.WARNED:
            # JUnit has no "warned" — represent as system-out.
            sysout = ET.SubElement(case, "system-out")
            sysout.text = f"WARNED: {s.message}\n{s.stdout_tail}"

    # ET.tostring returns bytes by default; we want a string.
    return ET.tostring(testsuites, encoding="unicode")

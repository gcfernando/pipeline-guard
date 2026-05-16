import json
from xml.etree import ElementTree as ET

from pipewarden.reporters import to_json, to_junit_xml, to_sarif
from pipewarden.types import Finding, Report, Severity, Status, StepResult


def _sample_report() -> Report:
    r = Report(root="/repo", tool_version="9.9.9")
    r.add(StepResult(name="py:lint", status=Status.PASSED, duration_s=1.2))
    r.add(StepResult(name="py:test", status=Status.FAILED, duration_s=3.4,
                     returncode=1, message="exit 1", stdout_tail="boom"))
    r.add(StepResult(name="docker:build", status=Status.SKIPPED,
                     message="no docker"))
    r.add(StepResult(name="secrets:fallback", status=Status.FAILED,
                     duration_s=0.1, message="1 finding",
                     findings=[Finding(
                         rule_id="aws.access_key", message="possible aws.access_key",
                         severity=Severity.CRITICAL,
                         file="src/x.py", line=10, column=5, snippet="AKIA…MPLE",
                     )]))
    r.duration_s = 4.7
    return r


def test_json_round_trip() -> None:
    rep = _sample_report()
    data = json.loads(to_json(rep))
    assert data["tool_version"] == "9.9.9"
    assert data["summary"]["total"] == 4
    assert data["summary"]["failed"] == 2
    assert data["summary"]["findings"] == 1
    names = [s["name"] for s in data["steps"]]
    assert "py:test" in names


def test_sarif_well_formed() -> None:
    rep = _sample_report()
    data = json.loads(to_sarif(rep))
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["tool"]["driver"]["name"] == "pipewarden"
    results = data["runs"][0]["results"]
    assert len(results) == 1
    assert results[0]["ruleId"] == "aws.access_key"
    assert results[0]["level"] == "error"
    loc = results[0]["locations"][0]["physicalLocation"]
    assert loc["artifactLocation"]["uri"] == "src/x.py"
    assert loc["region"]["startLine"] == 10


def test_junit_parses_as_xml() -> None:
    rep = _sample_report()
    xml = to_junit_xml(rep)
    root = ET.fromstring(xml)
    assert root.tag == "testsuites"
    suite = root.find("testsuite")
    assert suite is not None
    assert suite.attrib["tests"] == "4"
    assert suite.attrib["failures"] == "2"
    failure_cases = [c for c in suite.findall("testcase") if c.find("failure") is not None]
    assert len(failure_cases) == 2
    skipped_cases = [c for c in suite.findall("testcase") if c.find("skipped") is not None]
    assert len(skipped_cases) == 1


def test_sarif_empty_report() -> None:
    rep = Report(root="/r", tool_version="1.0")
    data = json.loads(to_sarif(rep))
    assert data["runs"][0]["results"] == []

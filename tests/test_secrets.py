from pathlib import Path

from pipewarden.config import SecretsConfig
from pipewarden.secrets import SECRET_PATTERNS, scan_secrets_fallback
from pipewarden.types import Status


def test_clean_repo(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("def hello(): return 'world'\n")
    r = scan_secrets_fallback(tmp_path, SecretsConfig())
    assert r.status == Status.PASSED
    assert r.findings == []


def test_aws_key_detected(tmp_path: Path) -> None:
    (tmp_path / "leak.py").write_text('KEY = "AKIAIOSFODNN7EXAMPLE"\n')
    r = scan_secrets_fallback(tmp_path, SecretsConfig())
    assert r.status == Status.FAILED
    assert any(f.rule_id == "aws.access_key" for f in r.findings)
    # snippet should be redacted (short) — never the full secret
    assert all(len(f.snippet) <= 20 for f in r.findings)


def test_github_pat_detected(tmp_path: Path) -> None:
    (tmp_path / "creds").write_text("token=ghp_" + "a" * 36 + "\n")
    r = scan_secrets_fallback(tmp_path, SecretsConfig())
    assert r.status == Status.FAILED
    assert any(f.rule_id == "github.pat_classic" for f in r.findings)


def test_private_key_detected(tmp_path: Path) -> None:
    (tmp_path / "id_rsa").write_text(
        "-----BEGIN RSA PRIVATE KEY-----\nMIIBOgIBAAJB\n-----END RSA PRIVATE KEY-----\n"
    )
    r = scan_secrets_fallback(tmp_path, SecretsConfig())
    assert r.status == Status.FAILED


def test_path_allowlist(tmp_path: Path) -> None:
    fixtures = tmp_path / "tests" / "fixtures"
    fixtures.mkdir(parents=True)
    (fixtures / "fake.txt").write_text("AKIAIOSFODNN7EXAMPLE")
    cfg = SecretsConfig(allowlist_paths=["tests/fixtures/*"])
    r = scan_secrets_fallback(tmp_path, cfg)
    assert r.status == Status.PASSED


def test_rule_allowlist(tmp_path: Path) -> None:
    (tmp_path / "leak.txt").write_text("AKIAIOSFODNN7EXAMPLE")
    cfg = SecretsConfig(allowlist_rules=["aws.access_key"])
    r = scan_secrets_fallback(tmp_path, cfg)
    assert r.status == Status.PASSED


def test_binary_files_skipped(tmp_path: Path) -> None:
    # An image with what looks like a secret in its bytes — shouldn't be read.
    (tmp_path / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\nAKIAIOSFODNN7EXAMPLE")
    r = scan_secrets_fallback(tmp_path, SecretsConfig())
    assert r.status == Status.PASSED


def test_large_files_skipped(tmp_path: Path) -> None:
    big = tmp_path / "big.txt"
    big.write_text("AKIAIOSFODNN7EXAMPLE" + "x" * 2_000_000)
    cfg = SecretsConfig(max_file_bytes=1000)
    r = scan_secrets_fallback(tmp_path, cfg)
    assert r.status == Status.PASSED


def test_findings_include_location(tmp_path: Path) -> None:
    (tmp_path / "leak.py").write_text("# line 1\n# line 2\nKEY='AKIAIOSFODNN7EXAMPLE'\n")
    r = scan_secrets_fallback(tmp_path, SecretsConfig())
    assert any(f.line == 3 for f in r.findings)


def test_all_patterns_compile() -> None:
    # Sanity: regression guard for badly-formed patterns.
    for rule_id, _sev, pattern in SECRET_PATTERNS:
        assert pattern.pattern, rule_id


def test_string_allowlist(tmp_path: Path) -> None:
    (tmp_path / "doc.md").write_text("Example: AKIAIOSFODNN7EXAMPLE\n")
    cfg = SecretsConfig(allowlist_strings=["AKIAIOSFODNN7EXAMPLE"])
    r = scan_secrets_fallback(tmp_path, cfg)
    assert r.status == Status.PASSED

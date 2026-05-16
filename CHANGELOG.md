# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-05-16

### Added
- Project detection for Python (pip/poetry/uv), Node (npm/pnpm/yarn), .NET, Go, Rust, Docker
- Secret scanning with `gitleaks` if installed, regex fallback otherwise
- Allowlists by path, rule, and string for the fallback scanner
- Dependency vulnerability scanning via `pip-audit`, `npm audit`, `cargo-audit`, `govulncheck`
- SARIF 2.1 and JUnit XML report writers
- TOML config file (`.pipeline-guard.toml`) with strict schema validation
- Stable CLI exit codes (0/1/2/3/130)
- `--version`, `--json`, `--only`, `--skip`, `--fail-fast`, `--log-file`, `--no-color`
- Subprocess timeouts on every command
- `python -m pipeline_guard` entry point
- 50+ tests; CI matrix across Linux/macOS/Windows and Python 3.10–3.13
- Signed releases via Sigstore (PyPI Trusted Publisher)

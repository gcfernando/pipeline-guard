# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

## Reporting a Vulnerability

**Please do not report security vulnerabilities via public GitHub issues.**

Email **f.gehan@gmail.com** with:

- A description of the vulnerability
- Steps to reproduce
- Potential impact

You will receive a response within **48 hours**. If the issue is confirmed, a patch will be released as soon as possible and you will be credited in the changelog.

## Scope

### In scope

- **False negatives in the built-in secret scanner** — a real credential format that the scanner fails to detect
- **False positives that expose user data** — scanner behaviour that could cause sensitive content to be logged or exfiltrated
- **Command injection via user-controlled input** — any path from config file / CLI flags to shell execution
- **Arbitrary file read / write** — via path traversal in `--root`, `--config`, or report output flags
- **Dependency vulnerabilities** — known CVEs in the tool's own dependency tree (currently zero runtime deps on Python 3.11+)

### Out of scope

- **Scanner coverage gaps** — a token format not yet in `SECRET_PATTERNS` is a feature request, not a security issue; open a public issue instead
- **False positives that only affect output** — a scanner match that is wrong but harmless
- **Issues requiring root / admin access on the user's own machine**
- **Social engineering**

## Disclosure Timeline

| Day | Action |
|-----|--------|
| 0   | Report received; acknowledgement sent within 48 hours |
| 7   | Severity triaged and communicated to reporter |
| 30  | Patch released (or extended timeline agreed with reporter for complex issues) |
| 30  | Public disclosure after patch is available |

For critical vulnerabilities (RCE, credential exfiltration), patches target a 7-day turnaround.

## Security Design Notes

Pipewarden is designed with a minimal attack surface:

- **Zero network calls at runtime.** The tool shells out only to local commands (`pip`, `npm`, `cargo`, `dotnet`, `go`, `trivy`, `grype`, `gitleaks`, etc.). No data is sent to any remote server by the tool itself. Note: the tools it invokes (e.g. `pip-audit`, `govulncheck`, `dotnet list --vulnerable`) may make their own network calls to fetch advisory databases.
- **No telemetry.** Nothing is tracked or transmitted by Pipewarden.
- **No shell=True.** All subprocesses are launched with explicit argument lists, never via a shell string. This prevents command injection from config values.
- **Strict TOML validation.** Unknown keys in `.pipewarden.toml` are rejected immediately (exit 3), preventing silently malformed configs.
- **Signed releases.** Every release is signed with Sigstore (PyPI Trusted Publisher workflow). Verify with `pip install sigstore && python -m sigstore verify pipewarden-*.tar.gz`.
- **Minimal Docker attack surface.** The official container image (`ghcr.io/gcfernando/pipewarden`) uses Alpine Linux rather than Debian-based images. Alpine carries a significantly smaller attack surface and zero known high-severity CVEs in the base layer.
- **Non-root container execution.** The container runs as UID 1000 (`guard` user), not root. If the container is ever compromised, the attacker has no root access to the host system.

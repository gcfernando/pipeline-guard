# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [1.3.2] — 2026-05-17

### Fixed

- **README factual errors corrected** — eight inaccuracies found by source-code audit: Rust commands now include `--all-targets`; step name corrected to `rust:lint(clippy)`; vulns stage shows exact flags (`pip-audit --strict`, `npm audit --audit-level=high --omit=dev`); gitleaks `--diff` fallback documented; Docker daemon absent behaviour distinguished (WARNED in CI, FAILED locally); Docker scan step absence when no scanner is on PATH clarified; `pipewarden.toml` (no dot) accepted as alternative config filename; mypy command corrected to `mypy .`.

- **README self-scan false positive fixed** — a C# connection-string example in the "dangerous pattern" section matched the `mssql.connection_string` regex, causing Pipewarden's own CI to exit 4. The password placeholder was changed to use angle-bracket syntax (`<YOUR-PASSWORD>`); the `<` character is excluded from the pattern's character class so the example no longer triggers the scanner.

---

## [1.3.1] — 2026-05-17

### Fixed

- **Docstrings added to all source and test files** — every public function in `cli.py`, `stages.py`, `secrets.py`, `config.py`, `runner.py`, `reporters.py`, `detect.py`, and all seven test modules now carries a one-line docstring describing what it does or verifies. This improves IDE hover-help and `help()` output without any behavioural change.

- **Pytest fixture shadow warning eliminated** — `test_stages.py` fixtures `cfg` and `recorder` are now registered via `@pytest.fixture(name=...)` with underscore-prefixed function names (`_cfg`, `_recorder`). This is the canonical pytest pattern for avoiding the "Redefining name from outer scope" IDE warning without suppression comments.

- **README `tool_version` example corrected** — the JSON output example showed `"tool_version": "1.0.0"`; updated to reflect the current version.

- **README Docker section updated** — added a callout noting that the official image uses `python:3.12-alpine`, eliminating 2 high CVEs present in the Debian slim base.

- **README table alignment corrected** — separator rows in the "Who Should Use It?", "What ruff catches", and "Available Hooks" tables now match their header column widths.

---

## [1.3.0] — 2026-05-17

### Added

- **`dotnet format` step** — `dotnet format --verify-no-changes` now runs between `dotnet restore` and `dotnet build` for all .NET projects, enforcing code style compliance. The step fails if any file needs reformatting. Controlled by `[dotnet] format = true` (default: on). Disable for legacy codebases via `format = false`.

- **`.NET NuGet vulnerability scanning** — `dotnet list package --vulnerable --include-transitive` runs after `dotnet test` and checks all direct and transitive NuGet packages against the GitHub Advisory Database. Controlled by `[dotnet] vulns = true` (default: on).

- **`.NET outdated package reporting** — `dotnet list package --outdated` is available as an opt-in non-blocking step. Reports available NuGet upgrades; always `WARNED`, never fails the pipeline. Controlled by `[dotnet] outdated = false` (default: off).

- **`[dotnet]` config section** — New TOML section providing fine-grained control over the .NET pipeline steps:
  ```toml
  [dotnet]
  format   = true    # dotnet format --verify-no-changes
  vulns    = true    # dotnet list package --vulnerable --include-transitive
  outdated = false   # dotnet list package --outdated (non-blocking, opt-in)
  ```

- **Container image scanning** — After a successful `docker build`, Pipewarden automatically scans the built image with `trivy` (preferred) or `grype` (fallback) if either is on the PATH. High and Critical CVEs fail the pipeline. Neither tool installed → `WARNED` (non-blocking). Step name: `docker:scan(trivy)` or `docker:scan(grype)`.

- **Cross-language `outdated` stage** — New top-level `outdated` stage runs best-effort outdated-package checks across all detected languages in one pass:
  - Python — `pip list --outdated` inside `.pipewarden-venv` (skipped if no venv)
  - Node — `npm outdated`
  - Go — `go list -m -u all`
  - Rust — `cargo outdated` (requires `cargo-outdated` on PATH; skipped if absent)
  - All findings are `WARNED` — the stage never fails the pipeline.

  Enable with `outdated = true` in `[stages]`.

- **Git history secret scanning** — New `scan_history = true` option in `[secrets]` causes the secrets stage to run `gitleaks detect` over the full git history rather than the working tree. Useful for auditing repositories before open-sourcing. Requires gitleaks; the built-in fallback does not support history mode.

### Changed

- Docker base image switched from `python:3.12-slim` to `python:3.12-alpine` — eliminates 2 high CVEs present in the Debian-based slim image, reduces attack surface.

- CI matrix now uses `"3.x"` as a forward-compatible Python sentinel (`actions/setup-python` resolves this to the current latest stable release at run time). Future Python versions (3.15, 3.16, …) are automatically tested with zero config changes. Pinned versions (3.10–3.13) remain in the matrix to preserve backward-compatibility testing.

- Coverage upload condition in `quality-gate.yml` changed from `matrix.python == '3.12'` to `matrix.python == '3.x'` — always uploads on the newest Python without needing future config updates.

- Test suite expanded to **160 tests**; branch coverage ≥ 85%.

## [1.2.0] — 2026-05-17

### Added

- **24 new secret patterns** — 46 total (up from 22 in 1.1.0), organised into 9 categories:
  - **Database URIs** — `postgres.connection_string`, `mysql.connection_string`, `redis.connection_string`, `amqp.connection_string`
  - **SQL / JDBC** — `mssql.connection_string` (SQL Server ADO.NET key=value format with negative lookahead to skip Windows Integrated Security), `jdbc.connection_string` (JDBC URL `password=` parameter)
  - **Azure** — `azure.storage_connection_string` (`DefaultEndpointsProtocol=…;AccountKey=…`), `azure.cosmos_connection_string` (`AccountEndpoint=…;AccountKey=…`), `azure.servicebus_connection_string` (`Endpoint=sb://…;SharedAccessKey=…`)
  - **AWS** — `aws.sts_key` (STS/AssumeRole temporary credentials, `ASIA` prefix)
  - **Developer platforms** — `digitalocean.token` (`dop_v1_`), `github.actions_token` (`ghs_`), `github.user_token` (`ghu_`), `linear.api_key` (`lin_api_`), `okta.token` (`SSWS `)
  - **AI / ML** — `huggingface.token` (`hf_`), `replicate.token` (`r8_`)
  - **Communication** — `telegram.bot_token` (`numeric_id:AA…`)
  - **Payment** — `stripe.test_key` (`sk_test_`), `stripe.webhook_secret` (`whsec_`)
  - **E-commerce** — `shopify.access_token` (`shpat_`), `shopify.storefront_token` (`shpss_`), `shopify.custom_app_token` (`shpca_`)
  - **Observability** — `newrelic.license_key` (`NRAK-`)

### Fixed

- **Self-scan false positive** — `.pipewarden.toml` is now always excluded from secret scanning via `allowlist_paths`; the config file's own `allowlist_strings` entries can match secret patterns, causing a loop
- **README documentation examples** — connection string examples in docs are now written in split form (e.g. `` `mongodb://HOST/DB` ``) so the scanner's `[^:@\s]` stop-at-whitespace rule cannot match across a documentation line

### Changed

- Test suite expanded from 73 to **160 tests** (+87); coverage ≥ 85 %

## [1.1.0] — 2026-05-17

### Added

- **22 secret patterns** (up from 12): GitLab PAT (`glpat-`), Twilio Account SID, SendGrid API key, Anthropic API key, OpenAI classic and project-format keys, Databricks personal token (`dapi`), HashiCorp Vault service token (`hvs.`), MongoDB connection string, PyPI API token
- **`**` glob support** in `allowlist_paths` — patterns like `tests/fixtures/**` now work correctly; previously `fnmatch` silently ignored `**`
- **`[retry]` config section** (`attempts`, `backoff_base`) — retries network-heavy steps (pip install, npm ci, cargo fetch, go mod download, etc.) on transient failures with exponential backoff
- **`PIPEWARDEN_*` environment variable overrides** — all major settings can be set via env vars (FAIL_FAST, SKIP, ONLY, TIMEOUT_*, NO_COLOR, QUIET, RETRY_ATTEMPTS, RETRY_BACKOFF); priority: CLI > env vars > TOML > defaults
- **`EXIT_SECRETS = 4`** — secrets scan failure now returns exit code 4 instead of 1, allowing CI scripts to distinguish "credential leak" from "test failure"
- **`--dry-run` flag** — prints which stages would run without executing anything
- **`--init` flag** — scaffolds a `.pipewarden.toml` with commented-out defaults
- **`--validate` flag** — validates the config file and exits (0 = valid, 3 = error)
- **`--list-stages` flag** — shows which stages are detected and enabled for the current project
- **`--markdown-out PATH` flag** — writes a Markdown summary table; pipe to `$GITHUB_STEP_SUMMARY` for GitHub Actions step panels
- **`--gh-annotations` flag** — prints GitHub Actions `::error file=...` annotations to stdout for inline PR diff comments
- **SARIF fingerprints** — each finding now includes a SHA-256 fingerprint (`primaryLocationLineHash/v1`) for GitHub Code Scanning deduplication; the same secret detected across multiple runs is no longer reported as a new alert each time
- **`to_github_annotations()`** in `reporters.py` — new report serializer
- **`to_markdown_summary()`** in `reporters.py` — new report serializer (truncates at 100 findings with a note to use `--sarif-out` for the full list)
- **Docker daemon availability check** — `run_docker()` now runs `docker info` before attempting `docker build`; emits `WARNED` (not `FAILED`) when the daemon is absent in a detected CI environment (CI / GITHUB_ACTIONS / GITLAB_CI / TF_BUILD)

### Fixed

- JUnit failure type was `PipelineGuardFailure` — corrected to `PipewarnedFailure`

## [1.0.0] — 2026-05-16

### Added
- Project detection for Python (pip/poetry/uv), Node (npm/pnpm/yarn), .NET, Go, Rust, Docker
- Secret scanning with `gitleaks` if installed, regex fallback otherwise
- Allowlists by path, rule, and string for the fallback scanner
- Dependency vulnerability scanning via `pip-audit`, `npm audit`, `cargo-audit`, `govulncheck`
- SARIF 2.1 and JUnit XML report writers
- TOML config file (`.pipewarden.toml`) with strict schema validation
- Stable CLI exit codes (0/1/2/3/130)
- `--version`, `--json`, `--only`, `--skip`, `--fail-fast`, `--log-file`, `--no-color`
- Subprocess timeouts on every command
- `python -m pipewarden` entry point
- 50+ tests; CI matrix across Linux/macOS/Windows and Python 3.10+ (auto-forward-compatible via `"3.x"`)
- Signed releases via Sigstore (PyPI Trusted Publisher)

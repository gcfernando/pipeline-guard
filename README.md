<div align="center">

<br>

<img src="https://img.shields.io/badge/🛡️-Pipewarden-0969DA?style=for-the-badge" alt="Pipewarden" height="48"/>

<br><br>

**One command. Every language. Every CI.**
**Install · Lint · Test · Build · Scan — automatically.**

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-D22128?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-160%20Passing-2EA44F?style=for-the-badge&logo=checkmarx&logoColor=white)](#)
[![Coverage](https://img.shields.io/badge/Coverage-80%25%2B-2EA44F?style=for-the-badge)](#)
[![Mypy](https://img.shields.io/badge/Mypy-Strict-1F5082?style=for-the-badge&logo=python&logoColor=white)](#)
[![Platforms](https://img.shields.io/badge/Platforms-Linux%20|%20macOS%20|%20Windows-555555?style=for-the-badge)](#)

<br>

</div>

---

## Table of Contents

| # | Section |
|---|---------|
| 1 | [What Is Pipewarden?](#-what-is-pipewarden) |
| 2 | [The Problem It Solves](#-the-problem-it-solves) |
| 3 | [Who Should Use It?](#-who-should-use-it) |
| 4 | [Installation](#-installation) |
| 5 | [Tutorial: Your First Run (5 Minutes)](#-tutorial-your-first-run-5-minutes) |
| 6 | [How It Works — The Pipeline Stages](#️-how-it-works--the-pipeline-stages) |
| 7 | [Python Projects — Complete Tutorial](#-python-projects--complete-tutorial) |
| 8 | [.NET Projects — Complete Tutorial](#-net-projects--complete-tutorial) |
| 9 | [Node.js / Go / Rust — Quick Guides](#-nodejs--go--rust--quick-guides) |
| 10 | [Polyglot Repos (Multiple Languages)](#-polyglot-repos-multiple-languages) |
| 11 | [Secret Scanning — Deep Dive](#-secret-scanning--deep-dive) |
| 12 | [What To Do When Secrets Are Found](#-what-to-do-when-secrets-are-found) |
| 13 | [Reading the Console Output](#-reading-the-console-output) |
| 14 | [Output Files — SARIF, JUnit XML, JSON, Markdown](#-output-files--sarif-junit-xml-json-markdown) |
| 15 | [How to Read Each Output File](#-how-to-read-each-output-file) |
| 16 | [How to Act on Findings](#-how-to-act-on-findings) |
| 17 | [Configuration Reference](#-configuration-reference) |
| 18 | [Environment Variable Overrides](#-environment-variable-overrides) |
| 19 | [Using Pipewarden Locally](#-using-pipewarden-locally) |
| 20 | [CI / CD Integration](#-ci--cd-integration) |
| 21 | [GitHub Actions (Official Action)](#-github-actions-official-action) |
| 22 | [Pre-Commit Hooks](#-pre-commit-hooks) |
| 23 | [CLI Reference](#-cli-reference) |
| 24 | [Frequently Asked Questions](#-frequently-asked-questions) |
| 25 | [Contributing](#-contributing) |

---

## What Is Pipewarden?

**Pipewarden** is a free, open-source command-line tool that acts as a **universal quality gate** for any software project.

You run **one command** and it automatically:

1. **Figures out what kind of project you have** — Python? Node? .NET? Go? Rust? Docker? All of them?
2. **Installs your dependencies** using the right package manager for your project
3. **Scans for leaked secrets** — API keys, passwords, connection strings, tokens — before they ever leave your machine
4. **Lints your code** to catch style and logic errors
5. **Runs your tests**
6. **Builds your application**
7. **Scans for known CVEs** in your dependencies (optional)
8. **Produces machine-readable reports** (SARIF, JUnit XML, JSON, Markdown) for your CI dashboard

Everything in the correct order. With timeouts. With human-readable output. With machine-readable reports. **Zero configuration required.**

> Drop Pipewarden into any repository and run `pipewarden` — it just works.

---

## The Problem It Solves

Every team writes the same CI pipeline over and over again. For a Python project it might look like this:

```yaml
- name: Install deps
  run: pip install -r requirements.txt

- name: Lint
  run: flake8 .

- name: Test
  run: pytest

- name: Check secrets
  run: # ... which tool do we use again?
```

Multiply this across dozens of repositories in multiple languages and you get:

| Problem | Impact |
|---------|--------|
| Every project has a different CI setup | New engineers waste hours understanding each one |
| Secret scanning is skipped or inconsistent | AWS keys, GitHub tokens get committed and leaked |
| Pipelines break silently | A missing tool is not caught until production |
| Polyglot repos need multiple pipelines | Maintenance cost multiplies with each language |
| No standard security reports | Findings live in logs, not trackable dashboards |

**With Pipewarden:**

```bash
pip install pipewarden
pipewarden
```

Same command. Every project. Every language. Every CI system.

---

## Who Should Use It?

| Role | How Pipewarden Helps |
|------|----------------------|
| **Individual Developer** | Run the same quality checks locally that CI runs remotely. Catch issues before pushing. |
| **Team Lead / Tech Lead** | Enforce a consistent quality baseline across all repositories with zero per-project setup. |
| **DevOps / Platform Engineer** | Replace bespoke CI scripts with one standard tool. Reduce pipeline maintenance. |
| **Security Engineer** | Automatically scan every commit for leaked secrets. Get SARIF reports in the GitHub Security tab. |
| **CTO / Engineering Manager** | Reduce security incidents. Speed up onboarding. Standardise engineering practices at scale. |
| **Open Source Maintainer** | Add comprehensive CI to any contributor's PR in seconds. |

---

## Installation

### Option 1 — Install from PyPI (recommended)

```bash
pip install pipewarden
```

Verify the installation:

```bash
pipewarden --version
# → pipewarden 1.3.1
```

### Option 2 — Install from Source

```bash
pip install git+https://github.com/gcfernando/pipewarden.git@v1.3.1
```

### Option 3 — Docker (no local Python required)

```bash
docker run --rm -v "$(pwd):/work" \
  ghcr.io/gcfernando/pipewarden:latest \
  --root /work
```

> The official image is based on `python:3.12-alpine` — a minimal, security-hardened base.

### Troubleshooting Installation

| Error | Fix |
|-------|-----|
| `Permission denied` | `pip install --user pipewarden` |
| `externally-managed-environment` | `pip install --break-system-packages pipewarden` |
| `command not found` after install | Add `~/.local/bin` to your `PATH` |

> **Zero runtime dependencies.** On Python 3.11+ Pipewarden has no third-party dependencies. On Python 3.10 it needs only `tomli` for TOML parsing — nothing else is installed into your project.

---

## Tutorial: Your First Run (5 Minutes)

This section walks you through Pipewarden from zero — from installation to understanding the output, step by step.

### Step 1 — Install

```bash
pip install pipewarden
```

### Step 2 — Navigate to your project

```bash
cd /path/to/your-project
```

If you do not have a project handy, create a minimal Python one for testing:

```bash
mkdir my-test-project && cd my-test-project
echo 'requests==2.31.0' > requirements.txt
mkdir tests
echo 'def test_pass(): assert 1 + 1 == 2' > tests/test_basic.py
pip install pytest   # for this demo only
```

### Step 3 — Run Pipewarden

```bash
pipewarden
```

You will see output like this:

```
════════════════════════════════════════════════════════════════
  Pipewarden 1.3.1
════════════════════════════════════════════════════════════════
  root:     /path/to/your-project
  config:   (defaults — no config file found)
  detected: python

════════════════════════════════════════════════════════════════
  Secrets
════════════════════════════════════════════════════════════════
✓ secrets:fallback (0.1s)

════════════════════════════════════════════════════════════════
  Python
════════════════════════════════════════════════════════════════
✓ py:venv (2.9s)
✓ py:deps(requirements) (4.1s)
✓ py:lint(ruff) (0.3s)
✓ py:test(pytest) (2.1s)

════════════════════════════════════════════════════════════════
  Summary
════════════════════════════════════════════════════════════════
  ✓ secrets:fallback      passed    0.1s   scanned 5 files, no secrets
  ✓ py:venv               passed    2.9s
  ✓ py:deps(requirements) passed    4.1s
  ✓ py:lint(ruff)         passed    0.3s
  ✓ py:test(pytest)       passed    2.1s

  ✓ all 5 steps passed in 9.5s
```

**Exit code `0`.** Everything passed. This is exactly what your CI will see.

### Step 4 — Understand what just happened

Pipewarden ran 5 steps automatically, in order:

| Step | What it did |
|------|-------------|
| `secrets:fallback` | Scanned all your files for leaked API keys, passwords, tokens |
| `py:venv` | Created `.pipewarden-venv/` — an isolated Python environment |
| `py:deps(requirements)` | Ran `pip install -r requirements.txt` inside that environment |
| `py:lint(ruff)` | Ran `ruff check .` — Python linter with 800+ rules |
| `py:test(pytest)` | Ran `python -m pytest -q` — your test suite |

Nothing was configured. Pipewarden detected `requirements.txt` and figured out the rest.

### Step 5 — Generate a report

```bash
pipewarden --json
```

This outputs a machine-readable JSON report (shown in full detail in the [Output Files](#-output-files--sarif-junit-xml-json-markdown) section).

```bash
pipewarden --sarif-out results.sarif --junit-out results.xml
```

This generates two report files: a SARIF file for security dashboards and a JUnit XML file for test result dashboards. Both are explained in detail below.

### Step 6 — Add a config file (optional)

If you want to customise behaviour, generate a starter config:

```bash
pipewarden --init
```

This creates `.pipewarden.toml` in your project root with all options and their defaults, ready to edit.

### Step 7 — Use it in CI

Add one step to your CI pipeline. For GitHub Actions:

```yaml
- run: pip install pipewarden
- run: pipewarden --sarif-out report.sarif --junit-out junit.xml
```

Done. The same command you ran locally now runs in CI.

---

## How It Works — The Pipeline Stages

Pipewarden always runs stages in this order. Each stage only runs if the relevant files are detected.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Pipewarden Pipeline                          │
├──────────┬──────────────────────────────────────────────────────┤
│ Stage 1  │  DETECT                                              │
│          │  Reads your project root. Identifies languages.      │
│          │  No files run. Pure detection only.                  │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 2  │  SECRETS  (always first — blocks everything else)    │
│          │  Scans every file for leaked credentials.            │
│          │  If anything is found → exit 4 immediately.          │
│          │  Optional: scan full git history with gitleaks.      │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 3  │  INSTALL                                             │
│          │  Creates isolated environments.                      │
│          │  Installs all declared dependencies.                 │
│          │  Auto-detects the right package manager.             │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 4  │  LINT / FORMAT                                       │
│          │  Runs the language-appropriate linter.               │
│          │  Python: ruff  .NET: dotnet format  Rust: clippy     │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 5  │  TEST                                                │
│          │  Runs your test suite.                               │
│          │  Python: pytest  .NET: dotnet test  Go: go test      │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 6  │  BUILD                                               │
│          │  Compiles or packages your application.              │
│          │  Docker: image scanned with trivy/grype after build. │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 7  │  VULNS  (optional — enable in config)               │
│          │  Scans dependencies for known CVEs.                  │
│          │  pip-audit --strict / npm audit --audit-level=high   │
│          │  --omit=dev / cargo audit / govulncheck ./...        │
│          │  / dotnet list package --vulnerable                  │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 8  │  OUTDATED  (optional, non-blocking)                  │
│          │  Reports newer package versions available.           │
│          │  NEVER fails the pipeline — informational only.      │
└──────────┴──────────────────────────────────────────────────────┘
```

### What Gets Detected and What Runs

| If the project contains… | Language detected | Tools used |
|--------------------------|-------------------|------------|
| `pyproject.toml`, `requirements.txt`, `setup.py`, `poetry.lock`, `uv.lock` | **Python** | venv + pip/poetry/uv → ruff → mypy → pytest |
| `package.json` | **Node.js** | npm/pnpm/yarn → lint → typecheck → test → build |
| `*.sln`, `*.csproj` (root or one level deep) | **.NET** | dotnet restore → format → build → test → vuln scan |
| `go.mod` | **Go** | go mod download → go vet → go build → go test |
| `Cargo.toml` | **Rust** | cargo fetch → clippy → build → test |
| `Dockerfile` or `Containerfile` | **Docker** | hadolint → docker build → trivy/grype scan |

> Polyglot repos are fully supported. A monorepo containing Python, Node, and Rust will run all three pipelines in a single `pipewarden` invocation — no configuration needed.

### Package Manager Auto-Detection

Pipewarden picks the right tool automatically:

**Python (priority order):**
```
1. uv.lock present AND uv on PATH?
      → uv sync --frozen          (10–100x faster than pip)

2. poetry.lock present AND poetry on PATH?
      → poetry install --no-interaction

3. pyproject.toml present?
      → pip install --quiet -e .   (editable install)

4. requirements.txt present?
      → pip install --quiet -r requirements.txt

5. None of the above?
      → step recorded as SKIPPED: "no manifest"
```

**Node.js (priority order):**
```
1. pnpm-lock.yaml?    → pnpm install --frozen-lockfile
2. yarn.lock?         → yarn install --frozen-lockfile
3. package-lock.json? → npm ci
4. (no lockfile)      → npm install
```

### Exit Codes — The Contract With Your CI

```
Exit Code  Meaning
─────────────────────────────────────────────────────────
    0      Everything passed (or skipped). Ship it.

    1      One or more stages failed (test failure,
           build error, lint error, etc.).
           Block the merge. Fix the issue.

    2      Bad CLI usage (unknown flag, invalid argument).
           Fix your workflow file.

    3      Invalid .pipewarden.toml.
           Fix your config file.

    4      Secrets specifically found — exposed credentials.
           Rotate the secret NOW. Assume it is compromised.
           Use exit code 4 to trigger a security alert in CI.

  130      SIGINT / Ctrl-C — run was cancelled.
```

**Why is there a separate exit code for secrets?** This lets CI scripts distinguish "a test failed" (code 1) from "a credential was leaked" (code 4) and trigger different responses — for example, paging an on-call security engineer only for code 4:

```bash
pipewarden
exit_code=$?
if [ $exit_code -eq 4 ]; then
  echo "CREDENTIAL LEAK DETECTED" | slack-notify "#security-alerts"
fi
```

---

## Python Projects — Complete Tutorial

### What a Python Pipeline Looks Like Before and After

**Before Pipewarden** — every Python project requires writing and maintaining its own CI:

```yaml
# 80+ lines across 4 separate jobs, manually maintained per project
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src/

  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: ${{ matrix.python-version }} }
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src --junit-xml=results.xml

  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

  vulns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pip-audit && pip-audit
```

**After Pipewarden** — 5 lines replace 80+:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
  security-events: write

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pipewarden
      - run: pipewarden --sarif-out report.sarif --junit-out junit.xml
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: report.sarif
```

Secret scanning, dependency installation, linting, type checking, testing, and vulnerability scanning — in the right order, every time, from one command.

---

### Step-by-Step: Exactly What Pipewarden Does for a Python Project

#### Step 1 — Detection

Pipewarden scans the project root for any of these files:

| File found | Result |
|------------|--------|
| `pyproject.toml` | Python stage enabled |
| `requirements.txt` | Python stage enabled |
| `setup.py` | Python stage enabled |
| `poetry.lock` | Python stage enabled (even without `pyproject.toml`) |
| `uv.lock` | Python stage enabled (even without `pyproject.toml`) |
| None of the above | Python stage skipped silently |

> `setup.cfg` alone does **not** trigger Python detection — only `pyproject.toml`, `requirements.txt`, `setup.py`, `poetry.lock`, or `uv.lock` do.

#### Step 2 — Create Virtual Environment

```bash
python -m venv .pipewarden-venv
```

Creates `.pipewarden-venv/` inside your project root. If it already exists, it is **reused** — making local re-runs fast.

```console
✓ py:venv (2.9s)    ← created fresh
✓ py:venv (0.0s)    ← reused existing (not shown if exists)
```

> Pipewarden **never touches** your existing `.venv`, `venv`, or `env` folder. It always uses its own isolated environment.

Add the folder to `.gitignore`:
```
.pipewarden-venv/
```

#### Step 3 — Install Dependencies

The step name in the output tells you exactly which path was taken:

```console
✓ py:deps(uv)            (1.2s)   ← uv sync --frozen was used
✓ py:deps(poetry)        (8.4s)   ← poetry install --no-interaction
✓ py:deps(pyproject)    (12.2s)   ← pip install -e .
✓ py:deps(requirements)  (9.7s)   ← pip install -r requirements.txt
```

#### Step 4 — Lint with ruff

```bash
ruff check .
```

```console
✓ py:lint(ruff) (0.3s)    ← No lint issues
✗ py:lint(ruff) (0.4s)    ← Lint errors found — full output printed below summary
· py:lint       (0.0s)    ← ruff not installed — step SKIPPED (not a failure), pipeline continues
```

**What ruff catches:**

| Category | Example |
|----------|---------|
| Unused imports | `import os` — never referenced |
| Undefined names | `pritn("hello")` — typo |
| Mutable defaults | `def f(x=[]):` — classic Python trap |
| Bare except | `except:` — silently swallows all errors |
| Shadowed builtins | `list = [1, 2, 3]` |
| Import order | Imports not grouped per PEP 8 |

If ruff is not on the PATH the step is `warned` — the pipeline does not fail. To enable linting:

```bash
pip install ruff            # globally
```

Or add it to your project:

```toml
# pyproject.toml
[project.optional-dependencies]
dev = ["ruff>=0.4.0"]
```

#### Step 5 — Type Check with mypy

mypy runs **only if both** conditions are met:
1. `mypy` is on the system PATH
2. A mypy config exists: `mypy.ini` exists, **or** `[tool.mypy]` in `pyproject.toml`

This prevents running mypy on a project with no type annotations and getting 500+ confusing errors.

```console
✓ py:typecheck(mypy) (1.2s)    ← All types are correct
✗ py:typecheck(mypy) (1.4s)    ← Type errors found
                                   (step not shown if mypy is unconfigured)
```

**Minimal mypy config to enable it:**

```toml
# pyproject.toml
[tool.mypy]
ignore_missing_imports = true
```

For strict type checking:

```toml
[tool.mypy]
strict = true
```

#### Step 6 — Test with pytest

If `pytest` is installed in the virtual environment and a `tests/` or `test/` directory exists:

```bash
python -m pytest -q
```

```console
✓ py:test(pytest) (6.2s)    ← All tests passed
✗ py:test(pytest) (6.4s)    ← Tests failed — last 60 lines printed automatically
⚠ py:test(pytest) (0.0s)    ← pytest not installed — add it as a dependency
```

If neither `tests/` nor `test/` exists and there is no `[tool.pytest.ini_options]` in `pyproject.toml`, the test step is silently skipped — not an error.

---

### Python Tutorial: Scenario A — New Package with uv (Modern Setup)

**Situation:** You have a brand-new Python package using `uv` for dependency management.

**Project layout:**
```
my-package/
├── pyproject.toml          ← Python detected; uv also detected
├── uv.lock                 ← uv selected as installer
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

**`pyproject.toml` (relevant parts):**
```toml
[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["requests>=2.28"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff>=0.4.0"]

[tool.mypy]
ignore_missing_imports = true
```

**Run Pipewarden:**
```bash
pipewarden
```

**What you see:**
```console
════════════════════════════════════════════════════════════════
  Pipewarden 1.3.1
════════════════════════════════════════════════════════════════
  root:     /home/alice/my-package
  config:   (defaults — no config file found)
  detected: python

════════════════════════════════════════════════════════════════
  Secrets
════════════════════════════════════════════════════════════════
✓ secrets:fallback (0.1s)

════════════════════════════════════════════════════════════════
  Python
════════════════════════════════════════════════════════════════
✓ py:venv (2.9s)
✓ py:deps(uv) (1.2s)
✓ py:lint(ruff) (0.3s)
✓ py:typecheck(mypy) (0.9s)
✓ py:test(pytest) (2.1s)

════════════════════════════════════════════════════════════════
  Summary
════════════════════════════════════════════════════════════════
  ✓ secrets:fallback    passed    0.1s   scanned 8 files, no secrets
  ✓ py:venv             passed    2.9s
  ✓ py:deps(uv)         passed    1.2s
  ✓ py:lint(ruff)       passed    0.3s
  ✓ py:typecheck(mypy)  passed    0.9s
  ✓ py:test(pytest)     passed    2.1s

  ✓ all 6 steps passed in 7.5s
```

**Why it worked:** Pipewarden found `uv.lock` and `uv` on the PATH, so it used `uv sync --frozen`. It found `[tool.mypy]` in `pyproject.toml`, so it also ran mypy.

---

### Python Tutorial: Scenario B — Legacy App with requirements.txt

**Situation:** You have an older Python application using `requirements.txt`.

**Project layout:**
```
my-flask-app/
├── requirements.txt        ← Python detected; pip selected
├── app/
│   ├── __init__.py
│   └── main.py
└── tests/
    └── test_main.py
```

**`requirements.txt`:**
```
flask==3.0.3
requests==2.31.0
pytest==8.1.1
ruff==0.4.4
```

> **Important:** `pytest` must be in `requirements.txt` (not only in a separate `requirements-dev.txt`). If it is only in a dev file, Pipewarden will not install it — add it to the main file or switch to `pyproject.toml` with extras.

**Run Pipewarden:**
```bash
pipewarden
```

**What you see:**
```console
  Python
✓ py:venv (2.9s)
✓ py:deps(requirements) (8.1s)
✓ py:lint(ruff) (0.3s)
✓ py:test(pytest) (3.4s)
```

**Run only Python (skip any other detected stages):**
```bash
pipewarden --only python
```

**Run with vulnerability scanning:**
```bash
# First, install pip-audit
pip install pip-audit

# Then enable vulns in config or run:
pipewarden --only python --only vulns
```

---

### Python Tutorial: Scenario C — Poetry Project

**Situation:** Your project uses Poetry for dependency management.

**Project layout:**
```
my-service/
├── pyproject.toml          ← Python detected
├── poetry.lock             ← Poetry selected as installer
├── my_service/
│   └── __init__.py
└── tests/
    └── conftest.py
```

**`pyproject.toml`:**
```toml
[tool.poetry]
name = "my-service"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.10"
httpx = "^0.27.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
ruff = "^0.4"

[tool.mypy]
ignore_missing_imports = true
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  Python
✓ py:venv (2.9s)
✓ py:deps(poetry) (6.4s)
✓ py:lint(ruff) (0.3s)
✓ py:typecheck(mypy) (1.1s)
✓ py:test(pytest) (4.2s)
```

---

### Python Tutorial: Scenario D — FastAPI / Django Web App with Docker

**Situation:** You have a FastAPI (or Django) web app with a Dockerfile. You want to lint, test, and build the Docker image in one command.

**Project layout:**
```
my-api/
├── pyproject.toml
├── uv.lock
├── src/
│   └── api/
│       ├── main.py
│       ├── models.py
│       └── routers/
│           └── users.py
├── tests/
│   ├── conftest.py
│   └── test_endpoints.py
└── Dockerfile
```

**`pyproject.toml`:**
```toml
[project]
name = "my-api"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.111",
    "uvicorn[standard]>=0.30",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "httpx>=0.27",    # for TestClient
    "ruff>=0.4",
]

[tool.mypy]
strict = false
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**`Dockerfile`:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

COPY src/ ./src/
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  Secrets
✓ secrets:fallback (0.1s)

  Python
✓ py:venv (2.9s)
✓ py:deps(uv) (1.3s)
✓ py:lint(ruff) (0.4s)
✓ py:typecheck(mypy) (2.1s)
✓ py:test(pytest) (8.7s)

  Docker
✓ docker:lint(hadolint) (0.2s)    ← Dockerfile best-practice check
✓ docker:build (22.1s)            ← docker build runs
✓ docker:scan(trivy) (8.4s)       ← only appears if trivy or grype is on PATH; absent otherwise (no WARNED step)
```

Both the Python pipeline and the Docker pipeline run automatically from a single `pipewarden` command.

**To run in CI with SARIF security report:**
```yaml
- run: pip install pipewarden
- run: pipewarden --sarif-out report.sarif --junit-out junit.xml
```

---

### Python Tutorial: Scenario E — Data Science / ML Project

**Situation:** A data science project with heavy dependencies (NumPy, pandas, PyTorch).

**Project layout:**
```
my-analysis/
├── requirements.txt        ← Python detected
├── notebooks/
│   └── analysis.ipynb
├── src/
│   └── preprocess.py
└── tests/
    └── test_preprocess.py
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  Python
✓ py:venv (2.9s)
✓ py:deps(requirements) (45.2s)   ← slow — numpy, pandas, torch are large
✓ py:lint(ruff) (0.3s)
✓ py:test(pytest) (3.1s)
```

**Tip:** For large dependencies, increase the install timeout:

```toml
# .pipewarden.toml
[timeouts]
install_s = 1800    # 30 minutes
```

**Notebooks are not executed** — only Python source files in `src/` and `tests/` are linted and tested.

---

### Python Tutorial: Scenario F — AWS Lambda Function

**Situation:** A Lambda function with no Dockerfile but with a `requirements.txt`.

**Project layout:**
```
my-lambda/
├── requirements.txt
├── handler.py
└── tests/
    └── test_handler.py
```

**Run locally:**
```bash
pipewarden --only secrets --only python
```

**Run in CI with secrets check and vulnerability scanning:**
```bash
pipewarden --only secrets --only python --only vulns
```

**`.pipewarden.toml`:**
```toml
fail_fast = true        # stop immediately if secrets are found

[stages]
python = true
vulns  = true           # check for CVEs in Lambda dependencies
docker = false          # no Dockerfile
node   = false
dotnet = false

[secrets]
allowlist_paths = [
    "tests/fixtures/**",
]
```

---

### Python Tutorial: Scenario G — Microservice Monorepo

**Situation:** A monorepo with three Python microservices, each in its own subdirectory.

**Project layout:**
```
services/
├── auth-service/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── tests/
├── payment-service/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── tests/
└── notification-service/
    ├── pyproject.toml
    ├── uv.lock
    └── tests/
```

**Run each service independently:**
```bash
pipewarden --root ./services/auth-service
pipewarden --root ./services/payment-service
pipewarden --root ./services/notification-service
```

**In CI — run all three in parallel jobs:**
```yaml
jobs:
  auth:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pipewarden
      - run: pipewarden --root ./services/auth-service --junit-out auth-junit.xml

  payment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pipewarden
      - run: pipewarden --root ./services/payment-service --junit-out payment-junit.xml

  notification:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pipewarden
      - run: pipewarden --root ./services/notification-service --junit-out notification-junit.xml
```

---

### Python Configuration Examples

**Run only Python (skip all other detected languages):**
```bash
pipewarden --only python
```

**Run secrets + Python (recommended pre-push hook):**
```bash
pipewarden --only secrets --only python
```

**Stop immediately on the first failure:**
```bash
pipewarden --only python --fail-fast
```

**Tune timeouts for a slow test suite:**
```toml
# .pipewarden.toml
[timeouts]
test_s    = 3600    # 60 minutes
install_s = 1800    # 30 minutes for heavy deps
```

**Enable vulnerability scanning:**
```toml
[stages]
vulns = true
```

**Full config for a Python microservice:**
```toml
# .pipewarden.toml
fail_fast = false

[stages]
python = true
docker = true
vulns  = true
node   = false
dotnet = false
go     = false
rust   = false

[timeouts]
install_s = 600
test_s    = 1200

[secrets]
allowlist_paths = [
    "tests/fixtures/**",
    "docs/**",
]
```

---

### Python Local Development Workflow

```bash
# First run — creates .pipewarden-venv and installs all deps (~10–30s)
pipewarden

# Subsequent runs — reuses venv, much faster
pipewarden

# Quick lint + test loop while developing
pipewarden --only python

# Pre-commit check: secrets only (sub-second)
pipewarden --only secrets

# Pre-push full check
pipewarden --only secrets --only python

# Force reinstall after changing dependencies
rm -rf .pipewarden-venv          # macOS/Linux
Remove-Item -Recurse -Force .pipewarden-venv   # Windows
pipewarden

# Preview what would run without executing
pipewarden --dry-run
```

---

### Python Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `py:deps` fails — `No module named pip` | Broken Python install | Reinstall Python or use pyenv/mise |
| `py:test` shows `WARNED: pytest not installed` | pytest not in project deps | Add `pytest` to `requirements.txt` or `pyproject.toml` |
| `py:lint` shows `⚠ ruff not installed` | ruff not on PATH | `pip install ruff` globally |
| `py:typecheck` never runs | mypy not configured | Add `[tool.mypy]` section to `pyproject.toml` |
| Tests time out | Slow suite or infinite loop | Increase `test_s` in config |
| Venv creation fails on Windows | Antivirus or permission issue | Add project folder to AV exclusions |
| Poetry install misses dev deps | Expected — poetry installs all groups by default | No action needed |
| uv not found despite being installed | uv not on system PATH | `pip install uv` to install globally |

---

## .NET Projects — Complete Tutorial

### What a .NET Pipeline Looks Like Before and After

**Before Pipewarden** — a typical production .NET CI pipeline:

```yaml
# 100+ lines across 3 separate jobs
jobs:
  build-and-test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        dotnet-version: ['8.0.x', '9.0.x']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with: { dotnet-version: ${{ matrix.dotnet-version }} }
      - uses: actions/cache@v4
        with:
          path: ~/.nuget/packages
          key: ${{ runner.os }}-nuget-${{ hashFiles('**/*.csproj') }}
      - run: dotnet restore
      - run: dotnet build --no-restore --configuration Release --nologo
      - run: |
          dotnet test --no-build --configuration Release --nologo \
            --logger "trx;LogFileName=test-results.trx" \
            --collect:"XPlat Code Coverage" \
            --results-directory ./TestResults
      - run: dotnet tool install -g trx2junit    # TRX → JUnit converter
      - run: trx2junit ./TestResults/*.trx
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.os }}-${{ matrix.dotnet-version }}
          path: ./TestResults/*.xml

  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

  code-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with: { dotnet-version: '9.0.x' }
      - uses: github/codeql-action/init@v3
        with: { languages: csharp }
      - run: dotnet build
      - uses: github/codeql-action/analyze@v3
```

**After Pipewarden** — 5 lines replace 100+:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
  security-events: write

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pipewarden
      - run: pipewarden --sarif-out report.sarif --junit-out junit.xml
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: report.sarif
```

Pipewarden handles: secret scanning, dotnet restore, dotnet format (code style check), dotnet build, dotnet test, and vulnerability scanning — all from one command with JUnit XML output natively (no trx2junit needed).

---

### Step-by-Step: Exactly What Pipewarden Does for a .NET Project

#### Step 1 — Detection

| File found | Result |
|------------|--------|
| `*.sln` | .NET stage enabled; all commands target the solution |
| `*.csproj` | .NET stage enabled; commands target this project |
| `*.fsproj` | .NET stage enabled (F# projects) |
| `*.vbproj` | .NET stage enabled (VB.NET projects) |
| None | .NET stage skipped silently |

If both `.sln` and `.csproj` are present, the `.sln` takes priority.

#### Step 2 — dotnet restore

```bash
dotnet restore
```

Downloads all NuGet packages declared in every project in the solution.

```console
✓ dotnet:restore (12.4s)    ← All packages resolved and downloaded
✗ dotnet:restore  (8.1s)    ← Failed — exact error printed below summary
```

If this step fails, Pipewarden stops — no point building without dependencies. The exact output from `dotnet restore` is printed so you see the specific package that failed.

**Common failure causes:**
- A package version was removed from NuGet.org
- A private feed credential is missing or expired
- The solution references a project file that does not exist on disk

#### Step 3 — dotnet format (code style check)

```bash
dotnet format --verify-no-changes
```

Checks that all C#/F#/VB files comply with `.editorconfig` code style rules **without modifying any files**. Fails if any file would be changed.

```console
✓ dotnet:format (1.2s)    ← All files are correctly formatted
✗ dotnet:format (0.8s)    ← Formatting violations — run `dotnet format` locally to fix
```

**To fix locally:**
```bash
dotnet format    # rewrites files in place, then commit the changes
```

**To disable** (for legacy projects without `.editorconfig`):
```toml
# .pipewarden.toml
[dotnet]
format = false
```

#### Step 4 — dotnet build

```bash
dotnet build --no-restore --nologo
```

Compiles every project in the solution.

- `--no-restore` — skips NuGet restore (already done); without this flag it would restore again, adding unnecessary time
- `--nologo` — suppresses the "Build Engine version…" Microsoft header

```console
✓ dotnet:build (18.7s)    ← Compiled, zero errors
✗ dotnet:build (14.2s)    ← Compilation errors — full compiler output printed
```

**What a build failure looks like:**
```
── dotnet:build ──
src/MyApp.Api/Controllers/UserController.cs(42,18): error CS0246:
  The type or namespace name 'UserService' could not be found
  (are you missing a using directive or an assembly reference?)

Build FAILED.
  Errors: 1
  Warnings: 3
```

The file, line number, and error code are printed — no log archaeology.

#### Step 5 — dotnet test

```bash
dotnet test --no-build --nologo
```

Runs every test project in the solution.

- `--no-build` — skips compilation (already done); without this, dotnet would rebuild before testing

```console
✓ dotnet:test (8.3s)     ← All tests passed
✗ dotnet:test (11.2s)    ← Failures — last 60 lines printed
```

**What a test failure looks like:**
```
── dotnet:test ──
  Failed MyApp.Tests.UserControllerTests.GetUser_Returns404_WhenNotFound [12ms]
  Error Message:
    Assert.Equal() Failure: Values differ
    Expected: 404
    Actual:   200

Failed!  - Failed:     1, Passed:    47, Skipped:     0, Total:    48
```

**Which projects are tested?** Any project in the solution referencing:
- `xunit` or `xunit.runner.visualstudio`
- `NUnit` or `NUnit3TestAdapter`
- `MSTest.TestFramework` or `MSTest.TestAdapter`
- Or any project with `<IsTestProject>true</IsTestProject>` in its `.csproj`

#### Step 6 — Vulnerability Scan (opt-in, default on)

```bash
dotnet list package --vulnerable --include-transitive
```

Checks every NuGet package against the **GitHub Advisory Database**. `--include-transitive` catches vulnerabilities in indirect dependencies.

```console
✓ dotnet:vulns (4.1s)    ← No vulnerable packages
✗ dotnet:vulns (3.8s)    ← CVEs found — package, version, severity, advisory ID printed
```

**To disable:**
```toml
[dotnet]
vulns = false
```

---

### .NET Tutorial: Scenario A — Solution with API + Library + Tests (Most Common)

**Situation:** A standard enterprise structure with an ASP.NET Core Web API, a business logic library, a data access layer, and xUnit test projects.

**Project layout:**
```
MyApp/
├── MyApp.sln                          ← .NET detected
├── src/
│   ├── MyApp.Api/
│   │   ├── MyApp.Api.csproj           ← ASP.NET Core Web API
│   │   ├── Program.cs
│   │   └── Controllers/
│   │       └── UserController.cs
│   ├── MyApp.Core/
│   │   ├── MyApp.Core.csproj          ← Business logic class library
│   │   └── Services/
│   │       └── UserService.cs
│   └── MyApp.Data/
│       ├── MyApp.Data.csproj          ← EF Core data access
│       └── Repositories/
│           └── UserRepository.cs
└── tests/
    ├── MyApp.Api.Tests/
    │   └── MyApp.Api.Tests.csproj     ← xUnit tests
    └── MyApp.Core.Tests/
        └── MyApp.Core.Tests.csproj    ← xUnit tests
```

**`.editorconfig`:**
```ini
root = true
[*.cs]
indent_style = space
indent_size = 4
dotnet_sort_system_directives_first = true
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
════════════════════════════════════════════════════════════════
  Pipewarden 1.3.1
════════════════════════════════════════════════════════════════
  root:     /home/alice/MyApp
  config:   (defaults — no config file found)
  detected: dotnet(MyApp.sln)

════════════════════════════════════════════════════════════════
  Secrets
════════════════════════════════════════════════════════════════
✓ secrets:fallback (0.1s)

════════════════════════════════════════════════════════════════
  .Net
════════════════════════════════════════════════════════════════
✓ dotnet:restore (12.4s)
✓ dotnet:format  (1.2s)
✓ dotnet:build   (18.7s)
✓ dotnet:test    (8.3s)
✓ dotnet:vulns   (4.1s)

════════════════════════════════════════════════════════════════
  Summary
════════════════════════════════════════════════════════════════
  ✓ secrets:fallback  passed    0.1s   scanned 22 files, no secrets
  ✓ dotnet:restore    passed   12.4s
  ✓ dotnet:format     passed    1.2s
  ✓ dotnet:build      passed   18.7s   5 projects compiled
  ✓ dotnet:test       passed    8.3s   48 tests across 2 test projects
  ✓ dotnet:vulns      passed    4.1s   no vulnerable packages

  ✓ all 6 steps passed in 44.8s
```

---

### .NET Tutorial: Scenario B — ASP.NET Core Minimal API

**Situation:** A modern .NET 9 minimal API — no controllers, just `Program.cs`.

**Project layout:**
```
OrdersApi/
├── OrdersApi.sln
├── src/
│   └── OrdersApi/
│       ├── OrdersApi.csproj
│       └── Program.cs
└── tests/
    └── OrdersApi.Tests/
        ├── OrdersApi.Tests.csproj
        └── OrderEndpointTests.cs
```

**`OrdersApi.csproj`:**
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

**`OrdersApi.Tests.csproj`:**
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="9.0.0" />
    <PackageReference Include="xunit" Version="2.9.0" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
</Project>
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  .Net
✓ dotnet:restore  (5.1s)
✓ dotnet:format   (0.9s)
✓ dotnet:build    (8.4s)
✓ dotnet:test     (3.2s)
✓ dotnet:vulns    (2.8s)
```

---

### .NET Tutorial: Scenario C — ASP.NET Core + Dockerfile (Polyglot)

**Situation:** An ASP.NET Core web API with a Dockerfile for containerised deployment.

**Project layout:**
```
MyWebApi/
├── MyWebApi.sln
├── src/
│   └── MyWebApi/
│       ├── MyWebApi.csproj
│       ├── Program.cs
│       └── appsettings.json
├── tests/
│   └── MyWebApi.Tests/
│       └── MyWebApi.Tests.csproj
└── Dockerfile
```

**`Dockerfile`:**
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /app
COPY . .
RUN dotnet restore && dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=build /app/out .
ENTRYPOINT ["dotnet", "MyWebApi.dll"]
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  Secrets
✓ secrets:fallback      (0.1s)

  .Net
✓ dotnet:restore        (10.2s)
✓ dotnet:format          (1.1s)
✓ dotnet:build          (15.4s)
✓ dotnet:test            (5.2s)
✓ dotnet:vulns           (3.9s)

  Docker
✓ docker:lint(hadolint)  (0.3s)
✓ docker:build          (45.2s)
✓ docker:scan(trivy)     (8.1s)
```

Secret scanning, .NET pipeline, Docker build, and container CVE scan — all from `pipewarden`.

---

### .NET Tutorial: Scenario D — Console Application (No Test Project)

**Situation:** A standalone console tool with no test project yet.

**Project layout:**
```
MyTool/
├── MyTool.csproj
└── Program.cs
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  .Net
✓ dotnet:restore  (3.1s)
✓ dotnet:build    (5.4s)
· dotnet:test               ← skipped — no test project found
```

The test step is silently skipped — not an error. This is correct for a project with no tests.

---

### .NET Tutorial: Scenario E — Worker Service / Background Service

**Situation:** A .NET Worker Service (background processing, hosted service).

**Project layout:**
```
OrderProcessor/
├── OrderProcessor.sln
├── src/
│   └── OrderProcessor/
│       ├── OrderProcessor.csproj    ← Worker project
│       ├── Program.cs
│       └── Workers/
│           └── OrderConsumerWorker.cs
└── tests/
    └── OrderProcessor.Tests/
        └── OrderProcessor.Tests.csproj
```

**`OrderProcessor.csproj`:**
```xml
<Project Sdk="Microsoft.NET.Sdk.Worker">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <UserSecretsId>...</UserSecretsId>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Hosting" Version="9.0.0" />
    <PackageReference Include="Azure.Messaging.ServiceBus" Version="7.18.0" />
  </ItemGroup>
</Project>
```

> **Secret scanning tip:** Worker Services often connect to message buses, databases, and queues. Do not put connection strings in `appsettings.json`. Use environment variables or Azure Key Vault, and let Pipewarden catch anything that slips through.

**`.pipewarden.toml`:**
```toml
[secrets]
allowlist_paths = [
    "tests/TestData/**",    # test fixtures with fake credentials
]

[dotnet]
format = true
vulns  = true

[timeouts]
install_s = 600
build_s   = 600
test_s    = 1200
```

**Run:**
```bash
pipewarden
```

---

### .NET Tutorial: Scenario F — Blazor Server Application

**Situation:** A Blazor Server app with shared components and an xUnit test project.

**Project layout:**
```
MyBlazorApp/
├── MyBlazorApp.sln
├── src/
│   ├── MyBlazorApp.Server/
│   │   ├── MyBlazorApp.Server.csproj
│   │   └── Pages/
│   └── MyBlazorApp.Shared/
│       ├── MyBlazorApp.Shared.csproj
│       └── Models/
└── tests/
    └── MyBlazorApp.Tests/
        └── MyBlazorApp.Tests.csproj
```

**Run:**
```bash
pipewarden
```

**What you see:**
```console
  .Net
✓ dotnet:restore   (9.8s)
✓ dotnet:format    (1.4s)
✓ dotnet:build    (22.1s)    ← Blazor build includes CSS isolation, Razor compilation
✓ dotnet:test      (4.7s)
✓ dotnet:vulns     (3.2s)
```

---

### .NET Tutorial: Scenario G — Microservice with Private NuGet Feed

**Situation:** A .NET microservice that depends on packages from a private Azure Artifacts feed.

**Project layout:**
```
PaymentService/
├── PaymentService.sln
├── NuGet.config              ← private feed configuration
├── src/
│   └── PaymentService/
│       └── PaymentService.csproj
└── tests/
    └── PaymentService.Tests/
        └── PaymentService.Tests.csproj
```

**`NuGet.config`:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <add key="nuget.org"     value="https://api.nuget.org/v3/index.json" />
    <add key="MyPrivateFeed" value="https://pkgs.dev.azure.com/myorg/_packaging/myfeed/nuget/v3/index.json" />
  </packageSources>
  <packageSourceCredentials>
    <MyPrivateFeed>
      <add key="Username"          value="%NUGET_USERNAME%" />
      <add key="ClearTextPassword" value="%NUGET_TOKEN%" />
    </MyPrivateFeed>
  </packageSourceCredentials>
</configuration>
```

Pipewarden passes your environment variables through to `dotnet restore` automatically.

**In GitHub Actions:**
```yaml
- name: Run Pipewarden
  env:
    NUGET_USERNAME: ${{ github.actor }}
    NUGET_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: pipewarden --junit-out junit.xml
```

**In Azure DevOps:**
```yaml
- script: pipewarden --junit-out junit.xml
  displayName: Run Pipewarden
  env:
    NUGET_USERNAME: $(Build.RequestedFor)
    NUGET_TOKEN: $(System.AccessToken)
```

---

### .NET Configuration Examples

**No config needed for a simple project:**
```bash
pipewarden    # auto-detects .sln, runs restore → build → test
```

**Skip Docker (no daemon in this CI environment):**
```toml
# .pipewarden.toml
[stages]
docker = false
```

Or from the CLI:
```bash
pipewarden --skip docker
```

**Increase timeouts for large enterprise solutions:**
```toml
[timeouts]
install_s = 600      # 10 min for NuGet restore
build_s   = 1200     # 20 min to compile large solutions
test_s    = 3600     # 60 min for extensive test suites
```

**Run only .NET (skip everything else):**
```bash
pipewarden --only dotnet
```

**Combine secrets + .NET (good for pre-push hooks):**
```bash
pipewarden --only secrets --only dotnet
```

**Pinning the .NET SDK Version:**

Add a `global.json` to ensure everyone builds with the same SDK:
```json
{
  "sdk": {
    "version": "9.0.100",
    "rollForward": "latestPatch"
  }
}
```

Pipewarden respects `global.json` — it does not override or replace the SDK selection.

**Full config for a .NET microservice:**
```toml
# .pipewarden.toml
fail_fast = false

[stages]
dotnet = true
docker = true
vulns  = true
python = false
node   = false
go     = false
rust   = false

[dotnet]
format   = true    # enforce code formatting via dotnet format
vulns    = true    # scan NuGet packages for CVEs
outdated = true    # report available upgrades (non-blocking)

[timeouts]
install_s = 600
build_s   = 900
test_s    = 1800

[secrets]
allowlist_paths = [
    "tests/TestData/**",     # test fixtures with fake credentials
    "docs/**",               # documentation examples
]
```

---

### .NET Local Development Workflow

```bash
# Full check — detects solution, runs restore → build → test
pipewarden

# .NET only (skip secrets, Docker, etc.)
pipewarden --only dotnet

# Stop on first failure (tight feedback loop while debugging)
pipewarden --only dotnet --fail-fast

# Run against a specific subdirectory (monorepo)
pipewarden --root ./services/payment-service

# Generate JUnit results for a local IDE test report
pipewarden --only dotnet --junit-out results.xml

# Preview what would run without executing
pipewarden --dry-run
```

---

### .NET Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `dotnet:restore` fails — `Unable to find package X` | Missing NuGet source | Check `NuGet.config`; verify feed URL is correct |
| `dotnet:restore` fails — `401 Unauthorized` | Private feed credential missing | Set `NUGET_USERNAME` and `NUGET_TOKEN` env vars |
| `dotnet:restore` fails — `No executable found: dotnet` | .NET SDK not installed | Install from dotnet.microsoft.com/download |
| `dotnet:build` fails — `framework 'net9.0' not found` | Wrong SDK version installed | Install the required SDK; add `global.json` to pin version |
| `dotnet:test` shows 0 tests found | No test framework referenced | Add `xunit` / `NUnit` / `MSTest` to a test project `.csproj` |
| `dotnet:test` times out | Large test suite | Increase `test_s` in `.pipewarden.toml` |
| Build succeeds locally, fails in CI | SDK version mismatch | Add `global.json` to pin the exact SDK version |
| Many nullable warnings break the build | `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` | Fix the null safety issues, or suppress specific codes with `<NoWarn>CS8600</NoWarn>` |
| `dotnet:restore` is slow in CI | No NuGet package cache | Add a cache step before Pipewarden in your CI YAML |
| `dotnet:format` fails on a legacy project | No `.editorconfig` or conflicting rules | Set `[dotnet] format = false` in `.pipewarden.toml` |

---

## Node.js / Go / Rust — Quick Guides

### Node.js

**Detected when:** `package.json` is present.

**What runs:**

| Step | Command | Condition |
|------|---------|-----------|
| Install | `npm ci` / `pnpm install --frozen-lockfile` / `yarn install --frozen-lockfile` | Lockfile determines which tool |
| Lint | `npm run lint` | Only if `"lint"` script exists in `package.json` |
| Type check | `npm run typecheck` | Only if `"typecheck"` script exists |
| Test | `npm test` | Only if `"test"` script exists |
| Build | `npm run build` | Only if `"build"` script exists |

**Example output:**
```console
  Node
✓ node:deps(npm)   (8.4s)
✓ node:lint        (3.2s)
✓ node:test       (12.1s)
✓ node:build       (5.7s)
```

**Example `package.json` scripts section:**
```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "typecheck": "tsc --noEmit",
    "test": "jest --ci",
    "build": "tsc -p tsconfig.build.json"
  }
}
```

**Common config:**
```toml
[stages]
node   = true
docker = false
```

**Troubleshooting:**

| Symptom | Fix |
|---------|-----|
| `node:lint` skipped | Add `"lint": "eslint ."` to `package.json` scripts |
| `node:test` skipped | Add `"test": "jest"` to scripts |
| `node:deps` fails — `npm ci` requires lockfile | Run `npm install` locally first to generate `package-lock.json` |
| Slow install | Install pnpm (`npm i -g pnpm`) — Pipewarden picks it up automatically |

---

### Go

**Detected when:** `go.mod` is present.

**What runs:**

| Step | Command |
|------|---------|
| Download modules | `go mod download` |
| Vet | `go vet ./...` |
| Build | `go build ./...` |
| Test | `go test ./...` |

**Example output:**
```console
  Go
✓ go:deps   (4.2s)
✓ go:vet    (0.8s)
✓ go:build  (3.1s)
✓ go:test   (7.4s)
```

**Example `.pipewarden.toml` for a Go service:**
```toml
[stages]
go     = true
docker = true
vulns  = true    # uses govulncheck if installed

[timeouts]
test_s = 900
```

**Troubleshooting:**

| Symptom | Fix |
|---------|-----|
| `go:deps` fails — `GOPROXY` error | Set `GOPROXY=direct` or ensure network access to `proxy.golang.org` |
| `go:test` times out | Increase `test_s` in `.pipewarden.toml` |
| Build fails — Go version mismatch | The `go.mod` `go` directive controls version; upgrade with `go mod tidy` |

---

### Rust

**Detected when:** `Cargo.toml` is present.

**What runs:**

| Step | Command |
|------|---------|
| Fetch crates | `cargo fetch` |
| Lint (Clippy) | `cargo clippy --all-targets -- -D warnings` |
| Build | `cargo build --all-targets` |
| Test | `cargo test --all-targets` |

**Example output:**
```console
  Rust
✓ rust:deps         (12.1s)
✓ rust:lint(clippy)  (8.4s)
✓ rust:build        (22.3s)
✓ rust:test          (6.7s)
```

**Troubleshooting:**

| Symptom | Fix |
|---------|-----|
| `cargo clippy` fails with warnings | Fix the warnings; they are treated as errors (`-D warnings`) — intentional |
| `rust:deps` times out on first run | Increase `install_s`; first Rust builds download many crates |
| `rust:build` slow in CI | Consider `sccache` or `cargo-cache` to reuse the Cargo registry across runs |

---

## Polyglot Repos (Multiple Languages)

If your project contains files for multiple languages — `pyproject.toml` AND `package.json` AND `go.mod`, for example — Pipewarden detects all of them and runs each pipeline in sequence automatically.

**Example — a microservice platform repo:**
```
platform/
├── backend/
│   └── pyproject.toml       ← Python
├── frontend/
│   └── package.json         ← Node.js
├── gateway/
│   └── go.mod               ← Go
└── Dockerfile               ← Docker
```

**Run from the repo root:**
```bash
pipewarden
```

**What you see:**
```console
  Secrets
✓ secrets:fallback   (0.2s)

  Python
✓ py:venv            (2.9s)
✓ py:deps(pyproject) (8.1s)
✓ py:lint(ruff)      (0.4s)
✓ py:test(pytest)    (6.2s)

  Node
✓ node:deps(npm)     (8.4s)
✓ node:lint          (3.2s)
✓ node:test         (12.1s)
✓ node:build         (5.7s)

  Go
✓ go:deps            (4.2s)
✓ go:vet             (0.8s)
✓ go:build           (3.1s)
✓ go:test            (7.4s)

  Docker
✓ docker:lint        (0.2s)
✓ docker:build      (18.3s)
```

To run only one language in a polyglot repo:
```bash
pipewarden --only python
pipewarden --only node
pipewarden --only go
pipewarden --only dotnet
```

---

## Secret Scanning — Deep Dive

Secret scanning runs **first**, before any code is installed or built. If secrets are found, the pipeline stops immediately with exit code 4.

### Detection Strategy

```
gitleaks installed AND prefer_external = true?
  YES → Use gitleaks (150+ patterns, maintained by security experts)
        Exception: if --diff is also used, fall back to built-in scanner
        (gitleaks cannot natively scope a scan to a git ref range)
  NO  → Use built-in regex scanner (46 high-precision patterns)
```

**Install gitleaks for broader coverage:**

```bash
# macOS
brew install gitleaks

# Linux (download binary)
curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64.tar.gz | tar -xz
sudo mv gitleaks /usr/local/bin/

# Windows (via winget)
winget install gitleaks

# Verify
gitleaks version
```

Once installed, Pipewarden picks it up automatically — `secrets:gitleaks` replaces `secrets:fallback` in the output.

### Scanning Full Git History (Audit Mode)

By default, Pipewarden scans only the **working tree** — files on disk right now.

For a thorough audit (e.g. before open-sourcing a private repo), scan the entire git history:

```toml
# .pipewarden.toml
[secrets]
scan_history = true    # uses gitleaks detect over full git history
```

> Requires `gitleaks`. History scanning can take several minutes on large repos. Use for one-time audits, not on every commit.

### What the Built-in Scanner Detects (46 Patterns)

**Cloud provider credentials:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `aws.access_key` | CRITICAL | AWS IAM Access Key ID (`AKIA` + 16 chars) |
| `aws.secret_key` | CRITICAL | AWS Secret Access Key |
| `aws.sts_key` | HIGH | AWS STS / temporary key (`ASIA` + 16 chars) |
| `google.api_key` | HIGH | Google API Key (`AIza` + 35 chars) |

**Version control & CI tokens:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `github.pat_classic` | CRITICAL | GitHub PAT (`ghp_` + 36 chars) |
| `github.pat_fine_grained` | CRITICAL | GitHub Fine-Grained PAT (`github_pat_` + 82 chars) |
| `github.oauth` | CRITICAL | GitHub OAuth Token (`gho_` + 36 chars) |
| `github.actions_token` | CRITICAL | GitHub Actions Runner Token (`ghs_` + 36 chars) |
| `github.user_token` | CRITICAL | GitHub User-to-Server Token (`ghu_` + 36 chars) |
| `gitlab.pat` | CRITICAL | GitLab PAT (`glpat-` + 20 chars) |
| `digitalocean.token` | CRITICAL | DigitalOcean Token (`dop_v1_` + 64 chars) |
| `linear.api_key` | HIGH | Linear API Key (`lin_api_` + 40 chars) |
| `okta.token` | HIGH | Okta SSWS API Token (`SSWS ` + 42 chars) |

**Database connection strings:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `mongodb.connection_string` | CRITICAL | MongoDB URI with credentials |
| `postgres.connection_string` | CRITICAL | PostgreSQL URI with credentials |
| `mysql.connection_string` | CRITICAL | MySQL URI with credentials |
| `redis.connection_string` | CRITICAL | Redis URI with password |
| `mssql.connection_string` | CRITICAL | SQL Server ADO.NET connection string |
| `jdbc.connection_string` | CRITICAL | JDBC URL with password param |
| `amqp.connection_string` | HIGH | AMQP / RabbitMQ URI with credentials |

**Azure connection strings:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `azure.storage_connection_string` | CRITICAL | Azure Storage Account Key |
| `azure.cosmos_connection_string` | CRITICAL | Azure Cosmos DB Account Key |
| `azure.servicebus_connection_string` | CRITICAL | Azure Service Bus SAS Key |

**AI / ML service API keys:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `anthropic.api_key` | CRITICAL | Anthropic API Key (`sk-ant-`) |
| `openai.api_key` | CRITICAL | OpenAI API Key classic (`sk-` + 48 chars) |
| `openai.api_key_project` | CRITICAL | OpenAI Project Key (`sk-proj-`) |
| `huggingface.token` | CRITICAL | Hugging Face token (`hf_`) |
| `replicate.token` | HIGH | Replicate token (`r8_`) |

**Payment & e-commerce:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `stripe.live_key` | CRITICAL | Stripe Live Secret Key (`sk_live_`) |
| `shopify.access_token` | CRITICAL | Shopify Admin API Token (`shpat_` + 32 chars) |
| `shopify.storefront_token` | CRITICAL | Shopify Storefront API Token (`shpss_` + 32 chars) |
| `shopify.custom_app_token` | CRITICAL | Shopify Custom App Token (`shpca_` + 32 chars) |
| `stripe.restricted` | HIGH | Stripe Restricted Key (`rk_live_`) |
| `stripe.webhook_secret` | HIGH | Stripe Webhook Signing Secret (`whsec_`) |
| `stripe.test_key` | MEDIUM | Stripe Test Secret Key (`sk_test_`) |

**Communication & messaging:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `slack.token` | HIGH | Slack Bot/App Token (`xox[abprs]-...`) |
| `sendgrid.api_key` | HIGH | SendGrid API Key (`SG.`) |
| `twilio.account_sid` | HIGH | Twilio Account SID |
| `telegram.bot_token` | HIGH | Telegram Bot Token |

**Private keys and certificates:**

| Rule ID | Severity | What It Finds |
|---------|----------|---------------|
| `private_key.pem` | CRITICAL | PEM Private Key Block (`-----BEGIN ... PRIVATE KEY-----`) |
| `npm.token` | HIGH | npm Automation Token (`npm_`) |
| `pypi.api_token` | HIGH | PyPI API Token (`pypi-`) |
| `jwt` | MEDIUM | JSON Web Token (`eyJ...eyJ...`) |

### Severity Levels Explained

| Severity | Meaning | Immediate Action |
|----------|---------|-----------------|
| CRITICAL | Direct service access (cloud keys, DB URIs, private keys) | Rotate immediately. Assume compromised. |
| HIGH | Scoped token with significant blast radius | Rotate within hours. Audit access logs. |
| MEDIUM | Lower-impact or possible false positive | Review and rotate if real. |
| LOW | Very low risk finding | Review at your discretion. |
| INFO | Informational only | Review at your discretion. |

### Understanding the Findings Output

When a secret is found:

```
  CRITICAL  src/config.py:14  [aws.access_key]  AKIA…WXYZ
  │          │                  │                 │
  │          │                  │                 └─ Truncated snippet — first 4 and last 4 chars only
  │          │                  │                    Never printed in full — safe to share in logs
  │          │                  └─ Rule ID that matched
  │          └─ File path : line number
  └─ Severity level
```

**Snippet truncation rule:** If the matched value is 16 characters or shorter it is shown in full. If it is longer than 16 characters it is truncated to `first4…last4` — e.g. `AKIA…WXYZ`. This is intentional: findings are logged safely without exposing the full credential in CI logs. The truncation is not configurable.

### Smart Allowlisting

For test fixtures or documentation examples that look like secrets:

```toml
# .pipewarden.toml
[secrets]
# Skip specific files or directories — supports ** glob (like gitignore)
allowlist_paths = [
    "tests/fixtures/**",    # all test fixture files
    "docs/examples/**",     # documentation examples
    "*.md",                 # all markdown files at root
]

# Skip a specific rule everywhere
allowlist_rules = ["jwt"]

# Ignore a specific known-safe string (e.g. AWS docs dummy key)
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]
```

### What Is NOT Scanned

To keep scans fast and accurate, the following are automatically skipped:
- **Binary files** — images, PDFs, compiled binaries, fonts, audio/video archives (`.png`, `.exe`, `.dll`, `.jar`, `.zip`, `.woff`, `.mp4`, etc.)
- **Build output** — `dist/`, `build/`, `target/`, `out/`, `.next/`, `.nuxt/`
- **Package directories** — `node_modules/`, `vendor/`
- **IDE directories** — `.idea/`, `.vscode/`
- **Compiled artefacts** — `bin/`, `obj/` (common in .NET projects)
- **VCS directories** — `.git/`, `.hg/`, `.svn/`
- **Python caches** — `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.tox/`
- **Virtual environments** — `.venv/`, `venv/`, `env/` (including Pipewarden's own `.pipewarden-venv/`)
- **Gradle caches** — `.gradle/`
- **Files larger than 1 MB** — configurable via `secrets.max_file_bytes` in `.pipewarden.toml`
- **Files after the first 10,000** — configurable via `secrets.max_files`

The scanner uses git (`git ls-files`) where available, so files listed in `.gitignore` are automatically excluded even if they are not in the above list.

---

## What To Do When Secrets Are Found

When Pipewarden exits with code `4`, follow these steps immediately.

### Step 1 — Do NOT push

If the secret was found **before pushing**, the credential is still local. Do not push.

If you already pushed, assume the credential is **compromised** — bots scrape GitHub and npm within minutes of a credential appearing. Proceed immediately to Step 2.

### Step 2 — Rotate the credential NOW

Go to the service dashboard and revoke the exposed key:

| Rule ID | Where to rotate |
|---------|----------------|
| `aws.access_key` / `aws.secret_key` | AWS Console → IAM → Users → Security credentials → Deactivate + delete |
| `github.pat_classic` | GitHub → Settings → Developer settings → Personal access tokens → Delete |
| `openai.api_key` | OpenAI → platform.openai.com → API keys → Delete |
| `anthropic.api_key` | Anthropic → console.anthropic.com → API keys → Delete |
| `stripe.live_key` | Stripe Dashboard → Developers → API keys → Roll key |
| `mongodb.connection_string` | Change the database user password via your cloud provider |
| `postgres.connection_string` | `ALTER USER username WITH PASSWORD 'new-password';` |
| `azure.storage_connection_string` | Azure Portal → Storage Account → Access keys → Rotate |
| `azure.cosmos_connection_string` | Azure Portal → Cosmos DB → Keys → Regenerate |
| `slack.token` | Slack API → Your Apps → OAuth & Permissions → Revoke |
| `shopify.access_token` | Shopify Partners → Apps → Regenerate credentials |

### Step 3 — Remove the Secret From Your Code

Replace the hardcoded value with an environment variable:

```python
# Python — Before (dangerous)
db_password = "Secr3t!"

# Python — After (safe)
import os
db_password = os.environ["DB_PASSWORD"]
```

```csharp
// C# — Before (dangerous)
var connStr = "Server=db;Password=<YOUR-PASSWORD>";

// C# — After (safe)
var connStr = Environment.GetEnvironmentVariable("DB_CONNECTION_STRING");

// Or use appsettings.json + environment variable override (ASP.NET Core)
// Set ConnectionStrings__DefaultConnection as an env var — never hardcode it
```

Or use a secrets manager:

```python
# AWS Secrets Manager
import boto3, json
client = boto3.client("secretsmanager")
secret = json.loads(client.get_secret_value(SecretId="prod/db/password")["SecretString"])
db_password = secret["password"]
```

```csharp
// Azure Key Vault (ASP.NET Core)
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{vaultName}.vault.azure.net/"),
    new DefaultAzureCredential());
```

### Step 4 — Clean Git History

If the secret was ever committed (even if since deleted from the file), it is still in git history:

```bash
# Install git-filter-repo (safer than git filter-branch)
pip install git-filter-repo

# Option A — remove a specific file entirely
git filter-repo --path src/config.py --invert-paths

# Option B — scrub a specific string across all history
git filter-repo --replace-text <(echo 'ACTUAL_SECRET==>REMOVED')
```

> If the commit was pushed to GitHub, contact GitHub Support to purge cached versions after you've rewritten history.

### Step 5 — Add to Allowlist (if it was a false positive)

```toml
[secrets]
allowlist_paths   = ["tests/fixtures/**"]
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]
allowlist_rules   = ["jwt"]
```

### Step 6 — Verify the Fix

```bash
pipewarden --only secrets
# Should print: scanned N files, no secrets
# Exit code: 0
```

---

## Reading the Console Output

### The Four Status Icons

Every step in the summary shows one of four icons:

```
✓  passed   — The step ran and succeeded.

✗  failed   — The step ran and found a problem. Exit code becomes 1.
               Full output is printed below the summary.

⚠  warned   — Something non-critical happened.
               Usually an optional tool (mypy, hadolint) is not installed.
               Does NOT fail the pipeline.

·  skipped  — This stage does not apply to your project.
               No Dockerfile found → docker stage skipped.
```

### Understanding the Summary Table

```
  ✓ py:lint(ruff)        passed      0.3s
  ✗ py:test(pytest)      failed      6.2s    exit 1
  ⚠ py:typecheck(mypy)   warned      0.0s    mypy not installed in the project
  · docker               skipped     0.0s    disabled in config/flags
  │         │            │           │       │
  │         │            │           │       └─ Extra context message
  │         │            │           └─ How long the step took
  │         │            └─ Pass / Fail / Warn / Skip
  │         └─ Step name: stage:tool
  └─ Status icon
```

### When Something Fails

The tool prints the last 60 lines of output from every failing step:

```
Failing step output (tail):

── py:test(pytest) ──
FAILED tests/test_auth.py::test_login - AssertionError: Expected 200, got 401
FAILED tests/test_auth.py::test_logout - AssertionError: Expected 204, got 500
2 failed, 47 passed in 12.3s
```

### Stage Failed — What To Do Next

| Step | What failed | Immediate action |
|---|---|---|
| `secrets:fallback` or `secrets:gitleaks` | Credential found | **Exit code 4.** Rotate the credential immediately. |
| `py:deps` | Dependency install failed | Read the error tail — missing package, bad credentials, or network timeout |
| `py:lint(ruff)` | Python lint errors | Run `ruff check --fix .` to auto-fix, then `ruff check .` to see what remains |
| `py:typecheck(mypy)` | Type errors | Each line shows the file, line, and mismatch. Fix the type annotations. |
| `py:test(pytest)` | Test failures | Run `pytest -x` locally to stop at the first failure and debug interactively |
| `dotnet:format` | Code formatting violations | Run `dotnet format` locally to rewrite files. Commit the result. |
| `dotnet:build` | C# compilation error | The file, line, and error code are shown. Fix the type or namespace error. |
| `dotnet:test` | .NET test failures | The failing test and assertion mismatch are shown. Run `dotnet test --filter "TestName"` locally. |
| `dotnet:vulns` | Vulnerable NuGet package | Upgrade the affected package. Check release notes for breaking changes. |
| `node:lint` | ESLint / prettier errors | Run `npm run lint -- --fix` to auto-fix |
| `node:test` | JavaScript test failures | Run `npm test` locally to see full output |
| `docker:lint(hadolint)` | Dockerfile violation | The rule ID and fix are printed. See hadolint.github.io for details. |
| `docker:build` | Docker build error | Full `docker build` output is printed. Usually a missing file or failed `RUN` command. |
| `docker:scan(trivy)` | Container image CVE | Upgrade the base image or the affected OS package. |
| `go:vet` | Go vet warnings | Fix the issue — `go vet` catches real bugs (unreachable code, format string mismatches). |
| `rust:lint` (clippy) | Clippy warnings | Run `cargo clippy --fix` to auto-fix. Remaining lints show the fix suggestion inline. |
| `vulns:pip-audit` | Python CVE | Upgrade the package shown. Run `pip install "package>=safe_version"`. |

---

## Output Files — SARIF, JUnit XML, JSON, Markdown

Pipewarden can generate four machine-readable report files simultaneously. These integrate with the dashboards and UIs your team already uses.

### Generating Output Files

All four formats can be generated in a single run:

```bash
pipewarden \
  --json \
  --sarif-out  results.sarif \
  --junit-out  results.xml \
  --markdown-out summary.md \
  --gh-annotations
```

In practice, for most CI pipelines:

```bash
# GitHub Actions (most common)
pipewarden --sarif-out report.sarif --junit-out junit.xml --markdown-out "$GITHUB_STEP_SUMMARY"

# GitLab CI
pipewarden --junit-out junit.xml --sarif-out report.sarif

# Azure DevOps
pipewarden --junit-out junit.xml

# Jenkins
pipewarden --junit-out junit.xml --sarif-out report.sarif

# Scripting / custom integrations
pipewarden --json > pipewarden-report.json
```

---

## How to Read Each Output File

### The JSON Report

**Generate:**
```bash
pipewarden --json > report.json
```

**Full annotated output:**
```json
{
  "root": "/home/alice/my-app",
  ← The directory that was scanned

  "tool_version": "1.3.1",
  ← Pipewarden version — useful for debugging version-specific behaviour

  "started_at": 1715860981.123,
  ← Unix timestamp (seconds since epoch) for when the run started.
     Convert to a readable date with: datetime.fromtimestamp(1715860981.123)
     Type is float, not a string — never an ISO date string.

  "config_path": ".pipewarden.toml",
  ← Path to the config file that was loaded.
     null (JSON null) when no .pipewarden.toml was found and defaults are used.

  "detected": ["python", "node(npm)", "docker(Dockerfile)"],
  ← Which languages/tools were auto-detected

  "duration_s": 61.4,
  ← Total wall-clock time in seconds

  "summary": {
    "total": 10,       ← Total steps that were attempted
    "passed": 10,      ← Steps that returned exit code 0
    "failed": 0,       ← Steps that returned non-zero exit code
    "warned": 0,       ← Steps that completed with a warning (tool missing, etc.)
    "skipped": 0,      ← Steps skipped because they did not apply
    "findings": 0      ← Total secrets/CVEs found across all steps
  },

  "steps": [
    {
      "name": "secrets:fallback",
      ← Step identifier in format stage:tool

      "status": "passed",
      ← "passed" | "failed" | "warned" | "skipped"

      "duration_s": 0.1,
      ← Wall-clock time for this step only

      "returncode": 0,
      ← Exit code of the underlying tool (0 = success)

      "message": "scanned 34 files, no secrets",
      ← Human-readable context message (empty string if none)

      "stdout_tail": "",
      ← Last 60 lines of stdout from the subprocess (empty if passed)

      "findings": []
      ← List of Finding objects (non-empty only for secrets and vulns steps)
    },
    {
      "name": "py:test(pytest)",
      "status": "failed",
      "duration_s": 6.4,
      "returncode": 1,
      "message": "",
      "stdout_tail": "FAILED tests/test_auth.py::test_login\n2 failed, 47 passed in 6.2s",
      "findings": []
    }
  ]
}
```

**How to use the JSON report in a script:**

```bash
# Check the overall result
result=$(pipewarden --json 2>/dev/null)
status=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['summary']['failed'])")
if [ "$status" -gt 0 ]; then
  echo "Pipeline failed: $status step(s) failed"
fi
```

```python
# Python script to process the report
import json, subprocess

result = subprocess.run(
    ["pipewarden", "--json"],
    capture_output=True, text=True
)
report = json.loads(result.stdout)

print(f"Detected: {', '.join(report['detected'])}")
print(f"Duration: {report['duration_s']:.1f}s")
print(f"Passed: {report['summary']['passed']}/{report['summary']['total']}")

for step in report["steps"]:
    if step["status"] == "failed":
        print(f"\nFailed step: {step['name']}")
        print(step["stdout_tail"])
```

```csharp
// C# script to process the report
using System.Diagnostics;
using System.Text.Json;

var process = Process.Start(new ProcessStartInfo("pipewarden", "--json") {
    RedirectStandardOutput = true
})!;
await process.WaitForExitAsync();

var json = await process.StandardOutput.ReadToEndAsync();
var report = JsonDocument.Parse(json).RootElement;

Console.WriteLine($"Detected: {report.GetProperty("detected")}");
Console.WriteLine($"Passed: {report.GetProperty("summary").GetProperty("passed")}/{report.GetProperty("summary").GetProperty("total")}");

foreach (var step in report.GetProperty("steps").EnumerateArray())
{
    if (step.GetProperty("status").GetString() == "failed")
    {
        Console.WriteLine($"\nFailed step: {step.GetProperty("name")}");
        Console.WriteLine(step.GetProperty("stdout_tail"));
    }
}
```

---

### The SARIF Report

**Generate:**
```bash
pipewarden --sarif-out results.sarif
```

**What is SARIF?**
SARIF (Static Analysis Results Interchange Format) is the industry standard for security and code analysis findings. GitHub Code Scanning, Azure DevOps, and many SAST platforms can read it natively.

**Annotated SARIF structure:**
```json
{
  "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "pipewarden",
          "version": "1.3.1",
          ← Tool name and version for provenance tracking

          "rules": [
            {
              "id": "aws.access_key",
              ← Rule ID used in allowlist_rules config

              "name": "aws.access_key",
              "shortDescription": { "text": "possible aws.access_key" },
              "defaultConfiguration": { "level": "error" }
              ← "error" = CRITICAL/HIGH, "warning" = MEDIUM, "note" = LOW
            }
          ]
        }
      },

      "results": [
        {
          "ruleId": "aws.access_key",
          ← Links back to the rules array above

          "level": "error",
          ← "error" | "warning" | "note"

          "message": { "text": "possible aws.access_key" },

          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": { "uri": "src/config.py" },
                "region": { "startLine": 14, "startColumn": 7 }
                ← Exact location for inline diff annotation
              }
            }
          ],

          "fingerprints": {
            "primaryLocationLineHash/v1": "a3f8d2..."
            ← SHA-256 fingerprint for deduplication — GitHub uses this to avoid
               re-alerting on the same finding across commits
          }
        }
      ]
    }
  ]
}
```

**How to use SARIF in GitHub Actions:**

```yaml
- name: Run Pipewarden
  run: pipewarden --sarif-out report.sarif
  continue-on-error: true    # upload report even if Pipewarden failed

- name: Upload to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: report.sarif
```

After upload, findings appear under **Security → Code scanning alerts** in your repository:
```
⚠ aws.access_key — possible aws.access_key
  src/config.py, line 14
  Severity: Critical
  [Dismiss]  [Create issue]  [Assign to reviewer]
```

Each alert can be dismissed with a reason, assigned to a team member, or linked to a tracking issue — exactly like a commercial SAST tool, for free.

**How to use SARIF in Azure DevOps:**

```yaml
- script: pipewarden --sarif-out $(Build.ArtifactStagingDirectory)/results.sarif
  displayName: Run Pipewarden

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: $(Build.ArtifactStagingDirectory)/results.sarif
    artifactName: sarif-results
```

---

### The JUnit XML Report

**Generate:**
```bash
pipewarden --junit-out results.xml
```

**What is JUnit XML?**
Every major CI system (GitHub Actions, GitLab, Jenkins, CircleCI, Azure DevOps, TeamCity, Bitbucket) can parse JUnit XML and display structured test results.

**Annotated JUnit XML structure:**

> Pipewarden produces **one `<testsuites>` root containing one `<testsuite>`**. Every pipeline step is a `<testcase>` inside that single suite — steps are not split by language. The `classname` attribute is always `"pipewarden"`.

```xml
<testsuites name="pipewarden" tests="6" failures="1" skipped="1" time="44.800">
<!-- ↑ Root element. "tests" = total step count, "failures" = failed steps,
       "skipped" = skipped steps. No "errors" attribute. -->

  <testsuite name="pipewarden" tests="6" failures="1" skipped="1" time="44.800">
  <!-- ↑ Always exactly one <testsuite> child. Same counts as the root. -->

    <testcase classname="pipewarden" name="secrets:fallback" time="0.100"/>
    <!-- ↑ PASSED step: no child elements. classname is always "pipewarden". -->

    <testcase classname="pipewarden" name="dotnet:restore" time="12.400"/>

    <testcase classname="pipewarden" name="dotnet:format" time="1.200"/>

    <testcase classname="pipewarden" name="dotnet:build" time="18.700"/>

    <testcase classname="pipewarden" name="dotnet:test" time="8.100">
      <failure message="step failed" type="PipewarnedFailure">
        FAILED MyApp.Tests.UserControllerTests.GetUser_Returns404_WhenNotFound
        Expected: 404  Actual: 200
        Failed! - Failed: 1, Passed: 47
        <!-- ↑ FAILED step: <failure> child with the stdout tail as text content.
               type is always "PipewarnedFailure". message is the step's message field. -->
      </failure>
    </testcase>

    <testcase classname="pipewarden" name="dotnet:vulns" time="0.000">
      <skipped message="disabled in config/flags"/>
      <!-- ↑ SKIPPED step: <skipped> child with the reason as the message attribute. -->
    </testcase>

    <!-- WARNED steps get a <system-out> element (JUnit has no "warned" type): -->
    <!-- <testcase classname="pipewarden" name="py:lint" time="0.000">       -->
    <!--   <system-out>WARNED: ruff not installed&#10;</system-out>           -->
    <!-- </testcase>                                                           -->

  </testsuite>
</testsuites>
```
</testsuites>
```

**How to read JUnit XML in different CI systems:**

**GitHub Actions:**
```yaml
- run: pipewarden --junit-out junit.xml

- name: Publish test results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: junit.xml
```

**GitLab CI:**
```yaml
pipewarden:
  script:
    - pipewarden --junit-out junit.xml
  artifacts:
    reports:
      junit: junit.xml    ← GitLab auto-displays this in the MR sidebar
```

**Jenkins:**
```groovy
post {
    always {
        junit 'junit.xml'    // Renders in Jenkins test results view
    }
}
```

**Azure DevOps:**
```yaml
- task: PublishTestResults@2
  condition: always()
  inputs:
    testResultsFormat: JUnit
    testResultsFiles: junit.xml
    testRunTitle: Pipewarden
```

**CircleCI:**
```yaml
- store_test_results:
    path: test-results    # directory containing junit.xml
```

---

### The Markdown Report

**Generate:**
```bash
pipewarden --markdown-out summary.md
```

**Write directly to GitHub Actions step summary:**
```yaml
- run: pipewarden --markdown-out "$GITHUB_STEP_SUMMARY"
```

When written to `$GITHUB_STEP_SUMMARY`, it appears as a formatted panel on the workflow run page:

```
## Pipewarden 1.3.1

| Step | Status | Duration | Message |
|---|---|---|---|
| secrets:fallback | ✓ passed | 0.1s | scanned 34 files, no secrets |
| py:venv | ✓ passed | 2.9s | |
| py:deps(pyproject) | ✓ passed | 4.1s | |
| py:lint(ruff) | ✓ passed | 0.3s | |
| py:test(pytest) | ✗ failed | 8.1s | exit 1 |

### Findings

| Severity | File | Line | Rule | Snippet |
|---|---|---|---|---|
| CRITICAL | src/config.py | 14 | aws.access_key | AKIA…WXYZ |
```

---

### GitHub Actions Inline Annotations

**Generate:**
```bash
pipewarden --gh-annotations
```

Prints GitHub Actions workflow commands to stdout. The runner picks them up and shows findings as **inline comments directly on the PR diff**:

```
::error file=src/config.py,line=14,col=7,title=aws.access_key::possible aws.access_key
```

In a workflow:
```yaml
- run: pipewarden --gh-annotations --sarif-out report.sarif
```

Findings appear inline on the changed lines in the PR review view — no extra upload step needed.

---

## How to Act on Findings

### After a Clean Run (exit 0)

```console
✓ all 10 steps passed in 61.4s
```

Nothing to do. Safe to merge or deploy.

### After a Secrets Finding (exit 4)

1. **Do not push if you have not yet.** If you have, assume compromised.
2. **Rotate the credential** — see the table in the [Secrets section](#what-to-do-when-secrets-are-found)
3. **Replace the hardcoded value** with an environment variable or secrets manager
4. **Clean git history** if the secret was committed
5. **Verify:** `pipewarden --only secrets` should return exit 0

### After a Test Failure (exit 1)

```console
✗ py:test(pytest) failed 8.1s exit 1
```

Read the output tail printed below the summary. It shows exactly which tests failed and why.

```bash
# Run just the failing test locally
pytest -x tests/test_auth.py::test_login -v

# Run the full Python pipeline with verbose output
pipewarden --only python --verbose
```

### After a Lint Failure (exit 1)

```console
✗ py:lint(ruff) failed 0.4s exit 1
```

Auto-fix what can be fixed:
```bash
ruff check --fix .
ruff format .
```

Then check what remains:
```bash
ruff check .
```

For .NET:
```bash
dotnet format    # rewrites files in place
```

### After a Vulnerability Finding (exit 1)

```console
✗ vulns:pip-audit failed 4.2s
── vulns:pip-audit ──
cryptography 41.0.0
  ID:       GHSA-jfh8-c2jp-5v3q
  Severity: HIGH
  Fix:      upgrade to 41.0.4 or later
```

1. Note the package name and the recommended fix version
2. Upgrade: `pip install "cryptography>=41.0.4"` and update your lockfile
3. For .NET: `dotnet add package PackageName --version SafeVersion`
4. Re-run: `pipewarden --only vulns` to confirm the finding is gone
5. If upgrading breaks your code, check if the CVE affects your code paths — some vulnerabilities are in features you don't use

### After a Build Failure (exit 1)

```console
✗ dotnet:build failed 14.2s
── dotnet:build ──
error CS0246: The type or namespace name 'UserService' could not be found
```

Read the error — it includes the file, line number, and error code. Fix the compilation error and re-run:

```bash
pipewarden --only dotnet --fail-fast
```

---

## Configuration Reference

Drop a `.pipewarden.toml` file at the root of your repository to customise behaviour. **All keys are optional** — the defaults work out of the box.

> **Config filename:** Both `.pipewarden.toml` (with leading dot) and `pipewarden.toml` (without) are accepted. The dot-prefixed name is checked first.

Generate a starter config:
```bash
pipewarden --init
```

Validate your config:
```bash
pipewarden --validate
# exit 0 = valid, exit 3 = error with message
```

**Full reference:**

```toml
# .pipewarden.toml
# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL SETTINGS
# ─────────────────────────────────────────────────────────────────────────────

# Stop on the first failure instead of collecting all failures.
fail_fast = false

# Docker image tag used when building.
docker_tag = "pipewarden-local:latest"

# Run ONLY these stages (all others skipped).
only = []

# Always skip these stages.
skip = []


# ─────────────────────────────────────────────────────────────────────────────
# STAGE TOGGLES
# ─────────────────────────────────────────────────────────────────────────────
[stages]
python   = true
node     = true
dotnet   = true
go       = true
rust     = true
docker   = true    # set to false if no Docker daemon in CI
vulns    = true    # dependency CVE scanning (optional external tools)
outdated = false   # non-blocking outdated package check


# ─────────────────────────────────────────────────────────────────────────────
# TIMEOUTS — increase for slow tests or large dependency trees
# ─────────────────────────────────────────────────────────────────────────────
[timeouts]
install_s = 900    # 15 min — dependency installation
build_s   = 900    # 15 min — build step
test_s    = 1800   # 30 min — test suite
scan_s    = 600    # 10 min — secret / vuln scan
default_s = 600    # 10 min — everything else


# ─────────────────────────────────────────────────────────────────────────────
# SECRET SCANNING
# ─────────────────────────────────────────────────────────────────────────────
[secrets]
enabled         = true    # set to false to skip secret scanning entirely
prefer_external = true    # use gitleaks if installed (recommended)
max_file_bytes  = 1000000 # skip files larger than 1 MB
max_files       = 10000   # stop after scanning this many files
scan_history    = false   # full git history scan (gitleaks only, for audits)

allowlist_paths = [
    # "tests/fixtures/**",
    # "docs/examples/**",
]

allowlist_rules = [
    # "jwt",
]

allowlist_strings = [
    # "AKIAIOSFODNN7EXAMPLE",
]


# ─────────────────────────────────────────────────────────────────────────────
# .NET PIPELINE CONTROL
# ─────────────────────────────────────────────────────────────────────────────
[dotnet]
format   = true    # dotnet format --verify-no-changes
vulns    = true    # dotnet list package --vulnerable --include-transitive
outdated = false   # dotnet list package --outdated (non-blocking)


# ─────────────────────────────────────────────────────────────────────────────
# RETRY — for flaky network-dependent steps
# Applies to: pip install, npm ci, cargo fetch, go mod download, pip-audit…
# ─────────────────────────────────────────────────────────────────────────────
[retry]
attempts     = 0    # 0 = disabled; max 5
backoff_base = 2.0  # seconds before first retry; doubles each attempt (2s, 4s, 8s…)


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
[output]
color = true    # set to false for dumb terminals
quiet = false   # suppress pretty output (use with --json)
```

### Config Validation

The config file is **strictly validated** — typos fail loudly rather than being silently ignored:

```bash
pipewarden --validate
# → config error: unknown key: pipewarden.stagess
```

---

## Environment Variable Overrides

Override any configuration value with a `PIPEWARDEN_*` environment variable. Useful in CI systems where you cannot edit the TOML file.

**Priority order (highest wins):** CLI flags → env vars → `.pipewarden.toml` (or `pipewarden.toml`) → built-in defaults.

| Environment Variable | Equivalent Config | Example Value |
|---------------------|-------------------|---------------|
| `PIPEWARDEN_FAIL_FAST` | `fail_fast = true` | `1` or `true` |
| `PIPEWARDEN_SKIP` | `skip = [...]` | `docker,vulns` |
| `PIPEWARDEN_ONLY` | `only = [...]` | `secrets,python` |
| `PIPEWARDEN_TIMEOUT_INSTALL_S` | `timeouts.install_s` | `1800` |
| `PIPEWARDEN_TIMEOUT_BUILD_S` | `timeouts.build_s` | `1200` |
| `PIPEWARDEN_TIMEOUT_TEST_S` | `timeouts.test_s` | `3600` |
| `PIPEWARDEN_TIMEOUT_SCAN_S` | `timeouts.scan_s` | `300` |
| `PIPEWARDEN_TIMEOUT_DEFAULT_S` | `timeouts.default_s` | `300` |
| `PIPEWARDEN_NO_COLOR` | `output.color = false` | `1` or `true` |
| `PIPEWARDEN_QUIET` | `output.quiet = true` | `1` or `true` |
| `PIPEWARDEN_RETRY_ATTEMPTS` | `retry.attempts` | `3` |
| `PIPEWARDEN_RETRY_BACKOFF` | `retry.backoff_base` | `5.0` |

**Example — GitHub Actions with env var overrides:**
```yaml
- name: Run Pipewarden
  env:
    PIPEWARDEN_SKIP: docker          # no Docker daemon on this runner
    PIPEWARDEN_RETRY_ATTEMPTS: "3"   # retry flaky network steps
    PIPEWARDEN_TIMEOUT_TEST_S: "3600"
  run: pipewarden --sarif-out report.sarif --junit-out junit.xml
```

---

## Using Pipewarden Locally

No CI/CD required. Pipewarden runs entirely on your machine — install it once and use it like any other developer tool. This section covers both the general workflow and a detailed step-by-step guide for scanning a .NET solution locally.

### Everyday Developer Workflow

```bash
# First run in a new project — detects languages, creates venv, installs deps
pipewarden

# Re-run after code changes (venv reused — much faster)
pipewarden

# Quick check while writing code — just lint and test, skip everything else
pipewarden --only python

# Pre-commit secrets check (sub-second)
pipewarden --only secrets

# Pre-push full check
pipewarden --only secrets --only python

# Stop at the first failure to debug quickly
pipewarden --only python --fail-fast

# Preview what would run without executing anything
pipewarden --dry-run

# See what languages were detected
pipewarden --list-stages

# Scaffold a config file
pipewarden --init
```

---

### Scanning a .NET Solution Locally (No CI/CD Needed)

If you want to scan your .NET solution on your own machine without touching CI/CD at all, follow this guide. You need two things installed: **Python 3.10+** and the **.NET SDK**. That is it.

---

#### Step 1 — Install Python (one-time, if not already installed)

Pipewarden is a Python tool. It does not touch your .NET project's own dependencies — Python is only needed to run Pipewarden itself.

**Windows:**
```powershell
# Option A — download installer from python.org (recommended)
# https://www.python.org/downloads/

# Option B — winget
winget install Python.Python.3.12

# Verify
python --version
# → Python 3.12.x
```

**macOS:**
```bash
brew install python@3.12

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip
python3 --version
```

---

#### Step 2 — Install Pipewarden (one-time)

```powershell
# Windows (PowerShell)
pip install pipewarden

# macOS / Linux
pip3 install pipewarden
```

Verify:
```bash
pipewarden --version
# → pipewarden 1.3.1
```

> You only ever do Steps 1 and 2 once. After that, `pipewarden` is always available.

---

#### Step 3 — Open a terminal at your solution root

Navigate to the folder that contains your `.sln` file (or the root `.csproj` if you have no solution file).

```powershell
# Windows (PowerShell)
cd C:\Projects\MyApp

# macOS / Linux
cd ~/projects/MyApp
```

Confirm Pipewarden can see your solution:
```bash
pipewarden --list-stages
```

You should see output like:
```
detected:  dotnet(MyApp.sln)
enabled:   secrets, dotnet
```

If `dotnet` is not listed, make sure you are in the folder that contains `MyApp.sln` or `MyApp.csproj`.

---

#### Step 4 — Run the scan

**Full scan (recommended for first use):**
```bash
pipewarden
```

This runs in order:
1. Scans all files for leaked credentials (API keys, connection strings, tokens)
2. Runs `dotnet restore`
3. Runs `dotnet format --verify-no-changes` (code style check)
4. Runs `dotnet build`
5. Runs `dotnet test`
6. Runs `dotnet list package --vulnerable` (NuGet CVE check)

**Scan only .NET — skip secret scanning and anything else:**
```bash
pipewarden --only dotnet
```

**Scan secrets + .NET only (skip Docker, Node, etc. if detected):**
```bash
pipewarden --only secrets --only dotnet
```

**Stop at the first failure (useful when debugging a broken build):**
```bash
pipewarden --only dotnet --fail-fast
```

**Skip a specific step you do not want (e.g. Docker if you have no daemon running):**
```bash
pipewarden --skip docker
```

**Skip both Docker and vulnerability scanning:**
```bash
pipewarden --skip docker --skip vulns
```

**Preview what would run without actually running anything:**
```bash
pipewarden --dry-run
```

Sample `--dry-run` output:
```
would run:
  secrets:fallback
  dotnet:restore
  dotnet:format
  dotnet:build
  dotnet:test
  dotnet:vulns
```

---

#### Step 5 — Read the console output

After the scan finishes, you see a summary table:

```
════════════════════════════════════════════════════════════════
  Summary
════════════════════════════════════════════════════════════════
  ✓ secrets:fallback    passed    0.1s   scanned 22 files, no secrets
  ✓ dotnet:restore      passed   12.4s
  ✓ dotnet:format       passed    1.2s
  ✓ dotnet:build        passed   18.7s
  ✓ dotnet:test         passed    8.3s   48 tests across 2 projects
  ✓ dotnet:vulns        passed    4.1s   no vulnerable packages

  ✓ all 6 steps passed in 44.8s
```

| Icon | Meaning | What to do |
|------|---------|-----------|
| `✓` | Passed — nothing to do | Continue working |
| `✗` | Failed — something broke | Read the output tail printed below the summary |
| `⚠` | Warned — optional tool missing | Install the tool if you want it; pipeline still passes |
| `·` | Skipped — not applicable | Nothing — the step was intentionally skipped |

**When a step fails**, the last 60 lines of output from that step are printed immediately below the summary. For example:

```
Failing step output (tail):

── dotnet:test ──
  Failed MyApp.Tests.UserControllerTests.GetUser_Returns404_WhenNotFound [12ms]
  Error Message:
    Assert.Equal() Failure
    Expected: 404
    Actual:   200

Failed!  - Failed: 1, Passed: 47, Skipped: 0, Total: 48
```

You see exactly which test failed and why — no log archaeology needed.

---

#### Step 6 — Save a local report (optional)

If you want to keep a record of the scan result, generate a report file:

**JSON report (full machine-readable detail):**
```bash
pipewarden --json > scan-report.json
```

This writes the complete report to `scan-report.json` in the current directory. Open it in any text editor or JSON viewer. Every field is explained in the [How to Read Each Output File](#-how-to-read-each-output-file) section.

**Markdown report (readable in any browser or editor):**
```bash
pipewarden --markdown-out scan-report.md
```

Open `scan-report.md` in VS Code, GitHub Desktop preview, or any Markdown viewer to see a formatted table of every step's status, duration, and findings.

**JUnit XML (if you want to open results in Visual Studio or Rider):**
```bash
pipewarden --junit-out results.xml
```

Visual Studio and JetBrains Rider can display JUnit XML as a test results view. In Rider: **Run → Import Tests from File → results.xml**.

**All formats at once:**
```bash
pipewarden --json > scan-report.json
pipewarden --sarif-out results.sarif --junit-out results.xml --markdown-out results.md
```

> Note: `--json` suppresses the pretty console output. Run it separately if you want both.

---

#### Step 7 — Re-run after fixing issues

After you fix a failing step, re-run only that stage to confirm the fix quickly:

```bash
# Fix a test failure — re-run only tests
pipewarden --only dotnet

# Fix a secret finding — re-run only secrets
pipewarden --only secrets

# Fix a lint issue — re-run the full .NET pipeline
pipewarden --only dotnet
```

---

#### All Local .NET Commands at a Glance

```bash
# ── First-time setup ──────────────────────────────────────────────────────────
pip install pipewarden                          # install Pipewarden (once)
pipewarden --version                            # verify: pipewarden 1.3.1
pipewarden --init                               # scaffold a .pipewarden.toml (optional)

# ── Detect what Pipewarden sees ───────────────────────────────────────────────
pipewarden --list-stages                        # shows: detected dotnet(MyApp.sln)
pipewarden --dry-run                            # shows steps that WOULD run

# ── Run the scan ─────────────────────────────────────────────────────────────
pipewarden                                      # full scan: secrets + dotnet (+ docker if Dockerfile present)
pipewarden --only dotnet                        # .NET pipeline only, no secrets scan
pipewarden --only secrets --only dotnet         # secrets + .NET, nothing else
pipewarden --skip docker                        # skip Docker (no daemon needed)
pipewarden --skip docker --skip vulns           # skip Docker and CVE scanning
pipewarden --only dotnet --fail-fast            # stop at the first failure

# ── Scan a specific directory (monorepo) ─────────────────────────────────────
pipewarden --root .\services\payment-service    # Windows
pipewarden --root ./services/payment-service    # macOS/Linux

# ── Save a report locally ─────────────────────────────────────────────────────
pipewarden --json > scan-report.json            # full JSON detail
pipewarden --markdown-out scan-report.md        # Markdown table (open in any viewer)
pipewarden --junit-out results.xml              # JUnit XML (Rider / VS test import)

# ── Debug a problem ───────────────────────────────────────────────────────────
pipewarden --verbose                            # print every subprocess call
pipewarden --log-file debug.log                 # write debug log to file
pipewarden --only secrets                       # re-check secrets after fixing

# ── Use a custom config ───────────────────────────────────────────────────────
pipewarden --config .\custom.pipewarden.toml    # Windows
pipewarden --config ./custom.pipewarden.toml    # macOS/Linux
pipewarden --validate                           # check config file is valid
```

---

#### Recommended `.pipewarden.toml` for Local .NET Use

If you are scanning locally and do not have Docker running, use this config to avoid the Docker stage blocking your scan:

```toml
# .pipewarden.toml — place this next to your .sln file

[stages]
dotnet = true
docker = false    # no Docker daemon needed locally
node   = false    # skip Node (not a Node project)
python = false    # skip Python (not a Python project)
vulns  = true     # check NuGet packages for CVEs

[dotnet]
format   = true   # check code formatting (dotnet format --verify-no-changes)
vulns    = true   # run dotnet list package --vulnerable
outdated = false  # set to true to see which packages have newer versions

[secrets]
allowlist_paths = [
    "tests/TestData/**",    # test fixtures with fake credentials
    "docs/**",              # documentation examples
]

[timeouts]
install_s = 600     # 10 min for dotnet restore
build_s   = 600     # 10 min for dotnet build
test_s    = 1800    # 30 min for dotnet test
```

After saving this file, just run:
```bash
pipewarden
```

---

#### Common Local Scenarios

**"I just want to check if my code compiles and tests pass — nothing else."**
```bash
pipewarden --only dotnet --skip docker
```

**"I made a change. Is my connection string leaking?"**
```bash
pipewarden --only secrets
```

**"I want to check for known CVEs in my NuGet packages."**
```bash
pipewarden --only dotnet
# (vulns is enabled by default — dotnet list package --vulnerable runs automatically)
```

**"I only want to check one service in my monorepo."**
```bash
pipewarden --root .\src\PaymentService    # Windows
pipewarden --root ./src/PaymentService   # macOS/Linux
```

**"I want to see everything Pipewarden is doing under the hood."**
```bash
pipewarden --verbose
```

**"The scan failed. I fixed the issue. How do I just re-run the failing step quickly?"**
```bash
# If dotnet:test failed:
pipewarden --only dotnet --fail-fast

# If secrets:fallback failed:
pipewarden --only secrets
```

**"I want a formatted report I can share with my team without setting up CI."**
```bash
pipewarden --markdown-out scan-$(date +%Y%m%d).md
# → creates scan-20260517.md — send it in Slack/Teams/email
```

Windows PowerShell equivalent:
```powershell
pipewarden --markdown-out "scan-$(Get-Date -Format 'yyyyMMdd').md"
```

---

### Resetting the Environment

If you change `requirements.txt` or `pyproject.toml` and Pipewarden's venv has stale deps:

```bash
# macOS / Linux
rm -rf .pipewarden-venv

# Windows (PowerShell)
Remove-Item -Recurse -Force .pipewarden-venv

pipewarden    # recreates from scratch
```

### Running Against a Subdirectory

```bash
# Monorepo — run against a specific service
pipewarden --root ./services/auth-service
pipewarden --root ./services/payment-service
```

### Using a Custom Config File

```bash
# Use a non-default config location
pipewarden --config /path/to/custom.pipewarden.toml
```

### Verbose Debug Output

```bash
# Print every subprocess call and its output to stderr
pipewarden --verbose

# Write a debug log to a file
pipewarden --log-file pipewarden.log
```

---

## CI / CD Integration

### GitHub Actions (Inline)

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  security-events: write    # required to upload SARIF to the Security tab

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Pipewarden
        run: pip install pipewarden

      - name: Run Pipewarden
        run: |
          pipewarden \
            --sarif-out report.sarif \
            --junit-out junit.xml \
            --markdown-out "$GITHUB_STEP_SUMMARY" \
            --gh-annotations

      - name: Upload security findings
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: report.sarif

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: pipewarden-results
          path: |
            junit.xml
            report.sarif
```

**GitHub Actions — .NET project with NuGet cache:**
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  security-events: write

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: "9.0.x"

      - uses: actions/cache@v4
        with:
          path: ~/.nuget/packages
          key: ${{ runner.os }}-nuget-${{ hashFiles('**/*.csproj') }}
          restore-keys: ${{ runner.os }}-nuget-

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install pipewarden

      - run: pipewarden --sarif-out report.sarif --junit-out junit.xml

      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: report.sarif
```

**GitHub Actions — alert on credential leak only:**
```yaml
- name: Run Pipewarden
  id: pipewarden
  run: pipewarden --sarif-out report.sarif
  continue-on-error: true

- name: Alert on credential leak
  if: steps.pipewarden.outcome == 'failure'
  run: |
    EXIT_CODE=${{ steps.pipewarden.outputs.exit-code }}
    if [ "$EXIT_CODE" -eq 4 ]; then
      echo "::error::CREDENTIAL LEAK DETECTED — rotate immediately"
    fi
```

---

### GitLab CI

```yaml
# .gitlab-ci.yml
pipewarden:
  image: python:3.12-slim
  before_script:
    - pip install pipewarden
  script:
    - pipewarden --junit-out junit.xml --sarif-out report.sarif
  artifacts:
    when: always
    reports:
      junit: junit.xml              # GitLab shows this in MR sidebar automatically
    paths:
      - report.sarif
    expire_in: 30 days
```

**GitLab CI — .NET project:**
```yaml
pipewarden-dotnet:
  image: mcr.microsoft.com/dotnet/sdk:9.0
  before_script:
    - apt-get update -qq && apt-get install -y python3 python3-pip
    - pip3 install pipewarden
  script:
    - pipewarden --only secrets --only dotnet --junit-out junit.xml
  artifacts:
    when: always
    reports:
      junit: junit.xml
```

---

### Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent { docker { image 'python:3.12' } }

    stages {
        stage('Quality Gate') {
            steps {
                sh 'pip install pipewarden'
                sh 'pipewarden --junit-out junit.xml --sarif-out report.sarif'
            }
            post {
                always {
                    junit 'junit.xml'
                    archiveArtifacts artifacts: 'report.sarif', fingerprint: true
                }
            }
        }
    }
}
```

**Jenkins — .NET project:**
```groovy
pipeline {
    agent { docker { image 'mcr.microsoft.com/dotnet/sdk:9.0' } }

    stages {
        stage('Quality Gate') {
            steps {
                sh 'apt-get update -qq && apt-get install -y python3 python3-pip'
                sh 'pip3 install pipewarden'
                sh 'pipewarden --only secrets --only dotnet --junit-out junit.xml'
            }
            post {
                always {
                    junit 'junit.xml'
                }
            }
        }
    }
}
```

---

### Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.12'

  - script: pip install pipewarden
    displayName: Install Pipewarden

  - script: pipewarden --junit-out $(Build.ArtifactStagingDirectory)/junit.xml
    displayName: Run Pipewarden

  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: JUnit
      testResultsFiles: $(Build.ArtifactStagingDirectory)/junit.xml
      testRunTitle: Pipewarden
```

**Azure DevOps — .NET project with private NuGet feed:**
```yaml
trigger:
  - main

pool:
  vmImage: ubuntu-latest

variables:
  - group: nuget-credentials    # variable group containing NUGET_TOKEN

steps:
  - task: UseDotNet@2
    inputs:
      version: '9.0.x'

  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.12'

  - script: pip install pipewarden
    displayName: Install Pipewarden

  - script: pipewarden --junit-out $(Build.ArtifactStagingDirectory)/junit.xml
    displayName: Run Pipewarden
    env:
      NUGET_USERNAME: $(Build.RequestedFor)
      NUGET_TOKEN: $(System.AccessToken)

  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: JUnit
      testResultsFiles: $(Build.ArtifactStagingDirectory)/junit.xml
```

---

### CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  quality-gate:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install Pipewarden
          command: pip install pipewarden
      - run:
          name: Run Pipewarden
          command: pipewarden --junit-out test-results/junit.xml
      - store_test_results:
          path: test-results

workflows:
  ci:
    jobs:
      - quality-gate
```

---

### Bitbucket Pipelines

```yaml
# bitbucket-pipelines.yml
image: python:3.12

pipelines:
  default:
    - step:
        name: Quality Gate
        script:
          - pip install pipewarden
          - pipewarden --junit-out test-reports/junit.xml
        after-script:
          - pipe: atlassian/junit-reporter:0.2.0
            variables:
              REPORT_PATHS: test-reports/junit.xml
```

---

### TeamCity

Add a Build Step of type **Command Line**:

```bash
pip install pipewarden
pipewarden --junit-out %teamcity.build.checkoutDir%/junit.xml
```

Then add a **XML report processing** Build Feature pointing to `junit.xml`.

---

## GitHub Actions (Official Action)

If your workflow already uses GitHub Actions, use the dedicated composite action:

```yaml
- name: Run Pipewarden
  uses: gcfernando/pipewarden@v1
  with:
    sarif-out: report.sarif
    junit-out: junit.xml
```

### Action Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `root` | `.` | Project root directory to scan |
| `only` | *(all)* | Comma-separated stages to run, e.g. `secrets,python` |
| `skip` | *(none)* | Comma-separated stages to skip, e.g. `docker,vulns` |
| `fail-fast` | `false` | Stop on first failure |
| `sarif-out` | *(none)* | Path to write SARIF report |
| `junit-out` | *(none)* | Path to write JUnit XML report |
| `diff` | *(none)* | Restrict secret scan to files changed vs this ref |
| `python-version` | `3.12` | Python version to use for the tool itself |
| `version` | *(latest)* | Specific pipewarden version to install |

---

## Pre-Commit Hooks

Catch issues **before** code reaches the remote repository.

### Setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gcfernando/pipewarden
    rev: v1.3.1
    hooks:
      - id: pipewarden-secrets     # Runs on every git commit
      - id: pipewarden-diff        # Runs on every git push (changed files only)
      # - id: pipewarden-full      # Full run (manual: pre-commit run pipewarden-full)
```

```bash
pre-commit install                         # enables commit-time hook
pre-commit install --hook-type pre-push    # enables push-time hook
```

### Available Hooks

| Hook ID | When it runs | What it does | Typical time |
|---------|--------------|--------------|--------------|
| `pipewarden-secrets` | Every `git commit` | Scans ALL files for secrets | ~0.1s |
| `pipewarden-diff` | Every `git push` | Scans only changed files vs `origin/main` | ~0.05s |
| `pipewarden-full` | Manual only | Full pipeline: install, lint, test, build, scan | 30–300s |

### The Complete Workflow With Pre-Commit Hooks

```
Developer writes code
       ↓
git commit
       ↓
[pipewarden-secrets runs automatically — ~0.1s]
  ✓ No secrets found → commit is created
  ✗ Secret found    → commit is BLOCKED, rotate before committing
       ↓
git push
       ↓
[pipewarden-diff runs automatically — ~0.05s]
  ✓ No secrets in changed files → push proceeds
  ✗ Secret found               → push BLOCKED
       ↓
CI runs: pipewarden --sarif-out report.sarif --junit-out junit.xml
       ↓
Pull request can be merged
```

No credential ever reaches the remote. No broken code is ever deployed.

---

## CLI Reference

### All Options

```
pipewarden [OPTIONS]

  Run against the current directory (all detected languages).

OPTIONS

  --root PATH          Project root to scan (default: current directory)
  --config FILE        Path to .pipewarden.toml (default: auto-discover)

  --only STAGE         Run only this stage — repeatable
                       Example: --only secrets --only python
  --skip STAGE         Skip this stage — repeatable
                       Example: --skip docker --skip vulns
  --diff REF           Restrict secret scan to files changed vs REF
                       Example: --diff origin/main
  --fail-fast          Stop immediately on the first failure
  --dry-run            Show which stages would run without executing

  --init               Scaffold a .pipewarden.toml and exit
  --validate           Validate the config file and exit (0 = valid, 3 = error)
  --list-stages        Show detected and enabled stages, then exit

  --json               Output JSON report to stdout (no pretty output)
  --sarif-out FILE     Write SARIF 2.1 report (GitHub Code Scanning, Azure DevOps)
  --junit-out FILE     Write JUnit XML report (CI test dashboards)
  --markdown-out FILE  Write Markdown summary (use $GITHUB_STEP_SUMMARY for GHA)
  --gh-annotations     Print GitHub Actions inline PR annotations to stdout
  --log-file FILE      Write verbose debug log to FILE
  --no-color           Disable ANSI colours
  --verbose / -v       Enable verbose logging to stderr
  --docker-tag TAG     Override the Docker image tag for the docker stage

  --version            Print version and exit
  --help               Show this help and exit
```

### Available Stage Names

```
secrets    Secret scanning (always first); full history scan via scan_history config
vulns      Dependency CVE scan (pip-audit --strict / npm audit --audit-level=high --omit=dev / cargo audit / govulncheck ./... / dotnet list package --vulnerable)
outdated   Outdated package check — non-blocking, informational
python     Python: venv + install + lint(ruff) + typecheck(mypy) + test(pytest)
node       Node.js: install + lint + typecheck + test + build
dotnet     .NET: restore + format + build + test + vuln scan
go         Go: mod download + vet + build + test
rust       Rust: fetch + clippy + build + test
docker     Docker: hadolint + docker build + container scan (trivy/grype)
```

### Common Usage Patterns

```bash
# Run everything (default)
pipewarden

# Secrets only — fastest, good for pre-commit
pipewarden --only secrets

# Secrets + Python — good for pre-push
pipewarden --only secrets --only python

# Secrets + .NET — good for .NET pre-push
pipewarden --only secrets --only dotnet

# Skip Docker (no daemon available)
pipewarden --skip docker

# Only scan changed files vs main
pipewarden --only secrets --diff origin/main

# Stop on first failure
pipewarden --fail-fast

# Preview without executing
pipewarden --dry-run

# Scaffold a config file
pipewarden --init

# Validate config
pipewarden --validate

# List what was detected
pipewarden --list-stages

# Run against a subdirectory
pipewarden --root ./services/my-service

# Generate all report formats
pipewarden \
  --json \
  --sarif-out findings.sarif \
  --junit-out results.xml \
  --markdown-out "$GITHUB_STEP_SUMMARY"

# Enable verbose logging
pipewarden --verbose

# Write debug log to file
pipewarden --log-file pipewarden.log
```

---

## Frequently Asked Questions

**Q: I have no `.pipewarden.toml` file. Will it still work?**

Yes. All configuration has sensible defaults. The tool detects your project type automatically. A config file is only needed if you want to override something specific.

---

**Q: My project uses Python AND Node.js. Which one runs?**

Both. Pipewarden detects all languages present and runs each in sequence. The summary shows every step from all languages.

---

**Q: What if I don't have pytest / ruff / mypy installed?**

Pipewarden creates an isolated virtual environment. If `pytest` is not installed in it, you get a `warned` step (not a failure). Optional tools like `mypy` are only run if installed AND configured. Nothing ever fails just because an optional tool is absent.

---

**Q: Will it delete my existing virtual environment?**

No. Pipewarden only touches `.pipewarden-venv/`. Your existing `.venv`, `venv`, or `env` folder is never modified.

---

**Q: Can I use it in a monorepo where each subdirectory is a different language?**

Yes. Use `--root` to point Pipewarden at each subdirectory:

```bash
pipewarden --root ./backend    # Python service
pipewarden --root ./frontend   # Node.js service
pipewarden --root ./api        # .NET service
```

Or run them in parallel CI jobs, each with its own `--root`.

---

**Q: The Docker stage fails because there is no Docker daemon in CI. How do I skip it?**

Note: when no Docker daemon is detected, the behaviour differs by environment:
- **In CI** (when `CI`, `GITHUB_ACTIONS`, `GITLAB_CI`, or `TF_BUILD` env vars are set): the step is marked **WARNED** and the pipeline continues.
- **Locally** (no CI env vars): the step is marked **FAILED** and, with `fail_fast`, the pipeline stops.

To skip the Docker stage entirely:

```bash
pipewarden --skip docker
```

Or permanently in config:
```toml
[stages]
docker = false
```

---

**Q: I have a Dockerfile but no `docker:scan` step appears in the output. Why?**

The container scan step only appears when `trivy` or `grype` is on your PATH. If neither is installed, the step is simply omitted — there is no WARNED entry. Install one to enable scanning:

```bash
# macOS
brew install trivy

# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
```

---

**Q: How do I handle a legitimate test fixture that looks like a secret?**

Add it to the allowlist:
```toml
[secrets]
allowlist_paths   = ["tests/fixtures/**"]
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]
```

---

**Q: The secrets scan reports something as CRITICAL but I am sure it is a false positive. What do I do?**

First, confirm it is actually a false positive — look at the file and line shown. If it genuinely is a test fixture or documentation example, allowlist it (see above). If the rule fires too broadly on your codebase, disable that specific rule:
```toml
[secrets]
allowlist_rules = ["jwt"]
```

---

**Q: How is Pipewarden different from running each tool separately?**

Pipewarden provides:
- **Automatic detection** — no config needed to pick the right tools
- **Correct ordering** — secrets always first, deps before lint, deps before test
- **Isolated environments** — never pollutes your project's venv
- **Stable exit codes** — exit 4 specifically for secrets lets CI react differently
- **Machine-readable reports** — SARIF, JUnit XML, JSON, Markdown from one command
- **Consistent output** — same format regardless of language or tool
- **Zero maintenance** — update one tool instead of maintaining per-project CI scripts

---

**Q: Does Pipewarden send any data anywhere?**

No. Zero telemetry. Zero network calls at runtime (except when downloading dependencies as part of your build). Fully private.

---

**Q: What Python version is required?**

Python 3.10 or later. On 3.11+ there are zero third-party dependencies. On 3.10, `tomli` is installed for TOML parsing.

---

**Q: I get `externally-managed-environment` when installing on Ubuntu/Debian.**

This is a Python packaging restriction on system Python. Use one of:

```bash
pip install --break-system-packages pipewarden   # simplest
pip install --user pipewarden                     # user install
pipx install pipewarden                           # isolated tool install (recommended)
```

---

## Contributing

### Setup

```bash
git clone https://github.com/gcfernando/pipewarden.git
cd pipewarden
pip install -e ".[dev]"
pipewarden    # runs itself — self-test
```

### Running Tests

```bash
pytest -q                          # run all tests
pytest -q --tb=short -x            # stop at first failure
pytest -q --cov=src/pipewarden     # with coverage
```

### Code Quality

```bash
ruff check .          # lint
ruff format .         # format
mypy .                # type check (mirrors what Pipewarden runs)
```

### Development Conventions

- **No new runtime dependencies** — product story is "zero deps"
- **Tests for every new feature** — 160 tests with ≥85% branch coverage
- **Type hints everywhere** — `mypy --strict` must pass
- **Stable exit codes** — do not change without a major version bump
- **Every new secret pattern** — add rule ID, positive test, negative test, update CHANGELOG
- **Every new language stage** — add to `ALL_STAGES`, `STAGES` registry, CLI init template, and tests

### How Pipewarden Tests Itself

Pipewarden uses itself as its own quality gate:

```bash
# Run in the Pipewarden repository
pipewarden
```

The `.github/workflows/quality-gate.yml` workflow runs Pipewarden on every push and pull request, scanning the Pipewarden codebase with Pipewarden.

---

<div align="center">

**Pipewarden** · [GitHub](https://github.com/gcfernando/pipewarden) · [PyPI](https://pypi.org/project/pipewarden/) · [Issues](https://github.com/gcfernando/pipewarden/issues)

MIT License · Made with ☕ by [Gehan Fernando](https://github.com/gcfernando)

</div>

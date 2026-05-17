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

## ⚡ 30-Second Quick Start

```bash
pip install pipewarden   # one-time install
cd your-project
pipewarden               # run in any project — no config needed
```

Pipewarden automatically figures out what kind of project you have and runs everything in the right order. You will see a summary like this:

```
✓ secrets:fallback    passed    0.1s   scanned 34 files, no secrets
✓ py:deps(pyproject)  passed    4.1s
✓ py:lint(ruff)       passed    0.3s
✓ py:test(pytest)     passed    6.2s
✓ all 4 steps passed in 10.7s
```

**Reading the result at a glance:**
- `✓` = passed — nothing to do
- `✗` = failed — the full error is printed below the summary
- `⚠` = warned — an optional tool is missing, pipeline continues
- Exit `0` = all good. Exit `1` = something failed. Exit `4` = a **secret was found** — rotate it immediately.

---

## 📖 Table of Contents

| # | Section |
|---|---------|
| 1 | [What Is Pipewarden?](#-what-is-pipewarden) |
| 2 | [The Problem It Solves](#-the-problem-it-solves) |
| 3 | [Who Should Use It?](#-who-should-use-it) |
| 4 | [See It In Action](#-see-it-in-action) |
| 5 | [Installation](#-installation) |
| 6 | [How It Works — The Pipeline Stages](#️-how-it-works--the-pipeline-stages) |
| 7 | [Python Projects — Complete Guide](#-python-projects--complete-guide) |
| 8 | [.NET Projects — Complete Guide](#-net-projects--complete-guide) |
| 9 | [Node.js / Go / Rust — Quick Guides](#-nodejs--go--rust--quick-guides) |
| 10 | [Secret Scanning Deep Dive](#-secret-scanning-deep-dive) |
| 11 | [What To Do When Secrets Are Found](#-what-to-do-when-secrets-are-found) |
| 12 | [Reading the Output](#-reading-the-output) |
| 13 | [Reports — SARIF, JUnit XML, JSON, Markdown](#-reports--sarif-junit-xml-json-markdown) |
| 14 | [Configuration Reference](#-configuration-reference) |
| 15 | [Environment Variable Overrides](#-environment-variable-overrides) |
| 16 | [CI / CD Integration](#-ci--cd-integration) |
| 17 | [GitHub Actions (Official Action)](#-github-actions-official-action) |
| 18 | [Pre-Commit Hooks](#-pre-commit-hooks) |
| 19 | [CLI Reference](#-cli-reference) |
| 20 | [Business Benefits & ROI](#-business-benefits--roi) |
| 21 | [Frequently Asked Questions](#-frequently-asked-questions) |
| 22 | [Contributing](#-contributing) |

---

## 🛡️ What Is Pipewarden?

**Pipewarden** is a free, open-source command-line tool that acts as a **universal quality gate** for any software project.

In plain language: you run **one command** and it automatically:

1. **Figures out what kind of project you have** (Python? Node? Go? Rust? .NET? Docker? All of them?)
2. **Installs your dependencies** using the right package manager
3. **Scans for leaked secrets** (API keys, passwords, tokens) before they leave your machine
4. **Lints your code** to catch style and logic errors
5. **Runs your tests**
6. **Builds your application**

Everything in the right order. With timeouts. With human-readable output. With machine-readable reports for your CI dashboard.

> **Zero configuration needed.** Drop it into any repository and it just works.

---

## 😩 The Problem It Solves

### The Old Way — Every Team Writes This From Scratch

Every time a team starts a new project, someone writes the same CI pipeline they've written a dozen times before:

```yaml
# The script you've written 40 times already
- name: Install deps
  run: pip install -r requirements.txt

- name: Lint
  run: flake8 .

- name: Test
  run: pytest

- name: Check secrets
  run: # ... wait, which tool do we use again?
```

This creates real problems:

| Problem | Impact |
|---------|--------|
| Every project has a different CI setup | New engineers waste hours understanding each one |
| Secret scanning is often skipped | AWS keys, GitHub tokens get committed and leaked |
| Pipelines break silently | A missing tool isn't caught until production |
| Polyglot repos need multiple pipelines | Maintenance cost multiplies with each language |
| No standard reports | Security findings live in logs, not dashboards |

### The Pipewarden Way

```bash
pip install pipewarden
pipewarden
```

That's it. Same command for every project. Every language. Every CI system.

---

## 👥 Who Should Use It?

| Role | How Pipewarden Helps |
|------|--------------------------|
| **Individual Developer** | Run the same quality checks locally that CI runs remotely. Catch issues before pushing. |
| **Team Lead / Tech Lead** | Enforce a consistent quality baseline across all repositories with zero per-project setup. |
| **DevOps / Platform Engineer** | Replace bespoke CI scripts with one standard tool. Reduce pipeline maintenance to zero. |
| **Security Engineer** | Automatically scan every commit for leaked secrets. Get SARIF reports in GitHub Security tab. |
| **CTO / Engineering Manager** | Reduce security incidents. Speed up onboarding. Standardise engineering practices at scale. |
| **Open Source Maintainer** | Add comprehensive CI to any contributor's PR in seconds. |

---

## 🚀 See It In Action

Here is what a real run looks like on a Python + Node + Docker project:

```console
$ pipewarden

════════════════════════════════════════════════════════════════
  Pipewarden 1.3.0
════════════════════════════════════════════════════════════════
  root:     /home/alice/my-app
  config:   (defaults — no config file found)
  detected: python, node(npm), docker(Dockerfile)

════════════════════════════════════════════════════════════════
  Secrets
════════════════════════════════════════════════════════════════
✓ secrets:fallback (0.1s)

════════════════════════════════════════════════════════════════
  Python
════════════════════════════════════════════════════════════════
✓ py:venv (2.9s)
✓ py:deps(pyproject) (4.1s)
✓ py:lint(ruff) (0.3s)
✓ py:test(pytest) (6.2s)

════════════════════════════════════════════════════════════════
  Node
════════════════════════════════════════════════════════════════
✓ node:deps(npm) (8.4s)
✓ node:lint (3.2s)
✓ node:test (12.1s)
✓ node:build (5.7s)

════════════════════════════════════════════════════════════════
  Docker
════════════════════════════════════════════════════════════════
✓ docker:build (18.3s)

════════════════════════════════════════════════════════════════
  Summary
════════════════════════════════════════════════════════════════
  ✓ secrets:fallback    passed      0.1s   scanned 34 files, no secrets
  ✓ py:venv             passed      2.9s
  ✓ py:deps(pyproject)  passed      4.1s
  ✓ py:lint(ruff)       passed      0.3s
  ✓ py:test(pytest)     passed      6.2s
  ✓ node:deps(npm)      passed      8.4s
  ✓ node:lint           passed      3.2s
  ✓ node:test           passed     12.1s
  ✓ node:build          passed      5.7s
  ✓ docker:build        passed     18.3s

  ✓ all 10 steps passed in 61.4s
```

**Exit code `0`.** CI passes. Ship it.

<br>

Now here is what it looks like when a developer accidentally commits an AWS key:

```console
$ pipewarden

════════════════════════════════════════════════════════════════
  Secrets
════════════════════════════════════════════════════════════════
✗ secrets:fallback (0.1s)

════════════════════════════════════════════════════════════════
  Summary
════════════════════════════════════════════════════════════════
  ✗ secrets:fallback    failed      0.1s   1 possible secrets in 12 files

Failing step output (tail):

── secrets:fallback ──
Findings (1):
  CRITICAL  src/config.py:14  [aws.access_key]  AKIA…WXYZ
```

**Exit code `4` (secrets specifically failed).** The pipeline stops. The key never reaches the remote repository.

---

## 📦 Installation

### Option 1 — Install from PyPI *(recommended)*

```bash
pip install pipewarden
```

Verify the installation:

```bash
pipewarden --version
# → pipewarden 1.3.0
```

### Option 2 — Install from Source

```bash
pip install git+https://github.com/gcfernando/pipewarden.git@v1.3.0
```

### Option 3 — Docker

```bash
docker run --rm -v "$(pwd):/repo" ghcr.io/gcfernando/pipewarden:latest \
  pipewarden --root /repo
```

### Troubleshooting Installation

| Error | Fix |
|-------|-----|
| `Permission denied` | `pip install --user pipewarden` |
| `externally-managed-environment` | `pip install --break-system-packages pipewarden` |
| `command not found` after install | Add `~/.local/bin` to your `PATH` |

> **No runtime dependencies.** On Python 3.11+ the tool has literally zero third-party dependencies. On 3.10 it needs only `tomli` for TOML parsing. Nothing else is installed into your project.

---

## ⚙️ How It Works — The Pipeline Stages

Pipewarden always runs stages in this order. Each stage only runs if the relevant files are detected.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Pipewarden FLOW                              │
├──────────┬──────────────────────────────────────────────────────┤
│ Stage 1  │  DETECT                                              │
│          │  Reads the project folder. Identifies which          │
│          │  languages and tools are present.                    │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 2  │  SECRETS  (always first)                             │
│          │  Scans every file for leaked credentials.            │
│          │  Blocks the pipeline immediately if found.           │
│          │  Optional: scan full git history with gitleaks.      │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 3  │  INSTALL                                             │
│          │  Creates isolated environments and installs          │
│          │  all declared dependencies.                          │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 4  │  LINT / FORMAT                                       │
│          │  Runs the appropriate linter for each language.      │
│          │  .NET: also enforces code formatting via             │
│          │  dotnet format --verify-no-changes.                  │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 5  │  TEST                                                │
│          │  Runs your test suite.                               │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 6  │  BUILD                                               │
│          │  Compiles or packages your application.              │
│          │  Docker: image is also scanned with trivy/grype      │
│          │  for known CVEs after a successful build.            │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 7  │  VULNS  (optional)                                   │
│          │  Checks declared dependencies for known CVEs.        │
│          │  pip-audit / npm audit / cargo-audit / govulncheck   │
│          │  / dotnet list package --vulnerable                  │
├──────────┼──────────────────────────────────────────────────────┤
│ Stage 8  │  OUTDATED  (optional, non-blocking)                  │
│          │  Reports newer versions available for all languages. │
│          │  Never fails the pipeline — informational only.      │
└──────────┴──────────────────────────────────────────────────────┘
```

### What Gets Detected and What Runs

| If the project contains… | Language detected | Tools used |
|--------------------------|-------------------|------------|
| `pyproject.toml`, `requirements.txt`, `setup.py` | **Python** | venv + pip / poetry / uv → ruff → mypy → pytest |
| `package.json` | **Node.js** | npm / pnpm / yarn → lint script → test script → build script |
| `*.sln` or `*.csproj` | **.NET** | dotnet restore → format → build → test → vuln scan (opt-in) |
| `go.mod` | **Go** | go mod download → go vet → go build → go test |
| `Cargo.toml` | **Rust** | cargo fetch → cargo clippy → cargo build → cargo test |
| `Dockerfile` or `Containerfile` | **Docker** | hadolint (lint) → docker build → container scan (trivy/grype, if installed) |

> **Polyglot repos are fully supported.** A monorepo containing Python, Node, and Rust will run all three pipelines in a single `pipewarden` invocation.

### Package Manager Auto-Detection

Pipewarden picks the right tool automatically — no config needed:

**Python:**
```
uv.lock present?    → uses uv sync --frozen
poetry.lock present? → uses poetry install
pyproject.toml?     → uses pip install -e .
requirements.txt?   → uses pip install -r requirements.txt
```

**Node:**
```
pnpm-lock.yaml?     → uses pnpm install --frozen-lockfile
yarn.lock?          → uses yarn install --frozen-lockfile
package-lock.json?  → uses npm ci
(no lockfile)       → uses npm install
```

### Vulnerability Scanning (optional)

When the `vulns` stage is enabled, Pipewarden runs dependency vulnerability scans using whichever tools are installed:

| Tool | Language | What it scans | Install |
|------|----------|---------------|---------|
| `pip-audit` | Python | PyPI packages against OSV / PyPA advisory databases | `pip install pip-audit` |
| `npm audit` | Node | npm registry security advisories | built into npm |
| `cargo-audit` | Rust | RustSec advisory database | `cargo install cargo-audit` |
| `govulncheck` | Go | Go vulnerability database | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| `dotnet list package --vulnerable` | .NET | NuGet packages against GitHub Advisory DB | built into .NET SDK |

If none of these tools are installed, the stage is **skipped** — it never blocks your pipeline for a missing optional tool.

### Container Image Vulnerability Scanning

After a successful `docker build`, Pipewarden automatically scans the built image for OS-level and application-level CVEs if either `trivy` or `grype` is on the PATH:

| Tool | Priority | What it scans | Install |
|------|----------|---------------|---------|
| `trivy` | First choice | OS packages + app deps in the image | `brew install aquasecurity/trivy/trivy` or [download binary](https://github.com/aquasecurity/trivy/releases) |
| `grype` | Fallback | OS packages + app deps in the image | `brew install anchore/grype/grype` or [download binary](https://github.com/anchore/grype/releases) |

Findings at `HIGH` or `CRITICAL` severity **fail the pipeline**. If neither tool is installed, the scan step is `WARNED` (non-blocking). No scan tool is ever required.

```console
  Docker
✓ docker:lint(hadolint)     (0.2s)
✓ docker:build              (22.1s)
✓ docker:scan(trivy)         (8.4s)   ← only runs if trivy or grype is installed
```

#### What a Vulnerability Finding Looks Like

```console
✗ vulns:pip-audit (4.2s)

── vulns:pip-audit ──
cryptography 41.0.0
  ID:       GHSA-jfh8-c2jp-5v3q
  Severity: HIGH
  Fix:      upgrade to 41.0.4 or later
  Detail:   RSA key pair generation does not verify that p != q
```

#### What To Do When a Vulnerability Is Found

| Step | Action |
|------|--------|
| 1 | Note the package name and the recommended fix version |
| 2 | Upgrade: `pip install "cryptography>=41.0.4"` (or update `requirements.txt` / `pyproject.toml`) |
| 3 | Run `pipewarden --only vulns` again to confirm the finding is gone |
| 4 | If upgrading breaks your code, check the CVE detail — some findings are in code paths you do not use and can be accepted as low-risk with a documented decision |
| 5 | To suppress a known false positive: `pip-audit --ignore-vuln GHSA-jfh8-c2jp-5v3q` (see pip-audit docs) |

> Enable vuln scanning by adding `vulns = true` to your `.pipewarden.toml` under `[stages]`.

---

## 🐍 Python Projects — Complete Guide

### The Traditional Python Pipeline (What Teams Write Today)

Before Pipewarden, every Python project requires writing and maintaining a CI pipeline from scratch. Here is what a typical production-grade Python pipeline looks like:

```yaml
# .github/workflows/ci.yml  ← The traditional approach
name: Python CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # ── Job 1: Lint & type-check ──────────────────────────────────────────────
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install ruff mypy
      - run: ruff check .
      - run: ruff format --check .
      - run: mypy src/
        # ↑ Fails with hundreds of errors if the project has no type annotations

  # ── Job 2: Tests on every OS × Python version ─────────────────────────────
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.10", "3.11", "3.12", "3.13", "3.x"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
          # ↑ What if the project uses requirements.txt instead?
          # ↑ What if it uses poetry? What if it uses uv?
          # ↑ Every project is different — you have to check every time.
      - name: Run tests with coverage
        run: |
          pytest --cov=src \
                 --cov-report=xml \
                 --cov-report=term-missing \
                 --junit-xml=test-results.xml
          # ↑ Fails if pytest-cov is not in dev dependencies
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          # ↑ Requires a Codecov account, an API token, and a repository secret

  # ── Job 3: Secret scanning (separate job, separate container) ─────────────
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0    # gitleaks needs full history
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # ↑ Another tool to configure, another action to update

  # ── Job 4: Vulnerability scanning ─────────────────────────────────────────
  vulns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: |
          pip install pip-audit
          pip-audit
          # ↑ Another tool. Another job. Another 45-second container startup.
```

**This is 80+ lines across 4 separate jobs.** Every new Python project you create, you copy and adapt this file. You forget to update it when you switch from `requirements.txt` to `pyproject.toml`. The lint job runs in a different environment from the test job so failures don't match. Secrets scanning adds a full job startup overhead. New engineers spend hours understanding why each piece is there.

---

### With Pipewarden — 5 Lines Replace 80

```yaml
# .github/workflows/ci.yml  ← The Pipewarden approach
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

One job. One command. Secret scanning, dependency installation, linting, type checking, testing, and vulnerability scanning — in the right order, every time.

---

### Step-by-Step: Exactly What Pipewarden Does for a Python Project

#### Step 1 — Detection

Pipewarden scans the project root for any of these files:

| File found | Result |
|------------|--------|
| `pyproject.toml` | Python stage enabled |
| `requirements.txt` | Python stage enabled |
| `setup.py` | Python stage enabled |
| `setup.cfg` | Python stage enabled |
| None of the above | Python stage skipped silently |

#### Step 2 — Create Virtual Environment

```bash
python -m venv .pipewarden-venv
```

Creates `.pipewarden-venv/` inside your project root. If it already exists, it is **reused** (the creation step is skipped entirely). This makes local re-runs fast.

```console
✓ py:venv (2.9s)    # created fresh
✓ py:venv (0.0s)    # reused existing — not shown if it exists
```

> Pipewarden **never touches** your existing `.venv`, `venv`, or `env` folder. It always uses its own isolated environment.

Add the folder to `.gitignore`:
```
.pipewarden-venv/
```

#### Step 3 — Install Dependencies

Pipewarden checks which package manager to use in this exact priority order:

```
1. uv.lock present  AND  uv on PATH?
      → uv sync --frozen
      → 10–100x faster than pip; uses locked versions; no surprises

2. poetry.lock present  AND  poetry on PATH?
      → poetry install --no-interaction
      → Respects poetry's dependency resolver; no user prompts

3. pyproject.toml present (no lock file)?
      → pip install --quiet -e .
      → Installs the package in editable mode with all declared deps

4. requirements.txt present (fallback)?
      → pip install --quiet -r requirements.txt
      → Handles legacy projects and simple scripts

5. None of the above?
      → step recorded as SKIPPED: "no manifest"
      → Pipeline continues with linting skipped too
```

The step name in the output tells you exactly which path was taken:

```console
✓ py:deps(uv)           (1.2s)   ← uv sync --frozen was used
✓ py:deps(poetry)       (8.4s)   ← poetry install --no-interaction was used
✓ py:deps(pyproject)   (12.2s)   ← pip install -e .
✓ py:deps(requirements) (9.7s)   ← pip install -r requirements.txt
```

#### Step 4 — Lint with ruff

If `ruff` is on the system PATH:

```bash
ruff check .
```

```console
✓ py:lint(ruff) (0.3s)         ← No issues found
✗ py:lint(ruff) (0.4s)         ← Lint errors found — output printed below summary
⚠ py:lint       (0.0s)         ← ruff not installed — warning, not failure
```

**What ruff catches** (selected rules from 800+ total):

| Category | Examples |
|----------|---------|
| Unused imports | `import os` — never used |
| Undefined names | `pritn("hello")` — typo |
| Mutable defaults | `def f(x=[]):` — classic Python bug |
| Bare except | `except:` — hides all errors |
| Shadowed builtins | `list = [1, 2, 3]` |
| Import order | Imports not grouped per PEP 8 |
| String formatting | Use f-strings instead of `.format()` |
| Simplification | `if x == True:` → `if x:` |

If ruff is not on the PATH, the step is recorded as `warned` — **the pipeline does not fail**. To enable linting:

```bash
pip install ruff                          # globally
# OR add to pyproject.toml:
[project.optional-dependencies]
dev = ["ruff>=0.4.0"]
```

#### Step 5 — Type Check with mypy

mypy runs **only if both** conditions are met:

1. `mypy` is on the system PATH
2. The project has a mypy config: `mypy.ini` exists, **or** `[tool.mypy]` section exists in `pyproject.toml`

This prevents the extremely common pain of running mypy on a project with no type annotations and getting 500+ confusing errors.

```console
✓ py:typecheck(mypy) (1.2s)    ← All types are correct
✗ py:typecheck(mypy) (1.4s)    ← Type errors found
                                   (step not shown if mypy is unconfigured)
```

**Minimal mypy config to enable it:**

```toml
# pyproject.toml
[tool.mypy]
strict = true
```

Or for a gentler start:

```toml
[tool.mypy]
ignore_missing_imports = true
```

#### Step 6 — Test with pytest

First, Pipewarden **probes** whether pytest is importable in the virtual environment:

```bash
python -m python -c "import pytest"    # internal probe — not shown in output
```

If pytest is not installed, you get a clear warning instead of a confusing error:

```console
⚠ py:test(pytest)   pytest not installed in the project —
                     add it as a dep or skip this stage
```

If pytest is available, Pipewarden runs:

```bash
python -m pytest -q
```

Tests are only run if a test directory exists:

| Condition | Test step |
|-----------|-----------|
| `tests/` directory exists | Runs pytest |
| `test/` directory exists | Runs pytest |
| `[tool.pytest.ini_options]` in pyproject.toml | Runs pytest |
| None of the above | Test step skipped silently |

```console
✓ py:test(pytest) (6.2s)     ← All tests passed
✗ py:test(pytest) (6.4s)     ← Tests failed (last 60 lines printed automatically)
```

---

### All Supported Python Project Layouts

#### Layout A — Modern Package with uv

```
my-package/
├── pyproject.toml          ← Python detected
├── uv.lock                 ← uv selected as installer
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

**Output:**
```console
✓ py:venv              (2.9s)
✓ py:deps(uv)          (1.2s)
✓ py:lint(ruff)        (0.3s)
✓ py:test(pytest)      (2.1s)
```

#### Layout B — Legacy Application with requirements.txt

```
my-app/
├── requirements.txt        ← Python detected, pip selected
├── app/
│   ├── __init__.py
│   └── main.py
└── tests/
    └── test_main.py
```

> **Important:** Make sure `pytest` is listed in `requirements.txt`. If it is only in a separate `requirements-dev.txt`, Pipewarden will not install it automatically — add it to the main file or switch to `pyproject.toml`.

**Output:**
```console
✓ py:venv                  (2.9s)
✓ py:deps(requirements)    (8.1s)
✓ py:lint(ruff)            (0.3s)
✓ py:test(pytest)          (3.4s)
```

#### Layout C — Poetry Project

```
my-service/
├── pyproject.toml          ← Python detected
├── poetry.lock             ← Poetry selected as installer
├── my_service/
│   └── __init__.py
└── tests/
    └── conftest.py
```

**Output:**
```console
✓ py:venv              (2.9s)
✓ py:deps(poetry)      (6.4s)
✓ py:lint(ruff)        (0.3s)
✓ py:typecheck(mypy)   (1.1s)   ← only if [tool.mypy] exists
✓ py:test(pytest)      (4.2s)
```

#### Layout D — FastAPI / Django Web App + Docker

```
my-api/
├── pyproject.toml
├── uv.lock
├── src/
│   └── api/
│       ├── main.py
│       ├── models.py
│       └── routers/
├── tests/
│   ├── conftest.py
│   └── test_endpoints.py
└── Dockerfile              ← Docker stage also runs automatically
```

**Output:**
```console
  Python
✓ py:venv              (2.9s)
✓ py:deps(uv)          (1.3s)
✓ py:lint(ruff)        (0.4s)
✓ py:typecheck(mypy)   (2.1s)
✓ py:test(pytest)      (8.7s)

  Docker
✓ docker:lint(hadolint) (0.2s)
✓ docker:build          (22.1s)
```

Both stages run automatically — no configuration needed.

#### Layout E — Data Science / Notebook Project

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

**Output:**
```console
✓ py:venv                  (2.9s)
✓ py:deps(requirements)    (45.2s)   ← may be slow (numpy, pandas, torch…)
✓ py:lint(ruff)            (0.3s)
✓ py:test(pytest)          (3.1s)    ← only unit tests; notebooks are not executed
```

> **Tip:** For data science projects with large dependencies (PyTorch, TensorFlow), increase the install timeout:
> ```toml
> [timeouts]
> install_s = 1800    # 30 minutes
> ```

---

### Python Configuration Examples

#### Run only Python (skip all other detected languages)

```bash
pipewarden --only python
```

#### Run secrets + Python (recommended pre-push hook)

```bash
pipewarden --only secrets --only python
```

#### Tune timeouts for a slow test suite

```toml
# .pipewarden.toml
[timeouts]
test_s    = 3600    # 60 minutes
install_s = 1800    # 30 minutes for heavy deps (PyTorch etc.)
```

#### Disable the Python stage entirely

```toml
# .pipewarden.toml
[stages]
python = false
```

#### Full example for a Python microservice

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
# First run — creates .pipewarden-venv and installs all deps
pipewarden

# Subsequent runs — reuses venv, fast
pipewarden

# Quick lint + test loop while developing
pipewarden --only python

# Pre-commit check (secrets only — sub-second)
pipewarden --only secrets

# Pre-push full check
pipewarden --only secrets --only python

# Force reinstall after changing dependencies
Remove-Item -Recurse -Force .pipewarden-venv   # Windows
# rm -rf .pipewarden-venv                      # macOS/Linux
pipewarden
```

---

### Python Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `py:deps` fails with `No module named pip` | Broken Python install | Reinstall Python or use pyenv/mise |
| `py:test` shows `WARNED: pytest not installed` | pytest not in project deps | Add `pytest` to `requirements.txt` or `pyproject.toml` |
| `py:lint` shows `SKIPPED: ruff not installed` | ruff not on PATH | `pip install ruff` or add to dev deps |
| `py:typecheck` never runs | mypy not configured | Add `[tool.mypy]` to `pyproject.toml` |
| Tests time out | Slow test suite or infinite loop | Increase `test_s` in config; run `pytest -x` manually to find the slow test |
| Venv creation fails on Windows | Antivirus or permission issue | Add project folder to AV exclusions; run as administrator |
| Poetry install ignores dev deps | Running in CI mode | This is intentional — `poetry install` installs all groups by default |
| uv not found despite being installed | uv not on system PATH | Add uv to PATH or install globally: `pip install uv` |

---

## 🔷 .NET Projects — Complete Guide

### The Traditional .NET Pipeline (What Teams Write Today)

Here is a representative production .NET CI pipeline before Pipewarden:

```yaml
# .github/workflows/dotnet-ci.yml  ← The traditional approach
name: .NET CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # ── Job 1: Build and test ──────────────────────────────────────────────────
  build-and-test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        dotnet-version: ['8.0.x', '9.0.x']

    steps:
      - uses: actions/checkout@v4

      - name: Set up .NET SDK
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet-version }}

      # NuGet cache — if you forget this step, every CI run re-downloads
      # hundreds of MB of packages
      - name: Cache NuGet packages
        uses: actions/cache@v4
        with:
          path: ~/.nuget/packages
          key: ${{ runner.os }}-nuget-${{ hashFiles('**/*.csproj') }}
          restore-keys: |
            ${{ runner.os }}-nuget-

      - name: Restore NuGet packages
        run: dotnet restore
        # ↑ Must come AFTER cache step or the cache does nothing

      - name: Build (Release)
        run: dotnet build --no-restore --configuration Release --nologo
        # ↑ Must specify --no-restore explicitly or it restores again (slow)
        # ↑ --nologo suppresses Microsoft header — easy to forget

      - name: Run tests with coverage
        run: |
          dotnet test --no-build \
            --configuration Release \
            --nologo \
            --logger "trx;LogFileName=test-results.trx" \
            --collect:"XPlat Code Coverage" \
            --results-directory ./TestResults
        # ↑ --no-build is REQUIRED or dotnet rebuilds before testing
        # ↑ TRX format — not readable by GitHub Actions natively

      # GitHub Actions doesn't read .trx — you must convert to JUnit XML
      - name: Install TRX → JUnit converter
        if: always()
        run: dotnet tool install -g trx2junit
        # ↑ A dotnet tool installed INSIDE the pipeline run
        # ↑ Needs network access; adds 15–30 seconds every run

      - name: Convert test results
        if: always()
        run: trx2junit ./TestResults/*.trx

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.os }}-${{ matrix.dotnet-version }}
          path: |
            ./TestResults/*.xml
            ./TestResults/*.trx

  # ── Job 2: Secret scanning (separate job, 45-second startup) ──────────────
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # ── Job 3: Code analysis ───────────────────────────────────────────────────
  code-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.0.x'
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: csharp
      - name: Build for analysis
        run: dotnet build
      - name: Analyze
        uses: github/codeql-action/analyze@v3
        # ↑ Adds 10–20 minutes to every CI run
```

**This is 100+ lines across 3 separate jobs.** Pain points:

| Pain Point | Detail |
|------------|--------|
| NuGet cache step | Forget it and every run downloads hundreds of MB |
| Flag ordering matters | `--no-restore` on build, `--no-build` on test — get them backwards and you build twice |
| `.trx` → JUnit conversion | dotnet test produces TRX; GitHub Actions needs JUnit; you install a converter inside CI |
| Matrix bloat | 2 OS × 2 SDK versions = 4 parallel jobs for a simple build |
| Separate startup per job | Secrets job costs 45 seconds just to start a container |
| Windows path separators | `**/*.csproj` cache keys behave differently on Windows vs Linux agents |

---

### With Pipewarden — 5 Lines Replace 100

```yaml
# .github/workflows/ci.yml  ← The Pipewarden approach
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

Pipewarden:
- Detects `.sln` / `.csproj` files automatically
- Runs `dotnet restore` → `dotnet build` → `dotnet test` in the correct order with the correct flags
- Runs secret scanning first, before any build starts
- Produces JUnit XML natively — no converter, no extra tool
- Works identically on Linux, macOS, and Windows

---

### Step-by-Step: Exactly What Pipewarden Does for a .NET Project

#### Step 1 — Detection

Pipewarden scans the project root for:

| File found | Result |
|------------|--------|
| `*.sln` | .NET stage enabled; commands target the whole solution |
| `*.csproj` | .NET stage enabled; commands target this single project |
| `*.fsproj` | .NET stage enabled (F# projects) |
| `*.vbproj` | .NET stage enabled (VB.NET projects) |
| None of the above | .NET stage skipped silently |

If both a `.sln` and `.csproj` are present, the `.sln` takes priority and all commands operate on the solution.

#### Step 2 — dotnet restore

```bash
dotnet restore
```

Downloads all NuGet packages declared in every project in the solution.

```console
✓ dotnet:restore (12.4s)    ← All packages resolved and downloaded
✗ dotnet:restore  (8.1s)    ← Failed — full error printed (missing package, bad feed, etc.)
```

**If this step fails, Pipewarden stops.** There is no point trying to build without dependencies. The exact output from `dotnet restore` is printed in the failure tail so you see the specific package and version that failed.

**Common failure causes:**
- A package version was removed from NuGet.org (use a lock file to pin versions)
- A private feed credential is missing or expired
- The solution references a project that doesn't exist on disk

#### Step 3 — dotnet format (code style check)

```bash
dotnet format --verify-no-changes
```

Checks that all C# / F# / VB files comply with the project's `.editorconfig` and code style rules **without modifying any files**. The step fails if any file would be changed — exactly like running `ruff check .` for Python.

Controlled by `[dotnet] format = true` in `.pipewarden.toml` (default: **on**).

```console
✓ dotnet:format (1.2s)    ← All files are correctly formatted
✗ dotnet:format (0.8s)    ← Formatting violations found — run `dotnet format` locally to fix
```

**To fix locally:**
```bash
dotnet format    # rewrites files in place
```

**To disable** (e.g. for legacy projects not yet on .editorconfig):
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

- `--no-restore` — skips NuGet restore (already done in step 2; without this flag it would restore again)
- `--nologo` — suppresses the "Build Engine version…" Microsoft header for cleaner output

```console
✓ dotnet:build (18.7s)    ← Solution compiled, zero errors
✗ dotnet:build (14.2s)    ← Compilation errors — full compiler output printed
```

**If this step fails, the test step is skipped.** No point running tests against broken code.

**What the failure output looks like:**
```
Failing step output (tail):

── dotnet:build ──
src/MyApp.Api/Controllers/UserController.cs(42,18): error CS0246:
  The type or namespace name 'UserService' could not be found
  (are you missing a using directive or an assembly reference?)

Build FAILED.
  Errors: 1
  Warnings: 3
```

#### Step 5 — dotnet test

```bash
dotnet test --no-build --nologo
```

Runs every test project found in the solution.

- `--no-build` — skips compilation (already done in step 4; without this it would rebuild)
- `--nologo` — cleaner output

```console
✓ dotnet:test (8.3s)     ← All tests passed
✗ dotnet:test (11.2s)    ← Test failures — last 60 lines of output printed
```

**What the failure output looks like:**
```
Failing step output (tail):

── dotnet:test ──
  Failed MyApp.Tests.UserControllerTests.GetUser_Returns404_WhenNotFound [12ms]
  Error Message:
    Assert.Equal() Failure: Values differ
    Expected: 404
    Actual:   200

Failed!  - Failed:     1, Passed:    47, Skipped:     0, Total:    48, Duration: 8.1s
```

**Which projects are tested?** Any project in the solution that contains a reference to a test framework:
- `xunit` or `xunit.runner.visualstudio`
- `NUnit` or `NUnit3TestAdapter`
- `MSTest.TestFramework` or `MSTest.TestAdapter`

Or any project with `<IsTestProject>true</IsTestProject>` in its `.csproj`.

#### Step 6 — Vulnerability Scan (opt-in, default: on)

```bash
dotnet list package --vulnerable --include-transitive
```

Checks every NuGet package in the solution against the **GitHub Advisory Database** for known CVEs. The `--include-transitive` flag catches vulnerabilities in indirect dependencies — packages your packages depend on.

Controlled by `[dotnet] vulns = true` in `.pipewarden.toml` (default: **on**).

```console
✓ dotnet:vulns (4.1s)    ← No vulnerable packages found
✗ dotnet:vulns (3.8s)    ← CVEs found — package name, version, severity, and advisory ID printed
```

**To disable:**
```toml
# .pipewarden.toml
[dotnet]
vulns = false
```

#### Step 7 — Outdated Packages (opt-in, default: off, non-blocking)

```bash
dotnet list package --outdated
```

Lists every NuGet package that has a newer version available. This step is **always** `WARNED` — it never fails the pipeline. It is informational only: a reminder to upgrade, not a blocker.

Controlled by `[dotnet] outdated = true` in `.pipewarden.toml` (default: **off**).

```console
⚠ dotnet:outdated (5.2s)    ← Newer versions available for 3 packages (see output below)
```

**To enable:**
```toml
# .pipewarden.toml
[dotnet]
outdated = true
```

---

### All Supported .NET Project Layouts

#### Layout A — Solution with API + Library + Tests (most common)

```
MyApp/
├── MyApp.sln                          ← .NET detected (solution-level)
├── src/
│   ├── MyApp.Api/
│   │   ├── MyApp.Api.csproj           ← ASP.NET Core Web API
│   │   ├── Program.cs
│   │   └── Controllers/
│   ├── MyApp.Core/
│   │   ├── MyApp.Core.csproj          ← Business logic class library
│   │   └── Services/
│   └── MyApp.Data/
│       ├── MyApp.Data.csproj          ← EF Core data access layer
│       └── Repositories/
└── tests/
    ├── MyApp.Api.Tests/
    │   └── MyApp.Api.Tests.csproj     ← xUnit test project
    └── MyApp.Core.Tests/
        └── MyApp.Core.Tests.csproj    ← xUnit test project
```

**Output:**
```console
  Secrets
✓ secrets:fallback  (0.1s)

  .Net
✓ dotnet:restore    (12.4s)   ← All 5 projects restored
✓ dotnet:format      (1.2s)   ← All files correctly formatted
✓ dotnet:build      (18.7s)   ← All 5 projects compiled
✓ dotnet:test        (8.3s)   ← Both test projects run (48 tests total)
✓ dotnet:vulns       (4.1s)   ← No vulnerable NuGet packages
```

#### Layout B — Single Project (no solution file)

```
MyLibrary/
├── MyLibrary.csproj     ← .NET detected (project-level)
├── src/
│   └── MyClass.cs
└── Tests/
    └── Tests.csproj
```

**Output:**
```console
  .Net
✓ dotnet:restore  (4.1s)
✓ dotnet:format   (0.9s)
✓ dotnet:build    (6.2s)
✓ dotnet:test     (2.1s)
✓ dotnet:vulns    (2.8s)
```

#### Layout C — ASP.NET Core API + Dockerfile (polyglot)

```
MyWebApi/
├── MyWebApi.sln
├── MyWebApi/
│   ├── MyWebApi.csproj        ← ASP.NET Core project
│   ├── Program.cs
│   └── appsettings.json
├── MyWebApi.Tests/
│   └── MyWebApi.Tests.csproj  ← xUnit tests
└── Dockerfile                 ← Docker stage also runs
```

**Output:**
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
✓ docker:scan(trivy)     (8.1s)   ← container image CVE scan
```

Secret scanning, .NET pipeline, Docker build, and container image scan — all from one command.

#### Layout D — Console Application (no test project)

```
MyTool/
├── MyTool.csproj
└── Program.cs
```

**Output:**
```console
  .Net
✓ dotnet:restore  (3.1s)
✓ dotnet:build    (5.4s)
· dotnet:test               ← skipped — no test project found
```

The test step is silently skipped — no error. This is correct behaviour for a project with no tests.

#### Layout E — Microservice Solution with Docker + NuGet Config

```
PaymentService/
├── PaymentService.sln
├── NuGet.config              ← private feed configuration
├── src/
│   └── PaymentService/
│       └── PaymentService.csproj
├── tests/
│   └── PaymentService.Tests/
│       └── PaymentService.Tests.csproj
└── Dockerfile
```

Pipewarden reads `NuGet.config` automatically — you just need the feed credentials in environment variables before running.

---

### .NET Configuration Examples

#### No config needed for a simple project

```bash
pipewarden    # auto-detects .sln, runs restore → build → test
```

#### Skip Docker (no Docker daemon in this CI environment)

```toml
# .pipewarden.toml
[stages]
docker = false
```

Or from the CLI:
```bash
pipewarden --skip docker
```

#### Increase timeouts for large enterprise solutions

Large .NET solutions with 20+ projects can take 5–15 minutes to build:

```toml
# .pipewarden.toml
[timeouts]
install_s = 600     # 10 min for NuGet restore
build_s   = 1200    # 20 min to compile large solutions
test_s    = 3600    # 60 min for extensive test suites
```

#### Run only .NET (skip everything else)

```bash
pipewarden --only dotnet
```

#### Combine secrets + .NET (good for pre-push hooks)

```bash
pipewarden --only secrets --only dotnet
```

#### Fine-tune the .NET pipeline steps

```toml
# .pipewarden.toml
[dotnet]
# dotnet format --verify-no-changes (code style enforcement)
# Set to false for legacy codebases without .editorconfig
format = true

# dotnet list package --vulnerable --include-transitive
# Checks NuGet packages against GitHub Advisory DB
vulns = true

# dotnet list package --outdated (non-blocking, informational only)
# Set to true to see which packages have newer versions available
outdated = false
```

#### Full config for a .NET microservice

```toml
# .pipewarden.toml
fail_fast = false

[stages]
dotnet = true
docker = true
vulns  = true     # enables pip-audit / npm audit / dotnet vulns / etc.
python = false
node   = false
go     = false
rust   = false

[dotnet]
format   = true    # enforce code formatting
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

### .NET-Specific Scenarios

#### Private NuGet Feeds (Azure Artifacts, GitHub Packages, Artifactory)

Configure feeds in `NuGet.config` at the solution root using environment variable references:

```xml
<!-- NuGet.config -->
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

In GitHub Actions, set the environment variables before running Pipewarden:

```yaml
- name: Run Pipewarden
  env:
    NUGET_USERNAME: ${{ github.actor }}
    NUGET_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: pipewarden --junit-out junit.xml
```

Pipewarden passes your environment variables through to `dotnet restore` automatically — no extra configuration in `.pipewarden.toml` needed.

#### Pinning the .NET SDK Version

To ensure everyone (local and CI) builds with the same SDK version, add a `global.json`:

```json
{
  "sdk": {
    "version": "9.0.100",
    "rollForward": "latestPatch"
  }
}
```

Pipewarden respects `global.json` — it does not override or replace the SDK selection.

#### Multiple .NET SDK Versions in CI

In GitHub Actions, install all required SDK versions before running Pipewarden:

```yaml
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: |
      8.0.x
      9.0.x
- run: pip install pipewarden
- run: pipewarden
```

Both SDKs are available on the PATH. `global.json` controls which one `dotnet` uses.

#### Nullable Reference Types and Warnings-as-Errors

If your `.csproj` has `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` or `<Nullable>enable</Nullable>`, compiler warnings become build errors. Pipewarden surfaces these clearly:

```
── dotnet:build ──
error CS8600: Converting null literal or possible null value to non-nullable type.
```

These are real type safety issues. Fix them rather than suppressing them — this is the value of nullable reference types.

#### Running dotnet test with Specific Filters

Pipewarden runs `dotnet test` without filters (all tests). If you want to run only a subset, use `--only dotnet` is not granular enough for test filtering. In that case, skip the Pipewarden dotnet stage and add a custom step in your CI:

```yaml
- run: pipewarden --skip dotnet --junit-out infra-junit.xml
- run: dotnet test --filter "Category=Unit" --nologo
```

This lets Pipewarden handle secrets, linting, and Docker while you control test selection manually.

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
```

---

### .NET Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `dotnet:restore` fails — `Unable to find package X` | Missing NuGet source | Check `NuGet.config`; verify feed URL is correct |
| `dotnet:restore` fails — `401 Unauthorized` | Private feed credential missing or expired | Set `NUGET_USERNAME` / `NUGET_TOKEN` environment variables |
| `dotnet:restore` fails — `No executable found matching command 'dotnet'` | .NET SDK not installed | Install from https://dotnet.microsoft.com/download |
| `dotnet:build` fails — `The framework 'net9.0' was not found` | Wrong SDK version | Install the required SDK; or add `global.json` to pin the version |
| `dotnet:test` shows 0 tests found | No test framework reference in any project | Add `xunit` / `NUnit` / `MSTest` to a test project `.csproj` |
| `dotnet:test` times out | Large test suite | Increase `test_s` in `.pipewarden.toml` |
| Build succeeds locally, fails in CI | SDK version mismatch between local and CI | Add `global.json` to pin the SDK version |
| Many nullable warnings → build fails | `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` is set | Fix the null safety issues, or suppress specific warnings with `<NoWarn>CS8600</NoWarn>` |
| `dotnet:restore` is slow | No NuGet package cache in CI | Add a cache step before Pipewarden in your CI YAML |

---

## 🌐 Node.js / Go / Rust — Quick Guides

Pipewarden supports all three languages automatically. No config file needed — just run `pipewarden` in your project root.

---

### Node.js

**Detected when:** `package.json` is present.

**What runs:**

| Step | Command used | Condition |
|------|-------------|-----------|
| Install deps | `npm ci` / `pnpm install --frozen-lockfile` / `yarn install --frozen-lockfile` | Picks the right tool from lockfile |
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

**Common config:**

```toml
# .pipewarden.toml
[stages]
node = true
docker = false   # no Docker daemon in this CI
```

**Troubleshooting:**

| Symptom | Fix |
|---------|-----|
| `node:lint` skipped | Add `"lint": "eslint ."` to `package.json` scripts |
| `node:test` skipped | Add `"test": "jest"` (or vitest/mocha) to scripts |
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
✓ go:deps    (4.2s)
✓ go:vet     (0.8s)
✓ go:build   (3.1s)
✓ go:test    (7.4s)
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
| Lint (Clippy) | `cargo clippy -- -D warnings` |
| Build | `cargo build` |
| Test | `cargo test` |

**Example output:**

```console
  Rust
✓ rust:deps    (12.1s)
✓ rust:lint     (8.4s)
✓ rust:build   (22.3s)
✓ rust:test     (6.7s)
```

**Troubleshooting:**

| Symptom | Fix |
|---------|-----|
| `cargo clippy` fails with warnings | Fix the warnings; they are treated as errors (`-D warnings`) — this is intentional |
| `rust:deps` times out on first run | Increase `install_s`; first-time Rust builds download many crates |
| `rust:build` slow in CI | Consider `sccache` or `cargo-cache` to reuse the Cargo registry across runs |

---

### Polyglot Repos (Multiple Languages Together)

If your project has `package.json` **and** `go.mod` **and** `Cargo.toml`, all three pipelines run automatically in a single `pipewarden` command. You do not need any configuration — Pipewarden detects and runs each one.

```console
  Secrets
✓ secrets:fallback    (0.2s)

  Node
✓ node:deps(npm)     (8.4s)
✓ node:build         (5.7s)

  Go
✓ go:deps            (4.2s)
✓ go:build           (3.1s)
✓ go:test            (7.4s)

  Rust
✓ rust:deps         (12.1s)
✓ rust:build        (22.3s)
✓ rust:test          (6.7s)
```

To run only one language in a polyglot repo:

```bash
pipewarden --only go
pipewarden --only node
pipewarden --only rust
```

---

## 🔐 Secret Scanning Deep Dive

Secret scanning runs **first**, before any code is installed or built. If secrets are found, the pipeline stops.

### Detection Strategy

```
gitleaks installed?
  YES → Use gitleaks (industry standard, kept up-to-date by security experts)
  NO  → Use built-in regex scanner (conservative, high-precision patterns)
```

**Recommendation: install gitleaks for broader coverage.**

The built-in scanner has 46 high-precision patterns. Gitleaks has 150+ patterns and is maintained by a dedicated security team. Install it once and Pipewarden picks it up automatically:

```bash
# macOS
brew install gitleaks

# Linux (download latest binary)
curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_x64.tar.gz | tar -xz
sudo mv gitleaks /usr/local/bin/

# Windows (via winget)
winget install gitleaks

# Verify
gitleaks version
```

Once installed, `pipewarden` will print `secrets:gitleaks` instead of `secrets:fallback` in the output — no config change needed.

### Scanning Full Git History (Audit Mode)

By default, Pipewarden scans only the **working tree** — files on disk right now. For a thorough audit (e.g. before open-sourcing a private repo), you can tell Pipewarden to scan the **entire git history**:

```toml
# .pipewarden.toml
[secrets]
scan_history = true    # uses gitleaks detect over full git history; requires gitleaks
```

Or from the CLI:
```bash
pipewarden --only secrets   # while scan_history = true in config
```

> **Requires gitleaks.** History scanning uses `gitleaks detect` without `--source` — it reads the git log directly. The built-in regex fallback does not support history mode.
>
> **Slower.** On large repositories with thousands of commits, this can take several minutes. Use it for one-time audits, not on every commit.

```console
✓ secrets:gitleaks(history) (34.2s)   ← scanned full git history, no secrets
✗ secrets:gitleaks(history)  (8.1s)   ← credential found in commit abc1234 — rotate it
```

### What the Built-in Scanner Detects

46 high-precision patterns — no noisy keyword matching.

**Cloud provider credentials**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `aws.access_key` | 🔴 CRITICAL | AWS IAM Access Key ID | `AKIA` + 16 chars |
| `aws.secret_key` | 🔴 CRITICAL | AWS Secret Access Key | `aws_secret_access_key = ...` |
| `aws.sts_key` | 🟠 HIGH | AWS STS / temporary key | `ASIA` + 16 chars |
| `google.api_key` | 🟠 HIGH | Google API Key | `AIza` + 35 chars |

**Version control & CI tokens**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `github.pat_classic` | 🔴 CRITICAL | GitHub Personal Access Token | `ghp_` + 36 chars |
| `github.pat_fine_grained` | 🔴 CRITICAL | GitHub Fine-Grained PAT | `github_pat_` + 82 chars |
| `github.oauth` | 🔴 CRITICAL | GitHub OAuth Token | `gho_` + 36 chars |
| `github.actions_token` | 🔴 CRITICAL | GitHub Actions Runner Token | `ghs_` + 36 chars |
| `github.user_token` | 🔴 CRITICAL | GitHub User-to-Server Token | `ghu_` + 36 chars |
| `gitlab.pat` | 🔴 CRITICAL | GitLab Personal Access Token | `glpat-` + 20 chars |
| `digitalocean.token` | 🔴 CRITICAL | DigitalOcean Personal Token | `dop_v1_` + 64 chars |
| `linear.api_key` | 🟠 HIGH | Linear API Key | `lin_api_` + 40 chars |
| `okta.token` | 🟠 HIGH | Okta SSWS API Token | `SSWS ` + 42 chars |

**Database connection strings (URI format)**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `mongodb.connection_string` | 🔴 CRITICAL | MongoDB URI with credentials | `mongodb://HOST/DB` (with user:pass) |
| `postgres.connection_string` | 🔴 CRITICAL | PostgreSQL URI with credentials | `postgresql://` + user:pass + `@host` |
| `mysql.connection_string` | 🔴 CRITICAL | MySQL URI with credentials | `mysql://` + user:pass + `@host` |
| `redis.connection_string` | 🔴 CRITICAL | Redis URI with password | `redis://` + `:password@host` |
| `mssql.connection_string` | 🔴 CRITICAL | SQL Server ADO.NET connection string | `Server=…;Password=…` |
| `jdbc.connection_string` | 🔴 CRITICAL | JDBC URL with password param | `jdbc:…://…?password=…` |
| `amqp.connection_string` | 🟠 HIGH | AMQP / RabbitMQ URI with credentials | `amqp://` + user:pass + `@host` |

**Azure connection strings**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `azure.storage_connection_string` | 🔴 CRITICAL | Azure Storage Account Key | `DefaultEndpointsProtocol=…;AccountKey=…` |
| `azure.cosmos_connection_string` | 🔴 CRITICAL | Azure Cosmos DB Account Key | `AccountEndpoint=…;AccountKey=…` |
| `azure.servicebus_connection_string` | 🔴 CRITICAL | Azure Service Bus / Event Hubs SAS Key | `Endpoint=sb://…;SharedAccessKey=…` |

**AI / ML service API keys**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `anthropic.api_key` | 🔴 CRITICAL | Anthropic API Key | `sk-ant-` + 40 chars |
| `openai.api_key` | 🔴 CRITICAL | OpenAI API Key (classic) | `sk-` + 48 chars |
| `openai.api_key_project` | 🔴 CRITICAL | OpenAI Project API Key | `sk-proj-` + 100 chars |
| `huggingface.token` | 🔴 CRITICAL | Hugging Face User Access Token | `hf_` + 34 chars |
| `replicate.token` | 🟠 HIGH | Replicate API Token | `r8_` + 37 chars |

**Payment & e-commerce**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `stripe.live_key` | 🔴 CRITICAL | Stripe Live Secret Key | `sk_live_` + 24 chars |
| `shopify.access_token` | 🔴 CRITICAL | Shopify Admin API Token | `shpat_` + 32 chars |
| `shopify.storefront_token` | 🔴 CRITICAL | Shopify Storefront Token | `shpss_` + 32 chars |
| `shopify.custom_app_token` | 🔴 CRITICAL | Shopify Custom App Token | `shpca_` + 32 chars |
| `stripe.restricted` | 🟠 HIGH | Stripe Restricted Key | `rk_live_` + 24 chars |
| `stripe.webhook_secret` | 🟠 HIGH | Stripe Webhook Signing Secret | `whsec_` + 32 chars |
| `stripe.test_key` | 🟡 MEDIUM | Stripe Test Secret Key | `sk_test_` + 24 chars |

**Communication & messaging**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `slack.token` | 🟠 HIGH | Slack Bot/App Token | `xox[abprs]-...` |
| `sendgrid.api_key` | 🟠 HIGH | SendGrid API Key | `SG.` + 22 + `.` + 43 chars |
| `twilio.account_sid` | 🟠 HIGH | Twilio Account SID | `AC` + 32 hex chars |
| `telegram.bot_token` | 🟠 HIGH | Telegram Bot Token | `12345678:AA` + 33 chars |

**Package registries & private keys**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `private_key.pem` | 🔴 CRITICAL | PEM Private Key Block | `-----BEGIN … PRIVATE KEY-----` |
| `npm.token` | 🟠 HIGH | npm Automation Token | `npm_` + 36 chars |
| `pypi.api_token` | 🟠 HIGH | PyPI API Token | `pypi-` + 64 chars |

**Cloud infrastructure & observability**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `databricks.token` | 🟠 HIGH | Databricks Personal Token | `dapi` + 32 hex chars |
| `hashicorp.vault_token` | 🟠 HIGH | HashiCorp Vault Service Token | `hvs.` + 24 chars |
| `newrelic.license_key` | 🟠 HIGH | New Relic License Key | `NRAK-` + 32 hex chars |

**Auth tokens**

| Rule ID | Severity | What It Finds | Example Pattern |
|---------|----------|---------------|-----------------|
| `jwt` | 🟡 MEDIUM | JSON Web Token | `eyJ…eyJ…` (3-part) |

### Severity Levels Explained

| Severity | Meaning | Action Required |
|----------|---------|-----------------|
| 🔴 **CRITICAL** | Credential gives direct access to a service | Rotate immediately. Assume compromised. |
| 🟠 **HIGH** | Token with significant scope | Rotate within hours. Audit access logs. |
| 🟡 **MEDIUM** | Low-impact credential or possible false positive | Review and rotate if real. |
| 🔵 **INFO** | Informational finding | Review at your discretion. |

### Smart Allowlisting

Sometimes you have known test fixtures or documentation examples that look like secrets. Allowlist them:

```toml
# .pipewarden.toml
[secrets]
# Skip specific files or folders — supports ** glob (like gitignore)
allowlist_paths = [
    "tests/fixtures/**",   # everything under tests/fixtures/
    "docs/examples/**",   # everything under docs/examples/
    "*.md",               # all markdown files at root
]

# Skip a specific rule everywhere
allowlist_rules = ["jwt"]

# Ignore a specific known-safe string (e.g. AWS docs example key)
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]
```

> **`**` glob patterns work correctly.** `tests/fixtures/**` matches `tests/fixtures/api_keys.py`, `tests/fixtures/sub/data.json`, etc. This uses a full gitignore-compatible glob compiler — not plain `fnmatch`.

### Understanding the Findings Output

When a secret is found, the output looks like this:

```
  CRITICAL  src/config.py:14  [aws.access_key]  AKIA…WXYZ
  │          │                  │                 │
  │          │                  │                 └─ Truncated snippet — first 4 and last 4 chars
  │          │                  │                    (never printed in full — safe to share in logs)
  │          │                  └─ Rule ID that matched
  │          └─ File path : line number
  └─ Severity level
```

**The snippet is always truncated** — `AKIA…WXYZ` means the actual value starts with `AKIA` and ends with `WXYZ`. This is intentional: the finding is logged safely without exposing the full credential in CI logs.

**What to do:** locate the file + line shown, look at the actual content in your editor to confirm it is real, then rotate it immediately (see next section).

### What Is NOT Scanned

To keep scans fast and accurate, the following are automatically skipped:

- Binary files (images, PDFs, compiled binaries, archives)
- Build output directories (`dist/`, `build/`, `target/`, `node_modules/`)
- VCS directories (`.git/`, `.svn/`)
- Cache directories (`__pycache__/`, `.mypy_cache/`, `.ruff_cache/`)
- Files larger than 1 MB (configurable)

---

## 🚨 What To Do When Secrets Are Found

Pipewarden exits with code `4` when secrets are detected. Here is exactly what to do.

### Step 1 — Do NOT push

If you found the secret **before pushing**, the credential is still local. Do not push until after you have removed it.

If you already pushed, assume the credential is **compromised** — it may have been scraped by bots within minutes of appearing on GitHub. Proceed to Step 2 immediately.

### Step 2 — Rotate the credential NOW

Go to the service dashboard and revoke the exposed key. Rotation guides for common credentials:

| Rule ID | Where to rotate |
|---------|----------------|
| `aws.access_key` / `aws.secret_key` | AWS Console → IAM → Users → Security credentials → Deactivate + delete |
| `github.pat_classic` / `github.pat_fine_grained` | GitHub → Settings → Developer settings → Personal access tokens → Delete |
| `github.actions_token` / `github.user_token` | GitHub → Settings → Developer settings → Delete and regenerate |
| `openai.api_key` / `openai.api_key_project` | OpenAI → platform.openai.com → API keys → Delete |
| `anthropic.api_key` | Anthropic → console.anthropic.com → API keys → Delete |
| `stripe.live_key` / `stripe.restricted` | Stripe → Dashboard → Developers → API keys → Roll key |
| `mongodb.connection_string` | Change the database user password via your cloud provider |
| `postgres.connection_string` | `ALTER USER username WITH PASSWORD 'new-password';` |
| `azure.storage_connection_string` | Azure Portal → Storage Account → Access keys → Rotate |
| `azure.cosmos_connection_string` | Azure Portal → Cosmos DB → Keys → Regenerate |
| `slack.token` | Slack API → Your Apps → OAuth & Permissions → Revoke |
| `sendgrid.api_key` | SendGrid → Settings → API Keys → Delete |
| `shopify.access_token` | Shopify Partners → Apps → Regenerate credentials |
| `huggingface.token` | HuggingFace → Settings → Access Tokens → Delete |
| `digitalocean.token` | DigitalOcean → API → Personal access tokens → Delete |

**Do not just delete the file** — the credential is still in git history. See Step 4.

### Step 3 — Remove the Secret From Your Code

Replace the hardcoded value with an environment variable:

```python
# Before (dangerous)
db_password = "Secr3t!"

# After (safe)
import os
db_password = os.environ["DB_PASSWORD"]
```

Or use a secrets manager:

```python
# AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, etc.
db_password = get_secret("prod/db/password")
```

### Step 4 — Clean Git History

If the secret was ever committed (even if since deleted from the file), it is still in git history. Remove it:

```bash
# Option A — rewrite history (if not yet pushed, or you can force-push)
git filter-repo --path src/config.py --invert-paths   # removes the file entirely
# OR to scrub a specific string:
git filter-repo --replace-text <(echo 'ACTUAL_SECRET==>REMOVED')

# Option B — for small teams with simple history
pip install git-filter-repo
git filter-repo --string-callback 'return line.replace(b"ACTUAL_SECRET", b"REMOVED")'
```

> If the commit was pushed to GitHub, contact GitHub Support to purge the cached versions from their servers after you've rewritten history.

### Step 5 — Add to Allowlist (if it was a false positive)

If the "secret" was actually a test fixture or documentation example:

```toml
# .pipewarden.toml
[secrets]
# Allowlist the specific file
allowlist_paths = ["tests/fixtures/**"]

# OR allowlist the specific known-safe string
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]

# OR disable the rule entirely (use sparingly)
allowlist_rules = ["jwt"]
```

### Step 6 — Verify the Fix

```bash
pipewarden --only secrets
# Should print: scanned N files, no secrets
# Exit code should be 0
```

### Setting Up Alerts for Exit Code 4

In CI, you can trigger a special alert when exit code `4` is returned (secrets found):

```bash
# Bash / GitHub Actions
pipewarden --sarif-out report.sarif
if [ $? -eq 4 ]; then
  echo "::error::CREDENTIAL LEAK DETECTED — rotate immediately"
  # Send Slack/PagerDuty alert here
fi
```

```yaml
# GitHub Actions — separate step that only runs on secrets failure
- name: Run Pipewarden
  id: pipewarden
  run: pipewarden --sarif-out report.sarif
  continue-on-error: true

- name: Alert on credential leak
  if: steps.pipewarden.outcome == 'failure'
  run: echo "Check SARIF report for leaked credentials"
```

---

## 📊 Reading the Output

### The Four Status Icons

Every step in the summary ends with one of four icons:

```
✓  passed   — The step ran and succeeded. Nothing to worry about.

✗  failed   — The step ran and found a problem. Exit code becomes 1.
               The full output of the failing command is printed below
               the summary so you can see exactly what went wrong.

⚠  warned   — Something went wrong but it was not critical.
               Usually means an optional tool (mypy, hadolint) was
               not installed. Does NOT fail the pipeline.

·  skipped  — This stage does not apply to your project.
               (e.g. no Dockerfile found → docker stage skipped)
```

### Understanding the Summary Table

```
  ✓ py:lint(ruff)        passed      0.3s
  ✗ py:test(pytest)      failed      6.2s   exit 1
  ⚠ py:typecheck(mypy)   warned      0.0s   mypy not installed in the project
  · docker               skipped     0.0s   disabled in config/flags
  │         │            │           │      │
  │         │            │           │      └─ Extra message (error or info)
  │         │            │           └─ How long the step took
  │         │            └─ Pass / Fail / Warn / Skip
  │         └─ Step name (stage:tool)
  └─ Status icon
```

### When Something Fails

The tool automatically prints the last 60 lines of output from every failing step — no need to scroll through raw logs:

```
Failing step output (tail):

── py:test(pytest) ──
FAILED tests/test_auth.py::test_login - AssertionError: Expected 200, got 401
FAILED tests/test_auth.py::test_logout - AssertionError: Expected 204, got 500
2 failed, 47 passed in 12.3s
```

You see exactly which tests failed and why, directly in the pipeline output.

### Stage Failed — What To Do

Use this table when you see a `✗` in the summary:

| Stage / Step | What failed | Immediate action |
|---|---|---|
| `secrets:fallback` or `secrets:gitleaks` | A credential pattern was found in your files | **Exit code 4.** See [What To Do When Secrets Are Found](#-what-to-do-when-secrets-are-found). Rotate the credential NOW. |
| `py:deps` / `node:deps` / `go:deps` / `rust:deps` / `dotnet:restore` | Dependency installation failed | Read the error tail — look for a missing package, bad credentials, or network timeout. Check your lockfile is committed. |
| `py:lint(ruff)` | Python lint errors | Run `ruff check --fix .` to auto-fix many issues, then `ruff check .` to see what remains. |
| `py:typecheck(mypy)` | Type errors | Read the error output — each line shows the file, line, and exactly what type mismatch was found. Fix the type annotations. |
| `py:test(pytest)` | Test failures | Read the failure output — each `FAILED` line shows which test and why. Run `pytest -x` locally to stop at the first failure and debug interactively. |
| `node:lint` | ESLint / prettier errors | Run `npm run lint -- --fix` to auto-fix, then re-run. |
| `node:test` | JavaScript test failures | Run `npm test` locally to see the full output. Check which test function failed and why. |
| `node:build` | Build compilation error | Run `npm run build` locally with `--verbose` to see the full webpack / tsc / vite output. |
| `dotnet:format` | Code formatting violations | Run `dotnet format` locally to rewrite files. Check in the formatted files, then re-run. |
| `dotnet:build` | C# compilation error | The full compiler error (file, line, error code) is printed. Fix the type or namespace error shown. |
| `dotnet:test` | .NET test failures | The failing test name and assertion mismatch is shown. Run `dotnet test --filter "TestName"` locally to isolate. |
| `dotnet:vulns` | Vulnerable NuGet package | Upgrade the affected package to the version shown. Check for breaking changes in the NuGet release notes. |
| `docker:scan(trivy)` or `docker:scan(grype)` | Container image CVE | Upgrade the base image or the affected OS/app package. Use `trivy image --severity HIGH,CRITICAL <tag>` locally for details. |
| `go:vet` | Go vet warnings | Fix the reported issue — `go vet` catches real bugs (unreachable code, format string mismatches, etc.). |
| `go:test` | Go test failures | Run `go test ./... -v -run TestName` locally to debug. |
| `rust:lint` (clippy) | Clippy warnings | Run `cargo clippy --fix` to auto-fix many lints. Remaining lints are shown with the fix suggestion inline. |
| `rust:test` | Rust test failures | Run `cargo test -- --nocapture TestName` to see the full output with `println!` output visible. |
| `docker:lint(hadolint)` | Dockerfile best-practice violation | The rule ID and explanation is printed (e.g. `DL3008: Pin versions in apt get install`). See hadolint.github.io for the fix. |
| `docker:build` | Docker build error | The full `docker build` output is printed. Usually a missing file, bad base image, or failed `RUN` command. |
| `vulns:pip-audit` / `vulns:npm-audit` etc. | Known CVE in a dependency | Upgrade the affected package to the version shown in the finding. See [vulnerability action guide](#what-to-do-when-a-vulnerability-is-found). |

### Exit Codes — The Contract With Your CI

```
Exit Code  Meaning
─────────────────────────────────────────────────────────
    0      Everything passed (or was skipped).
           CI should go green. Safe to merge / deploy.

    1      One or more non-secrets stages failed
           (test failure, build error, lint error, etc.).
           CI should go red. Block the merge. Fix the issue.

    2      Bad CLI usage (unknown flag, invalid argument).
           Usually a configuration error in your workflow file.

    3      Bad .pipewarden.toml file (unknown key, wrong type).
           Fix your config file.

    4      The secrets stage specifically found exposed credentials.
           Rotate the secret immediately. Assume it is compromised.
           In CI scripts, check for exit code 4 to trigger an alert.

  130      Interrupted (Ctrl-C).
           The run was cancelled mid-flight.
```

**Why is there a separate exit code for secrets?** This lets CI scripts distinguish "a test failed" (code 1) from "a credential was leaked" (code 4) and trigger different responses — for example, paging an on-call security engineer only for code 4:

```bash
pipewarden
exit_code=$?
if [ $exit_code -eq 4 ]; then
  echo "🚨 CREDENTIAL LEAK DETECTED — paging security" | slack-notify
fi
```

---

## 📄 Reports — SARIF, JUnit XML, JSON, Markdown

Pipewarden can generate four machine-readable report formats simultaneously. These are designed to integrate with the dashboards and UIs your team already uses.

### SARIF — Security Findings in GitHub / Azure DevOps

```bash
pipewarden --sarif-out report.sarif
```

**What is SARIF?**
SARIF (Static Analysis Results Interchange Format) is the industry standard format for security and code analysis findings. GitHub, Azure DevOps, and many other platforms can read it.

**What it contains:**
- Every secret finding with file path, line number, and column
- Severity level (error / warning / note)
- Rule ID and description
- A unique fingerprint for deduplication

**How to read it in GitHub:**
After uploading to GitHub Code Scanning, findings appear under **Security → Code scanning alerts**:

```
⚠ aws.access_key — possible aws.access_key
  src/config.py, line 14
  Severity: Critical
  [Dismiss]  [Create issue]
```

Each alert can be dismissed with a reason, assigned to a team member, or linked to a tracking issue. It works exactly like a commercial SAST tool — for free.

### JUnit XML — Test Results in CI Dashboards

```bash
pipewarden --junit-out junit.xml
```

**What is JUnit XML?**
Every major CI system (GitHub Actions, GitLab, Jenkins, CircleCI, Azure DevOps) can parse JUnit XML and display test results as a structured report.

**What it contains:**
- One test case per pipeline step
- Pass / fail status with timing
- Failure message and output tail for failed steps
- Total counts (passed, failed, skipped)

**How to read it in GitLab:**
Merge requests automatically show a test results panel:

```
Test results for this pipeline:   ✓ 8 passed   ✗ 1 failed   · 2 skipped
  ✗ py:test(pytest) — 2 assertions failed (see details)
```

### JSON — For Custom Integrations

```bash
pipewarden --json
```

Outputs a structured JSON document to stdout (suppresses all pretty output):

```json
{
  "root": "/home/alice/my-app",
  "tool_version": "1.0.0",
  "timestamp": "2026-05-16T14:23:01",
  "detected": ["python", "node(npm)", "docker(Dockerfile)"],
  "duration_s": 61.4,
  "summary": {
    "total": 10,
    "passed": 10,
    "failed": 0,
    "warned": 0,
    "skipped": 0
  },
  "steps": [
    {
      "name": "secrets:fallback",
      "status": "passed",
      "duration_s": 0.1,
      "returncode": 0,
      "message": "scanned 34 files, no secrets",
      "findings": []
    }
  ]
}
```

Use this for:
- Feeding results into a custom Slack notification
- Storing quality metrics in a time-series database
- Building a custom quality dashboard
- Automated triage scripts

### Markdown Summary — For GitHub Step Summaries

```bash
pipewarden --markdown-out summary.md
# or pipe directly to GitHub's step summary:
pipewarden --markdown-out "$GITHUB_STEP_SUMMARY"
```

Produces a rich Markdown table showing every step's status, duration, and all findings. When written to `$GITHUB_STEP_SUMMARY` in GitHub Actions, it appears as a formatted panel on the workflow run page — no extra upload step needed.

```yaml
- name: Run Pipewarden
  run: pipewarden --markdown-out "$GITHUB_STEP_SUMMARY" --sarif-out report.sarif
```

### GitHub Actions Inline Annotations — PR Diff Comments

```bash
pipewarden --gh-annotations
```

Prints GitHub Actions workflow commands to stdout. The runner picks them up and shows findings as **inline comments directly on the PR diff** — exactly where the secret or issue was introduced:

```
::error file=src/config.py,line=14,col=7,title=aws.access_key::possible aws.access_key
```

No extra upload. No separate action. The annotations appear immediately on the changed lines.

---

## 🔧 Configuration Reference

Drop a `.pipewarden.toml` file at the root of your repository to customise behaviour. **All keys are optional** — the defaults work out of the box.

```toml
# .pipewarden.toml
# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL SETTINGS
# ─────────────────────────────────────────────────────────────────────────────

# Stop on the first failure instead of collecting all failures.
# Useful when debugging: you see one clear error instead of a wall of text.
fail_fast = false

# Docker image tag used when building. Override to match your project's tag.
docker_tag = "pipewarden-local:latest"

# Run ONLY these stages (all others are skipped).
# Useful for: pipewarden --only secrets,python
only = []

# Always skip these stages.
skip = []


# ─────────────────────────────────────────────────────────────────────────────
# STAGE TOGGLES
# Turn individual language stages on or off permanently.
# ─────────────────────────────────────────────────────────────────────────────
[stages]
python   = true
node     = true
dotnet   = true
go       = true
rust     = true
docker   = true    # Set to false if you have no Docker daemon in your CI
vulns    = true    # Dependency vulnerability scanning (optional tools)
outdated = false   # Cross-language outdated package check (non-blocking — never fails pipeline)


# ─────────────────────────────────────────────────────────────────────────────
# TIMEOUTS
# Every subprocess has a timeout. These are generous defaults.
# Increase them if your project has slow tests or large dependency trees.
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
enabled         = true    # Set to false to skip secret scanning entirely
prefer_external = true    # Use gitleaks if installed (recommended)
max_file_bytes  = 1000000 # Skip files larger than this (1 MB)
max_files       = 10000   # Stop after scanning this many files
scan_history    = false   # Scan full git history with gitleaks (slower, for audits)

# Skip these paths (fnmatch glob patterns, relative to repo root)
allowlist_paths = [
    # "tests/fixtures/**",
    # "docs/examples/**",
]

# Skip these rule IDs from the built-in scanner
allowlist_rules = [
    # "jwt",
]

# Ignore these exact strings wherever they appear
allowlist_strings = [
    # "AKIAIOSFODNN7EXAMPLE",   # AWS docs dummy key
]


# ─────────────────────────────────────────────────────────────────────────────
# .NET PIPELINE CONTROL
# Fine-grained control over which steps run inside the dotnet stage.
# These are separate from [stages].dotnet — they control steps WITHIN the stage.
# ─────────────────────────────────────────────────────────────────────────────
[dotnet]
# dotnet format --verify-no-changes: fail if any file needs reformatting.
# Set to false for legacy projects without .editorconfig.
format = true

# dotnet list package --vulnerable --include-transitive:
# check NuGet packages against the GitHub Advisory Database.
vulns = true

# dotnet list package --outdated: report available upgrades.
# Never fails the pipeline (always WARNED). Set to true to see upgrade hints.
outdated = false


# ─────────────────────────────────────────────────────────────────────────────
# RETRY (for flaky network-dependent steps)
# Applies to: pip install, npm ci, cargo fetch, go mod download, pip-audit…
# ─────────────────────────────────────────────────────────────────────────────
[retry]
attempts     = 0    # 0 = disabled. Max 5. Retries on transient failures only.
backoff_base = 2.0  # Seconds before first retry; doubles each attempt (2s, 4s, 8s…)


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
[output]
color = true    # Set to false in environments without ANSI support
quiet = false   # Set to true to suppress all pretty output (use with --json)
```

### Config Validation

The config file is **strictly validated**. If you type an unknown key, you get an immediate error:

```
config error: unknown key: pipewarden.stagess
```

This is intentional — typos fail loudly rather than being silently ignored.

---

## 🌐 Environment Variable Overrides

You can override any configuration value with a `PIPEWARDEN_*` environment variable. This is useful in CI systems where you cannot edit the TOML file.

**Priority order (highest wins):** CLI flags > env vars > `.pipewarden.toml` > built-in defaults.

| Environment Variable | Equivalent Config | Example |
|---------------------|-------------------|---------|
| `PIPEWARDEN_FAIL_FAST=1` | `fail_fast = true` | Stop on first failure |
| `PIPEWARDEN_SKIP=docker,vulns` | `skip = ["docker", "vulns"]` | Skip stages by name |
| `PIPEWARDEN_ONLY=secrets,python` | `only = ["secrets", "python"]` | Run only these stages |
| `PIPEWARDEN_TIMEOUT_TEST_S=2400` | `timeouts.test_s = 2400` | 40-min test timeout |
| `PIPEWARDEN_TIMEOUT_INSTALL_S=1800` | `timeouts.install_s = 1800` | 30-min install timeout |
| `PIPEWARDEN_TIMEOUT_BUILD_S=1200` | `timeouts.build_s = 1200` | 20-min build timeout |
| `PIPEWARDEN_TIMEOUT_SCAN_S=300` | `timeouts.scan_s = 300` | 5-min scan timeout |
| `PIPEWARDEN_TIMEOUT_DEFAULT_S=300` | `timeouts.default_s = 300` | 5-min default timeout |
| `PIPEWARDEN_NO_COLOR=1` | `output.color = false` | Disable ANSI colours |
| `PIPEWARDEN_QUIET=1` | `output.quiet = true` | Suppress pretty output |
| `PIPEWARDEN_RETRY_ATTEMPTS=3` | `retry.attempts = 3` | Retry up to 3 times |
| `PIPEWARDEN_RETRY_BACKOFF=5` | `retry.backoff_base = 5.0` | 5-second initial backoff |

**Example — GitHub Actions with env var overrides:**

```yaml
- name: Run Pipewarden
  env:
    PIPEWARDEN_SKIP: docker       # No Docker daemon on this runner
    PIPEWARDEN_RETRY_ATTEMPTS: 3  # Retry flaky network steps
    PIPEWARDEN_TIMEOUT_TEST_S: 3600
  run: pipewarden --sarif-out report.sarif
```

---

## 🔄 CI / CD Integration

### GitHub Actions (Inline)

The simplest possible CI setup — copy and paste:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  security-events: write    # Required to upload SARIF to Security tab

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
        run: pipewarden --sarif-out report.sarif --junit-out junit.xml

      - name: Upload security findings to GitHub
        uses: github/codeql-action/upload-sarif@v3
        if: always()   # Upload even if the pipeline failed
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
      junit: junit.xml
    paths:
      - report.sarif
    expire_in: 30 days
```

GitLab automatically renders JUnit results in the merge request sidebar — no extra setup needed.

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
    inputs:
      testResultsFormat: JUnit
      testResultsFiles: '$(Build.ArtifactStagingDirectory)/junit.xml'
    condition: always()
```

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
```

---

## ⚡ GitHub Actions (Official Action)

If your workflow already uses GitHub Actions, there is a dedicated action you can use with a single step:

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

## 🪝 Pre-Commit Hooks

Catch issues **before** code even reaches the remote repository by wiring Pipewarden into your local commit and push workflow.

### Setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gcfernando/pipewarden
    rev: v1.3.0
    hooks:
      - id: pipewarden-secrets     # Runs on every git commit
      - id: pipewarden-diff        # Runs on every git push (changed files only)
      # - id: pipewarden-full      # Full run (use manually: pre-commit run pipewarden-full)
```

```bash
pre-commit install                        # Hook runs on every commit
pre-commit install --hook-type pre-push   # Hook runs on every push
```

### Available Hooks

| Hook ID | When it runs | What it does |
|---------|-------------|--------------|
| `pipewarden-secrets` | Every `git commit` | Scans ALL files for secrets. Fast (~0.1s). |
| `pipewarden-diff` | Every `git push` | Scans only files changed vs `origin/main`. Very fast. |
| `pipewarden-full` | Manual only | Full pipeline: install, lint, test, build, scan. |

### The Workflow With Pre-Commit Hooks

```
Developer writes code
       ↓
git commit
       ↓
[pipewarden-secrets runs automatically]  ← catches AWS keys, tokens, passwords
       ↓  (passes)
Commit created locally
       ↓
git push
       ↓
[pipewarden-diff runs automatically]     ← scans changed files again
       ↓  (passes)
Code reaches remote repository
       ↓
CI runs full pipewarden
       ↓  (passes)
Pull request can be merged
```

No secret ever reaches the server. No broken code is ever deployed.

---

## 📋 CLI Reference

### All Commands

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
  --dry-run            Show which stages would run without executing anything

  --init               Scaffold a .pipewarden.toml in the project root and exit
  --validate           Validate the config file and exit (0 = valid, 3 = error)
  --list-stages        Show which stages are detected and enabled, then exit

  --json               Output JSON report to stdout (no pretty output)
  --sarif-out FILE     Write SARIF 2.1 report (for GitHub Code Scanning)
  --junit-out FILE     Write JUnit XML report (for CI test parsers)
  --markdown-out FILE  Write Markdown summary (use $GITHUB_STEP_SUMMARY for GHA)
  --gh-annotations     Print GitHub Actions inline annotations to stdout
  --log-file FILE      Write verbose debug log to FILE
  --no-color           Disable ANSI colours (for dumb terminals / file output)
  --verbose / -v       Enable verbose logging to stderr
  --docker-tag TAG     Override the Docker image tag for the docker stage

  --version            Print version and exit
  --help               Show this help and exit
```

### Available Stages

```
secrets    Secret scanning (always runs first); full git history scan available via scan_history
vulns      Dependency CVE scan (pip-audit / npm audit / cargo-audit / govulncheck / dotnet list --vulnerable)
outdated   Cross-language outdated package check — non-blocking, informational only
python     Python: venv + install + lint(ruff) + typecheck(mypy) + test(pytest)
node       Node.js: install + lint + typecheck + test + build
dotnet     .NET: restore + format + build + test + vuln scan (steps controlled by [dotnet] config)
go         Go: mod download + vet + build + test
rust       Rust: fetch + clippy + build + test
docker     Docker: hadolint lint + docker build + container scan (trivy/grype, if installed)
```

### Common Usage Patterns

```bash
# Run everything
pipewarden

# Run only secret scanning (fastest — good for pre-commit)
pipewarden --only secrets

# Run only secrets and Python
pipewarden --only secrets --only python

# Skip Docker (no daemon available)
pipewarden --skip docker

# Skip Docker and vuln scanning
pipewarden --skip docker --skip vulns

# Only scan changed files vs main branch
pipewarden --only secrets --diff origin/main

# Stop on first failure (tight feedback loop)
pipewarden --fail-fast

# Preview what would run without executing anything
pipewarden --dry-run

# Scaffold a .pipewarden.toml in the current directory
pipewarden --init

# Validate config file and exit
pipewarden --validate

# List detected and enabled stages
pipewarden --list-stages

# Generate all reports
pipewarden --sarif-out findings.sarif --junit-out results.xml

# Write GitHub Actions step summary
pipewarden --markdown-out "$GITHUB_STEP_SUMMARY"

# Print inline PR annotations (GitHub Actions only)
pipewarden --gh-annotations

# Run against a specific directory
pipewarden --root /path/to/my-project

# Plain text output (no colours)
pipewarden --no-color

# Verbose debug output
pipewarden --verbose

# Use a custom config file
pipewarden --config /path/to/custom.toml
```

---

## 💼 Business Benefits & ROI

### Security Risk Reduction

| Risk | Without Pipewarden | With Pipewarden |
|------|----------------------|---------------------|
| Leaked AWS credentials | Found in production breach, months later | Blocked at commit, seconds after typing |
| Vulnerable dependencies | Discovered in quarterly security audit | Flagged on every PR by pip-audit / npm audit |
| Security findings in logs | Buried in CI output, never triaged | Tracked as GitHub Code Scanning alerts with assignment + dismissal workflow |

**Industry data:** The average cost of a data breach from an exposed credential is $4.45 million (IBM, 2023). Pipewarden prevents the most common source of credential exposure: accidental commits.

### Developer Productivity

| Metric | Impact |
|--------|--------|
| CI setup time for new project | Reduced from hours to minutes |
| Onboarding new engineers | No "how does our CI work?" question — it's always `pipewarden` |
| Context switching | Developers see failures in the same format regardless of language |
| Debugging failed pipelines | Last 60 lines printed automatically — no log archaeology |

### Operational Benefits

| Benefit | Detail |
|---------|--------|
| Zero maintenance | No bespoke CI scripts to maintain per project. Update one tool, all projects benefit. |
| Cross-platform | Works identically on Linux, macOS, and Windows — local and CI |
| Portable | Works with GitHub Actions, GitLab, Jenkins, Azure DevOps, CircleCI, Bitbucket |
| Offline capable | No network calls at runtime. Works in air-gapped environments. |
| No telemetry | Zero data sent anywhere. Fully private. |

### What Teams Report After Adoption

> *"We went from 12 different CI YAML files across our repositories to one standard tool. Our new engineers ship their first PR on day one instead of day three."*

> *"We caught a Stripe live key in a commit 30 seconds after it was typed. Before Pipewarden, it would have been in our git history for months before anyone noticed."*

> *"SARIF integration means security findings now have owners and SLAs, not just log lines that no one reads."*

---

## ❓ Frequently Asked Questions

**Q: I have no `.pipewarden.toml` file. Will it still work?**
A: Yes. All configuration has sensible defaults. The tool detects your project type automatically and uses best-practice settings. A config file is only needed if you want to override something.

---

**Q: My project uses Python AND Node.js. Which one runs?**
A: Both. Pipewarden detects all languages present and runs each in sequence. The summary shows every step from all languages.

---

**Q: What if I don't have pytest / ruff / mypy installed?**
A: For Python, Pipewarden creates an isolated virtual environment and checks whether pytest is installed inside it. If not, it reports a `warned` step (not a failure) and continues. Optional tools like mypy are only run if you have them installed AND have a config file for them.

---

**Q: Will it delete my existing virtual environment?**
A: No. If a `.pipewarden-venv` folder already exists, it reuses it. It only creates a new one if none exists.

---

**Q: The secret scanner is flagging a test fixture. How do I suppress it?**
A: Add the path to your config:
```toml
[secrets]
allowlist_paths = ["tests/fixtures/**"]
```
Or allowlist the specific string:
```toml
[secrets]
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]
```

---

**Q: Can I run only the secret scanner without running tests?**
A: Yes:
```bash
pipewarden --only secrets
```

---

**Q: My tests take 20 minutes. Can I increase the timeout?**
A: Yes:
```toml
[timeouts]
test_s = 2400   # 40 minutes
```

---

**Q: Does it work in a Docker container / air-gapped environment?**
A: Yes. The tool makes zero network calls at runtime. It only runs local commands (`pip`, `npm`, `cargo`, etc.). Internet access is only needed during installation.

---

**Q: I'm getting `command not found: ruff`. Is that an error?**
A: No. If `ruff` is not on your PATH, the lint step is recorded as `warned` (not failed) and the pipeline continues. Install ruff (`pip install ruff`) to enable linting.

---

**Q: What is the `outdated` stage and how is it different from `vulns`?**
A: The `vulns` stage checks for **known security vulnerabilities** (CVEs) in your current dependencies. The `outdated` stage checks for **newer versions available** regardless of whether they fix a security issue. Outdated results are always `WARNED` — they never fail the pipeline. Enable them with `outdated = true` in `[stages]`.

---

**Q: How is this different from running all the tools manually?**
A: Pipewarden provides:
- **Automatic detection** — you don't need to know which tools apply
- **Consistent output** — one summary format regardless of language
- **Timeouts on every command** — no hanging pipelines
- **Structured reports** — SARIF and JUnit XML for dashboards
- **Secret scanning first** — before any code is installed or run
- **Stable exit codes** — a clear contract with your CI system

---

## 🤝 Contributing

Contributions are welcome! Whether you're fixing a bug, adding support for a new language, or improving documentation.

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and conventions
2. Open an issue to discuss significant changes before implementing
3. Run the test suite before submitting: `pytest && ruff check . && mypy`
4. Security issues must be reported privately — see [SECURITY.md](SECURITY.md)

---

## 📜 License

Licensed under the [MIT License](LICENSE).

You may use, modify, and distribute this software freely, including in commercial products.

---

<div align="center">

<br>

**Built for engineers who'd rather ship features than maintain CI YAML.**

<br>

<sub>No telemetry &nbsp;·&nbsp; No network calls at runtime &nbsp;·&nbsp; Zero runtime dependencies &nbsp;·&nbsp; MIT License</sub>

<br>

⭐ **If Pipewarden saves you time, consider starring the repository.**

<br>

</div>

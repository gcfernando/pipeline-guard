<div align="center">

<br>

# Pipeline Guard

**One command to install, lint, test, build, and scan.**
**Any language. Any repo. Any CI.**

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-D22128?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-71_passing-2EA44F?style=for-the-badge)](#)
[![Type checked](https://img.shields.io/badge/Mypy-strict-1F5082?style=for-the-badge&logo=python&logoColor=white)](#)

<br>

</div>

> You know the drill. New repo, new CI YAML. You write the same script you wrote last time:
> install deps, lint, test, build, scan for secrets. Different language, different
> package manager, same five steps. **You've written that script forty times.**
>
> Pipeline Guard is that script, written once, for everyone.

<br>

## See it in action

```console
$ cd ~/my-project
$ pipeline-guard

  Pipeline Guard 1.0.0
  ─────────────────────────────────────────────────────────────
  root:     /home/you/my-project
  detected: python, node(npm), docker

  ✓ secrets:fallback     passed     0.0s    scanned 34 files
  ✓ py:venv              passed     2.9s
  ✓ py:deps(pyproject)   passed     2.2s
  ✓ py:lint(ruff)        passed     0.1s
  ✓ py:test(pytest)      passed     1.4s
  ✓ node:lint            passed     3.2s
  ✓ node:test            passed     8.1s
  ✓ node:build           passed     5.7s
  ✓ docker:build         passed    12.4s

  ✓ all 9 steps passed in 36.0s
```

No config. No flags. No setup. The exit code is `0` when things pass and `1` when they
don't — the only contract your CI needs.

<br>

## What it does

```
   1   detect       Reads the folder. Spots Python, Node, Go, Rust, .NET, Docker.
                    Polyglot repos are fine — multiple stages run in sequence.

   2   secrets      Scans every file for AWS keys, GitHub tokens, Stripe live
                    keys, private key blocks, JWTs, and a dozen other patterns.
                    Uses gitleaks if installed; falls back to a built-in regex
                    scanner otherwise.

   3   install      Creates an isolated venv. Respects your lockfile. Picks
                    pip / poetry / uv automatically. Same logic for npm / pnpm
                    / yarn / cargo / go / dotnet.

   4   lint         Runs ruff for Python, clippy for Rust, go vet for Go, your
                    declared `lint` script for Node, hadolint for Dockerfiles.

   5   test         pytest, npm test, cargo test, dotnet test, go test.
                    Whatever fits.

   6   build        cargo build, dotnet build, npm run build, docker build.
                    Skipped if your project has nothing to build.

   ───

   ALWAYS           Every command has a timeout. Failures are collected, not
                    raised. Output is captured for the summary. The exit code
                    is honest.
```

<br>

## Install

```bash
pip install git+https://github.com/gcfernando/pipeline-guard.git@v1.0.0
pipeline-guard --version
# → pipeline-guard 1.0.0
```

> Permission denied?  →  `pip install --user ...`
>
> Externally-managed environment?  →  `pip install --break-system-packages ...`

<br>

## The five commands that matter

Almost everything you'll do with this tool is one of these.

<br>

**Run everything.** This is what CI does.

```bash
pipeline-guard
```

<br>

**Just check for secrets.** Fast. Good as a pre-commit hook.

```bash
pipeline-guard --only secrets
```

<br>

**Only scan files you just changed.** Faster. Good as a pre-push hook.

```bash
pipeline-guard --only secrets --diff main
```

<br>

**Stop on the first failure.** Tighter feedback loop while debugging.

```bash
pipeline-guard --fail-fast
```

<br>

**Generate machine-readable reports** for GitHub Code Scanning and CI test parsers.

```bash
pipeline-guard --sarif-out report.sarif --junit-out junit.xml
```

<br>

## Reading the output

Four icons cover every possible outcome.

| Icon | Status | What it means | Affects exit code |
|:----:|--------|---------------|:------------------:|
| `✓` | **passed** | Step ran and returned zero. | No |
| `✗` | **failed** | Step ran and returned non-zero. | **Yes — exit 1** |
| `⚠` | **warned** | Couldn't run cleanly. Usually a missing optional tool. | No |
| `·` | **skipped** | Stage didn't apply (no Dockerfile, no tests folder, etc.). | No |

When something fails, the tool prints the last 60 lines of the command's output so you
can see exactly what went wrong. No hunting through log files.

<br>

## Configuration

For one-off runs the defaults are fine. For projects you'll run this on for years,
drop a `.pipeline-guard.toml` at the root:

```toml
# Every section is optional. Override only what you need.

fail_fast  = false
docker_tag = "myapp:ci-local"

[stages]
docker = false              # skip the docker stage
vulns  = true               # run dependency vulnerability scans

[timeouts]
install_s = 600
test_s    = 1800

[secrets]
allowlist_paths   = ["tests/fixtures/**"]
allowlist_strings = ["AKIAIOSFODNN7EXAMPLE"]   # AWS's documented dummy key
allowlist_rules   = ["jwt"]
```

The tool is **strict** about unknown keys on purpose — typos error out loudly instead
of being silently ignored. That's a feature.

<br>

## Wire it into CI

This is the whole point. Set it up once, push, and every change is checked from now on.

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]

permissions:
  contents: read
  security-events: write    # so SARIF lands in the Security tab

jobs:
  pipeline-guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install git+https://github.com/gcfernando/pipeline-guard.git@v1.0.0
      - run: pipeline-guard --sarif-out report.sarif --junit-out junit.xml
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with: { sarif_file: report.sarif }
```

Secret findings now appear under **Security → Code scanning** as real GitHub alerts
you can dismiss, triage, and reopen. Like a commercial scanner. For free.

### GitLab CI

```yaml
# .gitlab-ci.yml
pipeline-guard:
  image: python:3.12
  script:
    - pip install git+https://github.com/gcfernando/pipeline-guard.git@v1.0.0
    - pipeline-guard --junit-out junit.xml
  artifacts:
    when: always
    reports:
      junit: junit.xml
```

GitLab auto-renders the JUnit report in the merge request UI.

### Other CI systems

Jenkins, CircleCI, Azure DevOps, Bitbucket Pipelines — all work the same way:
install Python, `pip install` the tool, run it, archive the report. The tool
doesn't care.

<br>

## Pre-commit hook

If your repo uses [pre-commit](https://pre-commit.com), this is two lines of config:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gcfernando/pipeline-guard
    rev: v1.0.0
    hooks:
      - id: pipeline-guard-secrets    # on every commit
      - id: pipeline-guard-diff       # on every push, changed files only
```

```bash
pre-commit install
pre-commit install --hook-type pre-push
```

From now on, no committed secret leaves your laptop.

<br>

## Reference

```
   COMMAND                              MEANING

   pipeline-guard                       run everything in cwd
   pipeline-guard --root PATH           run against a specific folder

   pipeline-guard --only STAGE          run only this stage (repeatable)
   pipeline-guard --skip STAGE          skip a stage (repeatable)
   pipeline-guard --diff REF            scan only files changed vs REF
   pipeline-guard --fail-fast           abort on first failure

   pipeline-guard --json                JSON to stdout, no pretty output
   pipeline-guard --sarif-out FILE      write SARIF 2.1 (for code-scanning)
   pipeline-guard --junit-out FILE      write JUnit XML (for CI parsers)
   pipeline-guard --no-color            plain text, no ANSI codes
   pipeline-guard --version             print version and exit
   pipeline-guard --help                show all flags


   STAGES         secrets · python · node · dotnet · go · rust · docker · vulns

   EXIT CODES     0  all passed                 (or skipped)
                  1  one or more stages failed
                  2  usage error                (bad CLI flags)
                  3  config error               (bad .pipeline-guard.toml)
                130  interrupted                (Ctrl-C)
```

<br>

## Contributing

Bug reports, feature requests, and pull requests are welcome. See
[CONTRIBUTING.md](CONTRIBUTING.md) for setup, test commands, and the conventions
this project follows. Security issues should be reported privately — see
[SECURITY.md](SECURITY.md).

<br>

## License

Licensed under the [Apache License, Version 2.0](LICENSE).

<br>

---

<div align="center">

<br>

**Made for engineers who'd rather ship features than maintain CI YAML.**

<sub>No telemetry · No network calls · Zero runtime dependencies</sub>

<br>

</div>
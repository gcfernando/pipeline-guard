# Contributing

Thanks for considering a contribution!

## Setup

```bash
git clone <repo>
cd pipewarden
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Run the tests

```bash
pytest
ruff check .
mypy
```

All three must pass before a PR is merged. CI enforces this. The suite currently has **160 tests** with ≥ 85 % branch coverage enforced by `pytest --cov --cov-fail-under=80`.

The CI matrix tests against Python 3.10–3.13 and `"3.x"` (always the current latest release) on Linux, macOS, and Windows.

## Conventions

- **No new runtime dependencies.** The single-binary-no-deps story is the product. If you really need a dep, open an issue first.
- **Tests for new behavior.** Bugs get a regression test that fails before your fix and passes after.
- **Subprocess discipline.** Never call `subprocess` outside `runner.py`. Never use `shell=True`. Every command takes a timeout.
- **Stable exit codes.** Don't change them without a major version bump. Current codes: 0 (ok), 1 (non-secrets failure), 2 (usage), 3 (config), 4 (secrets found), 130 (interrupted).
- **Type hints everywhere.** `mypy --strict` must pass.
- **Stage registry.** Every new top-level stage must be added to `ALL_STAGES` in `config.py` and wired into the `STAGES` dict in `stages.py`. Add the stage name to `--init` template in `cli.py`.

## Adding a New Secret Pattern

New patterns live in `src/pipewarden/secrets.py` — the `SECRET_PATTERNS` list.

Each entry is a `(rule_id, Severity, compiled_regex)` tuple. Follow these guidelines:

1. **Use a namespaced rule ID.** Format: `provider.token_type` (e.g. `github.pat_classic`, `aws.access_key`).
2. **Prefer `\b` word boundaries.** Anchors prevent partial matches on longer strings.
3. **Add a real positive test** in `tests/test_secrets.py` — write a fake token that matches and assert `status == Status.FAILED`.
4. **Add a negative test** if the pattern has a common false-positive risk (e.g. Windows auth connection strings for MSSQL).
5. **Choose severity carefully:**
   - `CRITICAL` — direct service access (cloud keys, database URIs with credentials, private keys)
   - `HIGH` — scoped tokens with meaningful access (Slack bots, payment webhooks, monitoring keys)
   - `MEDIUM` — lower-impact or test-only credentials (JWTs, Stripe test keys)
6. **Documentation examples** — if you add examples to `README.md`, split any matching string across a backtick boundary (e.g. `` `scheme://` + credentials + `@host` ``) so the scanner's whitespace stop prevents a false positive during self-scan.
7. **Update `CHANGELOG.md`** — add to the `[Unreleased]` section, with the rule ID and what it detects.

## Adding a New Stage

When adding a new top-level pipeline stage (e.g. a new language or cross-language check):

1. **`src/pipewarden/config.py`** — add the stage name to `ALL_STAGES` and add a toggle to `StageToggles`.
2. **`src/pipewarden/stages.py`** — implement `run_<stage>(root, detected, cfg, results)` and add it to the `STAGES` registry dict.
3. **`src/pipewarden/cli.py`** — add the stage to the `--init` template (`_INIT_TEMPLATE`), `_cmd_list_stages`, and `_cmd_dry_run`.
4. **Tests** — add tests to `tests/test_stages.py` and `tests/test_config.py`. Every new stage needs at least a "runs when detected" and "skipped when not detected" test.
5. **Docs** — update `README.md` (stages diagram, CLI stage list, configuration reference) and add an entry to `CHANGELOG.md`.

## Releasing

Maintainers only. See `docs/release.md`.

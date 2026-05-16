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

All three must pass before a PR is merged. CI enforces this.

## Conventions

- **No new runtime dependencies.** The single-binary-no-deps story is the product. If you really need a dep, open an issue first.
- **Tests for new behavior.** Bugs get a regression test that fails before your fix and passes after.
- **Subprocess discipline.** Never call `subprocess` outside `runner.py`. Never use `shell=True`. Every command takes a timeout.
- **Stable exit codes.** Don't change them without a major version bump.
- **Type hints everywhere.** `mypy --strict` must pass.

## Releasing

Maintainers only. See `docs/release.md`.

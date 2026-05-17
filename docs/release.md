# Release Process

Maintainers only.

## Pre-release Checklist

Before tagging a release, verify everything is green:

```bash
# 1. Run the full test suite with coverage
pytest --cov=src/pipewarden --cov-branch --cov-fail-under=80

# 2. Lint and type-check
ruff check .
mypy

# 3. Verify the tool runs cleanly against itself
pipewarden --validate
pipewarden --list-stages
pipewarden --dry-run

# 4. Check for self-scan false positives
pipewarden --only secrets

# 5. Run the full pipeline against itself (dog-fooding)
pipewarden --root . --skip vulns --junit-out self-junit.xml
```

All five commands must exit with code 0.

## Version Bump

Update the version string in **two places** — they must match exactly:

1. `pyproject.toml` → `version = "X.Y.Z"`
2. `src/pipewarden/__init__.py` → `__version__ = "X.Y.Z"`

Also update the usage examples in `Dockerfile` and `action.yml` that reference the version in their documentation comments.

Verify with:

```bash
python -c "import pipewarden; print(pipewarden.__version__)"
pipewarden --version
```

## Changelog

1. Rename the `[Unreleased]` section at the top of `CHANGELOG.md` to `[X.Y.Z] — YYYY-MM-DD`.
2. Add a new empty `[Unreleased]` section above it for the next cycle.

Format:
```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added
- ...

### Fixed
- ...

### Changed
- ...
```

## PyPI Classifiers

When adding support for a new Python version that has been validated in CI:

1. Add the classifier to `pyproject.toml`:
   ```toml
   "Programming Language :: Python :: 3.15",
   ```
2. The CI matrix picks up new versions automatically via the `"3.x"` sentinel — no matrix changes needed.

## Release Steps

```bash
# 1. Commit the version bump and changelog
git add pyproject.toml src/pipewarden/__init__.py CHANGELOG.md Dockerfile action.yml
git commit -m "chore: release vX.Y.Z"

# 2. Push to main
git push origin main

# 3. Tag the release
git tag vX.Y.Z
git push origin vX.Y.Z
```

The **Publish to PyPI** GitHub Actions workflow (`publish.yml`) triggers automatically on the tag push. It:

1. Builds the source distribution and wheel (`python -m build`)
2. Signs artifacts with Sigstore (via PyPI Trusted Publisher OIDC — no API token stored in secrets)
3. Publishes to PyPI
4. Creates a GitHub Release with the signed artifacts attached

Monitor the workflow run at `https://github.com/gcfernando/pipewarden/actions`.

## Verifying a Release

After the workflow completes, verify the published package:

```bash
# Install from PyPI in a clean venv
python -m venv /tmp/verify-venv
/tmp/verify-venv/bin/pip install pipewarden==X.Y.Z
/tmp/verify-venv/bin/pipewarden --version

# Verify the Sigstore signature
pip install sigstore
python -m sigstore verify pipewarden-X.Y.Z.tar.gz
```

## Versioning Policy

Pipewarden follows [Semantic Versioning](https://semver.org/):

| Change type | Version bump |
|-------------|-------------|
| New stages, new CLI flags, new language support, new secret patterns | MINOR (`1.x.0`) |
| Bug fixes, documentation, performance improvements | PATCH (`1.0.x`) |
| Breaking config schema changes, removed CLI flags, exit code changes | MAJOR (`x.0.0`) |

Exit codes are part of the public API. Never change an existing exit code without a MAJOR bump.

## What Triggers Each Version Bump

| Change | Bump |
|--------|------|
| New secret detection pattern | MINOR |
| New `--flag` added to CLI | MINOR |
| New language stage (e.g. Swift, PHP) | MINOR |
| New step within existing stage (e.g. `dotnet format`) | MINOR |
| New config key in `.pipewarden.toml` | MINOR |
| Bug fix in existing behavior | PATCH |
| Docs / comments / test improvements | PATCH |
| Removing a CLI flag or config key | MAJOR |
| Changing an exit code's meaning | MAJOR |
| Renaming a stage | MAJOR |

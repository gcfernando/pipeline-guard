# Release Process

Maintainers only.

## Steps

1. Update `version` in `pyproject.toml` and `src/pipeline_guard/__init__.py` to the new version.
2. Add a section to `CHANGELOG.md` for the new version.
3. Commit: `git commit -m "chore: release vX.Y.Z"`
4. Push to main: `git push origin main`
5. Tag the release: `git tag vX.Y.Z && git push origin vX.Y.Z`

The `release` GitHub Actions workflow triggers automatically on the tag push, builds the package, signs artifacts with Sigstore, publishes to PyPI, and creates a GitHub Release.

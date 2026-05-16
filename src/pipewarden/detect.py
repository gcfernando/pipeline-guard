"""Project type detection. Pure: takes a Path, returns a Detection."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Detection:
    python: bool = False
    node: bool = False
    dotnet: bool = False
    go: bool = False
    rust: bool = False
    docker: bool = False

    has_pyproject: bool = False
    has_requirements: bool = False
    has_poetry_lock: bool = False
    has_uv_lock: bool = False
    has_setup_py: bool = False

    node_pm: str = "npm"   # npm | pnpm | yarn
    has_package_lock: bool = False
    has_pnpm_lock: bool = False
    has_yarn_lock: bool = False

    dockerfile_name: str = "Dockerfile"

    def labels(self) -> list[str]:
        out: list[str] = []
        if self.python:
            out.append("python")
        if self.node:
            out.append(f"node({self.node_pm})")
        if self.dotnet:
            out.append("dotnet")
        if self.go:
            out.append("go")
        if self.rust:
            out.append("rust")
        if self.docker:
            out.append(f"docker({self.dockerfile_name})")
        return out


def detect(root: Path) -> Detection:
    """Inspect `root` for project-type markers."""
    d = Detection()

    # Python
    d.has_pyproject    = (root / "pyproject.toml").is_file()
    d.has_requirements = (root / "requirements.txt").is_file()
    d.has_poetry_lock  = (root / "poetry.lock").is_file()
    d.has_uv_lock      = (root / "uv.lock").is_file()
    d.has_setup_py     = (root / "setup.py").is_file()
    d.python = any([d.has_pyproject, d.has_requirements,
                    d.has_poetry_lock, d.has_uv_lock, d.has_setup_py])

    # Node
    d.has_package_lock = (root / "package-lock.json").is_file()
    d.has_pnpm_lock    = (root / "pnpm-lock.yaml").is_file()
    d.has_yarn_lock    = (root / "yarn.lock").is_file()
    d.node = (root / "package.json").is_file()
    if d.node:
        if d.has_pnpm_lock:
            d.node_pm = "pnpm"
        elif d.has_yarn_lock:
            d.node_pm = "yarn"
        else:
            d.node_pm = "npm"

    # .NET — search shallow first, then one level deep (common for solutions)
    d.dotnet = bool(
        list(root.glob("*.sln")) or list(root.glob("*.csproj"))
        or list(root.glob("*/*.csproj"))
    )

    # Go / Rust
    d.go   = (root / "go.mod").is_file()
    d.rust = (root / "Cargo.toml").is_file()

    # Docker / Containerfile
    if (root / "Dockerfile").is_file():
        d.docker = True
        d.dockerfile_name = "Dockerfile"
    elif (root / "Containerfile").is_file():
        d.docker = True
        d.dockerfile_name = "Containerfile"

    return d

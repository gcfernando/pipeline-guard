"""CLI entry point. Parses args, loads config, runs stages, writes reports."""
from __future__ import annotations

import argparse
import logging
import signal
import sys
import time
from io import TextIOWrapper
from pathlib import Path

from . import __version__
from .config import ALL_STAGES, ConfigError, PipelineConfig, find_config_file, load_config
from .detect import detect
from .printer import Printer, print_summary
from .reporters import to_json, to_junit_xml, to_sarif
from .secrets import scan_secrets
from .stages import STAGES
from .types import Report, Status, StepResult

log = logging.getLogger("pipeline_guard")


# ---------------------------------------------------------------------------
# Exit codes — stable, documented.
# ---------------------------------------------------------------------------
EXIT_OK          = 0
EXIT_FAILURES    = 1
EXIT_USAGE       = 2
EXIT_CONFIG      = 3
EXIT_INTERRUPTED = 130


class _FailFast(Exception):
    """Used to abort the run loop when --fail-fast is set."""


def _setup_logging(log_path: str | None, verbose: bool) -> None:
    handlers: list[logging.Handler] = []
    if log_path:
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    if verbose:
        handlers.append(logging.StreamHandler(sys.stderr))
    if not handlers:
        handlers.append(logging.NullHandler())
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="pipeline-guard",
        description="Detect, install, lint, test, build, scan — locally or in CI.",
    )
    p.add_argument("--version", action="version", version=f"pipeline-guard {__version__}")
    p.add_argument("--root", type=Path, default=Path.cwd(),
                   help="project root (default: cwd)")
    p.add_argument("--config", type=Path, default=None,
                   help="path to a .pipeline-guard.toml (default: auto-discovered)")
    p.add_argument("--skip", action="append", default=[], choices=ALL_STAGES,
                   help="skip a stage (repeatable)")
    p.add_argument("--only", action="append", default=[], choices=ALL_STAGES,
                   help="run only these stages (repeatable)")
    p.add_argument("--fail-fast", action="store_true",
                   help="abort on first failure")
    p.add_argument("--json", dest="json_to_stdout", action="store_true",
                   help="emit JSON report on stdout (suppresses pretty output)")
    p.add_argument("--sarif-out", type=Path, default=None,
                   help="write SARIF 2.1 file (for GitHub Code Scanning etc.)")
    p.add_argument("--junit-out", type=Path, default=None,
                   help="write JUnit XML file (for CI test parsers)")
    p.add_argument("--log-file", type=Path, default=None,
                   help="write debug log to this file")
    p.add_argument("--no-color", action="store_true", help="disable colored output")
    p.add_argument("--verbose", "-v", action="store_true", help="verbose logging to stderr")
    p.add_argument("--docker-tag", default=None,
                   help="override docker image tag")
    p.add_argument("--diff", metavar="REF", default=None,
                   help="restrict scans to files changed vs REF (e.g. origin/main). "
                        "Currently affects the secrets stage.")
    return p.parse_args(argv)


def merge_cli_into_config(cfg: PipelineConfig, args: argparse.Namespace) -> None:
    """CLI flags override config file values."""
    if args.only:
        cfg.only = list(args.only)
    if args.skip:
        cfg.skip = list(args.skip)
    if args.fail_fast:
        cfg.fail_fast = True
    if args.json_to_stdout:
        cfg.output.quiet = True
    if args.no_color:
        cfg.output.color = False
    if args.docker_tag:
        cfg.docker_tag = args.docker_tag
    cfg.validate()


def _stage_enabled(name: str, cfg: PipelineConfig) -> bool:
    if cfg.only and name not in cfg.only:
        return False
    if name in cfg.skip:
        return False
    # stage-specific toggles
    toggle = getattr(cfg.stages, name, None)
    return toggle is not False


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv if argv is not None else sys.argv[1:])
    except SystemExit as e:
        # argparse calls sys.exit(2) on bad args; pass that through.
        return int(e.code) if e.code is not None else EXIT_USAGE

    # Ensure UTF-8 output on Windows where the default encoding may be cp1252.
    for _stream in (sys.stdout, sys.stderr):
        if isinstance(_stream, TextIOWrapper):
            _stream.reconfigure(encoding="utf-8", errors="replace")

    root: Path = args.root.resolve()
    if not root.is_dir():
        print(f"error: --root is not a directory: {root}", file=sys.stderr)
        return EXIT_USAGE

    _setup_logging(str(args.log_file) if args.log_file else None, args.verbose)

    # Load config
    cfg_path = args.config or find_config_file(root)
    try:
        cfg = load_config(cfg_path)
        merge_cli_into_config(cfg, args)
    except ConfigError as e:
        print(f"config error: {e}", file=sys.stderr)
        return EXIT_CONFIG

    printer = Printer(quiet=cfg.output.quiet, color=cfg.output.color)
    report = Report(root=str(root), tool_version=__version__,
                    config_path=str(cfg_path) if cfg_path else None)
    started = time.monotonic()

    # SIGINT → KeyboardInterrupt so we can still print a summary
    def _handle_sigint(_sig, _frame):  # type: ignore[no-untyped-def]  # pragma: no cover
        raise KeyboardInterrupt
    signal.signal(signal.SIGINT, _handle_sigint)

    printer.section(f"Pipeline Guard {__version__}")
    d = detect(root)
    report.detected = d.labels()
    printer.info(f"root:     {root}")
    printer.info(f"config:   {cfg_path or '(defaults — no config file found)'}")
    printer.info(f"detected: {', '.join(d.labels()) or '(nothing recognized)'}")

    detected_map = {
        "python": d.python, "node": d.node, "dotnet": d.dotnet,
        "go": d.go, "rust": d.rust, "docker": d.docker,
        "vulns": d.python or d.node or d.rust or d.go,
    }

    try:
        # Secrets first — fast and we want to stop early on a leak.
        if _stage_enabled("secrets", cfg) and cfg.secrets.enabled:
            printer.section("Secrets")
            r = scan_secrets(root, cfg.secrets, cfg.timeouts.scan_s,
                             diff_base=args.diff)
            report.add(r)
            _log_step(r, printer)
            if r.is_failure() and cfg.fail_fast:
                raise _FailFast()

        # Language stages
        for stage_name in ("python", "node", "dotnet", "go", "rust", "docker", "vulns"):
            if not detected_map.get(stage_name):
                continue
            if not _stage_enabled(stage_name, cfg):
                report.add(StepResult(name=stage_name, status=Status.SKIPPED,
                                      message="disabled in config/flags"))
                continue
            printer.section(stage_name.upper() if stage_name == "vulns"
                            else stage_name.capitalize())
            before = len(report.steps)
            STAGES[stage_name](root, d, cfg, report.steps)
            for s in report.steps[before:]:
                _log_step(s, printer)
            if cfg.fail_fast and any(s.is_failure() for s in report.steps):
                raise _FailFast()

    except _FailFast:
        printer.warn("--fail-fast triggered; stopping.")
    except KeyboardInterrupt:  # pragma: no cover
        printer.warn("interrupted")
        report.duration_s = time.monotonic() - started
        _emit_outputs(report, cfg, args, printer)
        return EXIT_INTERRUPTED

    report.duration_s = time.monotonic() - started
    _emit_outputs(report, cfg, args, printer)
    return EXIT_FAILURES if report.failed() else EXIT_OK


def _log_step(s: StepResult, printer: Printer) -> None:
    if s.status == Status.PASSED:
        printer.ok(f"{s.name} ({s.duration_s:.1f}s)")
    elif s.status == Status.FAILED:
        printer.fail(f"{s.name}: {s.message}")
    elif s.status == Status.WARNED:
        printer.warn(f"{s.name}: {s.message}")
    else:
        printer.info(f"{s.name}: {s.message}")


def _emit_outputs(report: Report, cfg: PipelineConfig,
                  args: argparse.Namespace, printer: Printer) -> None:
    # JSON to stdout (--json) is mutually exclusive with the pretty summary.
    if cfg.output.quiet:
        sys.stdout.write(to_json(report))
        sys.stdout.write("\n")
    else:
        print_summary(report, printer)

    if args.sarif_out:
        try:
            args.sarif_out.write_text(to_sarif(report), encoding="utf-8")
        except OSError as e:
            print(f"warning: could not write SARIF: {e}", file=sys.stderr)
    if args.junit_out:
        try:
            args.junit_out.write_text(to_junit_xml(report), encoding="utf-8")
        except OSError as e:
            print(f"warning: could not write JUnit XML: {e}", file=sys.stderr)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

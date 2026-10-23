# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — bounded metadata command interface

"""Expose fixed repository checks with caller-safe structured diagnostics."""

import argparse
import io
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Never

from bridge_validation.capabilities import validate_capabilities
from bridge_validation.report import Finding, Refusal, Report


class Parser(argparse.ArgumentParser):
    """Parse CLI options without echoing rejected received arguments."""

    def error(self, message: str) -> Never:
        """Raise a fixed invalid-invocation finding.

        Parameters
        ----------
        message : str
            Ignored parser diagnostic, which may contain received text.

        Raises
        ------
        Refusal
            Invocation cannot select a valid fixed operation.
        """
        raise Refusal(Finding("cli.invalid", ".", "Invalid command arguments.", 4))


def check_main(
    gate: str, checker: Callable[[Path], Report], argv: Sequence[str] | None = None
) -> int:
    """Expose a fixed project-owned repository checker through the common CLI.

    Parameters
    ----------
    gate : str
        Authored gate name, never selected by repository input.
    checker : Callable[[Path], Report]
        Fixed implementation supplied by the command script.
    argv : Sequence[str] or None
        Explicit arguments or the process command line.

    Returns
    -------
    int
        Scoped gate result, preserving invalid invocation and delivery failure.
    """
    parser = Parser(description=f"Validate {gate} for SPIKE-FORMAT-BRIDGE.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    try:
        options = parser.parse_args(argv)
        report = checker(options.root)
    except Refusal as exc:
        report = Report(gate, [exc.finding])
    return emit_report(report)


def emit_report(report: Report) -> int:
    """Write a complete safe report and refuse an unavailable output channel.

    Parameters
    ----------
    report : Report
        Authored infrastructure result to emit.

    Returns
    -------
    int
        Gate exit code, or 3 when output cannot be delivered.
    """
    try:
        sys.stdout.write(report.encode())
        sys.stdout.flush()
    except (OSError, UnicodeError):
        sys.stdout = io.StringIO()
        return 3
    return report.exit_code


def inventory_main(argv: Sequence[str] | None = None) -> int:
    """Generate or verify capability inventory with explicit operation scope.

    Parameters
    ----------
    argv : Sequence[str] or None
        Explicit arguments, or the process command line.

    Returns
    -------
    int
        Zero only for the requested operation; 2 refused, 3 unavailable, 4 invalid.
    """
    parser = Parser(description="Generate or verify SPIKE-FORMAT-BRIDGE inventory.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mode", choices=("generate", "verify"), default="verify")
    parser.add_argument("--output")
    try:
        options = parser.parse_args(argv)
        if (options.mode == "generate") != (options.output is not None):
            raise Refusal(
                Finding("cli.output", ".", "Only generate requires an explicit new output.", 4)
            )
        report = validate_capabilities(options.root, options.output)
        if options.mode == "verify":
            from bridge_validation.structure import validate_structure

            structural = validate_structure(options.root)
            report.gate = "repository_inventory"
            report.findings.extend(structural.findings)
    except Refusal as exc:
        report = Report("repository_inventory", [exc.finding])
    return emit_report(report)

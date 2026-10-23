# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — repository identity and validation foundation

"""Run repository-owned read-only checks with consistent public exit reports."""

import argparse
import io
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import NoReturn

from .inputs import CheckFailure
from .report import Finding, Refusal, Report


class Arguments(argparse.Namespace):
    """Typed values populated by the command-line parser.

    Attributes
    ----------
    root : Path
        Repository directory supplying the maintained sources.
    json : bool
        Whether to emit the machine-readable report.
    """

    root: Path
    json: bool


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser with a fixed caller-facing configuration failure."""

    def error(self, message: str) -> NoReturn:
        """Refuse invalid arguments without reflecting their received values.

        Parameters
        ----------
        message : str
            Parser diagnostic, which is not emitted.

        Raises
        ------
        Refusal
            With a fixed invalid-invocation finding for the canonical report.
        """
        raise Refusal(Finding("cli.invalid", ".", "Invalid command arguments.", 4))


def run(
    check: str,
    verify: Callable[[Path], None],
    argv: Sequence[str] | None,
    *,
    description: str,
) -> int:
    """Invoke one authored check and report its actual native outcome.

    Parameters
    ----------
    check : str
        Fixed check identifier selected by the public entry point.
    verify : Callable[[Path], None]
        Project-owned verification implementation.
    argv : Sequence[str] or None
        Actual argument sequence, or the process arguments when absent.
    description : str
        Fixed public help text provided by the owning entry point.

    Returns
    -------
    int
        Zero for a match, two for refusal, three for unavailable input.
        Invalid arguments exit four; help exits zero.
    """
    parser = ArgumentParser(prog=check, description=description)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--json", action="store_true")
    options = Arguments()
    options.root = Path(".")
    options.json = False
    findings: list[Finding] = []
    exit_code = 0
    try:
        parser.parse_args(argv, namespace=options)
        verify(options.root)
    except CheckFailure as error:
        exit_code = error.exit_code
        findings.append(
            Finding(
                error.code,
                error.location,
                "Required repository input was not accepted.",
                error.exit_code,
            )
        )
    except Refusal as error:
        exit_code = error.finding.exit_code
        findings.append(error.finding)
    status = {0: "passed", 2: "refused", 3: "unavailable", 4: "invalid"}[exit_code]
    report = Report(check, findings)
    try:
        if options.json or exit_code == 4:
            sys.stdout.write(report.encode())
        else:
            print(check + ": " + status)
        sys.stdout.flush()
    except (OSError, UnicodeError):
        sys.stdout = io.StringIO()
        return 3
    return exit_code

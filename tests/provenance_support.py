# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — source provenance command tests

"""Invoke the actual source command and prepare isolated native Git inputs."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import cast

from bridge_validation.inputs import Json

SOURCE = Path(__file__).resolve().parents[1]


def prepare(root: Path) -> Path:
    """Copy the actual maintained source cohort and initialise its own Git repository.

    Parameters
    ----------
    root : Path
        Test-owned directory receiving isolated mutable source inputs.

    Returns
    -------
    Path
        Complete actual-source fixture with an independent native Git index.
    """
    result = subprocess.run(
        ["git", "-C", str(SOURCE), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        capture_output=True,
        check=True,
        timeout=10,
    )
    for name in result.stdout.decode("utf-8").split("\0")[:-1]:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / name, target)
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(root)],
        capture_output=True,
        check=True,
        timeout=10,
    )
    return root


def invoke(
    root: Path,
    *arguments: str,
    machine: bool = True,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the actual public provenance command in a separately measured interpreter.

    Parameters
    ----------
    root : Path
        Received source directory.
    arguments : str
        Additional public command arguments.
    machine : bool
        Whether to request JSON output.
    environment : dict[str, str] or None
        Actual child environment changes for dependency-availability controls.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Native status and original streams.
    """
    args = [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--parallel-mode",
        "--branch",
        "--source=" + str(SOURCE / "tools") + "," + str(SOURCE / "tests"),
        str(SOURCE / "tools/check_source_provenance.py"),
        "--root",
        str(root),
    ]
    if machine:
        args.append("--json")
    args.extend(arguments)
    env = dict(os.environ)
    if environment is not None:
        env.update(environment)
    env["COVERAGE_FILE"] = os.environ.get(
        "COVERAGE_FILE", str(SOURCE / ".tool-cache/coverage/data")
    )
    return subprocess.run(args, cwd=SOURCE, env=env, capture_output=True, text=True, timeout=15)


def check(
    result: subprocess.CompletedProcess[str],
    expected: int,
    code: str = "",
    location: str = "",
) -> None:
    """Assert the native result against the independently declared source contract.

    Parameters
    ----------
    result : subprocess.CompletedProcess[str]
        Actual process outcome.
    expected : int
        Expected public exit.
    code : str
        Authored refusal or unavailable finding.
    location : str
        Expected repository-relative location.
    """
    assert result.returncode == expected, (result.stdout, result.stderr)
    assert result.stderr == ""
    data = cast(dict[str, Json], json.loads(result.stdout))
    assert data["gate"] == "source_provenance"
    assert data["scope"] == "local_scaffold_infrastructure"
    assert data["status"] == {0: "pass", 2: "refused", 3: "unavailable"}[expected]
    reasons = cast(list[dict[str, Json]], data["reasons"])
    assert [{"code": row["code"], "location": row["path"]} for row in reasons] == (
        [] if expected == 0 else [{"code": code, "location": location}]
    )

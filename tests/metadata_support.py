# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — repository metadata command tests

"""Invoke the real metadata command with isolated complete declaration inputs."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

from bridge_validation.inputs import Json

SOURCE = Path(__file__).resolve().parents[1]
INPUTS = ("repository-domain.json", "schemas/repository-domain.schema.json", "requirements-dev.txt")


def run(
    root: Path, *arguments: str, machine: bool = True, explicit_root: bool = True
) -> subprocess.CompletedProcess[str]:
    """Execute the actual public command in a measured child interpreter.

    Parameters
    ----------
    root : Path
        Directory supplying complete declaration inputs.
    arguments : str
        Additional native command arguments.
    machine : bool
        Whether to request JSON output.
    explicit_root : bool
        Whether to supply the root argument or use the current directory.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Actual child status and unmodified standard streams.
    """
    command = [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--parallel-mode",
        "--branch",
        "--source=" + str(SOURCE / "tools") + "," + str(SOURCE / "tests"),
        str(SOURCE / "tools/check_repository_metadata.py"),
    ]
    if explicit_root:
        command.extend(("--root", str(root)))
    if machine:
        command.append("--json")
    command.extend(arguments)
    environment = dict(os.environ)
    environment["COVERAGE_FILE"] = os.environ.get(
        "COVERAGE_FILE", str(SOURCE / ".tool-cache/coverage/data")
    )
    return subprocess.run(
        command,
        cwd=SOURCE if explicit_root else root,
        env=environment,
        capture_output=True,
        text=True,
        timeout=15,
    )


def report(result: subprocess.CompletedProcess[str], expected: int) -> dict[str, Json]:
    """Check native exit and safe report semantics.

    Parameters
    ----------
    result : subprocess.CompletedProcess[str]
        Actual command outcome.
    expected : int
        Independently expected public exit status.

    Returns
    -------
    dict[str, Json]
        Parsed command report.
    """
    assert result.returncode == expected, (result.stdout, result.stderr)
    assert result.stderr == ""
    parsed = cast(dict[str, Json], json.loads(result.stdout))
    assert parsed["scope"] == "local_scaffold_infrastructure"
    assert parsed["gate"] == "repository_metadata"
    assert parsed["status"] == {0: "pass", 2: "refused", 3: "unavailable"}[expected]
    parsed["findings"] = [
        {"code": row["code"], "location": row["path"]}
        for row in cast(list[dict[str, Json]], parsed["reasons"])
    ]
    return parsed


def change(root: Path, path: tuple[str, ...], value: Json) -> None:
    """Replace a received metadata value without changing other declaration files.

    Parameters
    ----------
    root : Path
        Complete input set.
    path : tuple[str, ...]
        Actual metadata member path.
    value : Json
        Replacement received value.
    """
    metadata = cast(dict[str, Json], json.loads((root / "repository-domain.json").read_text()))
    node = metadata
    for part in path[:-1]:
        node = cast(dict[str, Json], node[part])
    node[path[-1]] = value
    (root / "repository-domain.json").write_text(json.dumps(metadata) + "\n")

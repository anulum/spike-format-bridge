# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — repository metadata command tests

"""Exercise declaration identity, parser bounds and acyclic metadata bootstrap."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from bridge_validation.inputs import Json

from .metadata_support import INPUTS, SOURCE, change, report, run


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """Copy the actual complete declaration inputs to an owned temporary directory.

    Parameters
    ----------
    tmp_path : Path
        Test-owned Samsung directory.

    Returns
    -------
    Path
        Complete input set, without an inventory or other repository files.
    """
    for name in INPUTS:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((SOURCE / name).read_bytes())
    return tmp_path


def test_bootstrap_is_read_only_and_requires_no_inventory(root: Path) -> None:
    """Valid metadata succeeds before inventory generation without changing bytes.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    """
    before = {name: (root / name).read_bytes() for name in INPUTS}
    assert not (root / "capability-inventory.json").exists()
    assert report(run(root), 0)["findings"] == []
    assert {name: (root / name).read_bytes() for name in INPUTS} == before
    assert not (root / "capability-inventory.json").exists()
    (root / "capability-inventory.json").write_text("not JSON")
    assert report(run(root), 0)["findings"] == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        (("repository_name",), "OTHER"),
        (("owner_group",), "OTHER"),
        (("lifecycle",), "local_scaffold"),
        (("public_remote",), "https://github.com/anulum/other-repository"),
        (("public_remote",), "https://github.com/anulum/SPIKE-FORMAT-BRIDGE"),
        (("evidence_maturity",), "qualified"),
        (("capabilities",), ["convert"]),
        (("claims",), ["lossless"]),
        (("qualified_owned_schema_ids",), ["spike_format_bridge.conversion.v1"]),
        (("planned_owned_schema_ids",), []),
        (("domain_runtime_dependencies",), ["numpy"]),
        (("unexpected",), True),
        (("validation_profile", "id"), "other"),
        (("validation_profile", "revision"), "2026-08-30"),
        (("validation_profile", "standard_sha256"), "0" * 64),
        (("validation_profile", "profile_sha256"), "0" * 64),
        (("tooling_python", "design_baseline"), "3.14"),
        (("tooling_python", "actual_version"), "3.13.15"),
        (("tooling_python", "supported_range"), ">=3"),
        (("tooling_python", "development_lock_sha256"), "0" * 64),
    ],
)
def test_changed_declarations_refuse(root: Path, field: tuple[str, ...], value: Json) -> None:
    """Ownership, empty capability and source-policy declarations cannot be relabelled.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    field : tuple[str, ...]
        Received member path.
    value : Json
        Altered member value.
    """
    change(root, field, value)
    assert report(run(root), 2)["findings"] == [
        {"code": "metadata_mismatch", "location": "repository-domain.json"}
    ]


@pytest.mark.parametrize(
    "raw",
    [
        b'{"same":1,"same":2}',
        b'{"bad":NaN}',
        b'{"bad":Infinity}',
        b'{"bad":-Infinity}',
        b'{"bad":1e999}',
        b'{"bad":"\\ud800"}',
        b"[]",
        b"null",
        b"1",
        b"{",
        b"\xff",
        b"[" * 1100 + b"null" + b"]" * 1100,
    ],
)
def test_invalid_json_refuses_without_interpreter_text(root: Path, raw: bytes) -> None:
    """Malformed, duplicate, nonfinite, invalid-Unicode and deep inputs stay refused.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    raw : bytes
        Actual received JSON bytes.
    """
    (root / "repository-domain.json").write_bytes(raw)
    assert report(run(root), 2)["findings"] == [
        {"code": "input_invalid", "location": "repository-domain.json"}
    ]


@pytest.mark.parametrize("name", INPUTS)
@pytest.mark.parametrize("directory", [False, True])
def test_unavailable_inputs_are_not_policy_passes(root: Path, name: str, directory: bool) -> None:
    """Absent files and directories in file positions produce unavailable status.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    name : str
        Actual required input path.
    directory : bool
        Whether a directory replaces the file.
    """
    target = root / name
    target.unlink()
    if directory:
        target.mkdir()
    assert report(run(root), 3)["findings"] == [{"code": "input_unavailable", "location": name}]


def test_changed_schema_is_not_admitted_by_shape(root: Path) -> None:
    """Even whitespace changes require explicit schema source-policy reconciliation.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    """
    path = root / "schemas/repository-domain.schema.json"
    path.write_bytes(path.read_bytes() + b" ")
    assert report(run(root), 2)["findings"] == [
        {"code": "schema_source_changed", "location": "schemas/repository-domain.schema.json"}
    ]


def test_metadata_byte_limit_is_inclusive(root: Path) -> None:
    """Accept the exact 64 KiB JSON boundary and reject the next byte.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    """
    path = root / "repository-domain.json"
    raw = path.read_bytes()
    path.write_bytes(raw + b" " * (65536 - len(raw)))
    assert report(run(root), 0)["findings"] == []
    path.write_bytes(path.read_bytes() + b" ")
    assert report(run(root), 2)["findings"] == [
        {"code": "input_too_large", "location": "repository-domain.json"}
    ]


def test_lock_bytes_are_bound_with_an_inclusive_limit(root: Path) -> None:
    """A changed lock needs a matching declaration; bounds remain enforced.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    """
    path = root / "requirements-dev.txt"
    path.write_bytes(b"#" * 1048576)
    assert report(run(root), 2)["findings"] == [
        {"code": "metadata_mismatch", "location": "repository-domain.json"}
    ]
    change(
        root,
        ("tooling_python", "development_lock_sha256"),
        hashlib.sha256(path.read_bytes()).hexdigest(),
    )
    assert report(run(root), 0)["findings"] == []
    path.write_bytes(path.read_bytes() + b"#")
    assert report(run(root), 2)["findings"] == [
        {"code": "input_too_large", "location": "requirements-dev.txt"}
    ]


def test_native_default_root_and_human_output(root: Path) -> None:
    """The default directory and human output exercise the same real check.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    """
    assert report(run(root, explicit_root=False), 0)["findings"] == []
    result = run(root, machine=False)
    assert result.returncode == 0
    assert result.stdout == "repository_metadata: passed\n"
    assert result.stderr == ""


def test_help_and_invalid_arguments_preserve_public_exit_contract(root: Path) -> None:
    """Help succeeds while malformed arguments cannot reflect received values.

    Parameters
    ----------
    root : Path
        Complete declaration inputs.
    """
    help_result = run(root, "--help")
    assert help_result.returncode == 0
    assert "Spike Format Bridge" in help_result.stdout
    assert help_result.stderr == ""
    bad = run(root, "--received-untrusted-value")
    assert bad.returncode == 4
    assert bad.stderr == ""
    data = json.loads(bad.stdout)
    assert data["gate"] == "repository_metadata" and data["status"] == "invalid"
    assert data["reasons"][0]["code"] == "cli.invalid"
    assert "received-untrusted-value" not in bad.stdout


def test_unavailable_native_report_output(root: Path) -> None:
    """Refuse real report delivery failure without returning a metadata pass.

    Parameters
    ----------
    root : Path
        Complete original declarations supplied to the actual public command.
    """
    with Path("/dev/full").open("w") as output:
        result = subprocess.run(
            [
                sys.executable,
                str(SOURCE / "tools/check_repository_metadata.py"),
                "--root",
                str(root),
                "--json",
            ],
            stdout=output,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=15,
        )
    assert result.returncode == 3
    assert "Traceback" not in result.stderr

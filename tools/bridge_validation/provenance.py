# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — maintained source provenance

"""Validate the actual Git-maintained source cohort and its licence notices."""

import hashlib
import shutil
from pathlib import Path

from .execution import run_tool
from .inputs import CheckFailure, read_bytes, read_object
from .provenance_policy import (
    ASSETS,
    COPYRIGHT_FIELDS,
    HEADER_FIELDS,
    LICENCE_SHA256,
    PROJECT_NOTICE,
    REUSE_SHA256,
)
from .report import Refusal


def _cohort(root: Path) -> list[str]:
    """Read tracked and nonignored untracked names through native Git."""
    if not (root / ".git").exists():
        raise CheckFailure("git_unavailable", ".", unavailable=True)
    try:
        result = run_tool(
            [
                shutil.which("git") or "/unavailable-required-git",
                "-c",
                "core.fsmonitor=false",
                "-C",
                str(root),
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            root=root,
            timeout=10,
        )
    except Refusal as error:
        raise CheckFailure("git_unavailable", ".", unavailable=True) from error
    if result.returncode:
        raise CheckFailure("git_unavailable", ".", unavailable=True)
    try:
        names = result.stdout.decode("utf-8").split("\0")
    except UnicodeError as error:
        raise CheckFailure("git_names_invalid", ".", unavailable=True) from error
    return sorted(set(names) - {""})


def _notice(lines: list[str], name: str) -> None:
    """Validate the seven fixed notice fields and a nonempty module description."""
    if (
        len(lines) < 7
        or tuple(lines[:6]) != HEADER_FIELDS
        or not lines[6].startswith(PROJECT_NOTICE)
        or not lines[6][len(PROJECT_NOTICE) :].strip()
    ):
        raise CheckFailure("source_notice_mismatch", name)


def _text_notice(raw: bytes, name: str) -> None:
    """Check native source or invisible Markdown notices without decoding binaries."""
    try:
        text = raw.decode("utf-8")
    except UnicodeError as error:
        raise CheckFailure("source_not_utf8", name) from error
    lines = text.splitlines()
    if name.lower().endswith(".md"):
        if len(lines) < 9 or lines[0] != "<!--" or lines[8] != "-->":
            raise CheckFailure("markdown_notice_visible", name)
        _notice(lines[1:8], name)
    else:
        if any(not line.startswith("# ") for line in lines[:7]):
            raise CheckFailure("source_notice_mismatch", name)
        _notice([line.removeprefix("# ") for line in lines[:7]], name)
    label = "SPDX-" + "License-Identifier:"
    for line in lines:
        if label in line:
            expression = line.split(label, 1)[1].strip()
            if expression != "AGPL-3.0-or-later":
                raise CheckFailure("conflicting_licence", name)


def _sidecar(root: Path, name: str) -> None:
    """Check the exact JSON sidecar fields without relabelling the JSON payload."""
    raw = read_bytes(root, name, 8192)
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeError as error:
        raise CheckFailure("sidecar_invalid", name) from error
    if len(lines) != 9 or tuple(lines[7:]) != COPYRIGHT_FIELDS:
        raise CheckFailure("sidecar_invalid", name)
    _notice(lines[:7], name)


def verify(root: Path) -> None:
    """Check notices and selected original bytes across the maintained Git cohort.

    Parameters
    ----------
    root : Path
        Local repository supplying tracked and nonignored untracked files.

    Raises
    ------
    CheckFailure
        For unavailable Git or files, symlinks, changed original legal/assets,
        missing or invalid JSON sidecars, malformed JSON or incorrect notices.

    Notes
    -----
    This validates maintained source identity and notices. It does not qualify
    installed dependencies, a full repository inventory or recording formats.
    Ignored files are outside this cohort; private projection checks are separate.
    """
    names = _cohort(root)
    if not names:
        raise CheckFailure("source_cohort_empty", ".")
    selected = set(names)
    required = {
        "LICENSE",
        "LICENSES/AGPL-3.0-or-later.txt",
        "REUSE.toml",
        "repository-domain.json",
        "schemas/repository-domain.schema.json",
        *ASSETS,
    }
    for name in sorted(required):
        if name not in selected:
            raise CheckFailure("required_source_missing", name)
    for name in names:
        path = root / name
        if path.is_symlink():
            raise CheckFailure("source_symlink", name)
        if name == "REUSE.toml":
            if hashlib.sha256(read_bytes(root, name, 1048576)).hexdigest() != REUSE_SHA256:
                raise CheckFailure("reuse_policy_changed", name)
        elif name in ("LICENSE", "LICENSES/AGPL-3.0-or-later.txt"):
            if hashlib.sha256(read_bytes(root, name, 1048576)).hexdigest() != LICENCE_SHA256:
                raise CheckFailure("original_licence_changed", name)
        elif name in ASSETS:
            size, digest = ASSETS[name]
            raw = read_bytes(root, name, size)
            if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
                raise CheckFailure("original_asset_changed", name)
        elif name.lower().endswith(".json"):
            _, _ = read_object(root, name, 1048576)
            if name + ".license" not in selected:
                raise CheckFailure("json_sidecar_missing", name)
            if (root / (name + ".license")).is_symlink():
                raise CheckFailure("source_symlink", name + ".license")
            _sidecar(root, name + ".license")
        elif name.endswith(".license"):
            if not name[:-8].lower().endswith(".json") or name[:-8] not in selected:
                raise CheckFailure("orphan_sidecar", name)
            _sidecar(root, name)
        else:
            _text_notice(read_bytes(root, name, 1048576), name)

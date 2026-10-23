# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — source provenance command tests

"""Exercise source notices, original-byte identities and native Git cohort boundaries."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from .provenance_support import check, invoke, prepare


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """Prepare a complete mutable source cohort from the actual repository.

    Parameters
    ----------
    tmp_path : Path
        Owned Samsung test directory.

    Returns
    -------
    Path
        Original source copy with independent native Git administration.
    """
    return prepare(tmp_path)


def test_actual_complete_source_passes_without_rewriting(root: Path) -> None:
    """Validate every maintained source while preserving its exact original bytes.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    before = {
        str(p.relative_to(root)): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts
    }
    check(invoke(root), 0)
    after = {
        str(p.relative_to(root)): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts
    }
    assert after == before


@pytest.mark.parametrize("field", range(7))
def test_each_notice_field_is_enforced(root: Path, field: int) -> None:
    """Refuse altered provenance fields on a newly maintained Python file.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    field : int
        Header field being altered.
    """
    lines = (root / "tools/check_repository_metadata.py").read_text().splitlines()
    lines[field] = "# incorrect received field"
    (root / "additional.py").write_text("\n".join(lines) + "\n")
    check(invoke(root), 2, "source_notice_mismatch", "additional.py")


def test_module_description_cannot_be_empty(root: Path) -> None:
    """The project identity alone cannot replace a source module description.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    lines = (root / "tools/check_repository_metadata.py").read_text().splitlines()
    lines[6] = "# SPIKE-FORMAT-BRIDGE — "
    (root / "additional.py").write_text("\n".join(lines) + "\n")
    check(invoke(root), 2, "source_notice_mismatch", "additional.py")


@pytest.mark.parametrize("raw", [b"", b"# only one line\n", b"plain text\n"])
def test_short_or_uncommented_source_refuses(root: Path, raw: bytes) -> None:
    """Missing fields and non-native source notices stay refused.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    raw : bytes
        Received source bytes.
    """
    (root / "additional.py").write_bytes(raw)
    check(invoke(root), 2, "source_notice_mismatch", "additional.py")


@pytest.mark.parametrize("line", [0, 8])
def test_markdown_notice_must_be_invisible(root: Path, line: int) -> None:
    """Malformed comment delimiters cannot expose a Markdown licence header.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    line : int
        Received delimiter position.
    """
    path = root / "README.md"
    lines = path.read_text().splitlines()
    lines[line] = "visible notice"
    path.write_text("\n".join(lines) + "\n")
    check(invoke(root), 2, "markdown_notice_visible", "README.md")


def test_short_markdown_and_non_utf8_text_refuse(root: Path) -> None:
    """Actual invalid text bytes and incomplete Markdown get locating refusals.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    path = root / "additional.md"
    path.write_bytes(b"short")
    check(invoke(root), 2, "markdown_notice_visible", "additional.md")
    path.unlink()
    (root / "additional.py").write_bytes(b"\xff")
    check(invoke(root), 2, "source_not_utf8", "additional.py")


def test_later_conflicting_licence_refuses(root: Path) -> None:
    """A later declaration cannot override the actual source licence.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    path = root / "tools/check_repository_metadata.py"
    path.write_text(path.read_text() + "\n# SPDX-" + "License-Identifier: MIT\n")
    check(invoke(root), 2, "conflicting_licence", "tools/check_repository_metadata.py")


@pytest.mark.parametrize("name", ["LICENSE", "LICENSES/AGPL-3.0-or-later.txt"])
def test_original_gnu_text_is_unchanged(root: Path, name: str) -> None:
    """Edited standard licence bytes cannot be relabelled with a project notice.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    name : str
        Selected original licence path.
    """
    (root / name).write_bytes(b"replaced original")
    check(invoke(root), 2, "original_licence_changed", name)


def test_annotation_policy_is_source_bound(root: Path) -> None:
    """A changed REUSE policy cannot authorise different source ownership.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    path = root / "REUSE.toml"
    path.write_bytes(path.read_bytes() + b"\n")
    check(invoke(root), 2, "reuse_policy_changed", "REUSE.toml")


@pytest.mark.parametrize(
    "name", ["anulum_logo_company.jpg", "anulum_logo.png", "fortis_studio_logo.jpg"]
)
def test_every_original_asset_is_bound(root: Path, name: str) -> None:
    """Actual branding bytes are checked separately from source text.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    name : str
        Selected original asset.
    """
    path = root / "docs/assets" / name
    raw = bytearray(path.read_bytes())
    raw[-1] ^= 1
    path.write_bytes(raw)
    check(invoke(root), 2, "original_asset_changed", "docs/assets/" + name)


def test_asset_length_and_read_bound_are_enforced(root: Path) -> None:
    """Truncated and oversized actual assets receive distinct locating refusals.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    path = root / "docs/assets/fortis_studio_logo.jpg"
    raw = path.read_bytes()
    path.write_bytes(raw[:-1])
    check(invoke(root), 2, "original_asset_changed", "docs/assets/fortis_studio_logo.jpg")
    path.write_bytes(raw + b"x")
    check(invoke(root), 2, "input_too_large", "docs/assets/fortis_studio_logo.jpg")


def test_json_must_be_a_strict_object(root: Path) -> None:
    """Source JSON receives the real duplicate-key parser before sidecar admission.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    (root / "repository-domain.json").write_bytes(b'{"same":1,"same":2}')
    check(invoke(root), 2, "input_invalid", "repository-domain.json")


@pytest.mark.parametrize("ignored", [False, True])
def test_json_sidecar_must_be_in_the_same_cohort(root: Path, ignored: bool) -> None:
    """A missing or merely ignored sidecar cannot qualify a JSON source.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    ignored : bool
        Whether to retain the physical sidecar but exclude it through Git.
    """
    name = "repository-domain.json.license"
    if ignored:
        path = root / ".gitignore"
        path.write_text(path.read_text() + "\n" + name + "\n")
    else:
        (root / name).unlink()
    check(invoke(root), 2, "json_sidecar_missing", "repository-domain.json")


@pytest.mark.parametrize("kind", ["short", "copyright", "encoding", "project"])
def test_sidecar_fields_are_exact(root: Path, kind: str) -> None:
    """Wrong copyright, project, length or encoding cannot qualify JSON ownership.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    kind : str
        Received sidecar defect.
    """
    path = root / "repository-domain.json.license"
    lines = path.read_text().splitlines()
    if kind == "short":
        path.write_text("\n".join(lines[:-1]) + "\n")
    elif kind == "copyright":
        lines[-1] = "incorrect copyright"
        path.write_text("\n".join(lines) + "\n")
    elif kind == "project":
        lines[6] = "OTHER — input"
        path.write_text("\n".join(lines) + "\n")
    else:
        path.write_bytes(b"\xff")
    code = "source_notice_mismatch" if kind == "project" else "sidecar_invalid"
    check(invoke(root), 2, code, "repository-domain.json.license")


@pytest.mark.parametrize("name", ["orphan.json.license", "orphan.txt.license"])
def test_orphan_or_non_json_sidecars_refuse(root: Path, name: str) -> None:
    """Sidecars cannot hide unrelated source types or absent payloads.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    name : str
        Orphan sidecar name.
    """
    (root / name).write_bytes((root / "repository-domain.json.license").read_bytes())
    check(invoke(root), 2, "orphan_sidecar", name)


@pytest.mark.parametrize(
    "name", ["LICENSE", "repository-domain.json", "repository-domain.json.license"]
)
def test_source_links_are_refused_before_reading_targets(root: Path, name: str) -> None:
    """Symlink entries and JSON sidecar links cannot substitute foreign source bytes.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    name : str
        Source entry replaced by a link to an owned ignored stash.
    """
    path = root / name
    stash = root / ".tool-cache/stash"
    stash.parent.mkdir()
    stash.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(stash)
    check(invoke(root), 2, "source_symlink", name)


def test_missing_required_and_deleted_tracked_sources_remain_visible(root: Path) -> None:
    """Required untracked absence and deleted tracked content cannot shrink the cohort.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    path = root / "docs/assets/anulum_logo.png"
    raw = path.read_bytes()
    path.unlink()
    check(invoke(root), 2, "required_source_missing", "docs/assets/anulum_logo.png")
    path.write_bytes(raw)
    subprocess.run(
        ["git", "-C", str(root), "add", "docs/assets/anulum_logo.png"],
        check=True,
        capture_output=True,
        timeout=10,
    )
    path.unlink()
    check(invoke(root), 3, "input_unavailable", "docs/assets/anulum_logo.png")


def test_native_git_dependency_and_root_failures_are_explicit(
    root: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    """Missing native Git, missing administration and invalid Git state are unavailable.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    tmp_path_factory : pytest.TempPathFactory
        Owned factory for an empty native repository.
    """
    check(invoke(root, environment={"PATH": ""}), 3, "git_unavailable", ".")
    shutil.rmtree(root / ".git")
    check(invoke(root), 3, "git_unavailable", ".")
    (root / ".git").write_text("invalid native Git administration\n")
    check(invoke(root), 3, "git_unavailable", ".")
    empty = tmp_path_factory.mktemp("empty-source-cohort")
    subprocess.run(
        ["git", "init", "--initial-branch=main", str(empty)],
        check=True,
        capture_output=True,
        timeout=10,
    )
    check(invoke(empty), 2, "source_cohort_empty", ".")


def test_non_utf8_git_name_has_a_safe_unavailable_report(root: Path) -> None:
    """Real native Git filename bytes cannot leak through a Unicode failure.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    with open(os.fsencode(root) + b"/non_utf8_\xff.py", "wb") as stream:
        stream.write(b"received file")
    check(invoke(root), 3, "git_names_invalid", ".")


def test_text_and_sidecar_byte_limits_are_inclusive(root: Path) -> None:
    """Real text and sidecar inputs accept their exact bound and refuse the next byte.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    text = root / "README.md"
    raw = text.read_bytes()
    text.write_bytes(raw + b" " * (1048576 - len(raw)))
    check(invoke(root), 0)
    text.write_bytes(text.read_bytes() + b" ")
    check(invoke(root), 2, "input_too_large", "README.md")
    text.write_bytes(raw)
    sidecar = root / "repository-domain.json.license"
    data = sidecar.read_bytes()
    lines = data.decode().splitlines()
    lines[6] += "x" * (8192 - len(data))
    sidecar.write_text("\n".join(lines) + "\n")
    assert sidecar.stat().st_size == 8192
    check(invoke(root), 0)
    lines[6] += "x"
    sidecar.write_text("\n".join(lines) + "\n")
    check(invoke(root), 2, "input_too_large", "repository-domain.json.license")


def test_public_human_help_and_argument_contracts(root: Path) -> None:
    """Both public output modes and authored argument failures remain reachable.

    Parameters
    ----------
    root : Path
        Complete actual-source fixture.
    """
    result = invoke(root, machine=False)
    assert result.returncode == 0 and result.stdout == "source_provenance: passed\n"
    assert result.stderr == ""
    help_result = invoke(root, "--help")
    assert help_result.returncode == 0 and "Spike Format Bridge" in help_result.stdout
    assert help_result.stderr == ""
    bad = invoke(root, "--unknown-received-value")
    assert bad.returncode == 4 and bad.stderr == ""
    data = json.loads(bad.stdout)
    assert data["gate"] == "source_provenance" and data["status"] == "invalid"
    assert data["reasons"][0]["code"] == "cli.invalid"
    assert "unknown-received-value" not in bad.stdout

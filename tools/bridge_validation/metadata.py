# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — repository metadata validation

"""Validate repository declarations without requiring their generated inventory."""

import hashlib
from pathlib import Path
from typing import Final, cast

from .inputs import CheckFailure, Json, read_bytes, read_object
from .report import Finding, Report

SCHEMA_SHA256: Final = "8acb17d37de05974eb1961953de18ef649cc5ab69ee8299b7aaf147722c96972"
PROFILE: Final[dict[str, Json]] = {
    "id": "gotm.enterprise-repository-tier0.local-scaffold",
    "revision": "2026-10-04",
    "standard_sha256": "8421674a61444474447fad2f4d2bfc54dc5a1ea12ae988785e57dbcab385938c",
    "profile_sha256": "f453a70eae008c41f8d26a1f495ec3636f64739bcedb9caac0bdf8774300905c",
}


def verify(root: Path) -> None:
    """Validate the complete declaration against the fixed local source policy.

    Parameters
    ----------
    root : Path
        Repository supplying the schema, metadata and development lock.

    Raises
    ------
    CheckFailure
        For missing, oversized or malformed inputs, a changed policy schema,
        or declarations inconsistent with the owned repository boundary.

    Notes
    -----
    This read-only operation neither reads nor creates capability-inventory.json.
    A declaration match does not qualify the installed dependency environment,
    domain format support, signatures or scientific evidence.
    """
    schema_name = "schemas/repository-domain.schema.json"
    schema_raw, _ = read_object(root, schema_name)
    if hashlib.sha256(schema_raw).hexdigest() != SCHEMA_SHA256:
        raise CheckFailure("schema_source_changed", schema_name)
    metadata_name = "repository-domain.json"
    _, metadata = read_object(root, metadata_name)
    lock = read_bytes(root, "requirements-dev.txt", 1048576)
    expected: dict[str, Json] = {
        "repository_name": "SPIKE-FORMAT-BRIDGE",
        "owner_group": "SC-NEUROMORPHIC-COMPUTING-SYSTEMS",
        "lifecycle": "public_repository",
        "public_remote": "https://github.com/anulum/spike-format-bridge",
        "evidence_maturity": "architecture_only",
        "capabilities": [],
        "claims": [],
        "qualified_owned_schema_ids": [],
        "planned_owned_schema_ids": ["spike_format_bridge.conversion.v1"],
        "validation_profile": PROFILE,
        "tooling_python": {
            "design_baseline": "3.13",
            "actual_version": "3.13.16",
            "supported_range": ">=3.13.16,<3.14",
            "development_lock_sha256": hashlib.sha256(lock).hexdigest(),
        },
        "domain_runtime_dependencies": [],
    }
    if metadata != expected:
        raise CheckFailure("metadata_mismatch", metadata_name)


def validate_metadata(root: Path) -> tuple[Report, dict[str, object] | None, bytes]:
    """Expose accepted original declarations to the acyclic inventory pipeline.

    Parameters
    ----------
    root : Path
        Repository supplying the original schema, metadata and exact lock.

    Returns
    -------
    tuple[Report, dict[str, object] or None, bytes]
        Canonical scoped result and usable original bytes only after acceptance.
        No generated inventory is required or inspected.
    """
    report = Report("repository_metadata", [])
    try:
        verify(root)
        raw, metadata = read_object(root, "repository-domain.json")
        return report, cast(dict[str, object], metadata), raw
    except CheckFailure as error:
        report.findings.append(
            Finding(
                error.code,
                error.location,
                "Repository declaration could not be accepted.",
                error.exit_code,
            )
        )
    return report, None, b""

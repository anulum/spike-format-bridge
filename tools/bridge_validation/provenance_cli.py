# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — maintained source provenance

"""Expose maintained source provenance through the public repository command."""

from collections.abc import Sequence

from .command import run
from .provenance import verify


def main(argv: Sequence[str] | None = None) -> int:
    """Check source notices and original byte identities with scoped results.

    Parameters
    ----------
    argv : Sequence[str] or None
        Explicit command arguments, or native process arguments.

    Returns
    -------
    int
        Zero for a match, two for refusal, three for unavailable input.
        Invalid arguments exit four; help exits zero.
    """
    return run(
        "source_provenance",
        verify,
        argv,
        description="Check Spike Format Bridge maintained source provenance.",
    )

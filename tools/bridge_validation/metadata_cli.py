# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SPIKE-FORMAT-BRIDGE — repository metadata validation

"""Expose the repository declaration check through its public command."""

from collections.abc import Sequence

from .command import run
from .metadata import verify


def main(argv: Sequence[str] | None = None) -> int:
    """Check declarations and report the actual bounded validation outcome.

    Parameters
    ----------
    argv : Sequence[str] or None
        Explicit command arguments, or the native process arguments.

    Returns
    -------
    int
        Zero for matching declarations, two for refusal, three for unavailable
        inputs. Invalid arguments exit four; help exits zero.
    """
    return run(
        "repository_metadata",
        verify,
        argv,
        description="Check Spike Format Bridge repository metadata declarations.",
    )

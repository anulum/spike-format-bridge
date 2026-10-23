<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Planned capabilities

The current implementation concerns local repository declarations and source
provenance. Remaining foundation work includes workflow policy, dependency
alignment, documentation, repository inventory and preflight checks.

The planned conversion library will cover selected directions for AEDAT3/4,
jAER2, RAW/EVT2/3, documented HDF5 layouts, N-MNIST, CSV/NPY/NPZ, NWB import and
Spike Log. NWB export and live capture are outside the initial boundary.

Conversion will preserve declared event ordering and source-scoped stream
identities. Timestamp transformations will use exact source values followed by
one explicit quantisation step. Spatial, polarity and deduplication transforms
will produce located loss accounting.

The library and command line will expose discovery, inspection, conversion,
verification and comparison. Whole logical round trips, chunk invariance,
bounded resources, recovery and genuine downstream consumption are required
before the corresponding capability is declared available.

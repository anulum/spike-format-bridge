<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Repository architecture

The current executable surfaces validate local metadata, source provenance,
workflow policy, installed dependencies, rendered documentation and inventory;
preflight aggregates their actual results. The metadata
public command delegates to a bounded JSON reader and fixed declaration policy.
It does not require generated capability inventory, preventing a bootstrap cycle.

Source provenance reads the actual Git-maintained file cohort and verifies its
notices, JSON sidecars and selected original legal and branding byte identities.

The planned domain flow is described in [the detailed architecture](docs/ARCHITECTURE.md).
Repository validation and conversion evidence are separate interfaces.

<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Separate conversion ownership from capture and evidence sealing

Status: accepted repository boundary.

Spike Format Bridge is a standalone recording-conversion repository. It will own
codec mappings, canonical event transformations, whole logical comparisons and
located loss accounting. Capture remains with Spike Log; shared evidence
sealing remains with Evidence Manifest Toolkit.

Current code implements repository declarations only. Domain modules and
capabilities will be added with their complete real entry points, native
documentation and tests. A reserved format name or an empty capability inventory
does not qualify a reader, writer or downstream consumer.

This boundary permits independent installation and evolution of codecs while
keeping native recording and shared verification contracts under their owners.

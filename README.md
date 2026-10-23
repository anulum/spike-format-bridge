<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Spike Format Bridge

Spike Format Bridge is being built to convert neuromorphic recordings with
explicit accounting of timestamp changes, omitted streams and other losses.

Current maturity is **architecture only**. The repository contains local repository validation tooling and its tests. Recording readers, writers, conversion commands and a
distributable domain package are planned.

The intended flow is a source reader, integer event chunks, explicit transforms,
a destination writer and independent round-trip verification. Evidence sealing
belongs to Evidence Manifest Toolkit; native recording containers belong to
Spike Log. Required unrepresentable streams must make a conversion infeasible.

For development, use Python 3.13.16 and the hash-locked tools described in
[CONTRIBUTING](CONTRIBUTING.md). The metadata and source commands are:

```sh
.venv/bin/python tools/check_repository_metadata.py --root . --json
.venv/bin/python tools/check_source_provenance.py --root . --json
```

Additional commands validate workflows, exact installed dependencies, rendered documentation and the complete inventory; preflight aggregates actual outcomes. These results concern repository infrastructure. See [VALIDATION](VALIDATION.md) for
scope and exit codes, and [ROADMAP](ROADMAP.md) for planned functionality.

Code is licensed under [AGPL-3.0-or-later](LICENSE). Commercial licensing is
available from Miroslav Šotek through [ANULUM](https://www.anulum.li).
Report sensitive issues through the contact in [SECURITY](SECURITY.md).

The reservation below was added to this repository on 2026-10-20.

## Text and data mining reservation

The rightsholder, Miroslav Šotek (ANULUM), expressly reserves the use of the
works in this repository for text and data mining, including the collection of
this content for, and its use in, training, fine-tuning or evaluating machine
learning and artificial intelligence models, in accordance with Article 4(3) of
Directive (EU) 2019/790 and the national provisions transposing it.

No permission for such use has been granted beyond what the licence in
`LICENSE` grants. This reservation does not change that licence: uses the
licence permits remain permitted on its terms, including its attribution and
share-alike conditions.

Reservation made on 2026-10-19. Requests for permission: contact the
rightsholder through the contact listed in this repository.

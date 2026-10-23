<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Contributing to Spike Format Bridge

Development currently concerns repository validation infrastructure. Changes to
recording codecs will also require original format documentation, explicit
recording rights and whole-population reference results.

Use Python 3.13.16 and uv 0.13.4. Create a separate environment and install the
complete hashed development lock (all tools are development-only):

```sh
UV_LINK_MODE=hardlink uv venv --python 3.13.16 .venv
UV_LINK_MODE=hardlink uv pip sync --python .venv/bin/python --require-hashes --build-constraints requirements-dev.txt requirements-dev.txt
.venv/bin/python -m ruff check tools tests
.venv/bin/python -m ruff format --check tools tests
.venv/bin/python -m mypy --strict tools tests
```

uv should hard-link packages from a cache on the same filesystem. Keep temporary
files, coverage data and build output under the ignored .tool-cache directory.

Run the dedicated test module for the changed public contract. The metadata
module is exercised with tests/test_repository_metadata.py; its child processes
invoke the real command. Measure both statement and branch coverage, including
the child processes. Do not substitute helper-only assertions for CLI behaviour.

Keep changes cohesive, fully typed and documented. Report actual command exits,
input identities and remaining limitations. Preserve original recording bytes,
stream identities and declared clocks. A conversion verdict needs actual
reader/writer and consumer evidence before it can be documented as supported.

Use the current local main branch and explicit task-owned paths. Run installed
pre-commit hooks on commits. Publication, external services, recording capture
and device operations require separate authorisation.


Regenerate the own complete hash lock with the same exact direct inputs:

    .venv/bin/uv pip compile requirements-dev.in --python .venv/bin/python --generate-hashes --no-header --no-annotate --output-file .tool-cache/generated-lock.txt

Retain the native seven-line provenance header when reviewing the generated lock.
Changed package bytes require renewed source/licence and installed metadata
observations, metadata lock identity and capability inventory; a dependency
update cannot be accepted by copying another environment.

The make native-tools target downloads the two fixed upstream archives, verifies
archive and executable checksums, and exposes the exact local actionlint and
secret scanner. The metadata, source, workflows, dependencies, docs, inventory,
lint and types Make targets run their named actual checks. The preflight target
selects the full local-scaffold profile; complete suites remain subject to the
active execution policy. These commands do not publish, deploy, commit, upload
or qualify recording codecs.

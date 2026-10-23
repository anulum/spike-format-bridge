<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Repository validation interfaces

Run the actual public command from the repository root:

```sh
.venv/bin/python tools/check_repository_metadata.py --root . --json
```

The command accepts the explicit input root or uses the current directory.
Without --json it prints a short human result. Help exits zero; invalid arguments
exit four without reflecting received argument values.

A declaration match exits zero, refused content exits two and missing input
exits three. Reports identify only local declaration scope. Unknown capabilities
and claims cannot be introduced by editing metadata or generated inventory.

The checker is read-only and accepts a complete declaration set before any
inventory exists. It binds the selected schema bytes and lock digest.
Installed dependency alignment, licence provenance and complete repository
acceptance require their separate checks.

## Native Python interfaces

::: bridge_validation.metadata.verify

::: bridge_validation.metadata_cli.main

::: bridge_validation.inputs.CheckFailure

::: bridge_validation.inputs.read_bytes

::: bridge_validation.inputs.read_object

::: bridge_validation.command.run

## Maintained source provenance

The source command validates notices and selected original legal and asset bytes
through the actual Git-maintained cohort:

```sh
.venv/bin/python tools/check_source_provenance.py --root . --json
```

It includes nonignored untracked files and retains unavailable deleted tracked
paths. An ignored sidecar cannot qualify JSON in the maintained source cohort.
Its declaration, source, unavailable-input and argument exits are scoped to
source provenance; they do not qualify recording formats or installed tools.

::: bridge_validation.provenance.verify

::: bridge_validation.provenance_cli.main

## Complete infrastructure commands

The other real commands and result boundaries are described in
the repository-root VALIDATION.md. Inventory creation needs an explicit
new output and never requires its own prior generated file; verification is
read-only. All machine reports use gate/scope/status/reasons with actual native
exit codes and caller-safe authored diagnostics. The original declaration and
source verifiers retain their finding codes and human mode.

## Actual native workflow composition

The coordinator runs eight real native jobs, four complete category gates and
the stable required gate. Exact source bindings compare expanded jobs with their
maintained standalone sources. Missing descendants, changed executable commands,
masked non-success results, workflow calls and job-level secret inheritance
refuse. Both actual native linters inspect the real workflow files.

::: bridge_validation.capabilities

::: bridge_validation.ci_dependencies

::: bridge_validation.cli

::: bridge_validation.dependencies

::: bridge_validation.dependency_lock

::: bridge_validation.dependency_records

::: bridge_validation.documentation

::: bridge_validation.execution

::: bridge_validation.native_tools

::: bridge_validation.paths

::: bridge_validation.preflight

::: bridge_validation.preflight_cli

::: bridge_validation.provenance_policy

::: bridge_validation.report

::: bridge_validation.structure

::: bridge_validation.validation_profile

::: bridge_validation.workflows

::: bridge_validation.yaml_input

::: bridge_validation.metadata.validate_metadata

::: bridge_validation.inputs.read_file

::: bridge_validation.inputs.read_json

::: bridge_validation.inputs.parse_json

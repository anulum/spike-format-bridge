<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SPIKE-FORMAT-BRIDGE — repository foundation
-->

# Validation scope

The available repository metadata checker validates a closed local descriptor,
the exact selected metadata schema, declared ownership and maturity, empty
capabilities and claims, the selected validation profile and development-lock
byte identity.

```sh
.venv/bin/python tools/check_repository_metadata.py --root . --json
```

It operates before inventory generation and never reads or creates
capability-inventory.json. Schema acceptance and a matching lock hash are
declaration checks; installed packages and recording-format behaviour require
their own checks.

| Exit | Meaning |
| --- | --- |
| 0 | Complete metadata declaration check passed |
| 2 | Authored input or declaration refusal |
| 3 | Required input unavailable |
| 4 | Invalid command arguments |

Machine reports contain gate, scope, status and locating reasons. The scope is
local_scaffold_infrastructure; native process exits remain authoritative. This
initial protocol replaces the earlier uncommitted declaration/source report shape.
Malformed JSON, duplicate keys, nonfinite numbers, invalid Unicode and excessive
nesting are refused. Metadata and schema inputs have a 65,536-byte bound; the
development lock has a 1,048,576-byte bound. Inputs are read without rewriting.

The dedicated tests exercise the public command, whole input preservation,
identity and policy changes, unavailable inputs, exact byte limits and bootstrap
without an inventory. Source checks cover tools and tests with strict mypy,
Ruff, formatting and NumPy-style API documentation.

## Maintained source provenance

```sh
.venv/bin/python tools/check_source_provenance.py --root . --json
```

This command checks the actual tracked and nonignored untracked source cohort
through native Git, with filesystem-monitor execution disabled. Deleted tracked
files remain unavailable. Symlink entries are refused before their targets are
read. Every selected JSON source needs its exact sidecar in the same cohort.

Project notice fields, invisible Markdown headers and JSON sidecar copyright
records are checked. Original GNU licence text, selected branding assets and the
REUSE annotation policy have fixed byte identities. Source text and JSON have a
1,048,576-byte limit; sidecars have an 8,192-byte limit. Each known binary asset
has its own exact original size and digest.

Ignored files are outside this provenance cohort. Complete repository inventory,
private projection and installed dependency checks remain separate obligations.
The source command uses the same exit meanings as the metadata command, with
scope `local_scaffold_infrastructure`.

Full recording conversion remains planned. No domain capability or scientific
acceptance follows from these infrastructure results.

## Other repository controls

| Command below tools/ | What the complete named result covers |
| --- | --- |
| check_workflow_policy.py --root . --json | Actual workflow taxonomy, immutable sources, source-equal native jobs, category results, bounded authority and triggers |
| check_dependency_alignment.py --root . --json | Exact direct inputs, complete hashed graph, actual installed metadata/licences and native tool/hook/CI parity |
| check_documentation.py --root . --json | Actual local links/anchors, strict native render and private/public projection |
| check_repository_inventory.py --root . --json | Complete required/forbidden paths and deterministic empty capability inventory bound to current metadata |
| preflight.py --root . --profile local-scaffold --json | Every actual configured child outcome, preserving failed, unavailable and invalid results |

Inventory generation is a distinct operation: --mode generate --output new.json
creates only a new caller-owned relative path, before a complete inventory exists.
Verification is read-only and never replaces an existing output. Both consume the
original metadata verifier, keeping bootstrap acyclic.

New controls use zero only for the named result, two for refusal, three for
unavailable and four for invalid invocation/configuration. Required outcomes are
never inferred from absent child reports. A failed report write returns three.

Nine workflow files implement eight native CI leaf jobs, four category gates and
the required aggregate. Twelve exact source equalities bind expanded jobs to
their standalone leaf sources. Both actual native workflow linters inspect these
files; hosted execution and service settings remain unqualified. CodeQL prepares
local analysis without uploading results. Documentation and SBOM jobs build local
artefacts without publishing. No badge or public service result is inferred.

All maintained Python under tools and tests belongs to the full statement/branch
coverage denominator, with no exclusions. Dedicated cohorts exercise real CLI,
file, Git, renderer, installed-package and bounded child-tool behaviour. Original
recording reference failures, codec directions and numerical contracts require
their own complete implementation and independent validation.

# SRWF CI Runtime Lab — Execution Procedure

This procedure implements `docs/authority/CI_RUNTIME_LAB.md` without changing the product/runtime authority model.

## Invocation

The initial workflow is `.github/workflows/ci-runtime-lab.yml`.

It runs automatically only when the Lab workflow or `tests/runtime-lab/**` changes, and it is also manually dispatchable. This keeps the real-runtime probe reproducible without running it for unrelated documentation-only edits.

For manual dispatch, `scaffold_url` may point to an Owner-authorized public copy of the exact candidate. The URL itself is not treated as identity: the downloaded bytes must match the pinned candidate SHA-256 before runtime setup proceeds.

## Runtime cell

The first cell reuses the established GPP disposable-runtime shape:

- GitHub-hosted `ubuntu-24.04` runner;
- pinned MariaDB container service;
- exact PHP runtime;
- pinned WP-CLI phar;
- exact WordPress version;
- authentic Owner-authorized Gravity Forms package pinned by exact version, size and SHA-256;
- no persistent service and no staging/network control plane.

The form is imported through Gravity Forms' own `GFExport::import_file()` path, explicitly kept inactive, and read back through `GFAPI`.

## Source-defined settings verification

`LAB_PASS` requires the exact scaffold hash plus successful real import/read-back assertions. The source-to-runtime verifier compares source-defined form and field settings against authentic GFAPI read-back. Source-defined `confirmations` and `notifications` are included in that form-setting projection; they are not blanket-excluded. Only demonstrated runtime-owned form identity/state properties are excluded, and fields are verified separately.

The focused verifier self-test proves confirmation drift and notification drift produce `LAB_FAIL`, while an intentionally different runtime-owned form identity/state value remains acceptable. The current exact scaffold must still pass this stricter verifier.

## Canonical terminal evidence

All reachable Lab phases have stable step IDs. `tests/runtime-lab/finalize-evidence.py` runs with `if: always()` before summary/upload/enforcement and is the sole terminal evidence finalizer:

- a valid scenario evidence file is preserved when phase outcomes are consistent with it;
- exact-input/admission and pre-runtime dependency blockers become machine-readable `LAB_BLOCKED`;
- runtime/import/assertion/guard defects become machine-readable `LAB_FAIL`;
- missing or corrupt terminal evidence becomes `LAB_FAIL` and cannot be green;
- the finalizer never manufactures `LAB_PASS`.

The finalizer writes or preserves one canonical `lab-evidence.json` and records its SHA-256. GitHub Step Summary and final enforcement verify and consume that same file; the artifact upload includes that file and its checksum. `LAB_BLOCKED` and `LAB_FAIL` remain failing job outcomes.

The harness includes deliberately broken verifier cases. The guards must reject bad expectations; accepting one is a workflow failure.

GitHub-hosted runner or service-container failures that occur before any repository step can execute are outside the reachable in-workflow finalization boundary; no repository code can materialize an artifact before checkout/step execution exists. This limit is not represented as Lab PASS.

## Scope boundaries

- No real PII or operational production data.
- No Implementation Mapping writes from CI IDs.
- No finance/manual-cheque behavior or GP Nested Forms cheque POC.
- No claim that plugin-specific runtime behavior is proven merely because unknown/custom field properties survived Gravity Forms import serialization.
- No staging claim until real staging is executed.

After a true `LAB_PASS`, the next justified operation is the governed real staging import/read-back of the same candidate, still inactive and synthetic-only.

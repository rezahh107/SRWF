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

## Evidence contract

Machine-readable evidence is uploaded for every run that reaches the evidence step, including blockers. Human-readable GitHub Step Summary is derived from the same evidence.

`LAB_PASS` requires the exact scaffold hash plus successful real import/read-back assertions. The verifier compares source-defined form and field settings to runtime read-back and records generated CI IDs while marking them non-authoritative.

The harness includes a deliberately broken read-back assertion check. The guard must reject the bad expectation and emit `LAB_FAIL`; accepting it is a workflow failure.

`LAB_BLOCKED` is a failing job outcome, not a green skip. The current admission layer records why runtime could not be exercised and does not manufacture substitute evidence.

## Scope boundaries

- No real PII or operational production data.
- No Implementation Mapping writes from CI IDs.
- No finance/manual-cheque behavior or GP Nested Forms cheque POC.
- No claim that plugin-specific runtime behavior is proven merely because unknown/custom field properties survived Gravity Forms import serialization.
- No staging claim until real staging is executed.

After a true `LAB_PASS`, the next justified operation is the governed real staging import/read-back of the same candidate, still inactive and synthetic-only.

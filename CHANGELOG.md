# Changelog

All material SRWF documentation/contract changes are recorded here. Runtime implementation evidence remains in `SRWF_RUNTIME_STATE` and validation artifacts; this file does not promote runtime status.

## Unreleased — repository baseline

### Added
- Stable repository entrypoints: `README.md`, `AGENTS.md`, `repository.manifest.yaml`.
- Stable active authority/playbook/governance paths.
- Standalone machine-readable and human-readable Semantic Field Contract.
- Workflow, access-control, environment, privacy/retention and Implementation Mapping contracts.
- Validation/POC/DoD and release/rollback artifacts.
- Runtime SSOT boundary and non-canonical snapshot area.
- Byte-exact pre-repository source corpus `01..11` in `history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz` with per-source provenance hashes.
- Repository integrity validator and GitHub Actions workflow.

### Corrected
- Preserved `home_phone` as `include_in_form: true` while keeping `value_required: false`.
- Preserved explicit `father_name` and `student_mobile` field requirements.
- Repaired stale Master/Playbook/Addendum/Owner-Comprehension/Overlay pointers by using stable repository paths.
- Normalized Product Knowledge/Constructability retrieval to provenance archive materialization instead of nonexistent `.txt.gz` or `knowledge/products/` paths.

### Validation note
- GitHub Actions runs were observed failing before runner allocation (`runner_id=0`, no steps executed); this is classified as CI infrastructure unavailable, not validator failure.
- Repository-baseline acceptance therefore uses the documented manual-equivalent integrity fallback: complete tree/read-back, exact uploaded archive Git blob identity matched to locally SHA/member-verified archive, contract invariant checks, Mapping/SSOT checks, stale-pointer audit, and PII/operational-ledger path audit.
- This validation concerns documentation/repository integrity only. It does not promote `V-01..V-06`, staging behavior, production readiness, or any runtime POC.

## Pre-repository history

Earlier version-suffixed source documents are retained byte-exact in the provenance archive and Git history. They are historical/reference sources unless the current repository authority chain makes them applicable.

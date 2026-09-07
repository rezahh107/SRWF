# Changelog

All material SRWF documentation/contract/runtime-governance changes are recorded here. Runtime evidence is canonical only when reflected in `runtime/CURRENT_STATE.yaml` and appended to `runtime/DECISION_HISTORY.jsonl`; documentation alone does not promote validation status.

## Unreleased — repository runtime SSOT migration

### Added
- Canonical `runtime/CURRENT_STATE.yaml` for current Stage/Gate/decision/candidate/result/blockers/next action.
- Append-only `runtime/DECISION_HISTORY.jsonl` for post-cutover material runtime events.
- Runtime schemas under `runtime/schemas/`.
- Complete pre-cutover Decision History archive as immutable JSONL chunks under `history/pre-runtime-ssot/`, with `DECISION_HISTORY_INDEX.json` and `MIGRATION_MANIFEST.json`.
- Repository-first agent boot/read/write rules so a future session can continue from GitHub `main` without relying on chat memory or Google Sheets.

### Changed
- GitHub `main` becomes the sole project/runtime SSOT after accepted migration merge + read-back.
- Google Sheet `SRWF_RUNTIME_STATE` becomes `DEPRECATED_READ_ONLY_MIGRATION_SOURCE` after cutover; no dual-write is allowed.
- `README.md`, `AGENTS.md`, `repository.manifest.yaml`, Master, Playbook, Decision Ledger and documentation index now point current execution work to `runtime/CURRENT_STATE.yaml`.
- Runtime state writes require updating `CURRENT_STATE` and appending the corresponding decision/probe event in the same accepted Git change, followed by main read-back.

### Removed
- Old `runtime/snapshots/` state files that identified Google Sheets as live SSOT and would create a stale parallel-state surface after cutover.

### Preserved truth
- This governance migration does not promote `V-01..V-06`, staging validation, production readiness, or any POC.
- Current implementation resumes at the existing `v0.5` `finance_status` semantic mismatch; privacy/retention and residual environment/server-binding gaps remain open.

## Repository documentation baseline

### Added
- Stable repository entrypoints: `README.md`, `AGENTS.md`, `repository.manifest.yaml`.
- Stable active authority/playbook/governance paths.
- Standalone machine-readable and human-readable Semantic Field Contract.
- Workflow, access-control, environment, privacy/retention and Implementation Mapping contracts.
- Validation/POC/DoD and release/rollback artifacts.
- Byte-exact pre-repository source corpus `01..11` in `history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz` with per-source provenance hashes.
- Repository integrity validator and GitHub Actions workflow.

### Corrected
- Preserved `home_phone` as `include_in_form: true` while keeping `value_required: false`.
- Preserved explicit `father_name` and `student_mobile` field requirements.
- Repaired stale Master/Playbook/Addendum/Owner-Comprehension/Overlay pointers by using stable repository paths.
- Normalized Product Knowledge/Constructability retrieval to provenance archive materialization instead of nonexistent `.txt.gz` or `knowledge/products/` paths.

### Validation note
- GitHub Actions runs were observed failing before runner allocation (`runner_id=0`, no steps executed); this is classified as CI infrastructure unavailable, not validator failure.
- Repository-baseline acceptance therefore used documented manual-equivalent integrity evidence.
- This validation concerns repository integrity only. It does not promote runtime behavior or release readiness.

## Pre-repository history

Earlier version-suffixed source documents are retained byte-exact in the provenance archive and Git history. They are historical/reference sources unless the current repository authority chain makes them applicable.

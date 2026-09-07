# Changelog

All material SRWF documentation/contract/runtime-governance changes are recorded here. Runtime evidence is canonical only when reflected in `runtime/CURRENT_STATE.yaml` and appended to `runtime/DECISION_HISTORY.jsonl`; documentation alone does not promote validation status.

## Unreleased — portable project package v1.1.0

### Added
- Reproducible portable project-package profile under `bundle/`.
- Repository-first `02_PROJECT_INSTRUCTIONS.md` for ChatGPT Projects / similar model environments.
- Deterministic `scripts/build_project_bundle.py` with sorted ZIP paths, fixed metadata, per-file SHA-256 manifest/checksum, packaged validation evidence and exact-artifact handling.
- GitHub Actions workflow `.github/workflows/project-bundle.yml` that validates the repository, builds the package and uploads the ZIP + SHA-256.
- Product/Constructability sources `04..09` are materialized from the exact pre-repository archive into the portable package at build time.
- Pre-cutover runtime history is included as immutable provenance; live runtime state remains GitHub `main`.

### Package boundary
- Package version: `1.1.0`.
- Profile: `BUNDLE_PACKAGE_MAKER_5_COMPATIBILITY`.
- Formal Package Maker 5 specification: `NOT_RETRIEVED`; compatibility is based on observed GPT Project package and repository-first portable-bundle conventions, not a false claim of formal conformance.
- ZIP/runtime snapshot never supersedes GitHub `main` when the repository is available.
- An artifact named/hash-recorded in runtime history is embedded only when exact hash-matching bytes exist in the repository; otherwise it remains `REFERENCED_NOT_EMBEDDED`.

### Current runtime truth at package work start
- `GF_IMPORT_SCAFFOLD_V051_PROVISIONAL` is the current candidate.
- v0.5.1 `finance_status` local semantic/structural audit = PASS.
- Actual Gravity Forms staging import remains `UNEXECUTED`.
- Current next action is synthetic-data staging import of `SRWF_GravityForms_Import_v0.5.1_PROVISIONAL.json` while the form remains inactive.

## Repository runtime SSOT migration

### Added
- Canonical `runtime/CURRENT_STATE.yaml` for current Stage/Gate/decision/candidate/result/blockers/next action.
- Append-only `runtime/DECISION_HISTORY.jsonl` for post-cutover material runtime events.
- Runtime schemas under `runtime/schemas/`.
- Complete pre-cutover Decision History archive as immutable JSONL chunks under `history/pre-runtime-ssot/`, with `DECISION_HISTORY_INDEX.json` and `MIGRATION_MANIFEST.json`.
- Repository-first agent boot/read/write rules so a future session can continue from GitHub `main` without relying on chat memory or Google Sheets.

### Changed
- GitHub `main` is the sole project/runtime SSOT after accepted migration merge + read-back.
- Google Sheet `SRWF_RUNTIME_STATE` is `DEPRECATED_READ_ONLY_MIGRATION_SOURCE`; no dual-write is allowed.
- `README.md`, `AGENTS.md`, `repository.manifest.yaml`, Master, Playbook, Decision Ledger and documentation index point current execution work to `runtime/CURRENT_STATE.yaml`.
- Runtime state writes require updating `CURRENT_STATE` and appending the corresponding decision/probe event in the same accepted Git change, followed by main read-back.

### Removed
- Old `runtime/snapshots/` state files that identified Google Sheets as live SSOT.

### Validation
- PR #3 GitHub Actions integrity run `34160923750` executed and passed.
- This governance validation does not promote `V-01..V-06`, staging validation, production readiness, or any POC.

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

## Pre-repository history

Earlier version-suffixed source documents are retained byte-exact in the provenance archive and Git history. They are historical/reference sources unless the current repository authority chain makes them applicable.

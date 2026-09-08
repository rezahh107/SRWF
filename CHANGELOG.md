# Changelog

Material SRWF documentation/contract/runtime-governance changes are recorded here. Documentation does not itself promote runtime validation.

## Unreleased — event86 SFC sync / v0.6.0 scaffold

### Changed
- Synced active Semantic Field Contract to Owner decisions through `event86 / OWNER-20260908-SFC-BATCH-MAIN-FORM-CONSTRUCTION-READY`.
- Replaced stale independent `registration_status_code` with sole canonical `finance_status`; registration center is Officer-only/default center.
- Materialized current education/group/school/Bonyad/discount semantics and event85/event86 stale-data/file-lifecycle rules.
- School contract now uses the selected 946-record SchoolReport set + Other, excludes four invalid codes, requires GP Advanced Select, and locks gender+education-level filtering only.
- D-12 documentation amended narrowly: GP File Upload Pro 3:4 crop/max 1200×1600 is allowed/required; custom/background/AI processing remains forbidden.
- Current amount defaults clarified to empty; net derivation treats blank discount as zero without persisting zero.
- Privacy contract records closed primary student-file lifecycle while backup/export/log policy remains open.
- Environment/DoD/Test Matrix now include File Upload Pro and post-import read-back requirements.

### Candidate artifact evidence
- `SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json` SHA-256 `445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89`.
- `SRWF_GF_Export_Python_Mapping_v0.6.0.json` SHA-256 `0efc73af564a9035a6981a1e466d7b7bfd24f560021f2c15c29d9f138d3010c7`.
- Artifact/local structure can PASS independently; actual Gravity Forms staging import, server bindings and Gravity Flow whitelist remain unexecuted/not-proven.

## Project package v1.2.0 / AIGOV-inspired v5 runtime topology

- Runtime ZIP topology standardized to `02_PROJECT_INSTRUCTIONS.md` + `PROJECT_SOURCES/**`; build-only artifacts excluded.
- GitHub main remains live Project/Runtime SSOT; package state/history are fallback snapshots.
- Package build/integrity acceptance does not promote staging/runtime validation.

## Repository runtime SSOT migration

- Added `runtime/CURRENT_STATE.yaml` and append-only `runtime/DECISION_HISTORY.jsonl`.
- GitHub main became sole runtime SSOT after accepted cutover; Google Sheet became deprecated read-only migration provenance.
- Material runtime state writes require state+history same accepted commit and main read-back.

## Repository documentation baseline

- Added stable authority/contracts/governance/validation/release paths and preserved pre-repository provenance archive.
- Corrected `home_phone` include-vs-required semantics and preserved father/name/student-mobile requirements.

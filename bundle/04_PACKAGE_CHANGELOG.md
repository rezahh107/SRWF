# SRWF Project Package Changelog

## v1.1.0

### Changed
- Runtime/Project SSOT moved from Google Sheet to GitHub `main`.
- Added repository-first session boot through `runtime/CURRENT_STATE.yaml` and `runtime/DECISION_HISTORY.jsonl`.
- Preserved complete pre-cutover Sheet history as immutable repository provenance.
- Added explicit bundle rule: repository `main` overrides packaged state whenever repository access is available.
- Updated Owner narration rule: after each execution batch, explain simply what was done and what changed.

### Current implementation snapshot included by build
- Stage remains `STAGE_0_IN_PROGRESS`.
- Semantic Field Contract is closed.
- Current candidate is `GF_IMPORT_SCAFFOLD_V051_PROVISIONAL`.
- `finance_status` v0.5.1 local semantic/structural audit passed.
- Actual Gravity Forms staging import remains `UNEXECUTED`.
- Current next action is staging import of v0.5.1 with synthetic data only.

### Qualification
- This package does not promote `V-01..V-06`, staging validation, release authorization, or production readiness.
- Exact v0.5.1 artifact bytes are embedded only if present and hash-matching in the source repository at build time; otherwise they are listed as `REFERENCED_NOT_EMBEDDED`.
- `BUNDLE_PACKAGE_MAKER_5_COMPATIBILITY` is an observed-convention compatibility profile because the formal Package Maker 5 specification was not retrieved during this build.

# Changelog

همهٔ تغییرات مادی SRWF در این فایل و Git history ثبت می‌شوند. این فایل جایگزین Decision Ledger نیست.

## Unreleased — Repository Baseline Migration

### Added
- repository governance baseline (`README.md`, `AGENTS.md`, `repository.manifest.yaml`).
- standalone Semantic Field Contract با تفکیک `include_in_form` از `value_required`.
- standalone workflow/access/environment/privacy/implementation contracts.
- validation/release artifact skeletons required by Master.
- repository integrity checks and PII guardrails.
- classified reference knowledge/provenance layout.

### Normalized
- active internal pointers use stable repository paths instead of version-suffixed filenames.
- corrected stale Master dashboard label from `1.8.1` to current `1.9.0` in repository materialization.
- current Overlay path normalized to `knowledge/constructability/APPLICABILITY_OVERLAY.md`.

### Owner decisions included
- `father_name` required.
- `first_name` and `last_name` required.
- `student_mobile` required; contact mobiles optional.
- `home_phone` must exist in the public form but its value is optional; this supersedes the earlier ambiguous required-value interpretation.
- finance/manual-cheque fields current-release optional, non-public, Registration-Officer-only.
- scanner path deferred; seven Sayad outputs hidden/future-reserved.
- SRWF repository becomes canonical documentation/contracts home after baseline merge; `SRWF_RUNTIME_STATE` remains live operational-state SSOT.

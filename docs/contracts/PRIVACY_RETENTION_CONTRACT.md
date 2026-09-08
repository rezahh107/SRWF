# Privacy & Retention Contract

**Status:** `OWNER_DECISION_REQUIRED / PARTIAL_FILE_LIFECYCLE_BOUND`  
**Gate effect:** blocks **real PII** in staging/UAT/production; synthetic scaffold/POCs remain allowed.

## Data classes requiring explicit policy

1. Student identity PII.
2. Student files — photo, report card.
3. Education/school data.
4. Financial data.
5. Cheque data.
6. Workflow history.
7. GravityRevisions history.
8. backups/exports/logs containing any of the above.

## Owner bindings still required

For each class: purpose/need, role access, retention duration, deletion/anonymization trigger, backup retention, export/download policy, incident/revocation behavior, and staging/UAT copied-production policy.

## Closed primary-file lifecycle — event85/event86

For `student_photo` and `report_card_file` primary Gravity Forms storage:

- access remains Admin + Registration Officer only.
- replacing a file uses safe replace: persist/bind new file first; only then physically delete old file. On failure, keep old file.
- when `report_card_file` becomes inapplicable, clear the Entry value and physically delete that primary file.
- moving an Entry to Trash retains these primary files.
- permanent Entry deletion physically deletes `student_photo` and `report_card_file` primary files.
- **backup/export/log retention is still OPEN** and is not implied by primary-file deletion.

## Current hard rules

- synthetic data only until this contract is fully Owner-approved.
- finance/manual-cheque fields are non-public and Registration-Officer-only.
- raw Structured Scanner QR payload must not persist.
- repository contains no real PII/intake images/real operational exports.

## Closure

Overall Privacy/Retention becomes `OWNER_APPROVED` only after the remaining Owner bindings, especially backup/export/log retention, are explicitly signed off. The event85/event86 primary-file lifecycle is CLOSED but does not close the full privacy Gate.

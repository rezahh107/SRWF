# Privacy & Retention Contract

**Status:** `OWNER_DECISION_REQUIRED`  
**Gate effect:** blocks **real PII** in staging/UAT/production; does not block synthetic scaffold/POCs.

## Data classes requiring explicit policy

1. Student identity PII — name, father name, National ID, mobile/home/contact phones, DOB, gender.
2. Student files — photo, report card.
3. Education/school data.
4. Financial data — tuition/discount/net payable.
5. Cheque data — manual cheque fields and future Sayad identifiers.
6. Workflow history — approvals, review fields, timestamps.
7. GravityRevisions human-edit history.
8. backups/exports/logs containing any of the above.

## Owner bindings still required

For each class define:

- purpose / lawful organizational need
- roles allowed to view/edit
- retention duration
- deletion/anonymization trigger
- backup retention behavior
- export/download policy
- incident/revocation behavior
- whether staging/UAT may ever use copied production data

## Current hard rules

- synthetic data only until this contract is approved.
- student photo/report-card access is currently limited to Admin + Registration Officer.
- finance/manual-cheque fields are non-public and current-release Registration-Officer-only when exposed.
- raw Structured Scanner QR payload must not persist.
- repository must contain no real PII/intake images/real operational exports.

## Closure

This contract becomes `OWNER_APPROVED` only after explicit Owner sign-off. Documentation of a proposal is not approval.

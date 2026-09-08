# Environment Manifest

**State:** `PARTIAL / OWNER_ACCEPTED_FOR_PROGRESS`  
**Meaning:** enough environment evidence exists to continue Stage 0/scaffold, but this is not a completed compatibility PASS.

## Confirmed project/runtime facts

| Item | Observed/decision state | Confidence |
|---|---|---|
| Platform | WordPress | CONFIRMED project parent |
| Data authority | Gravity Forms | OWNER_LOCKED |
| Workflow authority | Gravity Flow | OWNER_LOCKED |
| PersianGravity | 4.1.0 installed/tested by Owner; no problem observed in unspecified smoke scope | OWNER_REPORTED_SMOKE_PASS; FULL_VALIDATION_NOT_PROVEN |
| GP Nested Forms entitlement/install | not yet bound here | NOT_PROVEN |
| GP File Upload Pro entitlement/install | required by event86 student_photo contract; exact target version/license/settings not yet read back | NOT_PROVEN |
| Gravity PDF Free runtime | selected first POC candidate; target PASS not executed | NOT_PROVEN |
| GravityRevisions target behavior | selected; V-04 unexecuted | NOT_PROVEN |
| WP All Import counter sync | selected by D-15/D-16; V-06 unexecuted | NOT_PROVEN |

## Required target inventory before release

Populate from real target environment, not vendor-latest assumptions:

- WordPress exact version
- PHP exact version
- database engine/version
- Gravity Forms exact version
- Gravity Flow exact version
- GravityView exact version if installed/used
- GravityRevisions exact version/license
- WP All Import + GF add-on exact version/license
- Gravity Perks + Nested Forms exact version/license/entitlement
- GP File Upload Pro exact version/license/entitlement and post-import 3:4 / 1200×1600 setting read-back
- PersianGravity exact installed build/commit/version
- Gravity PDF exact version if POC proceeds
- active theme
- cache/optimizer/CDN configuration
- staging identity
- production identity
- server upload/memory/execution limits relevant to files/PDF

## Gate meaning

- Missing residual inventory does **not** reopen the closed Semantic Field Contract.
- If a compatibility/license/cache/build-identity fact later becomes decision-critical, reopen only that environment sub-unit.
- Vendor current/latest documentation is not proof of installed target version.

## PII boundary

Environment probing/scaffold uses synthetic data until Privacy/Retention Contract is approved.

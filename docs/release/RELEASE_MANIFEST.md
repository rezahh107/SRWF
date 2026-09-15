# SRWF Release Manifest

## Scope
This artifact tracks release-document readiness. It does not authorize release by itself.

## Current status

`RELEASE_STATUS = NOT_READY`

Repository documentation baseline acceptance does not mean SRWF runtime release readiness.

## Scope applicability

After `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC`, finance/manual-cheque implementation is suspended until explicit Owner reopen. Preserved finance fields/semantics may remain in the contract/scaffold, but finance-specific validation and `PRB-NESTED-CHEQUE-001` are not current release blockers. Daily manager SMS is recorded for future implementation and is not a current release gate until explicitly activated by the Owner.

## Required before release

- [ ] Semantic Field Contract current and mapped to actual scaffold IDs for active scope.
- [ ] Environment Manifest confirmed for target deployment.
- [ ] Implementation Mapping bound/read-back from actual runtime for active scope.
- [ ] Required `V-01..V-06` executed with evidence.
- [ ] `D-17` print POC closed for selected production renderer.
- [ ] Privacy/retention Owner sign-off before real PII.
- [ ] Test Matrix / Definition of Done executed for active scope.
- [ ] Rollback Runbook verified for deployment scope.
- [ ] Production release authorization recorded separately from validation.

## Deferred / not current release gates

- `PRB-NESTED-CHEQUE-001` — `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN`.
- finance-specific Flow whitelist, amount/discount derivation/validation, Bonyad/Hekmat bindings, cheque composition, POS/PC-POS and Sayad work — suspended/deferred until Owner reopen.
- `REQ-DAILY-MANAGER-SMS` — requirement recorded, implementation unselected; becomes a release gate only after explicit Owner activation.

## Repository baseline note

The repository may become the Accepted Current durable documentation/contracts corpus after its baseline is merged to `main` and read back. That event is **documentation-governance acceptance only** and must not be represented as staging validation, production readiness, publication or release authorization.

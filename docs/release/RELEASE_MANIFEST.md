# SRWF Release Manifest

## Scope
This artifact tracks release-document readiness. It does not authorize release by itself.

## Current status

`RELEASE_STATUS = NOT_READY`

Repository documentation baseline acceptance does not mean SRWF runtime release readiness.

## Required before release

- [ ] Semantic Field Contract current and mapped to actual scaffold IDs.
- [ ] Environment Manifest confirmed for target deployment.
- [ ] Implementation Mapping bound/read-back from actual runtime.
- [ ] Required `V-01..V-06` executed with evidence.
- [ ] `PRB-NESTED-CHEQUE-001` PASS for current-release multi-cheque surface.
- [ ] `D-17` print POC closed for selected production renderer.
- [ ] Privacy/retention Owner sign-off before real PII.
- [ ] Test Matrix / Definition of Done executed.
- [ ] Rollback Runbook verified for deployment scope.
- [ ] Production release authorization recorded separately from validation.

## Repository baseline note

The repository may become the Accepted Current durable documentation/contracts corpus after its baseline is merged to `main` and read back. That event is **documentation-governance acceptance only** and must not be represented as staging validation, production readiness, publication or release authorization.

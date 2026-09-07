# SRWF Release Manifest

**Current status:** `NOT_RELEASE_READY`  
**Reason:** repository baseline is documentation migration only; authoritative scaffold/runtime validations/privacy sign-off are incomplete.

## Release identity

- release version: `UNASSIGNED`
- Git commit/tag: `UNBOUND`
- target environment: `UNBOUND`
- Implementation Mapping version: `UNBOUND`

## Required pre-release evidence

- [ ] Semantic Field Contract current and Owner-approved
- [ ] Implementation Mapping bound/verified to actual Form/Field/Input/Step IDs
- [ ] Environment Manifest complete for target
- [ ] Privacy/Retention Contract Owner-approved
- [ ] `V-01 PASS`
- [ ] `V-02 PASS`
- [ ] `V-03 PASS`
- [ ] `V-04 PASS`
- [ ] `V-05 PASS`
- [ ] `V-06 PASS`
- [ ] GP Nested Forms entitlement/runtime POC PASS if used in release
- [ ] D-17 print POC PASS
- [ ] staging regression PASS
- [ ] rollback exercise completed
- [ ] no real PII/secrets in repository artifacts
- [ ] current release has no POS/PC-POS/online-Sayad runtime dependency
- [ ] current release has no Scanner population dependency

## Deployment artifact inventory

Populate only when implementation exists:

- WordPress/plugin/config changes
- Gravity Forms form export(s)
- Gravity Flow workflow/config export(s) if supported/appropriate
- SRWF-owned template/integration files
- version/license prerequisites
- cache/routing requirements
- environment-specific secrets/config references (never secret values in Git)

## Authorization

A filled manifest is not release authorization by itself. Release requires Owner authorization after evidence review.

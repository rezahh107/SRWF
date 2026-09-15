# SRWF CI Runtime Lab Authority

**Authority:** current Owner decision, 2026-09-15  
**Applicability:** materially simulatable runtime work before real staging  
**Status:** approved execution-path extension; does not replace Native-First architecture or staging proof

## Decision

For SRWF runtime work that can be meaningfully simulated, the governed order is:

`approved change/runtime step → smallest useful disposable CI Runtime Lab → real staging → environment-specific confirmation as required`

The Lab is a risk-reduction and diagnosis layer. It is not a second application platform, workflow authority, staging controller, persistent executor, self-hosted runner, remote-control service, or deployment system.

A CI result must use only the bounded evidence states `LAB_PASS`, `LAB_FAIL`, `LAB_BLOCKED`, or `NOT_TESTED`. `LAB_PASS` must never be represented as `OBSERVED_IN_STAGING`, staging PASS, production proof, or production readiness.

## Current first scenario

The first admitted scenario is the exact current Gravity Forms scaffold preflight:

- candidate: `SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json`;
- pinned candidate SHA-256: `445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89`;
- synthetic data only; no production/student PII;
- imported form must remain inactive;
- verify form creation, title/settings, field structure, source-defined settings preservation, and observable disposable CI Form/Field IDs;
- disposable CI IDs are evidence only and MUST NOT be written into `docs/contracts/IMPLEMENTATION_MAPPING.yaml`;
- finance/manual-cheque behavior and `PRB-NESTED-CHEQUE-001` remain suspended/deferred and are not implemented or validated by this scenario.

## Dependency rule

Use the smallest authentic dependency set needed for the specific claim. The current import/read-back scenario requires WordPress and authentic Gravity Forms only. Gravity Flow, PersianGravity, Gravity Perks, GravityView, GNM, or other plugins are added only when a later scenario actually exercises behavior owned by them.

Externally supplied packages/artifacts must be pinned by exact version and SHA-256 where applicable. If exact required bytes are unavailable, the result is `LAB_BLOCKED`; do not substitute a mock, reconstructed artifact, or silently different package and claim equivalent proof.

## Current handoff rule

Only a meaningful `LAB_PASS` for the exact v0.6.0 candidate justifies moving to the governed real staging import/read-back. The staging import blocker remains open until staging itself is exercised. Actual staging Form/Field IDs—not CI IDs—are the only IDs eligible for authoritative Implementation Mapping binding.

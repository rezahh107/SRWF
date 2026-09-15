# SRWF CI Runtime Lab

This directory owns the smallest disposable CI preflight for the current Stage 0 Gravity Forms scaffold. It is a test harness only; it is not a staging controller, workflow authority, persistent executor, or deployment system.

## Current scenario

`GF_V060_IMPORT_READBACK`:

1. Admit only the exact `SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json` bytes whose pinned SHA-256 is `445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89`.
2. Boot disposable WordPress + MariaDB on a GitHub-hosted runner.
3. Install the real Owner-authorized Gravity Forms `3.1.1.1` package pinned by SHA-256 `542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b`.
4. Import through Gravity Forms' own `GFExport::import_file()` path.
5. Force the imported form inactive as a fail-safe and read it back through `GFAPI`.
6. Compare source-defined form and field settings against the runtime read-back, while ignoring only runtime identity/state fields that are expected to change.
7. Record generated CI Form/Field IDs as evidence only. They are disposable and must never populate `docs/contracts/IMPLEMENTATION_MAPPING.yaml`.

The first scenario intentionally does not activate Gravity Flow, PersianGravity, Gravity Perks, GravityView, GNM, or finance/cheque components because it tests import/read-back persistence only. Behavior owned by those plugins remains outside this scenario until a concrete SRWF test requires it.

## Source admission

The exact scaffold may be supplied in either of two ways:

- repository-managed fixture at `tests/runtime-lab/fixtures/SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json`; or
- an Owner-authorized public URL passed explicitly to `workflow_dispatch` as `scaffold_url`.

Both paths are accepted only after the same pinned SHA-256 check. An absent or mismatching scaffold is not replaced, regenerated, mocked, or treated as success.

## Evidence states

- `LAB_PASS`: the exact admitted scaffold completed the real Gravity Forms import/read-back assertions in disposable CI.
- `LAB_FAIL`: the scenario executed but one or more required assertions failed.
- `LAB_BLOCKED`: the scenario could not reach the runtime boundary because a required exact input was unavailable.
- `NOT_TESTED`: used only for explicitly unexercised sub-boundaries.

A Lab result is never `OBSERVED_IN_STAGING`, staging PASS, production proof, or production readiness. Finance/manual-cheque behavior and the GP Nested Forms cheque POC remain suspended/deferred and are not tested here.

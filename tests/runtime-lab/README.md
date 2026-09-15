# SRWF CI Runtime Lab

This directory owns the smallest disposable CI preflight for the current Stage 0 Gravity Forms scaffold. It is a test harness only; it is not a staging controller, workflow authority, persistent executor, or deployment system.

## Current scenario

`GF_V060_IMPORT_READBACK`:

1. Admit only the exact `SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json` bytes whose current pinned SHA-256 is `5d099c908a245823aa0a3b40c718c35922e23a8afd56141cc7f97194d558c2fb`.
2. Boot disposable WordPress + MariaDB on a GitHub-hosted runner.
3. Install the real Owner-authorized Gravity Forms `3.1.1.1` package pinned by SHA-256 `542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b`.
4. Import through Gravity Forms' own `GFExport::import_file()` path.
5. Force the imported form inactive as a fail-safe and read it back through `GFAPI`.
6. Assert the locked `student_photo` source profile: File Upload Pro enabled, crop enabled/required, aspect ratio `3:4`, maximum dimensions `1200×1600`, no minimum/exact dimensions, one `jpg/jpeg` file up to 5 MB.
7. Compare source-defined form and field settings against runtime read-back. `confirmations` and `notifications` are source-defined settings and participate in equivalence; only demonstrated runtime-owned form identity/state properties are excluded. This comparison also verifies that the source-defined File Upload Pro metadata survives Gravity Forms import/GFAPI serialization.
8. Record generated CI Form/Field IDs as evidence only. They are disposable and must never populate `docs/contracts/IMPLEMENTATION_MAPPING.yaml`.

The earlier v0.6.0 SHA-256 `445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89` remains historical evidence for the previous Lab execution. The current provisional bytes are identified by the new pinned SHA-256 above.

The first scenario intentionally does not activate Gravity Flow, PersianGravity, Gravity Perks, GravityView, GNM, or finance/cheque components because it tests Gravity Forms import/read-back persistence only. File Upload Pro field metadata preservation is covered, but actual File Upload Pro crop/downscale behavior is not runtime-proven by this scenario. Behavior owned by those plugins remains outside this scenario until a concrete SRWF test requires it.

## Source admission

The exact scaffold may be supplied through a repository-managed fixture or an explicit Owner-authorized public dispatch URL.

The repository-managed representation may be either:

- the raw JSON at `tests/runtime-lab/fixtures/SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json`; or
- the deterministic gzip+base64 transport split across `tests/runtime-lab/fixtures/SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json.gz.b64.part-{00..03}` (with a single `.json.gz.b64` file also supported).

The encoded fixture is transport only: CI reconstructs the original JSON bytes before use. Every repository-managed or dispatch-source path is admitted only after the reconstructed/downloaded JSON matches the same pinned SHA-256. An absent or mismatching scaffold is not replaced, regenerated, mocked, or treated as success.

## Canonical terminal evidence

`tests/runtime-lab/finalize-evidence.py` is the single terminal evidence finalizer for all reachable Lab phases after checkout. It preserves an already valid scenario evidence file when the completed phase outcomes are consistent with it; otherwise it deterministically materializes the first relevant terminal `LAB_BLOCKED` or `LAB_FAIL` state. Missing or corrupt terminal evidence is itself finalized as `LAB_FAIL` and cannot produce a green job.

The GitHub Step Summary and final enforcement read the same finalized `lab-evidence.json`, verify its recorded SHA-256, and the artifact upload contains that canonical file plus its checksum. Phase-local helpers do not independently manufacture authoritative terminal evidence.

## Evidence states

- `LAB_PASS`: the exact admitted scaffold completed the real Gravity Forms import/read-back assertions in disposable CI.
- `LAB_FAIL`: the scenario/runtime/assertion or Lab guard executed and a required check failed.
- `LAB_BLOCKED`: a required exact input or pre-runtime dependency prevented the intended runtime boundary from being exercised.
- `NOT_TESTED`: used only for explicitly unexercised sub-boundaries.

`LAB_BLOCKED` and `LAB_FAIL` remain failing job outcomes. A Lab result is never `OBSERVED_IN_STAGING`, staging PASS, production proof, or production readiness. Finance/manual-cheque behavior and the GP Nested Forms cheque POC remain suspended/deferred and are not tested here.

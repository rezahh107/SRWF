# SRWF CI Runtime Lab

This directory owns bounded disposable CI preflights for Stage 0 Gravity Forms scaffold candidates. It is a test harness only; it is not a staging controller, workflow authority, persistent executor, or deployment system.

## Current successor qualification — v0.6.2

`GF_V062_CURRENT_PG_MINIMAL_READBACK` qualifies the material change from the historical v0.6.1 candidate against the maintained PersianGravity release:

1. Admit only the repository-managed raw JSON at `tests/runtime-lab/fixtures/SRWF_GravityForms_Import_v0.6.2_PROVISIONAL.json` with exact SHA-256 `d371ece6587b956d693eed556b5d6d1aa6d0bb60e10c8d40c73f3750607d7ee8` and size `350906` bytes.
2. Run the fail-closed static contract guard plus its negative self-tests.
3. Boot disposable WordPress `6.8.3` + MariaDB on a GitHub-hosted runner.
4. Install authentic Gravity Forms `3.1.1.1` pinned by SHA-256 `542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b`.
5. Install the published PersianGravity `4.4.0` release artifact pinned by SHA-256 `0033ecf1ef1e43b0f73f792e446b09fad4038973511aa17232e310189b5f4780`.
6. Import through Gravity Forms' own `GFExport::import_file()` path, keep the form inactive, and read it back through `GFAPI`.
7. Require `national_id` to hydrate as `PGR_GF_Field_National_ID` / `pgr_national_id` and prove Persian-digit normalization, canonical ten-ASCII-digit persistence, valid checksum acceptance, and invalid checksum rejection.
8. Require `dob_jalali` to hydrate as `PGR_GF_Field_Jalali_Date` / `pgr_jalali_date`, prove `ymd_slash` Jalali presentation, canonical ASCII `YYYY-MM-DD` persistence, valid Jalali acceptance, and invalid Jalali rejection.
9. Preserve the unchanged school/photo metadata and perform authentic Gravity Forms export preparation to prove the current custom field types survive round-trip serialization.

The v0.6.2 automatic lane deliberately proves only the changed Gravity Forms + PersianGravity boundary. It does **not** convert historical paid-stack evidence into new v0.6.2 proof.

### v0.6.2 full-stack mode

`GF_V062_CURRENT_PG_FULL_STACK_READBACK` additionally requires the exact authentic paid stack:

- Gravity Perks `2.3.16`, SHA-256 `a160d166fb7894b0dfc558ae92e0c230a1336ed2a81e78fa1216be72b1024e7c`;
- GP File Upload Pro `1.5.13`, SHA-256 `fdab5621dc0c1b9d33384696f554ef9ac0d646a70f8cee652a1bc05c43f8f7ce`;
- GP Advanced Select `1.1.21`, with its exact Owner-authorized package SHA-256 supplied alongside the package.

The manual FULL_STACK lane obtains licensed package URLs/hashes only from repository secrets. Missing exact inputs produce `LAB_BLOCKED`; they are never replaced with mocks, guessed metadata, stale signed URLs, or substitute packages. When admitted, the probe also verifies the File Upload Pro 3:4 crop/max-dimension interpretation and GP Advanced Select recognition of `school_code`.

Until an exact-head FULL_STACK run passes, v0.6.2 remains a successor **under qualification** and must not be promoted as the governed staging-import candidate merely because the minimal current-PersianGravity lane passes.

## Historical accepted preflight — v0.6.0

`GF_V060_IMPORT_READBACK` remains historical evidence for the exact v0.6.0 scaffold:

1. Admit only `SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json` bytes whose pinned SHA-256 is `445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89`.
2. Boot disposable WordPress + MariaDB.
3. Install authentic Gravity Forms `3.1.1.1`.
4. Import through `GFExport::import_file()`.
5. Keep the imported form inactive and read it back through `GFAPI`.
6. Treat generated CI Form/Field IDs as disposable evidence only.

The existing `.github/workflows/ci-runtime-lab.yml` remains the implementation of that historical reusable lane. Its accepted v0.6.0 result does not prove current PersianGravity custom-field behavior.

## Historical v0.6.1 paid-stack evidence

The closed evidence-only PR #11 / run `35014441345` proved the exact v0.6.1 candidate with authentic Gravity Forms `3.1.1.1`, Gravity Perks `2.3.16`, and GP File Upload Pro `1.5.13`. That run established executable/readable `student_photo` crop `3:4`, max `1200x1600`, no min/exact dimensions, frontend localization, and Gravity Forms round-trip preservation.

That evidence remains valid historical evidence for those exact bytes and plugin identities. It does not prove the v0.6.2 successor, GP Advanced Select `1.1.21`, staging, or production behavior.

## Source admission and evidence semantics

Exact hashes are admission boundaries, not documentation hints. An absent/mismatching artifact or package is not regenerated, mocked, silently upgraded, or treated as success.

Evidence states:

- `LAB_PASS`: the exact admitted inputs completed the assertions in disposable CI.
- `LAB_FAIL`: the runtime/assertion or guard executed and a required check failed.
- `LAB_BLOCKED`: a required exact input prevented the intended boundary from being exercised.
- `NOT_TESTED`: an explicitly unexercised sub-boundary.

`LAB_PASS` is never `OBSERVED_IN_STAGING`, staging PASS, production proof, or production readiness. CI Form/Field IDs are disposable and must never populate `docs/contracts/IMPLEMENTATION_MAPPING.yaml`. Synthetic values only. Finance/manual-cheque behavior and the GP Nested Forms cheque POC remain suspended/deferred and are not activated or validated by these lanes.

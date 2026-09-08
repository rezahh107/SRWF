# SRWF Definition of Done

Release acceptance requires **executed evidence**, not only documentation.

## Data contract

- Semantic Field Contract = Owner Approved.
- Implementation Mapping = Bound/Verified to real target IDs.
- new form baseline; no legacy ID compatibility/migration requirement.
- machine values/crosswalk dependencies validated in UI and server paths.
- National ID normalized/validated; duplicate National ID remains allowed.
- Jalali DOB valid; student mobile validated through selected maintained solution.
- finance contract enforced: Rial, optional/non-public/Registration-Officer-only; amount inputs default empty; net empty if tuition empty else tuition-discount (empty discount treated as zero without persisting zero); invalid discount no save; finance/status/catalog cleanup rules enforced.
- cheque cardinality `1..N`; child mapping bound; no parallel relationship DB/state.

## Workflow

- `V-01 PASS`.
- Needs Review = Entry field + reason only; no custom state/step/endpoint.
- Officer finance editing remains native Gravity Flow.

## Access

- `V-02 PASS`.
- public unauthorized access rejected.
- Officer only appropriate assigned operational access.
- Admin Actions not exposed to Officer.
- UI visibility is not treated as authorization.

## Public form

- `V-03 PASS` for Persian school search/mobile + correct canonical school value.
- `student_photo` read-back proves single jpg/jpeg <=5MB, GP File Upload Pro enabled, required 3:4 crop and max 1200×1600; no minimum dimensions/custom background/AI processing.
- `home_phone` exists and remains optional.
- `father_name`, names, student mobile required as SFC specifies.
- if Nested Forms used, `PRB-NESTED-CHEQUE-001 PASS` with manual current-release entry path.
- seven Sayad fields remain hidden/future-reserved; scanner is not current-release dependency.

## Audit

- `V-04 PASS` for human edits; Admin-only full revision history.

## Operations/freshness

- `V-05 PASS`.
- no custom polling/worker/queue introduced.

## Counter

- `V-06 PASS`.
- exact National-ID match; same ID => same counter; import does not advance Flow.

## Print

- `D-17-GRAVITY-PDF PASS` before dossier renderer is release-ready.
- no paid Gravity PDF template/extension baseline.
- no custom PDF engine/dual Browser Print production renderer.

## Environment/release

- exact target compatibility inventory recorded.
- staging regression exercised after material vendor/version changes.
- privacy/retention Owner sign-off before real PII.
- release manifest and rollback runbook complete.
- changelog and evidence references versioned.
- POS/PC-POS and online Sayad absent from current-release runtime dependencies.

## Current completion state

`NOT_DONE` — authoritative scaffold and runtime validation have not yet completed; `V-01..V-06`, Nested host POC and D-17 POC remain unproven unless later evidence changes them.

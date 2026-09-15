# SRWF Definition of Done

Release acceptance requires **executed evidence**, not only documentation.

## Scope applicability

`OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC` suspends finance/manual-cheque implementation and validation until explicit Owner reopen. Existing finance semantics and optional/non-public reserved fields remain preserved in the SFC/history, but they are not current release/progression acceptance gates. The daily manager SMS is a recorded future requirement with implementation still unselected and is not a current release gate unless the Owner explicitly activates it for that release.

## Data contract

- Semantic Field Contract = Owner Approved.
- Implementation Mapping = Bound/Verified to real target IDs for active/non-suspended scope.
- new form baseline; no legacy ID compatibility/migration requirement.
- machine values/crosswalk dependencies validated in UI and server paths for active scope.
- National ID normalized/validated; duplicate National ID remains allowed.
- Jalali DOB valid; student mobile validated through selected maintained solution.
- preserved finance fields may exist as optional/non-public reserved fields, but finance-specific amount derivation, discount validation/catalog cleanup, Bonyad/Hekmat bindings and manual-cheque composition are deferred and do not block current release acceptance.
- cheque cardinality/child mapping rules remain preserved for future finance reopen; no parallel relationship DB/state is authorized.

## Workflow

- `V-01 PASS`.
- Needs Review = Entry field + reason only; no custom state/step/endpoint.
- finance-specific Officer editing/whitelist proof is deferred with finance scope; when reopened it must remain native Gravity Flow.

## Access

- `V-02 PASS`.
- public unauthorized access rejected.
- Officer only appropriate assigned operational access.
- Admin Actions not exposed to Officer.
- UI visibility is not treated as authorization.
- preserved finance fields must not become public merely because finance implementation is suspended.

## Public form

- `V-03 PASS` for Persian school search/mobile + correct canonical school value.
- `student_photo` read-back proves single jpg/jpeg <=5MB, GP File Upload Pro enabled, required 3:4 crop and max 1200×1600; no minimum dimensions/custom background/AI processing.
- `home_phone` exists and remains optional.
- `father_name`, names, student mobile required as SFC specifies.
- `PRB-NESTED-CHEQUE-001` is retained but `DEFERRED_WITH_FINANCE_SCOPE`; it is not required for current release acceptance until Owner reopen.
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
- finance/cheque integration into the final dossier is deferred with finance scope; renderer capability may still be tested with synthetic representative content without promoting finance implementation.

## Daily manager SMS — future recorded requirement

- requirement is preserved: end-of-working-day SMS to manager with the count of Officer approvals/advances to Accountant for that business day.
- implementation mechanism/time/calendar/provider/mobile binding/retry semantics remain `OPEN / NOT_SELECTED`.
- it cannot own/mutate workflow state.
- Cron/Cron-like shared-host scheduling is not an accepted baseline without Owner re-adjudication.
- this feature becomes a release acceptance item only when the Owner explicitly activates its implementation scope.

## Environment/release

- exact target compatibility inventory recorded.
- staging regression exercised after material vendor/version changes.
- privacy/retention Owner sign-off before real PII.
- release manifest and rollback runbook complete.
- changelog and evidence references versioned.
- POS/PC-POS and online Sayad absent from current-release runtime dependencies.

## Current completion state

`NOT_DONE` — authoritative scaffold and runtime validation have not yet completed; `V-01..V-06` and D-17 remain unproven unless later evidence changes them. Nested-cheque POC is `DEFERRED_WITH_FINANCE_SCOPE`, not a current completion blocker.

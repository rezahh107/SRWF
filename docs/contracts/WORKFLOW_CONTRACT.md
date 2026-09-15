# SRWF Workflow Contract

## Authority

Gravity Flow تنها authority برای workflow state، assignment و formal Approval است. Gravity Forms canonical Entry/data را نگه می‌دارد.

## Current flow

1. Public Gravity Forms registration submit
2. Registration Officer step — native Gravity Flow Approval/Entry Details
3. Accountant Approval — native Gravity Flow Approval
4. Final external-pending / downstream-ready step according to configured Flow

Exact Step IDs در Gate B (`IMPLEMENTATION_MAPPING`) بعد از scaffold bind می‌شوند.

## Registration Officer

- single Officer baseline؛ no multi-officer reassignment/concurrency matrix.
- operational inbox = native Gravity Flow Inbox only.
- Entry review/edit = native Gravity Flow Entry Details.
- Officer edits only whitelisted fields.
- code-backed fields are edited via human-readable label/choice; system updates canonical code/value.
- formal progress occurs only through native Gravity Flow Approve.
- Officer Reject action is not part of baseline.

## Needs Review

Needs Review **workflow state نیست**.

- `review_status` ordinary Entry field
- `review_reason` ordinary Entry field
- Entry remains on same Officer step/assignee
- no custom POST endpoint
- no second queue
- no custom state/transition
- no Entry Notes dependency

Resolving review = correct fields on same native surface, then native Approve.

## Finance applicability — Owner scope suspension

`OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC` changes applicability, not historical finance semantics:

- existing finance/cheque semantics and reserved field definitions remain preserved in the SFC/history;
- finance/manual-cheque fields may remain present as optional, non-public reserved fields in the scaffold;
- finance-specific implementation/validation is **SUSPENDED** until explicit Owner reopen;
- current progression does not require finance-specific Gravity Flow whitelist proof, amount derivation/discount validation, Bonyad Shahid/Hekmat server bindings, cheque child composition, GP Nested Forms POC, POS/PC-POS or Sayad implementation;
- no suspended finance item is a current blocker or release gate unless the Owner explicitly reopens that scope.

## Notifications / freshness

- routine edits / Needs Review changes generate no notification.
- native Gravity Flow Live Refresh is the freshness mechanism.
- no polling/WebSocket/custom worker/Cron for Inbox freshness.
- operational pages must not be badly cached.

## Daily manager SMS requirement

A separate reporting requirement is recorded; it does **not** own workflow state:

- at the end of each working day, send the manager an SMS containing the count of Entries that the Registration Officer approved/advanced to the Accountant during that working day;
- the count must be derived read-only from canonical Gravity Forms/Gravity Flow evidence; reporting must not advance, rewrite or duplicate workflow state;
- implementation mechanism, exact send time, business-day calendar, SMS provider, manager-mobile binding/source and retry/failure behavior are `OPEN / NOT_SELECTED`;
- Cron or Cron-like background scheduling on shared hosting is not an accepted baseline for this feature. A candidate that depends on it requires Owner re-adjudication rather than silent adoption;
- Gravity Forms Notification Scheduler, `gravity-notification-manager`, or any other candidate remains only a candidate until separately evaluated/selected; none is selected by this requirement record.

This reporting requirement is recorded for future implementation and is not a blocker for the current Stage 0 scaffold path.

## Accountant

- formal approval is native Gravity Flow Approval.
- prior finance-field visibility semantics remain preserved, but finance implementation is currently suspended. If finance scope is reopened and Accountant needs direct finance read access, reopen only that visibility binding.

## Import/counter

WP All Import may write only `registration_counter` using exact National ID matching. Import must not advance Gravity Flow. Any finalization uses native Flow mechanisms if needed.

## Forbidden workflow ownership

The following may not own SRWF workflow state/assignment/approval:

- GravityView
- Elementor
- WP All Import
- PDF renderer
- PersianGravity Scanner
- POS integration
- Uncanny Automator/external automation
- reporting/SMS automation
- custom DB/table/state/queue

## POC status

`V-01..V-06` remain `UNEXECUTED/NOT_PROVEN` unless an executed target-environment record explicitly changes them.

`PRB-NESTED-CHEQUE-001` remains historical/retained as `NOT_PROVEN`, but is `DEFERRED_WITH_FINANCE_SCOPE` and is not a current progression/release gate until Owner reopen.

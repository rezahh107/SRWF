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

## Notifications / freshness

- routine edits / Needs Review changes generate no notification.
- native Gravity Flow Live Refresh is the freshness mechanism.
- no polling/WebSocket/custom worker/Cron for Inbox freshness.
- operational pages must not be badly cached.

## Accountant

- formal approval is native Gravity Flow Approval.
- direct finance-field visibility is not silently broadened. Current finance visibility decision is Registration-Officer-only; if Accountant needs direct finance read access, reopen only that visibility binding.

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
- custom DB/table/state/queue

## POC status

`V-01..V-06` remain `UNEXECUTED/NOT_PROVEN` unless an executed target-environment record explicitly changes them.

# SRWF Access Control Contract

## Principles

UI hiding is not authorization. Every operational URL/action must rely on authenticated WordPress user + native Gravity Flow assignment/capability checks.

## Roles

### Public registrant

- may submit the public Gravity Forms registration form.
- cannot access Gravity Flow Inbox/Entry Details/Admin/Revisions/importer.
- cannot see reserved finance/manual-cheque Officer fields.

### Registration Officer

Allowed for active scope:

- native Gravity Flow Inbox items assigned to the Officer.
- native Entry Details for assigned workflow items.
- edit explicit Officer whitelist through native Flow editing.
- edit human-readable school/group/status choices; canonical code is system-mediated.
- set `review_status`/`review_reason`.
- native Approve.
- student photo/report-card access when operationally presented.

Preserved but currently suspended:

- prior finance/manual-cheque access semantics remain Registration-Officer-only/non-public if/when finance scope is reopened;
- reserved optional finance fields may remain stored/hidden in the scaffold, but finance-specific Officer editing/exposure is not a current implementation or validation requirement under `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC`.

Denied:

- Gravity Flow admin actions capability.
- entries outside assignment authorization.
- raw technical code direct editing.
- direct `registration_counter` editing.
- complete GravityRevisions history.
- importer configuration/execution unless separately Admin-authorized.
- GravityView workflow/approval/delete surfaces.

### Admin

- WordPress/GF/Flow configuration and permitted administrative entry access.
- full GravityRevisions view/compare/restore for human edits.
- school list administration and canonical corrections where governed.
- WP All Import counter sync operation.
- privacy/retention administration when policy is approved.

### Accountant

Formal Accountant Approval is native Gravity Flow. Exact field visibility/capabilities are **UNBOUND** until scaffold mapping. The preserved finance decision does not authorize silent direct finance-field visibility expansion beyond Registration Officer. Finance implementation is currently suspended; if finance scope is reopened and Accountant needs direct finance read access, reopen only that visibility binding.

## Daily manager SMS reporting boundary

- the manager-SMS feature is a read-only reporting requirement and does not grant the manager operational Entry/Flow access by itself;
- the reporting integration may read only the minimum canonical evidence needed to count Registration Officer approvals/advances for the configured business day;
- it may not own, advance, rewrite or duplicate workflow state/assignment/Approval;
- manager-mobile source/binding and SMS-provider credentials/permissions remain `OPEN / NOT_SELECTED` and must be bound explicitly before implementation.

## File access

`student_photo` and `report_card_file`: Admin + Registration Officer only under current decision; retention policy remains open.

## Front-end security

- direct Entry URL must re-authorize current user and assignment on every view/action.
- no anonymous/all-entry bypass settings.
- no email-token one-click action baseline.
- operational pages must not rely on menu visibility for security.

## Audit visibility

GravityRevisions full history = Admin-only. Officer does not get revision history parity.

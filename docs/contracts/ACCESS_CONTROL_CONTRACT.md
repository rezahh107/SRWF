# SRWF Access Control Contract

## Principles

UI hiding is not authorization. Every operational URL/action must rely on authenticated WordPress user + native Gravity Flow assignment/capability checks.

## Roles

### Public registrant

- may submit the public Gravity Forms registration form.
- cannot access Gravity Flow Inbox/Entry Details/Admin/Revisions/importer.
- cannot see finance/manual-cheque Officer fields.

### Registration Officer

Allowed:

- native Gravity Flow Inbox items assigned to the Officer.
- native Entry Details for assigned workflow items.
- edit explicit Officer whitelist through native Flow editing.
- edit human-readable school/group/status choices; canonical code is system-mediated.
- set `review_status`/`review_reason`.
- native Approve.
- current-release optional finance/manual-cheque fields on the Officer operational surface.
- student photo/report-card access when operationally presented.

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

Formal Accountant Approval is native Gravity Flow. Exact field visibility/capabilities are **UNBOUND** until scaffold mapping. Current Owner decision does not authorize silent direct finance-field visibility expansion beyond Registration Officer. If direct finance read access is required, reopen only that binding.

## File access

`student_photo` and `report_card_file`: Admin + Registration Officer only under current decision; retention policy remains open.

## Front-end security

- direct Entry URL must re-authorize current user and assignment on every view/action.
- no anonymous/all-entry bypass settings.
- no email-token one-click action baseline.
- operational pages must not rely on menu visibility for security.

## Audit visibility

GravityRevisions full history = Admin-only. Officer does not get revision history parity.

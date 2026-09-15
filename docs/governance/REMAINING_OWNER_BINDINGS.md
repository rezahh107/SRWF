# Remaining Owner Bindings

این فایل فقط bindingهای **واقعاً باز** را نگه می‌دارد. تصمیم بسته‌شده دوباره به‌عنوان سؤال باز مطرح نمی‌شود.

## CLOSED — do not reopen silently

- Officer edit whitelist/model: CLOSED.
- human-readable code-backed edit + system-mediated canonical code update: CLOSED.
- finance semantic unit = Rial: CLOSED/PRESERVED.
- finance field visibility/requiredness semantics: optional, non-public, Registration-Officer-only: CLOSED/PRESERVED.
- invalid discount semantic: `discount > tuition` => no save: CLOSED/PRESERVED.
- finance/manual-cheque **implementation and validation applicability**: `SUSPENDED` by `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC`; do not treat finance-specific bindings/POCs as current blockers until explicit Owner reopen.
- scanner current-release path: DEFERRED; seven Sayad fields hidden/future-reserved: CLOSED for current release.
- `home_phone`: included in public form, value optional: CLOSED.
- `father_name`: required: CLOSED.
- `first_name`, `last_name`, `student_mobile`: required: CLOSED.

## OPEN — Owner decision required

### `BIND-PRIVACY-RETENTION`

Define retention/deletion/access policy for:

- identity PII and contact data;
- student photo;
- report card;
- finance and cheque data if/when finance scope reopens;
- historical Entries;
- GravityRevisions/audit history;
- backups/exports/logs.

**Gate effect:** real PII remains blocked in staging/UAT/production until sign-off. Synthetic work is allowed.

### `BIND-DAILY-MANAGER-SMS`

Requirement is recorded but implementation bindings are intentionally open:

- exact end-of-working-day send time/timezone rule;
- business-day calendar/holiday behavior;
- SMS provider/integration;
- authoritative manager-mobile source/binding;
- retry/failure/duplicate-send behavior;
- exact counting boundary if a workflow item is reprocessed/reassigned.

**Current effect:** not a Stage 0 blocker and not a current release gate until Owner explicitly activates implementation scope. Candidate selection must not silently introduce Cron/Cron-like shared-host scheduling; such a dependency requires Owner re-adjudication.

## Repository materialization gaps — evidence/retrieval, not necessarily new Owner business decisions

### `MAT-SFC-CHOICE-CATALOG`

For active non-finance scope, exact accepted education/group choice/value catalogs must be materialized/verified from authoritative Crosswalk/source before final scaffold freeze. Event86 already closes `registration_center_code` and the preserved `finance_status` value semantics; do not reopen those merely because finance implementation is suspended.

### `MAT-SFC-MANUAL-CHEQUE-FIELDS` — DEFERRED

Exact manual-cheque machine-key inventory remains preserved as a future finance materialization need, but it is `DEFERRED_WITH_FINANCE_SCOPE` and is **not** a current artifact-support blocker. Bind it only after explicit Owner finance/cheque reopen; do not invent keys in the meantime.

These artifact support gaps do not reopen parent architecture or unrelated SFC decisions.

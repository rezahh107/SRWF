# Remaining Owner Bindings

این فایل فقط bindingهای **واقعاً باز** را نگه می‌دارد. تصمیم بسته‌شده دوباره به‌عنوان سؤال باز مطرح نمی‌شود.

## CLOSED — do not reopen silently

- Officer edit whitelist/model: CLOSED.
- human-readable code-backed edit + system-mediated canonical code update: CLOSED.
- finance unit = Rial: CLOSED.
- finance current-release visibility/requiredness: all optional, non-public, Registration-Officer-only: CLOSED.
- invalid discount: `discount > tuition` => no save: CLOSED.
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
- finance and cheque data;
- historical Entries;
- GravityRevisions/audit history;
- backups/exports/logs.

**Gate effect:** real PII remains blocked in staging/UAT/production until sign-off. Synthetic work is allowed.

## Repository materialization gaps — evidence/retrieval, not necessarily new Owner business decisions

### `MAT-SFC-CHOICE-CATALOG`
Exact accepted current choice/value catalog for education/group/registration center/registration status must be materialized from authoritative Crosswalk/source before final scaffold freeze. If source conflicts, stop affected unit and ask Owner; do not choose a code silently.

### `MAT-SFC-MANUAL-CHEQUE-FIELDS`
Current active Master states manual cheque fields are optional but does not enumerate every manual cheque machine key in the retrieved section. Bind the exact list from accepted source/Owner before Cheque Child Form freeze; do not invent keys.

These two are **artifact support gaps**. They do not by themselves reopen parent architecture or unrelated SFC decisions.

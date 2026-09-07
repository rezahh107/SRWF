# SRWF Decision Ledger

این ledger تصمیم‌های durable و current را نگه می‌دارد. وضعیت اجرایی جاری در `runtime/CURRENT_STATE.yaml` و history مادی repository-era در `runtime/DECISION_HISTORY.jsonl` است. تاریخچهٔ Google Sheet قبل از cutover فقط immutable provenance زیر `history/pre-runtime-ssot/` است.

## Architecture locks

- `D-01` Needs Review = ordinary Entry field + reason; no custom state/queue/POST/Entry Notes dependency.
- `D-02` single operational inbox = Gravity Flow Inbox.
- `D-03` single Registration Officer baseline.
- `D-04` native Gravity Flow Officer edit with smallest whitelist.
- `D-05` formal Approval only native Gravity Flow Approval.
- `D-06` routine/review edits: no notifications.
- `D-07` native Live Refresh; no custom polling.
- `D-08` no custom concurrency/locking.
- `D-09` school search criterion = fast Persian-name search/mobile; first serious maintained candidate to PASS wins.
- `D-10` repeated National ID allowed; no duplicate block.
- `D-11` simple maintained Iranian mobile/Jalali/National-ID solution; no custom kernel.
- `D-12` photo processing out of current scope; required upload only.
- `D-13` human edit audit only via GravityRevisions; Admin-only.
- `D-14` no direct GFAPI update path baseline.
- `D-15` WP All Import owns counter sync by exact National ID.
- `D-16` importer writes counter, not Flow progression.
- `D-17` first renderer POC = Gravity PDF Free + SRWF-owned print layer; no paid template/extension baseline; no custom PDF engine.

## Current Owner decisions — Semantic Field Contract

| Decision | Current effect | State |
|---|---|---|
| `OWNER-20260830-OFFICER-EDIT-NATIVE` | Officer corrections stay native Gravity Flow/GF; no custom edit UI. | CONFIRMED |
| `OWNER-20260830-HEKMAT-PACKAGE-HIDDEN` | `hekmat_package=آزمون` hidden fixed value. | CONFIRMED |
| `OWNER-20260830-STUDENT-PHOTO-REQUIRED` | `student_photo` included + value required; native File Upload only. | CONFIRMED |
| `OWNER-20260830-REPORT-CARD-CONDITIONAL` | `report_card_file` optional by default, conditional required. | CONFIRMED |
| `OWNER-20260830-REPORT-CARD-SCHOOL-CODES` | Required school codes = 283,286,291,650,663,666,667,1320,1351. | CONFIRMED |
| `OWNER-20260830-HEKMAT-TRACKING-HIDDEN` | `hekmat_tracking=1111111111111111` hidden fixed when Hekmat. | CONFIRMED |
| `OWNER-20260830-GROUP-CODE-DERIVATION` | user edits visible education/group; `group_code` derived/stored canonical; no redundant `exam_group`. | CONFIRMED |
| `OWNER-20260830-MOBILE-REQUIREDNESS` | `student_mobile` required; contact mobiles optional. | CONFIRMED |
| `OWNER-20260830-CONTACT-RELATION-MOBILE` | keep relationship+mobile for contacts; remove contact names. | CONFIRMED |
| `OWNER-20260830-CONTACT-RELATION-FIXED` | contact1=پدر, contact2=مادر fixed/hidden. | CONFIRMED |
| `OWNER-20260830-GRADUATION-STATUS-CONDITIONAL` | auto status for single-status groups; visible choice for dual-status groups. | CONFIRMED |
| `OWNER-20260830-FILE-ACCESS-SCOPE` | photo/report-card access = Admin + Officer; retention deferred to privacy gate. | CONFIRMED |
| `OWNER-20260830-FATHER-NAME-REQUIRED` | `father_name` required. | CONFIRMED |
| `OWNER-20260830-NAME-REQUIRED` | `first_name`, `last_name` required. | CONFIRMED |
| `OWNER-20260907-HOME-PHONE-INCLUDED-OPTIONAL` | `home_phone` must exist, but value is optional. | CONFIRMED; supersedes earlier ambiguous required-value row |

## Current Owner decisions — school selector

- Native Gravity Forms Enhanced UI was observed to fail responsive requirement in target runtime: `PROBE-20260830-SCHOOL-ENHANCED-UI-RESPONSIVE-FAIL`.
- `OWNER-20260830-SCHOOL-ADVANCED-SELECT`: current maintained candidate = GP Advanced Select with GF Enhanced UI disabled; `V-03` still `NOT_PROVEN` until target mobile/search PASS.

This rejects only the failed candidate; D-09 architecture/criterion remains intact.

## Current Owner decisions — finance/cheque/scanner

| Decision | Effect |
|---|---|
| `OWNER-20260906-FINANCE-UNIT-RIAL` | canonical/display money unit = Rial. |
| `OWNER-20260906-FINANCE-INVALID-DISCOUNT-BLOCK` | discount > tuition => validation error + no save. |
| `OWNER-20260907-FINANCE-OFFICER-ONLY-NONE-REQUIRED` | all current-release finance/manual-cheque fields optional, non-public, Registration-Officer-only. |
| `OWNER-20260907-FINANCE-STATUS-OFFICER-DEFAULT-NORMAL` | `finance_status`: Officer-only, non-public, optional; canonical default `0=عادی`; allowed values remain `0,1,3`. |
| `OWNER-20260906-NESTED-FORMS-SELECTED` | multi-cheque host = GP Nested Forms; Parent-Child Forms fallback only after bounded FAIL. |
| `OWNER-20260906-SCANNER-NONPERSISTENT-CONTROLLER` | Structured Scanner does not own/persist canonical data/raw payload. |
| `OWNER-20260906-SAYAD-V01-ATOMIC-SEVEN-OUTPUT` | seven deterministic outputs; atomic population if scanner phase is active. |
| `OWNER-20260907-DEFER-SCANNER-HIDE-SAYAD-FIELDS` | SRWF current release defers scanner; seven Sayad fields remain hidden/future-reserved. |
| `OWNER-20260906-D17-GRAVITY-PDF-FREE-POC` | first print POC = Gravity PDF Free + SRWF-owned print layer. |
| `OWNER-20260905-FIN-POS-DEFER` + later POS decisions | POS/PC-POS deferred from current release. |

## Current Owner decisions — code editing

`OWNER-20260907-OFFICER-EDIT-LABELS-SYSTEM-CODES`: Officer edits human-readable school/group/status labels/choices. System writes matching canonical code/value. Raw technical codes are not directly editable. This refines old `school_code Admin-only` interpretation only for system-mediated updates caused by Officer-visible selection.

## Environment progression

`OWNER-20260906-SKIP-RESIDUAL-ENV-INVENTORY`: Environment Inventory remains `PARTIAL/OWNER_ACCEPTED_FOR_PROGRESS`; residual staging/license/cache/build identity reopens only when decision-critical. This is not a PASS.

## Repository governance

### `OWNER-20260907-SRWF-REPO-CANONICAL-DOCS`

- `rezahh107/SRWF` is canonical home for durable project documentation/contracts after baseline merge/read-back.
- `README.md`, `AGENTS.md`, manifest, standalone contracts, validation/release artifacts and classified provenance are required.
- real PII/intake images/operational data ledgers must not be committed.

### `OWNER-20260907-REPOSITORY-RUNTIME-SSOT`

This later Owner decision **supersedes the former split-state boundary** that kept Google Sheets as live runtime SSOT.

After cutover merge + `main` read-back:

- `GitHub main` = sole project/runtime SSOT.
- `runtime/CURRENT_STATE.yaml` = canonical current execution state.
- `runtime/DECISION_HISTORY.jsonl` = append-only repository-era material history.
- pre-cutover Sheet state/history = immutable provenance under `history/pre-runtime-ssot/`.
- Google Sheet `SRWF_RUNTIME_STATE` = `DEPRECATED_READ_ONLY_MIGRATION_SOURCE`; no dual-write.
- a material runtime state change is persisted only after state + event are in the same accepted commit and read back from `main`.

Reopen only by Owner decision or if repository availability/concurrency creates a material execution problem that commit/blob-SHA discipline cannot safely handle.

## Superseded / historical decision rows

These remain in history but do not control current behavior:

- `OWNER-20260907-HOME-PHONE-REQUIRED` — superseded by `OWNER-20260907-HOME-PHONE-INCLUDED-OPTIONAL`.
- native List field as primary multi-cheque candidate — superseded by later Owner host decision.
- Gravity Flow Parent-Child Forms as selected primary host — superseded by GP Nested Forms selection; retained only as fallback.
- Scanner population as current-release cheque path — superseded by current-release scanner deferral.
- older product-knowledge global Stage0 blockers — superseded by Addendum/current Master.
- Google Sheet as live runtime SSOT — superseded by `OWNER-20260907-REPOSITORY-RUNTIME-SSOT` after completed repository cutover.

## Evidence observations that must not be promoted

- PersianGravity 4.1.0 Owner smoke = `OWNER_REPORTED_SMOKE_PASS` with unspecified coverage, not full runtime validation.
- PR merge/CI = source implementation evidence, not browser/Nested Forms lifecycle proof.
- `V-01..V-06` remain unexecuted unless later live evidence explicitly updates them.
- D-17 remains POC-gated/not-proven.

## Update rule

A material Owner decision or executed probe/result must update `runtime/CURRENT_STATE.yaml` and append one event to `runtime/DECISION_HISTORY.jsonl` in the same accepted Git commit; then both are read back from `main`. Reflect it here only when it changes durable project semantics. Discussion-only events do not belong here.

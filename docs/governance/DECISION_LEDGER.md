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
- `D-09` school search criterion remains fast Persian-name search/mobile; native Enhanced UI failed target responsive behavior, and event86 locks GP Advanced Select with GF Enhanced UI off for the current main form; `V-03` remains `NOT_PROVEN`.
- `D-10` repeated National ID allowed; no duplicate block.
- `D-11` simple maintained Iranian mobile/Jalali/National-ID solution; no custom kernel.
- `D-12` amended by event86: no custom/background/AI image-processing pipeline. Required student photo remains a GF upload; maintained GP File Upload Pro crop/downscale is allowed/required only for 3:4 crop and max 1200×1600, with no minimum dimensions.
- `D-13` human edit audit only via GravityRevisions; Admin-only.
- `D-14` no direct GFAPI update path baseline.
- `D-15` WP All Import owns counter sync by exact National ID.
- `D-16` importer writes counter, not Flow progression.
- `D-17` first renderer POC = Gravity PDF Free + SRWF-owned print layer; no paid template/extension baseline; no custom PDF engine.

## Current Owner decisions — Semantic Field Contract

| Decision | Current effect | State |
|---|---|---|
| `OWNER-20260830-OFFICER-EDIT-NATIVE` | Officer corrections stay native Gravity Flow/GF; no custom edit UI. | CONFIRMED |
| `OWNER-20260830-HEKMAT-PACKAGE-HIDDEN` | `hekmat_package=آزمون` hidden fixed value. | CONFIRMED; refined by event81 server set/clear; implementation applicability later suspended |
| `OWNER-20260830-STUDENT-PHOTO-REQUIRED` | `student_photo` included + value required. | CONFIRMED; D-12 processing detail amended by event86 |
| `OWNER-20260830-REPORT-CARD-CONDITIONAL` | `report_card_file` optional by default, conditional required. | CONFIRMED; visibility/lifecycle refined by event85 |
| `OWNER-20260830-REPORT-CARD-SCHOOL-CODES` | Required school codes = 283,286,291,650,663,666,667,1320,1351. | CONFIRMED |
| `OWNER-20260830-HEKMAT-TRACKING-HIDDEN` | `hekmat_tracking=1111111111111111` hidden/system-owned when Hekmat. | CONFIRMED; refined by event81 server set/clear; implementation applicability later suspended |
| `OWNER-20260830-GROUP-CODE-DERIVATION` | user edits visible education/group; `group_code` derived/stored canonical; no redundant `exam_group`. | CONFIRMED |
| `OWNER-20260830-MOBILE-REQUIREDNESS` | `student_mobile` required; contact mobiles optional. | CONFIRMED |
| `OWNER-20260830-CONTACT-RELATION-MOBILE` | keep relationship+mobile for contacts; remove contact names. | CONFIRMED |
| `OWNER-20260830-CONTACT-RELATION-FIXED` | contact1=پدر, contact2=مادر fixed/hidden. | CONFIRMED |
| `OWNER-20260830-GRADUATION-STATUS-CONDITIONAL` | auto status for single-status groups; visible choice for dual-status groups. | CONFIRMED |
| `OWNER-20260830-FILE-ACCESS-SCOPE` | photo/report-card access = Admin + Officer. | CONFIRMED; primary lifecycle refined by event85/86; backup retention open |
| `OWNER-20260830-FATHER-NAME-REQUIRED` | `father_name` required. | CONFIRMED |
| `OWNER-20260830-NAME-REQUIRED` | `first_name`, `last_name` required. | CONFIRMED |
| `OWNER-20260907-HOME-PHONE-INCLUDED-OPTIONAL` | `home_phone` must exist, but value is optional. | CONFIRMED; supersedes earlier ambiguous required-value row |

## Current Owner decisions — school selector

- Native Gravity Forms Enhanced UI was observed to fail responsive requirement in target runtime: `PROBE-20260830-SCHOOL-ENHANCED-UI-RESPONSIVE-FAIL`.
- `OWNER-20260830-SCHOOL-ADVANCED-SELECT` selected GP Advanced Select as maintained candidate with GF Enhanced UI disabled.
- event86 makes GP Advanced Select mandatory for the current main-form scaffold; final `V-03` still `NOT_PROVEN` until target mobile/search and stored-value PASS.

This rejects only the failed native candidate; it does not promote `V-03`.

## Current Owner decisions — finance/cheque/scanner semantics

The decisions below remain durable semantic history. Their **current implementation applicability** is overridden by the later finance-suspension decision; they are not deleted.

| Decision | Effect |
|---|---|
| `OWNER-20260906-FINANCE-UNIT-RIAL` | canonical/display money unit = Rial. |
| `OWNER-20260906-FINANCE-INVALID-DISCOUNT-BLOCK` | discount > tuition => validation error + no save. |
| `OWNER-20260907-FINANCE-OFFICER-ONLY-NONE-REQUIRED` | finance/manual-cheque fields optional, non-public, Registration-Officer-only when finance scope is active. |
| `OWNER-20260907-FINANCE-STATUS-OFFICER-DEFAULT-NORMAL` | `finance_status`: Officer-only, non-public, optional; canonical default `0=عادی`; allowed values remain `0,1,3`. |
| `OWNER-20260906-NESTED-FORMS-SELECTED` | future multi-cheque host = GP Nested Forms; Parent-Child Forms fallback only after bounded FAIL. Current POC applicability is deferred with finance scope. |
| `OWNER-20260906-SCANNER-NONPERSISTENT-CONTROLLER` | Structured Scanner does not own/persist canonical data/raw payload. |
| `OWNER-20260906-SAYAD-V01-ATOMIC-SEVEN-OUTPUT` | seven deterministic outputs; atomic population if scanner phase is active. |
| `OWNER-20260907-DEFER-SCANNER-HIDE-SAYAD-FIELDS` | scanner deferred; seven Sayad fields remain hidden/future-reserved. |
| `OWNER-20260906-D17-GRAVITY-PDF-FREE-POC` | first print POC = Gravity PDF Free + SRWF-owned print layer. |
| `OWNER-20260905-FIN-POS-DEFER` + later POS decisions | POS/PC-POS deferred. |

## Owner scope decision — finance suspension + daily manager SMS

### `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC`

This is an **applicability/scope decision**, not deletion of prior finance semantics.

- Finance/manual-cheque implementation and validation are `SUSPENDED` until explicit Owner reopen.
- Existing finance semantics/catalogs remain preserved for future reuse and for interpreting reserved scaffold fields.
- Optional/non-public finance fields may remain present in the scaffold, but finance-specific Flow whitelist proof, calculations, discount/Bonyad/Hekmat server bindings, cheque composition and `PRB-NESTED-CHEQUE-001` are not current blockers/release gates.
- `PRB-NESTED-CHEQUE-001` becomes `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN`.
- The active non-finance scaffold/workflow path continues; suspension must not be misread as removal of fields or runtime PASS.
- A new reporting requirement is recorded: at the end of each working day, SMS the manager the count of Entries the Registration Officer approved/advanced to Accountant during that working day.
- Daily SMS reporting must be read-only relative to GF/Flow state and may not own/advance workflow.
- exact send time, business calendar, SMS provider, manager-mobile binding/source and retry/idempotency behavior remain `OPEN / NOT_SELECTED`.
- Cron/Cron-like shared-host scheduling is not an accepted baseline; a candidate that depends on it requires Owner re-adjudication.
- Gravity Forms Notification Scheduler and `gravity-notification-manager` remain candidates only; no implementation candidate is selected by this decision.
- Daily SMS is recorded but not a current Stage 0/release gate until Owner explicitly activates its implementation scope.

Reopen finance implementation only by explicit Owner instruction. Reopen the Cron constraint only by explicit Owner re-adjudication.

## Event78–86 — preserved main-form refinements

These Owner decisions extend/supersede only the named older projections; earlier unrelated decisions remain preserved. Finance-related rows remain semantically valid but implementation applicability is suspended by the later 2026-09-15 scope decision.

| Decision | Durable current effect |
|---|---|
| `OWNER-20260908-FOUNDATION-FIELDS-OFFICER-ONLY` | Bonyad Shahid case/type field semantics preserved as non-public Officer-only optional fields when `finance_status=1`; implementation suspended. |
| `OWNER-20260908-DISCOUNT-CODE-CATALOG-41-SEPARATE-FINANCE` | `discount_code` remains semantically separate from `discount_amount/title`; 41 controlled choices. |
| `OWNER-20260908-DISCOUNT-CODE-CATALOG-NAME-CODE-ONLY` | percentage is not SRWF data; coded discount is code + name only. |
| `OWNER-20260908-HEKMAT-SERVER-DERIVED-CLEAR-ON-EXIT` | Hekmat server-owned set/clear semantics preserved; implementation suspended. |
| `OWNER-20260908-SCHOOL-GENDER-FILTER-AUTHORITATIVE-METADATA` | school gender compatibility uses authoritative metadata; `Other=0` exempt. |
| `OWNER-20260908-SCHOOL-SOURCE-1405-EXCLUDE-INVALID-4` | SchoolReport 1405 selected; codes `1296,1314,1316,1319` excluded; retained named set = 946. |
| `OWNER-20260908-SCHOOL-LEVEL-MAPPING-SECONDARY-AND-EXAM` | school filter uses gender + approved education-level mapping; no group inference. |
| `OWNER-20260908-SFC-BATCH-SCHOOL-FINANCE-FILE-LIFECYCLE` | school/file semantics remain active; finance mirror/cleanup semantics preserved but implementation suspended. |
| `OWNER-20260908-SFC-BATCH-MAIN-FORM-CONSTRUCTION-READY` | main-form semantics closed for materialization; v0.6 synthetic scaffold authorized; implementation/runtime remains `NOT_PROVEN`; later finance suspension narrows active implementation scope. |

### event86 exact finance / file consequences — finance semantics preserved

- independent `registration_status_code` is removed; `finance_status` remains the preserved canonical status field definition.
- `registration_center_code` semantics remain Officer-only/non-public with `0=مرکز` default, `1=گلستان`, `2=صدرا`.
- `tuition_amount`, `discount_amount`, `discount_title` initial defaults are empty.
- `net_payable_amount` semantic is system-owned: empty if tuition is empty; otherwise `tuition - (discount if present else 0)` without writing zero into blank `discount_amount`.
- final discount catalog has 41 code/name choices, explicitly includes `109=سازمان زندان‌ها` and excludes `102=سپاه پاسداران`.
- all finance-specific runtime implementation/validation above is suspended until Owner reopen.
- `student_photo`: one jpg/jpeg <=5MB, GP File Upload Pro, required 3:4 crop, max 1200×1600, no minimum dimensions, no custom/background/AI pipeline.
- `report_card_file`: one jpg/jpeg/pdf <=5MB; event85 visibility/requiredness and safe file lifecycle remain.
- Trash retains primary photo/report-card files; permanent Entry deletion removes primary files; backup/export/log retention remains open Privacy scope.

## Current Owner decisions — code editing

`OWNER-20260907-OFFICER-EDIT-LABELS-SYSTEM-CODES`: Officer edits human-readable school/group/status labels/choices. System writes matching canonical code/value. Raw technical codes are not directly editable. This refines old `school_code Admin-only` interpretation only for system-mediated updates caused by Officer-visible selection.

## Environment progression

`OWNER-20260906-SKIP-RESIDUAL-ENV-INVENTORY`: Environment Inventory remains `PARTIAL/OWNER_ACCEPTED_FOR_PROGRESS`; residual staging/license/cache/build identity reopens only when decision-critical. This is not a PASS.

event86 adds GP File Upload Pro exact installed version/license/entitlement and post-import `3:4` + `1200×1600` read-back to the environment facts that must be proven before release; this does not close Environment Inventory.

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
- Scanner population as current-release cheque path — superseded by scanner deferral.
- older product-knowledge global Stage0 blockers — superseded by Addendum/current Master.
- Google Sheet as live runtime SSOT — superseded by `OWNER-20260907-REPOSITORY-RUNTIME-SSOT` after completed repository cutover.
- independent/public `registration_status_code` projection — superseded by event86; `finance_status` remains the preserved canonical status definition.
- old D-12 projection that disallowed all maintained crop/downscale — superseded only to the limited event86 GP File Upload Pro behavior; custom/background/AI processing remains forbidden.
- prior projection that finance/manual-cheque implementation and Nested Forms POC are current progression/release gates — applicability superseded by `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC`; finance semantics themselves are preserved.

## Evidence observations that must not be promoted

- PersianGravity 4.1.0 Owner smoke = `OWNER_REPORTED_SMOKE_PASS` with unspecified coverage, not full runtime validation.
- PR merge/CI = source implementation evidence, not browser/Nested Forms lifecycle proof.
- `V-01..V-06` remain unexecuted unless later live evidence explicitly updates them.
- `PRB-NESTED-CHEQUE-001` remains `NOT_PROVEN` even while deferred; deferred does not mean PASS or absence.
- D-17 remains POC-gated/not-proven.
- v0.6.0 local artifact conformance does not equal Gravity Forms staging import/read-back.
- recording the daily manager SMS requirement does not prove a scheduler/provider/candidate has been selected or implemented.

## Update rule

A material Owner decision or executed probe/result must update `runtime/CURRENT_STATE.yaml` and append one event to `runtime/DECISION_HISTORY.jsonl` in the same accepted Git commit; then both are read back from `main`. Reflect it here only when it changes durable project semantics. Discussion-only events do not belong here.

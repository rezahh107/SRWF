# SRWF Decision Ledger

این ledger تصمیم‌های durable/current را نگه می‌دارد. Runtime truth در `runtime/CURRENT_STATE.yaml` و `runtime/DECISION_HISTORY.jsonl` است.

## Architecture locks

- `D-01` Needs Review = ordinary Entry field + reason; no custom state/queue/POST/Entry Notes.
- `D-02` single operational inbox = Gravity Flow Inbox.
- `D-03` single Registration Officer baseline.
- `D-04` native Gravity Flow Officer edit with smallest whitelist.
- `D-05` formal Approval only native Gravity Flow Approval.
- `D-06` routine/review edits: no notifications.
- `D-07` native Live Refresh; no custom polling.
- `D-08` no custom concurrency/locking.
- `D-09` current main-form school surface = GP Advanced Select, GF Enhanced UI off; `V-03` still NOT_PROVEN.
- `D-10` repeated National ID allowed.
- `D-11` maintained Iranian mobile/Jalali/National-ID solution; no custom kernel.
- `D-12` **amended by event86**: no custom/background/AI image-processing pipeline; maintained GP File Upload Pro crop/downscale is allowed/required only for 3:4 crop + max 1200×1600, no minimum dimensions.
- `D-13` human edit audit via GravityRevisions; Admin-only.
- `D-14` no direct GFAPI update path baseline.
- `D-15` WP All Import owns counter sync by exact National ID.
- `D-16` importer writes counter, not Flow progression.
- `D-17` first renderer POC = Gravity PDF Free + SRWF-owned print layer.

## Durable SFC decisions

- names + father_name + student_mobile required; `home_phone` included but optional; contact mobiles optional and relationships fixed hidden.
- `finance_status`: `0=عادی,1=بنیاد شهید,3=حکمت`, non-public/Officer-only/optional/default 0.
- `registration_status_code` independent field is removed by event86.
- `registration_center_code`: Officer-only, `0=مرکز` default, `1=گلستان`, `2=صدرا`.
- `education_level` five controlled labels; one `grade_group_selection` Dropdown; hidden system `group_code`; graduation status conditional/server-validated.
- school: Owner SchoolReport source, 946 retained + Other, exclude `1296,1314,1316,1319`; full-name labels; filter gender+education level only; GP Advanced Select mandatory; no group-specific school filter.
- report-card required codes: `283,286,291,650,663,666,667,1320,1351`; Other visible optional; hidden otherwise.
- current file access = Admin + Registration Officer.

## Event78–86 material Owner decisions

| Decision | Durable effect |
|---|---|
| `OWNER-20260908-FOUNDATION-FIELDS-OFFICER-ONLY` | restore Bonyad Shahid case/type as Officer-only optional when finance=1. |
| `OWNER-20260908-DISCOUNT-CODE-CATALOG-41-SEPARATE-FINANCE` | separate 41-choice coded discount from amount/title. |
| `OWNER-20260908-DISCOUNT-CODE-CATALOG-NAME-CODE-ONLY` | percentage removed; code+name only. |
| `OWNER-20260908-HEKMAT-SERVER-DERIVED-CLEAR-ON-EXIT` | Hekmat values server-owned and cleared when finance leaves 3. |
| `OWNER-20260908-SCHOOL-GENDER-FILTER-AUTHORITATIVE-METADATA` | gender filter requires authoritative per-school metadata; Other exempt. |
| `OWNER-20260908-SCHOOL-SOURCE-1405-EXCLUDE-INVALID-4` | current SchoolReport selected; four invalid codes excluded; retained set=946. |
| `OWNER-20260908-SCHOOL-LEVEL-MAPPING-SECONDARY-AND-EXAM` | SchoolReport level mapping locked; no group inference. |
| `OWNER-20260908-SFC-BATCH-SCHOOL-FINANCE-FILE-LIFECYCLE` | full-name school labels, school-name mirrors, file lifecycle, Bonyad/discount cleanup/export semantics closed. |
| `OWNER-20260908-SFC-BATCH-MAIN-FORM-CONSTRUCTION-READY` | main-form business semantics closed through event86; v0.6 materialization authorized with synthetic data; runtime implementation remains NOT_PROVEN. |

### Event86 finance/file specifics

- amounts are raw integer Rial; `tuition_amount`/`discount_amount`/`discount_title` default empty.
- net is system-owned: empty if tuition empty, else tuition minus discount treating blank discount as zero without persisting zero.
- discount>tuition => error/no-save.
- final discount catalog = 41 code/name choices, includes `109=سازمان زندان‌ها`, excludes `102=سپاه پاسداران`.
- `student_photo`: one jpg/jpeg <=5MB, File Upload Pro, required 3:4 crop, max 1200×1600.
- `report_card_file`: one jpg/jpeg/pdf <=5MB.
- safe replace/delete; Trash retains primary files; permanent Entry deletion deletes primary student files; backup retention still open.

## Finance/cheque/scanner

- canonical/display unit = Rial; current finance/manual-cheque fields non-public/Officer-only.
- multi-cheque host = GP Nested Forms, `POC_NOT_PROVEN`; Parent-Child fallback only after bounded FAIL.
- current scanner path deferred; seven Sayad fields hidden/future-reserved.
- POS/PC-POS and online Sayad deferred.

## Repository governance

`OWNER-20260907-REPOSITORY-RUNTIME-SSOT`: GitHub `main` is sole project/runtime SSOT after cutover; Google Sheet is deprecated read-only provenance. Material state changes require CURRENT_STATE + append-only history in one accepted commit and main read-back.

## Superseded/historical

- `OWNER-20260907-HOME-PHONE-REQUIRED` superseded by included-but-optional.
- public/independent `registration_status_code` superseded by event86.
- old D-12 “upload only/no maintained crop” projection amended by event86 limited File Upload Pro allowance.
- native Enhanced UI school candidate failed; event86 locks GP Advanced Select for current form.
- scanner population current-release path superseded by scanner deferral.
- Google Sheet live SSOT superseded after repository cutover.

## Evidence boundary

`V-01..V-06`, Nested host POC and D-17 remain unexecuted/not-proven unless later runtime evidence says otherwise. Documentation/artifact PASS is not staging/runtime PASS.

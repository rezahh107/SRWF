---
document_id: SRWF-MASTER
source_version: 1.9.0
repository_materialization: 1.0.0-baseline
status: NATIVE_FIRST_SELECTED_PRESERVED__IMPLEMENTATION_AUTHORIZED_NOT_COMPLETED
language: fa-IR
full_pre_repository_source: history/pre-repository/srwf_pre_repository_sources.tar.gz.b64.part01
---

# SRWF Master Authority — Repository Entrypoint

این فایل **entrypoint پایدار** سند مادر SRWF در دورهٔ repository است. متن کامل byte-exact سند مادر pre-repository و سایر sourceهای 01..11 در archive provenance زیر `history/pre-repository/` حفظ می‌شود. این entrypoint current governing semantics را با stable paths و Owner decisions جاری ارائه می‌کند؛ presence یک source تاریخی به معنی current authority نیست.

## Authority order

1. safety/platform
2. current explicit Owner decision
3. repository governance (`AGENTS.md`, `repository.manifest.yaml`)
4. این Master
5. `docs/operations/EXECUTION_PLAYBOOK.md` + governance addenda
6. standalone contracts زیر `docs/contracts/`
7. accepted decision/validation evidence
8. knowledge/evidence/history
9. general knowledge

اگر contract یا supporting doc با این Master تعارض مادی داشت، silently merge نکن. `CONTRADICTION → STOP → OWNER RE-ADJUDICATION`.

## Architecture — locked

- WordPress + Gravity Forms + Gravity Flow = parent architecture.
- Gravity Forms = canonical data authority.
- Gravity Flow = تنها workflow/assignment/formal Approval authority و primary Officer operational surface.
- parallel DB/workflow state/queue/Desk ممنوع.
- GravityView فقط presentation اختیاری پس از proven gap.
- Elementor operational baseline نیست.
- thin custom integration فقط برای residual proven gap.

## Locked decisions D-01..D-17

| ID | Current lock |
|---|---|
| `D-01` | Needs Review فقط ordinary Entry field + reason؛ نه custom state/queue/POST و نه Entry Notes dependency. |
| `D-02` | operational inbox واحد = native Gravity Flow Inbox؛ no GravityView queue. |
| `D-03` | یک Registration Officer؛ no multi-officer reassignment/concurrency matrix. |
| `D-04` | Officer editing = native Gravity Flow با smallest whitelist؛ no custom edit system/GFAPI baseline. |
| `D-05` | formal Approval exclusively native Gravity Flow Approval. |
| `D-06` | routine/Needs Review edits notification ندارند. |
| `D-07` | native Gravity Flow Live Refresh کافی؛ no custom polling؛ operational cache نباید freshness را بشکند. |
| `D-08` | no custom concurrency/locking. |
| `D-09` | school selector فقط باید Persian-name search سریع/mobile را پاس کند؛ simplest native/maintained candidate first، stop at first PASS. Native Enhanced UI در target runtime FAIL شده و current maintained candidate = GP Advanced Select؛ `V-03` هنوز NOT_PROVEN است. |
| `D-10` | duplicate National ID blocking حذف؛ repeated National ID allowed/all Entries preserved. |
| `D-11` | mobile/Jalali/National-ID از ساده‌ترین maintained Iranian solution؛ no custom kernel. |
| `D-12` | photo processing out of current scope؛ simple required photo upload only. |
| `D-13` | human-edit audit only via GravityRevisions, Admin-only؛ no API/import/system parity bridge. |
| `D-14` | no direct GFAPI update path baseline. |
| `D-15` | WP All Import syncs `registration_counter`; exact National ID business key; same National ID => same counter. |
| `D-16` | importer writes counter, not Flow progression; native Flow bulk completion if sufficient. |
| `D-17` | dossier print first POC = Gravity PDF Free + SRWF-owned print layer; no paid template/extension baseline; no custom PDF engine; Browser Print not parallel production renderer. |

## Current verification set

`V-01..V-06` همگی تا executed target-runtime evidence برابر `UNEXECUTED / NOT_PROVEN` هستند:

- `V-01`: Inbox → Entry Details → allowed edit → native Approve → correct next step.
- `V-02`: minimal access smoke.
- `V-03`: responsive Persian school search/mobile + correct stored value.
- `V-04`: GravityRevisions human edit history, Admin-only.
- `V-05`: Live Refresh + cache correctness.
- `V-06`: WP All Import counter sync by exact National ID.

## Stage/Gate state

| Unit | Current state |
|---|---|
| Parent architecture | `SELECTED/PRESERVED` |
| Environment Inventory | `PARTIAL / OWNER_ACCEPTED_FOR_PROGRESS` |
| Semantic Field Contract | `OWNER APPROVED / CLOSED` semantically; repository materialization has named gaps, not silent guesses |
| Authoritative scaffold | `AUTHORIZED / NOT YET BUILT` |
| Implementation Mapping | `AFTER SCAFFOLD / UNBOUND` |
| Privacy/retention | `OWNER DECISION REQUIRED` before real PII |
| GP Nested Forms cheque host | `SELECTED / POC_NOT_PROVEN` |
| Structured Scanner in current SRWF release | `DEFERRED` |
| D-17 renderer | `POC_GATED / NOT_PROVEN` |
| Production readiness | `NOT ACHIEVED` |

## Semantic Field Contract Gate

Machine-readable field semantics live in `docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml`.

For every material field explicitly separate:

- `include_in_form`
- `value_required`
- source/canonical representation
- normalization/server validation
- public/Officer/Accountant visibility
- Officer editability
- workflow/export/print role
- sensitivity/retention
- write paths
- semantic status / binding status

**Current explicit correction:** `home_phone` must exist in public scaffold but its value is optional. `father_name`, `first_name`, `last_name`, and `student_mobile` are required. This follows current Owner decisions and prevents the prior summary omission from recurring.

Legacy GF/report column presence alone is not a current requirement. An unbound field stays `UNBOUND`; do not infer it into the scaffold.

## Implementation Mapping Gate

After scaffold, bind actual runtime IDs only in `docs/contracts/IMPLEMENTATION_MAPPING.yaml`:

- Form IDs
- Field/Input IDs
- Officer Approval Step ID
- Accountant Approval Step ID
- final external-pending Step ID
- route/page/View IDs where applicable
- plugin/version manifest

Binding by translated label or invented ID has no authority.

## Current-release finance

- canonical/display unit = Rial.
- `tuition_amount`, `discount_amount`, `discount_title`, `net_payable_amount` current-release optional and non-public/Registration-Officer-only.
- `discount_amount` may default to 0.
- `net_payable_amount = tuition_amount - discount_amount`.
- `discount_amount > tuition_amount` => validation error + no save.
- manual cheque fields current-release optional/Officer-only.
- POS/PC-POS and online Sayad inquiry deferred.

## Multi-cheque / Scanner

- requirement = `1..N` cheques.
- selected host = GP Nested Forms; each cheque = child Entry.
- Parent-Child Forms fallback only after bounded Nested Forms FAIL.
- no custom relationship DB/workflow/state.
- current release = manual cheque entry only.
- Scanner path deferred; seven Sayad fields hidden/future-reserved: `qr_version`, `owner_type`, `owner_identifier`, `iban`, `bank_branch`, `cheque_serial`, `sayad_id`.
- generic PersianGravity Structured Scanner capability may exist independently; it does not own SRWF data/workflow and raw payload must not persist.

## Officer operational contract

- native Gravity Flow Inbox + Entry Details.
- Officer edits human-readable school/group/status choices; system writes matching canonical code/value. raw technical code direct edit ممنوع.
- Needs Review remains Entry overlay field; same step/assignee.
- only native Approve advances workflow.
- no notification for routine edits.
- no custom Desk/list/lock.

## Security / PII

- UI hiding != authorization.
- every operational action requires authenticated user + native assignment/capability authorization.
- student photo/report-card: Admin + Registration Officer under current decision.
- full GravityRevisions = Admin-only.
- no real PII in staging/UAT/production before `PRIVACY_RETENTION_CONTRACT` Owner sign-off.
- no real PII/intake images/operational ledgers in Git.

## Required release artifacts

Before release, repo must contain current/verified:

- Semantic Field Contract
- Implementation Mapping
- Environment Manifest
- required POC reports / `V-01..V-06` evidence
- Test Matrix / Definition of Done evidence
- Release Manifest
- Rollback Runbook
- Privacy/Retention sign-off

`DOCUMENTED` does not equal `OBSERVED_IN_STAGING`.

## Repository-era provenance and normalization

- Full pre-repository source corpus 01..11 is preserved byte-exact in `history/pre-repository/` as an encoded compressed archive with SHA-256 manifest.
- Active paths are stable; versions live in metadata/Git history rather than version-suffixed active filenames.
- Repository migration repaired pointer drift only; it does not promote runtime validation or reopen architecture.
- A known repository materialization gap must remain visible as `INCOMPLETE`, never be filled by guess.

## Exact next action

Complete and validate the repository documentation baseline. After baseline merge/read-back, return to authoritative Gravity Forms + Gravity Flow scaffold using synthetic data only, unless a named contract materialization gap is decision-critical to that scaffold. Then bind actual IDs in Implementation Mapping. Real PII remains blocked until privacy/retention sign-off.

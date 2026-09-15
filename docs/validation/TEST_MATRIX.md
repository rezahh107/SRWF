# SRWF Test Matrix

**Rule:** generated/documented test ≠ executed test. A row changes from `UNEXECUTED/NOT_PROVEN` only with executed evidence on the named target/environment.

| ID | Requirement | Current state | PASS observable | Evidence location |
|---|---|---|---|---|
| `V-01` | native Flow operational slice | `UNEXECUTED / NOT_PROVEN` | Inbox → assigned Entry Details → edit allowed field without step/assignee change → native Approve → correct next step | `pocs/V-01/` |
| `V-02` | minimal access | `UNEXECUTED / NOT_PROVEN` | public denied operational data; Officer only assigned operational access; Admin administrative access; tampered URL/action rejected | `pocs/V-02/` |
| `V-03` | Persian school search/mobile | `NOT_PROVEN`; native Enhanced UI candidate observed FAIL | fast Persian-name typing/search on mobile at real-scale school catalog; correct canonical school value persisted | `pocs/V-03/` |
| `V-04` | human edit revisions | `UNEXECUTED / NOT_PROVEN` | Officer/Admin human edit produces revision; Admin can view/compare/restore; Officer cannot access full history | `pocs/V-04/` |
| `V-05` | live freshness/cache | `UNEXECUTED / NOT_PROVEN` | native Gravity Flow Live Refresh updates work; operational routes not held stale by cache/optimizer | `pocs/V-05/` |
| `V-06` | counter import | `UNEXECUTED / NOT_PROVEN` | exact National-ID matching updates only `registration_counter`; all same-ID Entries receive same counter; import does not advance Flow | `pocs/V-06/` |
| `PRB-NESTED-CHEQUE-001` | GP Nested Forms host | `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN` | retained future criterion: child form renders in required Flow editable surface; manual entry/correction persists; submit links correct parent; reload survives; finance/print composition reads all children | `pocs/PRB-NESTED-CHEQUE-001/` |
| `D-17-GRAVITY-PDF` | dossier renderer | `POC_GATED / NOT_PROVEN` | Persian/RTL/ZWNJ + leading-zero National ID + Jalali date + representative amounts/table content + A4 pagination + searchable/copyable Unicode + normal Officer open/print UX | `pocs/D-17-GRAVITY-PDF/` |

`PRB-NESTED-CHEQUE-001` is retained so its future PASS contract is not lost, but after `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC` it is **not a current progression or release gate** until finance scope is explicitly reopened.

## Main-form scaffold read-back prerequisites (event86 + scope suspension)

These are required observations before promoting the v0.6.0 scaffold beyond artifact-level PASS; they do not create a new workflow authority or replace `V-01..V-06`.

- Gravity Forms imports the provisional form without material warning/error and real Form/Field IDs are read back into Implementation Mapping.
- `student_photo`: GP File Upload Pro enabled; one jpg/jpeg <=5MB; crop required; UI read-back shows `3:4`; Maximum Dimensions `1200×1600`; no minimum dimensions.
- `school_code`: 947 choices import, excluded four codes absent, GP Advanced Select active, GF Enhanced UI off; runtime gender+level filtering and server guard remain implementation tests before `V-03`.
- finance/status/discount/Bonyad/Hekmat/manual-cheque fields may remain present as reserved optional non-public fields according to the preserved SFC, but finance-specific Flow exposure, calculations, conditional cleanup and cheque composition are suspended and are not required to promote the current non-finance scaffold path.
- current required server-binding work is limited to non-suspended scope such as DOB/mobile/group/school/report-card/file-access/file-lifecycle and other non-finance canonical/validation rules. Finance-specific amount/discount/Bonyad/Hekmat/cheque bindings remain deferred until Owner reopen.

## Recorded future requirement — daily manager SMS

`REQ-DAILY-MANAGER-SMS` = `RECORDED / IMPLEMENTATION_UNSELECTED / NOT_A_CURRENT_GATE`.

Future observable after implementation selection: at the end of a configured working day, the manager receives an SMS whose count equals the Entries the Registration Officer actually approved/advanced to Accountant during that business day. Count evidence must come read-only from canonical GF/Flow data and the reporting action must not mutate workflow state. Exact time/calendar/provider/mobile binding/retry semantics are still open. Cron/Cron-like shared-host scheduling is not an accepted baseline without Owner re-adjudication.

## Historical candidate observations

### School search
- Gravity Forms Drop Down + native Enhanced UI: target-runtime responsive behavior observed unacceptable → candidate FAIL only.
- GP Advanced Select: current maintained candidate selected; final `V-03` PASS still pending.

### Scanner
Generic PersianGravity Structured Scanner source/UI evidence exists, but **scanner population is deferred from current SRWF release** and is not a current-release PASS requirement.

## Test data rule

Until Privacy/Retention sign-off, every POC/test uses synthetic data. No copied production/student PII.

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
| `PRB-NESTED-CHEQUE-001` | GP Nested Forms host | `SELECTED / POC_NOT_PROVEN` | child form renders in required Flow editable surface; manual entry/correction persists; submit links correct parent; reload survives; finance/print composition reads all children | `pocs/PRB-NESTED-CHEQUE-001/` |
| `D-17-GRAVITY-PDF` | dossier renderer | `POC_GATED / NOT_PROVEN` | Persian/RTL/ZWNJ + leading-zero National ID + Jalali date + amounts/cheque table + A4 pagination + searchable/copyable Unicode + normal Officer open/print UX | `pocs/D-17-GRAVITY-PDF/` |

## Historical candidate observations

### School search
- Gravity Forms Drop Down + native Enhanced UI: target-runtime responsive behavior observed unacceptable → candidate FAIL only.
- GP Advanced Select: current maintained candidate selected; final `V-03` PASS still pending.

### Scanner
Generic PersianGravity Structured Scanner source/UI evidence exists, but **scanner population is deferred from current SRWF release** and is not a current-release PASS requirement for Nested cheque POC.

## Test data rule

Until Privacy/Retention sign-off, every POC/test uses synthetic data. No copied production/student PII.

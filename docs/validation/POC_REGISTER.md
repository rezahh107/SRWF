# SRWF POC Register

## Current POCs

| POC | Candidate / surface | State | Current meaning |
|---|---|---|---|
| `V-01 / PRB-NF-V01` | Native Gravity Flow Inbox/Entry Details/Edit/Approve | `UNEXECUTED / NOT_PROVEN` | required before release |
| `V-02 / PRB-NF-V02` | Native access/security | `UNEXECUTED / NOT_PROVEN` | required before release |
| `V-03 / PRB-NF-V03-SCHOOL-SEARCH` | Persian school search/mobile | `NOT_PROVEN` | native Enhanced UI candidate FAIL; GP Advanced Select current candidate |
| `V-04 / PRB-NF-V04-HUMAN-REVISION` | GravityRevisions human edits | `UNEXECUTED / NOT_PROVEN` | required before release |
| `V-05 / PRB-NF-V05` | Live Refresh + cache | `UNEXECUTED / NOT_PROVEN` | required before release |
| `V-06 / PRB-NF-V06` | WP All Import counter sync | `UNEXECUTED / NOT_PROVEN` | required before release |
| `PRB-NESTED-CHEQUE-001` | GP Nested Forms cheque child Entries | `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN` | selected future host retained; not a current gate; Parent-Child Forms fallback only after bounded FAIL following Owner reopen |
| `D-17-GRAVITY-PDF` | Gravity PDF Free + SRWF print layer | `POC_GATED / NOT_PROVEN` | first print renderer candidate |

`OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC` preserves the Nested Forms candidate/PASS contract but suspends execution until finance/cheque scope is explicitly reopened. `DEFERRED` does not mean PASS or proven absence.

## Recorded requirement without active POC

### `REQ-DAILY-MANAGER-SMS`

State: `REQUIREMENT_RECORDED / IMPLEMENTATION_UNSELECTED / NOT_A_CURRENT_GATE`.

Need: at the end of each working day, send the manager an SMS containing the count of Entries the Registration Officer approved/advanced to Accountant during that business day, derived read-only from canonical Gravity Forms/Gravity Flow evidence.

No POC is authorized yet because implementation mechanism/time/calendar/provider/mobile binding/retry behavior remain open. Cron/Cron-like shared-host scheduling is not an accepted baseline without Owner re-adjudication. Gravity Forms Notification Scheduler and `gravity-notification-manager` remain candidates only.

## Closed candidate observations

### Native school Enhanced UI
`FAIL_CANDIDATE` — Owner observed responsive/mobile behavior unacceptable. This rejects only that candidate and does not reopen D-09.

### Gravity Forms import scaffold v0.1-v0.4 historical work
- v0.1 generated and locally checked, then target import warnings observed.
- v0.2 metadata patch pending retry at that point.
- v0.3 wrapper format observed wrong for native GF import container.
- v0.4 retained as a **historical provisional candidate** with no successful target-runtime import proof.

Repository baseline does **not** promote old v0.4 into authoritative current scaffold because the current Semantic Field Contract has since changed/refined. New authoritative scaffold must be built from the current contract.

## Scanner evidence boundary

PersianGravity Structured Scanner source/CI and some browser UI presence were observed historically, but:

- raw scanner capture is designed non-persistent;
- scan-to-populate target behavior is not a current SRWF release gate;
- scanner population remains deferred;
- seven Sayad fields remain hidden/future-reserved.

## POC record format

Each executed POC folder should contain:

- `README.md` — requirement/candidate/environment
- `criteria.yaml` — exact observable PASS/FAIL
- `execution.md` — steps actually executed
- `evidence/` — non-PII screenshots/log excerpts/IDs as appropriate
- `result.yaml` — PASS/FAIL/INCOMPLETE + date + environment + evidence refs

No synthetic/generative report may be labeled executed evidence without actual run evidence.

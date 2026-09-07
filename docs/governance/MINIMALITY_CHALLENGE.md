# SRWF Minimality Challenge

`ACTIVE_NORMATIVE` — هر dependency/سطح جدید باید یک gap اثبات‌شدهٔ capability بومی را حل کند.

| Component/addition | Current ruling |
|---|---|
| Gravity Forms + Gravity Flow | `KEEP — AUTHORITY` |
| GravityRevisions | `KEEP — REQUIRED BY V-04` |
| WP All Import | `KEEP — REQUIRED BY V-06` |
| simple maintained Iranian input solution | `KEEP IF SIMPLEST PASSING` |
| GravityView | `OPTIONAL — ONLY IF PRESENTATION GAP PROVEN` |
| custom Desk/queue/list | `REJECT` |
| custom locking/concurrency | `REJECT` |
| custom Needs Review endpoint | `REJECT` |
| system/API audit bridge | `REJECT` under current D-13 scope |
| duplicate blocking | `REJECT` |
| custom Iranian validation kernel | `REJECT` |
| photo processing/optimization | `OUT_OF_CURRENT_SCOPE` |
| direct project GFAPI write path | `REJECT` |
| Gravity PDF Free + SRWF print layer | `KEEP AS D-17 POC CANDIDATE` |
| GP Nested Forms | `KEEP AS SELECTED HOST PENDING POC`; no automatic purchase |
| PersianGravity Structured Scanner | `CAPABILITY RETAINED`; current SRWF scanner use deferred |
| custom cheque relationship table/state | `REJECT` |
| POS/Windows utility current release | `DEFER` |
| CPT/ACF/JetEngine mirror | `REJECT` |
| monitoring platform | `REJECT` unless a later scoped requirement proves need |

## WHAT NOT TO BUILD

Do not build or introduce as baseline:

- second workflow step/branch/state for Needs Review;
- custom Boolean replacing Flow current step;
- Officer Reject;
- wp-admin replacement/SPA/REST front-end only for Desk appearance;
- dual Inbox implementations;
- Quick Actions approval;
- GravityView workflow/bulk-approval/delete for Officer;
- custom optimistic success state;
- label-based field lookup;
- raw SQL against GF/Flow tables;
- custom state/audit DB;
- runtime school DB/sync service when controlled static mapping suffices;
- city inference from National ID;
- unconditional duplicate prevention;
- heavy image editor/forced crop/compression pipeline;
- PDF archive subsystem or custom PDF engine;
- WebSocket/message queue/Cron polling/background worker for current operational freshness;
- analytics/SLA/escalation dashboard before requirement;
- custom field versioning parallel to GravityRevisions;
- data mirror for Elementor;
- Elementor visibility as authorization;
- Entry creator ownership as Officer authorization;
- Entry Notes as workflow state;
- GravityView Entry Approval/Tags as parallel workflow state;
- GravityImport for counter update;
- WP All Import `Update all`, `Delete missing`, fuzzy Entry match in counter path;
- assumptions that importer/automation writes run GF validation/feeds/Flow/Revisions automatically;
- automations owning Officer assignment/Needs Review/Approval/current step;
- direct SQL writes into GF/Flow;
- global Jalali/number conversion without storage/export regression evidence;
- Matrix2 workflow logic;
- legacy form ID compatibility/migration as a requirement;
- plugin-core modifications;
- large god-script/framework introduced before a proven residual gap.

## Challenge question

Before adding anything, answer: **کدام acceptance criterion فعلی با native/maintained stack قابل برآورده‌شدن نیست، و چه executed evidence این gap را اثبات کرده است؟**

اگر پاسخ وجود ندارد، addition مجاز نیست.

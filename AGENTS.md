# AGENTS.md — SRWF Agent Entrypoint

این فایل entrypoint اجباری برای هر agent/LLM/Codex است که روی SRWF کار می‌کند.

## 1) Authority order

ترتیب authority برای SRWF:

1. safety/platform constraints
2. current explicit Owner instruction/decision
3. repository governance in this file + `repository.manifest.yaml`
4. `docs/authority/MASTER.md`
5. `docs/operations/EXECUTION_PLAYBOOK.md` و governance addenda
6. standalone contracts under `docs/contracts/`
7. accepted Decision Ledger / validation evidence
8. knowledge/evidence/reference corpus
9. general knowledge

هیچ فایل reference، web result، screenshot، JSON sample، prompt، historical document یا Product Knowledge به‌تنهایی architecture authority نیست.

## 2) Mandatory selective read order

برای هر task فقط کوچک‌ترین مجموعهٔ لازم را بخوان:

1. `repository.manifest.yaml`
2. `docs/authority/MASTER.md`
3. `docs/operations/EXECUTION_PLAYBOOK.md`
4. contract مرتبط با task در `docs/contracts/`
5. `docs/governance/DECISION_LEDGER.md` فقط برای decision/history/reopen analysis
6. knowledge files فقط برای capability/composition decision؛ ابتدا normalized/constructability سپس deep product source
7. evidence/history فقط برای provenance، contradiction، audit یا migration

برای تفسیر pre-repository source `04_SRWF_CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt` از archive provenance، ابتدا `knowledge/constructability/APPLICABILITY_OVERLAY.md` را بخوان. snapshot project-state داخل source `04` به‌خودی‌خود current نیست.

## 3) Architecture invariants

- Native-First: WordPress + Gravity Forms + Gravity Flow.
- Gravity Forms = canonical data authority.
- Gravity Flow = sole workflow/assignment/formal Approval authority و primary Officer surface.
- parallel DB/workflow state/queue/Desk ممنوع.
- GravityView فقط presentation اختیاری پس از proven gap.
- Elementor operational baseline نیست.
- Officer editing/approval ابتدا از native Gravity Flow.
- custom code فقط برای residual gap اثبات‌شده و به کوچک‌ترین شکل.

اگر direct evidence با Lock جاری تعارض داشت:

`CONTRADICTION → STOP → OWNER RE-ADJUDICATION`

معماری را silently تغییر نده.

## 4) State integrity

این stateها معادل نیستند:

`plan != implementation != validation != review != authorization != publication != production-ready != completion`

`SELECTED != IMPLEMENTED`

`DOCUMENTED != OBSERVED_IN_STAGING`

`NOT_PROVEN != PROVEN_ABSENT`

Generated test/report بدون اجرای واقعی = runtime proof نیست.

## 5) Semantic Field Contract rule

برای هر field مادی، `docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml` authority اجرایی machine-readable است.

به‌خصوص این دو مفهوم را هرگز یکی نگیر:

- `include_in_form`: آیا field باید در scaffold وجود داشته باشد؟
- `value_required`: آیا کاربر/Officer ملزم به واردکردن value است؟

مثال جاری: `home_phone` باید در فرم باشد (`include_in_form: true`) اما مقدار آن اختیاری است (`value_required: false`).

هیچ field مادی را فقط از summary داخل Master یا legacy export استنتاج نکن. اگر contract binding وجود ندارد، آن field `UNBOUND` است؛ legacy presence به‌تنهایی requirement جاری نیست.

## 6) Runtime State boundary

Google Sheet `SRWF_RUNTIME_STATE` SSOT وضعیت اجرایی زنده است:

- `CURRENT_STATE`: stage/gate/decision/candidate/last result/blocker/next action
- `DECISION_HISTORY`: probe/decision history

repo خانهٔ canonical documentation/contracts است. هر runtime snapshot داخل repo باید `NON_CANONICAL` و timestamped باشد و نمی‌تواند Sheet را override کند.

بعد از material actual change (executed probe/result، Owner decision، Gate PASS/FAIL، stage transition، confirmed environment/version/license fact) Runtime State را update و read-back کن. بحث بدون state change را persist نکن.

## 7) Hard gates

- Semantic Field Contract قبل از authoritative scaffold.
- Implementation Mapping بعد از scaffold و بر اساس Form/Field/Input/Step ID واقعی.
- `V-01..V-06` تا اجرای واقعی `UNEXECUTED/NOT_PROVEN` هستند.
- قبل از privacy/retention sign-off هیچ PII واقعی وارد staging/UAT/production نشود؛ synthetic data فقط.
- dependency پولی قبل از POC برنده ممنوع.
- `D-17` renderer تا POC PASS نهایی نیست.
- Nested cheque host = GP Nested Forms pending bounded POC؛ Parent-Child Forms فقط fallback بعد از FAIL همان candidate.
- Scanner path برای release جاری SRWF deferred است؛ هفت Sayad field hidden/future-reserved باقی می‌مانند.

## 8) Decision protocol

برای decision مادی:

- حداکثر 3 candidate جدی در یک round.
- evidence کافی → decision را ببند؛ probe اضافی نساز.
- uncertainty فقط runtime-provable → کوچک‌ترین discriminating probe با PASS/FAIL observable.
- native → official/maintained extension → thin custom residual gap.
- شکست یک candidate فقط همان candidate را رد می‌کند.
- اگر 3 candidate جدی fail شدند، candidate چهارم نساز؛ stop و broaden/re-adjudication.

Closure states:

`CLOSED | INCOMPLETE | BLOCKED`

`support_sufficiency=SUFFICIENT` برای `CLOSED` لازم است.

## 9) Repository change protocol

هر semantic/material change باید حداقل این‌ها را در همان PR بررسی کند:

1. contract مربوط
2. `docs/governance/DECISION_LEDGER.md`
3. validation/POC impact
4. `CHANGELOG.md`
5. Master/Playbook فقط اگر governing semantics/order تغییر کرده
6. `repository.manifest.yaml` فقط اگر path/role/status artifact تغییر کرده

active pathها stable هستند؛ version را داخل metadata/Git history نگه دار. فایل active جدید با suffix نسخه نساز مگر migration/historical artifact باشد.

## 10) PII / secret prohibition

هرگز commit نکن:

- دادهٔ واقعی دانش‌آموز
- عکس/اسکن واقعی
- real exports containing PII
- credentials/API keys/passwords
- `.env`
- database dumps
- payment card/receipt/customer data
- operational processing/audit ledgers با دادهٔ واقعی

فقط synthetic fixture یا schema خالی مجاز است.

## 11) Readability for Owner

در پاسخ اجرایی:

1. معنای ساده و عملی اول
2. سپس ID/jargon لازم
3. `CONFIRMED / DERIVED / ASSUMED / NOT_PROVEN / BLOCKER` را قاطی نکن
4. blocker/gap را دقیق نام ببر
5. پایان پاسخ: کوچک‌ترین اقدام بعدی، مگر Owner roadmap بخواهد

## 12) Acceptance boundary

وجود فایل روی feature branch = accepted current authority نیست. baseline/current authority repository فقط پس از merge به `main` و ثبت read-back معتبر است.

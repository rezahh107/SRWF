# SRWF — Student Registration Workflow

SRWF سامانهٔ ثبت‌نام دانش‌آموز و گردش‌کار بررسی بر پایهٔ **WordPress + Gravity Forms + Gravity Flow** است.

## معماری قفل‌شده

- **Gravity Forms** مرجع canonical data است.
- **Gravity Flow** تنها مرجع workflow، assignment و formal Approval و رابط عملیاتی اصلی Officer است.
- parallel DB / workflow state / queue / Desk ممنوع است.
- **GravityView** فقط presentation اختیاری پس از اثبات gap است.
- Elementor baseline عملیاتی نیست.

## وضعیت فعلی

- Stage: `STAGE_0_IN_PROGRESS`
- Semantic Field Contract: `OWNER APPROVED / CLOSED`
- Environment Inventory: `PARTIAL / OWNER_ACCEPTED_FOR_PROGRESS`
- Next implementation unit: authoritative Gravity Forms/Gravity Flow scaffold با **synthetic data only**؛ سپس bind کردن IDهای واقعی در Implementation Mapping.
- تا بسته‌شدن privacy/retention هیچ PII واقعی وارد staging/UAT/production نمی‌شود.

> وضعیت اجرایی زنده در Google Sheet `SRWF_RUNTIME_STATE` نگهداری می‌شود. این repository خانهٔ canonical اسناد/قراردادهاست؛ snapshotهای runtime داخل repo در صورت وجود `NON_CANONICAL` هستند.

## Read order

1. [`repository.manifest.yaml`](repository.manifest.yaml)
2. [`AGENTS.md`](AGENTS.md) برای agentها / [`docs/INDEX.md`](docs/INDEX.md) برای انسان
3. [`docs/authority/MASTER.md`](docs/authority/MASTER.md)
4. [`docs/operations/EXECUTION_PLAYBOOK.md`](docs/operations/EXECUTION_PLAYBOOK.md)
5. contract مرتبط زیر [`docs/contracts/`](docs/contracts/)
6. فقط در صورت نیاز: [`knowledge/`](knowledge/) و [`evidence/`](evidence/)

## قراردادهای کلیدی

- [`SEMANTIC_FIELD_CONTRACT.yaml`](docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml) — canonical machine-readable field semantics
- [`SEMANTIC_FIELD_CONTRACT.md`](docs/contracts/SEMANTIC_FIELD_CONTRACT.md) — human-readable projection
- [`WORKFLOW_CONTRACT.md`](docs/contracts/WORKFLOW_CONTRACT.md)
- [`ACCESS_CONTROL_CONTRACT.md`](docs/contracts/ACCESS_CONTROL_CONTRACT.md)
- [`IMPLEMENTATION_MAPPING.yaml`](docs/contracts/IMPLEMENTATION_MAPPING.yaml) — بعد از scaffold bind می‌شود
- [`ENVIRONMENT_MANIFEST.md`](docs/contracts/ENVIRONMENT_MANIFEST.md)
- [`PRIVACY_RETENTION_CONTRACT.md`](docs/contracts/PRIVACY_RETENTION_CONTRACT.md)

## وضعیت‌ها را قاطی نکن

`plan != implementation != validation != review != authorization != publication != production-ready != completion`

`SELECTED != IMPLEMENTED`، `DOCUMENTED != OBSERVED_IN_STAGING`، `NOT_PROVEN != PROVEN_ABSENT`.

## تغییرات مادی

هر تغییر مادی باید:

1. authority/Owner decision لازم را داشته باشد؛
2. contract مربوط را update کند؛
3. در [`docs/governance/DECISION_LEDGER.md`](docs/governance/DECISION_LEDGER.md) ثبت شود؛
4. تست/POC مرتبط را update کند؛
5. در `CHANGELOG.md` ثبت شود؛
6. integrity checks را پاس کند.

## امنیت داده

دادهٔ واقعی دانش‌آموز، عکس/اسکن واقعی، export دارای PII، credential، database dump، payment data و operational ledger واقعی داخل Git قرار نمی‌گیرد. فقط schema، synthetic fixture و evidence غیرحساس مجاز است.

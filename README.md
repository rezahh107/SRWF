# SRWF — Student Registration Workflow

SRWF سامانهٔ ثبت‌نام دانش‌آموز و گردش‌کار بررسی بر پایهٔ **WordPress + Gravity Forms + Gravity Flow** است.

## معماری قفل‌شده

- **Gravity Forms** مرجع canonical data است.
- **Gravity Flow** تنها مرجع workflow، assignment و formal Approval و رابط عملیاتی اصلی Officer است.
- parallel DB / workflow state / queue / Desk ممنوع است.
- **GravityView** فقط presentation اختیاری پس از اثبات gap است.
- Elementor baseline عملیاتی نیست.

## Project SSOT

`main` در همین repository تنها SSOT پروژه است؛ هم اسناد/قراردادهای durable و هم وضعیت اجرایی جاری.

- وضعیت فعلی: [`runtime/CURRENT_STATE.yaml`](runtime/CURRENT_STATE.yaml)
- تاریخچهٔ material از cutover به بعد: [`runtime/DECISION_HISTORY.jsonl`](runtime/DECISION_HISTORY.jsonl)
- تاریخچهٔ قبل از cutover: [`history/pre-runtime-ssot/`](history/pre-runtime-ssot/)

Google Sheet قدیمی `SRWF_RUNTIME_STATE` بعد از cutover فقط `DEPRECATED_READ_ONLY_MIGRATION_SOURCE` است و برای state جدید update نمی‌شود.

این README عمداً Stage/next action پویا را کپی نمی‌کند؛ برای وضعیت واقعی همیشه `runtime/CURRENT_STATE.yaml` را بخوان.

Repository baseline: `ACCEPTED_CURRENT`.

## Read order

برای ادامهٔ یک session:

1. [`repository.manifest.yaml`](repository.manifest.yaml)
2. [`AGENTS.md`](AGENTS.md) برای agentها / [`docs/INDEX.md`](docs/INDEX.md) برای انسان
3. [`docs/authority/MASTER.md`](docs/authority/MASTER.md)
4. [`runtime/CURRENT_STATE.yaml`](runtime/CURRENT_STATE.yaml)
5. آخرین eventهای مرتبط در [`runtime/DECISION_HISTORY.jsonl`](runtime/DECISION_HISTORY.jsonl)
6. [`docs/operations/EXECUTION_PLAYBOOK.md`](docs/operations/EXECUTION_PLAYBOOK.md)
7. contract مرتبط زیر [`docs/contracts/`](docs/contracts/)
8. فقط در صورت نیاز: [`knowledge/`](knowledge/) و [`evidence/`](evidence/)

## قراردادهای کلیدی

- [`SEMANTIC_FIELD_CONTRACT.yaml`](docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml) — canonical machine-readable field semantics
- [`SEMANTIC_FIELD_CONTRACT.md`](docs/contracts/SEMANTIC_FIELD_CONTRACT.md) — human-readable projection
- [`WORKFLOW_CONTRACT.md`](docs/contracts/WORKFLOW_CONTRACT.md)
- [`ACCESS_CONTROL_CONTRACT.md`](docs/contracts/ACCESS_CONTROL_CONTRACT.md)
- [`IMPLEMENTATION_MAPPING.yaml`](docs/contracts/IMPLEMENTATION_MAPPING.yaml) — فقط بعد از scaffold با IDهای واقعی bind می‌شود
- [`ENVIRONMENT_MANIFEST.md`](docs/contracts/ENVIRONMENT_MANIFEST.md)
- [`PRIVACY_RETENTION_CONTRACT.md`](docs/contracts/PRIVACY_RETENTION_CONTRACT.md)

## Provenance

Exact pre-repository source corpus `01..11` در `history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz` نگهداری می‌شود. `evidence/provenance/SOURCE_MANIFEST.yaml` size/SHA-256 archive و هر source را ثبت می‌کند.

Pre-cutover runtime state و تمام ۷۲ رویداد قدیمی Sheet به‌صورت readable immutable files زیر `history/pre-runtime-ssot/` حفظ شده‌اند و `MIGRATION_MANIFEST.json` coverage/hash آن‌ها را ثبت می‌کند.

وجود archive یا hash صحیح = runtime proof نیست؛ provenance فقط evidence تاریخی است.

## وضعیت‌ها را قاطی نکن

`plan != implementation != validation != review != authorization != publication != production-ready != completion`

`SELECTED != IMPLEMENTED`، `DOCUMENTED != OBSERVED_IN_STAGING`، `NOT_PROVEN != PROVEN_ABSENT`.

## تغییرات مادی

هر تغییر مادی باید:

1. authority/Owner decision لازم را داشته باشد؛
2. contract/artifact مربوط را در صورت نیاز update کند؛
3. `runtime/CURRENT_STATE.yaml` را update کند؛
4. یک event جدید به `runtime/DECISION_HISTORY.jsonl` append کند؛
5. state/history در یک accepted Git commit ثبت شوند و از `main` read-back شوند؛
6. برای code/contract/documentation تغییرات branch + PR استفاده شود؛
7. integrity checks را پاس کند یا، اگر CI infrastructure واقعاً اجرا نمی‌شود، همان checkها با manual equivalent evidence انجام و صریحاً ثبت شوند.

## امنیت داده

دادهٔ واقعی دانش‌آموز، عکس/اسکن واقعی، export دارای PII، credential، database dump، payment data و operational ledger واقعی داخل Git قرار نمی‌گیرد. فقط schema، synthetic fixture و evidence غیرحساس مجاز است.

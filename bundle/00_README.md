# SRWF GPT Project Package

Version: `1.1.0`

این ZIP یک **portable consumption snapshot** از پروژهٔ SRWF برای ChatGPT Projects / محیط‌های مشابه است.

## Authority boundary

- اگر repository در دسترس است: `rezahh107/SRWF` → `main` تنها Project/Runtime SSOT است.
- `PROJECT_SOURCES/24_CURRENT_STATE.yaml` فقط snapshot زمان build است؛ هرگز state جدید را داخل ZIP persist نکن.
- اگر repo موقتاً در دسترس نبود، snapshot بسته فقط برای فهم/ادامهٔ محدود استفاده می‌شود و هر تغییر material باید `STATE_NOT_PERSISTED` تلقی شود تا repo دوباره در دسترس باشد.
- Google Sheet قدیمی `SRWF_RUNTIME_STATE` فقط provenance تاریخی و `DEPRECATED_READ_ONLY_MIGRATION_SOURCE` است.

## Start order

1. `02_PROJECT_INSTRUCTIONS.md`
2. `PROJECT_SOURCES/02_REPOSITORY_MANIFEST.yaml`
3. `PROJECT_SOURCES/03_MASTER_AUTHORITY.md`
4. اگر repo قابل دسترس است: live `runtime/CURRENT_STATE.yaml` از `main`; در غیر این صورت `PROJECT_SOURCES/24_CURRENT_STATE.yaml`
5. latest relevant events از live repo یا snapshot `25_DECISION_HISTORY.jsonl`
6. `PROJECT_SOURCES/04_EXECUTION_PLAYBOOK.md`
7. contract مرتبط
8. Product/Constructability Knowledge فقط در صورت نیاز decision-material

## Package integrity

- `01_PACKAGE_MANIFEST.json` هویت source commit، state snapshot و path/size/SHA-256 همهٔ فایل‌های payload را ثبت می‌کند.
- `CHECKSUMS.sha256` checksum payload را ثبت می‌کند.
- ZIP به‌صورت deterministic ساخته می‌شود: pathهای sorted، timestamp ثابت و permission ثابت.
- `PACKAGE_VALIDATION.json` نتیجهٔ validation زمان build را ثبت می‌کند.

## Product Knowledge

فایل‌های 04..09 از archive byte-exact pre-repository استخراج و در `PROJECT_SOURCES/KNOWLEDGE/` قرار می‌گیرند. `27_CONSTRUCTABILITY_APPLICABILITY_OVERLAY.md` باید قبل از استفاده از source 04 خوانده شود.

وجود source/hash صحیح = runtime proof نیست.

## Artifact references

اگر Runtime History یک artifact را با SHA-256 ثبت کرده ولی exact bytes آن در repository موجود نباشد، builder آن را **نمی‌سازد و حدس نمی‌زند**. در `ARTIFACT_REFERENCES.json` با وضعیت `REFERENCED_NOT_EMBEDDED` ثبت می‌شود.

## Package Maker 5 qualification

این build از profile `BUNDLE_PACKAGE_MAKER_5_COMPATIBILITY` استفاده می‌کند. spec رسمی Package Maker 5 در sourceهای قابل‌دسترسی این build retrieve نشده است؛ بنابراین این نام یک **compatibility profile based on observed project-package conventions** است، نه ادعای formal compliance اثبات‌شده.

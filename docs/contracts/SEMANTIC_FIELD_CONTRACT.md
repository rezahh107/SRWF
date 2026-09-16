# Semantic Field Contract — Human Projection

**Canonical machine-readable source:** `SEMANTIC_FIELD_CONTRACT.yaml`  
**Semantic scope:** `OWNER APPROVED / CURRENT PERSIANGRAVITY SYNC — event92`  
**Current applicability override:** `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC` suspends finance/manual-cheque implementation and validation without deleting or changing the preserved finance semantics below.  
**Runtime binding:** `UNBOUND / NOT_PROVEN` تا staging import و read-back IDهای واقعی.

این projection تصمیم‌های semantic Owner تا همگام‌سازی 2026-09-16 با PersianGravity جاری را خلاصه می‌کند. وجود field با اجباری بودن value یکی نیست. تصمیم scope مورخ 2026-09-15 semantic rows مالی را بازنویسی نمی‌کند؛ فقط تعیین می‌کند فعلاً اجرای آن‌ها در مسیر جاری لازم نیست.

`SRWF_GravityForms_Import_v0.6.1_PROVISIONAL.json` آخرین staging candidate دارای full-stack qualification پذیرفته‌شده است. `SRWF_GravityForms_Import_v0.6.2_PROVISIONAL.json` successor تحت qualification است و تا exact-head FULL_STACK PASS نباید صرفاً بر مبنای minimal current-PersianGravity PASS به staging candidate ارتقا یابد.

## فرم عمومی

- `first_name`, `last_name`, `father_name`, `national_id`, `dob_jalali`, `gender_code`, `student_mobile`, `student_photo`, `education_level`, `grade_group_selection`, `graduation_status`, `school_code` در مسیر عمومی هستند.
- `home_phone`, `contact1_mobile`, `contact2_mobile` در فرم هستند ولی optional. `contact1_relationship=پدر` و `contact2_relationship=مادر` hidden/system-owned هستند.
- `national_id`: فیلد جاری PersianGravity با type=`pgr_national_id`، کد ملی معتبر، canonical ده رقم ASCII با حفظ leading zero، duplicate مجاز.
- `dob_jalali`: فیلد جاری PersianGravity با type=`pgr_jalali_date` و `jalali_format=ymd_slash`؛ ورودی/نمایش جلالی `YYYY/MM/DD` و canonical persisted value برابر ASCII `YYYY-MM-DD` با همان semantics تقویم جلالی است؛ بدون age rule.
- موبایل‌ها: normalize ارقام فارسی/عربی، حذف space/hyphen، canonical `09xxxxxxxxx`; تلفن منزل digits-only و بدون طول ساختگی.

## عکس و کارنامه

`student_photo`: required، یک فایل `jpg/jpeg` تا 5MB، GP File Upload Pro، crop اجباری `3:4`، حداکثر `1200×1600`، بدون minimum dimensions و بدون AI/face/background checks. Crop/downscale maintained این Perk تنها supersession محدود `D-12` است؛ custom/background processing queue همچنان ممنوع است.

`report_card_file`: یک فایل `jpg/jpeg/pdf` تا 5MB. برای school codeهای `283,286,291,650,663,666,667,1320,1351` visible+required؛ برای `Other=0` visible+optional؛ برای سایر مدارس hidden. فایل نامرتبط پاک می‌شود؛ replace امن یعنی ابتدا فایل جدید persist/bind و فقط بعد فایل قبلی delete شود. Trash فایل را نگه می‌دارد؛ permanent Entry deletion فایل primary را حذف می‌کند. backup/export/log retention هنوز Privacy Gate باز دارد.

## تحصیل و مدرسه

- `education_level`: Radio با پنج مقدار `کنکوری/متوسطه دوم/متوسطه اول/دبستان/هنرستان`.
- `grade_group_selection`: یک Dropdown از 33 گروه، filtered by education level؛ `group_code` hidden/system-derived.
- `graduation_status`: `1=دانش‌آموز`, `0=فارغ‌التحصیل`; برای 11 گروه dual-status نمایش داده می‌شود و برای بقیه server-authoritative set می‌شود.
- `school_code`: یک Dropdown canonical + **GP Advanced Select الزامی**؛ GF Enhanced UI خاموش. Catalog = `946` مدرسه معتبر + `Other=0`؛ کدهای `1296,1314,1316,1319` حذف/رد می‌شوند.
- فیلتر مدرسه فقط `gender + education_level` است؛ `Other=0` exempt؛ group-specific filter نداریم. Mapping مقطع SchoolReport: دبستان→دبستان، راهنمایی→متوسطه اول، دبیرستان→متوسطه دوم و کنکوری، هنرستان→هنرستان.
- `school_name` system-owned mirror است؛ برای Other از `school_name_other` می‌آید.

## Registration Officer-only — finance semantics preserved, implementation suspended

موارد زیر semantic contract محفوظ هستند تا اگر Owner بخش مالی را دوباره باز کرد، از صفر تصمیم‌گیری نشود. در وضعیت فعلی، finance-specific exposure/editing/server logic/validation جزو implementation جاری نیست:

- `registration_center_code`: non-public Dropdown، `0=مرکز` default، `1=گلستان`, `2=صدرا`.
- `finance_status`: non-public optional Radio، `0=عادی` default، `1=بنیاد شهید`, `3=حکمت`. `registration_status_code` مستقل حذف شده است.
- Bonyad Shahid: `bonyad_shahid_case_number`, `bonyad_shahid_type_code` (18-choice)، `bonyad_shahid_type_name` mirror؛ فقط وقتی finance=1 و در خروج از آن پاک می‌شوند.
- Hekmat: `hekmat_package=آزمون` و `hekmat_tracking=1111111111111111` فقط server-side وقتی finance=3؛ در خروج از Hekmat پاک می‌شوند.
- `tuition_amount`, `discount_amount`, `discount_title` در submit اولیه خالی و optional هستند. مبلغ‌ها integer Rial. `discount_amount > tuition_amount` => error/no-save.
- `net_payable_amount`: system-owned؛ اگر tuition خالی است خالی، وگرنه `tuition - discount` با treat کردن discount خالی به صفر بدون نوشتن صفر در `discount_amount`.
- `discount_code`: optional، فقط finance=0، default `0=بدون تخفیف`، catalog دقیق 41 code/name؛ `109=سازمان زندان‌ها` موجود و `102=سپاه پاسداران` حذف. `discount_name` mirror system-owned است.

**Current applicability:** این قواعد فعلاً `PRESERVED / IMPLEMENTATION_SUSPENDED` هستند و نباید Flow whitelist، finance server bindings یا finance validation را به blocker مسیر جاری تبدیل کنند.

## Review/System

`review_status` و `review_reason` ordinary Entry fields هستند و workflow state جدیدی نمی‌سازند. `registration_counter` فقط WP All Import و exact National ID؛ importer Flow را جلو نمی‌برد.

## Cheque child form — deferred with finance scope

Host آینده انتخاب‌شده `GP Nested Forms` است و POC همچنان `NOT_PROVEN` است، اما اجرای آن `DEFERRED_WITH_FINANCE_SCOPE` است. هر cheque در صورت reopen یک child Entry خواهد بود؛ manual cheque fields optional/Officer-only می‌مانند. inventory کامل machine-keyها تا زمان reopen لازم نیست bind شود و نباید حدس زده شود. Scanner همچنان deferred و هفت Sayad field hidden/future-reserved هستند.

## Daily manager SMS — خارج از SFC field semantics

نیاز گزارش روزانه ثبت شده است: پایان هر روز کاری، تعداد پرونده‌هایی که Registration Officer واقعاً به Accountant approve/advance کرده برای مدیر SMS شود. این requirement field semantic جدیدی نمی‌سازد و workflow state را تغییر نمی‌دهد. mechanism/time/calendar/provider/mobile binding/retry هنوز `NOT_SELECTED` است و Cron/Cron-like shared-host baseline بدون re-adjudication Owner مجاز نیست.

## Gate باقی‌مانده

SFC semantics فرم اصلی با PersianGravity جاری همگام است، اما `DOCUMENTED != OBSERVED_IN_STAGING`: v0.6.2 full-stack qualification، Import واقعی staging، ID mapping، server bindings فعالِ غیرمالی، school filtering، `V-01/V-03` و سایر validationهای active scope هنوز `NOT_PROVEN` هستند. Finance/manual-cheque bindings و Nested Forms POC فعلاً deferred هستند و blocker جاری نیستند. تا Privacy/Retention sign-off فقط synthetic data.

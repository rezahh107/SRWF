# Semantic Field Contract — Human Projection

**Canonical machine-readable source:** `SEMANTIC_FIELD_CONTRACT.yaml`  
**Semantic scope:** `OWNER APPROVED / CLOSED THROUGH event86`  
**Runtime binding:** `UNBOUND / NOT_PROVEN` تا staging import و read-back IDهای واقعی.

این projection تصمیم‌های Owner تا `OWNER-20260908-SFC-BATCH-MAIN-FORM-CONSTRUCTION-READY` را خلاصه می‌کند. وجود field با اجباری بودن value یکی نیست.

## فرم عمومی

- `first_name`, `last_name`, `father_name`, `national_id`, `dob_jalali`, `gender_code`, `student_mobile`, `student_photo`, `education_level`, `grade_group_selection`, `graduation_status`, `school_code` در مسیر عمومی هستند.
- `home_phone`, `contact1_mobile`, `contact2_mobile` در فرم هستند ولی optional. `contact1_relationship=پدر` و `contact2_relationship=مادر` hidden/system-owned هستند.
- `national_id`: PersianGravity، کد ملی معتبر، ۱۰ رقم ASCII downstream، leading zero حفظ، duplicate مجاز.
- `dob_jalali`: PersianGravity Jalali، canonical `YYYY/MM/DD`، بدون age rule.
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

## Registration Officer-only

- `registration_center_code`: non-public Dropdown، `0=مرکز` default، `1=گلستان`, `2=صدرا`.
- `finance_status`: non-public optional Radio، `0=عادی` default، `1=بنیاد شهید`, `3=حکمت`. `registration_status_code` مستقل حذف شده است.
- Bonyad Shahid: `bonyad_shahid_case_number`, `bonyad_shahid_type_code` (18-choice)، `bonyad_shahid_type_name` mirror؛ فقط وقتی finance=1 و در خروج از آن پاک می‌شوند.
- Hekmat: `hekmat_package=آزمون` و `hekmat_tracking=1111111111111111` فقط server-side وقتی finance=3؛ در خروج از Hekmat پاک می‌شوند.
- `tuition_amount`, `discount_amount`, `discount_title` در submit اولیه خالی و optional هستند. مبلغ‌ها integer Rial. `discount_amount > tuition_amount` => error/no-save.
- `net_payable_amount`: system-owned؛ اگر tuition خالی است خالی، وگرنه `tuition - discount` با treat کردن discount خالی به صفر بدون نوشتن صفر در `discount_amount`.
- `discount_code`: optional، فقط finance=0، default `0=بدون تخفیف`، catalog دقیق 41 code/name؛ `109=سازمان زندان‌ها` موجود و `102=سپاه پاسداران` حذف. `discount_name` mirror system-owned است.

## Review/System

`review_status` و `review_reason` ordinary Entry fields هستند و workflow state جدید نمی‌سازند. `registration_counter` فقط WP All Import و exact National ID؛ importer Flow را جلو نمی‌برد.

## Cheque child form

Host انتخاب‌شده `GP Nested Forms` و `POC_NOT_PROVEN` است؛ هر cheque یک child Entry. manual cheque fields optional/Officer-only. inventory کامل machine-keyها هنوز `INCOMPLETE_ENUMERATION` است و قبل از child-form freeze باید bind شود. Scanner current release deferred و هفت Sayad field hidden/future-reserved هستند.

## Gate باقی‌مانده

SFC semantics فرم اصلی بسته است، اما `DOCUMENTED != OBSERVED_IN_STAGING`: Import واقعی، ID mapping، server bindings، Flow whitelist، `V-01/V-03` و سایر validationها هنوز `NOT_PROVEN` هستند. تا Privacy/Retention sign-off فقط synthetic data.

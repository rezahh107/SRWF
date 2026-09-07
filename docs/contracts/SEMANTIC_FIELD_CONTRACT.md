# Semantic Field Contract — Human Projection

**Canonical machine-readable source:** `SEMANTIC_FIELD_CONTRACT.yaml`  
**Gate:** `OWNER APPROVED / CLOSED` برای semantics؛ `UNBOUND` برای GF/Flow IDs تا بعد از scaffold.

## قاعده‌ای که نباید دوباره شکسته شود

`وجود فیلد در فرم` با `اجباری بودن مقدار` دو چیز جداست:

- `include_in_form: true` یعنی field باید در scaffold وجود داشته باشد.
- `value_required: true/false/conditional` یعنی آیا actor باید مقدار بدهد.

نمونهٔ قطعی: **تلفن منزل** باید در فرم باشد اما مقدار آن اختیاری است.

## Public student fields

| Contract | Machine purpose | در فرم | مقدار اجباری | نکته |
|---|---|---:|---:|---|
| `STUDENT_FIRST_NAME` | `first_name` | بله | بله | Owner-approved |
| `STUDENT_LAST_NAME` | `last_name` | بله | بله | Owner-approved |
| `STUDENT_FATHER_NAME` | `father_name` | بله | بله | Owner-approved؛ نباید دوباره از لیست حذف شود |
| `STUDENT_NATIONAL_ID` | `national_id` | بله | بله | ASCII 10 digits + Iranian checksum؛ duplicate blocking ممنوع |
| `STUDENT_MOBILE` | `student_mobile` | بله | بله | موبایل دانش‌آموز |
| `HOME_PHONE` | `home_phone` | **بله** | **خیر** | Owner clarification 2026-09-07 |
| `CONTACT1_MOBILE` | `contact1_mobile` | بله | خیر | رابط ۱ = پدر، ثابت/hidden |
| `CONTACT2_MOBILE` | `contact2_mobile` | بله | خیر | رابط ۲ = مادر، ثابت/hidden |
| `STUDENT_GENDER` | `gender_code` | بله | بله | دختر=0، پسر=1 |
| `EDUCATION_LEVEL` | `education_level` | بله | بله | controlled choice |
| `GRADE_GROUP_SELECTION` | `grade_group_selection` | بله | بله | label انسانی؛ `group_code` پشت‌صحنه |
| `GROUP_CODE` | `group_code` | بله/hidden | بله | raw code مستقیم editable نیست |
| `GRADUATION_STATUS` | `graduation_status` | بله | بله | بعضی گروه‌ها auto، بعضی visible choice |
| `REGISTRATION_CENTER` | `registration_center_code` | بله | بله | choice catalog از Crosswalk/source |
| `REGISTRATION_STATUS` | `registration_status_code` | بله | بله | exact current code catalog باید از accepted source materialize شود |
| `DATE_OF_BIRTH_JALALI` | `dob_jalali` | بله | بله | canonical `YYYY/MM/DD` Jalali؛ no age/grade-age rule |
| `STUDENT_PHOTO` | `student_photo` | بله | بله | native File Upload؛ no custom image processing |

## School fields

- `school_code`: Value canonical؛ `0=Other`؛ raw code برای Officer editable نیست.
- `school_name`: label انسانی؛ Officer انتخاب/نام را اصلاح می‌کند و سیستم code canonical را update می‌کند.
- `school_name_other`: وقتی `school_code=0`، اجباری.
- `report_card_file`: به‌طور پیش‌فرض اختیاری؛ فقط برای کدهای `283, 286, 291, 650, 663, 666, 667, 1320, 1351` اجباری.

## Compatibility hidden fields

- `hekmat_package = آزمون` در حالت حکمت.
- `hekmat_tracking = 1111111111111111` در حالت حکمت.

این‌ها user input نیستند و برای compatibility فعلی hidden هستند.

## Review/System

- `review_status`: field معمولی Entry؛ نه workflow state دوم.
- `review_reason`: دلیل Needs Review.
- `registration_counter`: در public submit تولید نمی‌شود؛ فقط از external source با WP All Import sync می‌شود.

## Finance — Registration Officer only

همهٔ این fieldها current-release **optional + non-public** هستند:

- `tuition_amount` — ریال
- `discount_amount` — ریال، default 0 مجاز
- `discount_title`
- `net_payable_amount = tuition_amount - discount_amount`

اگر `discount_amount > tuition_amount` باشد، validation error و **no save**.

## Cheque Child Form

- cardinality: `1..N`
- selected host: `GP Nested Forms` — `POC_NOT_PROVEN`
- هر چک = child Gravity Forms Entry
- parallel relationship DB/state ممنوع
- همهٔ manual cheque fields current-release optional و Officer-only هستند.

فیلدهای دستی که evidence جاری صریحاً پشتیبانی می‌کند:

- `cheque_amount`
- `cheque_due_date`

**Gap آشکار:** current active Master نام machine-key همهٔ manual cheque fields را کامل enumerate نکرده است. تا source/Owner binding، key جدید اختراع نمی‌شود.

## Future Sayad — Hidden

این هفت field باید در Cheque Form future-reserved/Hidden باقی بمانند و current-release Scanner آن‌ها را populate نمی‌کند:

`qr_version`, `owner_type`, `owner_identifier`, `iban`, `bank_branch`, `cheque_serial`, `sayad_id`.

## Legacy fields

وجود یک ستون در GF export/report قدیمی به‌تنهایی requirement جدید نیست. `contact1_name`, `contact2_name`, mentor/alias helpers و legacy output-shaping fields بدون current binding به scaffold برنمی‌گردند.

## Materialization gaps

1. **Choice catalog:** exact current education/group/center/registration-status mapping باید از accepted Crosswalk/source داخل repo materialize شود.
2. **Manual cheque inventory:** exact manual cheque field list هنوز کامل enumerate نشده.
3. **Privacy/retention:** policy فایل‌ها/مالی/چک قبل از real PII بسته شود.

این gapها باید visible بمانند؛ `NOT_FOUND/INCOMPLETE` را به `PROVEN_ABSENT` تبدیل نکن.

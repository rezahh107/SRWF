# Implementation Mapping

**Status:** `UNBOUND`  
**Gate:** بعد از authoritative scaffold.

این فایل mapping انسانی است؛ منبع machine-readable برابر `IMPLEMENTATION_MAPPING.yaml` است.

## چیزی که الان عمداً خالی است

- Registration Form ID
- Cheque Child Form ID
- هر GF Field/Input ID
- Registration Officer Approval Step ID
- Accountant Approval Step ID
- final external-pending Step ID
- page/route/View IDs
- exact plugin/version manifest target

خالی بودن این موارد defect نیست؛ قبل از scaffold ID واقعی وجود ندارد. label یا ID فرضی authority نمی‌گیرد.

## Binding procedure

1. scaffold واقعی در target/staging ساخته شود، synthetic data only.
2. Form/Field/Input/Step IDs از runtime واقعی خوانده شوند.
3. هر ID به `contract_id` متناظر در Semantic Field Contract bind شود.
4. mapping read-back شود.
5. mapping freeze شود و commit SHA ثبت گردد.
6. تغییر ID بعدی regression scope ایجاد می‌کند.

## ممنوع

- bind با label ترجمه‌پذیر
- reuse اجباری IDهای legacy form
- invent کردن ID برای جلو بردن implementation
- feature code/config freeze قبل از mapping واقعی

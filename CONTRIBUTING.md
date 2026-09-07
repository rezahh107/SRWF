# Contributing to SRWF Documentation

## Scope

این repo در حال حاضر documentation/contract/evidence repository پروژه SRWF است. تغییرات باید Native-First architecture و Owner locks را حفظ کنند.

## Change classes

### Mechanical
Typo، link/path، formatting یا metadata بدون تغییر semantics. باید `CHANGELOG.md` را فقط در صورت material بودن به‌روزرسانی کند.

### Semantic
هر تغییر در field meaning/requiredness/value/visibility/editability/workflow/access/privacy/POC criterion یا architecture. نیازمند:

- Owner/authority basis؛
- update contract مربوط؛
- update `docs/governance/DECISION_LEDGER.md`؛
- validation impact؛
- `CHANGELOG.md`؛
- در صورت اثر حاکمیتی، update Master/Playbook.

### Runtime evidence
نتیجهٔ probe/test واقعی. نباید به‌عنوان plan/documentation ثبت شود؛ PASS/FAIL و environment/evidence باید صریح باشد و live Runtime State نیز طبق governance update/read-back شود.

## Pull request requirements

- یک PR باید یک واحد تغییر قابل‌فهم داشته باشد.
- semantic changes بدون decision reference پذیرفته نیستند.
- generated/non-canonical snapshots باید source timestamp/ref داشته باشند.
- هیچ PII/secret/real operational export مجاز نیست.
- `scripts/validate_docs.py` باید پاس شود.

## Active filenames

active pathها stable هستند. برای نسخهٔ جدید `MASTER_vX.md` یا `PLAYBOOK_vY.md` نساز. version/history از metadata و Git نگهداری می‌شود. نسخه‌های pre-repository فقط زیر `history/` نگهداری می‌شوند.

# Pre-Repository SRWF Source Archive

این پوشه sourceهای exact پیش از migration به GitHub را برای provenance حفظ می‌کند.

## Archive

فایل canonical provenance archive:

`SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz`

ویژگی‌های مورد انتظار:

- size: `353740` bytes
- SHA-256: `82b0201ce3920214fe2ac7b9bd7defaa8769651fbbd1168abcd0a1ba91d32ed4`
- contents: exact source files `01..11`

برای materialization:

```bash
python scripts/materialize_archives.py
```

برای integrity check:

```bash
python scripts/validate_docs.py
```

Validator علاوه بر SHA کل archive، نام، size و SHA-256 هر ۱۱ source داخل tar را جداگانه بررسی می‌کند.

## Contents

1. Master Authority v1.9.0
2. Owner Knowledge & Composition Addendum v1.1.1
3. Execution Playbook v1.3.0
4. Constructability Runtime Knowledge snapshot
5. Product Knowledge Normalized
6. Gravity Forms deep Product Knowledge
7. Gravity Flow deep Product Knowledge
8. GravityView deep Product Knowledge
9. Gravity Perks deep Product Knowledge
10. Owner Comprehension Protocol v1.0.1
11. Constructability Applicability Overlay v1.0.1

## Authority warning

وجود source تاریخی، projectionهای project-state قدیمی را current نمی‌کند. مسیرهای active زیر `docs/` به‌همراه Owner Decisionهای جاری مرجع interpretation هستند. به‌طور خاص source `04` باید از طریق `knowledge/constructability/APPLICABILITY_OVERLAY.md` تفسیر شود.

این archive فقط provenance/reference است؛ presence یا hash integrity آن runtime proof نیست.

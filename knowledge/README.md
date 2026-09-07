# SRWF Knowledge Corpus

این بخش Product Knowledge و Constructability evidence را نگه می‌دارد. **این فایل‌ها architecture authority یا runtime proof نیستند.**

## Retrieval order

1. current Master/Playbook/Addendum
2. `constructability/APPLICABILITY_OVERLAY.md`
3. source 05 normalized knowledge از archive provenance
4. source 04 constructability snapshot از archive provenance
5. source 06..09 deep product files در صورت نیاز
6. fresh official vendor docs وقتی evidence local ناقص/کهنه/version-sensitive است

## Archived exact sources

به‌جای کپی‌های متعدد و drift-prone، فایل‌های exact pre-repository `04..09` همراه با sourceهای `01..11` در یک archive byte-exact زیر `history/pre-repository/` نگه‌داری می‌شوند. SHA-256 هر source در `evidence/provenance/SOURCE_MANIFEST.yaml` است.

برای materialize کردن sourceها:

```bash
python scripts/materialize_archives.py
```

خروجی local در `.knowledge-materialized/` قرار می‌گیرد و در Git commit نمی‌شود.

## Interpretation

- `depth=DEEP` = semantic density؛ نه full ingestion/decision readiness/runtime proof.
- `DOCUMENTED`/`SOURCE_INSPECTED` = source evidence؛ نه `OBSERVED_IN_STAGING`.
- absence در snapshot = `NOT_FOUND_IN_THIS_SOURCE`, نه `PROVEN_ABSENT`.
- Product Knowledge نمی‌تواند Owner Lock را silently override کند.

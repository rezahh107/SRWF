# Pre-Repository SRWF Source Archive

این پوشه sourceهای exact پیش از migration به GitHub را برای provenance حفظ می‌کند.

## Archive

`srwf_pre_repository_sources.tar.xz.b64.part00..part52`

- تعداد partها: `53`
- هر part به‌جز آخر: حداکثر `9000` بایت Base64
- SHA-256 archive decoded: `82b0201ce3920214fe2ac7b9bd7defaa8769651fbbd1168abcd0a1ba91d32ed4`

روش materialization:

```bash
python scripts/materialize_archives.py
```

Script تمام partها را concatenate می‌کند، Base64 decode می‌کند، SHA-256 archive را با `evidence/provenance/SOURCE_MANIFEST.yaml` مقایسه می‌کند، سپس tar.xz را در `.knowledge-materialized/pre-repository/` extract می‌کند.

## Contents

Exact source files 01..11:

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

Historical source presence does not make every old project-state projection current. Stable active docs under `docs/` plus current Owner decisions govern current project semantics. In particular, source `04` must be interpreted through `knowledge/constructability/APPLICABILITY_OVERLAY.md`.

## Why encoded split parts?

Connector transport for large single text payloads is bounded. Split parts preserve the complete compressed corpus byte-exact while allowing every part to be committed and independently visible. Parts are transport/storage artifacts only; they have no semantic authority by themselves.

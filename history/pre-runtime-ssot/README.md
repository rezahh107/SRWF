# Pre-cutover Runtime State Archive

This directory preserves the exact Google Sheets runtime-state workbook used before GitHub became the single SRWF project/runtime SSOT.

- Source: `SRWF_RUNTIME_STATE`
- Archived file: `SRWF_RUNTIME_STATE_PRE_CUTOVER.xlsx`
- Archived size: `57603` bytes
- SHA-256: `a8cc87682ab8a1ac884f1589bcef9aac4bc9e327f60237c444478facb6dfb594`
- Pre-cutover Decision History events: `72`
- Searchable compact index: `DECISION_HISTORY_INDEX.json`
- Cutover decision: `OWNER-20260907-REPOSITORY-RUNTIME-SSOT`

## Authority

This archive is **historical provenance only** after cutover.

Current execution state:
`runtime/CURRENT_STATE.yaml`

Repository-native append-only history starts at event `73`:
`runtime/DECISION_HISTORY.jsonl`

The compact index intentionally contains only sequence/date/ID/status. Exact pre-cutover row content remains in the archived workbook and durable accepted decisions remain in `docs/governance/DECISION_LEDGER.md`.

Do not update this archive after cutover. Do not treat it as a parallel SSOT.

# Pre-cutover Runtime State Archive

This directory preserves the complete Google Sheets runtime state used before GitHub became the single SRWF project/runtime SSOT.

## What is preserved

- `CURRENT_STATE_PRE_CUTOVER.yaml` — normalized exact pre-cutover Current State values/notes.
- Nine immutable Decision History chunks covering event sequence `1..72` with no gaps.
- `DECISION_HISTORY_INDEX.json` — compact lookup by event sequence / ID / status.
- `MIGRATION_MANIFEST.json` — source identity, coverage, file sizes and SHA-256 hashes.

The nine history chunks are:

- `DECISION_HISTORY_000001_000008.jsonl`
- `DECISION_HISTORY_000009_000016.jsonl`
- `DECISION_HISTORY_000017_000024.jsonl`
- `DECISION_HISTORY_000025_000032.jsonl`
- `DECISION_HISTORY_000033_000040.jsonl`
- `DECISION_HISTORY_000041_000048.jsonl`
- `DECISION_HISTORY_000049_000056.jsonl`
- `DECISION_HISTORY_000057_000064.jsonl`
- `DECISION_HISTORY_000065_000072.jsonl`

## Authority after cutover

These files are historical provenance only. Do not update them after cutover and do not treat them as a parallel state store.

Current execution state: `runtime/CURRENT_STATE.yaml`

Repository-native append-only history starts at event `73`: `runtime/DECISION_HISTORY.jsonl`

Cutover decision: `OWNER-20260907-REPOSITORY-RUNTIME-SSOT`.

# Runtime State — GitHub SSOT

## Simple rule

`main` in `rezahh107/SRWF` is the single project/runtime SSOT.

- Current execution position: `runtime/CURRENT_STATE.yaml`
- Append-only repository-era material history: `runtime/DECISION_HISTORY.jsonl`
- Durable business/governance decisions: `docs/governance/DECISION_LEDGER.md`
- Complete pre-cutover history: `history/pre-runtime-ssot/`

The Google Sheet `SRWF_RUNTIME_STATE` is a **DEPRECATED_READ_ONLY_MIGRATION_SOURCE** after cutover. Never update both stores.

Pre-cutover Sheet data is preserved as readable immutable text:

- `history/pre-runtime-ssot/CURRENT_STATE_PRE_CUTOVER.yaml`
- `history/pre-runtime-ssot/DECISION_HISTORY_000001_000008.jsonl` through `DECISION_HISTORY_000065_000072.jsonl`
- `history/pre-runtime-ssot/DECISION_HISTORY_INDEX.json`
- `history/pre-runtime-ssot/MIGRATION_MANIFEST.json`

## Session boot

For any progress-dependent task or `ادامه`:

1. read `repository.manifest.yaml`
2. read `docs/authority/MASTER.md`
3. read `runtime/CURRENT_STATE.yaml`
4. read the last relevant events from `runtime/DECISION_HISTORY.jsonl`
5. read `docs/operations/EXECUTION_PLAYBOOK.md`
6. read only the contract/evidence needed for the current unit

Do not rely on chat memory when the repository is available.

If older context is needed, use `history/pre-runtime-ssot/DECISION_HISTORY_INDEX.json` to locate the immutable pre-cutover chunk and read only that chunk.

## Material state write protocol

A material change includes an executed probe/result, Owner decision, Gate PASS/FAIL, stage transition, confirmed environment/version/license fact, accepted artifact change, or material blocker open/close.

For each material change:

1. read the current `main` blob SHA for `runtime/CURRENT_STATE.yaml` and `runtime/DECISION_HISTORY.jsonl`
2. perform the real action and collect evidence
3. increment `state_version`
4. append exactly one new JSONL event with the next contiguous `event_seq`
5. update `history.last_event_seq` and `history.last_event_id` in `CURRENT_STATE.yaml`
6. commit both state files in the **same accepted Git commit**
7. read them back from `main`
8. only then claim persistence

Runtime-only state/history changes may be committed directly to `main` when repository policy permits. Code, contract, architecture, or durable documentation changes use branch + PR; after merge/read-back, record the resulting runtime event.

If concurrent state changed since the initial read, stop and re-read. Never force-overwrite newer runtime state.

## Integrity

- `runtime/DECISION_HISTORY.jsonl` is append-only after cutover.
- `event_seq` is contiguous and strictly increasing.
- `CURRENT_STATE.history.last_event_seq` must equal the final active JSONL event.
- `CURRENT_STATE.history.last_event_id` must equal the final active JSONL `decision_id`.
- `state_version` increases on every accepted material runtime-state commit.
- Pre-cutover events `1..72` are immutable and covered by `MIGRATION_MANIFEST.json`.
- `plan != implementation != validation`.
- `NOT_PROVEN != PROVEN_ABSENT`.

## Data safety

Never put real student PII, real uploaded documents/images, credentials, payment data, or operational intake records in these runtime files.

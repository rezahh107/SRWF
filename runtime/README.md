# Runtime State — GitHub SSOT

## Simple rule

`main` in `rezahh107/SRWF` is the single project/runtime SSOT.

- Current execution position: `runtime/CURRENT_STATE.yaml`
- Append-only material history: `runtime/DECISION_HISTORY.jsonl`
- Durable business/governance decisions: `docs/governance/DECISION_LEDGER.md`
- Historical pre-cutover Google Sheet: `history/pre-runtime-ssot/SRWF_RUNTIME_STATE_PRE_CUTOVER.xlsx`

The Google Sheet is a **DEPRECATED_READ_ONLY_MIGRATION_SOURCE** after cutover. Never update both stores.

## Session boot

For any progress-dependent task or `ادامه`:

1. read `repository.manifest.yaml`
2. read `docs/authority/MASTER.md`
3. read `runtime/CURRENT_STATE.yaml`
4. read the last relevant events from `runtime/DECISION_HISTORY.jsonl`
5. read `docs/operations/EXECUTION_PLAYBOOK.md`
6. read only the contract/evidence needed for the current unit

Do not rely on chat memory when the repository is available.

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

Runtime-only state/history commits may go directly to `main` when repository policy permits. Code, contract, architecture, or documentation changes use branch + PR; after merge/read-back, record the resulting runtime event.

If concurrent state changed since the initial read, stop and re-read. Never force-overwrite newer runtime state.

## Integrity

- `DECISION_HISTORY.jsonl` is append-only.
- `event_seq` is contiguous and strictly increasing.
- `CURRENT_STATE.history.last_event_seq` must equal the final JSONL event.
- `CURRENT_STATE.history.last_event_id` must equal the final JSONL `decision_id`.
- `state_version` increases on every accepted material runtime-state commit.
- `plan != implementation != validation`.
- `NOT_PROVEN != PROVEN_ABSENT`.

## Data safety

Never put real student PII, real uploaded documents/images, credentials, payment data, or operational intake records in these runtime files.

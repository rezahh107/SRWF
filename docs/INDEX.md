# SRWF Documentation Index

## Start here

1. `../repository.manifest.yaml` — machine-readable repository map and SSOT boundary
2. `../AGENTS.md` — mandatory agent/LLM entrypoint
3. `authority/MASTER.md` — current architecture/semantic/Lock authority
4. `../runtime/CURRENT_STATE.yaml` — current execution state
5. recent relevant events in `../runtime/DECISION_HISTORY.jsonl`
6. `operations/EXECUTION_PLAYBOOK.md` — current stage/gate execution map
7. relevant file under `contracts/`

## Durable authority and governance

- `authority/MASTER.md`
- `operations/EXECUTION_PLAYBOOK.md`
- `governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md`
- `governance/OWNER_COMPREHENSION_PROTOCOL.md`
- `governance/DECISION_LEDGER.md`
- `governance/RISK_REGISTER.md`
- `governance/MINIMALITY_CHALLENGE.md`
- `governance/REMAINING_OWNER_BINDINGS.md`

## Runtime state

- `../runtime/CURRENT_STATE.yaml` — **live operational-state SSOT on `main`**
- `../runtime/DECISION_HISTORY.jsonl` — append-only repository-era material event history
- `../runtime/README.md` — session boot and write/read-back protocol
- `../runtime/schemas/` — runtime state/event schemas
- `../history/pre-runtime-ssot/` — immutable complete pre-cutover Google Sheet history

Google Sheet `SRWF_RUNTIME_STATE` is `DEPRECATED_READ_ONLY_MIGRATION_SOURCE` after cutover and is not a parallel state store.

## Executable contracts

- `contracts/SEMANTIC_FIELD_CONTRACT.yaml` — machine-readable field semantics
- `contracts/SEMANTIC_FIELD_CONTRACT.md` — human-readable projection
- `contracts/WORKFLOW_CONTRACT.md`
- `contracts/ACCESS_CONTROL_CONTRACT.md`
- `contracts/IMPLEMENTATION_MAPPING.yaml` / `.md`
- `contracts/ENVIRONMENT_MANIFEST.md`
- `contracts/PRIVACY_RETENTION_CONTRACT.md`

## Validation and release

- `validation/TEST_MATRIX.md`
- `validation/DEFINITION_OF_DONE.md`
- `validation/POC_REGISTER.md`
- `release/RELEASE_MANIFEST.md`
- `release/ROLLBACK_RUNBOOK.md`

## Knowledge and provenance

- `../knowledge/README.md` — retrieval/classification rules
- `../knowledge/constructability/APPLICABILITY_OVERLAY.md`
- `../evidence/provenance/SOURCE_MANIFEST.yaml`
- `../history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz` — byte-exact source corpus `01..11`
- `../history/pre-runtime-ssot/MIGRATION_MANIFEST.json` — pre-cutover runtime history coverage/hash manifest

Materialize archived pre-repository sources locally with:

```bash
python scripts/materialize_archives.py
```

## Acceptance rule

Feature branch/file presence is not Accepted Current. Repository changes become current only after merge to `main` plus read-back. Runtime-only state/history changes must update both canonical runtime files in one accepted commit and then be read back from `main`.

Documentation integrity evidence must distinguish a validator execution from a CI infrastructure failure before runner allocation.

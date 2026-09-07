# SRWF Documentation Index

## Start here

1. `../repository.manifest.yaml` — machine-readable repository map and acceptance boundary
2. `../AGENTS.md` — mandatory agent/LLM entrypoint
3. `authority/MASTER.md` — current architecture/semantic/Lock authority
4. `operations/EXECUTION_PLAYBOOK.md` — current stage/gate execution map
5. relevant file under `contracts/`

## Durable authority and governance

- `authority/MASTER.md`
- `operations/EXECUTION_PLAYBOOK.md`
- `governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md`
- `governance/OWNER_COMPREHENSION_PROTOCOL.md`
- `governance/DECISION_LEDGER.md`
- `governance/RISK_REGISTER.md`
- `governance/MINIMALITY_CHALLENGE.md`
- `governance/REMAINING_OWNER_BINDINGS.md`

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

Materialize archived sources locally with:

```bash
python scripts/materialize_archives.py
```

## Runtime boundary

`../runtime/README.md` defines the boundary: Google Sheet `SRWF_RUNTIME_STATE` remains the live operational-state SSOT. Repository runtime snapshots are `NON_CANONICAL`.

## Acceptance rule

Feature branch/file presence is not Accepted Current. Repository baseline becomes current only after merge to `main` plus read-back. Documentation integrity evidence must distinguish a validator execution from a CI infrastructure failure before runner allocation.

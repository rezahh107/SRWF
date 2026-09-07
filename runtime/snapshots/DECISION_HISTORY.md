# Runtime Decision History Mirror

Status: `NON_CANONICAL / GENERATED_MIRROR_PENDING`

The live operational decision history remains the `DECISION_HISTORY` tab of the external `SRWF_RUNTIME_STATE` Google Sheet.

This repository file is intentionally not populated with a hand-copied ledger because that would create a second operational SSOT and would drift. Durable accepted decisions that govern repository semantics are recorded in `docs/governance/DECISION_LEDGER.md`.

When an automated snapshot/export path is introduced, this file may be replaced by a generated snapshot that records its source timestamp and source identity. Until then, consult the live sheet for operational progression.

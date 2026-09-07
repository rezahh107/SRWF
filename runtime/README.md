# Runtime State Boundary

## Live SSOT

Google Sheet `SRWF_RUNTIME_STATE` is the live operational-state SSOT.

- `CURRENT_STATE`: current stage/gate/decision/candidate/last result/blocker/next action.
- `DECISION_HISTORY`: material probe/decision history.

## Repository role

Git repository is the canonical home for durable documentation/contracts after accepted baseline merge. It does **not** replace the live Sheet for progress/current runtime status.

Any file under `runtime/snapshots/` is:

- `NON_CANONICAL`
- timestamped
- a read-only projection for review/provenance
- stale as soon as the external Sheet changes

An agent must read live `CURRENT_STATE` before answering `ادامه` or making progress-dependent recommendations when the connector is available.

## No parallel state

Do not build a second operational state machine in GitHub issues/YAML/DB. A durable Owner decision may be reflected in `docs/governance/DECISION_LEDGER.md`, but current execution progress remains in the Sheet.

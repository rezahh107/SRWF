---
document_id: SRWF-CONSTRUCTABILITY-APPLICABILITY-OVERLAY
title: "SRWF Constructability Snapshot Applicability Overlay"
version: 1.0.2
status: CURRENT_APPLICABILITY_OVERLAY
language: en/fa
applies_to: history/pre-repository source 04 + repository constructability archive
current_authority: docs/authority/MASTER.md + docs/operations/EXECUTION_PLAYBOOK.md + docs/governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md
---

# SRWF Constructability Snapshot Applicability Overlay v1.0.2

## 1. Purpose

`04_SRWF_CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt` is retained as a derived technical/evidence snapshot. It contains valuable capability, composition, lifecycle, limitation and source records, but some **project-level authority projections and Gate states** were generated against older SRWF authority.

This overlay defines how those stale project-level records must be interpreted under the current authority. It does **not** rewrite the historical snapshot, alter product evidence, or claim new runtime proof.

## 2. Authority boundary

Current authority order for affected SRWF project semantics is:

1. `docs/authority/MASTER.md`
2. `docs/operations/EXECUTION_PLAYBOOK.md`
3. `docs/governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md`
4. this applicability overlay for interpretation of `04`
5. the original `04` records as derived evidence/snapshot data

If a record in `04` conflicts with current Master/Playbook/Addendum on a project Gate, Lock, selected component, decision state or execution ordering, the record is **historical/non-current for that project-state dimension**. Its underlying product/evidence content remains usable when otherwise applicable.

## 3. Explicit supersessions

| Record / pattern in `04` | Current applicability |
|---|---|
| `BLK-KNOW-001` / `PRE_STAGE0_CORE_PRODUCT_KNOWLEDGE_COMPLETENESS` | `SUPERSEDED_AS_GLOBAL_GATE`; knowledge incompleteness remains an evidence limitation but does not block Stage 0 globally. |
| `BLK-REVAL-001` / `PRE_STAGE0_LOCKED_DECISION_FULL_KNOWLEDGE_REVALIDATION` | `SUPERSEDED_AS_GLOBAL_GATE`; D-01..D-17 are not automatically reopened/revalidated because knowledge is incomplete or later becomes more complete. |
| `PENDING_KNOWLEDGE_COMPLETION` in `project/locked_decision_revalidation_register.json` | `HISTORICAL_SNAPSHOT_STATE`; not the current decision state. Current Master/Decision Ledger governs. |
| `AUTH-OWNER-KNOWLEDGE-COVERAGE` stating full coverage is required before Stage 0 | `SUPERSEDED` by current Addendum/Master/Playbook. |
| `AUTH-OWNER-DECISION-REVALIDATION` requiring automatic full-knowledge revalidation of D-01..D-17 | `SUPERSEDED` by current Addendum/Lock rules. |
| Any project projection declaring an older SRWF-MASTER as current authority | `HISTORICAL_PROVENANCE_ONLY`; use `docs/authority/MASTER.md` for current semantics. |
| D-17 projection saying renderer is simply `DEFERRED` / no candidate selected | `SUPERSEDED`; current state is `POC_GATED / NOT_PROVEN`, first candidate `Gravity PDF Free` + SRWF-owned print layer. |
| Older project projections that imply GravityView operational Desk/edit ownership | `SUPERSEDED`; current Officer operational surface is native Gravity Flow Inbox + Entry Details, with GravityView optional presentation only. |
| Any projection that treats finance/manual-cheque implementation, finance-specific validation, or `PRB-NESTED-CHEQUE-001` as a current progression/release gate | `SUPERSEDED_IN_APPLICABILITY` by `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC`; finance semantics/capability evidence remain preserved, but implementation/validation is suspended and Nested POC is `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN` until explicit Owner reopen. |
| Any projection that treats a particular daily manager SMS scheduler/provider as selected | `NOT_CURRENT / NOT_SELECTED`; the SMS requirement is recorded, but mechanism/time/calendar/provider/mobile binding/retry behavior remain open. Cron/Cron-like shared-host scheduling is not an accepted baseline without Owner re-adjudication. |

## 4. What remains usable from `04`

Unless contradicted by fresher evidence/version scope, continue to use `04` for product capability/configuration facts, cross-product composition surfaces, mutation/lifecycle behavior, limitations/security/failure modes, evidence tiers/source references, still-relevant runtime unknowns/probe rationales, and historical provenance.

A record marked `DOCUMENTED`, `SOURCE_INSPECTED` or similar remains documentation/source evidence only; it does not become `OBSERVED_IN_STAGING`.

Finance-related product/capability evidence in `04` remains usable for future re-adjudication even while current finance implementation is suspended. Suspension changes project applicability, not the truth/provenance of product evidence.

## 5. Current project additions absent from the old snapshot

Absence from `04` does not mean absence from current SRWF. Current authority/runtime state additionally includes:

- preserved finance semantics with Rial canonical/display, optional/non-public/Registration-Officer-only reserved fields and invalid-discount no-save semantics, while current finance/manual-cheque implementation/validation is `SUSPENDED` until explicit Owner reopen;
- POS/PC-POS and online Sayad inquiry deferred;
- multi-cheque cardinality `1..N` with `GP Nested Forms` selected as the future host, but its POC is `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN` and not a current gate;
- generic non-persistent `PersianGravity Structured Scanner` retained while SRWF scanner population is deferred and seven Sayad outputs remain Hidden/future-reserved;
- Sayad v01 seven-output atomic contract;
- D-17 `Gravity PDF Free` first POC candidate;
- future daily manager SMS requirement: end-of-working-day count of Officer approvals/advances to Accountant, derived read-only from canonical GF/Flow evidence, with implementation `NOT_SELECTED` and no Cron/Cron-like shared-host baseline without Owner re-adjudication.

## 6. Retrieval rule

When a decision uses `04`:

1. retrieve current Master/Playbook/Addendum;
2. apply this overlay to project-level statuses/projections;
3. materialize/retrieve the relevant `04` technical records from repository provenance/archive;
4. check normalized knowledge, then deep product sources as needed;
5. use fresh official vendor documentation when local evidence is stale, partial, version-sensitive or insufficient;
6. keep runtime claims bounded to executed evidence.

## 7. No mutation of historical evidence

Do not edit old `04` rows to make them look as though they were generated under current authority. That would destroy provenance. Current interpretation belongs in this overlay and current authority/runtime state.

## Changelog
### v1.0.2 — 2026-09-15
- Added applicability override for Owner finance implementation suspension while preserving prior finance semantics/evidence.
- Marked GP Nested Forms cheque POC as deferred/not-proven rather than a current gate.
- Recorded daily manager SMS as a future requirement with implementation unselected and no Cron/Cron-like shared-host baseline without Owner re-adjudication.
- No historical `04` evidence mutated and no runtime PASS claimed.

### v1.0.1 — 2026-09-07
- Stable repository paths normalized during migration; project/evidence semantics unchanged.
- Current decisions reflected: SFC closed; scanner current-release deferred; code-backed visible choices system-mediated; finance optional/non-public/Registration-Officer-only.
- No historical `04` evidence mutated and no runtime PASS claimed.

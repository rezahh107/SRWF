# SRWF Execution Playbook — Runtime Source v1.3.0

## Purpose
This is the compact execution map for the SRWF implementation Project. It does not replace the full Master. When details matter, retrieve `docs/authority/MASTER.md`.

## Architecture baseline
- `Gravity Forms` = canonical form/entry data authority.
- `Gravity Flow` = only workflow, assignment, formal approval, and primary Officer operational surface.
- `GravityView` = optional read-only presentation only when a real presentation gap is proven.
- `Elementor` = outside the current operational baseline.
- Custom code/add-ons are allowed only for a named residual native-capability gap and must stay thin; never create parallel data/workflow/state authority.
- D-01..D-16 remain locked. `D-17` is Owner-refined to `POC_GATED / NOT_PROVEN`: first print candidate = `Gravity PDF Free` + SRWF-owned print layer, with no paid Gravity PDF template/extension and no custom PDF engine. A failed print candidate does not reopen parent architecture; it triggers Owner re-adjudication of the next renderer. A direct runtime contradiction to a lock must be escalated to the Owner.
- Current-release finance remains in Gravity Forms and on the Registration Officer's native Gravity Flow surface only: canonical/display unit = Rial; financial/manual-cheque fields are optional and non-public; `discount_amount` may default to 0; `net_payable_amount = tuition_amount - discount_amount`; `discount_amount > tuition_amount` must fail validation and not save. POS/PC-POS and online Sayad inquiry are deferred.
- Multi-cheque requirement is `1..N`. Current host selection = `GP Nested Forms` with one cheque per child Entry; runtime/entitlement are `NOT_PROVEN`. Parent-Child Forms is fallback only after a bounded Nested Forms failure.
- `PersianGravity Structured Scanner` remains a generic, host-agnostic, non-persistent capability, but the SRWF scanner path is **deferred from the current release**. All seven Sayad v01 output fields remain Hidden/future-reserved and are not populated by Scanner now.

## Execution sequence
### Stage 0 — Contract + environment
1. Runtime/environment inventory remains `PARTIAL/OWNER_ACCEPTED_FOR_PROGRESS`. Preserve the already-observed production versions; reopen residual staging/license/cache/build-identity details only when a later compatibility/deployment decision requires them.
2. Semantic Field Contract is `OWNER APPROVED / CLOSED`. Authoritative scaffold is now allowed with synthetic data only. After scaffold, bind the real Form/Field/Input/Step IDs in Implementation Mapping.
3. Keep real PII out of staging/UAT until privacy/retention is signed off.

### Stage 1 — Public form
- Build Gravity Forms after Field Contract Gate.
- School selector: simplest maintained/native path first; gate `V-03` = real Persian school-name search on mobile with real-scale dataset and correct stored school value.
- Iranian data quality: use simplest maintained solution; no custom kernel unless a proven gap remains.
- Photo field is upload only; image processing is out of current scope.

### Stage 2 — Native workflow
- Registration Officer Approval uses the Owner-approved native whitelist. Officer edits human-readable code-backed school/group/status choices; the system writes the matching canonical code/value, while raw technical codes are not directly editable. Optional current-release finance fields stay on this native Officer-only surface; no Windows/POS utility replaces Officer editing.
- Current-release finance semantics are closed: unit=Rial; `tuition_amount`, `discount_amount`, `discount_title` and manual-cheque finance fields are optional/non-public/Registration-Officer-only; `discount_amount` may default to 0; `net_payable_amount = tuition_amount - discount_amount`; `discount_amount > tuition_amount` => validation error and no save.
- Multi-cheque: one Cheque child Entry per cheque through GP Nested Forms when the host POC passes. Current release uses manual editing only; Scanner population is deferred.
- Accountant Approval and final external-pending step.
- Gate `V-01`: Inbox → Entry Details → edit allowed field without leaving current step/assignee → native Approve → correct next step.

### Stage 3 — Access
- Minimal Officer role/capabilities; no anonymous/display-all bypass on operational pages.
- Gate `V-02`.

### Stage 4 — Officer operational UI
- Native Gravity Flow Inbox + Entry Details; configure display fields/layout/timeline first.
- CSS-only visual refinement before custom markup. No custom Desk/list/table and no custom locking.
- Gate `V-05`: native Live Refresh works and cache does not break operations.

### Stage 5 — Human edit audit
- GravityRevisions, Admin-only.
- Gate `V-04`.

### Stage 6 — registration_counter
- WP All Import sync by canonical National ID; same National ID → same counter; importer does not advance Flow.
- Gate `V-06`.

### Stage 7 — Release
- Compatibility/regression on staging; privacy/retention sign-off; release/rollback evidence.
- `D-17` must be closed before the print/dossier surface is release-ready: `Gravity PDF Free` must PASS the bounded print POC, and the final dossier template is built only after the Semantic Field Contract is stable.
- No paid Gravity PDF template/extension is a baseline dependency; Browser Print is not maintained as a parallel production renderer.
- Current-release SRWF does **not** require a cheque Scanner path or `PRB-SCANNER-SOURCE-001`. The selected GP Nested Forms host still requires its bounded current-release POC for render/manual-edit/submit/link/reload/composition before that surface is release-ready.
- POS/PC-POS and online Sayad must remain absent from current-release runtime dependencies.

## Current-release finance + cheque contract
- `POS/PC-POS = DEFERRED`; do not build a Windows agent/utility, localhost bridge, payment queue, local payment ledger, or WordPress payment state for the current release.
- `ONLINE_SAYAD_INQUIRY = DEFERRED`.
- Manual cheque entry is the current-release path. Structured Scanner is deferred to a later phase; its seven Sayad output fields remain Hidden/future-reserved and no Scanner-based finance/cheque population occurs now.
- Each cheque is a separate GF child Entry under the selected maintained host; no custom relationship DB/state.

## Structured Scanner source-code contract — future-phase retained capability
This remains a technical capability contract, not runtime proof and **not a current-release SRWF gate**. It applies only if/when the Owner reopens scanner-based input in a future phase:
1. `parseScan(raw, profile)` is a pure JS module with no DOM dependency.
2. `buildUpdatePlan(parsed, mappings, existingTargets)` is pure and returns `updateSet | error`; it must enforce all-or-nothing planning.
3. `applyUpdatePlan(updateSet)` is the thin DOM layer; no target is changed if parse/plan fails.
4. If the repository lacks a JS harness, use built-in `node:test` for pure parser/planner tests rather than downgrading deterministic tests to manual-only. Browser-only lifecycle/focus behavior may remain integration/manual until an automated harness exists.
5. Scanner state is per-instance; no global initialized flag or shared mutable handler state. Multiple scanners/forms must not interfere.
6. Activation/focus behavior must not steal focus from an active editable control. Provide an explicit control/targeting path for the scanner instance.
7. `Enter` and `Tab` are valid scan terminators; an idle timeout may complete a scan, but exact timing is configuration/POC detail, not architecture.
8. Sayad v01 outputs are exactly: `qr_version`, `owner_type`, `owner_identifier`, `iban`, `bank_branch`, `cheque_serial`, `sayad_id`. Do not add stronger bank/version validation without broader evidence.

### `PRB-SCANNER-SOURCE-001` PASS — future scanner phase only
- Pure parser/planner tests execute and pass.
- Invalid parse/mapping produces no partial update plan.
- Seven-output Sayad v01 ordering is deterministic.
- Multiple scanner instances keep independent state in unit/integration coverage available to the repo.

### `PRB-NESTED-CHEQUE-001` PASS
With synthetic data on the target stack:
- Cheque child form opens/renders in the required Gravity Flow editable surface.
- Current-release criterion: manual child entry works without Scanner. Scanner initialization/population is excluded from this POC until a future Owner reopen.
- Officer can manually correct permitted fields.
- Child submit persists and remains linked to the correct parent.
- Reload preserves values and multi-cheque finance/print composition can read every child Entry.

**FAIL:** reject only the failing candidate/surface. A Nested Forms failure routes to the already-recorded Parent-Child Forms fallback; it does not authorize a custom relationship DB/workflow/state. Scanner behavior is outside the current-release POC and cannot be used to block this release path.

## D-17 print POC gate
`D-17` remains `NOT_PROVEN` until a synthetic-data POC on the target stack passes all of the following:
1. Persian/RTL glyph shaping is visually correct.
2. ZWNJ is preserved visually and through copy/paste.
3. A leading-zero National ID remains exact.
4. Jalali date text remains exact.
5. Amounts and at least one cheque/table row render correctly.
6. A4 pagination and page breaks are stable.
7. PDF text is searchable/copyable as logical Unicode, not only visually correct.
8. Normal Officer UX is `Print dossier` → PDF opens directly for viewing/printing; manual file download is not a required normal step. Automatic browser print-dialog opening is not required.

**PASS:** select `Gravity PDF Free` as the single production print renderer and proceed to the SRWF-owned dossier template/integration layer. A dedicated `SRWF Print` plugin is introduced only if a residual capability gap beyond a custom template/configuration is proven.

**FAIL:** stop that candidate. Do not auto-authorize paid Gravity PDF extensions/templates, a custom PDF engine, or a permanent Browser Print fallback. Re-adjudicate the next renderer with the Owner.

## Decision/probe method
For the current decision unit:
1. Identify the Gate/requirement and retrieve current project authority.
2. Retrieve local product knowledge before proposing a tool/plugin.
3. If existing evidence is sufficient, recommend/close without inventing a probe.
4. If the uncertainty is behavioral/runtime-only, define the smallest discriminating probe.
5. Use at most 3 serious candidates in one round. If all fail, stop and escalate candidate-space/requirement reconsideration instead of generating an endless fourth/fifth option.
6. Prefer native → official maintained extension → thin custom integration only for a proven residual gap.

## Knowledge retrieval order
1. Project meaning/locks/order: `docs/authority/MASTER.md`, then `docs/governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md`.
2. Fast cross-product capability lookup: materialize `knowledge/normalized/PRODUCT_KNOWLEDGE_NORMALIZED.txt.gz` when needed.
3. Project-specific constructability/composition details: apply `knowledge/constructability/APPLICABILITY_OVERLAY.md` first, then materialize `knowledge/constructability/CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt.gz`. The overlay supersedes stale project-level Gate/status projections only; underlying technical evidence/provenance remains usable.
4. Deep product details: materialize the corresponding archive under `knowledge/products/`.
5. If local evidence is missing, stale, contradictory, or insufficient for a material decision, use fresh **official vendor documentation**. Official-source fallback is evidence gathering, not permission to override Owner locks.

## Interpretation rule for normalized knowledge
`depth=DEEP` means higher semantic density in the normalized corpus; it does **not** by itself mean `FULLY_INGESTED`, closed knowledge boundary, runtime proof, or decision readiness. Check source status, limitations, material unknowns, and fresh official docs when decision-material.

## Runtime state store
External operational state store: Google Sheet `SRWF_RUNTIME_STATE`.
- `CURRENT_STATE` = current stage/gate/decision/candidate/last result/blocker/next action.
- `DECISION_HISTORY` = material probe/decision history.
The Project Instructions govern when it must be read/written. This file does not claim connector availability.

## Repository-baseline normalization
- Active paths are stable repository paths; old version-suffixed source names are historical provenance only.
- Current Overlay active path is `knowledge/constructability/APPLICABILITY_OVERLAY.md`.
- No architecture, Stage/Gate order, candidate selection, PASS/FAIL contract or runtime evidence state is promoted by repository migration.

## v1.3.0 Owner-decision / Gate sync
- Semantic Field Contract is now Owner-approved/closed; authoritative scaffold with synthetic data is the current next action.
- Scanner-based financial/cheque input is deferred from the current release; seven Sayad output fields stay Hidden/future-reserved.
- Officer edits human-readable code-backed choices and the system updates canonical codes; raw codes are not directly editable.
- Current-release finance/manual-cheque fields are optional, non-public and Registration-Officer-only; Rial is canonical/display; discount above tuition is rejected without save.
- Residual Environment Inventory remains partial/Owner-accepted for progression; privacy/retention still blocks real PII.
- No runtime PASS/validation claim is promoted by this documentation update.

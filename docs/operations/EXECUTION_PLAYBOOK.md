# SRWF Execution Playbook — Runtime Source v1.3.2

## Purpose
This is the compact execution map for the SRWF implementation Project. It does not replace the full Master. When details matter, retrieve `docs/authority/MASTER.md`. Current execution progress is always read from `runtime/CURRENT_STATE.yaml` on `main`.

## Architecture baseline
- `Gravity Forms` = canonical form/entry data authority.
- `Gravity Flow` = only workflow, assignment, formal approval, and primary Officer operational surface.
- `GravityView` = optional read-only presentation only when a real presentation gap is proven.
- `Elementor` = outside the current operational baseline.
- Custom code/add-ons are allowed only for a named residual native-capability gap and must stay thin; never create parallel data/workflow/state authority.
- D-01..D-16 remain locked. `D-17` is Owner-refined to `POC_GATED / NOT_PROVEN`: first print candidate = `Gravity PDF Free` + SRWF-owned print layer, with no paid Gravity PDF template/extension and no custom PDF engine. A failed print candidate does not reopen parent architecture; it triggers Owner re-adjudication of the next renderer. A direct runtime contradiction to a lock must be escalated to the Owner.
- Finance/manual-cheque semantics remain preserved in the SFC/history, but `OWNER-20260915-FINANCE-SUSPENSION-DAILY-MANAGER-SMS-SCOPE-SYNC` sets **finance implementation/validation = SUSPENDED** until explicit Owner reopen. Reserved finance fields may remain optional/non-public in the scaffold; finance-specific Flow whitelist, calculations, Bonyad/Hekmat bindings, cheque composition and POCs are not current blockers/gates.
- Multi-cheque requirement/host selection is preserved for future reopen: `1..N`, `GP Nested Forms` selected, Parent-Child Forms fallback after bounded FAIL. Current applicability = `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN`.
- `PersianGravity Structured Scanner` remains a generic, host-agnostic, non-persistent capability, but the SRWF scanner path is deferred. All seven Sayad v01 output fields remain Hidden/future-reserved.
- Daily manager SMS is a recorded future reporting requirement with implementation `NOT_SELECTED`; it must remain read-only relative to GF/Flow workflow state. Cron/Cron-like shared-host scheduling is not an accepted baseline without Owner re-adjudication.

## Session execution boot
Before any progress-dependent recommendation or `ادامه`:
1. read `repository.manifest.yaml`;
2. read `docs/authority/MASTER.md`;
3. read `runtime/CURRENT_STATE.yaml`;
4. read recent relevant events from `runtime/DECISION_HISTORY.jsonl`;
5. then use this Playbook and only the relevant contract/evidence.

Do not use the deprecated Google Sheet as a parallel current-state source.

## Execution sequence
### Stage 0 — Contract + environment
1. Runtime/environment inventory may remain `PARTIAL/OWNER_ACCEPTED_FOR_PROGRESS`. Preserve already-observed production facts; reopen residual staging/license/cache/build-identity details only when a later compatibility/deployment decision requires them.
2. Semantic Field Contract must be `OWNER APPROVED / CLOSED` before authoritative scaffold. After scaffold, bind the real Form/Field/Input/Step IDs in Implementation Mapping for active scope.
3. Keep real PII out of staging/UAT until privacy/retention is signed off.
4. Do not allow preserved finance semantics to become a finance implementation task while the Owner suspension remains active.

### Stage 1 — Public form
- Build Gravity Forms after Field Contract Gate.
- School selector: event86 locks GP Advanced Select for the current main form with GF Enhanced UI off; gate `V-03` still requires real Persian-name mobile search at real-scale plus correct stored school value.
- Iranian data quality: use simplest maintained solution; no custom kernel unless a proven gap remains.
- Photo field: required single jpg/jpeg <=5MB using GP File Upload Pro; required 3:4 crop and max 1200×1600 are the Owner-approved limited D-12 amendment. No custom/background/AI processing pipeline or minimum dimensions.
- Finance fields already present in the provisional scaffold may remain as optional/non-public reserved fields; do not add finance-specific runtime behavior as part of this stage while suspension is active.

### Stage 2 — Native workflow
- Registration Officer Approval uses the Owner-approved native whitelist for active scope. Officer edits human-readable code-backed school/group/status choices; the system writes the matching canonical code/value, while raw technical codes are not directly editable.
- Finance/manual-cheque editing/whitelist proof is **suspended**. Do not implement or validate amount derivation, discount rules, Bonyad/Hekmat conditional bindings, cheque child composition or finance-specific visibility as a prerequisite for current progression. When finance is reopened, all editing must remain native Gravity Flow and the preserved finance semantics apply.
- Accountant Approval and final external-pending step remain part of the native workflow.
- Gate `V-01`: Inbox → Entry Details → edit allowed active-scope field without leaving current step/assignee → native Approve → correct next step.

### Stage 3 — Access
- Minimal Officer role/capabilities; no anonymous/display-all bypass on operational pages.
- Preserved finance fields must not become public merely because finance implementation is suspended.
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
- `PRB-NESTED-CHEQUE-001` is retained but `DEFERRED_WITH_FINANCE_SCOPE`; it is not a current release gate until explicit Owner finance/cheque reopen.
- POS/PC-POS and online Sayad remain absent from current runtime dependencies.
- Daily manager SMS is not a release gate until the Owner explicitly activates that implementation scope.

## Preserved finance + cheque contract — suspended applicability
The following rules are preserved for future finance reopen and for interpreting reserved scaffold fields; they are **not current implementation requirements**:

- canonical/display money unit = Rial.
- finance/manual-cheque fields are optional and non-public/Registration-Officer-only.
- `discount_amount` initial default is empty; net is system-owned and empty when tuition is empty, otherwise tuition minus discount treating empty discount as zero without persisting zero.
- `discount_amount > tuition_amount` => validation error and no save.
- `finance_status` values remain `0=عادی, 1=بنیاد شهید, 3=حکمت`, optional/non-public/Officer-only, default `0`; independent `registration_status_code` remains removed by event86.
- Bonyad/Hekmat/coded-discount semantics remain preserved as locked by event78–86.
- `POS/PC-POS = DEFERRED`; do not build a Windows agent/utility, localhost bridge, payment queue, local payment ledger, or WordPress payment state.
- `ONLINE_SAYAD_INQUIRY = DEFERRED`.
- selected future multi-cheque host = GP Nested Forms; no custom relationship DB/state.

Reopen this implementation surface only by explicit Owner decision. A finance contract row in SFC is not permission to resume implementation by itself.

## Daily manager SMS — future requirement contract
- Need: at the end of each working day, send the manager an SMS containing the count of Entries the Registration Officer approved/advanced to Accountant during that working day.
- Source of truth for the count: read-only canonical Gravity Forms/Gravity Flow evidence.
- The reporting mechanism may not own, advance, rewrite, mirror or duplicate workflow state.
- Exact send time, business-day calendar, SMS provider, manager-mobile binding/source, retry/idempotency/failure behavior remain `OPEN / NOT_SELECTED`.
- Cron or Cron-like background scheduling on shared hosting is not an accepted baseline. If a serious candidate requires it, stop that candidate and return to Owner re-adjudication.
- Gravity Forms Notification Scheduler and `gravity-notification-manager` remain candidates only; no candidate is selected yet.
- Do not add a probe until the execution mechanism is an active decision unit. When activated, evaluate at most 3 serious candidates and stop at the first sufficient PASS.

## Structured Scanner source-code contract — future-phase retained capability
This remains a technical capability contract, not runtime proof and not a current SRWF gate. It applies only if/when the Owner reopens scanner-based input in a future phase:
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

### `PRB-NESTED-CHEQUE-001` PASS — retained future contract
Current applicability: `DEFERRED_WITH_FINANCE_SCOPE / NOT_PROVEN`.

When finance/cheque scope is explicitly reopened, with synthetic data on the target stack:
- Cheque child form opens/renders in the required Gravity Flow editable surface.
- manual child entry works without Scanner unless Scanner is separately reopened.
- Officer can manually correct permitted fields.
- Child submit persists and remains linked to the correct parent.
- Reload preserves values and multi-cheque finance/print composition can read every child Entry.

**FAIL after reopen:** reject only the failing candidate/surface. A Nested Forms failure routes to the already-recorded Parent-Child Forms fallback; it does not authorize a custom relationship DB/workflow/state.

## D-17 print POC gate
`D-17` remains `NOT_PROVEN` until a synthetic-data POC on the target stack passes all of the following:
1. Persian/RTL glyph shaping is visually correct.
2. ZWNJ is preserved visually and through copy/paste.
3. A leading-zero National ID remains exact.
4. Jalali date text remains exact.
5. Representative amounts and at least one table row render correctly; this may use synthetic representative content and does not reopen finance workflow implementation.
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
2. Apply `knowledge/constructability/APPLICABILITY_OVERLAY.md` before using constructability source `04`.
3. When local Product Knowledge is needed, materialize the byte-exact corpus with `python scripts/materialize_archives.py`. The original files are written under `.knowledge-materialized/pre-repository/` with their source names: `05_PRODUCT_KNOWLEDGE_NORMALIZED.txt`, `04_SRWF_CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt`, and deep product sources `06..09`.
4. Retrieve only the decision-relevant materialized source(s); source presence/hash integrity is evidence provenance, not runtime proof or decision readiness.
5. If local evidence is missing, stale, contradictory, or insufficient for a material decision, use fresh **official vendor documentation**. Official-source fallback is evidence gathering, not permission to override Owner locks.

## Interpretation rule for normalized knowledge
`depth=DEEP` means higher semantic density in the normalized corpus; it does **not** by itself mean `FULLY_INGESTED`, closed knowledge boundary, runtime proof, or decision readiness. Check source status, limitations, material unknowns, and fresh official docs when decision-material.

## Runtime state store
Owner decision `OWNER-20260907-REPOSITORY-RUNTIME-SSOT` establishes the repository as the live operational state store after cutover:

- `runtime/CURRENT_STATE.yaml` = current stage/gate/decision/candidate/last result/blockers/next action.
- `runtime/DECISION_HISTORY.jsonl` = append-only material runtime history after cutover.
- `history/pre-runtime-ssot/` = immutable complete pre-cutover Google Sheet history.
- Google Sheet `SRWF_RUNTIME_STATE` = `DEPRECATED_READ_ONLY_MIGRATION_SOURCE`; do not dual-write.

For a material state change, state + one appended event must be committed together and read back from `main` before persistence is claimed. If concurrent state changed, re-read instead of overwriting.

## Repository normalization
- Active paths are stable repository paths; old version-suffixed source names are historical provenance only.
- Current Overlay active path is `knowledge/constructability/APPLICABILITY_OVERLAY.md`.
- Exact pre-repository sources `01..11` live in `history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz`; materialization is local-only and not committed.
- Pre-cutover Runtime State and event history live under `history/pre-runtime-ssot/` with migration manifest/hash evidence.
- No architecture, Stage/Gate order, candidate selection, PASS/FAIL contract or runtime validation state is promoted merely by repository migration.

## Current Owner-decision / Gate sync
- Semantic Field Contract is Owner-approved/closed; authoritative scaffold is allowed with synthetic data subject to the current runtime blockers/next action in `runtime/CURRENT_STATE.yaml`.
- Scanner-based financial/cheque input remains deferred; seven Sayad output fields stay Hidden/future-reserved.
- Officer edits human-readable code-backed choices and the system updates canonical codes; raw codes are not directly editable.
- Finance/manual-cheque semantics are preserved, but implementation/validation is `SUSPENDED` until Owner reopen. Reserved fields may remain optional/non-public; finance-specific blockers/POCs must not control the active path.
- Daily manager SMS requirement is recorded; implementation is unselected and non-blocking until activated. No Cron/Cron-like baseline without Owner re-adjudication.
- Residual Environment Inventory remains partial/Owner-accepted for progression; privacy/retention still blocks real PII.
- Repository is the single runtime SSOT after accepted cutover; no Google Sheet dual-write.
- No runtime PASS/validation claim is promoted by documentation/state migration.

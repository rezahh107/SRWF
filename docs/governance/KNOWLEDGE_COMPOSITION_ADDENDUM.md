# SRWF Owner Knowledge & Native Composition Addendum v1.1.1

**Status:** OWNER-LOCKED GOVERNANCE ADDENDUM — MASTER-ALIGNED  
**Applies to:** `SRWF-MASTER v1.9.0` + `Execution Playbook v1.3.0` + current Product Knowledge / Constructability sources  
**Purpose:** preserve broad native/official capability awareness and disciplined composition analysis without turning incomplete product-knowledge coverage into a global prerequisite for Stage 0 or implementation.

## A. Authority boundary

This addendum does **not** replace or override `docs/authority/MASTER.md` as product/business/architecture authority, and it does not replace `docs/operations/EXECUTION_PLAYBOOK.md` as the compact execution map.

The Master governs architecture, semantics, Locks and current Stage/Gate ordering. This addendum governs **how product knowledge is gathered and used** when a material capability/composition decision is being made.

No item in this addendum may:

- require `FULL_OFFICIAL_KNOWLEDGE_COVERAGE` as a prerequisite for starting Stage 0;
- automatically reopen `D-01..D-17` merely because additional documentation is ingested;
- promote a product-knowledge checkpoint, manifest, normalized record or constructability snapshot into runtime proof;
- silently change the Native-First parent architecture.

A direct runtime contradiction to an active Lock remains subject to `CONTRADICTION → STOP → OWNER RE-ADJUDICATION`.

## B. Core Product Knowledge scope

The following four product families remain `CORE_KNOWLEDGE_PRODUCTS` for broad capability awareness:

1. Gravity Forms family
2. Gravity Flow family
3. GravityView family
4. Gravity Perks family

`FULL_OFFICIAL_KNOWLEDGE_COVERAGE` remains a valid **knowledge-base quality target**. It is useful for long-term completeness, discovery and future re-evaluation, but it is **not a hard Stage 0 Gate** and is not required before bounded implementation work that is already authorized by the current Master/Playbook.

For a current material decision, the required knowledge scope is **decision-scoped**: retrieve enough relevant official/local evidence to establish the serious candidate space and make a supportable decision or define the smallest discriminating runtime probe.

If the evidence is materially insufficient, the decision unit is `INCOMPLETE` or `BLOCKED`; this does not automatically block unrelated Stage 0 work or independent surfaces.

## C. Completeness semantics

When a product family or checkpoint claims completeness, distinguish:

- `DOCUMENTATION_SURFACE_COMPLETENESS`: all in-scope official documentation items for the frozen snapshot are classified with no unresolved discovery item within that declared boundary; and
- `SEMANTIC_CAPABILITY_EXTRACTION_COMPLETENESS`: material documented capability/configuration/limitation/integration/extension semantics are represented or explicitly classified with reason.

Source presence, URL visitation, manifest coverage, hash integrity, `depth=DEEP`, schema validity or generated reports do not by themselves establish complete semantic knowledge or runtime behavior.

Incomplete family coverage must remain visible as an evidence limitation. It must **not** be transformed into `PROVEN_ABSENT` for a capability and must **not** be used as a global Stage 0 blocker.

Product truth remains independent of current SRWF selection: non-selected capabilities may remain in the knowledge corpus without reopening current architecture.

## D. Native/Official Capability Composition

`NATIVE_FIRST` does not mean `SINGLE_PLUGIN_FIRST`.

For a material open requirement, the serious candidate space should include, as relevant:

- native single capabilities;
- maintained same-product compositions;
- maintained cross-product compositions with documented/evidence-supported interaction;
- official/maintained extensions;
- only then, thin custom integration for a proven residual gap.

Do not brute-force meaningless combinations. Candidate generation is bounded by the actual requirement and available evidence.

The selection objective is the least-complex solution that satisfies mandatory requirements with acceptable correctness, security, workflow consistency, auditability, UX, maintenance and upgrade risk. Native/official is a strong preference, not permission to accept a materially inferior result.

## E. Scoped Native Capability Exhaustion

Before recommending **new project custom code** or a **new external component** for a material requirement, the decision record must show that relevant native/official capabilities and serious valid compositions were considered to the extent supported by current evidence. This is `SCOPED_NATIVE_CAPABILITY_EXHAUSTION`.

This is a decision-scoped obligation, not a requirement to finish every documentation surface in all four product families.

If the uncertainty is only runtime-provable, stop documentation expansion and run the smallest discriminating probe with observable PASS/FAIL criteria.

If enough evidence already supports a candidate, close the decision without additional non-discriminating probes.

## F. Locked Decision handling

`D-01..D-17` are not automatically reopened by new ingestion, new checkpoint creation, broader product discovery or a higher knowledge-completeness percentage.

A locked decision is reconsidered only when one of the following applies:

1. the Owner explicitly re-adjudicates it;
2. direct runtime evidence contradicts an active Lock;
3. a newly retrieved capability/composition is materially relevant and could change the decision, in which case the affected decision unit is brought to the Owner rather than silently changed;
4. the current Master/Playbook explicitly defines a POC-gated decision whose result requires re-adjudication.

A decision can be described as `RECONFIRMED`, `REFINED` or `SUPERSEDED` only when an actual re-adjudication/revalidation has been performed under current authority. Historical `PENDING_KNOWLEDGE_COMPLETION` records in older constructability snapshots are not current decision state.

## G. Current execution ordering

Knowledge work is interleaved **just-in-time** with execution; it is not a mandatory global pre-Stage0 phase.

Current ordering is:

1. Retrieve current authority: Master, current Playbook, this Addendum.
2. Stage 0: record real environment/version/license/entitlement inventory and complete the Owner-approved Semantic Field Contract required by the current scope.
3. Before each material component/capability choice, retrieve relevant normalized/constructability/deep product knowledge and fresh official docs when needed.
4. If evidence is sufficient, decide/close; if uncertainty is runtime-only, run the smallest discriminating probe.
5. Build authoritative scaffold only after the relevant Semantic Field Contract Gate.
6. Bind Implementation Mapping to real IDs after scaffold.
7. Execute required `V-01..V-06` and other surface-specific POCs/tests in governed order.
8. Privacy/retention sign-off is required before real PII is introduced into staging/UAT/production.

No broad product family is added to a mandatory completeness set without an Owner decision. Product-knowledge maintenance may continue independently and must not falsely promote `plan/documented/checkpoint` states into runtime validation.

## H. Constructability snapshot applicability

`knowledge/constructability/CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt.gz` is a derived evidence/constructability snapshot. Its historical project-level Gate/status projections may refer to older Master/Addendum semantics.

When using that archive, apply `knowledge/constructability/APPLICABILITY_OVERLAY.md` first. The overlay changes **applicability of stale project projections**, not the underlying product-capability evidence or historical provenance.

## Changelog
### v1.1.1 — 2026-09-07
- Pointer-only alignment to Master v1.9.0 and Playbook v1.3.0 after Owner decision sync; no knowledge-governance semantics changed.

### v1.1.0 — 2026-09-06
- Removed the obsolete global requirement that all four Core Product families reach 100% knowledge completeness before Stage 0.
- Recast full product-knowledge coverage as a long-term knowledge quality target rather than an execution Gate.
- Replaced global `NATIVE_CAPABILITY_EXHAUSTION` with decision-scoped exhaustion/retrieval.
- Removed automatic full-knowledge revalidation of `D-01..D-17`; current Locks reopen only under current authority/Owner/runtime contradiction/material new evidence.
- Historical v1.1.0 alignment was to Master v1.8.1 and Playbook v1.2.2; current active paths are stable repository paths.

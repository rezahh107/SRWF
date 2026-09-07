# SRWF Risk Register

`ACTIVE_NORMATIVE` — derived from current Master, with repository-era wording normalized.

| ID | Risk | Impact | Mitigation | Fallback |
|---|---|---|---|---|
| `R-01` | target environment never validated and design remains unproven | Critical | keep environment gaps visible; execute `V-01..V-06` before release | no release |
| `R-02` | Officer Approval edit whitelist exposes forbidden field | Critical | explicit whitelist + `V-01` | tighten whitelist |
| `R-03` | operational access leaks to unauthorized user | Critical | native auth/assignment/capability checks + `V-02` | disable affected front-end surface |
| `R-04` | school-name search slow/unreliable on mobile | High | `V-03` with real-scale synthetic/non-PII catalog; stop at first PASS | next simple maintained candidate |
| `R-05` | cache/optimizer causes stale operational page | High | exclude operational routes from bad cache + `V-05` | disable cache on route |
| `R-06` | human edit audit incomplete or exposed beyond Admin | High | access config + `V-04` | restrict history access |
| `R-07` | counter sync updates wrong Entry or creates inconsistent counters | Critical | exact National ID, dry-run/ambiguity report + `V-06` | stop import + manual source correction |
| `R-08` | import accidentally advances workflow | Critical | importer writes counter only + `V-06` | native/manual finalization |
| `R-09` | vendor upgrade changes relied-on native behavior | High | version matrix + staging regression | rollback version |
| `R-10` | complexity pressure reintroduces custom Desk/queue/locking/audit bridge | Medium | Native-First + ADR/Owner re-adjudication | reject request |
| `R-11` | Persian/Unicode/A4/Officer print UX POC fails | High | bounded D-17 synthetic POC; no paid dependency/dual renderer | fail candidate + Owner re-adjudication |
| `R-12` | Nested Forms fails child render/save/link/finance composition in Flow surface | High | bounded synthetic POC; no custom relationship state | fail candidate; Parent-Child Forms fallback only |
| `R-13` | future Sayad QR bank/version differs from seven-output v01 | High | conservative validation + broader samples before stronger rules | new profile version/Owner review |
| `R-14` | future scanner parse error partially mutates targets | Critical | pure parse/plan + atomic apply + tests | reject update plan, preserve targets |
| `R-15` | persisted finance contradicts `tuition-discount` | High | SFC + server validation/recompute | reject save + Entry correction |
| `R-16` | documentation drift hides a current field/decision | Critical for implementation correctness | standalone contracts + stable paths + manifest + validator + Decision Ledger | block affected materialization/PR until reconciled |
| `R-17` | real PII enters Git or pre-policy staging | Critical | `.gitignore`, validator/CI, synthetic-only gate, Privacy Contract | remove/revoke/rotate as applicable; stop affected release work |
| `R-18` | repo and live Runtime State become parallel/conflicting SSOTs | High | repo = canonical docs/contracts; Sheet = live operational state; repo snapshots non-canonical | read live Sheet and reconcile durable docs explicitly |

## Review rule

A risk can be closed only by current evidence that addresses its acceptance condition. `DOCUMENTED` mitigation is not execution proof.

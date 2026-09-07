## SRWF change classification
- [ ] Architecture / Lock
- [ ] Semantic contract
- [ ] Implementation Mapping / runtime binding
- [ ] Validation / POC evidence
- [ ] Documentation / provenance only

## Required integrity
- [ ] Current authority and affected contract were read before editing.
- [ ] `plan != implementation != validation` has been preserved.
- [ ] `NOT_PROVEN != PROVEN_ABSENT` has been preserved.
- [ ] No real PII, intake images, credentials, DB dumps or operational data ledgers were added.
- [ ] `README.md`, `AGENTS.md`, manifests and active pointers still resolve to real repository paths.
- [ ] If Semantic Field Contract changed, `include_in_form` and `value_required` were reviewed independently.
- [ ] If Implementation Mapping changed, IDs came from actual runtime read-back and were not invented.
- [ ] Provenance archive/member hashes remain valid when source corpus changed.
- [ ] `scripts/validate_docs.py` passed, or CI infrastructure was explicitly proven unavailable and equivalent manual validation evidence was recorded.

## Acceptance boundary
A feature branch/PR is not Accepted Current. Acceptance requires merge to `main` and post-merge read-back.

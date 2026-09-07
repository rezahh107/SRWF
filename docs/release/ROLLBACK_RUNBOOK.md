# SRWF Rollback Runbook

**Status:** `DRAFT / NOT_EXECUTED`

## Goal
Rollback must restore the last known-good SRWF configuration without inventing alternate workflow/data authority.

## Preconditions before any release

Record in Release Manifest:

- pre-release Git commit/tag;
- exact WordPress/plugin versions;
- Gravity Forms form export/backup;
- Gravity Flow workflow/config backup or reproducible configuration record;
- database/application backup according to approved privacy policy;
- cache/CDN state and operational route exclusions;
- implementation mapping version.

## Rollback triggers

- unauthorized data exposure;
- workflow/assignment/Approval regression;
- wrong canonical field persistence;
- counter import corruption/ambiguity;
- operational cache/freshness failure;
- print renderer produces materially wrong dossier data;
- vendor upgrade incompatibility;
- release dependency/license failure.

## Procedure

1. Stop affected write/import operations.
2. Preserve non-PII diagnostic evidence and exact failure timestamp/environment.
3. Restore previous approved plugin/code/config versions.
4. Restore previous GF/Flow configuration only from known-good backup/reproducible artifact.
5. Clear/bypass caches as required for operational routes.
6. Verify authentication/authorization and native Flow Inbox/Approval before reopening operations.
7. Verify a synthetic known-good registration path.
8. If data writes occurred, reconcile affected Entries using canonical Gravity Forms data and approved backups; do not create a parallel correction DB/state.
9. Record incident/result in Runtime State and Decision Ledger if it changes durable semantics.

## Counter import rollback

If `V-06`/production import detects ambiguity or wrong targeting:

- stop import;
- do not advance Flow;
- correct source/match logic;
- restore/reconcile only `registration_counter` values from authoritative evidence.

## Print rollback

A D-17 candidate failure does not authorize dual production renderers. Disable the failing renderer path and return to Owner re-adjudication.

## Privacy/security rollback

If PII/secret is accidentally committed:

- stop sharing/release work;
- remove from active branch/history according to repository security process;
- rotate affected secrets immediately if applicable;
- treat deletion from latest commit alone as insufficient for secret exposure;
- record incident without reproducing sensitive values.

## Validation

This runbook is not proven until a staging rollback exercise is actually executed and recorded. Current state: `UNEXECUTED`.

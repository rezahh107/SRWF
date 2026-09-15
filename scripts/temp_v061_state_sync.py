from pathlib import Path
import json
import re

state_path = Path('runtime/CURRENT_STATE.yaml')
history_path = Path('runtime/DECISION_HISTORY.jsonl')
s = state_path.read_text(encoding='utf-8')

def one(old: str, new: str) -> None:
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'expected exactly one match for {old!r}, found {n}')
    s = s.replace(old, new, 1)

one('state_version: 18', 'state_version: 19')
one('  decision: OBS-20260915-CI-RUNTIME-LAB-V060-PASS', '  decision: OBS-20260915-CI-RUNTIME-LAB-V061-FUP-PASS')
one('  candidate: GF_IMPORT_SCAFFOLD_V060_PROVISIONAL', '  candidate: GF_IMPORT_SCAFFOLD_V061_PROVISIONAL')
one('  next_action_id: STAGING_IMPORT_GF_V060_SYNTHETIC', '  next_action_id: STAGING_IMPORT_GF_V061_SYNTHETIC')
s, n = re.subn(r'^  last_observed_result: .*$', '  last_observed_result: CI_RUNTIME_LAB_V061_FUP_PASS / EXACT_CANDIDATE_SHA_VERIFIED / GF_3_1_1_1_GP_2_3_16_FUP_1_5_13_REAL_IMPORT_READBACK_PASS / STUDENT_PHOTO_3_4_MAX_1200X1600_RUNTIME_AND_FRONTEND_LOCALIZATION_PASS / GF_ROUNDTRIP_EXPORT_PRESERVED / FORM_INACTIVE / 37_FIELDS / STAGING_IMPORT_UNEXECUTED / FINANCE_SUSPENSION_PRESERVED', s, count=1, flags=re.M)
if n != 1:
    raise SystemExit('last_observed_result replacement failed')
s, n = re.subn(r'^  next_action: .*$', '  next_action: Execute the governed real staging import of the exact SRWF_GravityForms_Import_v0.6.1_PROVISIONAL.json bytes matching SHA-256 a2e10c6eae8c29715a038899a989fa4c85d83e1eebd44127bf9904d986752642 while the form remains inactive and using synthetic data only, then read back actual staging Form/Field IDs and critical settings including GP File Upload Pro 3:4 crop and maximum 1200x1600 before Implementation Mapping is bound. Never bind disposable CI Form/Field IDs into Implementation Mapping. Current executor must use an existing authorized staging identity/control path; do not introduce a standalone remote-control platform/plugin merely to obtain staging access.', s, count=1, flags=re.M)
if n != 1:
    raise SystemExit('next_action replacement failed')

old_gf = "- id: GF_STAGING_IMPORT_UNEXECUTED\n  effect: exact v0.6.0 disposable CI import/read-back passed with authentic Gravity Forms 3.1.1.1, but the actual Gravity Forms staging import/post-import settings/ID read-back remains unexecuted; CI-generated IDs are disposable and must not be bound into Implementation Mapping\n"
new_gf = "- id: GF_STAGING_IMPORT_UNEXECUTED\n  effect: exact v0.6.1 disposable authentic full-stack import/read-back passed with Gravity Forms 3.1.1.1, Gravity Perks 2.3.16 and GP File Upload Pro 1.5.13, including executable student_photo 3:4 crop and max 1200x1600 plus authentic GF round-trip preservation; actual Gravity Forms staging import/post-import settings/ID read-back remains unexecuted; CI-generated IDs are disposable and must not be bound into Implementation Mapping\n"
one(old_gf, new_gf)

marker = 'deferred_non_blockers:\n'
blocker = "- id: STAGING_EXECUTION_PATH_NOT_CONNECTED\n  effect: current executor has no authoritative SRWF staging identity or connected authorized WP-CLI/REST/SSH/browser control channel; no repository staging workflow/secret path or connected Drive/Gmail target identity was found; Owner runtime-management decision forbids introducing a standalone External Executor, staging self-hosted runner, persistent daemon or general-purpose WordPress remote-control plugin merely to obtain staging control\n"
one(marker, blocker + marker)

gov_marker = '  project_package:\n'
v061 = '''  v061_fup_runtime_qualification:
    observed_status: LAB_PASS
    source_artifact: SRWF_GravityForms_Import_v0.6.1_PROVISIONAL.json
    source_artifact_sha256: a2e10c6eae8c29715a038899a989fa4c85d83e1eebd44127bf9904d986752642
    source_artifact_size: 308200
    lab_run: 35014441345
    lab_head: 7445bba98e4dcf687f115dc7579b0d4951c6a672
    evidence_artifact_id: 10415485138
    evidence_artifact_digest: sha256:f505c4eec635a9fbf3884f1168c97efa79168fae7622626c5ecafb9adaebc49a
    evidence_file_sha256: 4db8de24d488e431744560bc14fd2802b453d8652136feb2f72661ef8276aaa0
    roundtrip_export_sha256: 52100137273a16fbed7121318025fc5d623431293d25c7ce522e0791b8d5dfc2
    wordpress_version: 6.8.3
    php_version: 8.2.33
    database: MariaDB 11.4.8
    gravityforms_version: 3.1.1.1
    gravityforms_package_sha256: 542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b
    gravity_perks_version: 2.3.16
    gravity_perks_package_sha256: a160d166fb7894b0dfc558ae92e0c230a1336ed2a81e78fa1216be72b1024e7c
    gp_file_upload_pro_version: 1.5.13
    gp_file_upload_pro_package_sha256: fdab5621dc0c1b9d33384696f554ef9ac0d646a70f8cee652a1bc05c43f8f7ce
    form_inactive: true
    field_count: 37
    student_photo_aspect_ratio: 0.75
    student_photo_max_width: 1200
    student_photo_max_height: 1600
    student_photo_min_dimensions: null
    student_photo_exact_dimensions: null
    frontend_localization_verified: true
    authentic_gf_roundtrip_preserved: true
    staging_exercised: false
    ci_ids_authoritative_for_mapping: false
    proof_pr: 11
    proof_pr_merged: false
'''
one(gov_marker, v061 + gov_marker)
one('  last_event_seq: 90', '  last_event_seq: 91')
one('  last_event_id: OBS-20260915-CI-RUNTIME-LAB-V060-PASS', '  last_event_id: OBS-20260915-CI-RUNTIME-LAB-V061-FUP-PASS')

if not s.endswith('\n'):
    s += '\n'
s += '''- SRWF_GravityForms_Import_v0.6.1_PROVISIONAL.json sha256=a2e10c6eae8c29715a038899a989fa4c85d83e1eebd44127bf9904d986752642 size=308200
- GitHub Actions SRWF v0.6.1 FUP Runtime Proof run 35014441345 = LAB_PASS / staging not exercised
- Runtime proof exact head 7445bba98e4dcf687f115dc7579b0d4951c6a672; PR #11 closed unmerged after evidence capture
- Runtime proof artifact 10415485138 digest sha256:f505c4eec635a9fbf3884f1168c97efa79168fae7622626c5ecafb9adaebc49a
- Runtime proof evidence sha256=4db8de24d488e431744560bc14fd2802b453d8652136feb2f72661ef8276aaa0
- Authentic Gravity Forms round-trip export sha256=52100137273a16fbed7121318025fc5d623431293d25c7ce522e0791b8d5dfc2
- Gravity Perks 2.3.16 package sha256=a160d166fb7894b0dfc558ae92e0c230a1336ed2a81e78fa1216be72b1024e7c
- GP File Upload Pro 1.5.13 package sha256=fdab5621dc0c1b9d33384696f554ef9ac0d646a70f8cee652a1bc05c43f8f7ce
- Controlled staging-path search on 2026-09-15 found no authoritative SRWF staging identity or connected WP-CLI/REST/SSH/browser control path in repository, connected Drive, or SRWF-related Gmail evidence; unrelated WordPress sites were not treated as SRWF staging
'''
state_path.write_text(s, encoding='utf-8')

lines = history_path.read_text(encoding='utf-8').splitlines()
last = json.loads(lines[-1])
if last.get('event_seq') != 90 or last.get('decision_id') != 'OBS-20260915-CI-RUNTIME-LAB-V060-PASS':
    raise SystemExit(f'unexpected history tail: {last.get("event_seq")} {last.get("decision_id")}')
event = {
    'schema_version': 1,
    'event_seq': 91,
    'date_time': '2026-09-15',
    'stage_gate': 'STAGE_0 / CI_RUNTIME_LAB_V061_FUP_ACCEPTANCE',
    'decision_id': 'OBS-20260915-CI-RUNTIME-LAB-V061-FUP-PASS',
    'need': 'Close the v0.6.0 student_photo executable-metadata gap with an authentic GP File Upload Pro runtime proof before governed staging.',
    'candidates': 'Proceed with v0.6.0 despite missing executable 3:4/max-dimension metadata; guess File Upload Pro property names; materialize v0.6.1 only from exact GP File Upload Pro 1.5.13 source/runtime behavior and prove it in a disposable authentic full-stack runtime.',
    'probe_or_evidence': 'Exact v0.6.1 candidate SHA-256 a2e10c6eae8c29715a038899a989fa4c85d83e1eebd44127bf9904d986752642, size 308200. GitHub Actions run 35014441345 on exact head 7445bba98e4dcf687f115dc7579b0d4951c6a672 completed success with WordPress 6.8.3, PHP 8.2.33, MariaDB 11.4.8, Gravity Forms 3.1.1.1, Gravity Perks 2.3.16 and GP File Upload Pro 1.5.13. One inactive form with 37 fields imported; student_photo read-back exposed required crop 3:4, max 1200x1600, no min/exact dimensions; plugin-derived ratio was 0.75; FUP frontend localization exposed the same ratio/max values; authentic Gravity Forms export preparation preserved the settings. Evidence artifact 10415485138 digest sha256:f505c4eec635a9fbf3884f1168c97efa79168fae7622626c5ecafb9adaebc49a; evidence JSON SHA-256 4db8de24d488e431744560bc14fd2802b453d8652136feb2f72661ef8276aaa0; round-trip export SHA-256 52100137273a16fbed7121318025fc5d623431293d25c7ce522e0791b8d5dfc2. PR #11 was closed unmerged after evidence capture so temporary runner URLs/harness did not enter main. Controlled repository/Drive/Gmail discovery did not find an authoritative SRWF staging identity or connected authorized WP-CLI/REST/SSH/browser execution path.',
    'observed_result': 'v0.6.1 is LAB_PASS in an authentic disposable full stack. student_photo 3:4 and max 1200x1600 are executable/readable through GP File Upload Pro runtime and frontend localization; min/exact dimensions are empty; authentic Gravity Forms export preserves them. Staging was not exercised and CI IDs remain non-authoritative. No authorized staging control path is connected to this executor.',
    'decision': 'Promote v0.6.1 as the current provisional staging-import candidate and supersede v0.6.0 for the next action. Execute governed real staging import of exact v0.6.1 only when an existing authorized staging identity/control path is available; keep the form inactive and use synthetic data only; then read back real staging IDs/settings before Implementation Mapping. Do not install or introduce a standalone remote-control platform/plugin merely to gain staging access.',
    'reopen_condition': 'Authentic replay fails; staging import drops or changes a locked setting; Owner changes the candidate or staging-execution policy; or authoritative target evidence contradicts the v0.6.1 FUP behavior.',
    'status': 'LAB_PASS / V061_CURRENT_STAGING_CANDIDATE / STUDENT_PHOTO_EXECUTABLE_3_4_MAX_1200X1600_PROVEN_IN_DISPOSABLE_RUNTIME / GF_ROUNDTRIP_PRESERVED / STAGING_IMPORT_UNEXECUTED / STAGING_EXECUTION_PATH_NOT_CONNECTED / CI_IDS_NON_AUTHORITATIVE / NO_STAGING_VALIDATION_PROMOTION',
    'source': {
        'kind': 'OWNER_PACKAGES_PLUS_GITHUB_ACTIONS_AUTHENTIC_FULL_STACK_RUNTIME',
        'candidate_sha256': 'a2e10c6eae8c29715a038899a989fa4c85d83e1eebd44127bf9904d986752642',
        'candidate_size': 308200,
        'lab_run': 35014441345,
        'lab_head': '7445bba98e4dcf687f115dc7579b0d4951c6a672',
        'artifact_id': 10415485138,
        'artifact_digest': 'sha256:f505c4eec635a9fbf3884f1168c97efa79168fae7622626c5ecafb9adaebc49a',
        'evidence_sha256': '4db8de24d488e431744560bc14fd2802b453d8652136feb2f72661ef8276aaa0',
        'roundtrip_export_sha256': '52100137273a16fbed7121318025fc5d623431293d25c7ce522e0791b8d5dfc2',
        'gravityforms_version': '3.1.1.1',
        'gravityforms_sha256': '542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b',
        'gravity_perks_version': '2.3.16',
        'gravity_perks_sha256': 'a160d166fb7894b0dfc558ae92e0c230a1336ed2a81e78fa1216be72b1024e7c',
        'gp_file_upload_pro_version': '1.5.13',
        'gp_file_upload_pro_sha256': 'fdab5621dc0c1b9d33384696f554ef9ac0d646a70f8cee652a1bc05c43f8f7ce',
        'staging_exercised': False,
        'pr': 11,
        'pr_merged': False,
    },
}
lines.append(json.dumps(event, ensure_ascii=False, separators=(',', ':')))
history_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

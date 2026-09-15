#!/usr/bin/env bash
set -Eeuo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
finalizer="$root/tests/runtime-lab/finalize-evidence.py"
expected_sha='445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89'

all_success='{"identity":"success","php":"success","harness":"success","scaffold":"success","wordpress":"success","gravityforms":"success","import":"success","assertion":"success","negative":"success"}'

# Pre-runtime dependency failure => canonical LAB_BLOCKED.
blocked="$tmp/blocked.json"
SRWF_PHASE_OUTCOMES_JSON='{"identity":"success","php":"success","harness":"success","scaffold":"success","wordpress":"success","gravityforms":"failure","import":"skipped","assertion":"skipped","negative":"skipped"}' \
python3 "$finalizer" "$blocked" "$expected_sha" >/dev/null
grep -q '"lab_status": "LAB_BLOCKED"' "$blocked"
grep -q 'GRAVITY_FORMS_DEPENDENCY_SETUP_FAILED' "$blocked"
set +e
python3 "$finalizer" --enforce "$blocked" >/dev/null 2>&1
status=$?
set -e
[[ "$status" -ne 0 ]]

# Executed runtime/assertion failure => canonical LAB_FAIL.
failed="$tmp/failed.json"
SRWF_PHASE_OUTCOMES_JSON='{"identity":"success","php":"success","harness":"success","scaffold":"success","wordpress":"success","gravityforms":"success","import":"failure","assertion":"skipped","negative":"skipped"}' \
python3 "$finalizer" "$failed" "$expected_sha" >/dev/null
grep -q '"lab_status": "LAB_FAIL"' "$failed"
grep -q 'GRAVITY_FORMS_IMPORT_READBACK_FAILED' "$failed"
set +e
python3 "$finalizer" --enforce "$failed" >/dev/null 2>&1
status=$?
set -e
[[ "$status" -ne 0 ]]

# Existing valid LAB_PASS is byte-for-byte preserved on the successful path.
pass="$tmp/pass.json"
cat >"$pass" <<'JSON'
{"schema_version":"1.0.0","lab_status":"LAB_PASS","scenario":"GF_V060_IMPORT_READBACK","sentinel":"preserve-me"}
JSON
before="$(sha256sum "$pass" | awk '{print $1}')"
SRWF_PHASE_OUTCOMES_JSON="$all_success" python3 "$finalizer" "$pass" "$expected_sha" >/dev/null
after="$(sha256sum "$pass" | awk '{print $1}')"
[[ "$before" = "$after" ]]
python3 "$finalizer" --enforce "$pass"

# Missing/corrupt evidence can never become green after otherwise-successful phases.
for kind in missing corrupt; do
  evidence="$tmp/$kind.json"
  if [[ "$kind" = corrupt ]]; then printf '{not-json' >"$evidence"; fi
  SRWF_PHASE_OUTCOMES_JSON="$all_success" python3 "$finalizer" "$evidence" "$expected_sha" >/dev/null
  grep -q '"lab_status": "LAB_FAIL"' "$evidence"
  set +e
  python3 "$finalizer" --enforce "$evidence" >/dev/null 2>&1
  status=$?
  set -e
  [[ "$status" -ne 0 ]]
done

# Admission blocker is finalized centrally as LAB_BLOCKED without a per-step writer.
admission="$tmp/admission.json"
SRWF_PHASE_OUTCOMES_JSON='{"identity":"success","php":"success","harness":"success","scaffold":"success","wordpress":"skipped","gravityforms":"skipped","import":"skipped","assertion":"skipped","negative":"skipped"}' \
SRWF_ADMISSION_BLOCKED=true SRWF_ADMISSION_BLOCKER=EXACT_SCAFFOLD_BYTES_UNAVAILABLE \
python3 "$finalizer" "$admission" "$expected_sha" >/dev/null
grep -q '"lab_status": "LAB_BLOCKED"' "$admission"
grep -q 'EXACT_SCAFFOLD_BYTES_UNAVAILABLE' "$admission"

# Summary and enforcement consume the same finalized canonical file.
summary="$tmp/summary.txt"
python3 "$root/tests/runtime-lab/render-summary.py" "$admission" >"$summary"
grep -q 'status: `LAB_BLOCKED`' "$summary"
set +e
python3 "$finalizer" --enforce "$admission" >/dev/null 2>&1
status=$?
set -e
[[ "$status" -ne 0 ]]

echo 'SRWF_LAB_FINALIZER_SELF_TEST_PASS dependency_blocked=PASS runtime_fail=PASS pass_preserved=PASS missing_corrupt_fail_closed=PASS canonical_summary_enforcement=PASS'

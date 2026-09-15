#!/usr/bin/env bash
set -Eeuo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

source_json="$tmp/source.json"
readback_json="$tmp/readback.json"
positive_json="$tmp/positive.json"
confirmation_drift_json="$tmp/confirmation-drift.json"
notification_drift_json="$tmp/notification-drift.json"
title_drift_json="$tmp/title-drift.json"

cat >"$source_json" <<'JSON'
{"version":"3.1.1.1","0":{"id":"SOURCE_FORM_ID","date_created":"2024-01-01 00:00:00","version":"2.9.0","title":"SRWF Lab Guard Fixture","labelPlacement":"top_label","notifications":{"notify-admin":{"id":"notify-admin","name":"Synthetic notification","event":"form_submission","to":"{admin_email}","subject":"Synthetic subject","message":"Synthetic body"}},"confirmations":{"default":{"id":"default","name":"Default Confirmation","isDefault":true,"type":"message","message":"Synthetic confirmation","url":"","pageId":"","queryString":""}},"fields":[{"id":1,"type":"text","label":"Synthetic Field","isRequired":true}]}}
JSON

source_sha="$(sha256sum "$source_json" | awk '{print $1}')"
gf_sha='542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b'

cat >"$readback_json" <<JSON
{
  "runtime": {
    "gravity_forms": "3.1.1.1",
    "gravity_forms_package_sha256": "$gf_sha"
  },
  "source": {"sha256": "$source_sha"},
  "import": {
    "count": 1,
    "form_id": 77,
    "title": "SRWF Lab Guard Fixture",
    "is_active": false,
    "form": {
      "id": 77,
      "date_created": "2026-09-15 12:00:00",
      "version": "3.1.1.1",
      "title": "SRWF Lab Guard Fixture",
      "labelPlacement": "top_label",
      "notifications": {"notify-admin":{"id":"notify-admin","name":"Synthetic notification","event":"form_submission","to":"{admin_email}","subject":"Synthetic subject","message":"Synthetic body"}},
      "confirmations": {"default":{"id":"default","name":"Default Confirmation","isDefault":true,"type":"message","message":"Synthetic confirmation","url":"","pageId":"","queryString":""}},
      "fields": [{"id":1,"type":"text","label":"Synthetic Field","isRequired":true,"formId":77}]
    }
  }
}
JSON

run_verifier() {
  local readback="$1"
  local evidence="$2"
  SRWF_SCAFFOLD_SHA256="$source_sha" \
  SRWF_GF_SHA256="$gf_sha" \
  SRWF_GF_VERSION='3.1.1.1' \
  php "$root/tests/runtime-lab/assert-readback.php" "$source_json" "$readback" "$evidence"
}

expect_fail() {
  local readback="$1"
  local evidence="$2"
  local expected_marker="$3"
  set +e
  run_verifier "$readback" "$evidence" >/dev/null 2>&1
  local status=$?
  set -e
  if [[ "$status" -eq 0 ]]; then
    echo "Verifier incorrectly accepted drift: $expected_marker" >&2
    exit 1
  fi
  grep -q '"lab_status": "LAB_FAIL"' "$evidence"
  grep -q "$expected_marker" "$evidence"
}

# Positive fixture proves source-defined confirmations/notifications are compared while
# runtime-owned form identity/state differences remain intentionally excluded.
run_verifier "$readback_json" "$positive_json" >/dev/null
grep -q '"lab_status": "LAB_PASS"' "$positive_json"
grep -q '"source_defined_confirmations_readback": true' "$positive_json"
grep -q '"source_defined_notifications_readback": true' "$positive_json"

cp "$readback_json" "$tmp/confirmation-drift-readback.json"
python3 - "$tmp/confirmation-drift-readback.json" <<'PY'
import json, sys
p=sys.argv[1]
data=json.load(open(p, encoding='utf-8'))
data['import']['form']['confirmations']['default']['message']='DRIFTED confirmation'
open(p,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False))
PY
expect_fail "$tmp/confirmation-drift-readback.json" "$confirmation_drift_json" 'form.confirmations.default.message'

cp "$readback_json" "$tmp/notification-drift-readback.json"
python3 - "$tmp/notification-drift-readback.json" <<'PY'
import json, sys
p=sys.argv[1]
data=json.load(open(p, encoding='utf-8'))
del data['import']['form']['notifications']['notify-admin']
open(p,'w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False))
PY
expect_fail "$tmp/notification-drift-readback.json" "$notification_drift_json" 'form.notifications.notify-admin'

set +e
SRWF_SCAFFOLD_SHA256="$source_sha" \
SRWF_GF_SHA256="$gf_sha" \
SRWF_GF_VERSION='3.1.1.1' \
SRWF_LAB_EXPECT_TITLE_OVERRIDE='__BROKEN_EXPECTATION__' \
php "$root/tests/runtime-lab/assert-readback.php" "$source_json" "$readback_json" "$title_drift_json" >/dev/null 2>&1
status=$?
set -e
if [[ "$status" -eq 0 ]]; then
  echo 'Verifier incorrectly accepted a deliberately broken title expectation.' >&2
  exit 1
fi
grep -q '"lab_status": "LAB_FAIL"' "$title_drift_json"
grep -q 'form_title_mismatch' "$title_drift_json"

echo 'SRWF_LAB_VERIFIER_SELF_TEST_PASS confirmation_drift=REJECTED notification_drift=REJECTED runtime_identity_difference=ACCEPTED title_drift=REJECTED'

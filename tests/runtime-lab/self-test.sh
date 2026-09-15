#!/usr/bin/env bash
set -Eeuo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

source_json="$tmp/source.json"
readback_json="$tmp/readback.json"
positive_json="$tmp/positive.json"
negative_json="$tmp/negative.json"

cat >"$source_json" <<'JSON'
{"version":"3.1.1.1","0":{"title":"SRWF Lab Guard Fixture","labelPlacement":"top_label","fields":[{"id":1,"type":"text","label":"Synthetic Field","isRequired":true}]}}
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
      "title": "SRWF Lab Guard Fixture",
      "labelPlacement": "top_label",
      "fields": [{"id":1,"type":"text","label":"Synthetic Field","isRequired":true,"formId":77}]
    }
  }
}
JSON

SRWF_SCAFFOLD_SHA256="$source_sha" \
SRWF_GF_SHA256="$gf_sha" \
SRWF_GF_VERSION='3.1.1.1' \
php "$root/tests/runtime-lab/assert-readback.php" "$source_json" "$readback_json" "$positive_json" >/dev/null

grep -q '"lab_status": "LAB_PASS"' "$positive_json"

set +e
SRWF_SCAFFOLD_SHA256="$source_sha" \
SRWF_GF_SHA256="$gf_sha" \
SRWF_GF_VERSION='3.1.1.1' \
SRWF_LAB_EXPECT_TITLE_OVERRIDE='__BROKEN_EXPECTATION__' \
php "$root/tests/runtime-lab/assert-readback.php" "$source_json" "$readback_json" "$negative_json" >/dev/null 2>&1
status=$?
set -e

if [[ "$status" -eq 0 ]]; then
  echo 'Verifier incorrectly accepted a deliberately broken read-back assertion.' >&2
  exit 1
fi

grep -q '"lab_status": "LAB_FAIL"' "$negative_json"
echo 'SRWF_LAB_GUARD_SELF_TEST_PASS'

#!/usr/bin/env bash
set -Eeuo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

positive="$tmp/positive.json"
negative="$tmp/negative.json"

cat >"$positive" <<'JSON'
{"version":"3.1.1.1","0":{"fields":[{"adminLabel":"student_photo","gpfupEnable":true,"gpfupEnableCrop":true,"gpfupCropRequired":true,"gpfupAspectRatioAntecedent":3,"gpfupAspectRatioConsequent":4,"gpfupMaxWidth":1200,"gpfupMaxHeight":1600,"multipleFiles":true,"maxFiles":"1","allowedExtensions":"jpg,jpeg","maxFileSize":"5"}]}}
JSON

python3 "$root/tests/runtime-lab/assert-scaffold-photo-settings.py" "$positive" >/dev/null

python3 - "$positive" "$negative" <<'PY'
import json, sys
source, target = sys.argv[1:]
data = json.load(open(source, encoding='utf-8'))
field = data['0']['fields'][0]
for key in ('gpfupAspectRatioAntecedent', 'gpfupAspectRatioConsequent', 'gpfupMaxWidth', 'gpfupMaxHeight'):
    field.pop(key, None)
open(target, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False))
PY

set +e
python3 "$root/tests/runtime-lab/assert-scaffold-photo-settings.py" "$negative" >/dev/null 2>&1
status=$?
set -e
if [[ "$status" -eq 0 ]]; then
  echo 'Photo-settings guard incorrectly accepted missing ratio/max metadata.' >&2
  exit 1
fi

echo 'SRWF_PHOTO_SETTINGS_SELF_TEST_PASS positive=ACCEPTED missing_machine_settings=REJECTED'

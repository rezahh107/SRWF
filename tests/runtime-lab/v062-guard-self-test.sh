#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="${1:-$ROOT/tests/runtime-lab/fixtures/SRWF_GravityForms_Import_v0.6.2_PROVISIONAL.json}"
VALIDATOR="$ROOT/tests/runtime-lab/assert-v062-artifact.php"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

expect_rejected() {
  local label="$1"
  local path="$2"
  local needle="$3"
  set +e
  SRWF_V062_SKIP_BYTE_IDENTITY=1 php "$VALIDATOR" "$path" >"$TMP/$label.out" 2>&1
  local status=$?
  set -e
  if [[ $status -eq 0 ]]; then
    echo "Mutation unexpectedly accepted: $label" >&2
    cat "$TMP/$label.out" >&2
    exit 1
  fi
  grep -Fq "$needle" "$TMP/$label.out" || {
    echo "Mutation $label failed for the wrong reason" >&2
    cat "$TMP/$label.out" >&2
    exit 1
  }
  echo "REJECTED $label"
}

python3 - "$SOURCE" "$TMP" <<'PY'
import copy, json, pathlib, sys
source, outdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
root = json.loads(source.read_text(encoding='utf-8'))
form = next(v for k, v in root.items() if k != 'version')
fields = {f['adminLabel']: f for f in form['fields']}

def write(name, mutate):
    candidate = copy.deepcopy(root)
    cform = next(v for k, v in candidate.items() if k != 'version')
    cfields = {f['adminLabel']: f for f in cform['fields']}
    mutate(cfields)
    (outdir / f'{name}.json').write_text(json.dumps(candidate, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')

write('legacy-national-id', lambda f: f['national_id'].__setitem__('type', 'ir_national_id'))

def legacy_dob(f):
    f['dob_jalali']['type'] = 'date'
    f['dob_jalali']['check_jalali'] = 1
write('legacy-dob', legacy_dob)
write('school-without-gpadvs', lambda f: f['school_code'].__setitem__('gpadvsEnable', False))
write('photo-min-dimension', lambda f: f['student_photo'].__setitem__('gpfupMinWidth', '600'))
PY

expect_rejected legacy-national-id "$TMP/legacy-national-id.json" 'legacy ir_national_id is forbidden'
expect_rejected legacy-dob "$TMP/legacy-dob.json" 'dob_jalali must use current PersianGravity pgr_jalali_date'
expect_rejected school-without-gpadvs "$TMP/school-without-gpadvs.json" 'school_code must enable GP Advanced Select'
expect_rejected photo-min-dimension "$TMP/photo-min-dimension.json" 'student_photo gpfupMinWidth must stay unset'

# Byte identity is independently fail-closed, not just semantic validation.
cp "$SOURCE" "$TMP/byte-drift.json"
printf ' ' >> "$TMP/byte-drift.json"
if php "$VALIDATOR" "$TMP/byte-drift.json" >/dev/null 2>&1; then
  echo 'byte-drift was incorrectly accepted' >&2
  exit 1
fi
echo 'REJECTED byte-drift'

echo 'V062_GUARD_SELF_TEST_PASS'

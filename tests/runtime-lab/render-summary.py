#!/usr/bin/env python3
"""Render a concise human-readable GitHub Actions summary from Lab evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: render-summary.py <lab-evidence.json>")

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
status = data.get("lab_status", "LAB_FAIL")
print(f"- status: `{status}`")
print(f"- scenario: `{data.get('scenario', 'unknown')}`")

source = data.get("source_artifact", {})
print(f"- scaffold SHA-256: `{source.get('sha256') or source.get('expected_sha256') or 'unknown'}`")

runtime = data.get("runtime", {})
gf_version = runtime.get("gravity_forms") or runtime.get("gravity_forms_expected")
gf_hash = runtime.get("gravity_forms_package_sha256") or runtime.get("gravity_forms_package_sha256_expected")
print(f"- Gravity Forms: `{gf_version or 'NOT_TESTED'}`")
print(f"- Gravity Forms package SHA-256: `{gf_hash or 'NOT_TESTED'}`")

observed = data.get("observed", {})
if status == "LAB_PASS":
    print(f"- disposable CI Form ID: `{observed.get('generated_form_id')}`")
    print(f"- disposable CI field count: `{observed.get('field_count')}`")
    print("- scope: exact form import + read-back only; CI IDs are non-authoritative")
elif status == "LAB_BLOCKED":
    print(f"- blocker: `{data.get('blocker', 'UNKNOWN')}`")
    print("- runtime/import/read-back: `NOT_TESTED`")
else:
    failures = data.get("failures", [])
    print(f"- assertion failures: `{len(failures)}`")

print("- staging exercised: `false`")
print("- finance/manual-cheque behavior: `NOT_TESTED / SUSPENDED`")

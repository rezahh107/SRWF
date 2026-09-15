#!/usr/bin/env python3
"""Write bounded machine-readable evidence when the CI Runtime Lab cannot start."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("usage: write-blocked-evidence.py <output> <reason> <expected-scaffold-sha256>")

output = Path(sys.argv[1])
reason = sys.argv[2]
expected_sha = sys.argv[3]
output.parent.mkdir(parents=True, exist_ok=True)

payload = {
    "schema_version": "1.0.0",
    "lab_status": "LAB_BLOCKED",
    "scenario": "GF_V060_IMPORT_READBACK",
    "blocker": reason,
    "source_artifact": {
        "name": "SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json",
        "expected_sha256": expected_sha,
        "bytes_admitted": False,
    },
    "runtime": {
        "wordpress_expected": os.environ.get("SRWF_WP_VERSION"),
        "php_expected": os.environ.get("SRWF_PHP_VERSION"),
        "gravity_forms_expected": os.environ.get("SRWF_GF_VERSION"),
        "gravity_forms_package_sha256_expected": os.environ.get("SRWF_GF_SHA256"),
        "runtime_booted": False,
    },
    "observed": {
        "form_created": False,
        "generated_form_id": None,
        "generated_field_ids": [],
        "import_readback_executed": False,
    },
    "evidence_semantics": {
        "ci_form_field_ids_are_disposable": True,
        "write_ids_to_implementation_mapping": False,
        "staging_exercised": False,
        "staging_pass": False,
        "production_ready_claim": False,
        "finance_manual_cheque_behavior": "NOT_TESTED_SUSPENDED",
        "synthetic_entry_data_created": False,
        "mock_or_regenerated_scaffold_substituted": False,
    },
}

output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"SRWF_RUNTIME_LAB LAB_BLOCKED reason={reason}")

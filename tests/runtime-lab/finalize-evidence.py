#!/usr/bin/env python3
"""Finalize or enforce the single canonical SRWF Runtime Lab evidence file."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

SCENARIO = "GF_V060_IMPORT_READBACK"
ALLOWED_STATUSES = {"LAB_PASS", "LAB_FAIL", "LAB_BLOCKED", "NOT_TESTED"}
REQUIRED_PASS_ASSERTIONS = (
    "exact_scaffold_hash",
    "single_form_import",
    "form_inactive",
    "title_readback",
    "field_structure_readback",
    "source_defined_confirmations_readback",
    "source_defined_notifications_readback",
    "source_defined_settings_readback",
)

PHASE_RULES = (
    ("identity", "LAB_FAIL", "REPOSITORY_IDENTITY_CHECK_FAILED"),
    ("php", "LAB_BLOCKED", "PHP_RUNTIME_SETUP_FAILED"),
    ("harness", "LAB_FAIL", "HARNESS_VALIDATION_FAILED"),
    ("scaffold", "LAB_BLOCKED", "SCAFFOLD_ADMISSION_FAILED"),
    ("wordpress", "LAB_BLOCKED", "WORDPRESS_RUNTIME_SETUP_FAILED"),
    ("gravityforms", "LAB_BLOCKED", "GRAVITY_FORMS_DEPENDENCY_SETUP_FAILED"),
    ("import", "LAB_FAIL", "GRAVITY_FORMS_IMPORT_READBACK_FAILED"),
    ("assertion", "LAB_FAIL", "IMPORT_READBACK_ASSERTION_FAILED"),
    ("negative", "LAB_FAIL", "NEGATIVE_ASSERTION_GUARD_FAILED"),
)


def validate_evidence(data: Any, expected_sha: str | None = None) -> str | None:
    if not isinstance(data, dict):
        return "TERMINAL_EVIDENCE_NOT_OBJECT"
    if data.get("schema_version") != "1.0.0":
        return "TERMINAL_EVIDENCE_SCHEMA_INVALID"
    if data.get("scenario") != SCENARIO:
        return "TERMINAL_EVIDENCE_SCENARIO_INVALID"
    status = data.get("lab_status")
    if status not in ALLOWED_STATUSES:
        return "TERMINAL_EVIDENCE_STATUS_INVALID"

    if status == "LAB_PASS":
        source = data.get("source_artifact")
        runtime = data.get("runtime")
        observed = data.get("observed")
        assertions = data.get("assertions")
        semantics = data.get("evidence_semantics")
        failures = data.get("failures")
        if not all(isinstance(value, dict) for value in (source, runtime, observed, assertions, semantics)):
            return "TERMINAL_PASS_EVIDENCE_STRUCTURE_INVALID"
        source_sha = source.get("sha256")
        pinned_sha = source.get("expected_sha256")
        if not isinstance(source_sha, str) or source_sha == "" or source_sha != pinned_sha:
            return "TERMINAL_PASS_SOURCE_SHA_INVALID"
        if expected_sha is not None and source_sha != expected_sha:
            return "TERMINAL_PASS_SOURCE_SHA_UNEXPECTED"
        if not runtime.get("gravity_forms") or not runtime.get("gravity_forms_package_sha256"):
            return "TERMINAL_PASS_RUNTIME_IDENTITY_MISSING"
        if observed.get("form_created") is not True or observed.get("inactive") is not True:
            return "TERMINAL_PASS_FORM_STATE_INVALID"
        if not isinstance(observed.get("generated_form_id"), (int, str)) or not isinstance(observed.get("field_count"), int):
            return "TERMINAL_PASS_RUNTIME_IDS_INVALID"
        if observed.get("field_count", 0) <= 0:
            return "TERMINAL_PASS_FIELD_COUNT_INVALID"
        if any(assertions.get(name) is not True for name in REQUIRED_PASS_ASSERTIONS):
            return "TERMINAL_PASS_ASSERTIONS_INCOMPLETE"
        if failures != []:
            return "TERMINAL_PASS_FAILURES_NONEMPTY"
        if semantics.get("ci_form_field_ids_are_disposable") is not True:
            return "TERMINAL_PASS_CI_ID_SEMANTICS_INVALID"
        if semantics.get("write_ids_to_implementation_mapping") is not False:
            return "TERMINAL_PASS_MAPPING_SEMANTICS_INVALID"
        if semantics.get("staging_exercised") is not False or semantics.get("staging_pass") is not False:
            return "TERMINAL_PASS_STAGING_SEMANTICS_INVALID"
    elif status == "LAB_BLOCKED":
        if not isinstance(data.get("blocker") or data.get("terminal_reason"), str):
            return "TERMINAL_BLOCKED_REASON_MISSING"
    elif status == "LAB_FAIL":
        failures = data.get("failures")
        if not isinstance(failures, list) or len(failures) == 0:
            return "TERMINAL_FAIL_REASON_MISSING"
    return None


def read_existing(path: Path, expected_sha: str | None = None) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "TERMINAL_EVIDENCE_MISSING"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "TERMINAL_EVIDENCE_CORRUPT"
    error = validate_evidence(data, expected_sha)
    if error is not None:
        return None, error
    return data, None


def load_phase_outcomes() -> dict[str, str]:
    raw = os.environ.get("SRWF_PHASE_OUTCOMES_JSON", "{}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid SRWF_PHASE_OUTCOMES_JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("SRWF_PHASE_OUTCOMES_JSON must be an object")
    return {str(key): str(value) for key, value in data.items()}


def first_phase_failure(outcomes: dict[str, str]) -> tuple[str, str, str] | None:
    for phase, status, reason in PHASE_RULES:
        outcome = outcomes.get(phase, "")
        if outcome in {"failure", "cancelled"}:
            if outcome == "cancelled":
                reason = f"{phase.upper()}_PHASE_CANCELLED"
            return phase, status, reason
    return None


def build_terminal_evidence(
    *,
    status: str,
    reason: str,
    terminal_phase: str,
    expected_sha: str,
    outcomes: dict[str, str],
) -> dict[str, Any]:
    scaffold_admitted = outcomes.get("scaffold") == "success" and os.environ.get("SRWF_ADMISSION_BLOCKED", "false") != "true"
    import_executed = outcomes.get("import") in {"success", "failure"}
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "lab_status": status,
        "scenario": SCENARIO,
        "terminal_phase": terminal_phase,
        "terminal_reason": reason,
        "phase_outcomes": outcomes,
        "source_artifact": {
            "name": "SRWF_GravityForms_Import_v0.6.0_PROVISIONAL.json",
            "expected_sha256": expected_sha,
            "bytes_admitted": scaffold_admitted,
        },
        "runtime": {
            "wordpress_expected": os.environ.get("SRWF_WP_VERSION"),
            "php_expected": os.environ.get("SRWF_PHP_VERSION"),
            "gravity_forms_expected": os.environ.get("SRWF_GF_VERSION"),
            "gravity_forms_package_sha256_expected": os.environ.get("SRWF_GF_SHA256"),
            "wordpress_setup_succeeded": outcomes.get("wordpress") == "success",
            "gravity_forms_setup_succeeded": outcomes.get("gravityforms") == "success",
        },
        "observed": {
            "form_created": False,
            "generated_form_id": None,
            "generated_field_ids": [],
            "import_readback_executed": import_executed,
        },
        "evidence_semantics": {
            "canonical_terminal_evidence": True,
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
    if status == "LAB_BLOCKED":
        payload["blocker"] = reason
    elif status == "LAB_FAIL":
        payload["failures"] = [reason]
    return payload


def write_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def finalize(path: Path, expected_sha: str) -> int:
    outcomes = load_phase_outcomes()
    existing, existing_error = read_existing(path, expected_sha)

    phase_failure = first_phase_failure(outcomes)
    if phase_failure is not None:
        phase, desired_status, reason = phase_failure
        if existing is not None and existing.get("lab_status") == desired_status:
            print(f"SRWF_RUNTIME_LAB FINALIZED preserved={desired_status} phase={phase}")
            return 0
        write_payload(
            path,
            build_terminal_evidence(
                status=desired_status,
                reason=reason,
                terminal_phase=phase,
                expected_sha=expected_sha,
                outcomes=outcomes,
            ),
        )
        print(f"SRWF_RUNTIME_LAB FINALIZED status={desired_status} phase={phase} reason={reason}")
        return 0

    if os.environ.get("SRWF_ADMISSION_BLOCKED", "false") == "true":
        reason = os.environ.get("SRWF_ADMISSION_BLOCKER") or "EXACT_SCAFFOLD_BYTES_UNAVAILABLE"
        write_payload(
            path,
            build_terminal_evidence(
                status="LAB_BLOCKED",
                reason=reason,
                terminal_phase="scaffold",
                expected_sha=expected_sha,
                outcomes=outcomes,
            ),
        )
        print(f"SRWF_RUNTIME_LAB FINALIZED status=LAB_BLOCKED phase=scaffold reason={reason}")
        return 0

    if existing is not None:
        print(f"SRWF_RUNTIME_LAB FINALIZED preserved={existing['lab_status']}")
        return 0

    reason = existing_error or "TERMINAL_EVIDENCE_MISSING"
    write_payload(
        path,
        build_terminal_evidence(
            status="LAB_FAIL",
            reason=reason,
            terminal_phase="finalize",
            expected_sha=expected_sha,
            outcomes=outcomes,
        ),
    )
    print(f"SRWF_RUNTIME_LAB FINALIZED status=LAB_FAIL phase=finalize reason={reason}")
    return 0


def enforce(path: Path) -> int:
    existing, error = read_existing(path)
    if existing is None:
        print(f"SRWF Runtime Lab canonical evidence invalid: {error}", file=sys.stderr)
        return 1
    status = existing["lab_status"]
    if status == "LAB_PASS":
        return 0
    if status == "LAB_BLOCKED":
        print("SRWF Runtime Lab is blocked; see canonical machine-readable evidence.", file=sys.stderr)
        return 78
    print(f"SRWF Runtime Lab did not pass: {status}", file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--enforce":
        if len(sys.argv) != 3:
            raise SystemExit("usage: finalize-evidence.py --enforce <lab-evidence.json>")
        return enforce(Path(sys.argv[2]))
    if len(sys.argv) != 3:
        raise SystemExit("usage: finalize-evidence.py <lab-evidence.json> <expected-scaffold-sha256>")
    return finalize(Path(sys.argv[1]), sys.argv[2])


if __name__ == "__main__":
    raise SystemExit(main())

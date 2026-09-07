#!/usr/bin/env python3
"""Repository integrity checks for SRWF documentation/contracts.

Stdlib-only by design: this validator is a structural/drift guard, not a YAML
or semantic theorem prover. It intentionally checks the specific invariants that
previously caused SRWF documentation drift/field omission.
"""
from __future__ import annotations

import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


def require(path: str) -> Path:
    p = ROOT / path
    if not p.exists():
        fail(f"missing required path: {path}")
    return p


REQUIRED = [
    "README.md",
    "AGENTS.md",
    "repository.manifest.yaml",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    ".gitignore",
    "docs/INDEX.md",
    "docs/authority/MASTER.md",
    "docs/operations/EXECUTION_PLAYBOOK.md",
    "docs/governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md",
    "docs/governance/OWNER_COMPREHENSION_PROTOCOL.md",
    "docs/governance/DECISION_LEDGER.md",
    "docs/governance/RISK_REGISTER.md",
    "docs/governance/MINIMALITY_CHALLENGE.md",
    "docs/governance/REMAINING_OWNER_BINDINGS.md",
    "docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml",
    "docs/contracts/SEMANTIC_FIELD_CONTRACT.md",
    "docs/contracts/WORKFLOW_CONTRACT.md",
    "docs/contracts/ACCESS_CONTROL_CONTRACT.md",
    "docs/contracts/IMPLEMENTATION_MAPPING.yaml",
    "docs/contracts/IMPLEMENTATION_MAPPING.md",
    "docs/contracts/ENVIRONMENT_MANIFEST.md",
    "docs/contracts/PRIVACY_RETENTION_CONTRACT.md",
    "docs/validation/TEST_MATRIX.md",
    "docs/validation/DEFINITION_OF_DONE.md",
    "docs/validation/POC_REGISTER.md",
    "docs/release/RELEASE_MANIFEST.md",
    "docs/release/ROLLBACK_RUNBOOK.md",
    "knowledge/README.md",
    "knowledge/constructability/APPLICABILITY_OVERLAY.md",
    "evidence/provenance/SOURCE_MANIFEST.yaml",
    "runtime/README.md",
    "runtime/snapshots/CURRENT_STATE.yaml",
    "history/pre-repository/README.md",
    "schemas/semantic-field-contract.schema.json",
    "schemas/implementation-mapping.schema.json",
    "schemas/repository-manifest.schema.json",
    "scripts/materialize_archives.py",
    "scripts/validate_docs.py",
]


def check_required() -> None:
    for p in REQUIRED:
        require(p)


def extract_field_blocks(text: str) -> dict[str, str]:
    # Each block begins with '- contract_id:' and ends before the next such block.
    matches = list(re.finditer(r"(?m)^\s*-\s+contract_id:\s*([^\s#]+)\s*$", text))
    blocks: dict[str, str] = {}
    for idx, match in enumerate(matches):
        cid = match.group(1).strip('"\'')
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        if cid in blocks:
            fail(f"duplicate contract_id: {cid}")
        blocks[cid] = text[start:end]
    return blocks


def assert_block(blocks: dict[str, str], cid: str, expected: list[str]) -> None:
    block = blocks.get(cid)
    if not block:
        fail(f"missing material field contract: {cid}")
        return
    for needle in expected:
        if needle not in block:
            fail(f"{cid} missing invariant: {needle}")


def check_sfc() -> None:
    p = require("docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml")
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "include_in_form" not in text or "value_required" not in text:
        fail("SFC must explicitly distinguish include_in_form and value_required")
    blocks = extract_field_blocks(text)
    assert_block(blocks, "HOME_PHONE", ["include_in_form: true", "value_required: false"])
    assert_block(blocks, "STUDENT_FATHER_NAME", ["include_in_form: true", "value_required: true"])
    assert_block(blocks, "STUDENT_MOBILE", ["include_in_form: true", "value_required: true"])
    assert_block(blocks, "STUDENT_FIRST_NAME", ["value_required: true"])
    assert_block(blocks, "STUDENT_LAST_NAME", ["value_required: true"])
    for key in ["qr_version", "owner_type", "owner_identifier", "iban", "bank_branch", "cheque_serial", "sayad_id"]:
        if f"machine_purpose: {key}" not in text:
            fail(f"missing hidden future Sayad field: {key}")
    if "manual_field_inventory_status: INCOMPLETE_ENUMERATION" not in text:
        fail("manual cheque inventory gap must remain explicit until bound")


def check_mapping() -> None:
    p = require("docs/contracts/IMPLEMENTATION_MAPPING.yaml")
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "status: UNBOUND" in text:
        # At baseline no real IDs may be invented.
        suspicious = re.findall(r"(?m)^\s*(form_id|field_id|step_id|route_or_page_id):\s*([^\s#]+)", text)
        for key, value in suspicious:
            if value not in {"null", "~"}:
                fail(f"unbound Implementation Mapping contains non-null {key}={value}")


def check_ssot_boundary() -> None:
    agents = require("AGENTS.md")
    runtime = require("runtime/README.md")
    for p in [agents, runtime]:
        if p.exists():
            t = p.read_text(encoding="utf-8")
            if "SRWF_RUNTIME_STATE" not in t or "SSOT" not in t:
                fail(f"runtime SSOT boundary missing in {p.relative_to(ROOT)}")


def check_archive() -> None:
    history = ROOT / "history" / "pre-repository"
    parts = sorted(history.glob("srwf_pre_repository_sources.tar.gz.b64.part*"))
    if len(parts) != 16:
        fail(f"pre-repository source archive must have 16 parts; found {len(parts)}")
        return
    try:
        encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
        raw = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        fail(f"source archive decode failed: {exc}")
        return
    expected = "d3aa23753aabae2db95381e57c5050c5d0429865c94b9c1a15b5e0b0d3eb27a8"
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        fail(f"source archive SHA mismatch: {actual}")


def check_forbidden_repo_paths() -> None:
    forbidden_fragments = [
        "srwf_processing_ledger",
        "srwf_audit_ledger",
        "paper_intake_images",
        "/pii/",
        "/intake/real/",
        "/exports/real/",
    ]
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = "/" + str(p.relative_to(ROOT)).lower().replace("\\", "/")
        for frag in forbidden_fragments:
            if frag in rel:
                fail(f"forbidden operational/PII path present: {rel}")


def check_active_entrypoints() -> None:
    master = require("docs/authority/MASTER.md")
    playbook = require("docs/operations/EXECUTION_PLAYBOOK.md")
    overlay = require("knowledge/constructability/APPLICABILITY_OVERLAY.md")
    for p in [master, playbook, overlay]:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        if "NOT_PROVEN != PROVEN_ABSENT" in text or p == master:
            pass
    if master.exists() and "Gravity Forms = canonical data authority" not in master.read_text(encoding="utf-8"):
        fail("Master missing canonical data authority invariant")
    if master.exists() and "Gravity Flow = تنها workflow/assignment/formal Approval authority" not in master.read_text(encoding="utf-8"):
        fail("Master missing Gravity Flow workflow authority invariant")


def main() -> int:
    check_required()
    check_sfc()
    check_mapping()
    check_ssot_boundary()
    check_archive()
    check_forbidden_repo_paths()
    check_active_entrypoints()

    if ERRORS:
        print("SRWF documentation integrity: FAIL")
        for err in ERRORS:
            print(f"- {err}")
        return 1
    print("SRWF documentation integrity: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

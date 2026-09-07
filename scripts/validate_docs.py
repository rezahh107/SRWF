#!/usr/bin/env python3
"""SRWF repository structural, contract, runtime-state and provenance integrity guard."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
ARCHIVE_REL = "history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz"
ARCHIVE_SHA256 = "82b0201ce3920214fe2ac7b9bd7defaa8769651fbbd1168abcd0a1ba91d32ed4"
ARCHIVE_SIZE = 353740
EXPECTED_SOURCES = {
    "01_SRWF_MASTER_AUTHORITY_v1.9.0-fa.md": (230874, "0f986c7104d3884e95ff4a5db7f125f6cf3eb639c745a55fcfef4abf3c0ad27a"),
    "02_SRWF_OWNER_KNOWLEDGE_AND_COMPOSITION_ADDENDUM_v1.1.1.md": (8728, "83497b157328ba82d1b6900dbe05b4635e7acf22600cc3cbf35a8f92da89930d"),
    "03_SRWF_EXECUTION_PLAYBOOK_v1.3.0.md": (13690, "0fb1979eadb3241161f5942278f05c27a0a60b8680f66fa1fa3f61b247dd3a47"),
    "04_SRWF_CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt": (924039, "0b9aa5208f2c3c5b3f12b196ec8a70de71d536dcb00d2ecc8c5e85d94f138f98"),
    "05_PRODUCT_KNOWLEDGE_NORMALIZED.txt": (2305256, "7a4e93e3a2919e72b9e74fb78af553698fe320455049fee428e8d1c43170f112"),
    "06_GRAVITY_FORMS_PRODUCT_KNOWLEDGE.txt": (2626276, "5c6777c951d4732bc7e2ce728582c8ce7191658f9a755aa0e03b9eeb100b4148"),
    "07_GRAVITY_FLOW_PRODUCT_KNOWLEDGE.txt": (266287, "f3dfcfa294d94e5060af46d2ce38981ef7013123f71bf0a3eba6263f8ee9fe54"),
    "08_GRAVITYVIEW_PRODUCT_KNOWLEDGE.txt": (601551, "f290ddd3b5a528ebf1213bf9c4247b202b3f86dda574b90b6e101f7c7051bd5f"),
    "09_GRAVITY_PERKS_PRODUCT_KNOWLEDGE.txt": (651713, "afe196760396cd23c1ef9b29437689cabd6b21805c89a9bd18e714fe0d5cb319"),
    "10_SRWF_OWNER_COMPREHENSION_PROTOCOL_v1.0.1.md": (12106, "966cf2500a91f82ba2774a57e1499badc7277220d3f33d19057d6d7282fb4e44"),
    "11_SRWF_CONSTRUCTABILITY_APPLICABILITY_OVERLAY_v1.0.1.md": (6346, "755f3aeeaf4dcd0314efe721184a59b8b1b2b6b931a12f4f5cbaee82d20332fd"),
}
RUNTIME_CHUNKS = [
    "history/pre-runtime-ssot/DECISION_HISTORY_000001_000008.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000009_000016.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000017_000024.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000025_000032.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000033_000040.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000041_000048.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000049_000056.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000057_000064.jsonl",
    "history/pre-runtime-ssot/DECISION_HISTORY_000065_000072.jsonl",
]
REQUIRED = [
    "README.md", "AGENTS.md", "repository.manifest.yaml", "CHANGELOG.md", "CONTRIBUTING.md", ".gitignore",
    "docs/INDEX.md", "docs/authority/MASTER.md", "docs/operations/EXECUTION_PLAYBOOK.md",
    "docs/governance/KNOWLEDGE_COMPOSITION_ADDENDUM.md", "docs/governance/OWNER_COMPREHENSION_PROTOCOL.md",
    "docs/governance/DECISION_LEDGER.md", "docs/governance/RISK_REGISTER.md", "docs/governance/MINIMALITY_CHALLENGE.md",
    "docs/governance/REMAINING_OWNER_BINDINGS.md", "docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml",
    "docs/contracts/SEMANTIC_FIELD_CONTRACT.md", "docs/contracts/WORKFLOW_CONTRACT.md",
    "docs/contracts/ACCESS_CONTROL_CONTRACT.md", "docs/contracts/IMPLEMENTATION_MAPPING.yaml",
    "docs/contracts/IMPLEMENTATION_MAPPING.md", "docs/contracts/ENVIRONMENT_MANIFEST.md",
    "docs/contracts/PRIVACY_RETENTION_CONTRACT.md", "docs/validation/TEST_MATRIX.md",
    "docs/validation/DEFINITION_OF_DONE.md", "docs/validation/POC_REGISTER.md", "docs/release/RELEASE_MANIFEST.md",
    "docs/release/ROLLBACK_RUNBOOK.md", "knowledge/README.md", "knowledge/constructability/APPLICABILITY_OVERLAY.md",
    "evidence/provenance/SOURCE_MANIFEST.yaml", "runtime/README.md", "runtime/CURRENT_STATE.yaml",
    "runtime/DECISION_HISTORY.jsonl", "runtime/schemas/current-state.schema.json", "runtime/schemas/decision-event.schema.json",
    "history/pre-runtime-ssot/README.md", "history/pre-runtime-ssot/CURRENT_STATE_PRE_CUTOVER.yaml",
    "history/pre-runtime-ssot/DECISION_HISTORY_INDEX.json", "history/pre-runtime-ssot/MIGRATION_MANIFEST.json",
    *RUNTIME_CHUNKS,
    "history/pre-repository/README.md", ARCHIVE_REL, "schemas/semantic-field-contract.schema.json",
    "schemas/implementation-mapping.schema.json", "schemas/repository-manifest.schema.json",
    "scripts/materialize_archives.py", "scripts/validate_docs.py",
]


def fail(msg: str) -> None:
    ERRORS.append(msg)


def require(path: str) -> Path:
    p = ROOT / path
    if not p.exists():
        fail(f"missing required path: {path}")
    return p


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_required() -> None:
    for path in REQUIRED:
        require(path)
    for obsolete in ["runtime/snapshots/CURRENT_STATE.yaml", "runtime/snapshots/DECISION_HISTORY.md"]:
        if (ROOT / obsolete).exists():
            fail(f"obsolete parallel runtime snapshot must not exist: {obsolete}")


def field_blocks(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^\s*-\s+contract_id:\s*([^\s#]+)\s*$", text))
    out: dict[str, str] = {}
    for i, match in enumerate(matches):
        cid = match.group(1).strip('"\'')
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        if cid in out:
            fail(f"duplicate contract_id: {cid}")
        out[cid] = text[match.start():end]
    return out


def check_sfc() -> None:
    p = require("docs/contracts/SEMANTIC_FIELD_CONTRACT.yaml")
    if not p.exists(): return
    text = p.read_text(encoding="utf-8")
    if "include_in_form" not in text or "value_required" not in text:
        fail("SFC must distinguish include_in_form and value_required")
    blocks = field_blocks(text)
    invariants = {
        "HOME_PHONE": ["include_in_form: true", "value_required: false"],
        "STUDENT_FATHER_NAME": ["include_in_form: true", "value_required: true"],
        "STUDENT_MOBILE": ["include_in_form: true", "value_required: true"],
        "STUDENT_FIRST_NAME": ["value_required: true"],
        "STUDENT_LAST_NAME": ["value_required: true"],
    }
    for cid, needles in invariants.items():
        block = blocks.get(cid)
        if not block:
            fail(f"missing material field contract: {cid}")
            continue
        for needle in needles:
            if needle not in block:
                fail(f"{cid} missing invariant: {needle}")
    for key in ["qr_version", "owner_type", "owner_identifier", "iban", "bank_branch", "cheque_serial", "sayad_id"]:
        if f"machine_purpose: {key}" not in text:
            fail(f"missing hidden future Sayad field: {key}")
    if "manual_field_inventory_status: INCOMPLETE_ENUMERATION" not in text:
        fail("manual cheque inventory gap must remain explicit until bound")


def check_mapping() -> None:
    p = require("docs/contracts/IMPLEMENTATION_MAPPING.yaml")
    if not p.exists(): return
    text = p.read_text(encoding="utf-8")
    if "status: UNBOUND" in text:
        for key, value in re.findall(r"(?m)^\s*(form_id|field_id|step_id|route_or_page_id):\s*([^\s#]+)", text):
            if value not in {"null", "~"}:
                fail(f"unbound Implementation Mapping contains non-null {key}={value}")


def parse_jsonl(path: Path) -> list[dict]:
    events: list[dict] = []
    if not path.exists(): return events
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{lineno}: {exc}")
            continue
        if not isinstance(value, dict):
            fail(f"JSONL event is not object: {path.relative_to(ROOT)}:{lineno}")
            continue
        events.append(value)
    return events


def check_runtime_ssot() -> None:
    current = require("runtime/CURRENT_STATE.yaml")
    active_history = require("runtime/DECISION_HISTORY.jsonl")
    manifest_path = require("history/pre-runtime-ssot/MIGRATION_MANIFEST.json")
    index_path = require("history/pre-runtime-ssot/DECISION_HISTORY_INDEX.json")
    if not all(p.exists() for p in [current, active_history, manifest_path, index_path]): return

    current_text = current.read_text(encoding="utf-8")
    for needle in [
        "provider: GitHub", "repository: rezahh107/SRWF", "branch: main",
        "runtime_ssot_status: ACTIVE_ON_MAIN_AFTER_CUTOVER_MERGE_READBACK",
        "last_event_seq: 73", "last_event_id: OBS-20260907-REPOSITORY-RUNTIME-SSOT-CUTOVER",
    ]:
        if needle not in current_text:
            fail(f"CURRENT_STATE missing runtime SSOT invariant: {needle}")

    events = parse_jsonl(active_history)
    if not events:
        fail("active runtime DECISION_HISTORY is empty")
    else:
        seqs = [e.get("event_seq") for e in events]
        if seqs != list(range(73, 73 + len(events))):
            fail(f"active runtime event_seq not contiguous from 73: {seqs}")
        if events[-1].get("decision_id") != "OBS-20260907-REPOSITORY-RUNTIME-SSOT-CUTOVER":
            fail("CURRENT_STATE last_event_id does not match active history tail")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"runtime migration JSON invalid: {exc}")
        return

    if manifest.get("pre_cutover_event_count") != 72:
        fail("migration manifest pre_cutover_event_count must be 72")
    if manifest.get("archive_strategy") != "TEXT_NATIVE_NORMALIZED_ARCHIVE":
        fail("migration archive strategy must be TEXT_NATIVE_NORMALIZED_ARCHIVE")
    if index.get("event_count") != 72 or index.get("coverage", {}).get("contiguous") is not True:
        fail("pre-cutover decision index coverage invalid")

    index_meta = manifest.get("decision_index", {})
    if index_path.stat().st_size != index_meta.get("size"):
        fail("pre-cutover decision index size mismatch")
    if sha256_file(index_path) != index_meta.get("sha256"):
        fail("pre-cutover decision index SHA mismatch")

    all_pre_events: list[dict] = []
    chunk_meta = manifest.get("history_chunks", [])
    if len(chunk_meta) != len(RUNTIME_CHUNKS):
        fail("runtime migration chunk count mismatch")
    for meta in chunk_meta:
        rel = meta.get("path")
        p = require(rel) if isinstance(rel, str) else None
        if p is None or not p.exists(): continue
        if p.stat().st_size != meta.get("size"):
            fail(f"runtime migration chunk size mismatch: {rel}")
        if sha256_file(p) != meta.get("sha256"):
            fail(f"runtime migration chunk SHA mismatch: {rel}")
        chunk_events = parse_jsonl(p)
        all_pre_events.extend(chunk_events)
        if chunk_events:
            if chunk_events[0].get("event_seq") != meta.get("first_event_seq") or chunk_events[-1].get("event_seq") != meta.get("last_event_seq"):
                fail(f"runtime migration chunk sequence boundary mismatch: {rel}")
    pre_seqs = [e.get("event_seq") for e in all_pre_events]
    if pre_seqs != list(range(1, 73)):
        fail("pre-cutover runtime history is not exactly contiguous event_seq 1..72")

    active_paths = [
        "README.md", "AGENTS.md", "repository.manifest.yaml", "docs/INDEX.md",
        "docs/authority/MASTER.md", "docs/operations/EXECUTION_PLAYBOOK.md",
        "docs/governance/DECISION_LEDGER.md", "runtime/README.md", "runtime/CURRENT_STATE.yaml",
    ]
    stale_live_sheet_phrases = [
        "Google Sheet `SRWF_RUNTIME_STATE` remains the live operational-state SSOT",
        "Google Sheet `SRWF_RUNTIME_STATE` SSOT وضعیت اجرایی زنده است",
        "External operational state store: Google Sheet `SRWF_RUNTIME_STATE`",
        "read live `SRWF_RUNTIME_STATE`",
        "SRWF_RUNTIME_STATE_PRE_CUTOVER.xlsx",
    ]
    for rel in active_paths:
        p = require(rel)
        if not p.exists(): continue
        text = p.read_text(encoding="utf-8")
        for phrase in stale_live_sheet_phrases:
            if phrase in text:
                fail(f"stale live-Sheet pointer in active file {rel}: {phrase}")


def check_archive() -> None:
    archive = ROOT / ARCHIVE_REL
    if not archive.is_file(): return
    if archive.stat().st_size != ARCHIVE_SIZE:
        fail(f"source archive size mismatch: {archive.stat().st_size}")
        return
    actual = sha256_file(archive)
    if actual != ARCHIVE_SHA256:
        fail(f"source archive SHA mismatch: {actual}")
        return
    try:
        with tarfile.open(archive, mode="r:xz") as tf:
            members = [m for m in tf.getmembers() if m.isfile()]
            names = [m.name for m in members]
            if set(names) != set(EXPECTED_SOURCES) or len(names) != len(EXPECTED_SOURCES):
                fail(f"source archive member set mismatch: {names}")
                return
            for member in members:
                expected_size, expected_sha = EXPECTED_SOURCES[member.name]
                f = tf.extractfile(member)
                if f is None:
                    fail(f"cannot read archive member: {member.name}")
                    continue
                data = f.read()
                if len(data) != expected_size:
                    fail(f"{member.name} size mismatch: {len(data)}")
                member_sha = hashlib.sha256(data).hexdigest()
                if member_sha != expected_sha:
                    fail(f"{member.name} SHA mismatch: {member_sha}")
    except (tarfile.TarError, OSError) as exc:
        fail(f"source archive unreadable: {exc}")


def check_manifest() -> None:
    p = require("evidence/provenance/SOURCE_MANIFEST.yaml")
    if not p.exists(): return
    text = p.read_text(encoding="utf-8")
    for needle in [ARCHIVE_REL, ARCHIVE_SHA256, str(ARCHIVE_SIZE)]:
        if needle not in text:
            fail(f"SOURCE_MANIFEST missing archive invariant: {needle}")
    for name, (size, sha) in EXPECTED_SOURCES.items():
        for needle in [name, str(size), sha]:
            if needle not in text:
                fail(f"SOURCE_MANIFEST missing source invariant for {name}: {needle}")


def check_forbidden() -> None:
    fragments = ["srwf_processing_ledger", "srwf_audit_ledger", "paper_intake_images", "/pii/", "/intake/real/", "/exports/real/"]
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts: continue
        rel = "/" + str(p.relative_to(ROOT)).lower().replace("\\", "/")
        for fragment in fragments:
            if fragment in rel:
                fail(f"forbidden operational/PII path present: {rel}")


def check_master() -> None:
    p = require("docs/authority/MASTER.md")
    if not p.exists(): return
    text = p.read_text(encoding="utf-8")
    if "Gravity Forms = canonical data authority" not in text:
        fail("Master missing canonical data authority invariant")
    if "Gravity Flow = تنها workflow/assignment/formal Approval authority" not in text:
        fail("Master missing Gravity Flow workflow authority invariant")


def check_stale_pointers() -> None:
    stale = ["srwf_pre_repository_sources.tar.gz.b64", "CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt.gz"]
    for path in ["README.md", "AGENTS.md", "docs/authority/MASTER.md", "repository.manifest.yaml", "history/pre-repository/README.md"]:
        p = require(path)
        if not p.exists(): continue
        text = p.read_text(encoding="utf-8")
        for needle in stale:
            if needle in text:
                fail(f"stale active pointer in {path}: {needle}")


def main() -> int:
    check_required(); check_sfc(); check_mapping(); check_runtime_ssot(); check_archive(); check_manifest(); check_forbidden(); check_master(); check_stale_pointers()
    if ERRORS:
        print("SRWF repository integrity: FAIL")
        for error in ERRORS: print(f"- {error}")
        return 1
    print("SRWF repository integrity: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

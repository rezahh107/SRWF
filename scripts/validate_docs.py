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

PRE_RUNTIME_DIR = "history/pre-runtime-ssot"
PRE_RUNTIME_CHUNKS = [
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000001_000008.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000009_000016.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000017_000024.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000025_000032.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000033_000040.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000041_000048.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000049_000056.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000057_000064.jsonl",
    f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_000065_000072.jsonl",
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
    "evidence/provenance/SOURCE_MANIFEST.yaml",
    "runtime/README.md", "runtime/CURRENT_STATE.yaml", "runtime/DECISION_HISTORY.jsonl",
    "runtime/schemas/current-state.schema.json", "runtime/schemas/decision-event.schema.json",
    f"{PRE_RUNTIME_DIR}/README.md", f"{PRE_RUNTIME_DIR}/MIGRATION_MANIFEST.json",
    f"{PRE_RUNTIME_DIR}/CURRENT_STATE_PRE_CUTOVER.yaml", f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_INDEX.json",
    *PRE_RUNTIME_CHUNKS,
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_required() -> None:
    for path in REQUIRED:
        require(path)
    snapshots = ROOT / "runtime/snapshots"
    if snapshots.exists() and any(p.is_file() for p in snapshots.rglob("*")):
        fail("legacy runtime/snapshots files must be removed after repository runtime SSOT cutover")


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
    if not p.exists():
        return
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
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "status: UNBOUND" in text:
        for key, value in re.findall(r"(?m)^\s*(form_id|field_id|step_id|route_or_page_id):\s*([^\s#]+)", text):
            if value not in {"null", "~"}:
                fail(f"unbound Implementation Mapping contains non-null {key}={value}")


def check_runtime_ssot() -> None:
    manifest = require("repository.manifest.yaml")
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8")
        for needle in [
            "runtime_state:",
            "provider: GitHub",
            "role: LIVE_OPERATIONAL_STATE_SSOT",
            "current_state: runtime/CURRENT_STATE.yaml",
            "decision_history: runtime/DECISION_HISTORY.jsonl",
            "status_after_cutover: DEPRECATED_READ_ONLY_MIGRATION_SOURCE",
        ]:
            if needle not in text:
                fail(f"repository manifest missing runtime SSOT invariant: {needle}")
        if "external_runtime_state:" in text:
            fail("stale external_runtime_state block remains in repository manifest")

    for path in ["AGENTS.md", "README.md", "runtime/README.md", "docs/authority/MASTER.md", "docs/operations/EXECUTION_PLAYBOOK.md"]:
        p = require(path)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        if "runtime/CURRENT_STATE.yaml" not in text:
            fail(f"repository runtime current-state pointer missing in {path}")

    agents = require("AGENTS.md")
    if agents.exists():
        text = agents.read_text(encoding="utf-8")
        if "DEPRECATED_READ_ONLY_MIGRATION_SOURCE" not in text or "same accepted Git commit" not in text:
            fail("AGENTS.md missing cutover/write-integrity rules")


def parse_jsonl(path: Path) -> list[dict]:
    events: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL at {path.relative_to(ROOT)} line {i}: {exc}")
            continue
        if not isinstance(obj, dict):
            fail(f"non-object JSONL event at {path.relative_to(ROOT)} line {i}")
            continue
        events.append(obj)
    return events


def check_runtime_history() -> None:
    history = require("runtime/DECISION_HISTORY.jsonl")
    current = require("runtime/CURRENT_STATE.yaml")
    if not history.exists() or not current.exists():
        return
    events = parse_jsonl(history)
    if not events:
        fail("runtime/DECISION_HISTORY.jsonl must contain at least the cutover event")
        return
    seqs = [e.get("event_seq") for e in events]
    if not all(isinstance(x, int) for x in seqs):
        fail("active runtime history event_seq values must be integers")
        return
    expected = list(range(seqs[0], seqs[-1] + 1))
    if seqs != expected:
        fail(f"active runtime history event_seq is not contiguous: {seqs}")
    if seqs[0] != 73:
        fail(f"repository-native active history must start at event 73, got {seqs[0]}")
    ids = [e.get("decision_id") for e in events]
    if any(not isinstance(x, str) or not x for x in ids):
        fail("active runtime history contains missing decision_id")
        return
    text = current.read_text(encoding="utf-8")
    m_seq = re.search(r"(?m)^\s*last_event_seq:\s*(\d+)\s*$", text)
    m_id = re.search(r"(?m)^\s*last_event_id:\s*([^\n#]+?)\s*$", text)
    m_version = re.search(r"(?m)^state_version:\s*(\d+)\s*$", text)
    if not m_seq or not m_id or not m_version:
        fail("CURRENT_STATE missing state_version/last_event_seq/last_event_id")
        return
    if int(m_seq.group(1)) != seqs[-1]:
        fail("CURRENT_STATE last_event_seq does not match active runtime history")
    if m_id.group(1).strip('"\' ') != ids[-1]:
        fail("CURRENT_STATE last_event_id does not match active runtime history")
    if int(m_version.group(1)) < 1:
        fail("CURRENT_STATE state_version must be >= 1")


def check_pre_runtime_migration() -> None:
    manifest_path = require(f"{PRE_RUNTIME_DIR}/MIGRATION_MANIFEST.json")
    if not manifest_path.exists():
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"runtime migration manifest invalid JSON: {exc}")
        return
    if manifest.get("pre_cutover_event_count") != 72:
        fail("runtime migration manifest must record 72 pre-cutover events")
    coverage = manifest.get("coverage", {})
    if coverage != {"first_event_seq": 1, "last_event_seq": 72, "contiguous": True, "missing_event_seq": []}:
        fail(f"runtime migration coverage mismatch: {coverage}")

    declared: dict[str, tuple[int, str]] = {}
    state = manifest.get("current_state_snapshot", {})
    index = manifest.get("decision_index", {})
    for obj in [state, index, *manifest.get("history_chunks", [])]:
        path = obj.get("path")
        size = obj.get("size")
        sha = obj.get("sha256")
        if not isinstance(path, str) or not isinstance(size, int) or not isinstance(sha, str):
            fail(f"invalid runtime migration manifest file record: {obj}")
            continue
        declared[path] = (size, sha)

    for rel, (size, sha) in declared.items():
        p = require(rel)
        if not p.exists():
            continue
        if p.stat().st_size != size:
            fail(f"pre-runtime migration size mismatch for {rel}: {p.stat().st_size} != {size}")
        actual = sha256_file(p)
        if actual != sha:
            fail(f"pre-runtime migration SHA mismatch for {rel}: {actual}")

    events: list[dict] = []
    for rel in PRE_RUNTIME_CHUNKS:
        p = require(rel)
        if p.exists():
            events.extend(parse_jsonl(p))
    seqs = [e.get("event_seq") for e in events]
    if seqs != list(range(1, 73)):
        fail(f"pre-cutover event coverage must be exact 1..72, got {seqs[:3]}...{seqs[-3:] if seqs else []}")
    for e in events:
        source = e.get("source", {})
        if source.get("kind") != "GOOGLE_SHEET_PRE_CUTOVER":
            fail(f"pre-cutover event {e.get('event_seq')} missing source provenance")

    index_path = require(f"{PRE_RUNTIME_DIR}/DECISION_HISTORY_INDEX.json")
    if index_path.exists():
        try:
            idx = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"pre-cutover decision index invalid JSON: {exc}")
        else:
            idx_events = idx.get("events", [])
            if idx.get("event_count") != 72 or [x.get("event_seq") for x in idx_events] != list(range(1, 73)):
                fail("pre-cutover decision index must cover event_seq 1..72 exactly")


def check_archive() -> None:
    archive = ROOT / ARCHIVE_REL
    if not archive.is_file():
        return
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
    if not p.exists():
        return
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
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = "/" + str(p.relative_to(ROOT)).lower().replace("\\", "/")
        for fragment in fragments:
            if fragment in rel:
                fail(f"forbidden operational/PII path present: {rel}")


def check_master() -> None:
    p = require("docs/authority/MASTER.md")
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "Gravity Forms = canonical data authority" not in text:
        fail("Master missing canonical data authority invariant")
    if "Gravity Flow = تنها workflow/assignment/formal Approval authority" not in text:
        fail("Master missing Gravity Flow workflow authority invariant")
    if "runtime/CURRENT_STATE.yaml" not in text or "OWNER-20260907-REPOSITORY-RUNTIME-SSOT" not in text:
        fail("Master missing repository runtime SSOT boundary")


def check_stale_pointers() -> None:
    stale = [
        "srwf_pre_repository_sources.tar.gz.b64",
        "CONSTRUCTABILITY_RUNTIME_KNOWLEDGE.txt.gz",
        "SRWF_RUNTIME_STATE_PRE_CUTOVER.xlsx",
    ]
    active = [
        "README.md", "AGENTS.md", "docs/INDEX.md", "docs/authority/MASTER.md",
        "docs/operations/EXECUTION_PLAYBOOK.md", "docs/governance/DECISION_LEDGER.md",
        "repository.manifest.yaml", "runtime/README.md", "history/pre-runtime-ssot/README.md",
    ]
    for path in active:
        p = require(path)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for needle in stale:
            if needle in text:
                fail(f"stale active pointer in {path}: {needle}")

    forbidden_live_sheet_phrases = [
        "Google Sheet `SRWF_RUNTIME_STATE` remains the live operational-state SSOT",
        "Google Sheet `SRWF_RUNTIME_STATE` is the live operational-state SSOT",
        "External operational state store: Google Sheet `SRWF_RUNTIME_STATE`",
        "read live `SRWF_RUNTIME_STATE`",
    ]
    for path in active:
        p = ROOT / path
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for needle in forbidden_live_sheet_phrases:
            if needle in text:
                fail(f"stale Google Sheet live-SSOT statement in {path}: {needle}")


def main() -> int:
    check_required()
    check_sfc()
    check_mapping()
    check_runtime_ssot()
    check_runtime_history()
    check_pre_runtime_migration()
    check_archive()
    check_manifest()
    check_forbidden()
    check_master()
    check_stale_pointers()
    if ERRORS:
        print("SRWF repository integrity: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("SRWF repository integrity: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

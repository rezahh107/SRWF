#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
FIXED_ZIP_DT = (2026, 1, 1, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: str) -> bytes:
    p = ROOT / path
    if not p.is_file():
        raise SystemExit(f"Missing required source: {path}")
    return p.read_bytes()


def source_commit() -> str:
    env = os.getenv("GITHUB_SHA")
    if env:
        return env
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "UNKNOWN"


def parse_scalar(text: str, key: str) -> str | None:
    m = re.search(rf"(?m)^\s*{re.escape(key)}:\s*['\"]?([^'\"\n]+)", text)
    return m.group(1).strip() if m else None


def artifact_refs(history_text: str) -> list[dict]:
    refs: dict[str, dict] = {}
    for line in history_text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        hashes = ((event.get("source") or {}).get("artifact_sha256") or {})
        if not isinstance(hashes, dict):
            continue
        for name, digest in hashes.items():
            refs[name] = {
                "name": name,
                "sha256": digest,
                "source_event_seq": event.get("event_seq"),
                "source_event_id": event.get("decision_id"),
                "status": "REFERENCED_NOT_EMBEDDED",
            }
    return [refs[k] for k in sorted(refs)]


def find_exact_repo_artifact(name: str, digest: str) -> Path | None:
    excluded_parts = {".git", "dist", ".knowledge-materialized"}
    for p in ROOT.rglob(name):
        if any(part in excluded_parts for part in p.parts):
            continue
        if p.is_file() and sha256(p.read_bytes()) == digest:
            return p
    return None


def add_entry(entries: dict[str, tuple[bytes, str, str]], dest: str, data: bytes, classification: str, source: str) -> None:
    dest = dest.replace("\\", "/").lstrip("/")
    if ".." in Path(dest).parts:
        raise SystemExit(f"Unsafe package path: {dest}")
    if dest in entries:
        raise SystemExit(f"Duplicate package path: {dest}")
    entries[dest] = (data, classification, source)


def make_zip(path: Path, entries: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, FIXED_ZIP_DT)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, entries[name])


def validate_zip(zip_path: Path, manifest: dict) -> dict:
    expected = {f["path"]: f for f in manifest["files"]}
    errors: list[str] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        if names != sorted(names):
            errors.append("ZIP entries are not sorted")
        if len(names) != len(set(names)):
            errors.append("ZIP contains duplicate paths")
        for name in names:
            if name.startswith("/") or ".." in Path(name).parts:
                errors.append(f"unsafe ZIP path: {name}")
        for name, meta in expected.items():
            if name not in names:
                errors.append(f"missing payload: {name}")
                continue
            data = zf.read(name)
            if len(data) != meta["size"] or sha256(data) != meta["sha256"]:
                errors.append(f"hash/size mismatch: {name}")
        instructions = zf.read("02_PROJECT_INSTRUCTIONS.md").decode("utf-8")
        if len(instructions) > 8000:
            errors.append(f"02_PROJECT_INSTRUCTIONS.md exceeds 8000 chars: {len(instructions)}")
        for phrase in ["GitHub", "runtime/CURRENT_STATE.yaml", "DEPRECATED_READ_ONLY_MIGRATION_SOURCE"]:
            if phrase not in instructions:
                errors.append(f"instructions missing runtime SSOT phrase: {phrase}")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def main() -> int:
    cfg = json.loads(read("bundle/project-package.json").decode("utf-8"))
    version = read("bundle/VERSION").decode("utf-8").strip()
    commit = source_commit()
    entries: dict[str, tuple[bytes, str, str]] = {}

    add_entry(entries, "00_README.md", read("bundle/00_README.md"), "PACKAGE_GUIDE", "bundle/00_README.md")
    add_entry(entries, "02_PROJECT_INSTRUCTIONS.md", read("bundle/02_PROJECT_INSTRUCTIONS.md"), "PROJECT_INSTRUCTIONS", "bundle/02_PROJECT_INSTRUCTIONS.md")
    add_entry(entries, "03_INSTALLATION_AND_BOOT.md", read("bundle/03_INSTALLATION_AND_BOOT.md"), "PACKAGE_GUIDE", "bundle/03_INSTALLATION_AND_BOOT.md")
    add_entry(entries, "04_PACKAGE_CHANGELOG.md", read("bundle/04_PACKAGE_CHANGELOG.md"), "PACKAGE_CHANGELOG", "bundle/04_PACKAGE_CHANGELOG.md")

    for src, dest in cfg["canonical_source_mappings"].items():
        add_entry(entries, dest, read(src), "CURRENT_REPOSITORY_SOURCE", src)

    archive_rel = "history/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz"
    archive = ROOT / archive_rel
    if not archive.is_file():
        raise SystemExit(f"Missing provenance archive: {archive_rel}")
    add_entry(entries, "HISTORY/pre-repository/SRWF_PRE_REPOSITORY_SOURCES_01_11.tar.xz", archive.read_bytes(), "HISTORICAL_PROVENANCE", archive_rel)

    wanted = cfg["materialized_knowledge_sources"]
    with tarfile.open(archive, "r:xz") as tf:
        members = {m.name: m for m in tf.getmembers() if m.isfile()}
        for member_name, dest in wanted.items():
            if member_name not in members:
                raise SystemExit(f"Knowledge source missing from archive: {member_name}")
            f = tf.extractfile(members[member_name])
            if f is None:
                raise SystemExit(f"Cannot extract: {member_name}")
            add_entry(entries, dest, f.read(), "REFERENCE_PRODUCT_KNOWLEDGE", f"{archive_rel}::{member_name}")

    if cfg.get("include_pre_cutover_history"):
        hist_root = ROOT / "history/pre-runtime-ssot"
        for p in sorted(hist_root.rglob("*")):
            if p.is_file():
                rel = p.relative_to(ROOT).as_posix()
                add_entry(entries, f"HISTORY/{rel}", p.read_bytes(), "HISTORICAL_RUNTIME_PROVENANCE", rel)

    history_text = read("runtime/DECISION_HISTORY.jsonl").decode("utf-8")
    refs = artifact_refs(history_text)
    for ref in refs:
        p = find_exact_repo_artifact(ref["name"], ref["sha256"])
        if p is not None:
            dest = f"ARTIFACTS/{ref['name']}"
            rel = p.relative_to(ROOT).as_posix()
            add_entry(entries, dest, p.read_bytes(), "EXACT_ARTIFACT", rel)
            ref["status"] = "EMBEDDED_EXACT_HASH_MATCH"
            ref["package_path"] = dest
            ref["repository_path"] = rel
    refs_bytes = (json.dumps({"schema_version": 1, "artifacts": refs}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    add_entry(entries, "ARTIFACT_REFERENCES.json", refs_bytes, "ARTIFACT_REFERENCE_INDEX", "runtime/DECISION_HISTORY.jsonl")

    state_text = read("runtime/CURRENT_STATE.yaml").decode("utf-8")
    state_version = parse_scalar(state_text, "state_version")
    last_event_seq = parse_scalar(state_text, "last_event_seq")
    next_action_id = parse_scalar(state_text, "next_action_id")

    payload_meta = []
    for name in sorted(entries):
        data, classification, source = entries[name]
        payload_meta.append({"path": name, "size": len(data), "sha256": sha256(data), "classification": classification, "source": source})

    checksums = "".join(f"{m['sha256']}  {m['path']}\n" for m in payload_meta).encode("utf-8")
    add_entry(entries, "CHECKSUMS.sha256", checksums, "PACKAGE_CHECKSUM_INDEX", "GENERATED")

    manifest = {
        "schema_version": 1,
        "package": {
            "name": cfg["package_name"],
            "version": version,
            "builder_profile": cfg["builder_profile"],
            "formal_package_maker_5_spec_status": cfg["formal_package_maker_5_spec_status"],
            "authority": "PORTABLE_SNAPSHOT_NON_CANONICAL_WHEN_REPOSITORY_AVAILABLE"
        },
        "source": {
            "repository": "rezahh107/SRWF",
            "branch": os.getenv("GITHUB_REF_NAME", "UNKNOWN"),
            "commit": commit,
            "runtime_state_version": state_version,
            "runtime_last_event_seq": last_event_seq,
            "runtime_next_action_id": next_action_id
        },
        "rules": {
            "live_ssot": "GitHub main",
            "bundle_state": "BUILD_TIME_FALLBACK_ONLY",
            "google_sheet": "DEPRECATED_READ_ONLY_MIGRATION_SOURCE",
            "real_pii": "FORBIDDEN"
        },
        "files": payload_meta,
        "artifact_reference_count": len(refs),
        "artifact_embedded_count": sum(1 for r in refs if r["status"].startswith("EMBEDDED"))
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    add_entry(entries, "01_PACKAGE_MANIFEST.json", manifest_bytes, "PACKAGE_MANIFEST", "GENERATED")

    zip_entries = {name: data for name, (data, _, _) in entries.items()}
    output = DIST / f"SRWF_GPT_Project_Package_v{version}.zip"
    make_zip(output, zip_entries)
    validation = validate_zip(output, manifest)
    validation.update({
        "package": output.name,
        "source_commit": commit,
        "runtime_state_version": state_version,
        "runtime_last_event_seq": last_event_seq,
        "file_count": len(zip_entries)
    })
    validation_bytes = (json.dumps(validation, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    zip_entries["PACKAGE_VALIDATION.json"] = validation_bytes
    make_zip(output, zip_entries)
    final_sha = sha256(output.read_bytes())
    sha_path = DIST / f"{output.name}.sha256"
    sha_path.write_text(f"{final_sha}  {output.name}\n", encoding="utf-8")

    with zipfile.ZipFile(output, "r") as zf:
        required = {"00_README.md", "01_PACKAGE_MANIFEST.json", "02_PROJECT_INSTRUCTIONS.md", "CHECKSUMS.sha256", "PACKAGE_VALIDATION.json"}
        missing = required.difference(zf.namelist())
        if missing:
            raise SystemExit(f"Final ZIP missing: {sorted(missing)}")

    print(json.dumps({
        "status": validation["status"],
        "output": str(output.relative_to(ROOT)),
        "sha256": final_sha,
        "files": len(zip_entries),
        "state_version": state_version,
        "last_event_seq": last_event_seq,
        "referenced_artifacts": len(refs),
        "embedded_artifacts": sum(1 for r in refs if r["status"].startswith("EMBEDDED")),
        "validation_errors": validation["errors"]
    }, ensure_ascii=False))
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

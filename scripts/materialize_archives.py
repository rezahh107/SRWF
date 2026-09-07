#!/usr/bin/env python3
"""Materialize the byte-exact pre-repository SRWF source corpus.

The repository stores one binary XZ-compressed tar archive for provenance.
This script does not fetch network data and does not modify canonical docs.
"""
from __future__ import annotations

import hashlib
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "history" / "pre-repository"
ARCHIVE = HISTORY / "srwf_pre_repository_sources.tar.xz"
OUT = ROOT / ".knowledge-materialized" / "pre-repository"
EXPECTED_ARCHIVE_SHA256 = "82b0201ce3920214fe2ac7b9bd7defaa8769651fbbd1168abcd0a1ba91d32ed4"


def main() -> int:
    if not ARCHIVE.is_file():
        raise SystemExit(f"Source archive missing: {ARCHIVE.relative_to(ROOT)}")

    raw = ARCHIVE.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_ARCHIVE_SHA256:
        raise SystemExit(
            f"Archive SHA-256 mismatch: expected {EXPECTED_ARCHIVE_SHA256}, got {actual}"
        )

    OUT.mkdir(parents=True, exist_ok=True)
    with tarfile.open(ARCHIVE, mode="r:xz") as tf:
        root = OUT.resolve()
        for member in tf.getmembers():
            target = (OUT / member.name).resolve()
            if root != target and root not in target.parents:
                raise SystemExit(f"Unsafe archive member: {member.name}")
        tf.extractall(OUT)

    print(f"Materialized source corpus to {OUT}")
    print(f"archive_sha256={actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

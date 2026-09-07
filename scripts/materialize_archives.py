#!/usr/bin/env python3
"""Materialize the byte-exact pre-repository SRWF source corpus.

The archive is committed as split base64 text parts to keep Git transport simple.
This script does not fetch network data and does not modify canonical docs.
"""
from __future__ import annotations

import base64
import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "history" / "pre-repository"
OUT = ROOT / ".knowledge-materialized" / "pre-repository"
EXPECTED_ARCHIVE_SHA256 = "d3aa23753aabae2db95381e57c5050c5d0429865c94b9c1a15b5e0b0d3eb27a8"
PART_GLOB = "srwf_pre_repository_sources.tar.gz.b64.part*"


def main() -> int:
    parts = sorted(HISTORY.glob(PART_GLOB))
    if not parts:
        raise SystemExit("No archive parts found. Repository source corpus is incomplete.")

    encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    try:
        archive = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f"Archive base64 decode failed: {exc}") from exc

    actual = hashlib.sha256(archive).hexdigest()
    if actual != EXPECTED_ARCHIVE_SHA256:
        raise SystemExit(
            f"Archive SHA-256 mismatch: expected {EXPECTED_ARCHIVE_SHA256}, got {actual}"
        )

    OUT.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
        # Refuse path traversal even for repository-owned archives.
        root = OUT.resolve()
        for member in tf.getmembers():
            target = (OUT / member.name).resolve()
            if root != target and root not in target.parents:
                raise SystemExit(f"Unsafe archive member: {member.name}")
        tf.extractall(OUT)

    print(f"Materialized {len(parts)} parts to {OUT}")
    print(f"archive_sha256={actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fail closed unless the provisional scaffold materializes locked student-photo settings."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    print(f"SRWF scaffold photo-settings assertion failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: assert-scaffold-photo-settings.py <scaffold.json>")

    path = Path(sys.argv[1])
    try:
        root: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid scaffold JSON: {exc}")

    if not isinstance(root, dict):
        fail("scaffold root must be an object")

    forms = [value for key, value in root.items() if key != "version" and isinstance(value, dict)]
    if len(forms) != 1:
        fail(f"expected exactly one form, found {len(forms)}")

    fields = forms[0].get("fields")
    if not isinstance(fields, list):
        fail("form fields are missing")

    photos = [field for field in fields if isinstance(field, dict) and field.get("adminLabel") == "student_photo"]
    if len(photos) != 1:
        fail(f"expected exactly one student_photo field, found {len(photos)}")

    field = photos[0]
    failures: list[str] = []

    expected = {
        "gpfupEnable": True,
        "gpfupEnableCrop": True,
        "gpfupCropRequired": True,
        "gpfupAspectRatioAntecedent": 3,
        "gpfupAspectRatioConsequent": 4,
        "gpfupMaxWidth": 1200,
        "gpfupMaxHeight": 1600,
        "multipleFiles": True,
    }
    for key, value in expected.items():
        if field.get(key) != value:
            failures.append(f"{key}:expected={value!r}:actual={field.get(key)!r}")

    if str(field.get("maxFiles")) != "1":
        failures.append(f"maxFiles:expected='1':actual={field.get('maxFiles')!r}")
    if str(field.get("maxFileSize")) != "5":
        failures.append(f"maxFileSize:expected='5':actual={field.get('maxFileSize')!r}")

    extensions = [part.strip().lower() for part in str(field.get("allowedExtensions", "")).split(",") if part.strip()]
    if extensions != ["jpg", "jpeg"]:
        failures.append(f"allowedExtensions:expected=['jpg','jpeg']:actual={extensions!r}")

    for key in ("gpfupMinWidth", "gpfupMinHeight", "gpfupExactWidth", "gpfupExactHeight"):
        if key in field and field.get(key) not in (None, ""):
            failures.append(f"{key}:must_be_unset:actual={field.get(key)!r}")

    if failures:
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        fail("locked student_photo profile mismatch")

    print(
        "SRWF_SCAFFOLD_PHOTO_SETTINGS_PASS "
        "ratio=3:4 max=1200x1600 min=unset files=1 types=jpg,jpeg max_mb=5"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the duplicate_key_rejection_v1 fixture corpus.

The fixture intentionally exercises input validity before RFC 8785/JCS
canonicalization. Every case must be rejected before canonical bytes, hashes, or
signatures are produced.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "duplicate_key_rejection_v1"
MANIFEST = FIXTURE_DIR / "manifest.json"


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains duplicate property names."""


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    seen: set[str] = set()
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in seen:
            raise DuplicateKeyError(key)
        seen.add(key)
        result[key] = value
    return result


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "duplicate-key-rejection/v1"

    cases = manifest["cases"]
    assert cases, "manifest must declare at least one duplicate-key case"

    for case in cases:
        assert case["expect"] == "reject-before-canonicalization"
        source = (FIXTURE_DIR / case["file"]).read_text(encoding="utf-8")
        try:
            json.loads(source, object_pairs_hook=reject_duplicate_keys)
        except DuplicateKeyError:
            continue
        raise AssertionError(f"{case['id']} did not reject duplicate keys")


if __name__ == "__main__":
    main()

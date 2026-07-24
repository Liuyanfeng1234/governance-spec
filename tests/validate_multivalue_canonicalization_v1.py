#!/usr/bin/env python3
"""Validate the multivalue_canonicalization_v1 fixture corpus.

The corpus pins how a multi-value field becomes bytes so that a
content-addressed reference does not fork between two honest emitters. Every
case is recomputed here from its inputs; nothing is trusted on assertion.

Canonicalization note: the corpus uses only ASCII strings and arrays, no
numbers and no non-ASCII, so RFC 8785 canonical bytes coincide with
``json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)``.
A full JCS implementation is unnecessary to demonstrate the invariant.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "multivalue_canonicalization_v1"
MANIFEST = FIXTURE_DIR / "manifest.json"


class SeparatorError(ValueError):
    """Raised when a string-by-contract token smuggles a separator character."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_token(token: str, separators: list[str]) -> None:
    for sep in separators:
        if sep in token:
            raise SeparatorError(token)


def load_case(case: dict) -> dict:
    return json.loads((FIXTURE_DIR / case["file"]).read_text(encoding="utf-8"))


def check_order_is_semantic(data: dict) -> None:
    # Order is load-bearing: reordering the array must fork the digest.
    assert digest(data["input_a"]) != digest(data["input_b"])


def check_set_normalized(data: dict) -> None:
    field = data["field"]
    a, b = dict(data["input_a"]), dict(data["input_b"])
    # Without normalization the two input orders would already fork...
    assert digest(a) != digest(b)
    # ...and sorting the set before building the object collapses them to one.
    a[field] = sorted(a[field])
    b[field] = sorted(b[field])
    assert digest(a) == digest(b)


def check_string_join_collision(data: dict) -> None:
    field, sep = data["field"], data["separator"]
    x, y = data["list_x"], data["list_y"]
    # The join collides two distinct lists into identical bytes...
    assert sep.join(x) == sep.join(y)
    # ...while the array form keeps them distinct under canonicalization.
    assert digest({field: x}) != digest({field: y})


def check_scope_separator_rejection(data: dict) -> None:
    separators = data["separators"]
    # Honest tokens carry no separator and pass validation.
    for token in ("PII_BLOCKED", "US_SSN", "PHONE"):
        validate_token(token, separators)
    # The forged entity smuggles a separator and is rejected before canonicalization.
    try:
        validate_token(data["forged_entity"], separators)
    except SeparatorError:
        return
    raise AssertionError("forged entity was not rejected before canonicalization")


CHECKS = {
    "distinct-digests": check_order_is_semantic,
    "equal-digests-after-set-normalization": check_set_normalized,
    "join-collides-array-distinguishes": check_string_join_collision,
    "reject-before-canonicalization": check_scope_separator_rejection,
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "multivalue-canonicalization/v1"

    cases = manifest["cases"]
    assert cases, "manifest must declare at least one case"

    for case in cases:
        check = CHECKS[case["expect"]]
        check(load_case(case))
        print(f"ok  {case['id']}: {case['expect']}")

    print(f"\n{len(cases)} cases passed")


if __name__ == "__main__":
    main()

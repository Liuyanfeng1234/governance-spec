# duplicate_key_rejection_v1

This fixture corpus covers JSON input-validity failures that must be rejected
before RFC 8785/JCS canonicalization.

RFC 8785 section 3.1 says JSON objects used as input data must not exhibit
duplicate property names. A verifier should therefore reject these inputs and
emit no canonical bytes, digest, admission hash, anchoring hash, or signature.

This corpus is intentionally separate from byte-level JCS canonicalization
fixtures such as `jcs_edge_v1`: canonicalization fixtures test how valid input
is serialized, while this corpus tests whether invalid input is refused before
serialization.

## Cases

| ID | File | Boundary |
| --- | --- | --- |
| `direct_duplicate` | `cases/direct_duplicate.json` | Two literal property names match in the same object. |
| `escaped_equivalent_duplicate` | `cases/escaped_equivalent_duplicate.json` | A literal name and an escaped-equivalent name decode to the same property name. |
| `nested_duplicate` | `cases/nested_duplicate.json` | A nested object contains duplicate property names. |
| `array_nested_duplicate` | `cases/array_nested_duplicate.json` | An object inside an array contains duplicate property names. |
| `escaped_solidus_duplicate` | `cases/escaped_solidus_duplicate.json` | `/` and `\/` decode to the same property name. |

Run:

```bash
python tests/validate_duplicate_key_rejection_v1.py
```

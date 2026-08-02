# multivalue_canonicalization_v1

This fixture corpus pins how a multi-value field becomes bytes, so a
content-addressed reference does not fork between two honest emitters.

A JCS / RFC 8785 pin closes byte-determinism for scalar fields. It leaves
multi-value fields open: two emitters that agree on every value but order it
differently produce different canonical bytes, and a content address that
should match forks with nobody lying. The rule this corpus exercises: a
structured multi-value field is a JSON array with per-field semantics pinned
(order-is-semantic or set); it is never string-joined. A field that is a string
by contract closes separator collision by validation, a strictly weaker
guarantee named as such.

This corpus is separate from byte-level canonicalization fixtures such as
`jcs_edge_v1`: those test how a valid scalar payload serializes, while this
tests how a multi-value field must be shaped before it serializes.

## Cases

| ID | File | Boundary |
| --- | --- | --- |
| `order_is_semantic` | `cases/order_is_semantic.json` | Order is load-bearing, so reordering the array forks the digest. |
| `set_normalized` | `cases/set_normalized.json` | A set is sorted before the object is built, so two input orders recompute to one digest. |
| `string_join_collision` | `cases/string_join_collision.json` | Two distinct lists join to the same string but canonicalize to distinct array bytes. |
| `scope_separator_rejection` | `cases/scope_separator_rejection.json` | A string-by-contract field rejects a separator inside a value before canonicalization. |

Run:

```bash
python tests/validate_multivalue_canonicalization_v1.py
```

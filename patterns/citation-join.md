# The citation-join pattern

Compliance does not compose. A stack of independently-valid layers does not add up to a compliance guarantee; a payment proof, an action receipt, and a policy verdict can each verify and still describe three unrelated events. The join that holds them together does not merge them, it cites: each layer keeps its own integrity boundary and points at the others by content address, so a verifier checks any one alone or all of them together without one proof having to trust another.

This doc states the invariants that make a citation join sound, then closes the one edge the first four leave open.

## The four base invariants

Multiple independent frameworks on the AutoGen AAR thread (`microsoft/autogen#7353`) converged on the same four, without coordinating beforehand: governance-spec (`@Liuyanfeng1234`), the pre-action governance conformance suite (`@babyblueviper1`), argentum-core (`@giskard09`), and CKG (`@Yarmoluk`), all anchored to the shared `jcs-rfc8785-v1` canonicalization substrate (`@chopmob-cloud`). Stated as `@Liuyanfeng1234` enumerated them:

1. **Content-addressed**: the digest is computed before the citing party knows the outcome.
2. **Independently recomputable**: the digest re-derives from canonical bytes without touching the other system's state.
3. **Citation, not merge**: the reference field points at evidence in another layer; it does not embed that layer's semantics.
4. **Fail-closed on both sides**: if the digest does not recompute, or the reference resolves to nothing, the verifier rejects.

The four hold the join together for *scalar* payloads. They leave one edge open, and it is the edge that forks a content address between two honest emitters.

## Invariant 5: multi-value canonicalization

This is not a separate concern, it is the same argument one level deeper. Citation-not-merge only holds if the thing being cited is a deterministic address, and a multi-value field is exactly where that determinism can break even when every layer above it is correct.

A canonicalization pin (JCS, RFC 8785) closes byte-determinism for scalar fields and stops there. Feed it a multi-value field, a list of entities or a signer set or a typed evidence array, and two emitters that agree on every value but order it differently produce different bytes. The signatures are valid, the recompute is honest, and the two refs still don't match. The join breaks not because someone lied but because the pattern never said how a list becomes bytes.

The rule that closes it:

> A structured multi-value field is a JSON array with per-field semantics pinned; it is never string-joined.

RFC 8785 canonicalizes arrays without reordering them: object keys sort, array elements stay in the order given. So the array *is* the grammar, and the only decision left is what the order means:

- **order-is-semantic**: preserve the caller's order and make it load-bearing. A different order is a different assertion, and the address forking is the honest outcome, not a bug.
- **it's a set**: sort the elements before building the object, still as array items.

String-joining a structured field re-opens exactly what JCS closed: separator collision, lost typing, no nesting. `["a,b", "c"]` and `["a", "b,c"]` join to the same `"a,b,c"` and collide; as arrays they canonicalize to distinct bytes and stay distinct. The comma-join is correct in one case only, where the field was a string before you reached it, a string by contract across every published vector, and promoting it to an array would fork the preimage shape and every ref already signed against it. There the array fix is unavailable, and you close separator collision by validation instead: the parser rejects the separator characters inside each value.

State that asymmetry plainly rather than round it up. An array puts the grammar in the parser, so a malformed list cannot canonicalize. Validation-on-a-string is a parser-checks-the-grammar guarantee: a compliant emitter is safe, a buggy one that skips validation could still forge a colliding value. It is the strongest close available inside a fixed string field, and it is strictly weaker than making the field an array. If you can choose the field shape, choose the array.

## Conformance

`fixtures/multivalue_canonicalization_v1` exercises the fifth invariant with recomputable evidence, in the same shape as `duplicate_key_rejection_v1`:

- `order_is_semantic`: reordering a load-bearing array forks the digest (the fork is honest).
- `set_normalized`: a set sorted before the object is built recomputes to one digest regardless of input order.
- `string_join_collision`: a join collides two distinct lists; the array form keeps them distinct.
- `scope_separator_rejection`: a string-by-contract field rejects separator characters before canonicalization, the weaker close named as such.

Run: `python tests/validate_multivalue_canonicalization_v1.py`

## Reference implementation

`presidio-x402` ships the fifth invariant in production. Typed multi-value data that rides outside the flat preimage stays a JSON array with order-vs-set pinned per field; the one string-by-contract field (`action_ref.scope`) closes collision by validation, documented as the weaker guarantee it is.

- Merged conformance vector: `giskard09/argentum-core` at `examples/conformance/presidio/presidio-x402-decision-ref-v1.fixture.json` (PR #29), recompute-graded cross-language.
- Normative rule origin: the entity-segment exchange, argentum-core `action-ref.md` (`16dbc92`), corrected from comma-join to array-with-pinned-semantics.
- Extended rationale: Stantchev, *Computational Jurisprudence: Verifiable Law for Machine Societies*, Preprints 2026, [doi:10.20944/preprints202607.1528.v1](https://doi.org/10.20944/preprints202607.1528.v1).

Cite the fifth invariant the same way the other four are cited, by digest, recomputable on your side, no trust in ours required.

# Proposal: `v19.canonical_envelope.interop/1`

Status: **draft, synthetic interoperability only**. This is a new proposal, not a description of an existing V19 implementation. It cannot authorize any operation; a correct digest is not a signature, human approval, or an execution grant.

## Object

The top-level JSON object has exactly three case-sensitive members:

- `schema`: the exact string `v19.canonical_envelope.interop/1`.
- `profile`: the exact string `synthetic-interop/1`.
- `payload`: a JSON object of synthetic, non-sensitive test values with no authority semantics.

Missing, extra, or duplicate top-level members are rejected. Any decoded duplicate member name in a nested object is also rejected. Unknown versions or profiles are rejected. `payload` may be empty; its arbitrary member names and values are test data only, even if they spell `allow`, `issuer`, or `signature`.

## Input validation

Input is UTF-8 JSON without BOM, at most 16,384 bytes before parsing. Reject malformed UTF-8, duplicate decoded member names at every object level, invalid Unicode including lone surrogates, non-finite numbers, and values outside the I-JSON constraints required by [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html). Strings must not be Unicode-normalized or otherwise changed. Parse JSON numbers as IEEE 754 binary64 before canonicalization; an implementation that cannot ensure this and duplicate-key rejection must fail closed. The `payload` container depth is at most 16 (`payload` itself is depth 1; each child object or array increments it); any object has at most 128 members. These size/depth limits are proposed profile rules, not claims about RFC 8785.

## Canonical bytes and digest

After validation, canonicalize the **entire** three-member object according to RFC 8785: ECMAScript primitive serialization, required short escapes for JSON controls, recursive UTF-16 code-unit property ordering, and UTF-8 output. `canonical_bytes` is exactly that UTF-8 output. The detached digest is `SHA-256(canonical_bytes)`, represented as 64 lowercase hexadecimal characters. Both `schema` and `profile` are included in the hash input; no hidden prefix or excluded member is permitted.

The digest, signature, key identity, review decision, and publication status are external evidence, never authoritative fields inside this proposed object. A verifier must repeat validation and canonicalization before comparing a supplied digest. This profile defines no real governance-block fields, issuer trust, revocation, time anchoring, signature verification, or execution gateway. Adding any of those requires a separately reviewed, versioned contract.

## Candidate vector interpretation

`vectors.json` stores raw JSON input as a JSON string: decode `input_json_text` from the vector file, then UTF-8 encode its characters to obtain the candidate input bytes. For positive cases, compare the JCS UTF-8 bytes to `canonical_utf8_hex` and SHA-256 to `sha256_hex`. For negative cases, reject for the named contract reason **before** returning a digest. The file is a local review candidate, not an approved or independently held conformance suite. Contract adoption, publication, and external verification require separate decisions.

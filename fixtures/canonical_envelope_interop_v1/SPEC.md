# Proposal: `v19.canonical_envelope.interop/1` — artifact revision r2

Status: draft, synthetic interoperability only; local correction candidate, not published or adopted. This is not a description of an existing V19 implementation. A correct digest is not a signature, human approval, or execution grant.

## Object

The top-level JSON object has exactly three case-sensitive members:

- `schema`: the exact string `v19.canonical_envelope.interop/1`.
- `profile`: the exact string `synthetic-interop/1`.
- `payload`: a JSON object of synthetic, non-sensitive test values with no authority semantics.

Missing, extra, or duplicate top-level members are rejected. Any decoded duplicate member name in a nested object is also rejected. Unknown versions or profiles are rejected. `payload` may be empty; its arbitrary member names and values are test data only, even if they spell `allow`, `issuer`, or `signature`.

## Input validation

Input is UTF-8 JSON without BOM, at most 16,384 bytes before parsing. Reject malformed UTF-8, duplicate decoded member names at every object level, invalid Unicode including lone surrogates, non-finite numbers, and values outside the I-JSON constraints required by [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html). Strings must not be Unicode-normalized or otherwise changed.

Specifically, decoded member names and string values must not contain Unicode noncharacters, as required by [RFC 7493 §2.1](https://www.rfc-editor.org/rfc/rfc7493.html#section-2.1), whether encoded directly or escaped. U+FFFF is a noncharacter: its Unicode encoding is not inherently malformed, but it is outside this profile's I-JSON input domain. The r2 diagnostic `REJECT_IJSON_NONCHARACTER` names this contract expectation; it is not an RFC-mandated literal exception string or a measured implementation result.

Lone surrogates must cause a compliant JCS implementation to terminate with an appropriate error under [RFC 8785 §3.2.2.2](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.2.2.2). A validation wrapper may enforce this before a canonicalization core, but the complete implementation must reject the input. The existing N4 expectation is unchanged; no concrete package behavior has been independently reproduced here.

Parse JSON numbers as IEEE 754 binary64 before canonicalization; an implementation that cannot ensure this and duplicate-key rejection must fail closed. The `payload` container depth is at most 16 (`payload` itself is depth 1; each child object or array increments it); any object has at most 128 members. These size/depth limits are proposed profile rules, not claims about RFC 8785.

## Canonical bytes and digest

After validation, canonicalize the entire three-member object according to RFC 8785: ECMAScript primitive serialization, required short escapes for JSON controls, recursive UTF-16 code-unit property ordering, and UTF-8 output. `canonical_bytes` is exactly that UTF-8 output. The detached digest is `SHA-256(canonical_bytes)`, represented as 64 lowercase hexadecimal characters. Both `schema` and `profile` are included in the hash input; no hidden prefix or excluded member is permitted.

The digest, signature, key identity, review decision, and publication status are external evidence, never authoritative fields inside this proposed object. A verifier must repeat validation and canonicalization before comparing a supplied digest. This profile defines no real governance-block fields, issuer trust, revocation, time anchoring, signature verification, or execution gateway. Adding any of those requires a separately reviewed, versioned contract.

## Candidate vector interpretation

`vectors.json` stores raw JSON input as a JSON string: decode `input_json_text` from the vector file, then UTF-8 encode its characters to obtain the candidate input bytes. Do not add a newline, normalize strings, or substitute displayed characters. For positive cases, compare the JCS UTF-8 bytes to `canonical_utf8_hex` and SHA-256 to `sha256_hex`. For negative cases, reject for the named contract reason before returning a digest. Implementations may use other error names; evidence must establish the rejection and relevant cause, not merely a matching token.

The historical P2 input is a rejection expectation in r2 because its member name contains U+FFFF. Returning its historical canonical bytes or digest does not satisfy this input contract. The historical P2 artifacts and external report are retained, not re-scored as an execution of r2.

`artifact_revision` versions this candidate suite and documentation; the envelope schema remains `/1`. This file is a local review candidate, not an approved or independently held conformance suite. Contract adoption, publication, and external verification require separate decisions.

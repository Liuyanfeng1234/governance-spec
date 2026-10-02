# Canonical-envelope interop profile — proposed

Status: **proposal for review; not merged, adopted, or authoritative** (2026-09-28). This directory is intended for a possible public pull request to `governance-spec`. Opening a pull request would make the proposal visible, but would not make it an approved V19 contract.

This is a **new, synthetic-only** profile, `v19.canonical_envelope.interop/1`. It is not the previously mentioned V19 `canonical_envelope`. Its vectors do **not** answer the request for existing-contract vectors in [Issue #3](https://github.com/Liuyanfeng1234/governance-spec/issues/3) or satisfy that issue's independent-verification bar.

Contents:

- `SPEC.md`: proposed input, canonicalization, digest, and non-authority boundary.
- `vectors.json`: two locally cross-computed positive candidates and four contract-level rejection candidates. The rejection cases have not been certified against an independent complete validator.

All values are newly constructed synthetic test data. The profile defines no signature, issuer trust, human approval, execution grant, or real-governance metadata. A matching SHA-256 digest alone conveys none of those properties.

The intended publication license is the repository's CC-BY-4.0, subject to final owner approval of the exact public diff. A separate Issue reply draft remains local and is **not** part of this proposal or automatically posted.

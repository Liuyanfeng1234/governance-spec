# Canonical-envelope interoperability candidate: artifact revision r2

Status: local versioned correction candidate, not published, adopted, or independently certified (2026-10-03).

This corrects the P2 input-validity contradiction in the synthetic-only proposal at GitHub commit `2d4b623b1df6437212e8c8aff4e1f06c2063cc0e`, directory `fixtures/canonical_envelope_interop_v1/`. The historical commit and local `issue3_public_candidate_v2/` files remain unchanged.

The envelope schema remains `v19.canonical_envelope.interop/1` and the profile remains `synthetic-interop/1`. `r2` identifies an artifact revision; it does not adopt a new envelope version or make `/2` valid.

Changes:

- SPEC explicitly distinguishes ill-formed Unicode (including lone surrogates) from well-formed Unicode noncharacters prohibited by I-JSON. This clarifies the existing strict input boundary, not a relaxation.
- The original `P2-utf16-number` input is unchanged, but its expected outcome is now `REJECT_IJSON_NONCHARACTER`. Its historical case ID is retained for traceability; the `P` prefix no longer denotes acceptance in this revision.
- P2's active canonical-byte/digest fields and local byte-match claim are removed from this revision. Their original bytes and claims remain in the historical artifact, not valid conformance expectations.
- P1 and N1–N4 are unchanged. There is now one carried-forward positive candidate and five standards/contract-derived rejection expectations. No replacement positive case is added.

Consequently there is no valid positive coverage here for the former P2 UTF-16 ordering/number combination. This coverage loss is explicit, not hidden by a replacement fixture or score adjustment.

No complete validator or external toolchain has been run against r2. N4's standard requirement is established, but the reported package behavior remains unreplicated. A local artifact consistency check is not conformance testing. Even a later third-party execution of these public vectors would be non-blind cross-verification, not independent custody, historical V19 validation, or an RSI/safety-benefit result.

Publication, contract adoption, external execution, review, and merge remain separate actions. No signature, issuer trust, human approval, or execution authority is defined by this synthetic profile.

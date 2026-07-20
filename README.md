---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 9be3b1eaeb70b0dbe81eaea16f8645d8_2b70db77817f11f1b625525400e6dd8f
    ReservedCode1: 2BaGSAUSFul7AFIuHFAkVhiTV+VKRC5DwJDhCvj2I3eLO6QIlkSSecjct5XNRycL/eP2ce4V10kL1ofBKksIRECSGMzkiZIFrVavbcnQN6Qvg3+/y/8FX8U+kICiTuOGvDh828AZvJAjfAzU36AFgczqv08+mftb3U0Tjgw1DF60vDJaxbvpCwA7ab4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 9be3b1eaeb70b0dbe81eaea16f8645d8_2b70db77817f11f1b625525400e6dd8f
    ReservedCode2: 2BaGSAUSFul7AFIuHFAkVhiTV+VKRC5DwJDhCvj2I3eLO6QIlkSSecjct5XNRycL/eP2ce4V10kL1ofBKksIRECSGMzkiZIFrVavbcnQN6Qvg3+/y/8FX8U+kICiTuOGvDh828AZvJAjfAzU36AFgczqv08+mftb3U0Tjgw1DF60vDJaxbvpCwA7ab4=
---

© 2026 V19 Governance Protocol Contributors. Licensed under CC-BY-4.0.

---

# V19 Governance Protocol Specification

**Version 1.0.0** | **2026-07-17** | CC-BY-4.0

> **Independent release** — originally part of the V19 cognitive architecture, now available as a standalone specification.

---

## Why This Exists

AI coding agents generate code faster than traditional review cycles can handle. Cursor, Copilot, Claude Code — they all produce thousands of lines per session. But the security tooling hasn't caught up.

**Traditional SAST (regex-based)** finds known patterns:
- Hardcoded secrets (`api_key = "sk-xxx"`)
- SQL injection (`SELECT * FROM`)
- Path traversal (`../`)

**It cannot find semantic vulnerabilities** — problems that span multiple modules, involve runtime state, or require understanding code *intent* rather than just code *text*.

## Case Study: Grok Build Audit

When xAI open-sourced Grok Build CLI, the community focused on External Telemetry privacy concerns. We audited the 2,761-file codebase using a local LLM (Ollama qwen2.5:7b). The result was counterintuitive:

**External Telemetry was the best-designed module** — fail-closed, attribute allowlist, dual-channel isolation. The real problems were elsewhere.

### Three HIGH Findings

| ID | Module | Finding | Type |
|:--:|--------|---------|:----:|
| H-1 | `managed_mcp.rs` | MCP credentials cached in `ManagedMcpCache` — no zeroize over process lifetime | Credential lifecycle |
| H-2 | `subagent_coordinator.rs` | Sub-agent inherits full parent environment — can read `session_key` | Permission inheritance |
| H-3 | `agent_ops.rs` | `api_key_auth_disabled()` is a runtime toggle — no alert, no log when auth is silently disabled | Auth bypass |

### Why Regex Can't Find H-2

H-2 is not a line of code like `password = "xxx"`. It's a chain:

```
parent Agent → auth_manager.current_or_expired() → session_key
            → build_summary_client() → SamplingConfig.bearer_resolver
            → subagent inherits env vars → bearer_resolver callback → credential leak
```

This crosses **3 modules** and involves **runtime state inheritance**. No regex pattern can match it.

### Audit Track Record

| Metric | Value |
|--------|-------|
| Modules audited | 42 (35 SAE + 7 Grok) |
| Total findings | 306 |
| HIGH severity | 28 |
| Architecture layers covered | 10 (BCN, PRD, Cognition, Protocol, Trust, Evolution, Agent, EIF, Diagnosis, Audit) |
| Engine | Ollama qwen2.5:7b (fully local) |
| Data security | Code never leaves local machine |

---

## What's Included

| File | Description |
|------|-------------|
| [`governance-protocol-spec.md`](./governance-protocol-spec.md) | Complete protocol specification (20 sections, 90+ KB) |
| [`fixtures/duplicate_key_rejection_v1`](./fixtures/duplicate_key_rejection_v1/) | JSON duplicate-property rejection cases for pre-JCS input validity |
| [`LICENSE.txt`](./LICENSE.txt) | CC-BY-4.0 license |

## Protocol at a Glance

- **Service Matrix**: Core API (8700), Interaction Layer (8701), Memory Graph (8702), Execution Orchestration (8703)
- **Authentication**: Three-tier model (admin/pro/basic) with AuthManager
- **14 Sub-Protocols**: DecisionTracer, MCTE, PolarityDrive, SelfConsistencyValidator, KnowledgeTopology, CausalPathEngine, HeartbeatProtocol, POP, PRO, CVP, HGP, CPIP, ISP, KGA
- **PMI Trust Scoring**: Three-layer (L1 Trust, L2 Contribution, L3 Health) with gamma decay
- **Seven-Layer Defense**: Input validation through incident response
- **Self-Healing**: 9 named repair routines with SCD/MIEG validation
- **25 Axioms**: κ_Axiom framework with lifecycle management

## License

**CC-BY-4.0** — Share and adapt for any purpose, even commercially, with attribution.

## Repository

- **Primary**: https://github.com/Liuyanfeng1234/governance-spec

---

> **Disclaimer**: This specification describes a working system. API endpoints and module availability may vary depending on the deployment environment.

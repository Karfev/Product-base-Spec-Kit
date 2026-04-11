<!-- FILE: .specify/specs/005-multi-agent-portability/trace.md -->
# Traceability: 005-multi-agent-portability

| REQ-ID | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|
| `REQ-{SCOPE}-{NNN}` | `decisions/{INIT}-ADR-005-multi-agent-portability` | `contracts/openapi.yaml#/paths/~1{path}/post` | `contracts/schemas/{entity}.schema.json` | `tests/e2e/{test}::REQ-{SCOPE}-{NNN}` | `ops/slo.yaml#{slo-name}` |
| `REQ-{SCOPE}-{NNN}` | — | — | — | `tests/perf/{test}::REQ-{SCOPE}-{NNN}` | `ops/slo.yaml#{slo-name}` |

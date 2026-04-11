<!-- FILE: .specify/specs/004-adoption-path/trace.md -->
# Traceability: 004-adoption-path

| REQ-ID | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|
| `REQ-{SCOPE}-{NNN}` | `decisions/{INIT}-ADR-004-adoption-path` | `contracts/openapi.yaml#/paths/~1{path}/post` | `contracts/schemas/{entity}.schema.json` | `tests/e2e/{test}::REQ-{SCOPE}-{NNN}` | `ops/slo.yaml#{slo-name}` |
| `REQ-{SCOPE}-{NNN}` | — | — | — | `tests/perf/{test}::REQ-{SCOPE}-{NNN}` | `ops/slo.yaml#{slo-name}` |

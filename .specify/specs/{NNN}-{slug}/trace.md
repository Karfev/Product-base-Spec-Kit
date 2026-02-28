<!-- FILE: .specify/specs/{NNN}-{slug}/trace.md -->
# Traceability: {NNN}-{slug}

| REQ-ID | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|
| `REQ-{SCOPE}-{NNN}` | `decisions/{INIT}-ADR-{NNN}-{slug}` | `contracts/openapi.yaml#/paths/~1{path}/post` | `contracts/schemas/{entity}.schema.json` | `tests/e2e/{test}::REQ-{SCOPE}-{NNN}` | `ops/slo.yaml#{slo-name}` |
| `REQ-{SCOPE}-{NNN}` | — | — | — | `tests/perf/{test}::REQ-{SCOPE}-{NNN}` | `ops/slo.yaml#{slo-name}` |

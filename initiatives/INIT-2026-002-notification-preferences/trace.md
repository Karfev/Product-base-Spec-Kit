# RTM: INIT-2026-002-notification-preferences
Generated: 2026-04-10

| REQ-ID | Type | Priority | Status | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|---|---|---|
| `REQ-NOTIF-001` | functional | P0 | draft | — | `contracts/openapi.yaml#/paths/~1notification-preferences/get` | — | — | — |
| `REQ-NOTIF-002` | functional | P0 | draft | — | `contracts/openapi.yaml#/paths/~1notification-preferences~1channels/patch` | — | — | — |
| `REQ-NOTIF-003` | functional | P1 | draft | — | `contracts/openapi.yaml#/paths/~1notification-preferences~1frequency/patch` | — | — | — |
| `REQ-NOTIF-004` | functional | P0 | draft | — | `contracts/openapi.yaml#/paths/~1notification-preferences~1categories~1%7BcategoryId%7D/delete` | — | — | — |
| `REQ-NOTIF-005` | nfr | P1 | draft | — | — | — | — | `ops/slo.yaml#notification-preferences-latency` |
| `REQ-NOTIF-006` | functional | P1 | draft | — | `contracts/asyncapi.yaml#/channels/notifications.preferences.updated` | — | — | — |

## Coverage Summary

- **Total REQ-IDs:** 6
- **With ≥1 trace link:** 6 (100%)
- **With tests:** 0 (0%) — tests not yet written
- **With ADR:** 0 — lazy-init ADR proposed in plan but not yet created

## GAP Report

- All REQ-IDs have at least one contract or SLO link — no blockers for Standard DoD at this stage
- **Tests:** all 6 REQ-IDs missing test links — will be resolved in T2a/T2b
- **ADR:** REQ-NOTIF-001 references lazy-init pattern in plan.md but no formal ADR created yet
- **SLO:** ops/slo.yaml still contains template placeholders — needs to be filled in T4

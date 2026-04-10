<!-- FILE: .specify/specs/002-notification-preferences/trace.md -->
# Traceability: 002-notification-preferences

| REQ-ID | ADR | Contract | Schema | Tests | SLO |
|---|---|---|---|---|---|
| `REQ-NOTIF-001` | — | `contracts/openapi.yaml#/paths/~1notification-preferences/get` | — | — | — |
| `REQ-NOTIF-002` | — | `contracts/openapi.yaml#/paths/~1notification-preferences~1channels/patch` | — | — | — |
| `REQ-NOTIF-003` | — | `contracts/openapi.yaml#/paths/~1notification-preferences~1frequency/patch` | — | — | — |
| `REQ-NOTIF-004` | — | `contracts/openapi.yaml#/paths/~1notification-preferences~1categories~1%7BcategoryId%7D/delete` | — | — | — |
| `REQ-NOTIF-005` | — | — | — | — | `ops/slo.yaml#notification-preferences-latency` |
| `REQ-NOTIF-006` | — | `contracts/asyncapi.yaml#/channels/notifications.preferences.updated` | — | — | — |

## Coverage

- **Total REQ-IDs:** 6
- **With ≥1 trace link:** 6 (100%)
- **Full coverage (all applicable cells):** 0 — tests not yet written (T2a pending)

## GAPs

Нет REQ-IDs с полностью пустой трассировкой. Все имеют как минимум contract или SLO link.
Tests будут добавлены после T2a/T2b.

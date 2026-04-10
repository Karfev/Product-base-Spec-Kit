# Evidence Report: INIT-2026-002-notification-preferences
Generated: 2026-04-10
Profile: standard

## RTM Coverage

Overall: **20%** (6 of 30 trace cells filled)

| REQ-ID | ADR | Contract | Schema | Tests | SLO | Coverage |
|---|---|---|---|---|---|---|
| `REQ-NOTIF-001` | — | ✓ | — | — | — | 20% |
| `REQ-NOTIF-002` | — | ✓ | — | — | — | 20% |
| `REQ-NOTIF-003` | — | ✓ | — | — | — | 20% |
| `REQ-NOTIF-004` | — | ✓ | — | — | — | 20% |
| `REQ-NOTIF-005` | — | — | — | — | ✓ | 20% |
| `REQ-NOTIF-006` | — | ✓ | — | — | — | 20% |

All REQ-IDs have ≥1 trace link (no fully orphaned requirements).

## Requirements Status

| Status | Count |
|---|---|
| ❌ OPEN (draft) | 6 |
| 🟡 IN PROGRESS | 0 |
| ✅ DONE (verified) | 0 |
| 🔴 GAP (0 links) | 0 |

## PRR Status

| Category | DONE | OPEN (P1) | BLOCKING (P0) |
|---|---|---|---|
| SLO/SLI | 0 | 1 | 2 |
| Architecture | 0 | 2 | 1 |
| Observability | 0 | 2 | 2 |
| Deployment | 0 | 1 | 2 |
| Security | 0 | 1 | 2 |
| Ops | 0 | 2 | 1 |
| **Total** | **0** | **9** | **10** |

Note: Security P0 items include threat-model which is Extended-only but present in Standard template (framework bug P16).

## SLO Coverage

| NFR REQ-ID | SLO Defined | SLO Name | Target |
|---|---|---|---|
| REQ-NOTIF-005 | ✓ | `notification-preferences-latency` | P95 < 200ms |

## Gaps (Blockers)

1. **Tests missing** — all 6 REQ-IDs lack test evidence (T2a/T2b not executed)
2. **ADR missing** — lazy-init pattern proposed in plan.md but no formal ADR created
3. **PRR blocking** — 10 P0 items unchecked (including 2 Extended-only items in Standard template)
4. **Schemas** — no dedicated JSON Schema files (inline in OpenAPI/AsyncAPI)
5. **All requirements in `draft` status** — none moved to `implemented` or `verified`

## Recommendation

**NOT READY FOR RELEASE**

Reasons:
- RTM coverage 20% (threshold: 80%)
- 0 of 6 requirements verified
- 10 PRR blocking items unchecked
- No tests written

This is expected: test initiative covers spec/planning chain only, not implementation.

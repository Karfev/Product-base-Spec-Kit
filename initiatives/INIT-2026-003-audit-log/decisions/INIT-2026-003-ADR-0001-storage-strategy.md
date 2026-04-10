---
status: "proposed"
date: "2026-04-10"
decision-makers: ["@platform-team"]
consulted: ["@sre"]
informed: ["@product"]
---

# INIT-2026-003-ADR-0001: Audit log storage strategy

## Context and problem statement

The audit log service needs to store immutable audit events with 2-year retention (REQ-AUDIT-005) and support filtered queries with P95 < 300ms latency (REQ-AUDIT-004). The platform uses PostgreSQL as primary store. We need to decide whether to use PostgreSQL directly, add a specialized store (ClickHouse, Elasticsearch), or use an append-only table pattern.

## Decision drivers

- REQ-AUDIT-004: P95 < 300ms query latency over 2 years of data
- REQ-AUDIT-005: 2-year retention with automatic purge
- Operational simplicity: minimize new infrastructure
- Platform tech stack: PostgreSQL, Redis, RabbitMQ already available

## Considered options

- **Option A:** PostgreSQL append-only table with date-based partitioning
- **Option B:** ClickHouse for analytical queries + PostgreSQL for metadata
- **Option C:** Elasticsearch for full-text search + PostgreSQL for storage

## Decision outcome

**Chosen option:** "Option A — PostgreSQL append-only table with date-based partitioning", because it keeps the stack simple, leverages existing PostgreSQL expertise and infrastructure, and date-based partitioning enables efficient retention purge (DROP PARTITION) without impacting active queries. At our expected volume (< 10M events/year), PostgreSQL with proper indexing meets the P95 < 300ms SLO.

### Consequences

- **Good:** No new infrastructure; existing backup/monitoring/HA applies; partition pruning ensures old data purge has zero query impact
- **Bad:** If volume exceeds 10M events/year, may need to revisit; no full-text search on metadata field
- **Neutral:** Requires monthly partition creation cron job

### Confirmation

Monitor `audit.query.p95_latency_ms` metric. If P95 exceeds 300ms at 3-month mark, re-evaluate with Option B.

---

*Шаблон основан на [MADR](https://adr.github.io/madr/).*

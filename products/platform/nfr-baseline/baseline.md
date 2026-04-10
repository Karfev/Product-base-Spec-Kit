# NFR Baseline: platform
Updated: 2026-04-10

## Availability
- Target: 99.9% per month (43.8 min downtime/month)
- RTO: 15 minutes
- RPO: 1 hour
- Measurement: uptime monitor (Datadog synthetic)

## Latency
- P95 API response: < 200ms (general)
- P99 API response: < 500ms (general)
- Measurement: APM histogram `http_request_duration_seconds`

No conflicts with initiative NFRs:
- REQ-NOTIF-005 (INIT-2026-002): P95 < 200ms, P99 < 500ms — matches baseline exactly.

## Throughput
- Sustained RPS: 500 RPS
- Peak RPS: 2000 RPS (burst capacity)
- Measurement: load balancer metrics `requests_per_second`

## Security
- Auth: Bearer JWT (all endpoints)
- Data classification: PII (notification preferences contain user_id and behavioral data)
- Encryption in transit: TLS 1.2+
- Encryption at rest: AES-256 (PostgreSQL TDE)

## Data Retention
- Operational data: indefinite (while user account active)
- Audit logs (preference_audit_log): 2 years (GDPR compliance)
- Backups: daily full, hourly incremental
- Backup restoration SLA: < 4 hours

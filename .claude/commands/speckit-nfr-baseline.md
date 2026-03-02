---
description: Define or update the NFR baseline for a product and surface conflicts with L3 requirements
argument-hint: <product-name> (e.g., platform, analytics)
---

You are defining the Non-Functional Requirements baseline for product `$ARGUMENTS`.

## Your job

1. Read `products/$ARGUMENTS/nfr-baseline.md` (current state — may be stub).
2. Scan all `initiatives/*/requirements.yml` for `type: nfr` requirements whose `trace.components`
   includes `$ARGUMENTS` — these must be satisfied by the baseline.
3. Read `.specify/memory/constitution.md` for NFR principles.

4. Ask the user to define targets for each NFR dimension (or confirm existing values):

   **Availability:**
   - Monthly uptime target (e.g., 99.9% = 43.8 min/month downtime)
   - RTO (Recovery Time Objective) and RPO (Recovery Point Objective)

   **Latency:**
   - P95 response time for read endpoints (ms)
   - P95 response time for write endpoints (ms)
   - P99 target (ms)

   **Throughput:**
   - Sustained RPS (requests per second) under normal load
   - Peak RPS (burst capacity)

   **Data:**
   - Data retention period
   - Backup frequency and restoration SLA

   **Security:**
   - Authentication mechanism (Bearer JWT / API key / mTLS / OAuth2)
   - Data classification (PII / financial / internal / public)
   - Encryption at rest and in transit requirements

5. **Conflict detection**: Cross-reference with `nfr` requirements from L3 initiatives:
   ```
   ⚠️ CONFLICT: REQ-AUTH-004 (INIT-2026-000) requires P95 auth latency < 10ms
      Current NFR baseline target: P95 < 200ms
      → Baseline must be tightened to ≤ 10ms for auth endpoints, or REQ-AUTH-004 must be revised
   ```

6. Update `products/$ARGUMENTS/nfr-baseline.md` with confirmed targets and measurement sources:
   ```markdown
   ## Latency
   - P95 API response: < 200ms (general), < 10ms (auth endpoints — REQ-AUTH-004)
   - Measurement: APM histogram `http_request_duration_seconds`
   ```

7. Report:
   - NFR dimensions updated
   - Conflicts found (if any) with recommended resolution
   - Next step: `Add SLO definitions in initiatives/<INIT>/ops/slo.yaml for nfr requirements`

## Rules
- NFR baseline is a **floor**, not a ceiling — individual initiatives may set stricter targets
- Conflicts between baseline and initiative NFRs MUST be documented and resolved, not ignored
- Every target MUST specify a measurement source (APM metric, uptime monitor, etc.)
- Do NOT set targets without user confirmation — ask if unsure
- Mark unresolved conflicts with `⚠️ CONFLICT:` prefix in the baseline file

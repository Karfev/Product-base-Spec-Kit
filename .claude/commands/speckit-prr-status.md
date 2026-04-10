---
description: Review PRR checklist status — classify items as DONE / OPEN / BLOCKING
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are reviewing the Production Readiness Review for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/ops/prr-checklist.md`.
2. Read `initiatives/$ARGUMENTS/requirements.yml` to understand profile and priorities.
3. Read `initiatives/$ARGUMENTS/ops/slo.yaml` (if exists).
4. Read `initiatives/$ARGUMENTS/trace.md` (if exists).

5. **Artifact existence check**: Before classifying checklist items, verify backing artifacts for key MUST items:
   - SLO: check if `ops/slo.yaml` exists AND contains at least one `kind: SLO` block without `{placeholders}`
   - Rollout: check if `delivery/rollout.md` exists AND does NOT contain `{placeholders}`
   - Feature flags: check if `delivery/rollout.md` contains "feature flag" or "Feature flag"
   
   For items where the artifact exists and appears filled but the checkbox is unchecked, annotate with ⚡:
   ```
   🔴 BLOCKING: [SLO] SLO defined in ops/slo.yaml — checkbox unchecked ⚡ artifact exists and appears filled
   ```
   This helps distinguish "need to create artifact" from "need to verify and check the box".

6. **Parse checklist items** and classify each:
   - ✅ `DONE` — `[x]` checked
   - ❌ `OPEN` — `[ ]` unchecked, non-critical
   - 🔴 `BLOCKING` — `[ ]` unchecked AND marked as MUST in the checklist category

6. **PRR Categories to check** (Standard/Extended profile):

   | Category | Key MUST items |
   |---|---|
   | **SLO** | SLO defined in `ops/slo.yaml`, error budget policy documented |
   | **Observability** | Metrics/alerts exist, dashboard linked, on-call runbook written |
   | **Deployment** | Rollout strategy defined in `delivery/rollout.md`, rollback procedure exists |
   | **Security** | Secrets management reviewed, no credentials in code/config |
   | **Dependencies** | All downstream dependencies notified, contract compatibility verified |
   | **Capacity** | Load estimates reviewed, auto-scaling configured |
   | **Incidents** | Incident response runbook exists, P0/P1 escalation path defined |

7. Generate a status summary:
   ```
   PRR Status: $ARGUMENTS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━
   DONE:     12 items ✅
   OPEN:      3 items ❌ (non-blocking)
   BLOCKING:  2 items 🔴

   🔴 BLOCKERS (must resolve before release):
   1. [SLO] Error budget policy not documented
   2. [Incidents] On-call runbook not written

   ❌ OPEN (recommended to complete):
   1. [Capacity] Load estimates not reviewed
   2. [Observability] Dashboard not linked
   3. [Security] Threat model not reviewed (Extended profile only)

   Recommendation: NOT READY FOR RELEASE
   Next action: Resolve 2 blockers, then re-run /speckit-prr-status $ARGUMENTS
   ```

8. If all BLOCKING items are resolved:
   ```
   ✅ PRR PASSED — $ARGUMENTS is ready for release gate
   Run /speckit-evidence $ARGUMENTS for full evidence report
   ```

## Rules
- MUST NOT declare PRR passed if any 🔴 BLOCKING item remains unchecked
- For Minimal profile: skip SLO, Security, Capacity, Incidents categories
- Items the user asks to skip MUST be documented with explicit justification in `prr-checklist.md`
- Do not edit `prr-checklist.md` — only report status; user must check items manually

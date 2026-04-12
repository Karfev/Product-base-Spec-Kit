# Traceability Visualization: INIT-2026-009-smoke-test

Generated: 2026-04-12
Profile: Standard

## Coverage Summary

| Status | Count | REQ-IDs |
|--------|------:|---------|
| 🟢 Covered | 4 | REQ-EXPORT-001, REQ-EXPORT-002, REQ-EXPORT-003, REQ-EXPORT-004 |
| 🟡 Partial  | 0 | — |
| 🔴 Orphan   | 0 | — |

**Coverage: 4/4 REQ-IDs fully traced (100%)**

## Diagram

```mermaid
flowchart LR
  subgraph REQ["Requirements"]
    REQ_EXPORT_001["REQ-EXPORT-001\nP0 functional"]
    REQ_EXPORT_002["REQ-EXPORT-002\nP1 functional"]
    REQ_EXPORT_003["REQ-EXPORT-003\nP1 functional"]
    REQ_EXPORT_004["REQ-EXPORT-004\nP1 nfr"]
  end

  subgraph ADR["Decisions"]
    ADR_0001["ADR-0001\nasync-queue"]
  end

  subgraph Contract["Contracts"]
    OA_exports_post["OpenAPI\nPOST /exports"]
    OA_exports_get["OpenAPI\nGET /exports/id"]
    AA_completed["AsyncAPI\nexport.report.completed"]
  end

  subgraph Schema["Schemas"]
    SCH_export["export.schema.json"]
  end

  subgraph Test["Tests"]
    TEST_e2e["tests/e2e/\nexport.spec.ts"]
    TEST_perf["tests/perf/\nexport-latency.jmx"]
  end

  subgraph SLO["SLO"]
    SLO_latency["slo.yaml\nexport-latency"]
  end

  subgraph Component["Components"]
    COMP_export["export-service"]
  end

  REQ_EXPORT_001 -->|adr| ADR_0001
  REQ_EXPORT_001 -->|contract| OA_exports_post
  REQ_EXPORT_001 -->|schema| SCH_export
  REQ_EXPORT_001 -->|test| TEST_e2e
  REQ_EXPORT_001 -->|component| COMP_export

  REQ_EXPORT_002 -->|contract| OA_exports_post
  REQ_EXPORT_002 -->|test| TEST_e2e
  REQ_EXPORT_002 -->|component| COMP_export

  REQ_EXPORT_003 -->|contract| AA_completed
  REQ_EXPORT_003 -->|contract| OA_exports_get
  REQ_EXPORT_003 -->|test| TEST_e2e
  REQ_EXPORT_003 -->|component| COMP_export

  REQ_EXPORT_004 -->|test| TEST_perf
  REQ_EXPORT_004 -->|slo| SLO_latency
  REQ_EXPORT_004 -->|component| COMP_export

  style REQ_EXPORT_001 fill:#4CAF50,color:#fff
  style REQ_EXPORT_002 fill:#4CAF50,color:#fff
  style REQ_EXPORT_003 fill:#4CAF50,color:#fff
  style REQ_EXPORT_004 fill:#4CAF50,color:#fff
```

## Gaps

No gaps detected. All 4 REQ-IDs have at least 1 test link AND at least 1 contract or component link.

# Product-base-Spec-Kit

Build high-quality products and services faster.

A spec-driven artifact kit for B2B product teams, based on the **Spec Constitution** — an operational system of changes where machine-readable anchors are validated by CI.

---

## Structure

```text
.specify/
  memory/constitution.md     ← L0: Spec Constitution (principles, CI gates, profiles)
  specs/{NNN}-{slug}/        ← L4: Feature spec-kit (spec / plan / tasks / trace)

domains/{domain}/            ← L1: Glossary, canonical model, event catalog, NFR
products/{product}/          ← L2: Architecture, product ADR, NFR baseline
services/{service-code}/     ← L2.5: External/Internal Service Spec, SLO, catalogs, billing, RSM
initiatives/{INIT-slug}/     ← L3: PRD, requirements.yml, contracts, ops, decisions

tools/schemas/               ← CI validators (JSON Schema)
evidence/                    ← L5: CI-generated artifacts (RTM, reports)
```

**How the levels connect:**
```
products/{product}/  →  services/{service-code}/  →  initiatives/{INIT}/
     L2                        L2.5                         L3
(what we build)         (what we offer clients)      (how we improve it)
```

---

## Quick start

### New initiative (L3)
```bash
cp -r "initiatives/{INIT-YYYY-NNN-slug}/" initiatives/INIT-2026-042-my-feature/
# Edit all {placeholder} values
make validate
```

### New service spec (L2.5)
```bash
cp -r "services/{service-code}/" services/my-service/
# Fill README.md → external-spec.md → requirements.yml → ops/* → billing/*
make validate-services
```

### New feature spec (L4)
```bash
cp -r ".specify/specs/{NNN}-{slug}/" .specify/specs/042-my-feature/
# Fill spec.md → plan.md → tasks.md
```

### Validate everything
```bash
make check-all          # requirements + services + lint + contracts + trace
make validate-services  # service artifacts only (billing, incidents, requests, SLO)
make validate           # initiative requirements only
make lint-docs          # YAML + Markdown hygiene
make lint-contracts     # OpenAPI + AsyncAPI
```

---

## Profiles

### Initiatives (L3)

| Profile | When | Key artifacts |
|---|---|---|
| **Minimal** | Low-risk changes | `prd.md`, `requirements.yml`, `CHANGELOG.md` |
| **Standard** | Most initiatives | + `design.md`, `contracts/`, ADR, `slo.yaml`, `prr-checklist.md` |
| **Extended** | High-risk / regulated | + `threat-model.md`, `nfr-validation.md`, `migration.md`, `compliance/` |

### Services (L2.5)

| Profile | When | Key artifacts |
|---|---|---|
| **Minimal** | Internal / draft service | `README.md`, `external-spec.md`, `requirements.yml` |
| **Standard** | Client-facing service | + `internal-spec.md`, `rsm.md`, `responsibilities.yml`, `ops/slo.yaml`, `ops/incident-catalog.yml`, `ops/request-catalog.yml` |
| **Extended** | Critical / regulated service | + `billing/parameters.yml`, `ops/change-catalog.yml`, `appendices/*` |

---

## What's in a service (L2.5)

```
services/{service-code}/
├── README.md                   # Identity, links to product ↑ and initiatives ↓
├── external-spec.md            # Client-facing specification (narrative → machine-readable anchors)
├── internal-spec.md            # Internal delivery spec (architecture, RSM, responsibilities)
├── rsm.md                      # Resource-Service Model (Mermaid diagrams)
├── requirements.yml            # Machine-readable SLA/functional requirements (REQ-SVC-*)
├── responsibilities.yml        # Responsibility matrix by architectural block
├── billing/
│   └── parameters.yml          # Billable parameters, change steps and limits
└── ops/
    ├── slo.yaml                 # OpenSLO v1: availability, SLI/SLO/Error Budget
    ├── incident-catalog.yml     # Incident classification, thresholds, SLT
    ├── request-catalog.yml      # Service request catalog, priorities, SLT
    └── change-catalog.yml       # Standard/non-standard change parameters
```

See [`services/README.md`](./services/README.md) for full details and profile table.

**Example:** [`services/vtsod-vmwr-vs/`](./services/vtsod-vmwr-vs/) — Private Cloud VMware vDC (Extended profile, fully populated).

---

## Governance

Full principles, CI gates strategy, ID conventions, levels (L0–L5), and enforcement roadmap:
→ [`.specify/memory/constitution.md`](./.specify/memory/constitution.md)

## Design doc

→ [`docs/plans/2026-02-28-spec-kit-file-structure-design.md`](./docs/plans/2026-02-28-spec-kit-file-structure-design.md)

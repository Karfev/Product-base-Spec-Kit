# Product-base-Spec-Kit

Build high-quality products faster.

A spec-driven artifact kit for B2B SaaS teams, built around the **Spec Constitution** — a governance system where machine-readable anchors (requirements, contracts, SLOs) are validated by CI gates.

---

## What This Kit Does

- Provides a **five-level hierarchy** (L0–L5) of templates for all product artifacts
- Enforces **traceability by construction**: every requirement links to ADR, contract, schema, tests, and SLO
- Validates artifacts automatically via **CI gates** (requirements schema, OpenAPI lint, breaking change diff, markdown lint)
- Integrates with **Claude Code** via `/speckit.*` commands to guide spec authoring and task-based implementation

---

## Structure

```text
.specify/
  memory/constitution.md          ← L0: Spec Constitution (principles, CI gates, ID schemes, profiles)
  specs/{NNN}-{slug}/             ← L4: Feature spec-kit (spec / plan / tasks / trace)

domains/{domain}/            ← L1: Glossary, canonical model, event catalog, NFR
products/{product}/          ← L2: Architecture, product ADR, NFR baseline
services/{service-code}/     ← L2.5: External/Internal Service Spec, SLO, catalogs, billing, RSM
initiatives/{INIT-slug}/     ← L3: PRD, requirements.yml, contracts, ops, decisions

tools/
  init.sh                         ← Bootstrap: create new initiative + L4 spec from templates
  schemas/                        ← JSON Schema validators for requirements.yml
  scripts/check-trace.py          ← REQ-ID consistency check: L3 ↔ L4

evidence/                         ← L5: CI-generated artifacts (RTM, coverage, PRR status)

## Claude Code commands

All levels have dedicated `/speckit-*` commands. Use them instead of copying templates manually.

### L0 — Governance
| Command | What it does |
|---|---|
| `/speckit-constitution-review` | Audit all L1–L5 artifacts for compliance with the Spec Constitution |

### L1 — Domain
| Command | What it does |
|---|---|
| `/speckit-domain-init <domain>` | Scaffold glossary, canonical model, event catalog, NFR |
| `/speckit-domain-update <domain>` | Add terms, entities, or events with conflict detection |

### L2 — Product
| Command | What it does |
|---|---|
| `/speckit-product-init <product>` | Scaffold arc42 architecture, NFR baseline, decisions/ |
| `/speckit-adr-product <product>` | Create a Product ADR in MADR format via guided questions |
| `/speckit-nfr-baseline <product>` | Define NFR targets and surface conflicts with L3 requirements |

### L3 — Initiative
| Command | What it does |
|---|---|
| `/speckit-profile <INIT-slug>` | Select Minimal / Standard / Extended via risk assessment |
| `/speckit-init <INIT-slug>` | Scaffold full initiative folder for the chosen profile |
| `/speckit-prd <INIT-slug>` | Write the PRD with structured questions |
| `/speckit-requirements <INIT-slug>` | Fill requirements.yml, assign REQ-IDs, run `make validate` |
| `/speckit-contracts <INIT-slug>` | Generate OpenAPI 3.1 / AsyncAPI 3.0 stubs from requirements.yml |

### L4 — Feature spec
| Command | What it does |
|---|---|
| `/speckit-specify <NNN>-<slug>` | Create or update spec.md |
| `/speckit-plan <NNN>-<slug>` | Generate plan.md from filled spec.md |
| `/speckit-tasks <NNN>-<slug>` | Generate tasks.md from filled plan.md |
| `/speckit-implement <NNN>-<slug>` | Guide task-by-task implementation (RED → GREEN) |
| `/speckit-trace <NNN>-<slug>` | Build trace.md RTM and verify with `make check-trace` |

### L5 — Evidence
| Command | What it does |
|---|---|
| `/speckit-rtm <INIT-slug>` | Build the Requirements Traceability Matrix for an initiative |
| `/speckit-prr-status <INIT-slug>` | Review PRR checklist — DONE / OPEN / BLOCKING |
| `/speckit-evidence <INIT-slug>` | Generate full evidence report (RTM coverage, PRR status) |

**How the levels connect:**
```
products/{product}/  →  services/{service-code}/  →  initiatives/{INIT}/
     L2                        L2.5                         L3
(what we build)         (what we offer clients)      (how we improve it)
```

---

## Quick start

1. **New initiative (L3):**
   ```bash
   ./tools/init.sh INIT-2026-042-my-feature [042-my-feature]
   # или с профилем enterprise:
   ./tools/init.sh INIT-2026-042-my-feature 042-my-feature --profile enterprise
   ```

2. **New feature spec (L4):**
   ```bash
   cp -r .specify/specs/{NNN}-{slug}/ .specify/specs/042-my-feature/
   # Fill spec.md → plan.md → tasks.md
   ```

3. **Validate all requirements.yml:**
   ```bash
   make validate
   ```

4. **Lint OpenAPI contract:**
   ```bash
   redocly lint initiatives/INIT-2026-042-my-feature/contracts/openapi.yaml
   ```
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
| **Minimal** | Low-risk changes | prd.md, requirements.yml, CHANGELOG.md |
| **Standard** | Most initiatives | + design.md, contracts/, ADR, slo.yaml, prr-checklist.md |
| **Extended** | High-risk / regulated | + threat-model.md, nfr-validation.md, migration.md, compliance/ |
| **Enterprise** | Large IS-class systems | + design.md (3-layer АИС ontology), architecture-views/, subsystem-classification.yaml |

> Full profile artifact requirements and CI gate rules → `.specify/memory/constitution.md`

## Enterprise IS Profile

For large information systems following the АИС methodology (ArchiMate 3.2 / ГОСТ Р ИСО/МЭК 25020):

```bash
# Bootstrap enterprise initiative
./tools/init.sh INIT-2026-NNN-my-system --profile enterprise

# Fill architecture layers interactively (15 questions → Mermaid stubs)
/speckit-architecture INIT-2026-NNN-my-system
```

**What you get:**
- `design.md` — three-layer architecture (Activity / Application / Technology layer)
- `subsystem-classification.yaml` — machine-readable classification codes (system scale, subsystem type, owner)
- `architecture-views/` — stubs for all 11 view types (Д-1…О-1)
- CI gate `validate-enterprise` — blocks PR if classification file is missing or invalid

**Ontology domain:** `domains/is-ontology/` — glossary (~34 terms), canonical model, relationship taxonomy, NFR profile (ГОСТ 25020)

**Demo:** `initiatives/INIT-2026-001-ontology-demo/` — complete Enterprise IS profile example

## Governance

Full principles, CI gates strategy, ID conventions, levels (L0–L5), and enforcement roadmap:
→ [`.specify/memory/constitution.md`](./.specify/memory/constitution.md)

## Design Document

→ [`docs/plans/2026-02-28-spec-kit-file-structure-design.md`](./docs/plans/2026-02-28-spec-kit-file-structure-design.md)

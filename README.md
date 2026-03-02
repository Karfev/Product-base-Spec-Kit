# Product-base-Spec-Kit

Build high-quality product faster.

A spec-driven artifact kit for B2B SaaS teams, based on the **Spec Constitution** — an operational system of changes where machine-readable anchors are validated by CI.

---

## Structure

```text
.specify/
  memory/constitution.md     ← L0: Spec Constitution (principles, CI gates, profiles)
  specs/{NNN}-{slug}/        ← L4: Feature spec-kit (spec / plan / tasks / trace)

domains/{domain}/            ← L1: Glossary, canonical model, event catalog, NFR
products/{product}/          ← L2: Architecture, product ADR, NFR baseline
initiatives/{INIT-slug}/     ← L3: PRD, requirements.yml, contracts, ops, decisions

tools/schemas/               ← CI validators (JSON Schema)
evidence/                    ← L5: CI-generated artifacts (RTM, reports)
```

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

## Quick start

1. **New initiative (L3):**
   ```
   /speckit-profile INIT-2026-042-my-feature
   /speckit-init    INIT-2026-042-my-feature
   /speckit-prd     INIT-2026-042-my-feature
   /speckit-requirements INIT-2026-042-my-feature
   ```

2. **New feature spec (L4):**
   ```
   /speckit-specify  042-my-feature
   /speckit-plan     042-my-feature
   /speckit-tasks    042-my-feature
   /speckit-implement 042-my-feature
   /speckit-trace    042-my-feature
   ```

3. **Before release:**
   ```
   /speckit-rtm       INIT-2026-042-my-feature
   /speckit-prr-status INIT-2026-042-my-feature
   /speckit-evidence  INIT-2026-042-my-feature
   ```

4. **Validate manually:**
   ```bash
   make check-all
   ```

## Profiles

| Profile | When | Key artifacts |
|---|---|---|
| **Minimal** | Low-risk changes | prd.md, requirements.yml, CHANGELOG.md |
| **Standard** | Most initiatives | + design.md, contracts/, ADR, slo.yaml, prr-checklist.md |
| **Extended** | High-risk / regulated | + threat-model.md, nfr-validation.md, migration.md, compliance/ |

## Governance

Full principles, CI gates strategy, ID conventions, and enforcement roadmap:
→ `.specify/memory/constitution.md`

## Design doc

→ `docs/plans/2026-02-28-spec-kit-file-structure-design.md`

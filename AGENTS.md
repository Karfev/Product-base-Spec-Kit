# SpecKit — Spec-driven artifact framework

> Five-layer governance for B2B SaaS teams. Machine-readable requirements, CI-validated contracts, traceability from requirements to evidence.

## How to use this repo

All skills are in `.claude/commands/`. Invoke them by name: `/speckit-start`, `/speckit-prd`, etc.

**For first-time users (in priority order):**

1. **Read [`docs/tutorial/INDEX.md`](docs/tutorial/INDEX.md)** — full hands-on course for Dev / Tech Lead (RU, 2 hours).
2. **Or run `/speckit-tutorial`** — interactive 20-minute tour through a sample initiative.
3. **Or run `/speckit-start`** to jump straight to creating your first initiative.

## Quick orientation

- **Architecture overview:** [README.md](README.md#architecture--five-layers)
- **Quick Start (5 min):** [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Governance rules:** [.specify/memory/constitution.md](.specify/memory/constitution.md)
- **Full workflow:** [README.md](README.md#full-workflow--14-steps)

## All skills (32)

### Discovery & Onboarding

| Skill | Description |
|-------|-------------|
| /speckit-tutorial | **NEW.** Interactive guided tour through SpecKit on a sample case (~20 min). Companion to [`docs/tutorial/`](docs/tutorial/INDEX.md). |
| /speckit-start | Guided onboarding — from zero to validated initiative in one session |
| /speckit-quick | Express initiative creation — auto-detect profile from task description |
| /speckit-profile | Select initiative profile (Minimal / Standard / Extended / Enterprise) via risk assessment |
| /speckit-init | Scaffold a new initiative folder with all required artifacts for the chosen profile |
| /speckit-continue | Resume from last checkpoint or show multi-initiative dashboard |

### Requirements & Contracts

| Skill | Description |
|-------|-------------|
| /speckit-prd | Create or update the PRD for an initiative |
| /speckit-requirements | Fill or update requirements.yml for an initiative, then validate |
| /speckit-contracts | Generate or update OpenAPI / AsyncAPI contract stubs from requirements.yml |

### Spec-Driven Workflow (L4)

| Skill | Description |
|-------|-------------|
| /speckit-specify | Create or update a feature spec from a description |
| /speckit-plan | Generate plan.md from a filled spec.md |
| /speckit-tasks | Generate tasks.md from a filled plan.md |
| /speckit-implement | Guide task-by-task implementation from tasks.md |
| /speckit-trace | Generate or update trace.md (RTM) for a feature spec, then verify with make check-trace |

### Release & Evidence

| Skill | Description |
|-------|-------------|
| /speckit-release-rollout | Generate release rollout package (rollout/migration/links) and verify consistency with SLO/PRR |
| /speckit-prr-status | Review PRR checklist status — classify items as DONE / OPEN / BLOCKING |
| /speckit-evidence | Generate an evidence report for an initiative (RTM coverage, PRR status, open gaps) |
| /speckit-rtm | Build the Requirements Traceability Matrix for an initiative by scanning all artifacts |
| /speckit-reflect | Generate structured reflection and evolution proposals for a graduated initiative |

### Domain & Product (L1/L2)

| Skill | Description |
|-------|-------------|
| /speckit-domain-init | Scaffold a new domain spec folder with glossary, canonical model, event catalog, and NFR |
| /speckit-domain-update | Update domain artifacts — add glossary terms, canonical model entities, or events |
| /speckit-product-init | Scaffold a new product spec folder with architecture template, NFR baseline, and decisions/ |
| /speckit-nfr-baseline | Define or update the NFR baseline for a product and surface conflicts with L3 requirements |
| /speckit-adr-product | Create a Product ADR in MADR format via guided questions |
| /speckit-graduate | Graduate knowledge (REQ-IDs, ADRs, contracts) from an initiative to the product layer before archiving |

### Architecture & Audit

| Skill | Description |
|-------|-------------|
| /speckit-architecture | Guide architect through IS ontology layers and generate architecture view stubs for design.md |
| /speckit-consilium | Multi-perspective ADR review — generate domain evaluations from Архкомм-aligned roles |
| /speckit-constitution-review | Audit all L1-L5 artifacts for compliance with the Spec Constitution |

### Visualization

| Skill | Description |
|-------|-------------|
| /speckit-trace-viz | Visualize requirement traceability as a Mermaid diagram (REQ -> ADR -> Contract -> Test -> SLO) |

### GSD Integration (optional)

| Skill | Description |
|-------|-------------|
| /speckit-gsd-bridge | Convert Spec Kit tasks.md to GSD phase plans for parallel wave execution |
| /speckit-gsd-map | Map existing codebase with GSD and route findings to Spec Kit L2 architecture |
| /speckit-gsd-verify | Verify GSD execution results against spec.md and requirements.yml, generate evidence |

> GSD commands require installation: `./tools/init.sh ... --with-gsd`

## Agent setup

| Agent | Setup |
|-------|-------|
| Claude Code | Built-in. See [CLAUDE.md](CLAUDE.md) |
| OpenCode | [docs/SETUP-OPENCODE.md](docs/SETUP-OPENCODE.md) |
| Kilo Code | [docs/SETUP-KILOCODE.md](docs/SETUP-KILOCODE.md) |

## Validation

Run `make check-all` to validate all artifacts.

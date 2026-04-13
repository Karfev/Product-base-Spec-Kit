---
graduated_from: docs/plans/2026-02-28-spec-kit-file-structure-design.md
date: 2026-04-13
type: design-pattern
---

# Architecture Rationale: L0-L5 Hierarchy

## Summary

SpecKit uses a 6-layer artifact hierarchy (L0-L5) with a two-contour workflow model. This document captures the design rationale behind the structure choices made when the repository was created (2026-02-28).

## Two-Contour Workflow

1. **Lifecycle contour (L0-L5):** creates context and change safety frame. Governance, domains, products, initiatives, features, evidence.
2. **Spec-Driven contour (L4):** `spec → plan → tasks → implement` — inner loop within the lifecycle contour.

The contours are complementary: lifecycle provides the scaffolding (what artifacts must exist), spec-driven provides the execution loop (how features are built within that scaffolding).

## Profile System

Risk-based depth selection for L3 initiatives:

| Profile | Artifacts | Trigger |
|---|---|---|
| Minimal | prd.md, requirements.yml, README.md, CHANGELOG.md | Low risk, small scope |
| Standard | + design.md, ADR, contracts/*, rollout.md, slo.yaml, prr-checklist.md | API changes, moderate risk |
| Extended | + threat-model.md, nfr-validation.md, migration.md, compliance/ | PII, regulatory, cross-cutting |
| Enterprise | + IS ontology views, subsystem classification | AIS-class systems |

The profile determines which artifacts are mandatory. Higher profiles include all artifacts from lower profiles.

## CI Gates Rollout Strategy

Phased enforcement to avoid "big bang" adoption friction:

| Weeks | Gates | Mode |
|---|---|---|
| 1-2 | yamllint, markdownlint, requirements schema | warning → blocking |
| 3-4 | traceability RTM, REQ uniqueness | warning |
| 5-6 | OpenAPI/AsyncAPI validate, breaking diff | warning → blocking |
| 7-8 | slo.yaml OpenSLO, PRR gate | blocking on release |
| 9-12 | style rules escalation, domain packs, definition of done by profile | graduated |

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Governance center | `.specify/` directory | Separates framework config from domain content |
| Template syntax | `{placeholder}` in all templates | Copy→fill workflow, grep-friendly |
| L4 location | `.specify/specs/{NNN}-{slug}/` | Keeps feature specs separate from initiative-level docs |
| ID scheme | `INIT-YYYY-NNN-<slug>` | Year-scoped, sortable, ASCII-compatible |

## References

- Constitution (current): `.specify/memory/constitution.md`
- Template initiative: `initiatives/{INIT-YYYY-NNN-slug}/`
- Template spec: `.specify/specs/{NNN}-{slug}/`

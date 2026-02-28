# Design: Product-base-Spec-Kit File Structure

**Date:** 2026-02-28
**Source:** Конституция спецификаций и шаблоны артефактов (PDF, 21 pages)
**Approach:** A — .specify/ as governance center + full L0–L5 hierarchy
**Artifact content:** Full templates with {placeholder} syntax

---

## Goals and Constraints

- Goals: Create a ready-to-use spec-driven kit with full L0–L5 artifact templates
- Constraints: All templates follow {placeholder} syntax; structure matches the PDF constitution exactly
- Profiles: Minimal / Standard / Extended artifacts clearly annotated

---

## Architecture

Two-contour workflow per the constitution:
1. **Lifecycle contour (L0–L5):** creates context and change safety frame
2. **Spec-Driven contour (L4):** `spec → plan → tasks → implement` (compatible with spec-kit)

---

## Full File Structure

```
.specify/
  memory/
    constitution.md                    # L0: Governance — spec constitution, principles, CI gates
  specs/
    {NNN}-{slug}/
      spec.md                          # L4: Feature spec
      plan.md                          # L4: Architecture choices + contracts impact
      tasks.md                         # L4: Task checklist
      trace.md                         # L4: REQ → ADR/API/Schema/Tests/SLO

domains/
  {domain}/
    glossary.md                        # L1 Minimal
    canonical-model/
      model.md                         # L1 Standard+
    event-catalog/
      events.md                        # L1 Standard+
    nfr/
      domain-nfr.md                    # L1 Extended
    regulatory/
      requirements.md                  # L1 Extended

products/
  {product}/
    architecture/
      overview.md                      # L2 Minimal
    decisions/
      {PROD}-0001-{slug}.md            # L2 Standard+ — Product ADR
    nfr-baseline/
      baseline.md                      # L2 Standard+

initiatives/
  {INIT-YYYY-NNN-slug}/
    README.md                          # L3 Minimal — initiative index
    prd.md                             # L3 Minimal — PRD template
    requirements.yml                   # L3 Minimal — machine-readable REQ registry
    trace.md                           # L3 Standard — RTM: REQ → ADR/API/Schema/Tests/SLO
    design.md                          # L3 Standard — arc42-lite
    changelog/
      CHANGELOG.md                     # L3 Minimal — Keep a Changelog + SemVer
    contracts/
      openapi.yaml                     # L3 Standard — OpenAPI 3.1.1 minimal template
      asyncapi.yaml                    # L3 Standard — AsyncAPI template (if applicable)
      schemas/
        {entity}.schema.json           # L3 Standard — JSON Schema entity template
    decisions/
      ADR-template.md                  # L3 Standard — MADR-based ADR template
    delivery/
      rollout.md                       # L3 Standard
      migration.md                     # L3 Extended
    ops/
      slo.yaml                         # L3 Standard — OpenSLO v1
      prr-checklist.md                 # L3 Standard — Production Readiness Review
      nfr-validation.md                # L3 Extended
      threat-model.md                  # L3 Extended
    compliance/
      regulatory-review.md             # L3 Extended

tools/
  schemas/
    requirements.schema.json           # L0: JSON Schema 2020-12 for CI validation

evidence/
  .gitkeep                             # L5: placeholder — CI-generated artifacts go here
```

---

## Artifact Templates Summary

| File | Key fields | Profile | CI validator |
|---|---|---|---|
| `prd.md` | goal, metrics, scope, REQ-IDs | Minimal | markdownlint |
| `requirements.yml` | metadata, requirements[id/type/priority/status/trace] | Minimal | check-jsonschema |
| `design.md` | goals, context, C4, contracts, NFR, ADR links | Standard | markdownlint |
| `spec.md` | summary, motivation, user stories, REQ, AC | Minimal | markdownlint |
| `plan.md` | arch choices, contracts impact, data, SLO | Minimal | markdownlint |
| `tasks.md` | T1–T6 task checklist | Minimal | existence gate |
| `trace.md` | REQ → ADR/Contract/Schema/Tests/SLO table | Standard | trace gate |
| `prr-checklist.md` | P0/P1 readiness items | Standard | PRR gate |
| `slo.yaml` | DataSource/SLI/SLO (OpenSLO v1) | Standard | schema + SLO gate |
| `openapi.yaml` | OpenAPI 3.1.1, paths, schemas | Standard | Redocly/Spectral |
| `asyncapi.yaml` | AsyncAPI channels, messages | Standard | AsyncAPI CLI |
| `ADR-template.md` | MADR front-matter, context, options, outcome | Standard | ADR index |
| `CHANGELOG.md` | Keep a Changelog + SemVer | Minimal | changelog gate |
| `requirements.schema.json` | JSON Schema 2020-12 | L0 | metaschema |

---

## ID Conventions

- Initiative: `INIT-YYYY-NNN-<slug>` (e.g. `INIT-2026-003-export-data`)
- Requirements: `REQ-<SCOPE>-NNN` (e.g. `REQ-AUTH-042`, `REQ-PLAT-003`)
- Platform ADR: `PLAT-0001-<slug>`
- Product ADR: `<PROD>-0001-<slug>`
- Initiative ADR: `<INIT>-ADR-0001-<slug>`

---

## CI Gates Strategy (warning → blocking)

1. Week 1–2: yamllint + markdownlint (warning→blocking), requirements schema (blocking)
2. Week 3–4: traceability RTM (warning), REQ uniqueness (warning)
3. Week 5–6: OpenAPI/AsyncAPI validate (blocking on errors), breaking diff (warning→blocking)
4. Week 7–8: slo.yaml OpenSLO + PRR gate (blocking on release)
5. Week 9–12: style rules escalation, domain packs, definition of done by profile

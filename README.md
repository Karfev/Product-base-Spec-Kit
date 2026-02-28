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

## Quick start

1. **New initiative (L3):**
   ```bash
   cp -r initiatives/{INIT-YYYY-NNN-slug}/ initiatives/INIT-2026-042-my-feature/
   # Edit all {placeholder} values
   ```

2. **New feature spec (L4):**
   ```bash
   cp -r .specify/specs/{NNN}-{slug}/ .specify/specs/042-my-feature/
   # Fill spec.md → plan.md → tasks.md
   ```

3. **Validate requirements.yml:**
   ```bash
   check-jsonschema --schemafile tools/schemas/requirements.schema.json \
     initiatives/INIT-2026-042-my-feature/requirements.yml
   ```

4. **Lint OpenAPI contract:**
   ```bash
   redocly lint initiatives/INIT-2026-042-my-feature/contracts/openapi.yaml
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

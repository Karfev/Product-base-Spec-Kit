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

## Profiles

| Profile | When | Key artifacts |
|---|---|---|
| **Minimal** | Low-risk changes | prd.md, requirements.yml, CHANGELOG.md |
| **Standard** | Most initiatives | + design.md, contracts/, ADR, slo.yaml, prr-checklist.md |
| **Extended** | High-risk / regulated | + threat-model.md, nfr-validation.md, migration.md, compliance/ |
| **Enterprise** | Large IS-class systems | + design.md (3-layer АИС ontology), architecture-views/, subsystem-classification.yaml |

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

Full principles, CI gates strategy, ID conventions, and enforcement roadmap:
→ `.specify/memory/constitution.md`

## Design doc

→ `docs/plans/2026-02-28-spec-kit-file-structure-design.md`

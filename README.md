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
tools/scripts/               ← CI scripts (check-trace, collect-evidence)
evidence/                    ← L5: CI-generated artifacts (RTM, reports)
```

## Quick start

1. **Bootstrap a new initiative + feature spec:**
   ```bash
   ./tools/init.sh INIT-2026-042-my-feature 042-my-feature
   ```

2. **With GSD execution engine (optional):**
   ```bash
   ./tools/init.sh INIT-2026-042-my-feature 042-my-feature --with-gsd
   ```

3. **Spec cycle (Claude Code slash commands):**
   ```bash
   /speckit-specify 042-my-feature   # fill spec.md
   /speckit-plan    042-my-feature   # fill plan.md
   /speckit-tasks   042-my-feature   # generate tasks.md
   /speckit-implement 042-my-feature # implement task-by-task
   ```

4. **Validate:**
   ```bash
   make validate        # requirements.yml schema
   make lint-contracts  # OpenAPI + AsyncAPI
   make check-trace     # REQ-ID consistency
   make check-all       # everything
   ```

## Profiles

| Profile | When | Key artifacts |
|---|---|---|
| **Minimal** | Low-risk changes | prd.md, requirements.yml, CHANGELOG.md |
| **Standard** | Most initiatives | + design.md, contracts/, ADR, slo.yaml, prr-checklist.md |
| **Extended** | High-risk / regulated | + threat-model.md, nfr-validation.md, migration.md, compliance/ |

## GSD Integration (optional)

[GSD](https://github.com/gsd-build/get-shit-done) can replace the linear `/speckit-implement` with wave-based parallel execution and fresh context per agent.

```text
tasks.md → [/speckit-gsd-bridge] → .planning/PLAN.md
         → [/gsd-execute-phase]  → .planning/SUMMARY.md
         → [/speckit-gsd-verify] → evidence/
```

| Scenario | Command |
|---|---|
| Simple feature, < 1 day | `/speckit-implement` (linear) |
| Complex feature, > 1 day | `/speckit-gsd-bridge` + `/gsd-execute-phase` |
| Brownfield codebase | `/speckit-gsd-map` before spec cycle |

Install GSD into an existing project: `./tools/init.sh INIT-... slug --with-gsd`, or `npx get-shit-done-cc@latest --claude --local`.

Full policy: `.specify/memory/constitution.md` → section "GSD-интеграция".

## Governance

Full principles, CI gates strategy, ID conventions, and enforcement roadmap:
→ `.specify/memory/constitution.md`

## Design doc

→ `docs/plans/2026-02-28-spec-kit-file-structure-design.md`

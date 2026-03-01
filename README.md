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

domains/{domain}/                 ← L1: Glossary, canonical model, event catalog, NFR
products/{product}/               ← L2: Architecture, product ADRs, NFR baseline
initiatives/{INIT-YYYY-NNN-slug}/ ← L3: PRD, requirements.yml, contracts, ops, decisions

tools/
  init.sh                         ← Bootstrap: create new initiative + L4 spec from templates
  schemas/                        ← JSON Schema validators for requirements.yml
  scripts/check-trace.py          ← REQ-ID consistency check: L3 ↔ L4

evidence/                         ← L5: CI-generated artifacts (RTM, coverage, PRR status)

.github/workflows/
  validate.yml                    ← Core validation: schema check, lint, trace check
  contracts.yml                   ← Contract validation: OpenAPI lint + breaking diff, AsyncAPI

Makefile                          ← Local task runner
```

---

## Level Hierarchy

| Level | Location | Contents |
|---|---|---|
| **L0** | `.specify/memory/constitution.md` | Governance, principles, CI gates, ID schemes |
| **L1** | `domains/{domain}/` | Glossary, canonical model, event catalog, domain NFR |
| **L2** | `products/{product}/` | Architecture overview, product ADRs, NFR baseline |
| **L3** | `initiatives/{INIT}/` | PRD, requirements.yml, contracts, decisions, ops |
| **L4** | `.specify/specs/{NNN}-{slug}/` | spec.md → plan.md → tasks.md → trace.md |
| **L5** | `evidence/` | CI-generated: RTM, coverage reports, PRR results |

---

## Profiles

Choose a profile based on risk, not team size:

| Profile | When to use | Required artifacts |
|---|---|---|
| **Minimal** | Low-risk, internal changes | `prd.md`, `requirements.yml`, `README.md`, `CHANGELOG.md` |
| **Standard** | Most product initiatives | + `design.md`, `contracts/`, ADR, `rollout.md`, `slo.yaml`, `prr-checklist.md` |
| **Extended** | High-risk, regulated, public API | + `threat-model.md`, `nfr-validation.md`, `migration.md`, `compliance/` |

---

## Quick Start

### 1. Create a new initiative (L3)

```bash
./tools/init.sh INIT-2026-042-my-feature
```

This copies the template, substitutes all `{placeholder}` values, and prints next steps.
To also create a linked L4 feature spec:

```bash
./tools/init.sh INIT-2026-042-my-feature 042-my-feature
```

### 2. Fill the spec with Claude Code

```
/speckit-specify 042-my-feature   # Fill spec.md (problem, user stories, REQ-IDs)
/speckit-plan    042-my-feature   # Fill plan.md (architecture, contracts, SLO impact)
/speckit-tasks   042-my-feature   # Fill tasks.md (T1–T6 implementation checklist)
/speckit-implement 042-my-feature # Guide task-by-task implementation
```

### 3. Validate locally

```bash
make validate        # Validate all requirements.yml against JSON Schema (blocking)
make lint-docs       # Lint YAML + Markdown (warning mode → will become blocking)
make lint-contracts  # Lint OpenAPI/AsyncAPI contracts
make check-trace     # Check REQ-ID consistency: L3 ↔ L4
make check-all       # Run everything
```

---

## ID Conventions

| Artifact | Format | Example |
|---|---|---|
| Initiative | `INIT-YYYY-NNN-{slug}` | `INIT-2026-000-api-key-management` |
| Requirement | `REQ-{SCOPE}-NNN` | `REQ-AUTH-001`, `REQ-PLAT-003` |
| Platform ADR | `PLAT-0001-{slug}` | `PLAT-0001-event-sourcing` |
| Product ADR | `{PROD}-0001-{slug}` | `ANALYTICS-0003-cache-strategy` |
| Initiative ADR | `{INIT}-ADR-0001-{slug}` | `INIT-2026-000-ADR-0001-storage` |
| Feature spec | `NNN-{slug}` | `000-api-key-management` |
| API version | SemVer | `1.0.0`, `2.0.0-beta` |

---

## CI Gates

Two workflows run on every push/PR:

**`validate.yml`** — always runs:
- Validates every `initiatives/*/requirements.yml` against `tools/schemas/requirements.schema.json`
- Checks L3 ↔ L4 REQ-ID consistency via `tools/scripts/check-trace.py`
- Lints all YAML and Markdown (warning mode, escalates to blocking)

**`contracts.yml`** — runs when `initiatives/**/contracts/**` changes:
- Lints all OpenAPI specs with Redocly CLI (blocking on errors)
- Detects breaking changes with `oasdiff` (warning mode, escalates to blocking)
- Validates AsyncAPI specs (warning mode)

Enforcement follows a two-week warning → blocking escalation schedule defined in the constitution.

---

## Claude Code Integration

Four `/speckit.*` commands guide the full spec-to-implementation workflow:

| Command | Input | Output |
|---|---|---|
| `/speckit-specify NNN-slug` | Feature description | `spec.md`: problem, stories, REQ-IDs, acceptance criteria |
| `/speckit-plan NNN-slug` | Filled `spec.md` | `plan.md`: architecture choices, contracts impact, SLO, risks |
| `/speckit-tasks NNN-slug` | Filled `plan.md` | `tasks.md`: T1–T6 checklist (contracts → tests → impl → ops → trace → PRR) |
| `/speckit-implement NNN-slug` | Filled `tasks.md` | One task at a time, commit per task, stop and report |

The T1–T6 task sequence enforces: contracts first → RED tests → GREEN implementation → integration → observability → traceability → production readiness.

---

## Example Initiative

`initiatives/INIT-2026-000-api-key-management/` — Standard profile, `platform` product.

Demonstrates the full artifact set: `prd.md`, `requirements.yml` (5 REQ-IDs validated by schema), `design.md` (arc42-lite), `contracts/openapi.yaml` (OpenAPI 3.1.1), `contracts/schemas/api-key.schema.json`, `decisions/INIT-2026-000-ADR-0001-storage.md`, `ops/slo.yaml` (OpenSLO v1), `ops/prr-checklist.md`, `delivery/rollout.md`.

Linked L4 spec: `.specify/specs/000-api-key-management/`.

---

## Tools Required

Install all validators:

```bash
make install-tools
```

| Tool | Purpose |
|---|---|
| `yamllint` | YAML linting |
| `check-jsonschema` | `requirements.yml` schema validation |
| `markdownlint-cli2` | Markdown linting |
| `@redocly/cli` | OpenAPI lint and validation |
| `@asyncapi/cli` | AsyncAPI validation |
| `oasdiff` | OpenAPI breaking change detection |

---

## Governance

Full principles, CI gates strategy, ID conventions, source-of-truth matrix, and enforcement roadmap:

→ `.specify/memory/constitution.md`

## Design Document

→ `docs/plans/2026-02-28-spec-kit-file-structure-design.md`

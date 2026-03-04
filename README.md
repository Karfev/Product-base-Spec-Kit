# Product-base-Spec-Kit

> A spec-driven artifact kit for B2B SaaS teams — machine-readable requirements,
> CI-validated contracts, and a five-layer governance model from principles to evidence.

![Validate Specs](https://github.com/Karfev/Product-base-Spec-Kit/actions/workflows/validate.yml/badge.svg)
![Validate Contracts](https://github.com/Karfev/Product-base-Spec-Kit/actions/workflows/contracts.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

---

## Why this kit?

B2B SaaS teams accumulate disconnected specs — PRDs in Notion, contracts in Confluence,
requirements in Jira, ADRs scattered across markdown. When any of these drift, integration
bugs, compliance gaps, and slow onboarding follow.

Product-base-Spec-Kit gives a team:

- **One canonical place** for every artifact type (prd, requirements, contracts, ADRs, SLOs)
- **Machine-readable requirements** (`requirements.yml`) validated by CI on every PR
- **Traceability by construction** — REQ-IDs link L3 requirements to L4 specs to tests
- **Risk-calibrated depth** — three profiles so low-risk changes stay lightweight
- **Bootstrap in one command** — `./tools/init.sh` scaffolds a full initiative in seconds
- **Claude Code integration** — `/speckit-*` commands guide spec → plan → tasks → implement

---

## Architecture — Five Layers

```text
Layer  Location                          Purpose
─────  ────────────────────────────────  ──────────────────────────────────────────────────
L0     .specify/memory/constitution.md   Governance: principles, CI gates, ID conventions
L1     domains/{domain}/                 Domain: glossary, canonical model, event catalog, NFR
L2     products/{product}/               Product: architecture, product ADRs, NFR baseline
L3     initiatives/{INIT-slug}/          Initiative: prd.md, requirements.yml, contracts/, ops/
L4     .specify/specs/{NNN}-{slug}/      Feature: spec → plan → tasks → implement → trace
L5     evidence/                         Evidence: CI-generated RTMs, reports (auto-populated)
```

Supporting tooling:

```text
tools/schemas/          JSON Schema validators for requirements.yml
tools/scripts/          check-trace.py — REQ-ID consistency checker
tools/init.sh           Bootstrap: scaffold a full initiative + L4 spec
.github/workflows/      CI: validate.yml + contracts.yml
Makefile                Local task runner (make check-all)
```

---

## Quick Start

### 1. Install tools

```bash
make install-tools
```

Installs: `yamllint`, `check-jsonschema`, `pyyaml`, `markdownlint-cli2`, `@redocly/cli`, `@asyncapi/cli`.
For `oasdiff` (breaking change detection): see <https://github.com/oasdiff/oasdiff>

### 2. Bootstrap a new initiative

```bash
./tools/init.sh INIT-2026-042-my-feature 042-my-feature
```

This creates:

- `initiatives/INIT-2026-042-my-feature/` — full L3 scaffold (prd.md, requirements.yml, contracts/, ops/, decisions/)
- `.specify/specs/042-my-feature/` — L4 spec scaffold (spec.md, plan.md, tasks.md, trace.md)

### 3. Edit requirements and validate

```bash
# Edit initiatives/INIT-2026-042-my-feature/requirements.yml
make validate        # blocks on schema errors
make check-trace     # checks REQ-ID consistency L3 ↔ L4
```

### 4. (Optional) Use Claude Code to fill the spec

```text
/speckit-specify 042-my-feature
```

See [Claude Code Integration](#claude-code-integration) for the full workflow.

### See the demo

A fully worked Standard-profile initiative lives at:
`initiatives/INIT-2026-000-api-key-management/`

---

## Profiles

Choose a profile **by risk, not by size**.

| Profile | When to use | Required artifacts |
|---|---|---|
| **Minimal** | Low-risk / internal changes | prd.md, requirements.yml, CHANGELOG.md |
| **Standard** | Most initiatives | + design.md, contracts/, decisions/, slo.yaml, prr-checklist.md |
| **Extended** | High-risk / regulated | + threat-model.md, nfr-validation.md, migration.md, compliance/ |

The demo initiative (`INIT-2026-000-api-key-management`) uses the **Standard** profile.

---

## CI Gates

Two GitHub Actions workflows run on every PR and push to `main`.

### validate.yml — Core

| Check | Tool | Mode |
|---|---|---|
| `requirements.yml` JSON Schema | `check-jsonschema` | Blocking |
| REQ-ID traceability (L3 ↔ L4) | `check-trace.py` | Blocking |
| YAML hygiene | `yamllint` | Warning → blocking |
| Markdown hygiene | `markdownlint-cli2` | Warning → blocking |

### contracts.yml — Contracts (on `initiatives/**/contracts/**` changes)

| Check | Tool | Mode |
|---|---|---|
| OpenAPI lint | `redocly lint` | Blocking on errors |
| OpenAPI breaking change diff | `oasdiff` | Warning → blocking |
| AsyncAPI validation | `asyncapi validate` | Warning → blocking |

Run all checks locally:

```bash
make check-all
```

---

## Local Commands

```bash
make help            # List all commands
make validate        # Validate all requirements.yml against JSON Schema
make lint-docs       # Lint YAML and Markdown files (warning mode)
make lint-contracts  # Validate OpenAPI and AsyncAPI contracts
make check-trace     # Check REQ-ID consistency (L3 requirements.yml ↔ L4 trace.md)
make check-all       # Run all validation checks
make install-tools   # Install all required validation tools
```

---

## Claude Code Integration

This repository ships four Claude Code slash commands (`.claude/commands/`).
They guide you through the L4 spec-driven workflow step by step.

| Command | What it does |
|---|---|
| `/speckit-specify <NNN>-<slug>` | Create or update `spec.md` — scope, user stories, acceptance criteria |
| `/speckit-plan <NNN>-<slug>` | Generate `plan.md` — technical approach from spec |
| `/speckit-tasks <NNN>-<slug>` | Generate `tasks.md` — implementation tasks with test-first order |
| `/speckit-implement <NNN>-<slug>` | Guide task-by-task implementation, update `trace.md` |

### Typical L4 workflow with Claude Code

```bash
./tools/init.sh INIT-2026-042-my-feature 042-my-feature   # scaffold
```

Then in Claude Code:

```text
/speckit-specify 042-my-feature   # fill spec.md
/speckit-plan 042-my-feature      # fill plan.md
/speckit-tasks 042-my-feature     # fill tasks.md
/speckit-implement 042-my-feature # implement + trace
```

Requirements run through standard CI gates at every step.

---

## Key Artifacts

| Artifact | Format | Purpose |
|---|---|---|
| `requirements.yml` | YAML (JSON Schema validated) | Machine-readable requirements with REQ-IDs, priority, status, trace |
| `prd.md` | Markdown | Product Requirements Document (narrative) |
| `design.md` | Markdown (arc42-lite) | Architecture document |
| `contracts/openapi.yaml` | OpenAPI 3.1.1 | REST API contract |
| `contracts/asyncapi.yaml` | AsyncAPI 3.0 | Event / message contract |
| `decisions/*.md` | MADR | Architecture Decision Records |
| `ops/slo.yaml` | OpenSLO v1 | Service Level Objectives |
| `ops/prr-checklist.md` | Markdown | Production Readiness Review checklist |
| `.specify/specs/{N}/trace.md` | Markdown table | REQ-ID traceability matrix (L3 ↔ L4) |

---

## Governance

Full principles, CI gates strategy, ID conventions, and enforcement roadmap:
→ `.specify/memory/constitution.md`

**Ops → Spec feedback loop:** production incidents and SLO breaches trigger a spec update cycle —
see the Feedback Loop section in the constitution.

To contribute a change to the kit itself, open a PR with:

1. Updated artifact(s)
2. `make check-all` passing
3. An ADR in `decisions/` if the change affects architecture or conventions

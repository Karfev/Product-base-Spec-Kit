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
products/{product}/  →  services/{service-code}/  →  initiatives/{INIT}/
     L2                        L2.5                         L3
(what we build)         (what we offer clients)      (how we improve it)
```

---

This creates:

- `initiatives/INIT-2026-042-my-feature/` — full L3 scaffold (prd.md, requirements.yml, contracts/, ops/, decisions/)
- `.specify/specs/042-my-feature/` — L4 spec scaffold (spec.md, plan.md, tasks.md, trace.md)
- `.specify/specs/{NNN}-{slug}/spec.md` follows canonical sections: Scope, Non-goals, API/Contracts, Test strategy, Rollout (plus Summary, Requirements, Acceptance criteria).

### 3. Edit requirements and validate

```bash
# Edit initiatives/INIT-2026-042-my-feature/requirements.yml
make validate        # blocks on schema errors
make check-trace     # checks REQ-ID consistency L3 ↔ L4
make check-release-rollout # Validate rollout/migration consistency vs ops/slo.yaml + ops/prr-checklist.md
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

| Check | Tool | PR mode | Release mode |
|---|---|---|---|
| OpenAPI lint | `redocly lint` | Blocking on errors | Blocking |
| OpenAPI breaking change diff | `oasdiff` | Blocking | Blocking |
| AsyncAPI validation | `asyncapi validate` | Warning (non-blocking via `ASYNCAPI_ENFORCEMENT_MODE=warning`) | Blocking (`ASYNCAPI_ENFORCEMENT_MODE=blocking`) |

`contracts.yml` sets an explicit enforcement switch from GitHub event context:
- `CONTRACTS_ENFORCEMENT_MODE=pr|release` (transparency for OpenAPI gates)
- `ASYNCAPI_ENFORCEMENT_MODE=warning|blocking` (PR warning vs release blocking)

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
make check-release-rollout # Validate rollout/migration consistency vs ops/slo.yaml + ops/prr-checklist.md
make check-all       # Run all validation checks
make install-tools   # Install all required validation tools
```

---

## Claude Code Integration

This repository ships Claude Code slash commands (`.claude/commands/`) including a release-rollout gate helper.
They guide you through the L4 spec-driven workflow step by step.

| Command | What it does |
|---|---|
| `/speckit-specify <NNN>-<slug>` | Create or update `spec.md` in canonical format (Scope, Non-goals, API/Contracts, Test strategy, Rollout) |
| `/speckit-plan <NNN>-<slug>` | Generate `plan.md` — technical approach from spec |
| `/speckit-tasks <NNN>-<slug>` | Generate `tasks.md` — implementation tasks with test-first order |
| `/speckit-implement <NNN>-<slug>` | Guide task-by-task implementation, update `trace.md` |
| `/speckit-release-rollout <INIT-YYYY-NNN-slug>` | Build release rollout package (`delivery/rollout.md`, migration for Extended/Enterprise), validate SLO/PRR consistency |

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
/speckit-release-rollout INIT-2026-042-my-feature # finalize rollout/migration + consistency checks before release
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

Full principles, CI gates strategy, ID conventions, levels (L0–L5), and enforcement roadmap:
→ [`.specify/memory/constitution.md`](./.specify/memory/constitution.md)

**Ops → Spec feedback loop:** production incidents and SLO breaches trigger a spec update cycle —
see the Feedback Loop section in the constitution.

To contribute a change to the kit itself, open a PR with:

1. Updated artifact(s)
2. `make check-all` passing
3. An ADR in `decisions/` if the change affects architecture or conventions

# Product-base-Spec-Kit

> Spec-driven artifact framework for B2B SaaS teams.
> Machine-readable requirements, CI-validated contracts, five-layer governance from principles to evidence.

![Validate Specs](https://github.com/Karfev/Product-base-Spec-Kit/actions/workflows/validate.yml/badge.svg)
![Validate Contracts](https://github.com/Karfev/Product-base-Spec-Kit/actions/workflows/contracts.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

> **New here?** Start with [Quick Start](docs/QUICKSTART.md) — your first validated initiative in 30 minutes. Or run `/speckit-start` in Claude Code.

---

## Why this kit?

B2B SaaS teams accumulate disconnected specs: PRDs in Notion, contracts in Confluence, requirements in Jira, ADRs scattered across repos. When these drift, integration bugs, compliance gaps, and slow onboarding follow.

Spec Kit gives a team:

- **One canonical place** for every artifact type (PRD, requirements, contracts, ADRs, SLOs)
- **Machine-readable requirements** (`requirements.yml`) validated by CI on every PR
- **Traceability by construction** — REQ-IDs link L3 requirements to L4 specs to tests to SLOs
- **Risk-calibrated depth** — four profiles (Minimal / Standard / Extended / Enterprise) so low-risk changes stay lightweight
- **Bootstrap in one command** — `./tools/init.sh` scaffolds a full initiative in seconds
- **24 Claude Code commands** (`/speckit-*`) guide the full lifecycle: profile -> init -> prd -> requirements -> contracts -> spec -> plan -> tasks -> implement -> trace -> rollout -> evidence

---

## Architecture — Five Layers

```text
Layer  Location                          Purpose
-----  --------------------------------  --------------------------------------------------
L0     .specify/memory/constitution.md   Governance: principles, CI gates, ID conventions
L1     domains/{domain}/                 Domain: glossary, canonical model, event catalog, NFR
L2     products/{product}/               Product: architecture, product ADRs, NFR baseline
L2.5   services/{service-code}/          Service: contracts, SLO, catalogs, billing, RSM
L3     initiatives/{INIT-slug}/          Initiative: prd.md, requirements.yml, contracts/, ops/
L4     .specify/specs/{NNN}-{slug}/      Feature: spec -> plan -> tasks -> implement -> trace
L5     evidence/                         Evidence: CI-generated RTMs, reports
```

Supporting tooling:

```text
tools/schemas/          JSON Schema validators (requirements, services, billing, etc.)
tools/scripts/          CI scripts (check-trace, check-spec-quality, check-release-rollout)
tools/init.sh           Bootstrap: scaffold a full initiative + L4 spec
.github/workflows/      CI: validate.yml + contracts.yml
.claude/commands/       24 Claude Code slash commands for guided workflow
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

### 2. Select a profile

Decide on the conformity profile based on **risk**, not initiative size. In Claude Code:

```text
/speckit-profile INIT-2026-042-my-feature
```

Or answer these questions yourself:

| Question | YES shifts toward |
|---|---|
| Handles auth/tokens? | Standard+ |
| Involves PII/GDPR/SOC2? | Extended (mandatory) |
| Adds public API contracts? | Standard+ |
| Has SLO/SLA commitments? | Standard+ |
| Requires DB migrations? | Standard+ |
| Revenue/data loss risk? | Extended |
| IS-class ArchiMate system? | Enterprise |

Decision tree: 0-1 YES = Minimal, 2-4 = Standard, 5+ or PII = Extended, IS-class = Enterprise.

### 3. Bootstrap a new initiative

```bash
./tools/init.sh INIT-2026-042-my-feature 042-my-feature \
  --profile standard \
  --product platform \
  --owner @platform-team
```

This creates:

- `initiatives/INIT-2026-042-my-feature/` — full L3 scaffold (prd.md, requirements.yml, contracts/, ops/, decisions/)
- `.specify/specs/042-my-feature/` — L4 spec scaffold (spec.md, plan.md, tasks.md, trace.md)

All placeholders (`{INIT-YYYY-NNN-slug}`, `{YYYY-MM-DD}`, `{product}`, `{team}`, profile) are auto-replaced.

**init.sh options:**

| Flag | Purpose | Example |
|---|---|---|
| `--profile` | Conformity profile | `--profile extended` |
| `--product` | Product name (replaces `{product}`) | `--product platform` |
| `--owner` | Team/person (replaces `@{team}`) | `--owner @platform-team` |
| `--with-gsd` | Install GSD parallel execution engine | |
| `--preset archkom` | Enable Archkom governance chain | |

### 4. Fill requirements and validate

```bash
# In Claude Code:
/speckit-prd INIT-2026-042-my-feature           # fill PRD
/speckit-requirements INIT-2026-042-my-feature   # fill requirements.yml

# Validate:
make validate          # blocks on schema errors
make check-trace       # checks REQ-ID consistency L3 <-> L4
```

### 5. Run the L4 spec-driven workflow

```text
/speckit-specify 042-my-feature     # fill spec.md
/speckit-plan 042-my-feature        # fill plan.md from spec
/speckit-tasks 042-my-feature       # fill tasks.md from plan (T1-T6)
/speckit-implement 042-my-feature   # implement task-by-task (T1 -> T6)
/speckit-trace 042-my-feature       # build RTM (trace.md)
```

### 6. Prepare release

```text
/speckit-release-rollout INIT-2026-042-my-feature   # fill rollout.md, validate SLO/PRR
/speckit-prr-status INIT-2026-042-my-feature        # review PRR checklist
/speckit-evidence INIT-2026-042-my-feature           # generate evidence report
```

### 7. Final validation

```bash
make check-all              # all validation checks
make check-release-rollout  # rollout/SLO/PRR consistency
```

---

## Full Workflow — Step by Step

The framework enforces a two-loop workflow:

**Lifecycle loop (L3 Initiative):** Discovery -> Product -> Architecture/Contracts -> Ops/Readiness -> Evidence

**Spec-driven loop (L4 Feature):** spec -> plan -> tasks -> implement

### Phase 1: Discovery & Profiling

| Step | Command | Input | Output |
|---|---|---|---|
| 1 | `/speckit-profile <INIT>` | Risk questionnaire (10 yes/no) | Profile recommendation |
| 2 | `./tools/init.sh <INIT> <slug> --profile ...` | Initiative ID, slug, profile | Full L3 + L4 scaffold |

### Phase 2: Requirements & Contracts

| Step | Command | Input | Output |
|---|---|---|---|
| 3 | `/speckit-prd <INIT>` | 5 structured questions | `prd.md` filled |
| 4 | `/speckit-requirements <INIT>` | PRD scope items | `requirements.yml` with REQ-IDs |
| 5 | `/speckit-contracts <INIT>` | Requirements | `openapi.yaml`, `asyncapi.yaml`, `schemas/` |

**Validation checkpoint:**
```bash
make validate        # requirements schema
make lint-contracts  # OpenAPI + AsyncAPI
```

### Phase 3: L4 Specification Cascade

| Step | Command | Input | Output |
|---|---|---|---|
| 6 | `/speckit-specify <slug>` | Requirements + contracts | `spec.md` (all canonical sections) |
| 7 | `/speckit-plan <slug>` | spec.md | `plan.md` (architecture, contracts impact, risks) |
| 8 | `/speckit-tasks <slug>` | plan.md | `tasks.md` (T1-T6 implementation order) |

**Task order (T1-T6):**
1. **T1:** Update/add contracts -> `make lint-contracts`
2. **T2a:** Write failing tests (RED) -> `make test-unit` + `make test-contract`
3. **T2b:** Implement (GREEN) -> tests pass
4. **T3:** Integration tests -> `make test-integration`
5. **T4:** Observability: metrics, alerts, fill `ops/slo.yaml`
6. **T5:** Update `trace.md` + `CHANGELOG.md` -> `make check-trace`
7. **T6:** Complete PRR checklist items

### Phase 4: Implementation

| Step | Command | What happens |
|---|---|---|
| 9 | `/speckit-implement <slug>` | Finds first unchecked `[ ]` task, implements it, marks `[x]`, commits. Repeat. |

Or for complex features, use GSD parallel execution:
```text
/speckit-gsd-bridge <slug>      # convert tasks to GSD phases
/gsd-execute-phase SPEC-<NNN>   # execute in parallel waves
/speckit-gsd-verify <slug>      # verify coverage
```

### Phase 5: Traceability & Release

| Step | Command | Output |
|---|---|---|
| 10 | `/speckit-trace <slug>` | L4 `trace.md` (REQ-ID -> ADR -> Contract -> Test -> SLO) |
| 11 | `/speckit-rtm <INIT>` | L3 initiative-level RTM |
| 12 | `/speckit-release-rollout <INIT>` | `delivery/rollout.md` filled, SLO/PRR validated |
| 13 | `/speckit-prr-status <INIT>` | PRR checklist: DONE / OPEN / BLOCKING |
| 14 | `/speckit-evidence <INIT>` | `evidence/<INIT>-evidence-report.md` |

**Final gate:**
```bash
make check-all
make check-release-rollout
```

---

## Profiles

Choose a profile **by risk, not by size**.

| Profile | When to use | Required artifacts |
|---|---|---|
| **Minimal** | Low-risk, internal changes | prd.md, requirements.yml, CHANGELOG.md |
| **Standard** | Most initiatives | + design.md, contracts/, decisions/, slo.yaml, prr-checklist.md, rollout.md, trace.md |
| **Extended** | High-risk, regulated, PII | + threat-model.md, nfr-validation.md, migration.md, compliance/ |
| **Enterprise** | Large IS-class systems (AIS) | + design.md (3-layer ontology), architecture-views/, subsystem-classification.yaml |

**Profile decision tree (top-to-bottom, first match wins):**

1. Q9 or Q10 YES -> **Enterprise** (confirm with architect)
2. Q2 (PII/GDPR) YES -> **Extended** (mandatory, not overridable)
3. 5-8 YES answers -> **Extended** (downgrade needs Tech Lead sign-off)
4. 2-4 YES answers -> **Standard**
5. 0-1 YES answers -> **Minimal**
6. **Guard:** Q1 (auth) YES -> minimum **Standard**

Full profile requirements and CI gates -> `.specify/memory/constitution.md`

---

## Claude Code Commands — Full Reference

### L3 Initiative Management

| Command | Description |
|---|---|
| `/speckit-profile <INIT>` | Select profile via risk assessment (10 yes/no questions) |
| `/speckit-init <INIT>` | Scaffold initiative folder with all artifacts for chosen profile |
| `/speckit-prd <INIT>` | Create/update PRD with 5 structured questions |
| `/speckit-requirements <INIT>` | Fill requirements.yml with REQ-IDs, validate schema |
| `/speckit-contracts <INIT>` | Generate OpenAPI/AsyncAPI stubs from requirements |
| `/speckit-release-rollout <INIT>` | Build release package, validate SLO/PRR consistency |
| `/speckit-prr-status <INIT>` | Review PRR checklist: DONE / OPEN / BLOCKING |
| `/speckit-evidence <INIT>` | Generate evidence report (RTM coverage, gaps, recommendation) |
| `/speckit-constitution-review` | Audit all L1-L5 artifacts for compliance |

### L4 Spec-Driven Workflow

| Command | Description |
|---|---|
| `/speckit-specify <slug>` | Create/update spec.md (canonical sections: Scope, Non-goals, API, Tests, Rollout) |
| `/speckit-plan <slug>` | Generate plan.md from spec (architecture, contracts impact, risks) |
| `/speckit-tasks <slug>` | Generate tasks.md from plan (T1-T6, test-first order) |
| `/speckit-implement <slug>` | Guide task-by-task implementation (one task at a time) |
| `/speckit-trace <slug>` | Build L4 trace.md (REQ-ID traceability matrix) |
| `/speckit-rtm <INIT>` | Build L3 initiative-level RTM |

### L1 Domain & L2 Product

| Command | Description |
|---|---|
| `/speckit-domain-init <domain>` | Scaffold domain: glossary, canonical model, event catalog, NFR |
| `/speckit-domain-update <domain>` | Add terms, entities, or events to existing domain |
| `/speckit-product-init <product>` | Scaffold product: architecture, NFR baseline, decisions/ |
| `/speckit-nfr-baseline <product>` | Define/update NFR baseline, surface conflicts with L3 |
| `/speckit-adr-product <product>` | Create product ADR in MADR format |
| `/speckit-architecture <INIT>` | Guide IS ontology layers (Enterprise profile only) |

### GSD Integration (optional)

| Command | Description |
|---|---|
| `/speckit-gsd-bridge <slug>` | Convert tasks.md to GSD phase plans for parallel execution |
| `/speckit-gsd-map <product>` | Map existing codebase (brownfield), route to L2 architecture |
| `/speckit-gsd-verify <slug>` | Verify GSD execution against spec, generate evidence |

---

## Key Artifacts

| Artifact | Format | Validation | Location |
|---|---|---|---|
| `requirements.yml` | YAML (JSON Schema) | `make validate` | `initiatives/<INIT>/` |
| `prd.md` | Markdown | Manual review | `initiatives/<INIT>/` |
| `design.md` | Markdown (arc42-lite) | Manual review | `initiatives/<INIT>/` |
| `openapi.yaml` | OpenAPI 3.1.0 | `make lint-contracts` (redocly) | `initiatives/<INIT>/contracts/` |
| `asyncapi.yaml` | AsyncAPI 3.0.0 | `make lint-contracts` (asyncapi) | `initiatives/<INIT>/contracts/` |
| `decisions/*.md` | MADR | Manual review | `initiatives/<INIT>/decisions/` |
| `slo.yaml` | OpenSLO v1 | `check-release-rollout.py` | `initiatives/<INIT>/ops/` |
| `prr-checklist.md` | Markdown checklist | `/speckit-prr-status` | `initiatives/<INIT>/ops/` |
| `rollout.md` | Markdown | `check-release-rollout.py` | `initiatives/<INIT>/delivery/` |
| `spec.md` | Markdown (canonical sections) | `check-spec-quality.py` | `.specify/specs/<slug>/` |
| `plan.md` | Markdown | `check-spec-quality.py` | `.specify/specs/<slug>/` |
| `tasks.md` | Markdown checklist | `check-spec-quality.py` (T2a<T2b) | `.specify/specs/<slug>/` |
| `trace.md` | Markdown table | `check-trace.py` | `.specify/specs/<slug>/` |
| `evidence-report.md` | Markdown | `/speckit-evidence` | `evidence/` |

---

## ID Conventions

| Entity | Pattern | Example |
|---|---|---|
| Initiative | `INIT-YYYY-NNN-<slug>` | `INIT-2026-042-export-data` |
| Requirement | `REQ-<SCOPE>-NNN` | `REQ-AUTH-001`, `REQ-AUDIT-003` |
| Platform ADR | `PLAT-NNNN-<slug>` | `PLAT-0001-event-bus` |
| Product ADR | `<PROD>-NNNN-<slug>` | `ANALYTICS-0003-cache-strategy` |
| Initiative ADR | `<INIT>-ADR-NNNN-<slug>` | `INIT-2026-003-ADR-0001-storage-strategy` |

REQ-ID rules:
- `<SCOPE>` = 2-16 uppercase alphanumeric chars (domain area)
- `NNN` = zero-padded sequential number
- Pattern validated by JSON Schema: `^REQ-[A-Z0-9]{2,16}-[0-9]{3}$`
- IDs are **immutable** once status moves past `draft`

---

## CI Gates

### validate.yml (on every PR/push)

| Check | Tool | Mode |
|---|---|---|
| `requirements.yml` JSON Schema | `check-jsonschema` | Blocking |
| REQ-ID traceability (L3 <-> L4) | `check-trace.py` | Blocking |
| Spec quality (placeholders, T2a<T2b) | `check-spec-quality.py` | Blocking |
| Enterprise classification | `check-jsonschema` | Blocking (enterprise only) |
| YAML hygiene | `yamllint` | Warning -> blocking |
| Markdown hygiene | `markdownlint-cli2` | Warning -> blocking |

### contracts.yml (on contracts/ changes)

| Check | Tool | PR mode | Release mode |
|---|---|---|---|
| OpenAPI lint | `redocly lint` | Blocking | Blocking |
| OpenAPI breaking changes | `oasdiff` | Blocking | Blocking |
| AsyncAPI validation | `asyncapi validate` | Warning | Blocking |

---

## Local Commands

```bash
make help                  # List all commands
make validate              # Validate all requirements.yml (initiatives)
make validate-services     # Validate all service artifacts (L2.5)
make lint-docs             # Lint YAML and Markdown files
make lint-contracts        # Validate OpenAPI and AsyncAPI contracts
make check-trace           # Check REQ-ID consistency (L3 <-> L4)
make check-spec-quality    # Check .specify specs quality gates
make check-release-rollout # Validate rollout/migration vs SLO/PRR
make collect-evidence      # Collect GSD execution evidence into RTM
make check-all             # Run all validation checks
make install-tools         # Install all required tools
make test-unit             # Run unit tests (override TEST_UNIT_CMD)
make test-contract         # Run contract tests
make test-integration      # Run integration tests
make test-perf             # Run performance tests
```

---

## Enterprise IS Profile

For large information systems following the AIS methodology (ArchiMate 3.2 / GOST R ISO/IEC 25020):

```bash
./tools/init.sh INIT-2026-NNN-my-system NNN-my-system --profile enterprise
```

Then in Claude Code:
```text
/speckit-architecture INIT-2026-NNN-my-system
```

**What you get:**
- `design.md` with three-layer architecture (Activity / Application / Technology)
- `subsystem-classification.yaml` with machine-readable classification codes
- `architecture-views/` with stubs for all 11 view types
- CI gate `validate-enterprise` blocks PR if classification is missing/invalid

**Ontology domain:** `domains/is-ontology/` — glossary, canonical model, relationship taxonomy, NFR profile

---

## Archkom Preset (optional)

For organizations with formal architecture governance:

```bash
./tools/init.sh INIT-... slug --preset archkom
```

Enables extended artifact chain: `brd.md -> prd.md -> hld.md -> ADR -> design.md`

| Level | Trigger | Required |
|---|---|---|
| U0 | Local change | No Archkom |
| U1 | New API / contract change | HLD + ADR + domain reviews |
| U2 | Cross-cutting / high-risk | BRD + PRD + HLD + ADR + all domain reviews |

---

## GSD Integration (optional)

[GSD](https://github.com/gsd-build/get-shit-done) replaces linear `/speckit-implement` with wave-based parallel execution.

```bash
./tools/init.sh INIT-... slug --with-gsd
```

```text
tasks.md -> /speckit-gsd-bridge -> .planning/PLAN.md
         -> /gsd-execute-phase  -> .planning/SUMMARY.md
         -> /speckit-gsd-verify -> evidence/
```

| Scenario | Command |
|---|---|
| Simple feature (< 1 day) | `/speckit-implement` (linear) |
| Complex feature (> 1 day) | `/speckit-gsd-bridge` + `/gsd-execute-phase` |
| Brownfield codebase | `/speckit-gsd-map` before spec cycle |

---

## Repository Structure

```text
Product-base-Spec-Kit/
  .specify/
    memory/constitution.md              <- L0 governance
    specs/{NNN}-{slug}/                 <- L4 feature specs
      spec.md, plan.md, tasks.md, trace.md
  domains/
    {domain}/                           <- L1 domain layer
      glossary.md, canonical-model/, event-catalog/, nfr/
    is-ontology/                        <- IS architecture reference
  products/
    {product}/                          <- L2 product layer
      architecture/, nfr-baseline/, decisions/
  services/
    {service-code}/                     <- L2.5 service layer
      ops/, billing/, responsibilities.yml
  initiatives/
    {INIT-YYYY-NNN-slug}/              <- L3 initiative layer
      prd.md, requirements.yml, design.md
      contracts/ (openapi.yaml, asyncapi.yaml, schemas/)
      decisions/ (ADRs in MADR format)
      ops/ (slo.yaml, prr-checklist.md)
      delivery/ (rollout.md, migration.md)
      changelog/CHANGELOG.md
  evidence/                             <- L5 evidence reports
  tools/
    init.sh                             <- Bootstrap script
    schemas/                            <- JSON Schema validators
    scripts/                            <- Validation scripts
  .claude/commands/                     <- 24 Claude Code skills
  .github/workflows/                    <- CI pipelines
  Makefile                              <- Local task runner
```

---

## Demo Initiatives

| Initiative | Profile | Description |
|---|---|---|
| `INIT-2026-000-api-key-management` | Extended | API key CRUD, bcrypt hashing, rate limiting. Fully worked reference. |
| `INIT-2026-001-ontology-demo` | Enterprise | IS architecture ontology demo |
| `INIT-2026-002-notification-preferences` | Standard | User notification preferences (channels, frequency, opt-out) |
| `INIT-2026-003-audit-log` | Standard | Audit log infrastructure (E2E dogfooding test initiative) |

---

## Governance

Full principles, CI gates strategy, ID conventions, and enforcement roadmap:
[`.specify/memory/constitution.md`](./.specify/memory/constitution.md)

**Ops -> Spec feedback loop:** Production incidents and SLO breaches trigger a spec update cycle.

To contribute a change to the kit itself:

1. Updated artifact(s)
2. `make check-all` passing
3. An ADR in `decisions/` if the change affects architecture or conventions

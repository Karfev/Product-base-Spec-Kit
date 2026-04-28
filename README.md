# Product-base-Spec-Kit

> Spec-driven artifact framework for B2B SaaS teams.
> Machine-readable requirements, CI-validated contracts, five-layer governance from principles to evidence.

![Validate Specs](https://github.com/Karfev/Product-base-Spec-Kit/actions/workflows/validate.yml/badge.svg)
![Validate Contracts](https://github.com/Karfev/Product-base-Spec-Kit/actions/workflows/contracts.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

> **New here?**
>
> - 📘 **Hands-on tutorial (RU, ~2 hours):** [`docs/tutorial/INDEX.md`](docs/tutorial/INDEX.md) — пошаговый курс для Dev / Tech Lead с worked example и разбором всех артефактов.
> - ⚡ **Quick Start (5 min):** [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — first validated initiative in 30 minutes.
> - 🤖 **With AI agent:** run `/speckit-tutorial` (interactive 20-min tour) or `/speckit-start` (create new initiative).

---

## Why this kit?

B2B SaaS teams accumulate disconnected specs: PRDs in Notion, contracts in Confluence, requirements in Jira, ADRs scattered across repos. When these drift, integration bugs, compliance gaps, and slow onboarding follow.

Spec Kit gives a team:

- **One canonical place** for every artifact type (PRD, requirements, contracts, ADRs, SLOs)
- **Machine-readable requirements** (`requirements.yml`) validated by CI on every PR
- **Traceability by construction** — REQ-IDs link L3 requirements to L4 specs to tests to SLOs
- **Risk-calibrated depth** — four profiles (Minimal / Standard / Extended / Enterprise) so low-risk changes stay lightweight
- **Bootstrap in one command** — `./tools/init.sh` scaffolds a full initiative in seconds
- **32 slash commands** (`/speckit-*`) guide the full lifecycle: profile -> init -> prd -> requirements -> contracts -> spec -> plan -> tasks -> implement -> trace -> rollout -> evidence

## Agent Compatibility

SpecKit skills use the [SKILL.md](https://github.com/anthropics/skill-md) standard and work with multiple AI coding agents:

| Agent | Custom Commands | AGENTS.md | Local LLM | Setup Guide |
|-------|:--------------:|:---------:|:---------:|-------------|
| Claude Code | ✅ Native | ✅ | ❌ Cloud only | Built-in |
| OpenCode | ✅ via symlink | ✅ | ✅ Ollama | [Setup](docs/SETUP-OPENCODE.md) |
| Kilo Code (VS Code / JetBrains) | ✅ Native | ✅ | ✅ Ollama/vLLM | [Setup](docs/SETUP-KILOCODE.md) |
| Codex CLI | ❌ | ✅ | ❌ Cloud only | — |

27 of 31 commands are fully portable (file I/O + bash). 4 GSD commands require optional GSD installation.
See [AGENTS.md](AGENTS.md) for the complete skill catalog and [docs/COMPAT-MATRIX.md](docs/COMPAT-MATRIX.md) for detailed compatibility.

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
.claude/commands/       32 slash commands (SKILL.md standard)
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

Decide on the conformity profile based on **risk**, not initiative size. Run:

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
| `--with-example` | Copy golden reference initiative to `examples/` | |

### 4. Fill requirements and validate

```bash
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

**Test type selection (which tests are mandatory):**

| Requirement type | Test type | When mandatory | Command |
|---|---|---|---|
| functional | unit | Always for business logic | `make test-unit` |
| functional | contract | Standard+ with API changes | `make test-contract` |
| functional | integration | DB/external service/queue | `make test-integration` |
| nfr | perf | NFR by latency/throughput | `make test-perf` |

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

## Slash Commands

See [AGENTS.md](AGENTS.md) for the complete catalog of 32 slash commands with descriptions.

**By workflow phase:**
- **Discovery:** `/speckit-start`, `/speckit-quick`, `/speckit-profile`, `/speckit-continue`
- **L3 Initiative:** `/speckit-init`, `/speckit-prd`, `/speckit-requirements`, `/speckit-contracts`
- **L4 Spec-Driven:** `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`
- **Release & Evidence:** `/speckit-trace`, `/speckit-rtm`, `/speckit-evidence`, `/speckit-prr-status`, `/speckit-release-rollout`, `/speckit-graduate`, `/speckit-reflect`
- **Domain & Product:** `/speckit-domain-init`, `/speckit-domain-update`, `/speckit-product-init`, `/speckit-nfr-baseline`, `/speckit-adr-product`
- **Architecture & Audit:** `/speckit-architecture`, `/speckit-constitution-review`, `/speckit-consilium`
- **Visualization:** `/speckit-trace-viz`
- **GSD (optional):** `/speckit-gsd-bridge`, `/speckit-gsd-map`, `/speckit-gsd-verify`

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
| Initiative ADR | `<INIT>-ADR-NNNN-<slug>` | `INIT-2026-000-ADR-0001-storage` |

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

Then run:
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
    specs/000-api-key-management/       <- L4 golden reference
    specs/{NNN}-{slug}/                 <- L4 template
  domains/
    is-ontology/                        <- L1 reference (Enterprise IS)
    {domain}/                           <- L1 template
  products/
    platform/                           <- L2 reference (graduated knowledge)
    {product}/                          <- L2 template
  services/
    example-vm-hosting/                 <- L2.5 reference (anonymized)
    {service-code}/                     <- L2.5 template
  initiatives/
    INIT-2026-000-api-key-management/   <- L3 golden reference (Standard)
    INIT-2026-001-ontology-demo/        <- L3 reference (Enterprise)
    {INIT-YYYY-NNN-slug}/              <- L3 template
      prd.md, requirements.yml, design.md
      contracts/ (openapi.yaml, asyncapi.yaml, schemas/)
      decisions/ (ADRs in MADR format)
      ops/ (slo.yaml, prr-checklist.md)
      delivery/ (rollout.md, migration.md)
      changelog/CHANGELOG.md
  tests/                                <- Test stubs (traceability demo)
  evidence/                             <- L5 evidence reports
  tools/
    init.sh                             <- Bootstrap script
    schemas/                            <- JSON Schema validators
    scripts/                            <- Validation scripts
    requirements.txt                    <- Pinned Python dependencies
    package.json                        <- Pinned Node dependencies
  .claude/commands/                     <- 32 slash commands (SKILL.md)
  .github/workflows/                    <- CI pipelines
  Makefile                              <- Local task runner
```

---

## Golden Reference

The repository includes two fully worked reference initiatives that demonstrate the framework in action.

To copy the golden reference into your project for side-by-side comparison:

```bash
./tools/init.sh INIT-2026-042-my-feature 042-my-feature --profile standard --with-example
```

| Initiative | Profile | Purpose |
|---|---|---|
| `INIT-2026-000-api-key-management` | Standard | **Golden reference.** Complete L3 initiative + L4 spec + test stubs + evidence report. Start here. |
| `INIT-2026-001-ontology-demo` | Enterprise | Enterprise IS profile reference: 3-layer architecture, subsystem classification, architecture views. |

**INIT-2026-000** demonstrates the full traceability chain: `requirements.yml` → `contracts/openapi.yaml` → `decisions/ADR-0001` → `tests/api/api-keys.spec.ts` → `ops/slo.yaml` → `evidence/`.

---

## Governance

Full principles, CI gates strategy, ID conventions, and enforcement roadmap:
[`.specify/memory/constitution.md`](./.specify/memory/constitution.md)

**Ops -> Spec feedback loop:** Production incidents and SLO breaches trigger a spec update cycle.

To contribute a change to the kit itself:

1. Updated artifact(s)
2. `make check-all` passing
3. An ADR in `decisions/` if the change affects architecture or conventions

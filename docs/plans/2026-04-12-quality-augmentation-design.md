# Quality Augmentation Design

**Initiative:** INIT-2026-007-quality-augmentation
**Date:** 2026-04-12
**Approach:** Sequential (Spec 008 consilium → Spec 010 ai-quality-gates)

## Goal

Add two quality mechanisms to SpecKit: (1) multi-perspective ADR review via `/speckit-consilium`, (2) codified AI quality constraints via Five Pillars + enforcement in `/speckit-implement` + CI detection.

## Architecture

Sequential execution: Phase 1 (consilium) completes before Phase 2 (quality gates). Both features target Standard+ profile only.

- **Consilium:** Sequential role-switching pattern (one agent, multiple roles). Roles defined in YAML config. Output compatible with ADR-template-v2 "Доменные оценки" section.
- **Quality Gates:** Markdown document (human-readable, agent-interpreted). Primary enforcement via prompts in `/speckit-implement`. CI backup via `check-spec-quality.py` for T2a/T2b ordering.

## Phase 1: Consilium (Spec 008)

### New files

1. **`.specify/memory/consilium-roles.yml`** — 5 base roles (arch, security, db-load, infra, integrations) + 3 presets (standard, archkom-l1, archkom-l2). Each role: id, name, context_files, checklist, verdict format.

2. **`.claude/commands/speckit-consilium.md`** — Command: parse ADR path → determine panel (--preset/--roles/auto by profile) → sequential role execution (load context → analyze by checklist → verdict) → aggregate → inject "Доменные оценки" section into ADR.

### Algorithm

```
INPUT: ADR file path + profile (optional) + --roles/--preset (optional)

STEP 1: Determine panel
  --roles flag → custom roles from consilium-roles.yml
  --preset flag → preset from consilium-roles.yml
  auto → profile mapping (Standard→standard, Extended→archkom-l1, Enterprise→archkom-l2)

STEP 2: For each role (sequential):
  a. Load role definition + context files
  b. Read ADR content
  c. Evaluate checklist items → OK / Замечание / Блокер
  d. Generate structured review with artifact references

STEP 3: Aggregate
  Any Блокер → "требует доработки"
  Only Замечания → "одобрено с условиями"
  All OK → "одобрено"

STEP 4: Inject "Доменные оценки" section into ADR
```

### PoC

Run on `products/platform/decisions/PLAT-0003-async-queue.md` with standard preset (3 roles: arch, security, infra). Verify output format matches ADR-template-v2.

## Phase 2: AI Quality Gates (Spec 010)

### New file

1. **`tools/ai-quality-gates.md`** — Five Pillars:
   - Decomposition (max 50 LOC/method)
   - Test-First (T2a before T2b)
   - Architecture-First (stubs before logic)
   - Focused Work (one task = one bounded context)
   - Contract-Aware (implementation matches OpenAPI/AsyncAPI)

### Modifications

2. **`.claude/commands/speckit-implement.md`** — Pre-flight checklist before T2b:
   - T2a tests written and failing?
   - Architecture stubs created?
   - Stubs match contracts (make lint-contracts)?
   - Scope declared?
   - Warning if any unchecked, proceed if all checked.

3. **`tools/scripts/check-spec-quality.py`** — New `check_task_ordering()`:
   - Parse tasks.md checkboxes
   - Detect T2b `[x]` without T2a `[x]` → CI WARNING

## Phase 3: Closure

- Update requirements.yml: 6 REQ-IDs → status: implemented + trace links
- Update CHANGELOG.md: v0.2.0
- Run `make check-all` validation

## Key decisions

| Decision | Choice | Rationale |
|---|---|---|
| Role definitions | YAML config | Extensible without modifying command |
| Execution model | Sequential role switching | No coordination complexity |
| Quality gates format | Markdown | Agent reads and interprets naturally |
| Enforcement | Agent prompts + CI backup | Primary: prompt in implement, safety net: check-spec-quality.py |
| Scope | Standard+ only | Minimal = quick fix, overhead unjustified |

## Files affected

| File | Action | Phase |
|---|---|---|
| `.specify/memory/consilium-roles.yml` | CREATE | 1 |
| `.claude/commands/speckit-consilium.md` | CREATE | 1 |
| `tools/ai-quality-gates.md` | CREATE | 2 |
| `.claude/commands/speckit-implement.md` | MODIFY | 2 |
| `tools/scripts/check-spec-quality.py` | MODIFY | 2 |
| `initiatives/INIT-2026-007-.../requirements.yml` | MODIFY | 3 |
| `initiatives/INIT-2026-007-.../changelog/CHANGELOG.md` | MODIFY | 3 |

## Risk mitigations

| Risk | Mitigation |
|---|---|
| Shallow "OK" reviews from consilium | Checklist items require specific artifact references |
| Context window overload (5 roles x files) | Max 500 tokens per context file, heading-level extraction |
| Quality gates too strict | Gates = warnings, not hard blocks (except T2a→T2b) |
| T2b-before-T2a false positives | Strict `[x]` pattern parsing only |
| ADR format drift | Section injection by markdown heading, not line number |

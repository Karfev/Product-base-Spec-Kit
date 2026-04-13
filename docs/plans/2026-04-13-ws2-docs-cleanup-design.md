# WS2: Documentation Cleanup Design

**Date:** 2026-04-13
**Scope:** Orphaned docs removal, knowledge graduation, broken references, README deduplication
**Predecessor:** WS1 (162 files deleted: 9 initiatives + specs + domains + services)

---

## Context

WS1 removed 9 initiatives (INIT-002 through INIT-010) and their L3/L4/L5 artifacts, but left behind:
- 7 design/implementation plans in `docs/plans/` (5,410 lines = 35% of all docs)
- A superseded constitution v1 (298 lines, zero inbound references)
- Broken cross-references in SETUP guides and initiative registry
- 87% duplication between README Slash Commands section and AGENTS.md

Deep analysis revealed that 4 of 7 plan files contain reusable architectural knowledge that should be graduated before deletion.

---

## Part 1: Graduate Knowledge from Design Docs

### What gets graduated

| Source | Graduate to | Extracted patterns |
|---|---|---|
| `quality-augmentation-design.md` | `.specify/memory/presets/quality-governance.md` | Consilium multi-perspective review: sequential role-switching (arch → security → db-load → infra → integrations), verdict aggregation (Блокер/Замечание/OK), preset system (standard/archkom-l1/archkom-l2). Five Pillars: Decomposition (max 50 LOC), Test-First (T2a→T2b), Architecture-First (stubs before logic), Focused Work (one task = one bounded context), Contract-Aware. |
| `smart-discovery-design.md` | `.specify/memory/presets/discovery-patterns.md` | Auto-routing algorithm: risk-keyword scan → component count → profile suggestion → user confirm/override. Codebase-first context loading: question→file mapping table (PRD question → L1/L2/L3 artifact → section extraction → proposed answer with staleness warning). Depth modes: Quick (3-5 Q) / Standard (5-10 Q) / Deep (10-15 Q). |
| `session-state-and-self-evolution-design.md` | `.specify/memory/presets/session-protocol-design.md` | 8-step session middleware: read/create → update header → mark progress → compute next → append decisions → sync questions → update context files → write back. Lifecycle sequence: start → prd → requirements → contracts → specify → plan → tasks → implement → trace → rtm → consilium → graduate. Phase→context files table for selective loading. |
| `spec-kit-file-structure-design.md` | `.specify/memory/architecture-rationale.md` | L0-L5 hierarchy rationale: two-contour workflow (lifecycle + spec-driven), profile system (Minimal/Standard/Extended), CI gates phased rollout strategy (warning→blocking over weeks 1-12), artifact template conventions ({placeholder} syntax). |

### Format of graduated files

Each file: ~40-60 lines. Structure:

```markdown
---
graduated_from: docs/plans/{original-file}
date: 2026-04-13
type: design-pattern
---

# {Pattern Name}

## Summary
{2-3 sentences: what, why, when to use}

## Pattern
{Core algorithm/workflow/rules — distilled, not copied verbatim}

## Key Decisions
{Table: decision → choice → rationale}

## References
- Implemented in: {list of active files that use this pattern}
- Risk keywords: `.specify/memory/risk-keywords.yml`
- Consilium roles: `.specify/memory/consilium-roles.yml`
```

### Files deleted after graduation

All 7 files in `docs/plans/`:
- `2026-02-28-spec-kit-file-structure-design.md` (134 lines)
- `2026-02-28-spec-kit-file-structure.md` (2,086 lines)
- `2026-04-12-quality-augmentation-design.md` (114 lines)
- `2026-04-12-quality-augmentation-implementation.md` (840 lines)
- `2026-04-12-smart-discovery-design.md` (259 lines)
- `2026-04-12-smart-discovery-implementation.md` (580 lines)
- `2026-04-12-session-state-and-self-evolution-design.md` (1,082 lines)

Also delete empty `docs/plans/` directory.

**Net:** -5,410 lines removed, +~200 lines graduated.

---

## Part 2: Delete Remaining Orphans

| File | Lines | Reason |
|---|---|---|
| `.specify/memory/constitution-v1-full.md` | 298 | Superseded by v2.0.0. Zero inbound references from any file. |
| `tools/ai-quality-gates.md` | 198 | Content graduated to quality-governance.md. Only referenced from deleted plan files. |
| `docs/testing/test-strategy.md` | 35 | Content preserved via reference link added to README (see Part 4). Move essential info into graduated quality-governance.md under "Test ordering" section. |

**Net:** -531 lines.

---

## Part 3: Fix Broken References

### 3.1 SETUP guides — INIT-005 ADR link

**`docs/SETUP-KILOCODE.md` line 66:**
```
See [ADR: Model Selection](../initiatives/INIT-2026-005-.../ADR-0001-model-selection.md).
```
**Fix:** Remove the broken link. The model recommendation table already exists inline at lines 68-73. Change to:
```
> Model recommendations are in the table below.
```

**`docs/SETUP-OPENCODE.md` line 37:**
Same pattern — remove broken link, rely on inline content.

### 3.2 SETUP-KILOCODE command count

Line 38: "all 26 SpecKit skills" → "all 31 SpecKit skills"

### 3.3 README — GEMINI.md broken link

Line 37: references `docs/GEMINI.md` which doesn't exist.
**Fix:** Remove the Gemini row from the agent compatibility table or add note "setup guide planned". Decision: remove row — Gemini CLI is unsupported, listing it creates false expectations.

### 3.4 Initiative registry

`initiatives/README.md`: Remove rows for INIT-002 through INIT-007 (folders deleted in WS1). Resulting table:

| ID | Initiative | Status |
|---|---|---|
| INIT-2026-000 | api-key-management | active |
| INIT-2026-001 | ontology-demo | active |
| INIT-2026-008 | contracts-graduation | infra-only |
| INIT-2026-009 | smoke-test | archived |

### 3.5 COMPAT-MATRIX command count

`docs/COMPAT-MATRIX.md`: Update "26 skills" → "31 skills" throughout.

---

## Part 4: README Minimal Cleanup

### Remove Slash Commands section (lines ~270-316)

87% overlap with AGENTS.md. Replace ~50 lines with:

```markdown
## Slash Commands

See [AGENTS.md](AGENTS.md) for the complete catalog of 31 slash commands organized by workflow phase.

**Quick reference by phase:**
- **L3 Initiative:** /speckit-start, -profile, -init, -prd, -requirements, -contracts
- **L4 Spec-Driven:** /speckit-specify, -plan, -tasks, -implement
- **Release & Evidence:** /speckit-trace, -rtm, -evidence, -prr-status, -release-rollout, -graduate, -reflect
- **Domain & Product:** /speckit-domain-init, -domain-update, -product-init, -nfr-baseline, -adr-product
- **Architecture & Audit:** /speckit-architecture, -constitution-review, -consilium
- **GSD (optional):** /speckit-gsd-bridge, -gsd-map, -gsd-verify
- **Visualization:** /speckit-trace-viz
- **Utility:** /speckit-start, -continue, -quick
```

This preserves scanability (user can see all commands at a glance) while eliminating the 4-table duplication. ~15 lines vs ~50 lines.

### Fix command count

Line 25: verify "31 slash commands" matches actual count in AGENTS.md + codebase.

### Add test-strategy cross-reference

In Full Workflow section (~line 210), after T2a/T2b description, add:
```
> See `docs/testing/test-strategy.md` for the full requirement-type → test-type decision matrix.
```

Wait — we're deleting test-strategy.md (Part 2). Instead, add the cross-reference to the graduated quality-governance.md. Or better: inline the essential test ordering content (3-4 lines) into the Full Workflow section since test-strategy.md was only 35 lines.

**Decision:** Inline the test-type mapping table (6 rows) from test-strategy.md directly into Full Workflow section of README, replacing the bare T2a/T2b mention. Net: +6 lines, -35 lines (deleted file). This follows the "single source of truth" principle — the README already describes the workflow.

**README after:** ~470 lines (from 537). -50 (slash commands) +15 (compact reference) +6 (test mapping) = ~508 → wait, let me recalculate: 537 - 50 (removed section) + 15 (compact replacement) + 6 (test mapping) - 1 (Gemini row removed) = ~507 lines. Not ~470 as estimated.

Correction: README will be ~507 lines, not 470. The savings come from slash commands deduplication (-35 net lines).

---

## Summary of Changes

### Created (5 files, ~200 lines)
| File | Lines | Purpose |
|---|---|---|
| `.specify/memory/presets/quality-governance.md` | ~50 | Consilium pattern + Five Pillars |
| `.specify/memory/presets/discovery-patterns.md` | ~50 | Auto-routing + codebase-first loading |
| `.specify/memory/presets/session-protocol-design.md` | ~60 | Session middleware + lifecycle sequence |
| `.specify/memory/architecture-rationale.md` | ~40 | L0-L5 hierarchy + two-contour rationale |

### Deleted (10 files, -5,941 lines)
| File | Lines |
|---|---|
| `docs/plans/*` (7 files) | -5,410 |
| `.specify/memory/constitution-v1-full.md` | -298 |
| `tools/ai-quality-gates.md` | -198 |
| `docs/testing/test-strategy.md` | -35 |

### Modified (6 files)
| File | Change |
|---|---|
| `README.md` | Remove slash commands section → compact reference. Fix Gemini row. Add test mapping. |
| `docs/SETUP-KILOCODE.md` | Fix INIT-005 broken link. Fix command count 26→31. |
| `docs/SETUP-OPENCODE.md` | Fix INIT-005 broken link. |
| `initiatives/README.md` | Remove INIT-002 through INIT-007 rows. |
| `docs/COMPAT-MATRIX.md` | Update command count 26→31. |

### Net impact
- **Files:** -10 deleted, +4 created = **-6 net files**
- **Lines:** -5,941 deleted, +200 created = **~-5,740 net lines**
- **README:** 537 → ~507 lines (-30 lines, -5.6%)

---

## Verification

```bash
# 1. No broken references to deleted initiatives
grep -r "INIT-2026-005" docs/ initiatives/ --include="*.md"   # expect: 0 matches
grep -r "INIT-2026-00[2-7]" initiatives/README.md             # expect: 0 matches
grep -r "constitution-v1-full" . --include="*.md"              # expect: 0 matches
grep -r "ai-quality-gates" . --include="*.md"                  # expect: only quality-governance.md
grep -r "GEMINI" README.md                                     # expect: 0 matches

# 2. Graduated files exist and are valid
ls -la .specify/memory/presets/quality-governance.md
ls -la .specify/memory/presets/discovery-patterns.md
ls -la .specify/memory/presets/session-protocol-design.md
ls -la .specify/memory/architecture-rationale.md

# 3. docs/plans/ is gone
test ! -d docs/plans && echo "OK: docs/plans/ removed"

# 4. File counts
find docs/ -name "*.md" | wc -l     # expect: 4 (QUICKSTART, COMPAT-MATRIX, SETUP-x2)
wc -l README.md                      # expect: ~507

# 5. CI validation
make validate
```

---

## Execution Order

1. Graduate knowledge (create 4 new files)
2. Delete docs/plans/ (7 files) + constitution-v1-full + ai-quality-gates + test-strategy
3. Fix broken references (5 files)
4. README cleanup (slash commands dedup + test mapping + Gemini fix)
5. Verify (grep checks + make validate)

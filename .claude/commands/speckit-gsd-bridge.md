---
description: Convert Spec Kit tasks.md to GSD phase plans for parallel wave execution
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

You are converting `.specify/specs/$ARGUMENTS/` task list into GSD `.planning/` phase plans for wave-based parallel execution.

## Prerequisites — validate before proceeding

1. Read `.specify/specs/$ARGUMENTS/tasks.md` — MUST exist and have no `{placeholder}` tokens
2. Read `.specify/specs/$ARGUMENTS/spec.md` — for acceptance criteria
3. Read `.specify/specs/$ARGUMENTS/plan.md` — for architecture context, file paths, ADR refs
4. Resolve the initiative ID from `spec.md`'s `Initiative:` field
5. Read `initiatives/{INIT}/requirements.yml` — for REQ-IDs and trace entries
6. Verify GSD is installed: `.claude/commands/gsd/` directory MUST exist. If not — stop and tell the user to install GSD first (`npx get-shit-done-cc@latest --claude --local`)

## Generate phase structure

Create directory: `.planning/phases/SPEC-$ARGUMENTS/`

### 1. Generate CONTEXT.md

Write `.planning/phases/SPEC-$ARGUMENTS/CONTEXT.md` — a digest (<200 lines) combining:
- Summary + scope + non-goals from spec.md
- Architecture choices + data changes from plan.md
- REQ-ID list with titles and acceptance criteria from requirements.yml
- Relevant ADR references from plan.md
- File paths that will be modified (from plan.md contracts/data/observability sections)

This file is what every GSD subagent reads for context.

### 2. Generate PLAN.md files by wave mapping

Map tasks.md T1–T6 to GSD waves using this dependency graph:

| Wave | Plan file | Spec Kit task | depends_on | Notes |
|------|-----------|---------------|------------|-------|
| 1 | `01-01-PLAN.md` | T1 — Contracts | `[]` | Sequential, foundation |
| 2 | `01-02-PLAN.md` | T2a — RED tests | `["01"]` | Tests MUST fail |
| 3 | `01-03-PLAN.md` | T2b — Implementation | `["02"]` | Parallel with 04 |
| 3 | `01-04-PLAN.md` | T4 — Observability | `["02"]` | Parallel with 03 |
| 4 | `01-05-PLAN.md` | T3 — Integration tests | `["03"]` | Depends on implementation |
| 5 | `01-06-PLAN.md` | T5 — Trace + changelog | `["03", "04"]` | Parallel with 07 |
| 5 | `01-07-PLAN.md` | T6 — PRR checklist | `["03", "04"]` | Parallel with 06 |

If tasks.md marks T3 as "N/A" or absent — skip Plan 05 (Wave 4) and adjust dependencies: Wave 5 depends on `["03", "04"]` directly.

Each PLAN.md MUST follow this structure:

```markdown
---
phase: SPEC-$ARGUMENTS
plan: XX
type: execute
wave: N
depends_on: ["YY", ...]
files_modified: [list from plan.md]
autonomous: true
requirements: [REQ-IDs this plan addresses]
---

## Task 1: <description from tasks.md>

- **read_first**: [files the agent must read before acting — contracts, existing code, test patterns]
- **action**: <explicit instruction derived from tasks.md — what to create/modify and how>
- **verify**: <Makefile target or test command — e.g., `make lint-contracts`, `npm test -- --grep "api-keys"`>
- **acceptance_criteria**: <grep-verifiable criterion — e.g., "openapi.yaml contains path /api-keys", "test suite exits with code 1 (RED)">
- **commit**: `feat($ARGUMENTS): complete T<N> — <brief description>`
- **requirements_addressed**: [REQ-IDs]
```

Rules for PLAN.md generation:
- Derive `read_first` from plan.md file references and existing codebase paths
- Derive `verify` from Makefile targets: `make lint-contracts` (T1), test runner (T2a/T2b/T3), `make check-trace` (T5), `make check-all` (T5/T6)
- Acceptance criteria MUST be grep-verifiable, never subjective ("looks good")
- T2a acceptance criteria MUST include "tests execute and FAIL" (RED phase)
- T2b acceptance criteria MUST include "tests execute and PASS" (GREEN phase)
- Keep each plan to 1-2 tasks max (GSD constraint: fits single context window)
- `files_modified` for Wave 3 plans MUST NOT overlap (enables true parallel execution)

### 3. Generate STATE.md

Write `.planning/phases/SPEC-$ARGUMENTS/STATE.md`:

```markdown
# State: SPEC-$ARGUMENTS

## Position
- Phase: SPEC-$ARGUMENTS
- Current wave: 1
- Plans: 7 total (01-07)
- Status: Ready to execute

## Source artifacts
- Spec: .specify/specs/$ARGUMENTS/spec.md
- Plan: .specify/specs/$ARGUMENTS/plan.md
- Tasks: .specify/specs/$ARGUMENTS/tasks.md
- Requirements: initiatives/{INIT}/requirements.yml

## Decisions
(none yet — updated during execution)

## Blockers
(none)
```

## Output

After generating all files, print:

1. Wave execution plan table (wave → plans → tasks → parallel?)
2. Total plans generated
3. REQ-ID coverage check: every REQ-ID from requirements.yml appears in at least one plan
4. Next step: `Run /gsd-execute-phase SPEC-$ARGUMENTS to begin wave-based execution`

## Rules

- See `.specify/memory/constitution.md` section "Permission boundaries" for the full policy
- NEVER modify any file outside `.planning/` — this command only generates GSD artifacts
- NEVER modify requirements.yml, spec.md, plan.md, or tasks.md
- If tasks.md has custom tasks beyond T1-T6, map them to the appropriate wave based on their dependencies described in tasks.md
- If a task references files that don't exist yet (greenfield), note this in `read_first` as "to be created"

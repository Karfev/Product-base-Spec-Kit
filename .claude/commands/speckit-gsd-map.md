---
description: Map existing codebase with GSD and route findings to Spec Kit L2 architecture
argument-hint: <product-name> (e.g., platform-api)
---

You are running GSD codebase analysis and routing the results into Spec Kit's L2 product architecture layer.

Use this on brownfield projects before starting a spec cycle, to understand the existing codebase.

## Prerequisites

1. Verify GSD is installed: `.claude/commands/gsd/` directory MUST exist
2. Verify the product directory exists: `products/$ARGUMENTS/` — if not, tell user to create L2 structure first (`cp -r products/{product}/ products/$ARGUMENTS/`)

## Step 1: Run GSD codebase mapping

Execute `/gsd-map-codebase` — this creates `.planning/codebase/` with up to 7 documents:
- STACK.md — technology stack and dependencies
- INTEGRATIONS.md — external service integrations
- ARCHITECTURE.md — architectural patterns and structure
- STRUCTURE.md — file/directory organization
- CONVENTIONS.md — coding conventions and standards
- TESTING.md — test infrastructure and patterns
- CONCERNS.md — technical debt, risks, security concerns

Wait for mapping to complete before proceeding.

## Step 2: Route architecture findings to L2

Read `.planning/codebase/ARCHITECTURE.md` and `.planning/codebase/STRUCTURE.md`.

Read existing `products/$ARGUMENTS/architecture/overview.md`.

Merge findings into `products/$ARGUMENTS/architecture/overview.md`:
- **Additive only** — NEVER delete or replace existing content
- Mark all new sections with `<!-- [GSD-MAPPED {YYYY-MM-DD}] -->` comment
- If GSD findings conflict with existing docs, add a note: `<!-- [GSD-CONFLICT] GSD found X, existing docs say Y — needs review -->`
- Organize new findings under existing heading structure (Context, Containers, Components) if present
- If no existing structure, use arc42-lite headings consistent with Spec Kit's design.md template

## Step 3: Route concerns to NFR baseline

Read `.planning/codebase/CONCERNS.md`.

Read existing `products/$ARGUMENTS/nfr-baseline/baseline.md`.

For each concern that maps to an NFR category (performance, security, reliability, maintainability):
- Suggest an addition to `nfr-baseline/baseline.md` with `<!-- [GSD-MAPPED] -->` marker
- Do NOT auto-write — present the suggestions and let the user approve

## Step 4: Note testing patterns

Read `.planning/codebase/TESTING.md`.

Print a summary of testing patterns found (frameworks, coverage, test structure) — this informs future spec.md and tasks.md generation but does not modify any files.

## Output

1. Confirm `.planning/codebase/` was populated
2. List sections added to `products/$ARGUMENTS/architecture/overview.md`
3. Present NFR baseline suggestions (pending user approval)
4. Print testing pattern summary
5. Suggest next step: start spec cycle with `/speckit-specify <NNN>-<slug>`

## Rules

- See `.specify/memory/presets/gsd.md` section "Permission boundaries" for the full policy
- NEVER modify L0, L1, or L3 artifacts
- NEVER overwrite existing architecture docs — additive only
- NEVER auto-apply NFR suggestions — present and wait for approval
- `[GSD-MAPPED]` markers MUST be present on all additions for audit trail
- If `.planning/codebase/` already exists from a previous run, ask user whether to reuse or re-run

## Preset Loading

Read `.specify/memory/presets/gsd.md` — required for GSD permission boundaries and mapping rules.

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_

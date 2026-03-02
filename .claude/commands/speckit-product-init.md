---
description: Scaffold a new product spec folder with architecture template, NFR baseline, and decisions/
argument-hint: <product-name> (e.g., platform, analytics, billing)
---

You are initializing the product-level specification for `$ARGUMENTS`.

## Your job

1. Check if `products/$ARGUMENTS/` already exists — if so, ask the user whether to update or abort.
2. Read `products/README.md` for the expected structure.
3. Read `.specify/memory/constitution.md` for L2 requirements.

4. Ask the user:
   - What is the product's primary purpose? (1–2 sentences)
   - Which domain(s) does this product belong to? (links to `domains/`)
   - Who is the product owner? (`@handle`)
   - What is the tech stack? (language, framework, DB, message bus)
   - What is the current version? (SemVer)

5. Create `products/$ARGUMENTS/` with:

   **`architecture.md`** (arc42 skeleton):
   ```markdown
   # Architecture: $ARGUMENTS
   Owner: @<handle> | Version: <version> | Updated: <date>

   ## 1. Introduction & Goals
   {placeholder: product purpose, key quality goals, stakeholders}

   ## 2. Constraints
   {placeholder: technical, organizational, regulatory constraints}

   ## 3. Context & Scope
   {placeholder: system context diagram — what is inside/outside the system boundary}

   ## 4. Solution Strategy
   {placeholder: key architectural decisions and technology choices}

   ## 5. Building Blocks
   {placeholder: top-level components and their responsibilities}

   ## 6. Runtime Behaviour
   {placeholder: key runtime scenarios / sequence diagrams}

   ## 7. Deployment
   {placeholder: infrastructure, environments, deployment topology}

   ## 8. Crosscutting Concepts
   {placeholder: security, observability, error handling patterns}

   ## 9. Architecture Decisions
   → See `decisions/` for ADRs (format: `$ARGUMENTS-NNNN-slug`)

   ## 10. Quality Requirements
   → See `nfr-baseline.md` for measurable NFR targets
   ```

   **`nfr-baseline.md`** (stub):
   ```markdown
   # NFR Baseline: $ARGUMENTS
   Updated: <date>

   ## Availability
   - Target: {placeholder: e.g., 99.9% per month}
   - Measurement: {placeholder: uptime monitor / SLO}

   ## Latency
   - P95 API response: {placeholder: e.g., < 200ms}
   - P99 API response: {placeholder: e.g., < 500ms}

   ## Throughput
   - Peak RPS: {placeholder}
   - Sustained RPS: {placeholder}

   ## Security
   - Auth: {placeholder: Bearer JWT / API key / mTLS}
   - Data classification: {placeholder: PII / financial / public}

   ## Data Retention
   - {placeholder: retention policy, backup frequency}
   ```

   **`decisions/`** — empty directory with `.gitkeep`.

   **`README.md`**:
   ```markdown
   # $ARGUMENTS
   <one-line purpose>
   Owner: @<handle> | Stack: <stack>

   - Architecture: `architecture.md`
   - NFR baseline: `nfr-baseline.md`
   - Decisions: `decisions/` (ADR format: `$ARGUMENTS-NNNN-slug`)
   - Domains: `domains/<domain>/`
   ```

6. Report all created files and next steps:
   - `Run /speckit-nfr-baseline $ARGUMENTS to fill NFR targets`
   - `Run /speckit-adr-product $ARGUMENTS to record first architecture decision`

## Rules
- `architecture.md` MUST NOT duplicate content from domain glossaries — reference `domains/<domain>/`
- All `{placeholder}` sections MUST remain until user fills them — do not invent content
- `decisions/` naming: `$ARGUMENTS-NNNN-slug` (zero-padded, lowercase slug)

---
description: Audit all L1–L5 artifacts for compliance with the Spec Constitution
argument-hint: (optional) <INIT-YYYY-NNN-slug> to scope audit to one initiative; omit for full repo audit
---

You are auditing this repository for compliance with `.specify/memory/constitution.md`.

## Your job

1. Read `.specify/memory/constitution.md` — the authoritative governance rules.
2. Determine audit scope from `$ARGUMENTS`:
   - If empty → full repository audit (all domains, products, initiatives, specs)
   - If `INIT-YYYY-NNN-slug` → scope to that initiative only

### Audit Checklist

**L0 — Governance:**
- [ ] `constitution.md` version header is filled (not `{YYYY-MM-DD}`)
- [ ] All CI workflows exist in `.github/workflows/` and match constitution CI Gates table

**L1 — Domains (for each `domains/*/`):**
- [ ] `glossary.md` exists and has ≥1 term
- [ ] `canonical-model.md` exists (may be stub but must exist)
- [ ] `event-catalog.md` exists
- [ ] Event names follow pattern `<domain>.<entity>.<past-tense-verb>`
- [ ] No term conflicts between domains (scan all glossaries)

**L2 — Products (for each `products/*/`):**
- [ ] `architecture.md` exists (arc42 sections present)
- [ ] `nfr-baseline.md` exists with measurable targets
- [ ] `decisions/` directory exists

**L3 — Initiatives (for each `initiatives/INIT-*/`):**
- [ ] Folder name matches `INIT-YYYY-NNN-<slug>` pattern
- [ ] `requirements.yml` passes `make validate` (no schema errors)
- [ ] Profile matches artifact completeness (Minimal/Standard/Extended)
- [ ] All REQ-IDs follow `REQ-<SCOPE>-NNN` pattern
- [ ] `functional` requirements have `acceptance_criteria`
- [ ] `nfr` requirements have `metrics`
- [ ] Standard/Extended: contracts validated by `make lint-contracts`
- [ ] Standard/Extended: `trace.md` exists with ≥1 link per REQ-ID
- [ ] Standard/Extended: `ops/slo.yaml` exists for NFR requirements
- [ ] Standard/Extended: `ops/prr-checklist.md` exists
- [ ] Extended: `ops/threat-model.md` exists

**L4 — Feature Specs (for each `.specify/specs/*/`):**
- [ ] Folder name matches `NNN-<slug>` pattern
- [ ] `spec.md` has no unfilled `{placeholder}` markers
- [ ] `plan.md` exists if tasks.md exists
- [ ] `tasks.md` checklist follows T1–T6 structure
- [ ] All REQ-IDs in spec.md exist in the parent initiative's `requirements.yml`

**L5 — Traceability:**
- [ ] `make check-trace` passes (zero errors)
- [ ] Every REQ-ID with status `implemented` or `verified` has ≥1 trace link

3. Run automated checks:
   ```
   make check-all
   ```
   Include verbatim output in the report.

4. Generate audit report:
   ```
   # Constitution Compliance Audit
   Date: <YYYY-MM-DD>
   Scope: <full repo | INIT-YYYY-NNN-slug>

   ## Summary
   PASS: N checks ✅ | FAIL: M checks ❌ | WARN: K items ⚠️

   ## Failures (must fix)
   [list each ❌ with file path and specific violation]

   ## Warnings (recommended)
   [list each ⚠️ with file path and recommendation]

   ## Automated check output
   [make check-all verbatim output]
   ```

5. If failures exist: list specific remediation commands (e.g., `run /speckit-requirements INIT-XXX-YYY`)

## Rules
- Do NOT auto-fix violations — only report them; remediation is done by the user with appropriate Skills
- `make check-all` MUST be run and its output included verbatim
- A passing audit requires zero ❌ failures — warnings do not block
- Run this audit before any production release of a Standard/Extended initiative

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_

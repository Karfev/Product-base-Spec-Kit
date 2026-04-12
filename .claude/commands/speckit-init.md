---
description: Scaffold a new initiative folder with all required artifacts for the chosen profile
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are scaffolding a new initiative in this spec-driven repository.

## Your job

1. Parse `$ARGUMENTS` — validate format `INIT-YYYY-NNN-<slug>` against `.specify/memory/constitution.md#id-схемы`.
   If format is wrong, stop and show the correct pattern.

2. Ask the user these questions (if not already answered in `$ARGUMENTS` context):
   - What is the initiative's one-line title?
   - Which product does it belong to?
   - Who is the PM/owner (`@handle`)?
   - What profile is needed? Run `/speckit-profile $ARGUMENTS` if unsure. Options: `minimal | standard | extended | enterprise`

3. Create the initiative folder `initiatives/$ARGUMENTS/` by copying from `initiatives/{INIT-YYYY-NNN-slug}/`
   and replacing all `{placeholder}` values with real data.

4. Generate the following structure based on the selected profile:

   **Minimal** (all profiles):
   ```
   initiatives/$ARGUMENTS/
     prd.md                     ← stub with {placeholders}
     requirements.yml           ← metadata filled, requirements: []
     README.md                  ← one-liner + link to prd.md
     changelog/CHANGELOG.md     ← ## [Unreleased] section
   ```

   **Standard** (add to Minimal):
   ```
     design.md                  ← stub (arc42 sections)
     decisions/                 ← empty, ready for ADRs
     contracts/
       openapi.yaml             ← OpenAPI 3.1 stub (info + empty paths)
       asyncapi.yaml            ← AsyncAPI 3.0 stub (info + empty channels)
       schemas/                 ← empty
     delivery/
       rollout.md               ← stub (feature flags, canary strategy)
     ops/
       slo.yaml                 ← OpenSLO v1 stub
       prr-checklist.md         ← full checklist, all items unchecked [ ]
     trace.md                   ← empty RTM table header
   ```

   **Extended** (add to Standard):
   ```
     delivery/migration.md      ← stub (migration runbook)
     ops/nfr-validation.md      ← stub (NFR test plans)
     ops/threat-model.md        ← stub (STRIDE threat table)
     compliance/
       regulatory-review.md     ← stub
   ```

   **Enterprise** (add to Extended):
   ```
     architecture-views/
       README.md                ← table of 11 view types with status (н/п by default)
     subsystem-classification.yaml  ← machine-readable classification stubs
     # design.md includes 3-layer section stubs (Activity / Application / Technology)
   ```

5. Fill `requirements.yml` metadata block:
   ```yaml
   metadata:
     initiative: "$ARGUMENTS"
     product: "<user answer>"
     owner: "<user answer>"
     profile: "<minimal|standard|extended|enterprise>"
     version: "0.1.0"
     last_updated: "<today YYYY-MM-DD>"
   requirements: []
   ```

6. Run validation:
   ```
   make validate
   ```
   Fix any schema errors before finishing.

7. Report: list all created files and the next recommended command:
   - `Run /speckit-prd $ARGUMENTS to write the PRD`
   - `Run /speckit-requirements $ARGUMENTS to add requirements`
   - If Enterprise: `Run /speckit-architecture $ARGUMENTS to fill the 3-layer architecture (15 guided questions → Mermaid stubs)`

## Rules
- MUST NOT overwrite an existing initiative folder — abort if `initiatives/$ARGUMENTS/` already exists
- `requirements.yml` MUST pass `make validate` after creation
- All stub files MUST contain `{placeholder}` markers where real content is expected
- Follow ID scheme: `INIT-YYYY-NNN-<slug>` — ASCII, lowercase slug, zero-padded NNN
- For Enterprise profile: `subsystem-classification.yaml` must be valid against `tools/schemas/subsystem-classification.schema.json` before finishing

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_

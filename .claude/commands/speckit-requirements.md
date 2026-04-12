---
description: Fill or update requirements.yml for an initiative, then validate
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are managing the requirements registry for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/requirements.yml` (current state).
2. Read `initiatives/$ARGUMENTS/prd.md` to extract scope items and implied requirements.
3. Read `.specify/memory/constitution.md` for ID scheme and profile rules.
4. Read `tools/schemas/requirements.schema.json` to understand validation rules.

5. **Analyse gaps**: Compare scope in `prd.md` against existing REQ-IDs:
   - List requirements already covered (with REQ-ID)
   - List scope items with NO REQ-ID → propose new requirements for each

6. For each proposed new requirement, ask the user to confirm:
   - Title (concise, action-verb phrase)
   - Type: `functional` | `nfr` | `constraint` | `compliance`
   - Priority: `P0` | `P1` | `P2` | `P3`
   - Acceptance criteria (for `functional`) or metrics (for `nfr`)

7. Assign REQ-IDs using the scheme `REQ-<SCOPE>-NNN`:
   - `<SCOPE>` = 2–16 uppercase chars derived from domain/area (e.g., `AUTH`, `BILLING`, `EXPORT`)
   - `NNN` = zero-padded sequential number within the scope
   - Check existing IDs in the file and across `initiatives/*/requirements.yml` to avoid collisions
   - Also check `products/{product}/requirements-registry.yml` (if it exists) to ensure no collision with graduated REQ-IDs. Graduated IDs are immutable and MUST NOT be reassigned. If a collision is found, warn:
     ```
     WARNING: REQ-AUTH-001 already exists in the product registry (graduated from INIT-2026-000).
     Choose a different ID or increment the sequence number.
     ```

8. Write updated `requirements.yml` — each requirement MUST include:
   ```yaml
   - id: "REQ-<SCOPE>-NNN"
     title: "<concise title>"
     type: "functional|nfr|constraint|compliance"
     priority: "P0|P1|P2|P3"
     status: "draft"
     description: >
       <full description, MUST / SHOULD language>
     acceptance_criteria:          # required for functional
       - "Given ... when ... then ..."
     metrics:                      # required for nfr
       - name: "<metric_name>"
         target: <value>
         measurement: "<source>"
     trace:
       prd: "prd.md#<section-anchor>"
   ```

9. **For NFR requirements with metrics**: Fill the corresponding SLO stub in `initiatives/$ARGUMENTS/ops/slo.yaml` with target values from the requirement's `metrics:` section. This ensures SLO is defined early, not deferred to the rollout phase.

10. Run validation:
    ```
    make validate
    ```
    Fix ALL schema errors before finishing.

11. Report:
    - Count of new REQ-IDs added
    - Count of existing REQ-IDs updated
    - Any REQ-IDs that now need traces (contracts/tests/SLO) — these are gaps to close later

## Rules
- REQ-IDs are **immutable** once status moves past `draft` — never renumber existing IDs
- `functional` requirements MUST have `acceptance_criteria`
- `nfr` requirements MUST have `metrics`
- Every REQ-ID in `prd.md` MUST exist in `requirements.yml` — no dangling references
- MUST run `make validate` and confirm zero errors before reporting success
- Do NOT add trace links that don't yet exist — leave `trace: {}` or partial trace for now

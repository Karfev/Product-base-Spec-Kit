---
description: Build the Requirements Traceability Matrix for an initiative by scanning all artifacts
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

**Context loading:** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" per phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are building the Requirements Traceability Matrix (RTM) for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/requirements.yml` — the canonical list of all REQ-IDs.
2. Scan `initiatives/$ARGUMENTS/contracts/openapi.yaml` — extract all `operationId` and path+method pairs.
3. Scan `initiatives/$ARGUMENTS/contracts/asyncapi.yaml` — extract all channel names and message IDs.
4. Scan `initiatives/$ARGUMENTS/contracts/schemas/` — list all schema files.
5. Scan `initiatives/$ARGUMENTS/decisions/` — list all ADR files and their REQ-ID references.
6. Scan `initiatives/$ARGUMENTS/ops/slo.yaml` — extract SLO IDs.
7. Scan all `.specify/specs/*/trace.md` files that reference this initiative's REQ-IDs.

8. **Cross-reference matrix**: for each REQ-ID, find evidence of coverage:
   - **Contract**: OpenAPI path/method OR AsyncAPI channel that has `x-req-id` or `summary` containing the REQ-ID
   - **Schema**: JSON Schema file whose `$id` or `title` is referenced in the requirement's trace
   - **ADR**: Decision file that mentions the REQ-ID
   - **Tests**: Test file path from `requirements.yml` trace section
   - **SLO**: SLO ID from `ops/slo.yaml` that maps to the requirement

9. Write `initiatives/$ARGUMENTS/trace.md`:
   ```markdown
   # RTM: $ARGUMENTS
   Generated: <YYYY-MM-DD>

   | REQ-ID | Type | Priority | Status | ADR | Contract | Schema | Tests | SLO |
   |---|---|---|---|---|---|---|---|---|
   | `REQ-XXX-001` | functional | P0 | proposed | — | `contracts/openapi.yaml#/paths/~1resource/post` | `contracts/schemas/resource.json` | `tests/api/resource.spec.ts` | — |
   ```

10. Highlight gaps:
    ```
    ⚠️ GAP REPORT:
    - REQ-XXX-003: no contract, no tests — BLOCKER for Standard DoD
    - REQ-XXX-005: no SLO defined for nfr requirement
    ```

11. Run:
    ```
    make check-trace
    ```
    Report results.

## Rules
- RTM is a **read-derived** artifact — it reflects actual file contents, never aspirational state
- If a REQ-ID is in `requirements.yml` but absent from all contracts and tests, it MUST be listed as GAP
- Do NOT add trace links by inference — only link explicitly referenced IDs
- `make check-trace` MUST be run and results shown verbatim

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** lifecycle | **Next:** /speckit-consilium (Standard+) or /speckit-graduate (Minimal)

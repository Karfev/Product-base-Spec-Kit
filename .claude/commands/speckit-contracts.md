---
description: Generate or update OpenAPI / AsyncAPI contract stubs from requirements.yml
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

**Context loading (phase: L3 Contracts):** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" for the **L3: Contracts** row of the phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are generating machine-readable API contracts for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/requirements.yml` — collect all `functional` requirements.
2. Read `initiatives/$ARGUMENTS/prd.md` — understand the API surface implied by the scope.
3. Read existing `initiatives/$ARGUMENTS/contracts/openapi.yaml` and `asyncapi.yaml` (may be stubs).
4. Read `.specify/memory/constitution.md` for profile and contract rules.

5. **Classify requirements by interface type:**
   - **REST** (synchronous request/response) → `openapi.yaml`
   - **Event/async** (publish/subscribe, webhooks) → `asyncapi.yaml`
   - **Data schema only** → `contracts/schemas/*.json`

6. Ask the user to confirm the API surface for each unresolved functional requirement:
   - HTTP method + path (for REST) OR channel name + message (for events)
   - Key request/response fields
   - Auth mechanism (Bearer token, API key, etc.)

7. Generate / update `initiatives/$ARGUMENTS/contracts/openapi.yaml`:
   ```yaml
   openapi: "3.1.0"
   info:
     title: "<Initiative title> API"
     version: "0.1.0"
   paths:
     /resource:
       post:
         operationId: createResource
         summary: "<REQ-ID> <title>"
         tags: ["<domain>"]
         security: [{ bearerAuth: [] }]
         requestBody: ...
         responses:
           "201": ...
           "400": ...
           "401": ...
   components:
     securitySchemes:
       bearerAuth:
         type: http
         scheme: bearer
   ```
   Each path MUST reference its REQ-ID in `summary` or `x-req-id` extension.

8. Generate / update `initiatives/$ARGUMENTS/contracts/asyncapi.yaml` (if async requirements exist):
   ```yaml
   asyncapi: "3.0.0"
   info:
     title: "<Initiative title> Events"
     version: "0.1.0"
   channels:
     resource.created:
       address: "resource.created"
       messages:
         ResourceCreated:
           $ref: "#/components/messages/ResourceCreated"
   ```

9. Generate JSON Schema stubs in `contracts/schemas/` for each new resource type.

10. Run validation:
    ```
    make lint-contracts
    ```
    Fix ALL errors (not warnings) before finishing.

11. Update `requirements.yml` — add `trace.contracts` links for each REQ-ID covered:
    ```yaml
    trace:
      contracts:
        - "contracts/openapi.yaml#/paths/~1resource/post"
    ```
    Then run `make validate` again.

## Rules
- Each REST endpoint MUST map to at least one REQ-ID
- Breaking changes to existing contracts require a note: "BREAKING — run `make lint-contracts` to check oasdiff"
- Do NOT add endpoints without a corresponding REQ-ID — no spec = no code
- `make lint-contracts` MUST pass with zero errors before reporting success
- OpenAPI version MUST be `3.1.0`; AsyncAPI version MUST be `3.0.0` (intentional — 3.0.0 has wider tooling support; AsyncAPI CLI info about 3.1.0 can be ignored)
- `401` and `400` error responses are REQUIRED for all authenticated endpoints

## Index Generation (post-write hook)

After step 10 (validation passes), generate `initiatives/$ARGUMENTS/contracts/contracts-index.md`:

1. Compute SHA-256 hash of `initiatives/$ARGUMENTS/contracts/openapi.yaml` (and `asyncapi.yaml` if exists)
2. Write file in this format:
   ```markdown
   <!-- source-hash: <sha256-first-12-chars> | generated: YYYY-MM-DD -->
   # Contracts Index — $ARGUMENTS

   ## REST Endpoints
   | Method | Path | Summary | REQ-ID |
   |---|---|---|---|
   | POST | /resource | Create resource | REQ-XXX-001 |

   ## Events (if asyncapi.yaml exists)
   | Channel | Message | REQ-ID |
   |---|---|---|
   | resource.created | ResourceCreated | REQ-XXX-002 |
   ```
3. Commit this file alongside contract changes

If `contracts-index.md` already exists, overwrite it with fresh data.

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** lifecycle | **Next:** /speckit-specify

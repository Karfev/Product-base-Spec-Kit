---
description: Graduate knowledge (REQ-IDs, ADRs, contracts) from an initiative to the product layer before archiving
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-000-api-key-management)
---

**Context loading (phase: Governance graduate):** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" for the **Governance: graduate** row of the phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are graduating knowledge from initiative `$ARGUMENTS` to the product layer (L2).

Requirements, ADRs, the knowledge log and the `graduated: true` mark are handled by `tools/scripts/graduate.py`: do not edit `requirements-registry.yml` by hand. This prompt runs the dialog and merges contracts.

## Your job

### 1. Check product and outcome

1. Validate `$ARGUMENTS` matches `^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$`. Abort if invalid.
2. Read `metadata.product` from `initiatives/$ARGUMENTS/requirements.yml`. If `products/{product}/` does not exist, instruct the user: "Run `/speckit-product-init {product}` first." Stop.

### 2. Preview the plan

Run:
```
python3 tools/scripts/graduate.py $ARGUMENTS --dry-run --json
```

The output is one JSON document:

- `already_graduated: true` — inform the user. Stop unless they ask to re-run; then add `--force` to every call. Re-running is safe: what is already merged is a no-op.
- `conflicts` is not empty — show every `code`, `message` and `fix`. Stop: nothing can be applied until the initiative is corrected.
- otherwise present `merged`, `adrs` and `pending`:

  ```
  Requirements to merge:
  | # | ID           | Title          | Change         | Status      |
  |---|--------------|----------------|----------------|-------------|
  | 1 | REQ-AUTH-001 | Create API key | added, rev 1   | implemented |
  | 2 | REQ-AUTH-002 | Revoke API key | modified, rev 3| implemented |

  ADRs to copy:
  | # | Source                            | Product ADR       | Title                  |
  |---|-----------------------------------|-------------------|------------------------|
  | 1 | INIT-2026-000-ADR-0001-storage    | PLAT-0004-storage | Bcrypt hashing for ... |

  Stay in the initiative (status not eligible): REQ-AUTH-003

  Confirm? (or specify numbers to skip)
  ```

Skipped requirements become `--only <the rest>`, skipped ADRs become `--skip-adr <source>`.

### 3. Contract graduation (REQ-CONTR-001–005)

1. Scan `initiatives/$ARGUMENTS/contracts/` for contract files:
   - OpenAPI: `*.openapi.yml`, `*.openapi.json`, `openapi.yaml`
   - Protobuf: `*.proto`
   - AsyncAPI: `*.asyncapi.yml`, `asyncapi.yaml`

2. If no contracts directory or no contract files found — **silent skip**: log "No contracts found, skipping contract graduation" and proceed to Step 4.

3. Present found contracts to user:

   ```
   Contracts found for graduation:
   | # | Format   | File                    |
   |---|----------|-------------------------|
   | 1 | OpenAPI  | contracts/openapi.yaml  |
   | 2 | AsyncAPI | contracts/asyncapi.yaml |
   
   Confirm graduation of all N contract files? (or specify numbers to skip)
   ```

4. After user confirms, process each format:

   #### OpenAPI merge (upsert strategy)
   
   - Target: `products/{product}/contracts/openapi/baseline.openapi.yml`
   - If baseline does not exist → copy source file as the baseline (create `contracts/openapi/` directory)
   - If baseline exists → **upsert merge**:
     - For each `path` in source `paths`:
       - If path exists in baseline:
         - For each `method` in that path:
           - If method exists in baseline with **different** schema/operationId → **CONFLICT**
           - If method does not exist → add (new method for existing path)
       - If path does not exist → add (new path)
     - Merge `components.schemas` → baseline (upsert by schema name; conflict if same name, different definition)
     - Merge `components.securitySchemes` → baseline (upsert by name)
     - Merge `components.responses` → baseline (upsert by name)
   - Preserve baseline's `info.title`, `info.version`, `info.description` — do not overwrite with initiative values
   - Add initiative-specific paths/schemas to the baseline file
   
   #### Protobuf merge (copy with namespace isolation)
   
   - Target: `products/{product}/contracts/proto/`
   - For each `.proto` file:
     - Extract `package` declaration from the file
     - Target directory: `products/{product}/contracts/proto/{package}/`
     - If a file with the same name exists in target:
       - Compare content (hash) — if different → **CONFLICT**
       - If identical → skip (already graduated)
     - If no conflict → copy file to target directory
   
   #### AsyncAPI merge (upsert strategy)
   
   - Target: `products/{product}/contracts/asyncapi/baseline.asyncapi.yml`
   - If baseline does not exist → copy source as baseline (create `contracts/asyncapi/` directory)
   - If baseline exists → **upsert merge**:
     - For each `channel` in source `channels`:
       - If channel exists in baseline with **different** message schema → **CONFLICT**
       - If channel does not exist → add
     - Merge `operations` → baseline (upsert by operationId)
     - Merge `components.schemas` and `components.messages` → baseline (upsert by name)
   - Preserve baseline's `info.title`, `info.version`, `info.description`

5. **Conflict handling** (REQ-CONTR-003):
   - If any conflicts detected → STOP and display conflict report:
     ```
     CONFLICT: Cannot merge contracts automatically.
     | # | Format  | Conflict Type      | Detail                                      |
     |---|---------|--------------------|--------------------------------------------- |
     | 1 | OpenAPI | path+method exists | POST /api-keys — different request schema    |
     | 2 | Proto   | file hash mismatch | user.proto — different content in baseline   |
     
     Options:
       a) Resolve conflicts manually, then re-run /speckit-graduate
       b) Use --force to override baseline with initiative version
     ```
   - If `--force` is present in arguments → proceed with override, mark `forced: true` in registry

6. **Breaking change detection** (REQ-CONTR-004):
   - After successful merge, inform user about available breaking change tools:
     ```
     Breaking change detection (run manually if needed):
       OpenAPI: oasdiff breaking <old-baseline> <new-baseline> --format text
       Protobuf: buf breaking --against <old-proto-dir> <new-proto-dir>
     ```
   - If oasdiff is available, offer to run it. Report findings as WARNING.
   - If constitution contains `contracts.breaking_changes_block: true` and breaking changes detected → STOP

7. **Update contract-registry.yml** (REQ-CONTR-005):
   - Read or create `products/{product}/contracts/contract-registry.yml`:
     ```yaml
     version: "1.0"
     product: "{product}"
     entries: []
     ```
   - Determine next CONTR-ID: scan existing entries, find max number → increment. Format: `CONTR-{PRODUCT}-NNN` where `{PRODUCT}` is uppercase product prefix.
   - Append entry for each graduated format:
     ```yaml
     - id: "CONTR-PLAT-001"
       source_initiative: "{INIT-ID}"
       format: "openapi"
       artifacts:
         - "contracts/openapi/baseline.openapi.yml"
       paths_added:
         - "GET /api-keys"
         - "POST /api-keys"
         - "DELETE /api-keys/{id}"
       graduated_at: "{ISO 8601 date-time, e.g. 2026-04-12T00:00:00Z}"
       git_commit: "{output of git rev-parse --short HEAD: the base commit of this merge}"
       forced: false
       breaking_changes_detected: false
     ```

### 4. Apply

Run contracts first, so a contract conflict stops the graduation before anything else changes. Then:
```
python3 tools/scripts/graduate.py $ARGUMENTS [--only ID,...] [--skip-adr ADR,...] [--force]
```

If the script exits with 1, nothing was written: show the conflicts and stop.

### 5. Complete the knowledge log

The script adds a section for this initiative to the top of `products/{product}/knowledge-log.md`. In that section:

1. If contracts were graduated, add before "Key learnings":

   ```markdown
   ### Contracts graduated

   | Format | Artifacts | Paths/Channels Added |
   |--------|-----------|---------------------|
   | OpenAPI | baseline.openapi.yml | GET /api-keys, POST /api-keys, DELETE /api-keys/{id} |
   | AsyncAPI | baseline.asyncapi.yml | audit.event.recorded |
   ```

2. Ask the user for key learnings and replace the placeholder under "Key learnings".

### 6. Validate

Run:
```
make validate
make validate-registry
make check-deltas
make validate-contracts
```

Fix ALL errors before proceeding. All commands MUST pass.

### 7. Report

Summarize:
```
Graduation complete for {INIT-ID} → products/{product}/

  REQ-IDs merged:     N (added A, modified M, removed R)
  ADRs graduated:     M
  Contracts graduated: K (OpenAPI: X paths, AsyncAPI: Y channels, Protobuf: Z files)
  Stayed in initiative: P
  Knowledge log:      updated

Next steps:
  1. Commit the result
  2. Archive: tools/archive.sh {INIT-ID}  (or: make archive INIT={INIT-ID})
  3. Reflect: /speckit-reflect {INIT-ID}  — generate lessons learned and evolution proposals
```

## Rules

- **The registry is the current behaviour of the product; `requirements.yml` of an initiative is a proposed change.** Merge rules live in `tools/scripts/graduate.py`.
- **Graduation = COPY, never move.** Initiative artifacts remain until archive.
- **Only `implemented` and `verified` requirements merge** (`deprecated` for `delta: removed`). Others stay in the initiative.
- **REQ-IDs are immutable.** A changed requirement keeps its ID and gets a new `rev`; a deprecated ID is not reused.
- **If `products/{product}/` does not exist**, do NOT create it — direct user to `/speckit-product-init`.
- **Do NOT touch L1 (domains/) artifacts.** Domain knowledge graduation is a manual process.
- **Contract graduation = COPY + MERGE.** Source contracts remain in initiative. Baseline in `products/{product}/contracts/` is the merged result.
- **Contract conflicts block by default.** Use `--force` to override. Forced overrides are logged in contract-registry.yml.
- **Protobuf uses strict namespace isolation.** Each `.proto` file MUST have a unique package within the product scope.
- **MUST run `make validate`, `make validate-registry` and `make check-deltas`** before reporting success.

## Preset Loading

**Conditional:** If initiative profile is Standard or higher, Read `.specify/memory/presets/archkom.md` for Архкомм governance artifacts.

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** terminal | **Next:** _(session complete — remove or archive session file)_

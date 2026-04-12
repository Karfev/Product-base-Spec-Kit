---
description: Graduate knowledge (REQ-IDs, ADRs, contracts) from an initiative to the product layer before archiving
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-000-api-key-management)
---

You are graduating knowledge from initiative `$ARGUMENTS` to the product layer (L2).

Graduation extracts valuable artifacts (implemented requirements, ADRs) from L3 initiatives into `products/{product}/` so that knowledge persists after archiving.

## Your job

### 1. Load and validate initiative context

1. Validate `$ARGUMENTS` matches `^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$`. Abort if invalid.
2. Read `initiatives/$ARGUMENTS/requirements.yml` — extract `metadata.product`, `metadata.initiative`, `metadata.profile`.
3. Check `metadata.graduated`:
   - If `true` — inform user: "This initiative has already been graduated. Use `--force` in arguments to re-graduate." Stop unless user explicitly requests re-graduation.
4. Read `initiatives/$ARGUMENTS/prd.md` — extract the one-line **Outcome** from "Цель (Outcome)" or the first sentence of "Цель и ожидаемый эффект".
5. Verify `products/{product}/` directory exists. If not — instruct user: "Product directory not found. Run `/speckit-product-init {product}` first." Stop.

### 2. REQ-ID graduation (REQ-GRAD-001, REQ-GRAD-002)

1. Scan all requirements in `initiatives/$ARGUMENTS/requirements.yml` where `status` is `implemented` or `verified`.
2. Present candidate list to user:

   ```
   Requirements eligible for graduation:
   | # | ID           | Title              | Status      | Type       | Priority |
   |---|------------- |--------------------|-------------|------------|----------|
   | 1 | REQ-AUTH-001 | Create API key     | implemented | functional | P0       |
   | 2 | REQ-AUTH-002 | Revoke API key     | implemented | functional | P0       |
   ...
   
   Confirm graduation of all N requirements? (or specify numbers to skip)
   ```

3. After user confirms:
   - Read `products/{product}/requirements-registry.yml` if it exists. If not, create with stub:
     ```yaml
     # Product requirements registry.
     # Auto-maintained by /speckit-graduate. Do not edit manually.
     metadata:
       product: "{product}"
       owner: "{owner from initiative}"
       last_updated: "{today}"
     
     entries: []
     ```
   - For each confirmed REQ-ID:
     - Check if `id` already exists in registry entries — if yes, warn user and skip (or ask to update if `--force`)
     - Append entry:
       ```yaml
       - id: "{REQ-ID}"
         title: "{title}"
         type: "{type}"
         final_status: "{status}"
         source_initiative: "{INIT-ID}"
         graduated_date: "{today YYYY-MM-DD}"
       ```
   - Update `metadata.last_updated` to today.

### 3. ADR graduation (REQ-GRAD-004)

1. Scan `initiatives/$ARGUMENTS/decisions/` for `.md` files (ADRs).
2. If no ADR files found — skip this step, inform user: "No ADRs found in this initiative."
3. Present each ADR to user:

   ```
   ADRs eligible for graduation:
   | # | Source File                          | Title (from H1)                    |
   |---|--------------------------------------|------------------------------------|
   | 1 | INIT-2026-000-ADR-0001-storage.md    | Bcrypt hashing for API key secrets |
   
   Confirm graduation of all N ADRs? (or specify numbers to skip)
   ```

4. After user confirms, for each ADR:
   - Scan `products/{product}/decisions/` for existing files matching `{PRODUCT}-NNNN-*.md` (case-insensitive product prefix)
   - Find the maximum NNNN — set next number = max + 1 (start at 0001 if none exist)
   - Determine `{PRODUCT}` prefix: uppercase product name (e.g., `platform` → `PLAT`, or first 4+ chars uppercase). Use the same prefix as existing ADRs if any; otherwise derive from product name.
   - Extract `slug` from original filename: `INIT-xxx-ADR-NNNN-{slug}.md` → keep `{slug}`
   - Target filename: `products/{product}/decisions/{PRODUCT}-{NNNN}-{slug}.md`
   - **Verify** no file with target name exists (safety check)
   - Copy the ADR file (do NOT move the original)
   - In the copied file, add YAML frontmatter fields (or update existing frontmatter):
     ```yaml
     graduated_from: "{INIT-ID}"
     original_id: "{original ADR filename without .md}"
     graduated_date: "{today YYYY-MM-DD}"
     ```
   - Update the H1 heading from the initiative-scoped ID to the product-scoped ID

### 3b. Contract graduation (REQ-CONTR-001–005)

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
       graduated_at: "{ISO 8601 timestamp}"
       git_commit: "{current commit hash — fill after commit}"
       forced: false
       breaking_changes_detected: false
     ```

### 4. Knowledge log (REQ-GRAD-005)

1. Read or create `products/{product}/knowledge-log.md`. If creating, add header:
   ```markdown
   # Knowledge Log: {product}
   
   Graduation history — newest first. Auto-maintained by `/speckit-graduate`.
   ```

2. Prepend (newest first) a detailed section:

   ```markdown
   ---
   
   ## {YYYY-MM-DD} — {INIT-ID}
   
   **Outcome:** {one-line summary from prd.md}
   
   ### Requirements graduated
   
   | REQ-ID | Title | Final Status | Type |
   |--------|-------|--------------|------|
   | REQ-AUTH-001 | Create API key | implemented | functional |
   | REQ-AUTH-002 | Revoke API key | implemented | functional |
   
   ### ADRs graduated
   
   | Source | Product ADR | Title |
   |--------|-------------|-------|
   | INIT-2026-000-ADR-0001-storage | PLAT-0001-storage | Bcrypt hashing for API key secrets |
   
   ### Key learnings
   
   {placeholder — add key insights from this initiative}
   ```

   If no ADRs were graduated, omit the "ADRs graduated" sub-section.
   
   If contracts were graduated, add a "Contracts graduated" sub-section:

   ```markdown
   ### Contracts graduated
   
   | Format | Artifacts | Paths/Channels Added |
   |--------|-----------|---------------------|
   | OpenAPI | baseline.openapi.yml | GET /api-keys, POST /api-keys, DELETE /api-keys/{id} |
   | AsyncAPI | baseline.asyncapi.yml | audit.event.recorded |
   ```

### 5. Mark initiative as graduated

1. Set `graduated: true` in `initiatives/$ARGUMENTS/requirements.yml` under `metadata`.
2. Update `metadata.last_updated` to today.

### 6. Validate

Run:
```
make validate
make validate-registry
make validate-contracts
```

Fix ALL errors before proceeding. All commands MUST pass.

### 7. Report

Summarize:
```
Graduation complete for {INIT-ID} → products/{product}/

  REQ-IDs graduated:  N
  ADRs graduated:     M
  Contracts graduated: K (OpenAPI: X paths, AsyncAPI: Y channels, Protobuf: Z files)
  Knowledge log:      updated

Next steps:
  1. Review products/{product}/knowledge-log.md — add key learnings
  2. Archive: tools/archive.sh {INIT-ID}  (or: make archive INIT={INIT-ID})
```

## Rules

- **Graduation = COPY, never move.** Initiative artifacts remain until archive.
- **Only `implemented` and `verified` requirements qualify.** `draft`, `proposed`, `approved` stay in initiative.
- **REQ-IDs are immutable.** Same ID in registry as in initiative — never rename.
- **ADR numbering** in product scope is independent of initiative ADR numbering. Always scan `products/{product}/decisions/` to find the next sequential number.
- **If `products/{product}/` does not exist**, do NOT create it — direct user to `/speckit-product-init`.
- **Do NOT touch L1 (domains/) artifacts.** Domain knowledge graduation is a manual process.
- **Contract graduation = COPY + MERGE.** Source contracts remain in initiative. Baseline in `products/{product}/contracts/` is the merged result.
- **Contract conflicts block by default.** Use `--force` to override. Forced overrides are logged in contract-registry.yml.
- **Protobuf uses strict namespace isolation.** Each `.proto` file MUST have a unique package within the product scope.
- **MUST run `make validate` and `make validate-registry`** before reporting success.
- **Backward compatible**: `products/` without `requirements-registry.yml` continue to work. The registry is created on first graduation.

---
description: Graduate knowledge (REQ-IDs, ADRs) from an initiative to the product layer before archiving
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

### 5. Mark initiative as graduated

1. Set `graduated: true` in `initiatives/$ARGUMENTS/requirements.yml` under `metadata`.
2. Update `metadata.last_updated` to today.

### 6. Validate

Run:
```
make validate
make validate-registry
```

Fix ALL errors before proceeding. Both commands MUST pass.

### 7. Report

Summarize:
```
Graduation complete for {INIT-ID} → products/{product}/

  REQ-IDs graduated: N
  ADRs graduated:    M
  Knowledge log:     updated

Next steps:
  1. Review products/{product}/knowledge-log.md — add key learnings
  2. When ready to archive, run the archive workflow
```

## Rules

- **Graduation = COPY, never move.** Initiative artifacts remain until archive.
- **Only `implemented` and `verified` requirements qualify.** `draft`, `proposed`, `approved` stay in initiative.
- **REQ-IDs are immutable.** Same ID in registry as in initiative — never rename.
- **ADR numbering** in product scope is independent of initiative ADR numbering. Always scan `products/{product}/decisions/` to find the next sequential number.
- **If `products/{product}/` does not exist**, do NOT create it — direct user to `/speckit-product-init`.
- **Do NOT touch L1 (domains/) artifacts.** Domain knowledge graduation is a manual process.
- **Do NOT graduate contracts** (OpenAPI/AsyncAPI). This is deferred to a future initiative.
- **MUST run `make validate` and `make validate-registry`** before reporting success.
- **Backward compatible**: `products/` without `requirements-registry.yml` continue to work. The registry is created on first graduation.

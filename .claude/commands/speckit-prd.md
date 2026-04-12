---
description: Create or update the PRD for an initiative
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

**Context loading:** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only files listed in its "Context Files" section instead of reading full constitution.md. If session not found or any Context File missing, proceed with full context load as below.

You are helping write the Product Requirements Document for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/prd.md` (current state — may be stub or partial).
2. Read `initiatives/$ARGUMENTS/requirements.yml` to understand existing REQ-IDs.
3. Read `.specify/memory/constitution.md` for principles and profile definitions.

3b. **Determine discovery depth mode (REQ-DISC-005):**
   Read the `profile` field from `initiatives/$ARGUMENTS/requirements.yml` metadata.
   Map profile to depth:
   - `minimal` → **Quick mode** (3-5 questions): Problem+Outcome, Scope, Risks (optional), Metrics (optional)
   - `standard` → **Standard mode** (5-10 questions): Quick + Why now, Users/Scenarios, Architecture constraints, Contract changes, NFR targets, Dependencies
   - `extended` or `enterprise` → **Deep mode** (10-15 questions): Standard + Security/threat model, Compliance, Migration strategy, Rollout constraints, Cross-initiative impact

   If `$ARGUMENTS` contains `--depth quick|standard|deep`, use that override regardless of profile.

   Announce the mode: "Discovery mode: {Quick|Standard|Deep} ({N} вопросов по профилю {profile})"

4. **Scan for cross-initiative dependencies**: Read `initiatives/*/requirements-index.md` for cross-scan (skip template dirs with `{`). If an index is missing for any initiative, fall back to its full `requirements.yml` and warn: "Run /speckit-requirements for that initiative to generate index." Look for REQ-IDs that reference similar domains, resources, or capabilities. If found, present to the user:
   ```
   Found potentially related requirements in other initiatives:
   - REQ-NOTIF-004 (auditable opt-out) in INIT-2026-002
   - REQ-AUTH-001 (API key creation) in INIT-2026-000
   Consider referencing these in the Motivation or Scope sections.
   ```

4b. **Scan product requirements registry**: If `products/{product}/requirements-registry.yml` exists (where `{product}` comes from `initiatives/$ARGUMENTS/requirements.yml` metadata), scan it for graduated REQ-IDs that may overlap with the scope of this PRD. If found, present to the user:
   ```
   Found graduated requirements in the product registry:
   - REQ-AUTH-001 (Create API key) — graduated from INIT-2026-000 on 2026-06-15
   - REQ-AUTH-003 (Rate limiting) — graduated from INIT-2026-000 on 2026-06-15
   These are already implemented. Consider referencing or building upon them rather than re-specifying.
   ```

4c. **Scan product contract registry**: If `products/{product}/contracts/contract-registry.yml` exists, scan it for graduated API endpoints. If found, present to the user:
   ```
   Found graduated contracts in the product baseline:
   - CONTR-PLAT-001 (openapi): GET /api-keys, POST /api-keys, DELETE /api-keys/{id} — from INIT-2026-000
   - CONTR-PLAT-002 (asyncapi): audit.event.recorded — from INIT-2026-003
   These endpoints already exist in the product baseline. Avoid duplicating or conflicting with them.
   ```

4d. **Codebase-first context loading (REQ-DISC-003, REQ-DISC-004):**

   Before each PRD question, scan existing L1/L2/L3 artifacts for relevant context.
   Use this mapping to determine which files to check:

   | Question topic | Files to check | Section to extract |
   |---|---|---|
   | Problem / Outcome | Last 3 active L3 `initiatives/*/prd.md` (by last_updated) | "Цель и ожидаемый эффект" |
   | Architecture / Tech stack | `products/{product}/architecture/overview.md` | Technology, Stack, Components |
   | NFR targets | `products/{product}/nfr-baseline/baseline.md` | All measurable targets |
   | Terminology | `domains/*/glossary.md` (all domains) | All terms |
   | API patterns | Last 3 active L3 `initiatives/*/contracts/openapi.yaml` | paths section |
   | Users / Scenarios | Last 3 active L3 `initiatives/*/prd.md` | "Пользователи и сценарии" |
   | Security | Active L3 `initiatives/*/ops/threat-model.md` | Threats, Mitigations |
   | Compliance | `domains/*/regulatory/` (if exists) | All |

   **Loading rules:**
   - Max 3 files per question (sorted by `last_updated` desc if metadata available, else by filename desc)
   - Skip archived initiatives (`initiative_status == "archived"` in requirements.yml)
   - Skip template directories (containing `{` in path)
   - If a file doesn't exist at the expected path → silently skip

   **Proposed answer format:**
   If relevant context is found, present it BEFORE asking the question:
   ```
   📋 Контекст из репозитория:
   Предположительно: {extracted_content}
   (источник: {relative_path})
   Верно? [Да / Нет / Уточнить]
   ```

   If the source file's `last_updated` or git modification date is > 90 days old:
   ```
   ⚠️ Источник обновлён > 90 дней назад — проверьте актуальность
   ```

   **User responses:**
   - **Да** → use the proposed answer as-is, write it into prd.md, move to next question
   - **Нет** → discard the proposed answer, ask the question as open-ended
   - **Уточнить** → use the proposed answer as a starting point, ask user to modify

   **If no relevant context found** → ask the question as open-ended (current behavior, no change).

5. **Ask questions based on depth mode** (skip if already answered in existing prd.md):

   **Quick mode (3-5 questions) — Minimal profile:**
   - Q1 **Problem + Outcome:** What problem does this solve and what does success look like?
   - Q2 **Scope:** What is IN-scope? (2-4 items → maps to REQ-IDs)
   - Q3 **Risks:** Top risk? (optional — skip if user says "none")
   - Q4 **Metrics:** One key success metric? (optional — skip if user says "later")

   **Standard mode (5-10 questions) — Standard profile:**
   All Quick questions, plus:
   - Q5 **Why now:** Urgency driver — deadline, revenue risk, regulatory, competitive?
   - Q6 **Primary personas:** Who are the users? (role + JTBD format)
   - Q7 **Architecture constraints:** Any technology/stack constraints? (check L2 architecture first)
   - Q8 **Contract changes:** Does this add or change API endpoints or events?
   - Q9 **NFR targets:** Any latency, throughput, or availability requirements? (check L2 NFR baseline first)
   - Q10 **Dependencies:** Any upstream/downstream service dependencies?

   **Deep mode (10-15 questions) — Extended/Enterprise profile:**
   All Standard questions, plus:
   - Q11 **Security scope:** Authentication/authorization changes? Data classification?
   - Q12 **Compliance:** Regulatory requirements (GDPR, SOC2, PCI-DSS)?
   - Q13 **Migration:** Data migration or schema changes needed?
   - Q14 **Rollout constraints:** Feature flags? Canary? Regional rollout?
   - Q15 **Cross-initiative impact:** Does this affect other active initiatives?

6. Fill `initiatives/$ARGUMENTS/prd.md` with:
   - **Цель и ожидаемый эффект**: Problem statement, urgency, Outcome (user-facing goal)
   - **Пользователи и сценарии**: Primary personas, top 2–3 JTBD scenarios
   - **Метрики успеха**: Table — Метрика | Baseline | Target | Период | Источник
   - **Scope**: In-scope list with REQ-ID references, Non-goals list
   - **Риски и ограничения**: Top 3 risks with mitigations
   - **Требования (ссылки на REQ)**: Only REQ-ID references — full detail lives in `requirements.yml`
   - **Приёмка**: Links to test files and Definition of Done reference

7. Narrative text in `prd.md` MUST reference REQ-IDs from `requirements.yml` — do NOT duplicate requirement detail.

8. After writing, remind the user:
   - `Run /speckit-requirements $ARGUMENTS to add or update requirements`
   - `Run make validate to check requirements.yml schema`

## Rules
- `prd.md` is a narrative document — it MUST NOT duplicate machine-readable data from `requirements.yml`
- Every Scope item MUST reference at least one REQ-ID from `requirements.yml` (existing) or propose new ones with `[PROPOSED]` marker — these will be formalized by `/speckit-requirements`
- Mark unresolved questions as `[NEEDS CLARIFICATION: <question>]`
- Do not invent success metrics — ask the user for baseline and source
- Keep PRD focused: 1–2 pages maximum; link, don't embed
- Cross-initiative REQ-IDs SHOULD be mentioned in Motivation or Scope with initiative ID context (e.g., "REQ-NOTIF-004 from INIT-2026-002 requires auditable opt-out")

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** lifecycle | **Next:** /speckit-requirements

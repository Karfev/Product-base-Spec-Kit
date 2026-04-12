---
description: Select initiative profile (Minimal / Standard / Extended / Enterprise) via risk assessment
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are helping select the correct conformity profile for initiative `$ARGUMENTS`.

## Your job

1. Check whether `initiatives/$ARGUMENTS/` exists. If it does not, skip to the questionnaire — profile will be written later by `/speckit-init`. If it exists, read `initiatives/$ARGUMENTS/requirements.yml` (if exists) and `prd.md` (if exists).
2. Read `.specify/memory/constitution.md#профили` for profile definitions.

3. Run a **risk-assessment questionnaire** — ask the user these 8 yes/no questions:

   **Security & Compliance:**
   - [ ] Does this initiative handle authentication, authorization, or access tokens?
   - [ ] Does this involve PII, financial data, or data regulated by GDPR/SOC2/HIPAA?

   > **Edge case guidance for Q2:**
   > - `user_id` alone (without name/email) in logs/metadata → usually **NO** (indirect identifier, not PII per se)
   > - `user_id` + action context revealing behavior patterns → consider **YES** if regulators may classify as behavioral data
   > - Action metadata with IP addresses → **YES** (IP is PII under GDPR)
   > - GDPR retention requirements (e.g., 2-year audit trail) → this is an NFR constraint, not a PII question; answer **NO**, add NFR requirement instead
   > - SOC2 audit trail requirement → drives initiative existence, not profile; answer **NO** unless the data itself is regulated

   **API & Integration:**
   - [ ] Does this add or change public/external-facing API contracts (REST or events)?
   - [ ] Will other teams/services consume these APIs within 30 days?

   **Reliability & Operations:**
   - [ ] Does this have SLO/SLA commitments to customers or internal services?
   - [ ] Does this require DB schema migrations or data backfills?

   **Risk & Visibility:**
   - [ ] Could a bug in this initiative cause revenue loss or customer data exposure?
   - [ ] Is this a P0/P1 initiative on the roadmap with executive visibility?

   **Scale & Architecture (Enterprise indicator):**
   - [ ] Is this a large information system (IS-class) requiring ArchiMate / АИС 3-layer architecture documentation?
   - [ ] Does the system need machine-readable subsystem classification (system scale, type, owner)?

4. **Apply decision tree** (evaluate top-to-bottom, first match wins):

   1. Enterprise indicator (Q9 or Q10) YES → **Enterprise** (confirm with architect)
   2. Compliance question (Q2) YES → **Extended** (mandatory, not overrideable)
   3. Score 5–8 YES answers → **Extended** (downgrade requires Tech Lead sign-off)
   4. Score 2–4 YES answers → **Standard** (upgradeable to Extended)
   5. Score 0–1 YES answers → **Minimal**

   **Guard:** Security question (Q1) YES → at minimum **Standard** (overrides Minimal).

5. Show the user the **artifact checklist** for the recommended profile:

   **Minimal checklist:**
   - [ ] `prd.md` filled
   - [ ] `requirements.yml` valid (`make validate`)
   - [ ] `README.md` updated
   - [ ] `changelog/CHANGELOG.md` initialized

   **Standard checklist** (adds):
   - [ ] `design.md` filled (arc42 key sections)
   - [ ] `decisions/` — at least one ADR for key architecture choice
   - [ ] `contracts/openapi.yaml` validated (`make lint-contracts`)
   - [ ] `ops/slo.yaml` filled (OpenSLO format)
   - [ ] `ops/prr-checklist.md` — all items addressed
   - [ ] `trace.md` — all REQ-IDs have ≥1 trace link
   - [ ] `delivery/rollout.md` filled

   **Extended checklist** (adds):
   - [ ] `ops/threat-model.md` filled (STRIDE table)
   - [ ] `ops/nfr-validation.md` filled
   - [ ] `delivery/migration.md` filled (if DB changes)
   - [ ] `compliance/regulatory-review.md` filled

   **Enterprise checklist** (adds to Extended):
   - [ ] `design.md` — three-layer architecture (Activity / Application / Technology layer) filled via `/speckit-architecture`
   - [ ] `architecture-views/` — at least Д-1, Д-3, П-1, Т-1 diagrams
   - [ ] `subsystem-classification.yaml` valid (`make validate`)

6. Write the selected profile into `requirements.yml` metadata:
   ```yaml
   metadata:
     profile: "<minimal|standard|extended|enterprise>"
   ```
   Run `make validate` to confirm.

7. Report the selected profile and the next recommended action:
   - `Run /speckit-init $ARGUMENTS to scaffold missing artifact stubs`
   - If Enterprise: `Run /speckit-architecture $ARGUMENTS to fill the 3-layer architecture`

## Rules
- Profile is selected **by risk**, not by initiative size or team preference
- Profile can only be UPGRADED during development, not downgraded after Standard is reached without Tech Lead sign-off
- If the user is unsure about any question, default to YES (conservative)
- Document the profile rationale as a comment in `requirements.yml` metadata
- Enterprise profile requires explicit team/architect confirmation — it adds significant documentation overhead

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_

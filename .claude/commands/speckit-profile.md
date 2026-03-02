---
description: Select initiative profile (Minimal / Standard / Extended) via risk assessment
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are helping select the correct conformity profile for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/requirements.yml` (if exists) and `prd.md` (if exists).
2. Read `.specify/memory/constitution.md#профили` for profile definitions.

3. Run a **risk-assessment questionnaire** — ask the user these 8 yes/no questions:

   **Security & Compliance:**
   - [ ] Does this initiative handle authentication, authorization, or access tokens?
   - [ ] Does this involve PII, financial data, or data regulated by GDPR/SOC2/HIPAA?

   **API & Integration:**
   - [ ] Does this add or change public/external-facing API contracts (REST or events)?
   - [ ] Will other teams/services consume these APIs within 30 days?

   **Reliability & Operations:**
   - [ ] Does this have SLO/SLA commitments to customers or internal services?
   - [ ] Does this require DB schema migrations or data backfills?

   **Risk & Visibility:**
   - [ ] Could a bug in this initiative cause revenue loss or customer data exposure?
   - [ ] Is this a P0/P1 initiative on the roadmap with executive visibility?

4. **Score and recommend profile:**

   | Score (YES answers) | Recommended Profile | Override allowed? |
   |---|---|---|
   | 0–1 | **Minimal** | No |
   | 2–4 | **Standard** | Yes (up to Extended) |
   | 5–8 | **Extended** | No (downgrade requires Tech Lead sign-off) |

   Security/compliance questions answered YES → MUST be at least **Standard**.
   Any compliance YES → MUST be **Extended**.

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

6. Write the selected profile into `requirements.yml` metadata:
   ```yaml
   metadata:
     profile: "<minimal|standard|extended>"
   ```
   Run `make validate` to confirm.

7. Report the selected profile and the next recommended action:
   - `Run /speckit-init $ARGUMENTS to scaffold missing artifact stubs`

## Rules
- Profile is selected **by risk**, not by initiative size or team preference
- Profile can only be UPGRADED during development, not downgraded after Standard is reached without Tech Lead sign-off
- If the user is unsure about any question, default to YES (conservative)
- Document the profile rationale as a comment in `requirements.yml` metadata

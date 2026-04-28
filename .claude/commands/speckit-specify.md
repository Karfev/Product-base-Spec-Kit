---
description: Create or update a feature spec from a description
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

**Context loading (phase: L4 specify):** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" for the **L4: specify** row of the phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are helping create a spec for feature `$ARGUMENTS` in this spec-driven repository.

## Your job

**Index loading:** Read `initiatives/{INIT}/requirements-index.md` instead of full `requirements.yml` for context overview. If index is missing, fall back to full `requirements.yml` and warn: "Run /speckit-requirements to generate index." For specific REQ-IDs referenced in the spec, read targeted entries from `requirements.yml`.

1. Read `.specify/specs/$ARGUMENTS/spec.md` (current template state)
2. Read the parent initiative's `requirements-index.md` (or full `requirements.yml` per index loading rule above) — the initiative ID is in the spec's **Initiative:** field
3. Ask the user 3–5 clarifying questions about the feature (scope, users, constraints)
4. Fill `spec.md` with real content in canonical format:
   - **Summary**: 1–3 sentences — what changes and why
   - **Motivation/Problem**: link to `initiatives/{INIT}/prd.md`
   - **Scope**: explicit in-scope list
   - **Non-goals**: explicit out-of-scope list
   - **API/Contracts**: affected OpenAPI/AsyncAPI/schema files, or explicit `No contract changes`
   - **User stories**: "As a {role}, I want {capability}, so that {benefit}"
   - **Requirements**: REQ-IDs from `requirements.yml` (propose new ones if needed)
   - **Test strategy**: unit/integration(or contract)/acceptance coverage
   - **Acceptance criteria**: Given/When/Then format
   - **Rollout**: flag/guardrail, migration/backfill, monitoring/rollback
   - **Open Questions**: mark unknowns as `[NEEDS CLARIFICATION]`

5. If new REQ-IDs are needed, add them to `requirements.yml` and run:
   ```
   make validate
   ```

## Rules
- Follow ID conventions in `.specify/memory/constitution.md`
- Every REQ-ID referenced in spec.md MUST exist in `requirements.yml`
- Mark every unresolved item with `[NEEDS CLARIFICATION]` in Open Questions
- Do not propose technical solutions — that belongs in `plan.md`
- Populate all mandatory sections in one pass; do not leave Scope/Non-goals/API/Contracts/Test strategy/Rollout empty.

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from spec.md Initiative field | **Type:** lifecycle | **Next:** /speckit-plan

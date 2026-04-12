---
description: Generate plan.md from a filled spec.md
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

**Context loading:** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" per phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are helping create an architecture plan for `.specify/specs/$ARGUMENTS/`.

## Your job

**Index loading:** Read `initiatives/{INIT}/requirements-index.md` instead of full `requirements.yml` for context overview. If index is missing, fall back to full `requirements.yml` and warn: "Run /speckit-requirements to generate index." For specific REQ-IDs referenced in the spec, read targeted entries from `requirements.yml`.

1. Read `.specify/specs/$ARGUMENTS/spec.md`
   - If it contains unfilled `{placeholders}`, stop and ask the user to run `/speckit-specify $ARGUMENTS` first
2. Read `.specify/memory/constitution.md` for architectural principles
3. Read any existing ADRs in `initiatives/*/decisions/` relevant to this feature

Fill `.specify/specs/$ARGUMENTS/plan.md` with:
- **Architecture choices**: key decisions with links to ADRs (create new ADR stubs in `initiatives/{INIT}/decisions/` if needed)
- **Contracts impact**: which OpenAPI paths / AsyncAPI channels are added or changed
- **Data changes**: schema additions, migrations needed
- **Observability & SLO impact**: metrics to add, SLO changes in `ops/slo.yaml`
- **Rollout & rollback strategy**: reference `delivery/rollout.md`
- **Risks**: technical risks and mitigations

## Enterprise IS profile check

If `requirements.yml` has `profile: enterprise`:

4. Read `initiatives/*/decisions/` for ADRs related to IS ontology classification
5. Check that `design.md` contains filled **«Архитектурные слои»** section (three layers: деятельности / приложений / технологический). If section is missing or has `{placeholders}`, suggest running `/speckit-architecture $ARGUMENTS_INITIATIVE` first.
6. Check that `subsystem-classification.yaml` exists in the initiative directory. If missing, note it in the plan as a required action (needed for CI gate).
7. Add to the plan a **IS Classification** section:
   - Current classification codes (from `requirements.yml` metadata.classification or `subsystem-classification.yaml`)
   - List of architecture views that need to be completed (status: `в работе` or missing)
   - Reference: `domains/is-ontology/canonical-model/model.md`

## Rules
- Each architecture choice MUST reference or propose a new ADR
- Breaking API changes require a note: "run `make lint-contracts` to check oasdiff"
- Do not write implementation code — that belongs in T2b of `tasks.md`
- Check traceability after: `make check-trace`

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS (spec slug) | **Type:** lifecycle | **Next:** /speckit-tasks

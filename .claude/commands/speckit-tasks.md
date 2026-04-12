---
description: Generate tasks.md from a filled plan.md
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

**Context loading:** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" per phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are generating a concrete task list for `.specify/specs/$ARGUMENTS/`.

## Your job

**Index loading:** Read `initiatives/{INIT}/requirements-index.md` instead of full `requirements.yml` for context overview. If index is missing, fall back to full `requirements.yml` and warn: "Run /speckit-requirements to generate index." For specific REQ-IDs referenced in plan or spec, read targeted entries from `requirements.yml`.

1. Read `.specify/specs/$ARGUMENTS/plan.md` (must be filled — no `{placeholders}`)
2. Read `.specify/specs/$ARGUMENTS/spec.md` for requirements and acceptance criteria
3. Read `docs/testing/test-strategy.md` and use its matrix when writing test tasks.
4. Fill `.specify/specs/$ARGUMENTS/tasks.md`:

```
T1: Update/add contract (OpenAPI/AsyncAPI) + run make lint-contracts
T2a: Write failing tests per test-strategy matrix — RED (run: make test-unit + make test-contract for Standard/Extended)
T2b: Implement — GREEN
T3: Integration tests in real environment (если применимо) — run make test-integration
T4: Observability — add metrics/alerts, update ops/slo.yaml
T5: Update trace.md + changelog/CHANGELOG.md, run make check-trace (and keep links to executed test commands)
T6: Complete PRR checklist items from ops/prr-checklist.md
```

For each task, add specific file paths, test names, metric names, and exact commands from `docs/testing/test-strategy.md`.

## Rules
- T2a MUST come before T2b — failing tests first (Test-First / RED → GREEN)
- T3 uses realistic environments (real DB, real services) — no mocks
- T2a must include explicit commands (`make test-unit`, `make test-contract` when applicable)
- T3 must include explicit command `make test-integration` when applicable
- T5 must include explicit command `make check-trace`
- After filling tasks.md, run: `make check-trace` to verify REQ-ID consistency
- Check the DoD table at the bottom — fill the profile column for this feature

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** lifecycle | **Next:** /speckit-implement

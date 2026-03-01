---
description: Generate tasks.md from a filled plan.md
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

You are generating a concrete task list for `.specify/specs/$ARGUMENTS/`.

## Your job

1. Read `.specify/specs/$ARGUMENTS/plan.md` (must be filled — no `{placeholders}`)
2. Read `.specify/specs/$ARGUMENTS/spec.md` for requirements and acceptance criteria
3. Fill `.specify/specs/$ARGUMENTS/tasks.md`:

```text
T1: Update/add contract (OpenAPI/AsyncAPI) + run make lint-contracts
T2a: Write failing tests (unit + contract при Standard/Extended) — RED
T2b: Implement — GREEN
T3: Integration tests in real environment (если применимо)
T4: Observability — add metrics/alerts, update ops/slo.yaml
T5: Update trace.md + changelog/CHANGELOG.md, run make check-trace
T6: Complete PRR checklist items from ops/prr-checklist.md
```

For each task, add specific file paths, test names, and metric names from the plan.

## Rules

- T2a MUST come before T2b — failing tests first (Test-First / RED → GREEN)
- T3 uses realistic environments (real DB, real services) — no mocks
- After filling tasks.md, run: `make check-trace` to verify REQ-ID consistency
- Check the DoD table at the bottom — fill the profile column for this feature

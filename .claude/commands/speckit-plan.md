---
description: Generate plan.md from a filled spec.md
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

You are helping create an architecture plan for `.specify/specs/$ARGUMENTS/`.

## Your job

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

## Rules
- Each architecture choice MUST reference or propose a new ADR
- Breaking API changes require a note: "run `make lint-contracts` to check oasdiff"
- Do not write implementation code — that belongs in T2b of `tasks.md`
- Check traceability after: `make check-trace`

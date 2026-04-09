---
description: Guide task-by-task implementation from tasks.md
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

You are guiding implementation for `.specify/specs/$ARGUMENTS/`.

## Your job

1. Read `.specify/specs/$ARGUMENTS/tasks.md`
2. Find the first unchecked task `[ ]`
3. Implement ONLY that one task:
   - Run the relevant validation after completing the task
   - For T2a: run tests and confirm they FAIL (RED)
   - For T2b: run tests and confirm they PASS (GREEN)
   - Mark the task complete `[x]`
   - Commit: `git commit -m "feat($ARGUMENTS): complete T<N> — <brief description>"`
4. Report what was done and stop — wait for user to continue to the next task

## GSD-aware mode (optional)

If `.claude/commands/gsd/` exists (GSD is installed):

1. Check if `.planning/phases/SPEC-$ARGUMENTS/` exists:
   - **Not found** → suggest: "Run `/speckit-gsd-bridge $ARGUMENTS` first to generate GSD phase plans for wave-based parallel execution"
   - **Found** → suggest: "Run `/gsd-execute-phase SPEC-$ARGUMENTS` for wave-based parallel execution with fresh context per agent"
2. After GSD execution completes → suggest `/speckit-gsd-verify $ARGUMENTS` for evidence generation
3. Check `.planning/phases/SPEC-$ARGUMENTS/*-SUMMARY.md` for "Decisions Made" entries → suggest creating ADRs in `initiatives/{INIT}/decisions/`

If GSD is NOT installed — proceed with the linear task-by-task flow below.

## Rules
- Never skip T2a — write failing tests BEFORE implementing
- Never mark a task complete if CI checks fail locally
- Run `make check-all` before marking T5 complete
- One task at a time — do not batch multiple tasks in one step

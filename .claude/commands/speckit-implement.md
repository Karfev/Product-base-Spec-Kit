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

## Rules

- Never skip T2a — write failing tests BEFORE implementing
- Never mark a task complete if CI checks fail locally
- Run `make check-all` before marking T5 complete
- One task at a time — do not batch multiple tasks in one step

---
description: Guide task-by-task implementation from tasks.md
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

**Context loading (phase: L4 implement):** Before step 1, check if `.specify/session/{INIT-ID}.md` exists (where INIT-ID = $ARGUMENTS). If found, read session file and load only "Context Files" for the **L4: implement** row of the phase table in `.specify/session/protocol.md`. If `--full-context` passed, load all files. If no session found, proceed as below.

You are guiding implementation for `.specify/specs/$ARGUMENTS/`.

## Your job

**Index loading:** Read `initiatives/{INIT}/requirements-index.md` instead of full `requirements.yml` for context and status checks. If index is missing, fall back to full `requirements.yml` and warn: "Run /speckit-requirements to generate index." For specific REQ-IDs referenced in tasks or specs, read targeted entries from `requirements.yml`.

1. Read `.specify/specs/$ARGUMENTS/tasks.md`
2. Find the first unchecked task `[ ]`
3. Implement ONLY that one task:
   - Run the relevant validation after completing the task
   - For T2a: run tests and confirm they FAIL (RED)
   - **For T2b (Standard+ profile only) — run pre-flight checklist first (REQ-QUAL-005):**
     1. Read `tools/ai-quality-gates.md` — load Five Pillars
     2. Read the initiative's `requirements.yml` to check profile
     3. If profile is `standard`, `extended`, or `enterprise`:
        - Verify T2a is marked `[x]` in tasks.md. If not → STOP: "T2a incomplete — write tests first (Pillar 2: Test-First)"
        - Ask: "Architecture stubs created and match contracts? [Y/N]" (Pillar 3)
        - If contracts exist: run `make lint-contracts`. If fail → STOP with specific diff (Pillar 5)
        - Ask: "Scope for this task: {files, methods}. Confirmed? [Y/N]" (Pillar 4)
        - If any check fails → show WARNING with specific blocker from quality gates
        - If all pass → proceed to implementation
     4. If profile is `minimal` → skip pre-flight, proceed directly
   - For T2b: run tests and confirm they PASS (GREEN)
   - After T2b: if method > 50 LOC, suggest decomposition (Pillar 1)
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

## REQ status lifecycle

After completing **T2b (GREEN)** — all tests pass:
1. Read `initiatives/{INIT}/requirements.yml`
2. For each REQ-ID covered by passing tests:
   - Change `status: draft` → `status: implemented`
3. Run `make validate` to confirm

After completing **T5 (trace update)** — if all REQ-IDs have `status: implemented` and full trace links:
- Optionally set `status: verified` for fully traced REQ-IDs

This ensures graduation (`/speckit-graduate`) finds requirements with terminal status (`implemented` or `verified`), which is required by the requirements-registry schema.

## Rules
- Never skip T2a — write failing tests BEFORE implementing
- Never mark a task complete if CI checks fail locally
- Run `make check-all` before marking T5 complete
- One task at a time — do not batch multiple tasks in one step

## Preset Loading

**Conditional:** If GSD mode is detected (`.planning/` exists or user requests GSD), Read `.specify/memory/presets/gsd.md` for GSD permission boundaries.

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS | **Type:** lifecycle | **Next:** /speckit-trace

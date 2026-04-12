---
description: Verify GSD execution results against spec.md and requirements.yml, generate evidence
argument-hint: <NNN>-<slug> (e.g., 001-user-auth)
---

You are verifying that GSD execution for `.specify/specs/$ARGUMENTS/` correctly addresses all requirements and acceptance criteria, then generating evidence artifacts.

## Step 1: Read inputs

1. `.specify/specs/$ARGUMENTS/spec.md` — acceptance criteria (Given/When/Then blocks, user stories)
2. Resolve initiative ID from spec.md `Initiative:` field
3. `initiatives/{INIT}/requirements.yml` — all REQ-IDs with trace entries
4. All `.planning/phases/SPEC-$ARGUMENTS/*-SUMMARY.md` files — GSD execution output
5. All `.planning/phases/SPEC-$ARGUMENTS/*-PLAN.md` files — planned requirements mapping
6. `.specify/specs/$ARGUMENTS/trace.md` — existing traceability matrix

If no SUMMARY.md files exist — stop and tell the user to run `/gsd-execute-phase SPEC-$ARGUMENTS` first.

## Step 2: Cross-reference REQ-IDs

For each REQ-ID in requirements.yml:

1. **Planned?** — Find which PLAN.md lists it in `requirements` frontmatter
2. **Executed?** — Check the corresponding SUMMARY.md:
   - Does it report the task as completed?
   - Were the expected files created/modified?
3. **Traced?** — Check requirements.yml `trace` entries:
   - `trace.contracts` — do the referenced contract paths exist?
   - `trace.tests` — do the referenced test files exist?
   - `trace.slo` — does the SLO entry exist in ops/slo.yaml?

Status per REQ-ID:
- **PASS** — planned, executed successfully, trace entries verified
- **PARTIAL** — planned and executed, but trace entries incomplete
- **FAIL** — planned but SUMMARY.md reports failure, or not planned at all
- **SKIP** — REQ-ID has status `deprecated` or `draft` in requirements.yml

## Step 3: Check acceptance criteria coverage

For each acceptance criterion in spec.md (Given/When/Then, user stories, explicit criteria):
- Find the SUMMARY.md that claims to address it
- Check if the verification section confirms it was tested
- Flag any criteria not explicitly addressed as `UNCOVERED`

## Step 4: Generate verification report

Write `evidence/SPEC-$ARGUMENTS-verification.md`:

```markdown
# Verification Report: $ARGUMENTS

**Date:** {YYYY-MM-DD}
**Initiative:** {INIT}
**Profile:** {profile from spec.md}

## Requirements Coverage

| REQ-ID | Title | Plan | Status | Evidence |
|--------|-------|------|--------|----------|
| REQ-XXX-001 | ... | 01-03 | PASS | tests/api/xxx.spec.ts created, make test passes |
| REQ-XXX-002 | ... | 01-03 | PARTIAL | implementation done, trace.tests missing |
| ... | ... | ... | ... | ... |

**Summary:** N/M REQ-IDs passed (X%), Y partial, Z failed

## Acceptance Criteria Coverage

| Criterion | Source | Status | Evidence |
|-----------|--------|--------|----------|
| Given ... When ... Then ... | spec.md | COVERED | SUMMARY 01-03 verification |
| ... | ... | UNCOVERED | — |

## CI Validation

- `make check-trace`: {PASS/FAIL + output summary}
- `make check-all`: {PASS/FAIL + output summary}

## ADR Candidates

(List any architectural decisions from SUMMARY.md "Decisions Made" sections that are not yet captured as ADRs in `initiatives/{INIT}/decisions/`)

## Source References

- PLAN files: .planning/phases/SPEC-$ARGUMENTS/01-0{1..7}-PLAN.md
- SUMMARY files: .planning/phases/SPEC-$ARGUMENTS/01-0{1..7}-SUMMARY.md
- Requirements: initiatives/{INIT}/requirements.yml
```

## Step 5: Run CI validation

Execute:
1. `make check-trace` — verify REQ-ID consistency between L3 and L4
2. `make check-all` — run all validation checks

Include results in the report.

## Step 6: PRR cross-reference (if Standard/Extended profile)

If `initiatives/{INIT}/ops/prr-checklist.md` exists:
- Check which P0 items have evidence in SUMMARY.md outputs
- List P0 items still requiring manual verification
- Add this as a section in the verification report

## Output

1. Print the requirements coverage summary table
2. Highlight any FAIL or UNCOVERED items
3. Report `make check-trace` and `make check-all` results
4. If ADR candidates found — suggest creating them
5. Confirm evidence file was written to `evidence/SPEC-$ARGUMENTS-verification.md`

## Rules

- See `.specify/memory/presets/gsd.md` section "Permission boundaries" for the full policy
- NEVER modify requirements.yml, spec.md, or tasks.md — this is read-only verification
- NEVER mark tasks.md items as complete — that's speckit-implement's job
- If SUMMARY.md files are missing or incomplete, report gaps — do not fabricate evidence
- Evidence report MUST use consistent column format for machine parsing by collect-evidence.py

## Preset Loading

Read `.specify/memory/presets/gsd.md` — required for GSD permission boundaries and verification rules.

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_

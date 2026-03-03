---
description: Generate a sводный evidence report for an initiative (RTM coverage, PRR status, open gaps)
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are generating the evidence report for initiative `$ARGUMENTS` before release.

## Your job

1. Read `initiatives/$ARGUMENTS/requirements.yml` — list all REQ-IDs and their status.
2. Read `initiatives/$ARGUMENTS/trace.md` (L3-level RTM) if it exists.
3. Read all `.specify/specs/*/trace.md` files linked to this initiative.
4. Read `initiatives/$ARGUMENTS/ops/prr-checklist.md`.
5. Read `initiatives/$ARGUMENTS/ops/slo.yaml`.

6. **Compute RTM Coverage:**
   For each REQ-ID count how many trace dimensions are filled (ADR, Contract, Schema, Tests, SLO):
   ```
   REQ-AUTH-001  ████████░░  80%  (4/5 — missing SLO)
   REQ-AUTH-004  ██████████  100% (5/5)
   REQ-AUTH-002  ██████░░░░  60%  (3/5 — missing ADR, Schema)
   ```
   Overall coverage = (filled cells / total possible cells) × 100%

7. **Classify REQ-IDs by status:**
   - ✅ DONE: status=`verified` AND ≥1 trace link
   - 🟡 IN PROGRESS: status=`implemented` but missing trace links
   - ❌ OPEN: status=`draft`|`proposed`|`approved` — not yet implemented
   - 🔴 GAP: any status, but 0 trace links (blocker for release)

8. **PRR Checklist Status:**
   Parse `ops/prr-checklist.md` and classify each item:
   - ✅ DONE: `[x]`
   - ❌ OPEN: `[ ]`
   - 🔴 BLOCKING: items marked as MUST that are still `[ ]`

9. **SLO Readiness:**
   Check `ops/slo.yaml` — confirm SLO exists for every `nfr` requirement with `trace.slo`.

10. Write report to `evidence/$ARGUMENTS-evidence-report.md`:
    ```markdown
    # Evidence Report: $ARGUMENTS
    Generated: <YYYY-MM-DD>
    Profile: <minimal|standard|extended>

    ## RTM Coverage
    Overall: XX% (<N> of <M> REQ-IDs fully traced)
    [coverage table per REQ-ID]

    ## PRR Status
    DONE: N / OPEN: M / BLOCKING: K
    [checklist summary]

    ## SLO Coverage
    [SLO per nfr requirement]

    ## Gaps (Blockers)
    [list of 🔴 items]

    ## Recommendation
    READY FOR RELEASE / NOT READY — <reason>
    ```

11. Print the report summary to the user and state:
    - `READY FOR RELEASE` if: coverage ≥ 80%, zero 🔴 GAPs, zero 🔴 PRR blockers
    - `NOT READY` otherwise — list specific blockers

## Rules
- Do NOT declare `READY FOR RELEASE` if any MUST PRR item is unchecked
- Do NOT fabricate coverage numbers — compute from actual file contents
- For Minimal profile: skip SLO and PRR sections (not required)
- Evidence report is append-only — create a new file with date stamp, never overwrite

---
description: Visualize requirement traceability as a Mermaid diagram (REQ → ADR → Contract → Test → SLO)
argument-hint: <INIT-YYYY-NNN-slug> (e.g., INIT-2026-042-export-data)
---

You are generating a traceability visualization for initiative `$ARGUMENTS`.

## Your job

1. Read `initiatives/$ARGUMENTS/requirements.yml` — collect all REQ-IDs with their `trace:` blocks.
2. Read `initiatives/$ARGUMENTS/requirements.yml` metadata to determine the profile.
3. Optionally read `.specify/specs/*/trace.md` files to collect L4 trace data that references REQ-IDs from this initiative.
4. Optionally read `initiatives/$ARGUMENTS/trace.md` (if exists) for L3 trace data.

5. **Build a Mermaid flowchart** (`flowchart LR`) with these elements:

   **Subgraphs:**
   - `REQ` — one node per REQ-ID, labeled with `REQ-ID\nPriority Type`
   - `ADR` — one node per unique ADR reference found in traces
   - `Contract` — one node per unique contract path (openapi.yaml#path, asyncapi.yaml#channel)
   - `Test` — one node per unique test file reference
   - `SLO` — one node per unique SLO reference (for NFR requirements only)

   **Edges:**
   - `REQ-ID -->|adr| ADR-node` for each ADR in trace
   - `REQ-ID -->|contract| Contract-node` for each contract path
   - `REQ-ID -->|test| Test-node` for each test file
   - `REQ-ID -->|slo| SLO-node` for each SLO reference
   - `REQ-ID -->|component| Component-node` for each component path

   **Node coloring (coverage status):**
   - **Green** (`fill:#4CAF50,color:#fff`): REQ-ID has at least 1 test link AND at least 1 contract or component link
   - **Yellow** (`fill:#FFC107,color:#000`): REQ-ID has some trace links but incomplete coverage
   - **Red** (`fill:#f44336,color:#fff`): REQ-ID has NO trace links at all (orphan)

6. **Write the diagram** to `initiatives/$ARGUMENTS/trace-viz.md`:

   ```markdown
   # Traceability Visualization: $ARGUMENTS

   Generated: {today's date}
   Profile: {profile from metadata}

   ## Coverage Summary

   | Status | Count | REQ-IDs |
   |--------|------:|---------|
   | 🟢 Covered | N | REQ-XXX-001, ... |
   | 🟡 Partial  | N | REQ-XXX-002, ... |
   | 🔴 Orphan   | N | REQ-XXX-003, ... |

   **Coverage: M/N REQ-IDs fully traced ({percent}%)**

   ## Diagram

   ```mermaid
   flowchart LR
     ...
   ```

   ## Gaps

   List each orphan/partial REQ-ID with what's missing:
   - REQ-XXX-003: missing test, missing contract
   ```

7. **Print summary** to the user:
   ```
   📊 Traceability Visualization: $ARGUMENTS

   Total REQ-IDs: N
   🟢 Covered:    M (test + contract/component)
   🟡 Partial:    K (some links)
   🔴 Orphans:    J (no links)

   Coverage: {percent}%
   Written to: initiatives/$ARGUMENTS/trace-viz.md
   ```

## Profile-aware coverage rules

- **Minimal**: Trace links are optional. Show the diagram but don't flag orphans as blockers.
  Report: "Profile is Minimal — trace links are recommended but not required."
- **Standard+**: Every REQ-ID SHOULD have at least 1 trace link. Orphans are blockers for DoD.
- **Enterprise**: Additionally check for subsystem classification links.

## Rules

- Do NOT modify requirements.yml or trace.md — this command is read-only + generates trace-viz.md
- If requirements.yml has zero requirements, report "No requirements found" and exit
- Node IDs in Mermaid must be sanitized (replace `-` with `_` in IDs to avoid Mermaid parse errors)
- Keep the Mermaid diagram under 50 nodes total — if more, group by REQ prefix (subgraph per scope)
- If a trace link points to a file that doesn't exist on disk, mark the edge with `:::dashed` style

## Session Update

Execute session middleware per `.specify/session/protocol.md`.
**INIT-ID:** from $ARGUMENTS or context | **Type:** utility | **Next:** _(preserve current)_
